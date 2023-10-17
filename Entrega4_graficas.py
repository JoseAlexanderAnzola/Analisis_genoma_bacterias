import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from adjustText import adjust_text  # Import adjust_text

# Lista de nombres de archivos (sustitúyalos por sus nombres reales)
file_names = ['Ralstonia_pseudosolanacearum_statistics.tsv',
              'Xanthomonas_citri_statistics.tsv',
              'Citrobacter_rodentium_statistics.tsv']

# Recorrer cada archivo
for file_name in file_names:
    # Leer los datos del archivo actual
    df = pd.read_csv(file_name, sep="\t")

    # Calcular los cuartiles y el IQR
    q1 = np.percentile(df['GC (%)'], 25)
    q3 = np.percentile(df['GC (%)'], 75)
    iqr = q3 - q1

    # Calcular los límites inferior y superior de los valores atípicos.
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Crear una nueva columna 'Color' para indicar el color de los puntos
    df['Color'] = 'LightGray'  # Use a light gray color
    df.loc[(df['GC (%)'] < lower_bound) | (df['GC (%)'] > upper_bound), 'Color'] = 'Red'

    # Create a scatterplot using sns.scatterplot with a custom palette
    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed

    # Definir una paleta personalizada
    custom_palette = {'Red': 'red', 'LightGray': 'lightgray'}

    # Diagrama de dispersión para puntos dentro y fuera de los límites
    scatter = sns.scatterplot(data=df,
                              x="GC (%)",
                              y="Length",
                              hue="Color",
                              palette=custom_palette)

    # Añadir líneas para los límites inferior y superior con etiquetas de leyenda personalizadas.
    plt.axvline(x=lower_bound, color="black", linestyle="--", label="Lower Bound")
    plt.axvline(x=upper_bound, color="black", linestyle="-", label="Upper Bound")

    # Personalizar el gráfico
    plt.xlabel("GC (%)")
    plt.ylabel("Length (bp)")
    #plt.yscale("log")
    plt.xlim(0, 20000)
    plt.xlim(0, 100)

    # Establecer las etiquetas de leyenda personalizadas
    custom_legend_labels = {
        'Red': 'Outliers',
        'LightGray': 'Inliers',
        'Lower Bound': 'Lower Bound',
        'Upper Bound': 'Upper Bound'
    }

    # Obtener la leyenda actual y actualizar las etiquetas
    legend = plt.legend()
    for label in legend.get_texts():
        label.set_text(custom_legend_labels[label.get_text()])

    # Definir el nombre del archivo de salida para el gráfico
    plot_output_file = file_name.replace('_statistics.tsv', '.jpg')

    # Modifica el título para eliminar la extensión del archivo y las "estadísticas"
    species_name = os.path.splitext(os.path.basename(file_name))[0].replace('_statistics', '').replace('_', ' ')
    figure_title = f"Scatterplot {species_name}"

    # Establece el título modificado
    plt.title(figure_title, fontsize=12, fontstyle='italic')

    # Guardar los gráficas en archivo JPG
    plt.savefig(plot_output_file, format='jpg', dpi=600, bbox_inches='tight')

    # Mostrar el gráfico (opcional)
    plt.show()

    # Cierra la grafica actual para iniciar una nueva para el siguiente archivo
    plt.close()

    # Define los nombres de los archivos de salida para los valores atípicos inferiores y superiores
    outliers_output_file = file_name.replace('_statistics.tsv', '_outliers_lower.tsv')
    inliers_output_file = file_name.replace('_statistics.tsv', '_outliers_upper.tsv')

    # Extraer valores atípicos por debajo del limite inferior y superior
    outliers_lower = df[(df['GC (%)'] < lower_bound)]
    outliers_upper = df[(df['GC (%)'] > upper_bound)]

    # Guarda los valores atípicos inferiores y superiores, .tsv separados
    outliers_lower.to_csv(outliers_output_file, sep='\t', index=False)
    outliers_upper.to_csv(inliers_output_file, sep='\t', index=False)

    # Calcular el contenido medio global de GC
    overall_mean_gc = df["GC (%)"].mean()

    # Crear y guardar un histograma del contenido GC (%)
    histogram_output_file = file_name.replace('_statistics.tsv', '_histogram.jpg')
    plt.figure(figsize=(8, 6))
    sns.histplot(data=df,
                 x="GC (%)",
                 binwidth=1,
                 alpha=0.3,
                 color="MidnightBlue")
    sns.despine()

    # definir los limites en los ejes x y y
    plt.xlim(20, 80)
    plt.ylim(0, 600)

    # Nombres de los ejes
    plt.xlabel("GC (%)")
    plt.ylabel("Frequency")

    # automatizar el nombre de los histogramas con el nombre de archivo entrada
    plt.title(f"Histogram {species_name}")

    # trazar una linea que indica la media general para GC
    plt.axvline(overall_mean_gc,
                color="red", linestyle="--")

    # Mostrar la media global con dos decimales
    plt.text(x=45,
             y=550,s=f'Overall mean GC: {overall_mean_gc:.2f}')

    # modificar el nombre de las grafias, poner en cursiva
    plt.title(figure_title,
              fontsize=12,
              fontstyle='italic')

    # definir el formato de salida de las figuras y caracteristicas
    plt.savefig(histogram_output_file,
                format='jpg', dpi=600,
                bbox_inches='tight')

    # Mostrar el gráfico (opcional)
    plt.show()

    # Cierra la grafica actual para iniciar una nueva para el siguiente archivo
    plt.close()

