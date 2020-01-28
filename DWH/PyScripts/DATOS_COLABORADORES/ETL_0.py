import pandas as pd
import sqlite3

# Cargar datos
dat = pd.read_excel('dat/DATOS-COLABORADORES (4).xlsx')

dat = dat[[' ','NOMBRE COMPLETO','PUESTO','UNIDAD ASIGNADA (OP)','CELULAR EMPRESA', 'CELULAR PARTICULAR',
           'REGISTRO EN CAAT', 'ANTIGUEDAD']]

dat = dat.rename(columns ={' ':'ID_COLABORADOR','NOMBRE COMPLETO':'NOMBRE',
                 'UNIDAD ASIGNADA (OP)':'UNIDAD_OP','CELULAR EMPRESA':'CEL_1',
                 'CELULAR PARTICULAR': 'CEL_2', 'REGISTRO EN CAAT':'CAAT'})

# Crear conexión y subir información
db_engine = sqlite3.connect('../../DATABASES/SEVER.db')
dat.to_sql('COLABORADORES', db_engine, if_exists='replace',index = False)