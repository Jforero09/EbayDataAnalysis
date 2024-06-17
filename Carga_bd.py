import pymongo
import pandas as pd
import pymongo.mongo_client

#conexion con la base de datos
client=pymongo.MongoClient("mongodb://localhost:27017")

#lectura del dataset transformado
df=pd.read_csv('G:/Universidad/Trabajos, talleres, actividades, etc/Tendencias/Proyecto_Tendencias/Codigo_Tratamiento_Dataset/tendencias_dataset/ETL/Transformed_dataset/Transformed_dataset_2.csv')


#conversion de a Json del dataset
data=df.to_dict(orient='records')


#carga de dataset a la base de datos
db = client['EbayDataWareHouse']

db.DataSet_2.insert_many(data)

