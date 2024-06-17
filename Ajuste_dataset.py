import pandas as pd
import os

# Leer el archivo CSV original
og_file='G:/Universidad/Trabajos, talleres, actividades, etc/Tendencias/Proyecto_Tendencias/Codigo_Tratamiento_Dataset/tendencias_dataset/ETL/OG_dataset/ebay_dataset.csv'

df = pd.read_csv(og_file)

# Eliminar las columnas no deseadas
delete_col=['notice','image_url']
df = df.drop(columns=delete_col)

# Filtrar los 20 datos con las mayores ventas
df['sold_quantity (+)'] = pd.to_numeric(df['sold_quantity (+)'], errors='coerce')
df_top_20 = df.nlargest(20, 'sold_quantity (+)')

# Crear la ruta de la carpeta de destino
output_folder_path = 'G:/Universidad/Trabajos, talleres, actividades, etc/Tendencias/Proyecto_Tendencias/Codigo_Tratamiento_Dataset/tendencias_dataset/ETL/Transformed_dataset'

# Guardar el nuevo DataFrame en un nuevo archivo CSV en la carpeta de destino
output_file_path = os.path.join(output_folder_path, 'Transformed_dataset_1.csv')
df_top_20.to_csv(output_file_path, index=False)

print(f"Archivo guardado con exito en: {output_file_path}")