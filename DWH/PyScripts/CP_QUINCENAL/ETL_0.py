import pandas as pd
import sqlite3

# Cargar datos de CSV
# Descargamos reporte de Sistema DVN de quincena, con TODOS los campos activos, se filtran a través de pandas:
dat = pd.read_csv('dat/Bitacora_de_cartas_portes_20200128104930.csv',
                  usecols=['fecha_carta_porte','cliente_carta_porte', 'folio_carta_porte', 'agente_carta_porte',
                           'no_economico_caja','no_economico_tracto','operador_carta_porte','origen_carta_porte',
                           'destino_carta_porte','importe_total_pedido','estatus_carta_porte'])

# Jalar información de ID OPERADORES, y unimos para crear la serie de ID

db_engine = sqlite3.connect('../../DATABASES/SEVER.db')

query = """
SELECT ID_COLABORADOR, NOMBRE
FROM COLABORADORES

WHERE PUESTO = 'OPERADOR';"""

temp = pd.read_sql(query, db_engine)
temp = dat.set_index('operador_carta_porte').join(temp.set_index('NOMBRE'))
temp.reset_index(inplace= True)

temp = temp.rename(columns = {'index':'operador_carta_porte'})

# Separamos folio de carta porte para crear ID con sólo numeros y renombramos columna
id_cp = temp['folio_carta_porte'].str.split('CO0', n = 1, expand = True)
id_cp = id_cp[1].map(int)

temp['folio_carta_porte'] = id_cp
temp = temp.rename(columns = {'folio_carta_porte':'ID_CP'})

# Separamos No_económico para relacionarlo con ID y renombramos
no_eco = temp['no_economico_tracto'].str.split(n = 1, expand = True)
no_eco = no_eco[0]

temp['no_economico_tracto'] = no_eco
temp = temp.rename(columns = {'no_economico_tracto':'ECO'})

# Seleccionamos DataFrame a utilizar con columnas deseadas
dat = temp[['fecha_carta_porte','ID_CP','agente_carta_porte','ECO','operador_carta_porte','ID_COLABORADOR',
            'origen_carta_porte', 'destino_carta_porte', 'importe_total_pedido','estatus_carta_porte']]

# Subimos el DataFrame a la base de datos, esquema 'replace' para poder ir anexando información.

dat.to_sql('CP_Q',db_engine,if_exists='append',index = False)