# Importamos las librerías necesarias
import tkinter as tk
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Definimos una función que contenga el procesamiento que hicimos en el paso anterior
def process_info(file, path, path_export):

    # Importamos la información
    data = pd.read_csv(path + file)
    
    data = data[['Order ID','Order Date','Category','Sales']]
    data.columns = ['_'.join(x.split()).lower() for x in data.columns]
    data.order_date = pd.to_datetime(data.order_date, format = '%d/%m/%Y')
    data.category = data.category.astype('category')
    data['year'] = pd.DatetimeIndex(data['order_date']).year
    data['month'] = pd.DatetimeIndex(data['order_date']).month
    
    # Información para el csv con las ventas semanales del último año
    weekly_data = data[['order_date','sales','year']]
    weekly_data = weekly_data.loc[weekly_data.year == max(weekly_data.year)]
    weekly_data.set_index('order_date',inplace = True)
    weekly_data.sort_index(inplace=True)
    weekly_data = weekly_data.resample('W').sum()
    weekly_data.reset_index(inplace = True)
    weekly_data.columns = ['week','sales','year']
    weekly_data.to_csv(path_export + 'weekly_sales.csv',index = False)
    
    # Información para exportar imagen con ventas por categoría último mes
    chart_data = data[['order_date','sales','category','year','month']]
    chart_data = chart_data.loc[(chart_data.year == max(chart_data.year)) & (chart_data.month == max(chart_data.month))]
    ax = sns.barplot(x="category", y="sales", data=chart_data, ci = 0)
    ax.bar_label(ax.containers[0],padding = 1)
    plt.savefig(path_export + 'sales_per_category_last_week.png')


root=tk.Tk()
root.title("Sales Data")
root.geometry("250x100")

path_var = tk.StringVar() ## path hacia el archivo de datos
pathe_var = tk.StringVar()## path para la exportación de los resultados
  
# Declaramos la función que toma como inputs el path donde están los files y el path en el cual queremos
# exportar el resultado
def submit(): 
    ## tomamos el path escrito arriba
    path = path_var.get() 
    path_export = pathe_var.get()
    ## obtenemos los archivos .csv del path declarado
    files = [x for x in os.listdir(path) if x.endswith('.csv')]
    process_info(files[0], path, path_export)
    
# Diseñamos el aspecto de la interfaz gráfica
path_label = tk.Label(root, text = 'Path', font = ('calibre',10,'bold'))
# Este será el espacio para escribir el path en la interfaz gráfica
path_entry=tk.Entry(root, textvariable = path_var, font = ('calibre',10,'normal')) 

pathe_label = tk.Label(root, text = 'Export', font = ('calibre',10,'bold'))
# Este será el espacio para escribir el path de exportación en la interfaz gráfica
pathe_entry=tk.Entry(root, textvariable = pathe_var, font = ('calibre',10,'normal'))

sub_btn=tk.Button(root,text = 'Submit', command = submit) # Declaramos el botón que de inicio al procesamiento
  
path_label.grid(row=1,column=0)
path_entry.grid(row=1,column=1)
pathe_label.grid(row=2,column=0)
pathe_entry.grid(row=2,column=1)
sub_btn.grid(row=3,column=1)

root.mainloop()