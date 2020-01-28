import pandas as pd
import sqlite3

# Cargar datos de Métrica
dat = pd.read_excel('dat/Advanced Fuel and EV Energy Report_20200121_093811.xlsx', skiprows=12,usecols='A:H',
                    sheet_name='Report')

# Ingresar fechas variables
f0 = pd.datetime(year=2020, month=1, day=1)
f1 = pd.datetime(year=2020, month=1, day=15, hour=23, minute=59, second=59)

# Transformar datos
temp = dat['Vehículo'].str.split(' ', expand = True)
dat['UNIDAD'] = temp[0]
dat['F0_PERIODO'] = f0
dat['F1_PERIODO'] = f1

dat = dat[['UNIDAD', 'F0_PERIODO', 'F1_PERIODO', 'Distancia','Combustible consumido']]
dat = dat.rename(columns={'Distancia':'DISTANCIA', 'Combustible consumido':'LITROS_DIESEL'})

# REMOVEMOS OUTLIER
dat = dat[dat['UNIDAD'] != 'SEVER']

# Creamos conexión con DATABASE y subimos información
db_engine = sqlite3.connect('../../DATABASES/SEVER.db')

dat.to_sql('RENDIMIENTO_Q',db_engine, index=False)
