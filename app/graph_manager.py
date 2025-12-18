import pandas as pd
import plotly.express as px
import plotly.io as pio

def generate_pie_chart(df):
    df_counts = df.groupby('nota').size().reset_index(name='cantidad')
    df_counts['nota'] = df_counts['nota'].astype(str)
    fig = px.pie(df_counts, values='cantidad', names='nota', title='Distribución de Notas', hole=0.3)
    return pio.to_html(fig, full_html=False)

def generate_bar_chart(df):
    df_loc = df.groupby('localidad').size().reset_index(name='alumnos')
    fig = px.bar(df_loc, x='localidad', y='alumnos', title='Cantidad de Alumnos por Localidad')
    return pio.to_html(fig, full_html=False)

# --- NUEVOS GRÁFICOS ---

def generate_sorted_notes_chart(df):
    """Muestra todas las notas ordenadas de mayor a menor con el nombre del alumno."""
    # Ordenamos el DataFrame por nota de forma descendente
    df_sorted = df.sort_values(by='nota', ascending=False)
    
    # Creamos el gráfico indicando que 'nombre' aparezca en el hover (al poner el cursor)
    fig = px.bar(df_sorted, 
                 x='nombre', 
                 y='nota', 
                 title='Ranking de Notas (Mayor a Menor)',
                 color='nota',
                 hover_data=['nombre', 'localidad'], # Información extra al pasar el ratón
                 labels={'nombre': 'Alumno', 'nota': 'Calificación'})
    return pio.to_html(fig, full_html=False)

def generate_average_locality_chart(df):
    """Muestra el promedio de notas por cada localidad."""
    df_avg = df.groupby('localidad')['nota'].mean().reset_index()
    fig = px.bar(df_avg, 
                 x='localidad', 
                 y='nota', 
                 title='Nota Media por Localidad',
                 color_discrete_sequence=['#27ae60'])
    return pio.to_html(fig, full_html=False)