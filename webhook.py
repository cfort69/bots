import os, json,requests, logging
from urllib.parse import parse_qs
from modulos.clases import ldap
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify
from flask_basicauth import BasicAuth
from modulos.decrypt import desencripta
from modulos.funciones import buscaData

logging.basicConfig(filename='logs/webhook.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# WEBHOOK_VERIFY_TOKEN = None
# CLIENT_AUTH_TIMEOUT = 24 # in Hours

app = Flask(__name__)
# cHelpDesk_db = helpdesk_db(server=server_db,usuario=usuario_db,clave=clave_db,database=database_helpdesk, dominio=dominio_helpdesk)
# cLdap = ldap(server=api_ldap_server_url,port=api_ldap_server_port)

authorised_clients = {}

basic_auth = BasicAuth(app)

# @app.before_request
# def before_request():
#     g.data = request.get_json() or request.values or request.data

@app.route('/webhook', methods=['GET', 'POST'])
# @basic_auth.required
def webhook():
    # if request.method == 'POST':
    #     verify_token = request.args.get('verify_token')
    #     if verify_token == WEBHOOK_VERIFY_TOKEN:
    #         authorised_clients[request.remote_addr] = datetime.now()
    #         return jsonify({'status':'success'}), 200
    #     else:
    #         return jsonify({'status':'bad token'}), 401

    # elif request.method == 'POST':
    #     client = request.remote_addr
    #     if client in authorised_clients:
    #         if datetime.now() - authorised_clients.get(client) > timedelta(hours=CLIENT_AUTH_TIMEOUT):
    #             authorised_clients.pop(client)
    #             return jsonify({'status':'authorisation timeout'}), 401
    #         else:



    if request.method == 'POST':
        verify_token = request.headers.get('token')

        if verify_token != dialogflow_token: 
            logging.info('Sesion addr: {}'.format(request.remote_addr) + ' {}'.format('bad token'))
            return jsonify({'status':'bad token'}), 401


        # authorised_clients[request.remote_addr] = datetime.now()
        # print(authorised_clients)
        # solicitud = request.json
        # solicitud = request.data
        # solicitud = request.form
        # logging.info('Sesion addr: {}'.format(request.remote_addr) + ' {}'.format(solicitud))
        estado = ""
        accion = ""
        dato = ""
        item = ""
        contexto = False
        usuario = ""

        solicitud = request.json
        respuesta = solicitud["queryResult"]["fulfillmentText"]

        print(json.dumps(solicitud, indent=4, sort_keys=True))

        # parametro = solicitud["queryResult"]["action"]
        if "outputContexts" in solicitud["queryResult"]: contexto = True
        if "payload" in solicitud: usuario = solicitud["originalDetectIntentRequest"]["payload"]["usuario"]

        if contexto == True:
            accion = solicitud["queryResult"]["outputContexts"][0]["parameters"]["accion"]
            dato = solicitud["queryResult"]["outputContexts"][0]["parameters"]["dato"]
            item = solicitud["queryResult"]["outputContexts"][0]["parameters"]["item"]
            relacionado = solicitud["queryResult"]["outputContexts"][0]["parameters"]["relacionado"]
            estado = solicitud["queryResult"]["outputContexts"][0]["parameters"]["estado"]
            condicion = solicitud["queryResult"]["outputContexts"][0]["parameters"]["condicion"]
            # email = solicitud["queryResult"]["outputContexts"][0]["parameters"]["email"]
        else:
            accion = solicitud["queryResult"]["parameters"]["accion"]
            dato = solicitud["queryResult"]["parameters"]["dato"]
            item = solicitud["queryResult"]["parameters"]["item"]
            relacionado = solicitud["queryResult"]["parameters"]["relacionado"]
            estado = solicitud["queryResult"]["parameters"]["estado"]
            condicion = solicitud["queryResult"]["parameters"]["condicion"]
            # email = solicitud["queryResult"]["parameters"]["email"]

        session = solicitud["session"]


        ## acciones a ejecutar ##

        # if accion == "asigna"

        # print(accion + " " + dato + " " + item + " " + persona + " " + estado)
        # respuesta = cHelpDesk_db.buscaData(item, dato, estado, persona)
        # print(respuesta)

        # if accion == "desbloqueo":
        #     datos = cHelpDesk_db.buscaData(item, dato, estado, relacionado, condicion, usuario)
        #     respuesta = cLdap.desbloqueaUsuario(dato, datos["nombre"], datos["apellido"], session)
        
        if accion == "informacion": 
            datos = buscaData(item, dato, estado, relacionado, condicion, usuario)
            if datos != "":
                # if relacionado == "agente":
                #     datos = cHelpDesk_db.buscaData(item, dato, estado, relacionado, condicion, usuario)
                if item == "":
                    # respuesta = cLdap.infoUsuario(dato, datos["nombre"], datos["apellido"], session)
                    # respuesta = respuesta + "\n" + "Extension: " + datos["extension"] + " Celular: " + str(datos["codigoarea"]) + str(datos["celular"])
                    respuesta = "datos de usuario"
                else:
                    respuesta = datos

        return jsonify(fulfillmentText=respuesta),200

            # logging.info('Sesion addr: {}'.format(request.remote_addr) + ' {}'.format(respuesta))



            # return jsonify(fulfillmentText=respuesta),200

        # return jsonify(fulfillmentText="lo siento no puedo ayudarte con eso"),200
        # return jsonify({'status':'success'}), 200

        # else:
        #     return jsonify({'status':'bad token'}), 401

    # accion = request.json["result"]["parameters"]["accion"]


    # if accion == "informar": 
    #     resultado = comando_info(request.json["result"]["parameters"]["usuario"])
    #     print(resultado)
    #     return resultado




    # json_string = json.dumps(request.json, indent=4, sort_keys=True)
    # print(json_string)
    # print(request.json["queryResult"]["parameters"]["accion"])
    # print(request.json["queryResult"]["parameters"]["usuario"])
    # print(json_string)

    # return jsonify(fulfillmentText="This is a text response"),200
    #     else:
    #         return jsonify({'status':'not authorised'}), 401

    # else:
    #     abort(400)'


if __name__ == '__main__':
    # if WEBHOOK_VERIFY_TOKEN is None:
    #     print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
    #     token = temp_token()
    #     print('Token: %s' % token)
    #     WEBHOOK_VERIFY_TOKEN = token

    app.run(host='0.0.0.0')
