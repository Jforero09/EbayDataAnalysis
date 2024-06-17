import pandas as pd
import os
import re 

# Leer el archivo CSV original
og_file_2='G:/Universidad/Trabajos, talleres, actividades, etc/Tendencias/Proyecto_Tendencias/Codigo_Tratamiento_Dataset/tendencias_dataset/ETL/OG_dataset/ebay_dataset_2.csv'

df = pd.read_csv(og_file_2,on_bad_lines='skip')

# Eliminar las columnas no deseadas
delete_col=['Uniq Id','Pageurl','Website','Num Of Reviews','Average Rating','Number Of Ratings','Model Num'
            ,'Sku','Upc','Monthly Price','Stock','Carrier','Color Category','Internal Memory','Screen Size',
            'Specifications','Five Star','Four Star','Three Star','Two Star','One Star','Discontinued',
            'Broken Link']

df = df.drop(columns=delete_col)

# Eliminar filas con 'NA' en la columna 'raiting de ventas'
df = df[df['Seller Rating'] != 'NA']

#Eliminar filas con valores vacíos en la columna 'raiting de ventas'
df = df[df['Seller Rating'].notna()]
df = df[df['Seller Rating'] != '']

# Utilizar una expresión regular para eliminar todo excepto números y puntos decimales
df['Seller Rating'] = df['Seller Rating'].apply(lambda x: re.sub(r'[^0-9.]', '', x))

# Convertir la columna 'seller rating' a numérico
df['Seller Rating'] = pd.to_numeric(df['Seller Rating'], errors='coerce')


#Filtrar seller rating mayor o igual al 80%
df = df[df['Seller Rating'] >= 90]


#  Filtrar los 180 datos con las mayor rating
df_top_180 = df.nlargest(180, 'Seller Rating')

print(df_top_180)

# Crear la ruta de la carpeta de destino
output_folder_path = 'G:/Universidad/Trabajos, talleres, actividades, etc/Tendencias/Proyecto_Tendencias/Codigo_Tratamiento_Dataset/tendencias_dataset/ETL/Transformed_dataset'

# Guardar el nuevo DataFrame en un nuevo archivo CSV en la carpeta de destino
output_file_path = os.path.join(output_folder_path, 'Transformed_dataset_2.csv')
df_top_180.to_csv(output_file_path, index=False)

print(f"Archivo guardado con exito en: {output_file_path}")