# Descargamos reporte en CSV de CP, seleccionando todos los campos y fecha lo que va del primero del mes a hoy
import pandas as pd
import subprocess



# Leemos archivo CSV, escogemos columnas deseadas
# AUTOMATIZAR

dat = pd.read_csv('dat/Bitacora_de_cartas_portes_20200212124624.csv',
                  usecols=['fecha_carta_porte', 'cliente_carta_porte', 'folio_carta_porte', 'agente_carta_porte',
                           'no_economico_tracto', 'estatus_carta_porte'])

# Filtramos aquellas que tienen estatus desactualizados
no_status = dat[~dat['estatus_carta_porte'].str.contains('RUTA TERMINADA', case = False)]

# Descargamos reporte en CSV de Control de utilidad por carta porte,
# seleccionando todos los campos y fecha lo que va del primero del mes a hoy
dat = pd.read_csv('dat/Control_de_utilidad_por_carta_porte_20200212132216.csv',
                  usecols = ['fecha_carta_porte', 'cliente_carta_porte', 'folio_carta_porte', 'unidad_carta_porte',
                             'comida', 'permisos', 'pistas', 'diesel_efectivo', 'otros'])

# Creamos Vector de sumas de gastos y filtramos aquellos que no tienen y que no forman parte de operación de SECOS
dat['suma'] = dat.sum(axis = 1)

dat = dat[dat['suma'] == 0]
no_gastos = dat[~dat['unidad_carta_porte'].str.contains('S-18|S-15|S-16')]

# Generamos Excel que guarde esta información

# AUTOMATIZAR escritura y apertura

with pd.ExcelWriter('output/revision_sistema.xlsx') as writer:
    no_status.to_excel(writer, sheet_name='desactualizados')
    no_gastos.to_excel(writer, sheet_name= 'gastos_no_ingresados')

# Revisamos de forma manual y enviamos

# Removemos datos de entrada CSV para no almacenar demasiada información
subprocess.run(['rm', 'dat/*.csv'])