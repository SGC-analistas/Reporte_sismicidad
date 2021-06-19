# /**
#  * @author Emmanuel Castillo
#  * @email ecastillot@unal.edu.co / ecastillo@sgc.gov.co
#  * @create date 2021-06-08 11:39:32
#  * @modify date 2021-06-08 11:39:32
#  * @desc [description]
#  */

import os
import json
import logging
import argparse
import utils as ut
import datetime as dt

def read_args():
    prefix = "+"
    ini_msg = "#"*120
    obligatorio_msg = f"[Obligatorio]:\n\t{prefix*2}guardado"
    opcional_msg = f"[Opcional]:\n\t{prefix*2}fecha_inicial {prefix*2}fecha_final {prefix*2}type {prefix*2}mag_min {prefix*2}mag_max {prefix*2}prof_min {prefix*2}prof-max {prefix*2}rms_min\n"+\
                f"       \t{prefix*2}rms_max {prefix*2}gap_min {prefix*2}gap_max {prefix*2}eprof_min {prefix*2}eprof_max {prefix*2}elon_min {prefix*2}elon_max {prefix*2}elat_min\n"\
                f"       \t{prefix*2}elat_max {prefix*2}nombre {prefix*2}link {prefix*2}guardar {prefix*2}destinatarios\n"+\
                f"       \n\t[radial]: {prefix*2}lat_central {prefix*2}lon_central {prefix*2}radio\n"+\
                f"       \t[cuadrante]: {prefix*2}lat_min {prefix*2}lat_max {prefix*2}lon_min {prefix*2}lon_max\n"

    parser = argparse.ArgumentParser("Enviar reportes. ",prefix_chars=prefix,
                         usage=f'\n{ini_msg}\n{obligatorio_msg} \n{opcional_msg}\n[{prefix}h {prefix*2}help] \n[{prefix*2}debug] \n{ini_msg}\n ')

    parser.add_argument(prefix+"g",prefix*2+"guardado",
                        default=None,
                        type=bool,
                        metavar='',
                        help="True para coger una busqueda guardada", required = True)

    parser.add_argument(prefix+"n",prefix*2+"nombre",
                        metavar='', default=None,
                        type=str,
                        help="Nombre del lugar (sin espacios) donde se guardo el reporte.")

    parser.add_argument(prefix+"a",prefix*2+"asunto",
                        metavar='',default=None,
                        type=str,
                        help="Asunto del correo")

    parser.add_argument(prefix+"fi",prefix*2+"fecha_ini",
                        metavar='',default=None,
                        type=str,
                        help="[tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]."+\
                             " 2) Inicial del día, toma el día más cercano. W -> miercoles." +\
                                "3) 'hoy' toma la fecha de hoy")

    parser.add_argument(prefix+"ff",prefix*2+"fecha_fin",
                        metavar='',default=None,
                        type=str,
                        help="[tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]."+\
                             " 2) Inicial del día, toma el día más cercano. W -> miercoles." +\
                                "3) 'hoy' toma la fecha de hoy")
    
    parser.add_argument(prefix+"t",prefix*2+"type",
                        metavar='',default=None,
                        type=str,
                        help="[radial o cuadrante]. Para radial: ++lat_central, ++lon_central, ++radio."+\
                            " Para cuadrante: ++lat_min,++lon_min,++lat_max,++lon_max")

    parser.add_argument(prefix+"l",prefix*2+"link",
                        metavar='',default=None,
                        type=str,
                        help="link directo de busqueda. (A veces el grupo"+\
                            " de sistemas envia un link donde los paramateros ya estan definidos. )"+\
                            "Se debe definir ++type según sea el tipo de busqueda.")
    
    parser.add_argument(prefix+"e",prefix*2+"editar",
                        metavar='',default=None,
                        type=bool,
                        help="True para editar cosas generales del cuerpo del mensaje."+\
                            f"NO ELIMINE NI AGREGUE %%s. "+\
                            "Sirve para agregar o quitar datos adicionales a la plantilla.")

    parser.add_argument(prefix+"c",prefix*2+"comprobar",
                        metavar='',default=None,
                        type=bool,
                        help="True para comprobar el cuerpo del mensaje.")
    
    parser.add_argument(prefix+"ig",prefix*2+"info_guardado",
                        metavar='',default=None,
                        type=bool,
                        help="True para ver los que estan guardados.")

    parser.add_argument(prefix+"nav",prefix*2+"navegador",
                        metavar='',default=False,
                        type=bool,
                        help="True para abrir navegador")

    parser.add_argument(prefix+"magm",prefix*2+"mag_min",
                        metavar='',default=None,
                        type=float,
                        help="Magnitud minima.")

    parser.add_argument(prefix+"magM",prefix*2+"mag_max",
                        metavar='',default=None,
                        type=float,
                        help="Magnitud maxima.")

    parser.add_argument(prefix+"profm",prefix*2+"prof_min",
                        metavar='',default=None,
                        type=float,
                        help="Profundidad minima.")

    parser.add_argument(prefix+"profM",prefix*2+"prof_max",
                        metavar='',default=None,
                        type=float,
                        help="Profundidad maxima.")

    parser.add_argument(prefix+"rmsm",prefix*2+"rms_min",
                        metavar='',default=None,
                        type=float,
                        help="rms minimo.")

    parser.add_argument(prefix+"rmsM",prefix*2+"rms_max",
                        metavar='',default=None,
                        type=float,
                        help="rms maxima.")

    parser.add_argument(prefix+"gapm",prefix*2+"gap_min",
                        metavar='',default=None,
                        type=float,
                        help="gap minimo.")

    parser.add_argument(prefix+"gapM",prefix*2+"gap_max",
                        metavar='',default=None,
                        type=float,
                        help="gap maxima.")

    parser.add_argument(prefix+"eprofm",prefix*2+"eprof_min",
                        metavar='',default=None,
                        type=float,
                        help="Error minimo en profundidad.")

    parser.add_argument(prefix+"eprofM",prefix*2+"eprof_max",
                        metavar='',default=None,
                        type=float,
                        help="Error maximo en profundidad.")

    parser.add_argument(prefix+"elonm",prefix*2+"elon_min",
                        metavar='',default=None,
                        type=float,
                        help="Error minimo en longitud.")

    parser.add_argument(prefix+"elonM",prefix*2+"elon_max",
                        metavar='',default=None,
                        type=float,
                        help="Error maximo en longitud.")

    parser.add_argument(prefix+"elatm",prefix*2+"elat_min",
                        metavar='',default=None,
                        type=float,
                        help="Error minimo en latitud.")

    parser.add_argument(prefix+"elatM",prefix*2+"elat_max",
                        metavar='',default=None,
                        type=float,
                        help="Error maximo en latitud.")

    parser.add_argument(prefix+"d",prefix*2+"destinatarios",
                        metavar='',default= None,
                        nargs='+',
                        # type=list,
                        help= "Lista de correos a quienes se les va a enviar el reporte."+\
                                " Ejemplo: 'ecastillo@sgc.gov.co' 'rsncol@sgc.gov.co' ")
    
    parser.add_argument(prefix+"gg",prefix*2+"guardar",
                        metavar='', default= True,
                        type=bool,
                        help= "True para guardar la busqueda")

    parser.add_argument(prefix+"latc",prefix*2+"lat_central",
                        metavar='',default=None,
                        type=float,
                        help="Latitud central para tipo radial.")

    parser.add_argument(prefix+"lonc",prefix*2+"lon_central",
                        metavar='',default=None,
                        type=float,
                        help="Longitud central para tipo radial.")

    parser.add_argument(prefix+"r",prefix*2+"radio",
                        metavar='',default=None,
                        type=float,
                        help="Radio para tipo radial.")

    parser.add_argument(prefix+"latm",prefix*2+"lat_min",
                        metavar='',default=None,
                        type=float,
                        help="Latitud minima para tipo cuadrante.")

    parser.add_argument(prefix+"latM",prefix*2+"lat_max",
                        metavar='',default=None,
                        type=float,
                        help="Latitud maxima para tipo cuadrante.")

    parser.add_argument(prefix+"lonm",prefix*2+"lon_min",
                        metavar='',default=None,
                        type=float,
                        help="Longitud minima para tipo cuadrante.")

    parser.add_argument(prefix+"lonM",prefix*2+"lon_max",
                        metavar='',default=None,
                        type=float,
                        help="Longitud maxima para tipo cuadrante.")

    parser.add_argument(prefix+"-debug",
                        metavar='',default=None,
                        help= "Muestra toda la información del proceso de la rutina")

    args = parser.parse_args()
    ### comprobamos que las variables se guarden en los formatos adecuados
    bool_args = ['guardado','guardar','editar','comprobar','navegador','info_guardado']
    str_args = ['fecha_ini','fecha_fin','nombre','type']
    list_args = ['destinatarios']
    float_args = ['mag_max','mag_min','prof_min','prof_max','rms_min','rms_max',
                'gap_min','gap_max','eprof_min','eprof_max','elon_min','elon_max',
                'elat_min','elat_max','lat_central','lon_central','radio',
                'lat_min','lat_max','lon_min','lon_max']

    order = [bool,str,list,float]
    order_args = [bool_args,str_args,list_args,float_args]
    vars_args = vars(args)
    
    for i, type_args in enumerate(order_args):
        for arg in type_args: 
            if arg in vars_args:
                if isinstance(vars_args[arg],order[i]):
                    args_msg = f'{arg}-{vars_args[arg]}-{str(order[i])}-"Ok"'
                    ut.printlog("debug","Argumetos",args_msg)
                    # print(arg,vars_args[arg],str(order[i]),"Ok") 

    #Si info_guardado == True muestre los archivos que estan guardados.
    if vars_args['info_guardado']:
        reportes = os.path.join(os.getcwd(),"reportes")
        listall = os.listdir(reportes)
        onlyfiles = [f.split(".")[0] for f in listall if os.path.isfile(os.path.join(reportes, f))]
        ut.printlog("INFO","guardados",onlyfiles)
        exit()


    # #CONDICIONAL 1: Veamos que pasa si esta o no esta guardado
    #       1)si: Lea el json donde esta guardado
    #       2)no: Toca asegurarse que otras variable esten defindias
    #       3) Solo se puede si o no.
    if vars_args['guardado'] == True:
        if vars_args['nombre'] != None:
            jsonfile = os.path.join(os.getcwd(),"reportes",vars_args['nombre']+".json")
            with open(jsonfile) as jf:
                vars_args = json.load(jf)[0]
                vars_args["guardado"] = True
        else:
            raise Exception("Se necesita definir ++nombre")
    elif vars_args['guardado'] == False:
        if vars_args['asunto'] != None and vars_args['fecha_ini'] != None and\
           vars_args['fecha_fin'] != None and vars_args['nombre'] != None and\
            vars_args['type'] != None and vars_args['destinatarios'] != None:
            pass
        else:
            raise Exception("Se necesita definir: asunto, destinatarios,"+\
                " nombre","fecha_ini","fecha_fin","type")
    else:
        raise Exception("guardado: True o False")


    # #CONDICIONAL 2: Si se define link toca que se defina que 'tipo' de busqueda es.
    if vars_args['link'] != None:
        if vars_args['type'] != None:
            pass
        else:
            raise Exception(f"se debe definir ++type")

    # #CONDICIONAL 3: Si se define 'tipo' entonces se deben especificar 
    #                   los datos radiales o de cuadrante. Necesarios para
    #                   enviar la info de los datos en el cuerpo del correo.
    if vars_args['type'] != None:
        if vars_args['type'] == 'radial':
            if (vars_args['lat_central'] != None) and (vars_args['lon_central'] != None) and\
                (vars_args['radio'] != None):
                pass
            else:
                raise Exception(f"se debe definir ++lat_central, ++lon_central, ++radio")


        if vars_args['type'] == 'cuadrante':
            if vars_args['lat_min'] != None and vars_args['lon_min'] != None and\
                vars_args['lat_max'] != None and vars_args['lon_max'] != None:
                pass
            else:
                raise Exception(f"se debe definir ++lat_min, ++lat_max, ++lon_min, ++lon_max")

    # Preparemos el reporte: 1) Si esta guardado entonces compruebe que los archivos
    # necesarios estan disponibles. 2)Si quiere
    # guardarlo y ya existe pedir permiso para sobreescribirlo.
    ut.prepare_report(vars_args)


    ## Devolvemos un objeto Busqueda.
    def get_date(date):

        if date in ('L','M','W','J','V','S','D') or\
                date in ('l','m','w','j','v','s','d'):

            mydate = ut.get_last_day(date)
            
        elif len(date) == 8:
            mydate = dt.datetime.strptime(date, '%Y%m%d')

        elif date == "hoy":
            mydate = dt.datetime.today()
        return mydate

    class Busqueda(object):
        def __init__(self,**kwargs):
            """
            Parameters:
            -----------
                **kwargs: Argumentos de read_args
            """
            for key, value in kwargs.items():
                setattr(self, key, value)

            self.fecha_inicial = get_date(self.fecha_ini)
            self.fecha_final = get_date(self.fecha_fin)

    return Busqueda(**vars_args)

