import sys
import pandas as pd
import subprocess
import os

def revision_sistema(bitacora, control):
    print(f'Analizando archivo {bitacora}')
    dat = pd.read_csv(str(bitacora),
                      usecols=['fecha_carta_porte', 'cliente_carta_porte', 'folio_carta_porte', 'agente_carta_porte',
                               'no_economico_tracto', 'estatus_carta_porte'])
    no_status = dat[~dat['estatus_carta_porte'].str.contains('RUTA TERMINADA', case=False)]

    print(f'Analizando archivo {control}')
    dat = pd.read_csv(str(control),
                      usecols=['fecha_carta_porte', 'cliente_carta_porte', 'folio_carta_porte', 'unidad_carta_porte',
                               'comida', 'permisos', 'pistas', 'diesel_efectivo', 'otros'])
    dat['suma'] = dat.sum(axis=1)
    dat = dat[dat['suma'] == 0]
    no_gastos = dat[~dat['unidad_carta_porte'].str.contains('S-18|S-15|S-16')]

    print('Escribiendo archivos en output/revision_sistema.xlsx. Espere...')
    with pd.ExcelWriter('output/revision_sistema.xlsx') as writer:
        no_status.to_excel(writer, sheet_name='desactualizados')
        no_gastos.to_excel(writer, sheet_name='gastos_no_ingresados')

    print('Archivo escrito! Abriendo para revision manual')
    os.chdir('G:\\Mi unidad\\DWH\\PyScripts\\REVISION_DIARIA_DNV\\output')
    os.system('start excel.exe revision_sistema.xlsx')

    print(f'Eliminando archivos de entrada {bitacora} y {control}...')
    os.chdir('G:\\Mi unidad\\DWH\\PyScripts\\REVISION_DIARIA_DNV')
    subprocess.run(['rm', 'dat/*.csv'])

    print('Listo! Que tenga un excelente dia!! :)')

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    revision_sistema(arg1, arg2)