import pandas as pd
import sqlite3

# Constante global
CRE_precio = 21.44

# Creamos conexión con DB
db_engine = sqlite3.connect('../../DATABASES/SEVER.db')
query = """SELECT ECO, RENDIMIENTO_Q.ECO,
F0_PERIODO, F1_PERIODO, round(DISTANCIA,2) AS DISTANCIA,
round(LITROS_DIESEL,2) AS LITROS_DIESEL,
round(DISTANCIA / LITROS_DIESEL,2) AS REND_Q,
INDICADORES_RENDIMIENTO.RENDIMIENTO

FROM RENDIMIENTO_Q

INNER JOIN INDICADORES_RENDIMIENTO
ON INDICADORES_RENDIMIENTO.ID_UNIDAD = RENDIMIENTO_Q.ID_UNIDAD

WHERE RENDIMIENTO_Q.ECO IS NOT NULL
;"""

dat = pd.read_sql(query, db_engine)
dat = dat[dat['REND_Q'] < dat['RENDIMIENTO']]

dat['AC'] = ((dat['DISTANCIA'] / dat['RENDIMIENTO']) - dat['LITROS_DIESEL']) * CRE_precio

dat.to_excel('output/acciones_correctivas_diesel.xlsx')