import pandas as pd
import sqlite3

# Indicadores se encuentran en archivo de Excel
dat = pd.read_excel('dat/Todos los Rendimientos (2).xlsx')

# Renombramos columnas
dat = dat.rename(columns = {'RENDIMIENTO KM/L':'RENDIMIENTO', 'TIPO DE UNIDAD':'TIPO_UNIDAD', 'TRANSMISIÓN':'TRANSMISION'})

# Cargar información a SQL
db_engine = sqlite3.connect('../../DATABASES/SEVER.db')
dat.to_sql('INDICADORES_RENDIMIENTO',db_engine,if_exists='replace', index=False)