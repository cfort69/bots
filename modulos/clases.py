import requests, json, logging, unidecode, pymysql, pymysql.cursors, configparser
import dialogflow_v2 as dialogflow
from google.protobuf import struct_pb2


config = configparser.ConfigParser()
config.read("configuracion.ini")
abierto = config["HELPDESK"]["abierto"] 
cerrado = config["HELPDESK"]["cerrado"]
resuelto = config["HELPDESK"]["resuelto"]

# logging.basicConfig(filename='logfile.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class botdialogflow:
    def __init__(self, project_id, idioma):
        self.project_id = project_id
        self.idioma = idioma
        # self.session_id = session_id

    def declaraSesion(self,sesion_id):
        sesion_df= dialogflow.SessionsClient()
        sesion = sesion_df.session_path(self.project_id, sesion_id)
        logging.info('Sesion dialogflow: {}'.format(sesion))
        return sesion, sesion_df
    
    def buscaIntent(self, sesion_id, texto, usuario):
        sesion, sesion_df = self.declaraSesion(sesion_id)
        parameters_payload = struct_pb2.Struct()
        text_input = dialogflow.types.TextInput(text=texto, language_code=self.idioma)
        parameters_payload["usuario"] = usuario 
        query_input = dialogflow.types.QueryInput(text=text_input)
        query_parameters = dialogflow.types.QueryParameters(payload=parameters_payload)
        respuesta = sesion_df.detect_intent(session=sesion, query_input=query_input, query_params=query_parameters)
        return respuesta.query_result.fulfillment_text

class ldap:
    def __init__(self, server,port):
        self.server = server
        self.port = port

    def infoUsuario(self, user, nombre, apellido, solicitante):
        logging.info(solicitante + ' pidio info sobre: ' + user.strip())

        api_url = self.server + ":" + self.port + "/user/" + user.strip()
        result = requests.get(api_url)
        response = result.json()
        resultado = ""
        if 'displayName' in response:
            resultado = "*" + response["displayName"] + "*" + '\n' 
        if 'description' in response:
            resultado = resultado + response["description"] + '\n' 
        if 'mail' in response:
            resultado = resultado + response["mail"] + '\n' 
        if 'employeeID' in response:
            resultado = resultado + "Empleado: " + response["employeeID"]
        if resultado == "":
            resultado = "No encuentro al usuario " + user.encode("utf-8") +'\n' + "recuerda que debes pasarme el usuario y no el nombre o el apellido de la persona"

        logging.info(solicitante + ' informacion encontrada: ' + resultado)
        return resultado

    def desbloqueaUsuario(self, user, nombre, apellido, solicitante):
        logging.info(solicitante + ' pidio desbloquear a: ' + user.strip())

        api_url = self.server + ":" + self.port + "/user/" + user.strip() + "/unlock"
        result = requests.put(api_url)

        if result.status_code == 200:
            resultado = "Usuario *" + nombre.capitalize() + " " + apellido.capitalize() + "* desbloqueado"
        else:
            resultado = "Usuario *" + nombre.capitalize() + " " + apellido.capitalize() + "* no encontrado " + str(result.status_code)

        logging.info(solicitante + ' resultado: ' + resultado)
        return resultado


class sap:
    def __init__(self, credentials):
        self.credentials = credentials

    def new_session(self):
        ses = requests.Session()
        ses.headers.update(
            {'Authorization': self.credentials,
             'Content-type': 'application/json'})
        return ses

    def get_token(self, url, session):
        session.headers.update({'X-CSRF-Token': 'Fetch'})
        resp = session.get(url)
        token = resp.headers.get('x-csrf-token')
        return token

    def authenticate(self, url, session):
        token = self.get_token(url, session)
        session.headers.update({'X-CSRF-Token': token})

    def get_url(self, url):
        ses = self.new_session()
        resp = ses.get(url)
        print(resp.json())

    def post_url(self, url, data):
        ses = self.new_session()
        self.authenticate(url, ses)
        resp = ses.post(url, data=json.dumps(data))
        return resp.json()

    def test_fact(self, url, data):
        data = self.post_url(url, data)
        print('\nImprimiento Lista servicios..\n')
        print (json.dumps(data, indent=4, sort_keys=True))

