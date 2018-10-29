#!/usr/bin/env python3.7
# -*- coding: utf-8 -*- #

import json, requests, logging, unidecode, configparser
from modulos.clases import helpdesk_db, ldap, botdialogflow, helpdesk_api
from datetime import datetime, timedelta
from slackclient import SlackClient
from flask import Flask, request, abort, jsonify
from flask_basicauth import BasicAuth
from modulos.decrypt import desencripta

config = configparser.ConfigParser()
config.read("configuracion.ini")

usuario_hd = str(config["HELPDESK"]["usuario_hd"])
clave_hd = str(config["HELPDESK"]["clave_hd"])
server_db = str(config["HELPDESK"]["server_db"])
usuario_db = str(config["HELPDESK"]["usuario_db"])
clave_db = str(config["HELPDESK"]["clave_db"])
dominio_helpdesk = str(config["HELPDESK"]["dominio_helpdesk"])
database_helpdesk = str(config["HELPDESK"]["database"])
api_ldap_server_url = str(config["API"]["ldap_url"])
api_ldap_server_port = str(config["API"]["ldap_port"])
api_helpdesk_url = str(config["API"]["helpdeskV1_url"])
apiv2_helpdesk_url = str(config["API"]["helpdeskV2_url"])
api_helpdesk_url_authenticate = str(config["API"]["helpdesk_authenticate"])
edialogflow_token = str(config["TOKENS"]["dialogflow_token"])
eslack_bot_token = str(config["TOKENS"]["slack_bot_token"])
dialogflow_project = str(config["TOKENS"]["dialogflow_project"])
main_token = str(config["TOKENS"]["main_token"])

slack_bot_token = desencripta(main_token, eslack_bot_token).decode('utf-8')
dialogflow_token = desencripta(main_token, edialogflow_token).decode('utf-8')

# instantiate Slack client
slack_client = SlackClient(slack_bot_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
# starterbot_id = None

logging.basicConfig(filename='logs/notificaciones.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Faveo Notifiaciones Iniciando....')

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

WEBHOOK_VERIFY_TOKEN = None
CLIENT_AUTH_TIMEOUT = 24 # in Hours

app = Flask(__name__)
cHelpDesk_db = helpdesk_db(server=server_db,usuario=usuario_db,clave=clave_db,database=database_helpdesk, dominio=dominio_helpdesk)
cLdap = ldap(server=api_ldap_server_url,port=api_ldap_server_port)
cBotDialogflow = botdialogflow(project_id=dialogflow_project, idioma='es')

authorised_clients = {}

basic_auth = BasicAuth(app)

def slack_msq(user, mensaje):
    slack_client.rtm_connect(with_team_state=False)
    # starterbot_id = slack_client.api_call("auth.test")["user_id"]
    usuarios = slack_client.api_call("users.list")
    id_usuario = "UBRA74MQQ"
    # print(json.dumps(slack_client.api_call("channels.list",exclude_archived=1), indent=4, sort_keys=True))
    # print(json.dumps(usuarios, indent=4, sort_keys=True))
    for usuario in usuarios["members"]:
        if "email" in usuario["profile"]:
            if usuario["profile"]["email"] == user:
                id_usuario = usuario["id"]
                # if "phone" in usuario["profile"]: telefono = usuario["profile"]["phone"]

    slack_client.api_call(
        "chat.postMessage",
        text=mensaje,
        channel=id_usuario
    )

    return mensaje

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    if request.method == 'POST':
        # verify_token = request.headers.get('token')

        # print(verify_token)

        # if verify_token != dialogflow_token: 
        #     logging.info('Sesion addr: {}'.format(request.remote_addr) + ' {}'.format('bad token'))
        #     return jsonify({'status':'bad token'}), 401

        solicitud_str = json.dumps(request.form.to_dict())
        solicitud = json.loads(solicitud_str)

        if solicitud["event"] == "ticket_assigned" and "ticket[assigned_to]" in solicitud: 
            relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = cHelpDesk_db.buscaUsuario(solicitud["ticket[assigned_to]"])
            mensaje = "Hola " + relacionado_nombre + "\n"
            mensaje = mensaje + "El siguiente ticket te ha sido asignado: \n"
            mensaje = mensaje + cHelpDesk_db.buscaData("ticket", solicitud["ticket[ticket_number]"], "", "", "", relacionado_usuario)
            dummy = slack_msq(relacionado_usuario , mensaje)
            logging.info('Asignacion del ticket: {}'.format(solicitud["ticket[ticket_number]"]) + " al agente {}".format(relacionado_nombre) + " {}".format(relacionado_apellido) + " {}".format(relacionado_id) + " {}".format(relacionado_email) + " {}".format(relacionado_rol))

        return jsonify(webhook_ok="Recibido"),200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
