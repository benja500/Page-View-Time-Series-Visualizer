import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Cargar los datos y establecer el índice de la columna 'date'
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# 2. Limpiar los datos eliminando el top 2.5% y el bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    """
    Esta función genera un gráfico de líneas que muestra la cantidad de visualizaciones diarias 
    del foro de freeCodeCamp.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='tab:red')

    # Configurar el título y las etiquetas
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Guardar la imagen y retornarla
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    """
    Esta función genera un gráfico de barras que muestra el promedio de visualizaciones diarias
    por mes, agrupado por año.
    """
    # Preparar los datos para el gráfico de barras
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Asegurarse de que los meses están en orden cronológico
    df_bar['month'] = pd.Categorical(df_bar['month'], 
                                     categories=['January', 'February', 'March', 'April', 'May', 'June', 
                                                 'July', 'August', 'September', 'October', 'November', 'December'], 
                                     ordered=True)

    # Agrupar los datos por año y mes, y calcular el promedio de visitas diarias
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Crear gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(12, 7)).figure

    # Configurar el título, etiquetas y leyenda
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Guardar la imagen y retornarla
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    """
    Esta función genera dos gráficos de cajas:
    1. Gráfico de cajas por año (Year-wise Box Plot)
    2. Gráfico de cajas por mes (Month-wise Box Plot)
    """
    # Convertir explícitamente a float64 antes de pasar los datos a Seaborn
    df_box = df.copy()
    df_box['value'] = pd.to_numeric(df_box['value'], downcast='float')  # Convertir a float64
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.strftime('%b')

    # Crear gráficos de cajas
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico de cajas por año
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Gráfico de cajas por mes
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Guardar la figura y retornarla
    fig.savefig('box_plot.png')
    return fig
