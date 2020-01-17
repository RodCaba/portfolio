import pandas as pd
import tools

ubicaciones = pd.read_excel('dat/cat_reparto_cliente.xlsx', dtype={'rep_cli_codigo':str}, nrows=491)
names = [*ubicaciones.columns.values]

# Separar columnas de latitud y longitud
ubicaciones = tools.sep_str(ubicaciones,"rep_cli_direccion",'/',1)

# Unir código y nombre con un espacio
ubicaciones = tools.join_str(ubicaciones, 'Nombre', 'rep_cli_codigo', 'rep_cli_nombre')

# Crear archivo faltantes, debe tener mismo tratamiento que archivo Ubicaciones y append PROXIMA APERTURA
faltantes = pd.read_excel('dat/cat_reparto_cliente.xlsx', dtype={'rep_cli_codigo':str}, skiprows=491, header=None, names=names)
faltantes = tools.sep_str(faltantes,'rep_cli_direccion',' ',1)
faltantes = tools.join_str(ubicaciones, 'Nombre', 'rep_cli_codigo', 'rep_cli_nombre')

# Unir los datos de PRÓXIMA APERTURA a faltantes
temp = ubicaciones[ubicaciones['Latitud'] == 'PROXIMA APERTURA']
faltantes = faltantes.append(temp)
faltantes = faltantes.iloc[:,[0,1,2,3]]

faltantes.to_excel('output/faltantes.xlsx')

# Remover PROXIMA APERTURA de ubicaciones existentes
ubicaciones = ubicaciones[ubicaciones['Latitud'] != 'PROXIMA APERTURA']

# Mantener vectores deseados
ubicaciones = ubicaciones[['Nombre', 'Latitud', 'Longitud']]

# Agregar campos adicionales
ubicaciones['Referencia'] = 'Cliente'
ubicaciones['Comentarios'] = 'Exportado'
ubicaciones['¿La zona circular?'] = 'No'
ubicaciones['Diámetro (m)'] = 250

# Exportar datos
ubicaciones.to_excel('output/ubicaciones_exp.xlsx', index = False)
