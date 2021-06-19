![SGC](images/sgc_logo.png)<!-- .element width="700"-->

# Reporte de sismicidad

Rutina realizada para enviar reportes de sismicidad. Esta basado en web scraping. 

La rutina funciona para las fechas donde funciona seiscomp y únicamente si el siguiente link funciona bien:
[SGC-Catalogo](http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/consultaexperta.php)

## 1. Instalación en linux

### Requerimientos previos
Se corre en sistemas linux.

#### - Servidor SMTP
Tener un servidor SMTP *(Simple Mail Transfer Protocol)* el cual es un protocolo básico que permite que los emails viajen a través de Internet. 

### - Python
Python Versión 3.7 en adelante. (Usaremos como ejemplo python 3.8)

Tener virtualenv en python.
```bash
sudo apt-get install python3.8
sudo apt-get install python3.8-venv
```

#### Instalación con pip 
```bash
python3.8 -m venv .reporte
source .reporte/bin/activate
pip install -r requirements.txt
```

## 2. Instrucciones de uso

### 1. Crear y guardar consulta
#### cuadrante
python reporte.py +g True 

#### radial

#### link

## 3. Comandos
Al digitar 
```bash 
 python reporte.py +h
 ```
Pueden obaservar la siguiente ayuda:
Al digitar 
```bash 
  +h, ++help            Ayuda
  +g , ++guardado       True para coger una busqueda guardada. Se envia tal y como estaba guardado.
  +n , ++nombre         Nombre del lugar (sin espacios) donde se guardo el reporte.
  +a , ++asunto         Asunto del correo
  +fi , ++fecha_ini     [tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]. 2) Inicial del día, toma el día más cercano. W -> miercoles.3) 'hoy' toma la fecha de hoy
  +ff , ++fecha_fin     [tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]. 2) Inicial del día, toma el día más cercano. W -> miercoles.3) 'hoy' toma la fecha de hoy
  +t , ++type           [radial o cuadrante]. Para radial: ++lat_central, ++lon_central, ++radio. Para cuadrante: ++lat_min,++lon_min,++lat_max,++lon_max
  +l , ++link           link directo de busqueda. (A veces el grupo de sistemas envia un link donde los paramateros ya estan definidos. )Se debe definir ++type según sea el tipo de busqueda.
  +e , ++editar         True para editar cosas generales del cuerpo del mensaje.NO ELIMINE NI AGREGUE %s. Sirve para agregar o quitar datos adicionales a la plantilla.
  +c , ++comprobar      True para comprobar el cuerpo del mensaje.
  +ig , ++info_guardado  True para ver los que estan guardados.
  +nav , ++navegador    True para abrir navegador
  +magm , ++mag_min     Magnitud minima.
  +magM , ++mag_max     Magnitud maxima.
  +profm , ++prof_min   Profundidad minima.
  +profM , ++prof_max   Profundidad maxima.
  +rmsm , ++rms_min     rms minimo.
  +rmsM , ++rms_max     rms maxima.
  +gapm , ++gap_min     gap minimo.
  +gapM , ++gap_max     gap maxima.
  +eprofm , ++eprof_min Error minimo en profundidad.
  +eprofM , ++eprof_max Error maximo en profundidad.
  +elonm , ++elon_min   Error minimo en longitud.
  +elonM , ++elon_max   Error maximo en longitud.
  +elatm , ++elat_min   Error minimo en latitud.
  +elatM , ++elat_max   Error maximo en latitud.
  +d  [ ...], ++destinatarios  [ ...] Lista de correos a quienes se les va a enviar el reporte. Ejemplo: 'ecastillo@sgc.gov.co' 'rsncol@sgc.gov.co'
  +gg , ++guardar       True para guardar la busqueda
  +latc , ++lat_central Latitud central para tipo radial.
  +lonc , ++lon_central Longitud central para tipo radial.
  +r , ++radio          Radio para tipo radial.
  +latm , ++lat_min     Latitud minima para tipo cuadrante.
  +latM , ++lat_max     Latitud maxima para tipo cuadrante.
  +lonm , ++lon_min     Longitud minima para tipo cuadrante.
  +lonM , ++lon_max     Longitud maxima para tipo cuadrante.

 ```
 
## Autor

- Emmanuel David Castillo ecastillo@sgc.gov.co/ecastillot@unal.edu.co


