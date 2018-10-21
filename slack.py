#!/usr/bin/env python3.7
# -*- coding: utf-8 -*- #

import os, json, unidecode, time, re, sys, requests, logging, configparser
from modulos.clases import helpdesk_db, ldap, botdialogflow, helpdesk_api
from datetime import datetime, timedelta
from slackclient import SlackClient
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
starterbot_id = None

logging.basicConfig(filename='logs/slack.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Botler Slack Iniciando....')

# cHelpDesk = helpdesk(server=server_helpdesk,usuario=usuario_helpdesk,clave=clave_helpdesk,database=database_helpdesk, dominio=dominio_helpdesk)
# cLdap = ldap(server=api_ldap_server_url,port=api_ldap_server_port)
cBotDialogflow = botdialogflow(project_id=dialogflow_project, idioma='es')

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events, usuarios):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            # user_id, message = parse_direct_mention(event["text"])
            for usuario in usuarios["members"]:
                if usuario["id"] == event["user"]:
                    nombrecompleto = usuario["profile"]["real_name_normalized"]
                    nombre = usuario["profile"]["first_name"]
                    apellido = usuario["profile"]["last_name"]
                    email = usuario["profile"]["email"]
                    telefono = usuario["profile"]["phone"]

            message = event["text"]
            # print(usuario["id"])
            # if user_id == starterbot_id:
            #     return message, event["channel"]
            # else:
            return message, event["channel"], event["user"], nombrecompleto, nombre, apellido, email, telefono
    return None, None, None, None,None, None,None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(mensaje, channel, email, nombre, apellido):

    # Default response is help text for the user
    # default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!

    # texto = mensaje.encode('utf-8') + " " + email.encode('utf-8')
    # usuario = email.find("@")
    # texto = mensaje + " " + email
    print(mensaje)

    logging.info('Mensaje recibido de :{}'.format(channel) + ' {}'.format(mensaje))

    response = cBotDialogflow.buscaIntent(channel, mensaje, email)

    logging.info('Respuesta: {}'.format(response.encode('utf-8')))

    # if command.startswith(EXAMPLE_COMMAND):
    #     response = "Sure...write some more code then I can do that!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Botler Conectado!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        usuarios = slack_client.api_call("users.list")
        while True:
            # print(slack_client.rtm_read())

            mensaje, channel, usuario, nombrecompleto, nombre, apellido, email, telefono = parse_bot_commands(slack_client.rtm_read(), usuarios)
            if mensaje:
                handle_command(mensaje, channel, email, nombre, apellido)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Error de coneccion.")

