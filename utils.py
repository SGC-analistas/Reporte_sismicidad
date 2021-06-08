# /**
#  * @author Emmanuel Castillo
#  * @email ecastillot@unal.edu.co / ecastillo@sgc.gov.co
#  * @create date 2021-06-01 04:54:12
#  * @modify date 2021-06-08 11:39:17
#  * @desc [description]
#  */

import os
import pandas as pd
import sys
import glob
import logging
import json
import time
import calendar
import datetime as dt
import html2text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import smtplib 
import locale
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

ejecutar = "virtualenv"
if ejecutar == "virtualenv":
    from get_gecko_driver import GetGeckoDriver
    get_driver = GetGeckoDriver()
    get_driver.install()

def printlog(levelname,name,msg):
    """
    Parameters:
    -----------
    author: str
    """
    logger = logging.getLogger(name)
    if levelname in ("debug","Debug","DEBUG"):
        logger.debug(msg)
    elif levelname in ("info","information","INFO","Info","INFORMATION"):
        logger.info(msg)
    elif levelname in ("warning","Warning","WARNING"):
        logger.warning(msg)
    elif levelname in ("error","ERROR"):
        logger.error(msg)

def get_web_preferences(download_folder,hide=False):
    """
    Web preferences for Firefox Web Driver.

    Parameters:
    -----------
        hide = Bolean
            If true, web driver will be hided.

    Returns:
    --------
        options: Option class from selenium.webdriver.firefox.option
        profile: FirefoxProfile from web driver
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # not use the custom location for the download files
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_folder)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/force-download,'application/vnd.google-earth.kml+xml'")

    options = Options()
    if hide:
        options.add_argument('--headless')

    return options,profile

def get_day(driver,name):
    mytime = driver.find_element_by_xpath(f"//input[ @class='hasDatepicker' and @name='{name}' ]").get_attribute("value")
    mytime =  dt.datetime.strptime(mytime, '%d/%m/%Y')
    mytime =  mytime.strftime('%d de %B de %Y')
    return mytime

def select_day(driver,name,year,month,day):
    driver.find_element_by_xpath(f"//input[ @class='hasDatepicker' and @name='{name}']").click()
    driver.find_element_by_xpath(f"//*[@id='ui-datepicker-div']/div/div/select[1]/option[text()='{month}']").click()
    driver.find_element_by_xpath(f"//*[@id='ui-datepicker-div']/div/div/select[2]/option[text()='2021']").click()
    day_table = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody')
    days = day_table.find_elements(By.TAG_NAME, "a")
    for j,oneday in enumerate(days,1):
        if str(j) == day:
            oneday.click()

def mv_downloaded_files(download_folder):
    name = os.path.basename(download_folder)
    filepaths = []
    for downloaded_file in glob.glob(os.path.join(download_folder,"*")):
        basename = os.path.basename(downloaded_file)
        dirname = os.path.dirname(downloaded_file)
        filepath = os.path.join(dirname,".".join((name,basename.split(".")[-1])))

        msg = f"mv {downloaded_file} {filepath}"
        os.system(msg)

        filepaths.append(filepath)
    return filepaths

class SquareQuery(object):
    def __init__(self,min_date,max_date,min_lon=-90,max_lon=-66,
                min_lat=-7,max_lat=15,min_mag=0,max_mag=9,
                min_depth=0,max_depth=700,min_RMS=0,max_RMS=10,
                min_gap=0,max_gap=360,min_error_depth=0,
                max_error_depth=999,min_error_lon=0,max_error_lon=999,
                min_error_lat=0,max_error_lat=999,hide_driver=False):
        
        self.type = "square"
        self.min_date = min_date
        self.max_date = max_date
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_mag = min_mag
        self.max_mag = max_mag
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.min_RMS = min_RMS
        self.max_RMS = max_RMS
        self.min_gap = min_gap
        self.max_gap = max_gap
        self.min_error_depth = min_error_depth
        self.max_error_depth = max_error_depth
        self.min_error_lon = min_error_lon
        self.max_error_lon = max_error_lon
        self.min_error_lat = min_error_lat
        self.max_error_lat = max_error_lat
        self.hide_driver = hide_driver

    def go2query(self,download_folder):

        if os.path.isdir(download_folder) == False:
            os.makedirs(download_folder)

        _, _, filenames = next(os.walk(download_folder))
        for filename in filenames:
            try:    os.remove(  os.path.join(download_folder, filename)   )  
            except: pass  

        link = 'http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/consultaexperta.php'
        options, profile = get_web_preferences(download_folder=download_folder,hide=self.hide_driver)

        driver = webdriver.Firefox(options=options, firefox_profile=profile)
        driver.set_window_size(1800, 1200) #For a correct size for the screenshot
        driver.get(link)

        select_day(driver,"inicial",str(self.min_date.year),
                str(self.min_date.strftime("%b")),str(self.min_date.day))
        select_day(driver,"final",str(self.max_date.year),
                str(self.max_date.strftime("%b")),str(self.max_date.day))

        def send_key_to_container_main(driver,id,value):
            if value != None:
                driver.find_element_by_xpath(f'//*[@id="{id}"]').clear()
                driver.find_element_by_xpath(f'//*[@id="{id}"]').send_keys(str(value))

        driver.find_element_by_xpath('//*[@id="container-main"]/table[1]/tbody/tr/td/form/div').click()
        driver.find_element_by_xpath('//*[@id="ubi-l"]').click()
        send_key_to_container_main(driver,"longitudStart",self.min_lon)
        send_key_to_container_main(driver,"longitudEnd",self.max_lon)
        send_key_to_container_main(driver,"latitudStart",self.min_lat)
        send_key_to_container_main(driver,"latitudEnd",self.max_lat)
        send_key_to_container_main(driver,"magnitudStart",self.min_mag)
        send_key_to_container_main(driver,"magnitudEnd",self.max_mag)
        send_key_to_container_main(driver,"depthStart",self.min_depth)
        send_key_to_container_main(driver,"depthEnd",self.max_depth)
        send_key_to_container_main(driver,"rmsStart",self.min_RMS)
        send_key_to_container_main(driver,"rmsEnd",self.max_RMS)
        send_key_to_container_main(driver,"gapStart",self.min_gap)
        send_key_to_container_main(driver,"gapEnd",self.max_gap)
        send_key_to_container_main(driver,"eprofmin",self.min_error_depth)
        send_key_to_container_main(driver,"eprofmax",self.max_error_depth)
        send_key_to_container_main(driver,"elongmin",self.min_error_lon)
        send_key_to_container_main(driver,"elongmax",self.max_error_lon)
        send_key_to_container_main(driver,"elatmin",self.min_error_lat)
        send_key_to_container_main(driver,"elatmax",self.max_error_lat)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        starttime =  get_day(driver,'inicial')
        endtime =  get_day(driver,'final')

        driver.find_element_by_xpath('//*[@id="container-main"]/table[2]/tbody/tr/td/div/input').click()
        # time.sleep(3)

        result_text = driver.find_element_by_xpath(f'//*[@id="example_info"]').text
        result = int(result_text.split(" ")[-2])
        
        if result == 0:
            pass
        else:
            excel= driver.find_element_by_link_text("Generar Excel").click()
            # print("\nexcel ################################ 100%")
            printlog("info","excel","ok")
            kml= driver.find_element_by_link_text("Generar KML").click()
            # print("kml   ################################ 100%")
            printlog("info","kml","ok")
            mapa= driver.find_element_by_link_text("Ver Mapa Sismicidad").click()
            time.sleep(3)
            driver.save_screenshot(os.path.join(download_folder,'Reporte_Sismicidad.png'))
            # print("png   ################################ 100% \n")
            printlog("info","png","ok")
        
        resultados = {"sismos":result,"fecha_inicial":starttime,"fecha_final":endtime}

        filepaths = mv_downloaded_files(download_folder)
        resultados["archivos_descargados"] = filepaths


        printlog("info","resultados","Información del navegador: "+f"{resultados['sismos']}")
        printlog("info","resultados","Información del navegador: "+f"{resultados['fecha_inicial']}")
        printlog("info","resultados","Información del navegador: "+f"{resultados['fecha_final']}")
        return resultados

class RadialQuery(object):
    def __init__(self,min_date,max_date,lon=-76,lat=5,radius=100,min_mag=0,max_mag=9,
                min_depth=0,max_depth=700,min_RMS=0,max_RMS=10,
                min_gap=0,max_gap=360,min_error_depth=0,
                max_error_depth=999,min_error_lon=0,max_error_lon=999,
                min_error_lat=0,max_error_lat=999,hide_driver= False):
        
        self.type = "radial"
        self.min_date = min_date
        self.max_date = max_date
        self.lon = lon
        self.lat = lat
        self.radius = radius
        self.min_mag = min_mag
        self.max_mag = max_mag
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.min_RMS = min_RMS
        self.max_RMS = max_RMS
        self.min_gap = min_gap
        self.max_gap = max_gap
        self.min_error_depth = min_error_depth
        self.max_error_depth = max_error_depth
        self.min_error_lon = min_error_lon
        self.max_error_lon = max_error_lon
        self.min_error_lat = min_error_lat
        self.max_error_lat = max_error_lat
        self.hide_driver = hide_driver

    def go2query(self,download_folder):

        if os.path.isdir(download_folder) == False:
            os.makedirs(download_folder)

        _, _, filenames = next(os.walk(download_folder))
        for filename in filenames:
            try:    os.remove(  os.path.join(download_folder, filename)   )  
            except: pass  

        link = 'http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/consultaexperta.php'
        options, profile = get_web_preferences(download_folder=download_folder,hide=self.hide_driver)

        driver = webdriver.Firefox(options=options, firefox_profile=profile)
        driver.set_window_size(1800, 1200) #For a correct size for the screenshot
        driver.get(link)

        select_day(driver,"inicial",str(self.min_date.year),
                str(self.min_date.strftime("%b")),str(self.min_date.day))
        select_day(driver,"final",str(self.max_date.year),
                str(self.max_date.strftime("%b")),str(self.max_date.day))

        def send_key_to_container_main(driver,id,value):
            if value != None:
                driver.find_element_by_xpath(f'//*[@id="{id}"]').clear()
                driver.find_element_by_xpath(f'//*[@id="{id}"]').send_keys(str(value))

        driver.find_element_by_xpath('//*[@id="container-main"]/table[1]/tbody/tr/td/form/div').click()
        driver.find_element_by_xpath('//*[@id="ubi-e"]').click()
        send_key_to_container_main(driver,"longitudCentral",self.lon)
        send_key_to_container_main(driver,"latitudCentral",self.lat)
        send_key_to_container_main(driver,"radio",self.radius)
        send_key_to_container_main(driver,"magnitudStart",self.min_mag)
        send_key_to_container_main(driver,"magnitudEnd",self.max_mag)
        send_key_to_container_main(driver,"depthStart",self.min_depth)
        send_key_to_container_main(driver,"depthEnd",self.max_depth)
        send_key_to_container_main(driver,"rmsStart",self.min_RMS)
        send_key_to_container_main(driver,"rmsEnd",self.max_RMS)
        send_key_to_container_main(driver,"gapStart",self.min_gap)
        send_key_to_container_main(driver,"gapEnd",self.max_gap)
        send_key_to_container_main(driver,"eprofmin",self.min_error_depth)
        send_key_to_container_main(driver,"eprofmax",self.max_error_depth)
        send_key_to_container_main(driver,"elongmin",self.min_error_lon)
        send_key_to_container_main(driver,"elongmax",self.max_error_lon)
        send_key_to_container_main(driver,"elatmin",self.min_error_lat)
        send_key_to_container_main(driver,"elatmax",self.max_error_lat)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        starttime =  get_day(driver,'inicial')
        endtime =  get_day(driver,'final')

        driver.find_element_by_xpath('//*[@id="container-main"]/table[2]/tbody/tr/td/div/input').click()
        # time.sleep(3)

        result_text = driver.find_element_by_xpath(f'//*[@id="example_info"]').text
        result = int(result_text.split(" ")[-2])
        
        if result == 0:
            pass
        else:
            excel= driver.find_element_by_link_text("Generar Excel").click()
            # print("\nexcel ################################ 100%")
            printlog("info","excel","ok")
            kml= driver.find_element_by_link_text("Generar KML").click()
            # print("kml   ################################ 100%")
            printlog("info","kml","ok")
            mapa= driver.find_element_by_link_text("Ver Mapa Sismicidad").click()
            time.sleep(3)
            driver.save_screenshot(os.path.join(download_folder,'Reporte_Sismicidad.png'))
            # print("png   ################################ 100% \n")
            printlog("info","png","ok")

        resultados = {"sismos":result,"fecha_inicial":starttime,"fecha_final":endtime}


        filepaths = mv_downloaded_files(download_folder)
        resultados["archivos_descargados"] = filepaths

        printlog("info","resultados","Información del navegador: "+f"{resultados['sismos']}")
        printlog("info","resultados","Información del navegador: "+f"{resultados['fecha_inicial']}")
        printlog("info","resultados","Información del navegador: "+f"{resultados['fecha_final']}")

        return resultados

class LinkedQuery(object):
    def __init__(self,link,hide_driver=False):
        self.link = link
        self.hide_driver= hide_driver

    def go2query(self,download_folder):

        if os.path.isdir(download_folder) == False:
            os.makedirs(download_folder)

        _, _, filenames = next(os.walk(download_folder))
        for filename in filenames:
            try:    os.remove(  os.path.join(download_folder, filename)   )  
            except: pass  

        options, profile = get_web_preferences(download_folder=download_folder,hide=self.hide_driver)

        driver = webdriver.Firefox(options=options, firefox_profile=profile)
        driver.set_window_size(1800, 1200) #For a correct size for the screenshot
        driver.get(self.link)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        starttime =  get_day(driver,'inicial')
        endtime =  get_day(driver,'final')

        driver.find_element_by_xpath("//input[@type='submit' and @value='Consultar']").click()

        result_text = driver.find_element_by_xpath(f'//*[@id="example_info"]').text
        result = int(result_text.split(" ")[-2])
        
        if result == 0:
            pass
        else:
            excel= driver.find_element_by_link_text("Generar Excel").click()
            # print("\nexcel ################################ 100%")
            printlog("info","excel","ok")
            kml= driver.find_element_by_link_text("Generar KML").click()
            # print("kml   ################################ 100%")
            printlog("info","kml","ok")
            mapa= driver.find_element_by_link_text("Ver Mapa Sismicidad").click()
            time.sleep(3)
            driver.save_screenshot(os.path.join(download_folder,'Reporte_Sismicidad.png'))
            # print("png   ################################ 100% \n")
            printlog("info","png","ok")

        print((starttime,"-",endtime))
        print(result, "sismos")
        resultados = {"sismos":result,"fecha_inicial":starttime,"fecha_final":endtime}

        filepaths = mv_downloaded_files(download_folder)
        resultados["archivos_descargados"] = filepaths
        

        printlog("info","resultados","Información del navegador: "+f"sismos->{resultados['sismos']}")
        printlog("info","resultados","Información del navegador: "+f"fecha_inicial -> {resultados['fecha_inicial']}")
        printlog("info","resultados","Información del navegador: "+f"fecha_fina -> {resultados['fecha_final']}")
        return resultados

def get_last_day(str_day):
    fecha = str_day.upper()
    cdays= {'L':calendar.MONDAY,'M':calendar.TUESDAY,'W':calendar.WEDNESDAY,
            'J':calendar.THURSDAY,'V':calendar.FRIDAY,'S':calendar.SATURDAY,
            'D':calendar.SUNDAY}

    last_day = dt.date.today()
    oneday = dt.timedelta(days=1)
    while last_day.weekday() != cdays[fecha]:
        last_day -= oneday
        
    return last_day

def prepare_report(busqueda):
    correo_folder_path = os.path.join(os.getcwd(),"correos",busqueda['nombre'].lower())
    template_folder_path = os.path.join(os.getcwd(),"correos","template")
    archivo_folder_path = os.path.join(os.getcwd(),"archivos",busqueda['nombre'].lower())
    reportes_path = os.path.join(os.getcwd(),"reportes",busqueda['nombre'].lower()+".json")


    if os.path.isfile(reportes_path ) == True and (busqueda["guardado"] in ("no","No","NO")):

        while True:
            printlog("warning","Reporte",f"El nombre {busqueda['nombre']} ya fue creado. Quiere sobrescribir la informacion")
            print(u"\n "+" 1[si]    2[no]"+"\n ")
            seguro = input()

            if seguro == "1":
                os.system(f"rm -r  {correo_folder_path} {archivo_folder_path} {reportes_path}")
                break
            if seguro == "2":
                sys.exit()
            else:
                pass
    elif os.path.isfile(reportes_path ) == True and (busqueda["guardado"] in ("si","SI","Si")):
        return None
    elif os.path.isfile(reportes_path ) == False and (busqueda["guardado"] in ("si","SI","Si")):
        raise Exception(f"No tiene creado un reporte con el nombre {busqueda['nombre']}")
    else :
        seguro = "1"

    for folder_path in [correo_folder_path,archivo_folder_path]:
        if os.path.isdir(folder_path) == False:
            os.makedirs(folder_path)   

    if seguro == '1':
        if busqueda["type"] == "cuadrante":
            no_copiar = "mensaje_radial.html"
        if busqueda["type"] == "radial":
            no_copiar = "mensaje_cuadrante.html"


        ## copiar archivos de la carpeta correo
        msg = "cp"
        for dp, dn, filenames in os.walk(template_folder_path):
            for f in filenames:
                if f != no_copiar  :
                    template_file = os.path.join(dp, f)
                    msg += f" {template_file}"

        msg += f" {correo_folder_path}"

    
        # print(msg)
        printlog("debug","Guardar Reporte",msg)
        os.system(msg)
        tojson = busqueda.copy()
        tojson["fecha_inicial"] = tojson["fecha_ini"]
        tojson["fecha_final"] = tojson["fecha_fin"]
        with open(reportes_path,"w") as jsonfile:
            json.dump([tojson], jsonfile)

def email( busqueda,resultados):
    """
    Parametros:
    -----------
    busqueda: dict
        Diccionario del objeto busqueda.
    resultados: dict
        Resutlados de la busqueda

    Returns:
    --------
    Enviar correo
    """

    printlog("info","Correo","Alistando parametros para enviar email")
    asunto = busqueda["asunto"]
    destinatarios = busqueda["destinatarios"]
    filenames = list(map(lambda x: os.path.basename(x),resultados["archivos_descargados"]))

    #paths
    files_folder_path = os.path.join(os.getcwd(),'archivos', busqueda['nombre'].lower())
    emails_folder_path = os.path.join(os.getcwd(),'correos', busqueda['nombre'].lower())
    json_path = os.path.join(os.getcwd(),'reportes', busqueda['nombre'].lower()+".json")

    remitente_path = os.path.join(emails_folder_path, 'remitente.txt')
    problema_path = os.path.join(emails_folder_path, 'problema.html')
    mensaje_path = os.path.join(emails_folder_path,f"mensaje_{busqueda['type'].lower()}.html")
    problema_msg_path = os.path.join(emails_folder_path, 'problema.txt')

    # lee datos del remitente
    # print ('\nPreparando correo...')
    datosr=open( remitente_path,'r' ).readlines()
    remitente = datosr[0] 
    passw= datosr[1]
    
    if int(resultados['sismos']) == 0:
        aclaracion = "No se envian archivos porque no hay sismos para el intervalo de tiempo mencionado."
    else:
        aclaracion = " "


    if asunto in ("Problema","problema"):
        asunto = f"Problema en el reporte: {busqueda['nombre'].lower()}"


        printlog("info","Problema","Desea informar el problema?.")
        while True:
            print("\t1","[si]","    "+ "0","[no]"  )
            p = input()
            if p == "1":
                os.system(f"nano {problema_msg_path}")
                problema= open(problema_msg_path,"r", encoding='utf-8').read()
                mensaje=open( problema_path, encoding='utf-8' ).read()

                mensaje = mensaje%(busqueda['nombre'].lower(),
                                    dt.datetime.now().strftime('%d de %B de %Y a las %H:%M UT'),
                                    problema)
                break
            elif p == "0":
                break
            else:
                pass

    else:
        mensaje=open( mensaje_path).read()

        if busqueda["editar"]:
            printlog("info","Reporte-editar",f"Editando reporte con nano")

            os.system(f"nano {mensaje_path}")


        if busqueda['type'].lower() in ("radial"):
            mensaje = mensaje%(busqueda['radio'],
                               busqueda['lon_central'],
                               busqueda['lat_central'],
                               resultados['fecha_inicial'],
                               resultados['fecha_final'],
                               resultados['sismos'],
                               aclaracion)
        if busqueda['type'].lower() in ("cuadrante"):
            mensaje = mensaje%(busqueda['lat_min'],
                               busqueda['lat_max'],
                               busqueda['lon_min'],
                               busqueda['lon_max'],
                               resultados['fecha_inicial'],
                               resultados['fecha_final'],
                               resultados['sismos'],
                               aclaracion)

    if busqueda["comprobar"]:
        if resultados['sismos'] != 0:
            print("\n")
            printlog("info","Reporte-comprobar",f"Datos de los sismos")
            excel_file= pd.read_excel(   os.path.join( files_folder_path,
                                                f"{busqueda['nombre']}.xlsx"))
            print(excel_file.iloc[:,:4])
            print("\n")

        ast = "#"
        printlog("info","Reporte-comprobar",f"El mensaje es el siguiente:")
        print(f" \n\n{ast*60}\n ")
        print(html2text.html2text(mensaje))
        print(f"\n{ast*60}\n ")

    printlog("info","Correo","Desea enviar correos?") 
    while True:
        print("1","[si]","    "+ "0","[no]"  )
        p = input()
        if p == "1": 
            break   
        elif p== "0":
            asunto = f"Problema en el reporte: {busqueda['nombre'].lower()}"
            printlog("info","Problema","Desea informar el problema?.")
            while True:
                print("\t1","[si]","    "+ "0","[no]"  )
                c = input()
                if credits == "1":
                    os.system(f"nano {problema_msg_path}")
                    problema= open(problema_msg_path,"r", encoding='utf-8').read()
                    mensaje=open( problema_path, encoding='utf-8' ).read()

                    mensaje = mensaje%(busqueda['nombre'].lower(),
                                        dt.datetime.now().strftime('%d de %B de %Y a las %H:%M UT'),
                                        problema)
                    break
                elif c == "0":
                    break
                else:
                    pass
        else:
            pass


    msg = MIMEMultipart()
    msg['From'] = 'SGC <rsncol@sgc.gov.co>'
    msg['Subject'] = asunto

    if isinstance(destinatarios,list):
        msg['To'] =  ", ".join(destinatarios)
    if isinstance(destinatarios,str):
        msg['To'] =  destinatarios
    
    msg.attach(MIMEText(mensaje, 'html'))
    

    for filename in filenames:
        attachment = open( os.path.join(files_folder_path,  filename),'rb')
        part= MIMEBase('aplication','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= "+filename)   
        msg.attach(part)
        
    server = smtplib.SMTP('smtp.gmail.com:25') 
    server.starttls()
    server.login(remitente,passw)

    
    server.sendmail(remitente, destinatarios, msg.as_string())

    server.quit()

    printlog("info","Correo",f"Correo enviado a: {destinatarios}.\n")


    if busqueda['guardar'] == False:
        json 
        msg = f"rm -r {json_path} {files_folder_path} {emails_folder_path}"
        printlog("debug","Guardar","msg")


if __name__ == "__main__":
    print("archivos utiles para poder hacer busqueda y enviar correos")