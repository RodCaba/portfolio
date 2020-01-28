import pandas as pd
import sqlite3

path_dat = 'G:/Unidades compartidas/Seguridad y Procesos/Parque Vehicular 2019 Sever.xlsx'
# Cargamos datos del parque vehicular
dat = pd.read_excel(path_dat, skiprows=1,usecols='B:K')
temp = pd.read_excel(path_dat, skiprows=1, usecols='M:T', nrows=5)

# Rearrange cols as desired
dat = dat[['# Eco Camion/caja', 'Modelo', 'Marca', 'Placa', 'Tipo','Numero de Serie', 'Número de Póliza']]
temp = temp[['# Eco Camion/caja.1', 'Modelo.1', 'Marca.1', 'Placa.1', 'Tipo.1','Numero de Serie.1', 'Número de Póliza.1']]
temp = temp.rename(columns = {'# Eco Camion/caja.1' : '# Eco Camion/caja', 'Modelo.1':'Modelo',
                              'Marca.1':'Marca', 'Placa.1':'Placa', 'Tipo.1':'Tipo',
                              'Numero de Serie.1':'Numero de Serie', 'Número de Póliza.1':'Número de Póliza'})

dat = dat.append(temp)

# Crear conexión con DB
db_engine = sqlite3.connect('../../DATABASES/SEVER.db')

# Subir DF to SQL
dat.to_sql('UNIDADES', db_engine,if_exists='replace')