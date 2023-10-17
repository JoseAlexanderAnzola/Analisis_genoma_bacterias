import os
import csv

# Define las rutas de los archivos de entrada
input_files = ["Ralstonia_pseudosolanacearum.txt", "Xanthomonas_citri.txt", "Citrobacter_rodentium.txt"]

# Definir la ruta de la carpeta para guardar los archivos
output_folder = "Carpeta_entrega4"

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

for input_file in input_files:
    # Definir la ruta del archivo de salida en la carpeta específica añadiendo "_filtered.txt"
    # al nombre del archivo de entrada.
    output_file = os.path.join(output_folder, input_file.replace('.txt', '_filtered.txt'))

    # Inicializar variables para almacenar locus_tag y secuencias
    locus_tag = None
    sequences = {}

    # Leer los datos del archivo de entrada
    with open(input_file, 'r') as file:
        for line in file:
            if line.startswith(">"):
                # Comprueba si la descripción contiene [locus_tag=]
                if "[locus_tag=" in line:
                    locus_tag = line.split("[locus_tag=")[1].split("]")[0]
                    sequences[locus_tag] = ""
            else:
                # Añadir la secuencia si se encuentra un locus_tag
                if locus_tag is not None:
                    sequences[locus_tag] += line.strip()

    # Escribir las secuencias extraídas en el archivo de salida en la carpeta especificada.
    with open(output_file, 'w') as outfile:
        for locus_tag, sequence in sequences.items():
            outfile.write(f">{locus_tag}\n")
            outfile.write(sequence + "\n")

    print(f"Sequences from {input_file} have been saved to {output_file}")

    # Calcular la longitud y el contenido de GC de cada locus_tag
    locus_tags = []
    lengths = []
    gc_contents = []

    for locus_tag, sequence in sequences.items():
        length = len(sequence)
        # Calcular el contenido GC en porcentaje
        gc_content = (sequence.count("G") + sequence.count("C")) / length * 100
        locus_tags.append(locus_tag)
        lengths.append(length)
        gc_contents.append(gc_content)

    # Redondea los valores GC (%) a dos decimales
    rounded_gc_contents = [round(GC, 2) for GC in gc_contents]

    # Defina la ruta del archivo para guardar las estadísticas en la carpeta especificada
    statistics_file = os.path.join(output_folder,
                                   input_file.replace('.txt', '_statistics.tsv'))

    # Escribir los resultados en un archivo CSV en la carpeta especificada.
    with open(statistics_file, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")  # Set the delimiter to "\t"
        writer.writerow(["Locus_Tag", "Length", "GC (%)"])
        writer.writerows(zip(locus_tags, lengths, rounded_gc_contents))

    print(f"Statistics for {input_file} have been saved to {statistics_file}")






