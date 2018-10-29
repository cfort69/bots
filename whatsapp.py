import os, sys, json, unidecode, time, requests, logging
from modulos.clases import helpdesk_db, ldap, botdialogflow, helpdesk_api
from datetime import datetime, timedelta
from modulos.configuracion import server_helpdesk, usuario_helpdesk, clave_helpdesk, database_helpdesk, api_ldap_server_url, \
    api_ldap_server_port, id_whatsapp_soporte ,dominio_helpdesk, bot_name, \
    usuario_helpdesk, clave_helpdesk, server_helpdesk, database_helpdesk, dialogflow_project
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage

## Que puede hacer el bot ##
logging.basicConfig(filename='logfile.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('PCBot WhatsApp_Bot Iniciando....')


try:
   os.environ["SELENIUM"]
except KeyError:
   print ("Please set the environment variable SELENIUM to Selenium URL")
   sys.exit(1)

## Carga Driver y conecta con Whatsapp Web ##
driver = WhatsAPIDriver(client='remote', command_executor=os.environ["SELENIUM"]) #, profile='/home/aplicaciones/.mozilla/firefox/81yyy19w.whatsapp')
status = driver.get_status()
if status == "NotLoggedIn" or status == "Unknown":
    logging.info('No esta logueado')
    driver.get_qr()
    logging.info('Esperando codigo QR')
    driver.wait_for_login()
else:
    logging.info('Ya esta logueado')
# driver.save_firefox_profile(remove_old=True)

## Driver subio, carga diccionarios internos ##
# driver.send_message_to_id(id_whatsapp_soporte,'Bot Iniciando....')
# logging.info('Actualizacion inicial data helpdesk iniciada....')
# driver.send_message_to_id(id_whatsapp_soporte,'Actualizacion data helpdesk iniciada....')
# apphd = helpdesk(usuario=api_helpdesk_usuario, clave=api_helpdesk_clave, authenticate_url=api_helpdesk_url_authenticate)
# data_helpdesk = apphd.maestros(api_helpdesk_url)
# logging.info('Actualizacion inicial data helpdesk terminada....')
# driver.send_message_to_id(id_whatsapp_soporte,'Actualizacion data helpdesk terminada....')
logging.info('PCBot WhatsApp_Bot Arriba')
# driver.send_message_to_id(id_whatsapp_soporte, 'PCBot WhatsApp_Bot Arriba')

cHelpDesk = helpdesk(server=server_helpdesk,usuario=usuario_helpdesk,clave=clave_helpdesk,database=database_helpdesk, dominio=dominio_helpdesk)
cLdap = ldap(server=api_ldap_server_url,port=api_ldap_server_port)
cBotDialogflow = botdialogflow(project_id=dialogflow_project, idioma='es')

while True:
    time.sleep(1)

    # print ('Checking for more messages, status', driver.get_status())
    for contact in driver.get_unread():
        for message in contact.messages:

            ## Celular de quien chatea ##
            # celular_completo = message.sender.id
            # celular = celular_completo[1:celular_completo.find('@')]
            celular_completo = message.sender.id
            celular = celular_completo[1:len(celular_completo)]

            if message.type == 'chat':
                logging.info('Mensaje recibido de :{}'.format(message.sender.id) + ' {}'.format(message.content))

                respuesta = cBotDialogflow.buscaIntent(message.sender.id, message.content.encode('utf-8'))

                logging.info('Respuesta: {}'.format(respuesta))
                driver.send_message_to_id(message.sender.id, respuesta)


                # driver.send_message_to_id(message.sender.id, respuesta)
                # driver.send_message(respuesta)
                # driver.send_message_to_id(message.sender.id, respuesta

            # print(json.dumps(message.get_js_obj(), indent = 4))
            # print 'class', message.__class__.__name__
            # print 'message', message
            # print 'id', message.id
            # print 'type', message.type
            # print 'timestamp', message.timestamp
            # print 'chat_id', message.chat_id
            # print 'sender', message.sender
            # print 'sender.id', message.sender.id
            # print 'sender.safe_name', message.sender.get_safe_name()


            # elif message.type == 'image' or message.type == 'video' :
            #     print ('-- Image or Video')
            #     print ('filename', message.filename)
            #     print ('size', message.size)
            #     print ('mime', message.mime)
            #     print ('caption', message.caption)
            #     print ('client_url', message.client_url)
            #     message.save_media('./')
            # else:
            #     print ('-- Other')
