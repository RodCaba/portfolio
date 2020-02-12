## Revisión Diaria Automática de Sistema
Se trata de un archivo que realiza el análisis de el estatus de Sistema empresarial a partir de algunos parámetros de 2 archivos de entrada, Bitácora y Control.
Genera y abre automáticamente un archivo en Excel para comprobar la información de forma manual. 

Para probar el archivo posicionarse en el directorio REVISION_DIARIA_DNV y ejecutar el siguiente comando en el CMD

$ python revision_sistema.pý dat/[archivo_bitacora].csv dat/[archivo_control].csv
