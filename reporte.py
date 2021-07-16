# /**
#  * @author Emmanuel Castillo
#  * @email ecastillot@unal.edu.co / ecastillo@sgc.gov.co
#  * @create date 2021-06-08 11:39:32
#  * @modify date 2021-06-19 18:13:10
#  * @desc description]
#  */

import os
import json
import logging
import argparse

from colorama.ansi import Fore, Style
import utils as ut
import datetime as dt
from collections import OrderedDict

DEFAULT_VAL = {"guardado":"true","nombre":None,"asunto":None,"fecha_ini":None,"fecha_fin":None,
                "type":None,"link":None,"editar":"","eliminar":"false","comprobar":None,"info_guardado":"false",
                "navegador":"","mag_min":None,"mag_max":None,"prof_min":None,"prof_max":None,
                "rms_min":None,"rms_max":None,"gap_min":None,"gap_max":None,"eprof_min":None,
                "eprof_max":None,"elon_min":None,"elon_max":None,"elat_min":None,"elat_max":None,
                "destinatarios":None,"guardar":"false","lat_central":None,"lon_central":None,
                "radio":None,"lat_min":None,"lat_max":None,"lon_min":None,"lon_max":None,
                "info_reporte":None,"ejemplo":None}
cwd = os.path.dirname(__file__)