class helpdesk_api: ## clase para insertar on modificar registros en helpdesk via el api de faveo ##
    def __init__(self,usuario,clave,authenticate_url):
        self.usuario = usuario
        self.clave = clave
        self.authenticate_url = authenticate_url
        # self.ses = requests.Session()

    def new_session(self):
        ses = requests.Session()
        # ses.data.update("usuario=" + self.usuario + "&" + "clave=" + self.clave)
        return ses

    def get_token(self, url, session):
        payload = "username=" + self.usuario +  "&password=" + self.clave
        resp = session.post(url, params=payload)
        # resp = self.ses.post(url, params=payload)
        return resp.json()["data"]["token"]


    def get_url(self, url, valor):
        ses = self.new_session()
        if valor == "None":
            payload = "token=" + self.get_token(self.authenticate_url, ses)
        else:
            payload = valor + "&token=" + self.get_token(self.authenticate_url, ses)
        resp = ses.get(url, params=payload)
        # print(url + "  " + payload)
        return resp.json()

    def post_url(self, url, data):
        ses = self.new_session()
        
        if data != None:
            payload = "token=" + self.get_token(self.authenticate_url, ses) + data
            resp = ses.post(url, params=payload)
        else:
            payload = "token=" + self.get_token(self.authenticate_url, ses)
            resp = ses.post(url, params=payload)
        return resp.json()