def make_report(busqueda):
    """
    Parametros:
    -----------
        busqueda: Objeto Busqueda 
            El objeto Busqueda lo crea el metodo read_args

    Devuelve:
        resultados: diccionario
            keys: {'sismos', 'fecha_inicial','fecha_final','archivos_descargados'}
                sismos-> int: Numero de sismos que arrojo la busqueda
                fecha_inicial:-> str:fecha_inicial que tomo la busqueda
                fecha_final-> str: Fecha final que tomo la busqueda
                archivos_descargados-> list : Lista de rutas de los archivos que se deben anexar en el correo.
    ---------

    """

    if busqueda.navegador == True:
        hide = False
    else: 
        hide = True

    ut.printlog("info","Reporte","Creando reporte con web scraping")

    if busqueda.type == "radial":

        if busqueda.link !=None:
            query = ut.LinkedQuery(busqueda.link)
        else:
            query = ut.RadialQuery(min_date=busqueda.fecha_inicial,max_date=busqueda.fecha_final,
                                        lon=busqueda.lon_central,lat=busqueda.lat_central,radius=busqueda.radio,
                                        min_mag=busqueda.mag_min,max_mag=busqueda.mag_max,
                                        min_depth=busqueda.prof_min,max_depth=busqueda.prof_max,
                                        min_RMS=busqueda.rms_min,max_RMS=busqueda.prof_max,
                                        min_gap=busqueda.gap_min,max_gap=busqueda.gap_max,
                                        min_error_depth=busqueda.eprof_min,max_error_depth=busqueda.eprof_max,
                                        min_error_lon=busqueda.elon_min,max_error_lon=busqueda.elon_max,
                                        min_error_lat=busqueda.elat_min,max_error_lat=busqueda.elat_max,
                                        hide_driver=hide)
        resultados = query.go2query(os.path.join(os.getcwd(),"archivos",busqueda.nombre))

    elif busqueda.type == "cuadrante":
        if busqueda.link != None:
            query = ut.LinkedQuery(busqueda.link)
        else:
            query = ut.SquareQuery(min_date=busqueda.fecha_inicial,max_date=busqueda.fecha_final,
                                    min_lat=busqueda.lat_min,max_lat=busqueda.lat_max,
                                    min_lon=busqueda.lon_min,max_lon=busqueda.lon_max,
                                    min_mag=busqueda.mag_min,max_mag=busqueda.mag_max,
                                    min_depth=busqueda.prof_min,max_depth=busqueda.prof_max,
                                    min_RMS=busqueda.rms_min,max_RMS=busqueda.prof_max,
                                    min_gap=busqueda.gap_min,max_gap=busqueda.gap_max,
                                    min_error_depth=busqueda.eprof_min,max_error_depth=busqueda.eprof_max,
                                    min_error_lon=busqueda.elon_min,max_error_lon=busqueda.elon_max,
                                    min_error_lat=busqueda.elat_min,max_error_lat=busqueda.elat_max,
                                    hide_driver=hide)
        resultados = query.go2query(os.path.join(os.getcwd(),"archivos",busqueda.nombre))

    else:
        raise Exception(f"type:{busqueda.type} no esta definido. Solo radial o cuadrante")

    return resultados

def enviar_reporte(busqueda):
    """
    Parametros:
    -----------
        busqueda: Objeto Busqueda 
            El objeto Busqueda lo crea el metodo read_args

    Devuelve:
        Envia el correo

    """
    
    resultados = make_report(busqueda)
    ut.email(busqueda.__dict__,resultados)
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
                        datefmt='%m-%d %H:%M')
    print("\n\n")
    busqueda = read_args()
    enviar_reporte(busqueda)

    
    # python enviar_reporte.py +g no +n quetame +a Prueba:reporte_quetame +d ecastillo@sgc.gov.co +fi v +ff hoy +t radial +latc 4.33 +lonc -73.86 +r 100 +gg False