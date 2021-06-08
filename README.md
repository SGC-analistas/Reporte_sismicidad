![SGC](images/sgc_logo.png)<!-- .element width="700"-->

# Reporte de sismicidad

Rutina realizada para enviar reportes de sismicidad. Esta basado en web scraping. 

La rutina funciona para las fechas donde funciona seiscomp y únicamente si el siguiente link funciona bien:
[SGC-Catalogo](http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/consultaexperta.php)

## 1. Instalación en linux

### Requerimientos previos
Se corre en sistemas linux.

### - Python
Python Versión 3.7 en adelante. (Usaremos como ejemplo python 3.8)

Tener virtualenv en python.
```bash
sudo apt-get install python3.8
sudo apt-get install python3.8-venv
```

#### - Servidor SMTP
Tener un servidor SMTP *(Simple Mail Transfer Protocol)* el cual es un protocolo básico que permite que los emails viajen a través de Internet. 

```


### Instalación con pip 

```bash
python3.8 -m venv .reporte
source .reporte/bin/activate
pip install -r requirements.txt
```

## Autor

- Emmanuel David Castillo ecastillo@sgc.gov.co/ecastillot@unal.edu.co


