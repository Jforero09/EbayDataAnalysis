import pandas as pd
import json
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot, GridBox, layout
from bokeh.models import ColumnDataSource,Label
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bokeh.transform import cumsum
from math import pi
from bokeh.palettes import Category20c , turbo
from bokeh.models.widgets import Div
from bokeh.layouts import column,row,Spacer


# Conexión a MongoDB Atlas
uri = "mongodb://localhost:27017"
client = MongoClient(uri, server_api=ServerApi('1'))

# Selección de la base de datos y colección
db = client['EbayDataWareHouse']
collection1 = db['DataSet_1']
collection2 = db['DataSet_2']

# Cargar datos desde MongoDB Atlas
data1 = list(collection1.find())
data2 = list(collection2.find())

# Convertir datos JSON a DataFrame de pandas
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Información general de los datasets
info1 = df1.describe(include='all').transpose()
info2 = df2.describe(include='all').transpose()



# Pregunta 1: Productos más vendidos por país
df1_country_sales = df1.groupby('shipping from')['sold_quantity (+)'].sum().reset_index()
source1 = ColumnDataSource(df1_country_sales)
p1 = figure(height=350, width=700,x_range=df1_country_sales['shipping from'], title="Productos más vendidos por país", toolbar_location=None, tools="")
p1.vbar(x='shipping from', top='sold_quantity (+)', width=0.9, source=source1)
p1.xgrid.grid_line_color = None
p1.y_range.start = 0


# Gráfico de torta para productos más vendidos por país
df1_country_sales['angle'] = df1_country_sales['sold_quantity (+)'] / df1_country_sales['sold_quantity (+)'].sum() * 2 * pi
df1_country_sales['color'] = Category20c[len(df1_country_sales)] if len(df1_country_sales) <= 20 else turbo(len(df1_country_sales))
p1_pie = figure(height=350, width=450, title="Distribución de Ventas por País", toolbar_location=None, tools="hover", tooltips="@shipping from: @sold_quantity (+)", x_range=(-0.5, 1.0))
p1_pie.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
             line_color="white", fill_color='color', legend_field='shipping from', source=ColumnDataSource(df1_country_sales))
p1_pie.axis.axis_label = None
p1_pie.axis.visible = False
p1_pie.grid.grid_line_color = None
p1_pie.legend.location = "top_right"

# Pregunta 2: Producto remanufacturado con mayor cantidad de ventas
df1_refurbished = df1[df1['comments'].str.contains('Refurbished', na=False)]
df1_refurbished_max = df1_refurbished.loc[df1_refurbished['sold_quantity (+)'].idxmax()]
p2 = figure(title="Producto remanufacturado con mayor cantidad de ventas", toolbar_location=None, tools="", width=550, height=750)
p2.scatter([1], [df1_refurbished_max['sold_quantity (+)']], size=10)
p2.xaxis.visible = False
p2.yaxis.axis_label = "Cantidad de ventas"
p2.y_range.start = 0
p2.add_layout(Label(x=1, y=df1_refurbished_max['sold_quantity (+)'], text=df1_refurbished_max['item_name'], text_font_size='10pt', text_align='left'))


# Gráfico de torta para producto remanufacturado

df1_refurbished_sales = df1_refurbished.groupby('item_name')['sold_quantity (+)'].sum().reset_index()
df1_refurbished_sales['angle'] = df1_refurbished_sales['sold_quantity (+)'] / df1_refurbished_sales['sold_quantity (+)'].sum() * 2 * pi
df1_refurbished_sales['color'] = Category20c[len(df1_refurbished_sales)] if len(df1_refurbished_sales) <= 20 else turbo(len(df1_refurbished_sales))
p2_pie = figure(height=850, width=650, title="Productos remanufacturados más vendidos", toolbar_location=None, tools="hover", tooltips="@item_name: @sold_quantity (+)", x_range=(-0.5, 1.0))
p2_pie.wedge(x=0.2, y=1, radius=0.5, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
             line_color="white", fill_color='color', legend_field='item_name', source=ColumnDataSource(df1_refurbished_sales))

p2_pie.axis.axis_label = None
p2_pie.axis.visible = False
p2_pie.grid.grid_line_color = None
p2_pie.legend.visible = True


# Pregunta 3: Marca con mayor cantidad de ventas (mostrando solo las 5 más relevantes)
df2_brand_sales = df2.groupby('Manufacturer')['Title'].count().reset_index().rename(columns={'Title': 'Number of Sales'})
df2_brand_sales = df2_brand_sales.nlargest(5, 'Number of Sales')  # Mostrar solo los 5 más relevantes
df2_brand_max = df2_brand_sales.loc[df2_brand_sales['Number of Sales'].idxmax()]
source3 = ColumnDataSource(df2_brand_sales)
p3 = figure(x_range=df2_brand_sales['Manufacturer'], title="Ventas por fabricante (Top 5)", toolbar_location=None, tools="", width=1900, height=600)
p3.vbar(x='Manufacturer', top='Number of Sales', width=0.5, source=source3)
p3.xgrid.grid_line_color = None
p3.y_range.start = 0
p3.y_range.end = 20
p3.yaxis.ticker = list(range(0, 21, 1))

# Gráfico de torta para marca con mayor cantidad de ventas
df2_brand_sales['angle'] = df2_brand_sales['Number of Sales'] / df2_brand_sales['Number of Sales'].sum() * 2 * pi
df2_brand_sales['color'] = Category20c[len(df2_brand_sales)] if len(df2_brand_sales) <= 20 else turbo(len(df2_brand_sales))
p3_pie = figure(height=750, width=600, title="Distribución de Ventas por Marca ", toolbar_location=None, tools="hover", tooltips="@Manufacturer: @Number of Sales", x_range=(-0.5, 1.0))
p3_pie.wedge(x=0.2, y=1, radius=0.5, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
             line_color="white", fill_color='color', legend_field='Manufacturer', source=ColumnDataSource(df2_brand_sales))
p3_pie.axis.axis_label = None
p3_pie.axis.visible = False
p3_pie.grid.grid_line_color = None
p3_pie.legend.location = "top_right"

# Agregar títulos generales a cada sección
title1 = Div(text="<h2>Ventas por País</h2>")
title2 = Div(text="<h2>Productos remanufacturados</h2>")
title3 = Div(text="<h2>Ventas de productos tecnologicos por Marca</h2>")


# Layout
spacer = Spacer(width=50)

section1 = column(title1, row(p1,spacer ,p1_pie,))
section2 = column(title2, row(p2,spacer ,p2_pie,))
section3 = column(title3, row(p3))

custom_layout = column(section1, section2, section3, Spacer(height=20),p3_pie)

output_file("dashboard.html")
show(custom_layout)