def read_args():
    prefix = "+"
    ini_msg = "#"*120
    # obligatorio_msg = f"[Obligatorio]:\n\t{prefix*2}guardado"
    # opcional_msg = f"[Opcional]:\n\t{prefix*2}fecha_inicial {prefix*2}fecha_final {prefix*2}type {prefix*2}mag_min {prefix*2}mag_max {prefix*2}prof_min {prefix*2}prof-max {prefix*2}rms_min\n"+\
    #             f"       \t{prefix*2}rms_max {prefix*2}gap_min {prefix*2}gap_max {prefix*2}eprof_min {prefix*2}eprof_max {prefix*2}elon_min {prefix*2}elon_max {prefix*2}elat_min\n"\
    #             f"       \t{prefix*2}elat_max {prefix*2}nombre {prefix*2}link {prefix*2}guardar {prefix*2}destinatarios\n"+\
    #             f"       \n\t[radial]: {prefix*2}lat_central {prefix*2}lon_central {prefix*2}radio\n"+\
    #             f"       \t[cuadrante]: {prefix*2}lat_min {prefix*2}lat_max {prefix*2}lon_min {prefix*2}lon_max\n"
    # parser = argparse.ArgumentParser("Enviar reportes. ", prefix_chars=prefix)
    # parser = argparse.ArgumentParser("Enviar reportes. ",prefix_chars=prefix,
    #                      usage=f'\n{ini_msg}\n{obligatorio_msg} \n{opcional_msg}\n[{prefix}h {prefix*2}help] \n[{prefix*2}debug] \n{ini_msg}\n ')
    parser = argparse.ArgumentParser("Enviar reportes. ",prefix_chars=prefix,
                         usage=f'Enviar reportes.')

    parser.add_argument(prefix+"g",prefix*2+"guardado",
                        type=str,
                        default=DEFAULT_VAL["guardado"],
                        metavar='',
                        choices={"true", "false","True", "False"},
                        help="True para coger una busqueda guardada")

    parser.add_argument(prefix+"n",prefix*2+"nombre",
                        metavar='', default=DEFAULT_VAL["nombre"],
                        type=str,
                        help="Nombre del lugar (sin espacios) donde se guardo el reporte.")

    parser.add_argument(prefix+"a",prefix*2+"asunto",
                        metavar='',default=DEFAULT_VAL["asunto"],
                        type=str,
                        help="Asunto del correo")

    parser.add_argument(prefix+"fi",prefix*2+"fecha_ini",
                        metavar='',default=DEFAULT_VAL["fecha_ini"],
                        type=str,
                        help="[tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]."+\
                             " 2) Inicial del día, toma el día más cercano. W -> miercoles." +\
                                "3) 'hoy' toma la fecha de hoy")

    parser.add_argument(prefix+"ff",prefix*2+"fecha_fin",
                        metavar='',default=DEFAULT_VAL["fecha_fin"],
                        type=str,
                        help="[tres opciones] 1) Fecha de busqueda en el catalogo [YYYYmmdd]."+\
                             " 2) Inicial del día, toma el día más cercano. W -> miercoles." +\
                                "3) 'hoy' toma la fecha de hoy")

    parser.add_argument(prefix+"t",prefix*2+"type",
                        metavar='',default=DEFAULT_VAL["type"],
                        choices={"radial", "cuadrante"},
                        type=str,
                        help="[radial o cuadrante]. Para radial: ++lat_central, ++lon_central, ++radio."+\
                            " Para cuadrante: ++lat_min,++lon_min,++lat_max,++lon_max")

    parser.add_argument(prefix+"l",prefix*2+"link",
                        metavar='',default=DEFAULT_VAL["link"],
                        type=str,
                        help="link directo de busqueda. (A veces el grupo"+\
                            " de sistemas envia un link donde los paramateros ya estan definidos. )"+\
                            "Se debe definir ++type según sea el tipo de busqueda.")
    
    parser.add_argument(prefix+"e",prefix*2+"editar",
                        metavar='',default=DEFAULT_VAL["editar"],
                        type=str,
                        choices={"true", "false","True", "False"},
                        help="True para editar cosas generales del cuerpo del mensaje."+\
                            f"NO ELIMINE NI AGREGUE %%s. "+\
                            "Sirve para agregar o quitar datos adicionales a la plantilla.")

    parser.add_argument(prefix+"rm",prefix*2+"eliminar",
                        metavar='',default=DEFAULT_VAL["eliminar"],
                        type=str,
                        choices={"true", "false","True", "False"},
                        help="True para eliminar el reporte")

    parser.add_argument(prefix+"c",prefix*2+"comprobar",
                        metavar='',default=DEFAULT_VAL["comprobar"],
                        choices={"true", "false","True", "False"},
                        type=str,
                        help="True para comprobar el cuerpo del mensaje.")
    
    parser.add_argument(prefix+"ig",prefix*2+"info_guardado",
                        metavar='',default=DEFAULT_VAL["info_guardado"],
                        choices={"true", "false","True", "False"},
                        type=str,
                        help="True para ver los que estan guardados.")

    parser.add_argument(prefix+"ir",prefix*2+"info_reporte",
                        metavar='',default=DEFAULT_VAL["info_reporte"],
                        type=str,
                        help="Nombre del reporte que desea tener la información.")

    parser.add_argument(prefix+"nav",prefix*2+"navegador",
                        metavar='',default=DEFAULT_VAL["navegador"],
                        choices={"true", "false","True", "False"},
                        type=str,
                        help="True para abrir navegador")

    parser.add_argument(prefix+"magm",prefix*2+"mag_min",
                        metavar='',default=DEFAULT_VAL["mag_min"],
                        type=float,
                        help="Magnitud minima.")

    parser.add_argument(prefix+"magM",prefix*2+"mag_max",
                        metavar='',default=DEFAULT_VAL["mag_max"],
                        type=float,
                        help="Magnitud maxima.")

    parser.add_argument(prefix+"profm",prefix*2+"prof_min",
                        metavar='',default=DEFAULT_VAL["prof_min"],
                        type=float,
                        help="Profundidad minima.")

    parser.add_argument(prefix+"profM",prefix*2+"prof_max",
                        metavar='',default=DEFAULT_VAL["prof_max"],
                        type=float,
                        help="Profundidad maxima.")
    parser.add_argument(prefix+"rmsm",prefix*2+"rms_min",
                        metavar='',default=DEFAULT_VAL["rms_min"],
                        type=float,
                        help="rms minimo.")

    parser.add_argument(prefix+"rmsM",prefix*2+"rms_max",
                        metavar='',default=DEFAULT_VAL["rms_max"],
                        type=float,
                        help="rms maxima.")

    parser.add_argument(prefix+"gapm",prefix*2+"gap_min",
                        metavar='',default=DEFAULT_VAL["gap_min"],
                        type=float,
                        help="gap minimo.")

    parser.add_argument(prefix+"gapM",prefix*2+"gap_max",
                        metavar='',default=DEFAULT_VAL["gap_max"],
                        type=float,
                        help="gap maxima.")

    parser.add_argument(prefix+"eprofm",prefix*2+"eprof_min",
                        metavar='',default=DEFAULT_VAL["eprof_min"],
                        type=float,
                        help="Error minimo en profundidad.")

    parser.add_argument(prefix+"eprofM",prefix*2+"eprof_max",
                        metavar='',default=DEFAULT_VAL["eprof_max"],
                        type=float,
                        help="Error maximo en profundidad.")

    parser.add_argument(prefix+"elonm",prefix*2+"elon_min",
                        metavar='',default=DEFAULT_VAL["elon_min"],
                        type=float,
                        help="Error minimo en longitud.")

    parser.add_argument(prefix+"elonM",prefix*2+"elon_max",
                        metavar='',default=DEFAULT_VAL["elon_max"],
                        type=float,
                        help="Error maximo en longitud.")

    parser.add_argument(prefix+"elatm",prefix*2+"elat_min",
                        metavar='',default=DEFAULT_VAL["elat_min"],
                        type=float,
                        help="Error minimo en latitud.")

    parser.add_argument(prefix+"elatM",prefix*2+"elat_max",
                        metavar='',default=DEFAULT_VAL["elat_max"],
                        type=float,
                        help="Error maximo en latitud.")

    parser.add_argument(prefix+"d",prefix*2+"destinatarios",
                        metavar='',default= DEFAULT_VAL["destinatarios"],
                        nargs='+',
                        # type=list,
                        help= "Lista de correos a quienes se les va a enviar el reporte."+\
                                " Ejemplo: 'ecastillo@sgc.gov.co' 'rsncol@sgc.gov.co' ")
    
    parser.add_argument(prefix+"gg",prefix*2+"guardar",
                        metavar='', default= DEFAULT_VAL["guardar"],
                        choices={"true", "false","True", "False"},
                        type=str,
                        help= "True para guardar la busqueda")

    parser.add_argument(prefix+"latc",prefix*2+"lat_central",
                        metavar='',default=DEFAULT_VAL["lat_central"],
                        type=float,
                        help="Latitud central para tipo radial.")

    parser.add_argument(prefix+"lonc",prefix*2+"lon_central",
                        metavar='',default=DEFAULT_VAL["lon_central"],
                        type=float,
                        help="Longitud central para tipo radial.")

    parser.add_argument(prefix+"r",prefix*2+"radio",
                        metavar='',default=DEFAULT_VAL["radio"],
                        type=float,
                        help="Radio para tipo radial.")

    parser.add_argument(prefix+"latm",prefix*2+"lat_min",
                        metavar='',default=DEFAULT_VAL["lat_min"],
                        type=float,
                        help="Latitud minima para tipo cuadrante.")

    parser.add_argument(prefix+"latM",prefix*2+"lat_max",
                        metavar='',default=DEFAULT_VAL["lat_max"],
                        type=float,
                        help="Latitud maxima para tipo cuadrante.")

    parser.add_argument(prefix+"lonm",prefix*2+"lon_min",
                        metavar='',default=DEFAULT_VAL["lon_min"],
                        type=float,
                        help="Longitud minima para tipo cuadrante.")

    parser.add_argument(prefix+"lonM",prefix*2+"lon_max",
                        metavar='',default=DEFAULT_VAL["lon_max"],
                        type=float,
                        help="Longitud maxima para tipo cuadrante.")

    parser.add_argument(prefix+"ejemplo",prefix*2+"ejemplo",
                        metavar='',default=DEFAULT_VAL["ejemplo"],
                        choices={"crear_consulta","editar_consulta", "enviar_consulta"},
                        type=str,
                        help="Ejemplos-> crear_consulta, enviar_consulta")

    args = parser.parse_args()


    def check_variables(args):

        ### comprobamos que las variables se guarden en los formatos adecuados
        str_args = ['fecha_ini','fecha_fin','nombre','type','guardado','guardar',
                    'editar','comprobar','navegador','info_guardado',"info_reporte"]
        list_args = ['destinatarios']
        float_args = ['mag_max','mag_min','prof_min','prof_max','rms_min','rms_max',
                    'gap_min','gap_max','eprof_min','eprof_max','elon_min','elon_max',
                    'elat_min','elat_max','lat_central','lon_central','radio',
                    'lat_min','lat_max','lon_min','lon_max']

        order = [str,list,float]
        order_args = [str_args,list_args,float_args]
        vars_args = vars(args)
        
        for i, type_args in enumerate(order_args):
            for arg in type_args: 
                if arg in vars_args:
                    if isinstance(vars_args[arg],order[i]):
                        args_msg = f'{arg}-{vars_args[arg]}-{str(order[i])}-"Ok"'
                        ut.printlog("debug","Argumentos",args_msg)
                        # print(arg,vars_args[arg],str(order[i]),"Ok") 
        return vars_args

    vars_args = check_variables(args)
    #Si info_guardado == True muestre los archivos que estan guardados.

    if vars_args["ejemplo"] != None:

        if vars_args["ejemplo"] == "crear_consulta":
            while True:
                inp = input( Fore.GREEN + "[1] radial"+ "\t" +Fore.BLUE+"[2] cuadrante"+\
                 "\t"+Fore.YELLOW+"[3] link"+ Style.RESET_ALL+"\n")
                if inp == "1":
                    msg = 'python reporte.py'+\
                        Fore.RED + ' +g'+Style.RESET_ALL+ ' false'+\
                        Fore.RED + ' +gg'+Style.RESET_ALL+' true'+\
                        Fore.RED + ' +n'+Style.RESET_ALL+' quetame'+\
                        Fore.RED + ' +a'+Style.RESET_ALL+' "Reporte_radial"'+\
                        Fore.RED + ' +t'+Style.RESET_ALL+' radial'+\
                        Fore.RED + ' +d'+Style.RESET_ALL+' ecastillo@sgc.gov.co rsncol@sgc.gov.co'+\
                        Fore.RED + ' +fi'+Style.RESET_ALL+' V'+\
                        Fore.RED + ' +ff'+Style.RESET_ALL+' hoy'+\
                        Fore.RED + ' +latc'+Style.RESET_ALL+' 4.33'+\
                        Fore.RED + ' +lonc'+Style.RESET_ALL+' -73.86'+\
                        Fore.RED + ' +r'+Style.RESET_ALL+' 100'+\
                        Fore.RED + ' +e'+Style.RESET_ALL+' True'+\
                        Fore.RED + ' +c'+Style.RESET_ALL+' True'
                    break
                elif inp == "2":
                    msg = 'python reporte.py'+\
                        Fore.RED + ' +g'+Style.RESET_ALL+ ' false'+\
                        Fore.RED + ' +n'+Style.RESET_ALL+' puerto_gaitan'+\
                        Fore.RED + ' +a'+Style.RESET_ALL+" Reporte_cuadrante"+\
                        Fore.RED + ' +t'+Style.RESET_ALL+" cuadrante"+\
                        Fore.RED + ' +d'+Style.RESET_ALL+' ecastillo@sgc.gov.co rsncol@sgc.gov.co'+\
                        Fore.RED + ' +fi'+Style.RESET_ALL+' V'+\
                        Fore.RED + ' +ff'+Style.RESET_ALL+' hoy'+\
                        Fore.RED + ' +latm'+Style.RESET_ALL+' 3.42'+\
                        Fore.RED + ' +latM'+Style.RESET_ALL+' 4.41'+\
                        Fore.RED + ' +lonm'+Style.RESET_ALL+' -72.15'+\
                        Fore.RED + ' +lonM'+Style.RESET_ALL+' -70.84'+\
                        Fore.RED + ' +c'+Style.RESET_ALL+' True'
                    break
                elif inp == "3":
                    msg = 'python reporte.py'+\
                        Fore.RED + ' +g'+Style.RESET_ALL+ ' false'+\
                        Fore.RED + ' +n'+Style.RESET_ALL+' quetame_link'+\
                        Fore.RED + ' +a'+Style.RESET_ALL+" Reporte_link_radial"+\
                        Fore.RED + ' +t'+Style.RESET_ALL+" radial"+\
                        Fore.RED + ' +d'+Style.RESET_ALL+' ecastillo@sgc.gov.co rsncol@sgc.gov.co'+\
                        Fore.RED + ' +fi'+Style.RESET_ALL+' V'+\
                        Fore.RED + ' +ff'+Style.RESET_ALL+' hoy'+\
                        Fore.RED + ' +l'+Style.RESET_ALL+' http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Quetame/consultaexperta.php'+\
                        Fore.RED + ' +latc'+Style.RESET_ALL+' 4.33'+\
                        Fore.RED + ' +lonc'+Style.RESET_ALL+' -73.86'+\
                        Fore.RED + ' +r'+Style.RESET_ALL+' 100'+\
                        Fore.RED + ' +c'+Style.RESET_ALL+' True'
                    break
                else: 
                    pass
            
            print(msg+ Style.RESET_ALL)
            exit()
        elif vars_args["ejemplo"] == "editar_consulta":
            msg = 'python reporte.py'+\
                Fore.RED + ' +n'+Style.RESET_ALL+' quetame'+\
                Fore.RED + ' +a'+Style.RESET_ALL+" editando_consulta"+\
                Fore.RED + ' +d'+Style.RESET_ALL+' ecastillo@sgc.gov.co'
            print(msg+ Style.RESET_ALL)
            exit()
        elif vars_args["ejemplo"] == "enviar_consulta":
            msg = 'python reporte.py'+\
                Fore.RED + ' +n'+Style.RESET_ALL+' quetame'
            print(msg+ Style.RESET_ALL)
            exit()


    if vars_args['info_guardado'].lower() in ("true","t"):
        reportes = os.path.join(cwd,"reportes")
        listall = os.listdir(reportes)
        onlyfiles = [f.split(".")[0] for f in listall if os.path.isfile(os.path.join(reportes, f))]
        ut.printlog("INFO","guardados",onlyfiles)
        exit()
    elif vars_args['info_guardado'].lower() in ("false","f"):
        pass
    else: 
        raise Exception("info_guardado: True o False")

    # Muestre la info del reporte
    if vars_args['info_reporte'] != None:
        # try:
        jsonfile = os.path.join(cwd,"reportes",vars_args['info_reporte']+".json")
        with open(jsonfile) as jf:
            saved_args = json.load(jf)[0]

        saved_args = OrderedDict(sorted(saved_args.items()))
        for k, v in saved_args.items():
            print(k ,v)
        exit()

    # #CONDICIONAL 1: Veamos que pasa si esta o no esta guardado
    #       1)si: Lea el json donde esta guardado
    #       2)no: Toca asegurarse que otras variable esten defindias
    #       3) Solo se puede si o no.
    # Las variables extra en la línea de comando son tomadas en cuenta

    if vars_args['guardado'].lower() in ("true","t"):
        if vars_args['nombre'] != None:
            jsonfile = os.path.join(cwd,"reportes",vars_args['nombre']+".json")
            with open(jsonfile) as jf:
                saved_args = json.load(jf)[0]
                saved_args["guardado"] = "true"

                # tenga en cuenta las líneas que el usuario digito en el comando
                for key,value in vars_args.items():
                    if value != DEFAULT_VAL[key]:
                        saved_args[key] = value
                        ut.printlog("INFO","init_changes",f"{key}={saved_args[key]}")
                    else:
                        pass
                vars_args = saved_args

        else:
            raise Exception("Se necesita definir ++nombre")
    elif vars_args['guardado'].lower() in ("false","f"):
        if vars_args['asunto'] != None and vars_args['fecha_ini'] != None and\
        vars_args['fecha_fin'] != None and vars_args['nombre'] != None and\
            vars_args['type'] != None and vars_args['destinatarios'] != None:
            pass
        else:
            raise Exception("Se necesita definir: asunto, destinatarios,"+\
                " nombre","fecha_ini","fecha_fin","type")
    else:
        print(vars_args['guardado'].lower())
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
            # elif vars_args['link'] != None:
            #     pass
            else:
                raise Exception(f"se debe definir ++lat_central, ++lon_central, ++radio")


        if vars_args['type'] == 'cuadrante':
            if vars_args['lat_min'] != None and vars_args['lon_min'] != None and\
                vars_args['lat_max'] != None and vars_args['lon_max'] != None:
                pass
            # elif vars_args['link'] != None:
            #     pass
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
        else:
            raise Exception("Fechas mal digitadas")
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
    if busqueda.navegador.lower() in ("true","t"):
        hide = False
    else: 
        hide = True

    ut.printlog("info","Reporte","Creando reporte con web scraping")

    if busqueda.type == "radial":

        if busqueda.link !=None:
            query = ut.LinkedQuery(busqueda.link, hide_driver=hide)
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
        resultados = query.go2query(os.path.join(cwd,"archivos",busqueda.nombre))

    elif busqueda.type == "cuadrante":
        if busqueda.link != None:
            query = ut.LinkedQuery(busqueda.link, hide_driver=hide)
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
        resultados = query.go2query(os.path.join(cwd,"archivos",busqueda.nombre))

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
    print("\n")
    busqueda = read_args()
    # print(busqueda.__dict__)
    enviar_reporte(busqueda)

    
    # python enviar_reporte.py +g no +n quetame +a Prueba:reporte_quetame +d ecastillo@sgc.gov.co +fi v +ff hoy +t radial +latc 4.33 +lonc -73.86 +r 100 +gg False