class helpdesk_db: ## clase para hacer todas las consultas en db del helpdesk ##
    def __init__(self,server,usuario,clave, database, dominio):
        self.server_db = server
        self.usuario_db = usuario
        self.clave_db = clave
        self.database = database
        self.dominio = dominio
        self.conn = None

    def abreConeccion(self):
        if(self.conn is None):
            coneccion = pymysql.Connect(host=self.server_db, user=self.usuario_db,passwd=self.clave_db, db=self.database,cursorclass=pymysql.cursors.DictCursor)
            return coneccion
        # elif (not self.conn.open):
        #     coneccion = MySQLdb.Connect(host=self.server, user=self.usuario,passwd=self.clave, db=self.database,cursorclass=MySQLdb.cursors.DictCursor)            
        # return coneccion

    def ejecutaSql(self, sql):
        coneccion = self.abreConeccion()
        with coneccion.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            coneccion.close()
            self.conn = None
            return result

    def busca_id(self, tipo, dato):
        if tipo == "usuario":
            if "@" not in dato: dato = dato + self.dominio
            sql = "SELECT id from users \
            WHERE user_name = '" + dato + "'"
            filas = self.ejecutaSql(sql)
            return filas

        if tipo == "ticket":
            sql = "SELECT id from tickets WHERE ticket_number = '" + dato + "'"
            filas = self.ejecutaSql(sql) 
            return filas

    def buscaUsuario(self, usuario):
        if "@" in usuario:
            sql = "SELECT id, user_name, last_name, first_name, email, role FROM users where user_name = '" + usuario + "'"
        else:
            sql = "SELECT id, user_name, last_name, first_name, email, role FROM users where id = " + str(usuario)

        usuario = self.ejecutaSql(sql)

        for registro in usuario:
            relacionado_id = registro["id"]
            relacionado_usuario = registro["user_name"]
            relacionado_nombre = registro["first_name"]
            relacionado_apellido = registro["last_name"] 
            relacionado_email = registro["email"]
            relacionado_rol = registro["role"]

        return relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol


    def buscaData(self, item, dato, estado, relacionado, condicion, usuario):
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
                if "@" not in dato: dato = dato + self.dominio
                relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = self.buscaUsuario(dato)
            else: ## un solo ticket de un relacionado
                # relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = self.buscaUsuario(usuario)
                # if relacionado_rol == "user": 
                #     relacionado = "cliente"
                # else:
                #     relacionado = "agente"
                documento = True
        else:
            dato = usuario
            if relacionado != "":
                relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = self.buscaUsuario(dato)
            else: 
                relacionado_id, relacionado_usuario, relacionado_nombre, relacionado_apellido, relacionado_email, relacionado_rol = self.buscaUsuario(dato)
                if relacionado_rol == "user": 
                    relacionado = "cliente"
                else:
                    relacionado = "agente"


        if item == "":

            ## informacion de usuarios/clientes/agentes que esta en helpdesk ##
            if "@" not in dato: dato = dato + self.dominio
            sql = "SELECT \
            id, user_name, first_name, last_name,email, active, ext, \
            country_code, phone_number,mobile, primary_dpt,ban, role, \
            profile_pic, is_login, user_language from users \
            WHERE user_name = '" + dato + "' "
            
            if relacionado == "agente":
                sql = sql + "and (role = 'agent' or role = 'admin')" 
            else:
                sql = sql + "and role = 'user'"

            filas = self.ejecutaSql(sql)

            # print(dato + " " + estado)
            if filas != None:
                for fila in filas:
                    resultado = {
                        'id':fila["id"],
                        'usuario':fila["user_name"],
                        'nombre':fila["first_name"],
                        'apellido':fila["last_name"],
                        'email':fila["email"],
                        'activo':fila["active"],
                        'extension':fila["ext"],
                        'codigoarea':fila["country_code"],
                        'telefono':fila["phone_number"],
                        'celular':fila["mobile"],
                        'departamentoprimario':fila["primary_dpt"],
                        'bloqueado':fila["ban"],
                        'rol':fila["role"],
                        'fotoperfil':fila["profile_pic"],
                        'logueado':fila["is_login"],
                        'idioma':fila["user_language"]}

            return resultado


        if item == "ticket":
            ## busca el ticket por su numero de ticket 
            ## porque no se especifico que el ticket pertenecia a un relacionado

            ## SQL base de todos los queries, solo se adiciona la parte final de acuerdo a las condiciones ##
            sql = "SELECT \
            a.id as ticket_id, a.ticket_number as numero, t.title as titulo, a.user_id, b.user_name as uname_owner, b.first_name as fname_owner, \
            b.last_name as lname_owner, b.email as email_owner, b.role as rol_owner, b.country_code as ccode_owner, \
            b.mobile as mobile_owner, a.dept_id, c.name as deptname, a.help_topic_id, d.topic as topico, a.type, e.name as tipo, \
            e.type_desc, a.sla as sla_id, f.name as sla, f.admin_note, a.priority_id, h.priority as prioridad, a.status, i.name as estado, \
            a.assigned_to ,a.closed as cerrado, a.is_transferred as transferido, CAST(a.transferred_at AS CHAR) as fecha_transferido, \
            CAST(a.reopened_at AS CHAR) as fecha_reabierto, CAST(a.duedate AS CHAR) as fecha_vence, CAST(a.closed_at AS CHAR) as fecha_cierre , \
            a.first_response_time, CAST(a.created_at AS CHAR) as fecha_creacion, CAST(a.updated_at AS CHAR) as fecha_actualizado, a.resolution_time, \
            a.is_response_sla as respuesta_sla, a.is_resolution_sla as solucion_sla, t.poster as poster, t.thread_type as thread_type \
            from tickets a,users b, department c,help_topic d,ticket_type e,sla_plan f,ticket_priority h,ticket_status i, ticket_thread t \
            where a.user_id = b.id and a.dept_id = c.id and a.help_topic_id = d.id and a.type = e.id and a.sla = f.id and \
            a.priority_id = h.priority_id and a.status = i.id and t.title <> '' and t.ticket_id = a.id "

            if documento: 
                if nestado == 0: ## si el dato es un numero de documento y no se especifico estado busca ese solo numero de documento ##
                    sql = sql + "and a.ticket_number = '" + dato + "'"
                else: ## busca el documento con el estatus recibido ##
                    sql = sql + "and a.ticket_number = '" + dato + "' and a.status = " + str(nestado)
            else:
                if nestado == 0: nestado = 1 ## si no se pidio un estatus especifico para el documento se busca con el estatus 1 ##
                if relacionado == "agente":
                    if condicion == "sin asignar": 
                        sql = sql + "and a.assigned_to is null and a.status = " + str(nestado)
                    else:
                        sql = sql + "and a.assigned_to = " + str(relacionado_id) + " and a.status = " + str(nestado)
                else:
                    if condicion == "sin asignar": 
                        sql = sql + "and a.assigned_to is null and a.user_id = " + str(relacionado_id) + " and a.status = " + str(nestado)
                    else:
                        sql = sql + "and a.assigned_to is not null and a.user_id = " + str(relacionado_id) + " and a.status = " + str(nestado)

            filas = self.ejecutaSql(sql.strip())

            if filas != None:
                for registro in filas:
                    # titulo = registro["titulo"].encode("latin-1")
                    # titulo = titulo.decode("unicode_escape")
                    resultado = resultado + "-----------------------*" + "{}".format(registro["numero"]) + "*-----------------------" + "\n"
                    resultado = resultado + "*Titulo:* {}".format(registro["titulo"]) + "\n"
                    resultado = resultado + "*Estado:* {}".format(registro["estado"]) + " *Prioridad:* {}".format(registro["prioridad"]) + "\n"
                    resultado = resultado + "*Tipo:* {}".format(registro["tipo"]) + "\n" 
                    resultado = resultado + "*Topico:* {}".format(registro["topico"]) + "\n"
                    resultado = resultado + "*SLA:* {}".format(registro["sla"]) + "\n" 
                    resultado = resultado + "*Fecha Creacion:* {}".format(registro["fecha_creacion"]) + "\n" 
                    resultado = resultado + "*Fecha Vence:* {}".format(registro["fecha_vence"]) + "\n" 

                    if condicion != "sin asignar" and relacionado != "agente":
                        ## busca datos del agente asignado al ticket ##
                        sql = "SELECT user_name, last_name, first_name, email FROM users WHERE id = " + str(registro["assigned_to"])
                        asignado = self.ejecutaSql(sql)

                        if asignado != None: 
                            for tecnico in asignado:
                                resultado = resultado + "----------------------*Asignado A*----------------------" + "\n"
                                resultado = resultado + "*{}".format(registro["deptname"]) + "*" + "\n"
                                resultado = resultado + "*Agente:* {}".format(tecnico["first_name"]) + " {}".format(tecnico["last_name"]) + "\n"
                                resultado = resultado + "{}".format(tecnico["email"]) + "\n" 

            return resultado


        # if item == "ticket" and estado == "sin asignar":
        #     sql = "SELECT \
        #     a.id as ticket_id, a.ticket_number as numero,t.title as titulo, a.user_id, b.user_name as uname_owner, b.first_name as fname_owner, \
        #     b.last_name as lname_owner, b.email as email_owner, b.role as rol_owner, b.country_code as ccode_owner, \
        #     b.mobile as mobile_owner, a.dept_id, c.name as deptname, a.help_topic_id, d.topic as topico, a.type, e.name as tipo, \
        #     e.type_desc, a.sla as sla_id, f.name as sla, f.admin_note, a.priority_id, h.priority as prioridad, a.status, i.name as estado, \
        #     a.assigned_to ,a.closed as cerrado, a.is_transferred as transferido, CAST(a.transferred_at AS CHAR) as fecha_transferido, \
        #     CAST(a.reopened_at AS CHAR) as fecha_reabierto, CAST(a.duedate AS CHAR) as fecha_vence, CAST(a.closed_at AS CHAR) as fecha_cierre , \
        #     a.first_response_time, CAST(a.created_at AS CHAR) as fecha_creacion, CAST(a.updated_at AS CHAR) as fecha_actualizado, a.resolution_time, \
        #     a.is_response_sla as respuesta_sla, a.is_resolution_sla as solucion_sla \
        #     from tickets a,users b, department c,help_topic d,ticket_type e,sla_plan f,ticket_priority h,ticket_status i, ticket_thread t \
        #     where a.user_id = b.id and a.dept_id = c.id and a.help_topic_id = d.id and a.type = e.id and a.sla = f.id and \
        #     a.priority_id = h.priority_id and a.status = i.id and t.poster = 'client' and t.thread_type = 'first_reply' and t.title <> '' and t.ticket_id = a.id and \
        #     a.assigned_to is null and a.status = 1"
        #     filas = self.ejecutaSql(sql)

        #     if filas != None:
        #         for registro in filas:

        #             # print(registro["ticket_id"])
        #             # ## busca conversaciones en el ticket y selecciona el subject inicial ##
        #             # sql = "SELECT title from ticket_thread where poster = 'client' and thread_type = 'first_reply' and ticket_id = " + str(registro["ticket_id"])
        #             # conversacion = self.ejecutaSql(sql)

        #             resultado = resultado + "-----------------------*" + "{}".format(registro["numero"]) + "*-----------------------" + "\n"
        #             resultado = resultado + "*Titulo:* {}".format(registro["titulo"]) + "\n"
        #             resultado = resultado + "*Estado:* {}".format(registro["estado"]) + " *Prioridad:* {}".format(registro["prioridad"]) + "\n"
        #             resultado = resultado + "*Tipo:* {}".format(registro["tipo"]) + "\n" 
        #             resultado = resultado + "*Topico:* {}".format(registro["topico"]) + "\n"
        #             resultado = resultado + "*SLA:* {}".format(registro["sla"]) + "\n" 
        #             resultado = resultado + "*Fecha Creacion:* {}".format(registro["fecha_creacion"]) + "\n" 
        #             resultado = resultado + "*Fecha Vence:* {}".format(registro["fecha_vence"]) + "\n" 

        #     return resultado

        # if item == "telefono":
        #     # if "@" not in dato: dato = dato + dominio_usuario_helpdesk
        #     sql = "SELECT \
        #     id, user_name, first_name, last_name,email, active, ext, \
        #     country_code, phone_number,mobile, primary_dpt,ban, role, \
        #     profile_pic, is_login, user_language from users \
        #     WHERE mobile = '" + dato + "'"
        #     filas = self.ejecutaSql(sql)

        #     if filas != None:
        #         for fila in filas:
        #             resultado = {
        #                 'id':fila["id"],
        #                 'usuario':fila["user_name"],
        #                 'nombre':fila["first_name"],
        #                 'apellido':fila["last_name"],
        #                 'email':fila["email"],
        #                 'activo':fila["active"],
        #                 'extension':fila["ext"],
        #                 'codigoarea':fila["country_code"],
        #                 'telefono':fila["phone_number"],
        #                 'celular':fila["mobile"],
        #                 'departamentoprimario':fila["primary_dpt"],
        #                 'bloqueado':fila["ban"],
        #                 'rol':fila["role"],
        #                 'fotoperfil':fila["profile_pic"],
        #                 'logueado':fila["is_login"],
        #                 'idioma':fila["user_language"]}
            
        #     return resultado
