import configparser
from sqlalchemy import or_
from modulos.modelo import Ticket
from modulos.modelo import User
from modulos.modelo import TicketThread
from modulos.base import Session

session = Session()

config = configparser.ConfigParser()
config.read("../configuracion.ini")

# usuario_hd = str(config["HELPDESK"]["usuario_hd"])
# clave_hd = str(config["HELPDESK"]["clave_hd"])
# server_db = str(config["HELPDESK"]["server_db"])
# usuario_db = str(config["HELPDESK"]["usuario_db"])
# clave_db = str(config["HELPDESK"]["clave_db"])
dominio_helpdesk = str(config["HELPDESK"]["dominio_helpdesk"])
# database_helpdesk = str(config["HELPDESK"]["database"])
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

def buscaUsuario(usuario):
    if "@" in usuario:
        resultado = session.query(User).filter(User.user_name == usuario).first()
    else:
        resultado = session.query(User).filter(User.id == str(usuario).first()
    return resultado.id, resultado.user_name, resultado.first_name, resultado.last_name, resultado.email, resultado.role

def buscaData(item, dato, estado, relacionado, condicion, usuario):
    # resultado = []
    resultado = ""

    ## pasa los verdaderos estados a la variable nestado y define un estado por defecto
    nestado = 0
    if estado == "abierto": nestado = abierto
    if estado == "cerrado": nestado = cerrado
    if estado == "resuelto": nestado = resuelto
    documento = False

    if dato != "": 
        if relacionado != "": ## varios tickets de un relacionado
            if "@" not in dato: dato = dato + dominio_helpdesk
            relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = buscaUsuario(dato)
        else: ## un solo ticket de un relacionado
            documento = True
    else:
        dato = usuario
        if relacionado != "":
            relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = buscaUsuario(dato)
        else: 
            relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = buscaUsuario(dato)
            if relacionado_rol == "user": 
                relacionado = "cliente"
            else:
                relacionado = "agente"


    if item == "":
        ## informacion de usuarios/clientes/agentes que esta en helpdesk ##
        if "@" not in dato: dato = dato + dominio_helpdesk
        
        if relacionado == "agente":
            filas = session.query(User).filter(User.user_name == usuario).filter(User.role != "user").first()
        else:
            filas = session.query(User).filter(User.user_name == usuario).filter(User.role == "user").first()

        if filas != None:
            resultado = {
                'id':resultado.id,
                'usuario':resultado.user_name,
                'nombre':resultado.first_name,
                'apellido':resultado.last_name,
                'email':resultado.email,
                'activo':resultado.active,
                'extension':resultado.ext,
                'codigoarea':resultado.country_code,
                'telefono':resultado.phone_number,
                'celular':resultado.mobile,
                'departamentoprimario':resultado.primary_dpt,
                'bloqueado':resultado.ban,
                'rol':resultado.role,
                'fotoperfil':resultado.profile_pic,
                'logueado':resultado.is_login,
                'idioma':resultado.user_language                
            }   
        return resultado

    if item == "ticket":
        if documento: 
            if nestado == 0: ## si el dato es un numero de documento y no se especifico estado busca ese solo numero de documento ##
                filas = session.query(Ticket).filter(Ticket.ticket_number == dato).first()
            else: ## busca el documento con el estatus recibido ##
                filas = session.query(Ticket).filter(Ticket.ticket_number == dato).filter(Ticket.status == str(nestado)).first()
        else:
            if nestado == 0: nestado = 1 ## si no se pidio un estatus especifico para el documento se busca con el estatus 1 ##
            if relacionado == "agente":
                if condicion == "sin asignar": 
                    filas = session.query(Ticket).filter(Ticket.assigned_to == None).filter(Ticket.status == str(nestado)).all()
                else:
                    filas = session.query(Ticket).filter(Ticket.assigned_to == str(relacionado_id)).filter(Ticket.status == str(nestado)).all()
            else:
                if condicion == "sin asignar": 
                    filas = session.query(Ticket).filter(Ticket.assigned_to == None).filter(Ticket.user_id == str(relacionado_id)).filter(Ticket.status == str(nestado)).all()
                else:
                    filas = session.query(Ticket).filter(Ticket.assigned_to != None).filter(Ticket.user_id == str(relacionado_id)).filter(Ticket.status == str(nestado)).all()


        if filas != None:
            for registro in filas:
                thread = session.query(TicketThread).filter(TicketThread.ticket_id == registro.id).filter(TicketThread.poster == "client").filter(TicketThread.thread_type == "first_reply").filter(TicketThread.title != None)
                resultado = resultado + "-----------------------*" + "{}".format(registro.ticket_number) + "*-----------------------" + "\n"
                resultado = resultado + "*Titulo:* {}".format(thread.titulo) + "\n"
                resultado = resultado + "*Estado:* {}".format(registro.ticket_statu.name) + " *Prioridad:* {}".format(registro.priority.priority_desc) + "\n"
                # resultado = resultado + "*Tipo:* {}".format(registro["tipo"]) + "\n" 
                resultado = resultado + "*Topico:* {}".format(registro.help_topic.topic) + "\n"
                resultado = resultado + "*SLA:* {}".format(registro.sla_plan.name) + "\n" 
                resultado = resultado + "*Fecha Creacion:* {}".format(registro.created_at) + "\n" 
                resultado = resultado + "*Fecha Vence:* {}".format(registro.duedate) + "\n" 

                if condicion != "sin asignar" and relacionado != "agente":
                    ## busca datos del agente asignado al ticket ##
                    # sql = "SELECT user_name, last_name, first_name, email FROM users WHERE id = " + str(registro["assigned_to"])
                    # asignado = self.ejecutaSql(sql)

                    if registro.assigned_to != None: 
                        resultado = resultado + "----------------------*Asignado A*----------------------" + "\n"
                        resultado = resultado + "*{}".format(registro.dept.name]) + "*" + "\n"
                        resultado = resultado + "*Agente:* {}".format(registro.user1.first_name) + " {}".format(registro.user1.last_name) + "\n"
                        resultado = resultado + "{}".format(registro.user1.email) + "\n" 

        return resultado