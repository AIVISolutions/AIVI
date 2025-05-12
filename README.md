# AIVI - Cuestionario de Autoconocimiento en Liderazgo

AIVI es una aplicación interactiva que permite a los usuarios completar un cuestionario de autoconocimiento en liderazgo. Basada en un análisis de preferencias y comportamientos, la aplicación genera un reporte en formato PDF con recomendaciones personalizadas. La aplicación está disponible en dos idiomas: **Español** y **Inglés**.

## Descripción

Este proyecto está diseñado para ayudar a los individuos a identificar sus preferencias en el contexto del liderazgo y obtener recomendaciones basadas en sus respuestas. Utiliza **Streamlit** para la interfaz de usuario y **FPDF** para la generación de reportes en PDF.

## Requisitos

La aplicación requiere las siguientes dependencias:

- **Streamlit**: Framework para crear interfaces interactivas en Python.
- **Pandas**: Librería para manipulación de datos.
- **Matplotlib**: Para la creación de gráficos.
- **FPDF**: Para la creación de archivos PDF.
- **CSV**: Para manejar archivos de datos.

Para instalar las dependencias, ejecuta:

```bash
pip install -r requirements.txt

Archivos de entrada
La aplicación utiliza tres archivos CSV para sus datos:

Cuestionario.csv: Contiene las preguntas y opciones del cuestionario.

Preferencias.csv: Contiene las descripciones de cada preferencia para los usuarios.

acciones_por_filtro.csv: Proporciona las recomendaciones y acciones basadas en las respuestas de los usuarios.

Uso
Ejecuta la aplicación con el siguiente comando:

bash
streamlit run app_bi.py

La aplicación te pedirá que selecciones un idioma (Español o Inglés).

Completa las preguntas del cuestionario. Al finalizar, el sistema generará un reporte en PDF que podrás descargar.

Generación de Reportes
Una vez completado el cuestionario, la aplicación genera un reporte detallado en formato PDF. Este reporte incluye:

Preferencias de liderazgo.

Acciones recomendadas basadas en las respuestas.

Interpretación del perfil de liderazgo.

Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar la aplicación, puedes hacer un fork del proyecto, crear tu rama, hacer los cambios y realizar un pull request.

Licencia
Este proyecto está bajo la licencia MIT.
