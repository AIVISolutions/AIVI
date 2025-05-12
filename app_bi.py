# archivo: app.py
import matplotlib.pyplot as plt
import tempfile
import streamlit as st
import pandas as pd
from fpdf import FPDF
import csv

class PDFSafe(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def multi_cell_seguro(self, w, h, txt):
        if txt is None:
            return
        texto = str(txt).strip()
        if len(texto) > 1:
            try:
                texto = texto.encode('latin-1', errors='ignore').decode('latin-1')
                self.multi_cell(w, h, texto)
            except:
                pass
            
st.set_page_config(page_title="Cuestionario de Liderazgo Bilingüe", layout="centered")

cuestionario = pd.read_csv('Cuestionario.csv')
df_explicaciones = pd.read_csv('Preferencias.csv')
df_acciones = pd.read_csv("acciones_por_filtro.csv")

def obtener_descripcion(seccion, preferencia, idioma):
    if idioma == "Español":
        fila = df_explicaciones[
            (df_explicaciones["Sección (ES)"] == seccion) &
            (df_explicaciones["Preferencia (ES)"] == traduccion_preferencias_es.get(preferencia, preferencia))
        ]
        return fila.iloc[0]["Descripción Preferencia (ES)"] if not fila.empty else ""
    else:
        fila = df_explicaciones[
            (df_explicaciones["Sección (EN)"] == seccion) &
            (df_explicaciones["Preferencia (EN)"] == preferencia)
        ]
        return fila.iloc[0]["Descripción Preferencia (EN)"] if not fila.empty else ""


opciones_por_seccion = {
    "EN": {
        "Your Preferred Senses": ["HEARING", "FEELING", "VISUAL"],
        "Importance to Me (Focus)": ["PEOPLE", "PLACES", "ACTIVITIES", "KNOWLEDGE", "THINGS"],
        "My Processing Style": ["BIG", "SMALL"],
        "Source of Direction": ["AWAY FROM", "TOWARD"],
        "Source of Motivation": ["SELF", "OTHER"],
        "Preferences": ["DIFFERENCES", "SIMILARITIES"],
        "Preferred State": ["ASSOCIATED", "DISASSOCIATED"],
        "Time Reference": ["PAST", "PRESENT", "FUTURE"]
    },
    "ES": {
        "Tus Sentidos Preferidos": ["HEARING", "FEELING", "VISUAL"],
        "Lo que es Importante para Mí": ["PEOPLE", "PLACES", "ACTIVITIES", "KNOWLEDGE", "THINGS"],
        "Mi Estilo de Procesamiento": ["BIG", "SMALL"],
        "Fuente de Dirección": ["AWAY FROM", "TOWARD"],
        "Fuente de Motivación": ["SELF", "OTHER"],
        "Preferencias": ["DIFFERENCES", "SIMILARITIES"],
        "Estado Preferido": ["ASSOCIATED", "DISASSOCIATED"],
        "Referencia Temporal": ["PAST", "PRESENT", "FUTURE"]
    }
}

traduccion_preferencias_es = {
    "HEARING": "AUDITIVO",
    "FEELING": "KINESTÉSICO",
    "VISUAL": "VISUAL",
    "PEOPLE": "PERSONAS",
    "PLACES": "LUGARES",
    "ACTIVITIES": "ACTIVIDADES",
    "KNOWLEDGE": "CONOCIMIENTO",
    "THINGS": "OBJETOS",
    "BIG": "GLOBAL",
    "SMALL": "DETALLADO",
    "AWAY FROM": "ALEJADO DE",
    "TOWARD": "ORIENTADO A",
    "SELF": "YO",
    "OTHER": "OTROS",
    "DIFFERENCES": "DIFERENCIAS",
    "SIMILARITIES": "SIMILITUDES",
    "ASSOCIATED": "ASOCIADO",
    "DISASSOCIATED": "DESASOCIADO",
    "PAST": "PASADO",
    "PRESENT": "PRESENTE",
    "FUTURE": "FUTURO"
}

st.title("Cuestionario de Autoconocimiento en Liderazgo")
idioma = st.radio("Seleccione su idioma / Select your language:", ("Español", "English"), index=0)
st.markdown("---")
nombre = st.text_input("Por favor ingrese su nombre (opcional):")
st.markdown("---")

def mostrar_preguntas(df, idioma):
    respuestas = {}
    col_seccion = 'Sección (ES)' if idioma == "Español" else 'Sección (EN)'
    col_pregunta = 'Pregunta (ES)' if idioma == "Español" else 'Pregunta (EN)'
    opciones_cols = [f"Opción {letra} ({'ES' if idioma == 'Español' else 'EN'})" for letra in ['A', 'B', 'C', 'D', 'E']]

    secciones_ordenadas = df[col_seccion].dropna().unique().tolist()
    
    for seccion in secciones_ordenadas:
        st.subheader(seccion)
        grupo = df[df[col_seccion] == seccion]

        for _, row in grupo.iterrows():
            pregunta = row[col_pregunta]
            letras = []
            for letra, col in zip(['A', 'B', 'C', 'D', 'E'], opciones_cols):
                valor = row.get(col)
                if pd.notna(valor) and valor.strip() != '':
                    letras.append(letra)

            seleccionadas = st.multiselect(
                label=pregunta,
                options=letras,
                format_func=lambda x: f"{x}: {row.get(f'Opción {x} ({'ES' if idioma == 'Español' else 'EN'})')}",
                key=row['key_unico']
            )
            respuestas.setdefault(seccion.strip(), []).extend(seleccionadas)

    return respuestas, secciones_ordenadas

respuestas_por_seccion, secciones_ordenadas = mostrar_preguntas(cuestionario, idioma)

# ✅ Inicializar variable global aquí
acciones_por_zona = {"PREDOMINANT": [], "SUPPORTING": [], "DEVELOPMENTAL": []}

def obtener_accion_recomendada(preferencia, zona, idioma):
    if idioma == "Español":
        fila = df_acciones[
            (df_acciones["Preferencia (ES)"] == preferencia) &
            (df_acciones["Zona"] == zona)
        ]
        return fila.iloc[0]["Acción recomendada (ES)"] if not fila.empty else ""
    else:
        fila = df_acciones[
            (df_acciones["Preferencia (EN)"] == preferencia) &
            (df_acciones["Zona"] == zona)
        ]
        return fila.iloc[0]["Acción recomendada (EN)"] if not fila.empty else ""

if st.button("Generar Reporte en PDF"):
    col_seccion = 'Sección (ES)' if idioma == 'Español' else 'Sección (EN)'
    idioma_codigo = "ES" if idioma == "Español" else "EN"

    pdf = PDFSafe()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Visualizacion titulo
    titulo = f"Resultados de {nombre}" if nombre else "Resultados del Diagnóstico"
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)  # Azul suave
    pdf.cell(0, 10, titulo, ln=True, align='C')
    pdf.ln(8)
    pdf.set_text_color(0, 0, 0)  # Volver a negro
    
    #Inicializa el contador global antes del loop
    conteo_global = {}

    for seccion in secciones_ordenadas:
        seccion_limpia = seccion.strip()
        respuestas = respuestas_por_seccion.get(seccion_limpia, [])
        valores_clave = opciones_por_seccion.get(idioma_codigo, {}).get(seccion_limpia)

        if not valores_clave:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"Filtro: {seccion_limpia}", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 8, "Filtro no reconocido para análisis.", ln=True)
            pdf.ln(5)
            continue

        conteo = {clave: 0 for clave in valores_clave}

        for letra in respuestas:
            index = ord(letra.upper()) - ord('A')
            if 0 <= index < len(valores_clave):
                clave = valores_clave[index]
                conteo[clave] += 1

        # ✅ Ahora sí: ya hay datos en `conteo`, puedes sumarlos al global
        for clave, cantidad in conteo.items():
                conteo_global[clave] = conteo_global.get(clave, 0) + cantidad

        # seccion filtro         
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(51, 51, 102)
        pdf.cell(0, 10, f" {seccion_limpia}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)


        for clave, cantidad in conteo.items():
            etiqueta = traduccion_preferencias_es[clave] if idioma == "Español" else clave
            pdf.cell(0, 8, f"{etiqueta}: {cantidad}", ln=True)

        if conteo:
            max_valor = max(conteo.values())
            dominantes = [k for k, v in conteo.items() if v == max_valor and v > 0]
            pdf.set_font("Arial", 'I', 11)
            if dominantes:
                etiquetas = [traduccion_preferencias_es[d] if idioma == "Español" else d for d in dominantes]
                pdf.cell(0, 8, f"Dominante: {', '.join(etiquetas)}", ln=True)

                for dominante in dominantes:
                    
                    indice = list(conteo.keys()).index(dominante)
                    zona = ""
                    if len(conteo) >= 3:
                        if indice < len(conteo) // 3:
                            zona = "PREDOMINANT"
                        elif indice < 2 * len(conteo) // 3:
                            zona = "SUPPORTING"
                        else:
                            zona = "DEVELOPMENTAL"

                    preferencia_es = traduccion_preferencias_es[dominante] if idioma == "Español" else dominante
                    accion = obtener_accion_recomendada(preferencia_es, zona, idioma)

                    if accion:
                        acciones_por_zona[zona].append((preferencia_es, accion))

                    fila = df_explicaciones[
                        (df_explicaciones["Sección (ES)"] == seccion_limpia) &
                        (df_explicaciones["Preferencia (ES)"] == traduccion_preferencias_es[dominante])
                    ]
                    if not fila.empty:
                        descripcion = fila.iloc[0]["Descripción Preferencia (ES)"]
                        pdf.set_font("Arial", size=10)
                        pdf.multi_cell_seguro(0, 6, descripcion)
            else:
                pdf.cell(0, 8, "Sin respuestas seleccionadas.", ln=True)
        else:
            pdf.set_font("Arial", 'I', 11)
            pdf.cell(0, 8, "Sin respuestas seleccionadas.", ln=True)

        pdf.ln(5)

    nombre_archivo = f"Diagnostico_{nombre or 'Participante'}_{idioma_codigo}.pdf"
    
    # Clasificación única por grupos con empates respetados
    acciones_por_zona = {"PREDOMINANT": [], "SUPPORTING": [], "DEVELOPMENTAL": []}
    zona_por_clave = {}

    from collections import defaultdict
    positivas = [(k, v) for k, v in conteo_global.items() if v > 0]
    ceros = [(k, v) for k, v in conteo_global.items() if v == 0]

    grupos = defaultdict(list)
    for clave, valor in positivas:
        grupos[valor].append(clave)

    valores_ordenados = sorted(grupos.keys(), reverse=True)
    total_items = sum(len(grupos[v]) for v in valores_ordenados)
    tercio = total_items // 3

    cuenta = 0
    for valor in valores_ordenados:
        claves = grupos[valor]
        if cuenta < tercio:
            zona = "PREDOMINANT"
        elif cuenta < 2 * tercio:
            zona = "SUPPORTING"
        else:
            zona = "DEVELOPMENTAL"
        for clave in claves:
            zona_por_clave[clave] = zona
            preferencia_es = traduccion_preferencias_es.get(clave, clave) if idioma == "Español" else clave
            accion = obtener_accion_recomendada(preferencia_es, zona, idioma)
            if accion:
                acciones_por_zona[zona].append((preferencia_es, accion))
        cuenta += len(claves)

    for clave, _ in ceros:
        zona_por_clave[clave] = "DEVELOPMENTAL"
        preferencia_es = traduccion_preferencias_es.get(clave, clave) if idioma == "Español" else clave
        accion = obtener_accion_recomendada(preferencia_es, "DEVELOPMENTAL", idioma)
        if accion:
            acciones_por_zona["DEVELOPMENTAL"].append((preferencia_es, accion))

# Crear el gráfico a partir del conteo global
    if conteo_global:
        etiquetas = []
        valores = []

        for clave, cantidad in sorted(conteo_global.items(), key=lambda x: -x[1]):
            etiqueta = traduccion_preferencias_es[clave] if idioma == "Español" else clave
            etiquetas.append(etiqueta)
            valores.append(cantidad)
        
        zona_por_clave = {}
        for zona, items in acciones_por_zona.items():
            for preferencia, _ in items:
                clave = next((k for k, v in traduccion_preferencias_es.items() if v == preferencia), preferencia) if idioma == "Español" else preferencia
                zona_por_clave[clave] = zona
                
        # Crear el gráfico con matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        etiquetas_ordenadas = [x for _, x in sorted(zip(valores, etiquetas), reverse=True)]
        valores_ordenados = sorted(valores, reverse=True)
        bars = ax.barh(etiquetas_ordenadas, valores_ordenados)

        total = len(valores_ordenados)
        zona1 = total // 3
        zona2 = 2 * total // 3

        for i, bar in enumerate(bars):
            etiqueta = etiquetas_ordenadas[i]
            clave = next((k for k, v in traduccion_preferencias_es.items() if v == etiqueta), etiqueta) if idioma == "Español" else etiqueta

            zona = zona_por_clave.get(clave, "DEVELOPMENTAL")

            if zona == "PREDOMINANT":
                bar.set_color('#4CAF50')  # Verde
            elif zona == "SUPPORTING":
                bar.set_color('#FFC107')  # Amarillo
            else:
                bar.set_color('#F44336')  # Rojo  # Rojo

        # Etiquetas de zona
        ax.text(0.95, zona1 - 0.5, 'PREDOMINANT', transform=ax.get_yaxis_transform(), fontsize=9, color='green', ha='right')
        ax.text(0.95, zona2 - 0.5, 'SUPPORTING', transform=ax.get_yaxis_transform(), fontsize=9, color='orange', ha='right')
        ax.text(0.95, total - 0.5, 'DEVELOPMENTAL', transform=ax.get_yaxis_transform(), fontsize=9, color='red', ha='right')

        ax.set_xlabel('Total de respuestas')
        ax.set_title('Resumen General de Preferencias')
        plt.tight_layout()

        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            plt.savefig(tmpfile.name, dpi=200)
            ruta_img = tmpfile.name
            plt.close()

        # Insertar imagen en PDF
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Resumen General de Preferencias", ln=True, align='C')
        pdf.image(ruta_img, x=10, y=None, w=180)
        
        # Recalcular zona por preferencia usando conteo_global
        total = len(conteo_global)
        ordenadas = sorted(conteo_global.items(), key=lambda x: -x[1])
        zona1 = total // 3
        zona2 = 2 * total // 3

        acciones_por_zona = {"PREDOMINANT": [], "SUPPORTING": [], "DEVELOPMENTAL": []}

        for i, (clave, _) in enumerate(ordenadas):
            if i < zona1:
                zona = "PREDOMINANT"
            elif i < zona2:
                zona = "SUPPORTING"
            else:
                zona = "DEVELOPMENTAL"

            preferencia_es = traduccion_preferencias_es[clave] if idioma == "Español" else clave
            accion = obtener_accion_recomendada(preferencia_es, zona, idioma)

            if accion:
                acciones_por_zona[zona].append((preferencia_es, accion))

        
    # Bloque para agregar interpretación por zona (final del PDF)   

    import pandas as pd

    def limpiar_texto(texto):
        return str(texto).encode('latin-1', errors='ignore').decode('latin-1')

    def linea_valida(texto):
        try:
            texto.encode('latin-1')
            return len(texto.strip()) > 1
        except:
            return False
    # Recalcular zona por preferencia usando conteo_global
    acciones_por_zona = {"PREDOMINANT": [], "SUPPORTING": [], "DEVELOPMENTAL": []}

    # Separar las preferencias con valor > 0 y las que tienen 0
    positivas = [(k, v) for k, v in conteo_global.items() if v > 0]
    ceros = [(k, v) for k, v in conteo_global.items() if v == 0]

    # Ordenar las positivas y dividir en tercios
    ordenadas = sorted(positivas, key=lambda x: -x[1])
    total = len(ordenadas)
    zona1 = total // 3
    zona2 = 2 * total // 3

    for i, (clave, _) in enumerate(ordenadas):
        if i < zona1:
            zona = "PREDOMINANT"
        elif i < zona2:
            zona = "SUPPORTING"
        else:
            zona = "DEVELOPMENTAL"

        preferencia_es = traduccion_preferencias_es[clave] if idioma == "Español" else clave
        accion = obtener_accion_recomendada(preferencia_es, zona, idioma)
        if accion:
            acciones_por_zona[zona].append((preferencia_es, accion))

    # Agregar las preferencias con valor 0 como DEVELOPMENTAL
    for clave, _ in ceros:
        preferencia_es = traduccion_preferencias_es[clave] if idioma == "Español" else clave
        accion = obtener_accion_recomendada(preferencia_es, "DEVELOPMENTAL", idioma)
        if accion:
            acciones_por_zona["DEVELOPMENTAL"].append((preferencia_es, accion))

    
    
    def agregar_acciones_por_zona(pdf, idioma, acciones_por_zona):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        titulo = "Qué hacer según tus preferencias" if idioma == "Español" else "What to do based on your preferences"
        pdf.cell(0, 10, titulo, ln=True, align='C')
        pdf.ln(5)

        zonas_orden = ["PREDOMINANT", "SUPPORTING", "DEVELOPMENTAL"]
        colores = {
            "PREDOMINANT": (0, 102, 0),
            "SUPPORTING": (255, 165, 0),
            "DEVELOPMENTAL": (200, 0, 0)
        }

        for zona in zonas_orden:
            acciones = acciones_por_zona.get(zona, [])
            if not acciones:
                continue
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(*colores[zona])
            pdf.cell(0, 10, zona, ln=True)
            pdf.set_text_color(0, 0, 0)

            for preferencia, accion in acciones:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, preferencia, ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell_seguro(0, 6, accion)
                pdf.ln(2)    
    
    def agregar_interpretacion_por_zona_bilingue(pdf, idioma):
        try:
            df_zonas = pd.read_csv("zonas_info_bilingue_limpio.csv")

            titulo = "Interpretación por Zona" if idioma == "Español" else "Zone-Based Interpretation"
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, titulo, ln=True, align='C')
            pdf.ln(5)

            for _, row in df_zonas.iterrows():
                zona = row["Zona"]
                t_titulo = row["Título (ES)"] if idioma == "Español" else row["Título (EN)"]
                t_desc = row["Descripción (ES)"] if idioma == "Español" else row["Descripción (EN)"]
                t_que = row["Qué hacer (ES)"] if idioma == "Español" else row["Qué hacer (EN)"]
                t_preg = row["Preguntas útiles (ES)"] if idioma == "Español" else row["Preguntas útiles (EN)"]

                # Título zona
                pdf.set_font("Arial", 'B', 14)
                color = (0, 102, 0) if zona == "PREDOMINANT" else (255, 165, 0) if zona == "SUPPORTING" else (200, 0, 0)
                pdf.set_text_color(*color)
                pdf.cell(0, 10, str(t_titulo), ln=True)
                pdf.set_text_color(0, 0, 0)

                # Descripción
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, "DESCRIPCIÓN:" if idioma == "Español" else "DESCRIPTION:", ln=True)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell_seguro(0, 6, t_desc)
                pdf.ln(1)

                # Recomendaciones
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, "RECOMENDACIONES:" if idioma == "Español" else "RECOMMENDATIONS:", ln=True)
                pdf.set_font("Arial", '', 11)
                for line in str(t_que).split('\n'):
                    pdf.multi_cell_seguro(0, 6, "* " + line.strip())
                pdf.ln(1)

                # Preguntas útiles
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, "PREGUNTAS ÚTILES:" if idioma == "Español" else "USEFUL QUESTIONS:", ln=True)
                pdf.set_font("Arial", '', 11)
                for line in str(t_preg).split('\n'):
                    pdf.multi_cell_seguro(0, 6, "- " + line.strip())
                pdf.ln(5)

        except Exception as e:
            pdf.set_font("Arial", 'I', 10)
            pdf.set_text_color(200, 0, 0)
            mensaje = "Error al cargar interpretación por zona" if idioma == "Español" else "Error loading zone interpretation"
            pdf.cell(0, 10, f"{mensaje}: {e}", ln=True)
            pdf.set_text_color(0, 0, 0)
    
    agregar_interpretacion_por_zona_bilingue(pdf, idioma)
    agregar_acciones_por_zona(pdf, idioma, acciones_por_zona)

    pdf.output(nombre_archivo)

    st.success(f"¡Reporte generado exitosamente! Archivo: {nombre_archivo}")
    with open(nombre_archivo, "rb") as file:
        st.download_button(
            label="Descargar Reporte PDF",
            data=file,
            file_name=nombre_archivo,
            mime="application/pdf"
        )
