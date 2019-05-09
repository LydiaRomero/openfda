import json
import socketserver
import http.server
import http.client

PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    URL = "api.fda.gov"
    LABEL = "/drug/label.json"
    ACTIVE_INGREDIENT = '&search=active_ingredient:'
    COMPANY = '&search=openfda.manufacturer_name:'

    def app_principal(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                </head>
                <body align=center style='background-color: #F6CECE'>
                    <h1>Bienvenido a la App de búsqueda de medicamentos</h1>
                    <h2>A continuación tiene un formulario en el que podrá realizar la búsqueda que necesite</h2>
                    <br>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Límite de parámetros para la lista de medicamentos">
                        <input type = "text" name="limit"></input>
                        </input>
                    </form>
                    <br>
                    <br>

                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Introduce componente activo">
                        <input type = "text" name="active_ingredient"></input>
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Límite de parámetros para la lista de empresas">
                        <input type = "text" name="limit"></input>
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Introduce nombre empresa">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <br>
                    <br>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Límite de parámetros para la lista de advertencias">
                        <input type = "text" name="limit"></input>
                        </input>
                    </form>
                    <br>
                    <br>
		    <p> Ingeniería Biomédica  </p>
		    <p> Universidad Rey Juan Carlos  </p>
                    <p>  Grado en Ingeniería Biomédica  </p>
                    <p> Curso 2018-2019 - URJC </p>
		    <p> Lydia Marugán Romero  </p>
                </body>
            </html>
                """

        return html



    def app_secundaria(self, lista):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #F6CECE'>
                                                <h1> Resultado de su búsqueda: </h1>
                                                <br>
                                                <ul>
                                    """
        for item in lista:
            html += "<li>" + item + "</li>"

        html += """
                                                </ul>
                                            </body>
                                        </html>
                                    """
        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

    def resultado_vacio(self):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #F6CECE'>
                                                <h1> Respuesta vacía: </h1>
                                                <p> Introduzca una respuesta en la página inicial <p>
                                                <br>
                                                <ul>
                                    """

        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

    def resultado_incorrecto(self):
        html = """
                                        <html>
                                            <head>
                                                <title>Openfda Lydia </title>
                                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                                            </head>
                                            <body style='background-color: #F6CECE'>
                                                <h1> Respuesta no encontrada: </h1>
                                                <p> Introduzca una nueva respuesta en la página inicial <p>
                                                <br>
                                                <ul>
                                    """

        html += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver a la página inicial </a>'
                    '</body>\n'
                    '</html>')
        return html

#
    def resultados(self, limit=10):
        conexion = http.client.HTTPSConnection(self.URL)
        conexion.request("GET", self.LABEL + "?limit=" + str(limit))
        print (self.LABEL + "?limit=" + str(limit))
        r1 = conexion.getresponse()
        label = r1.read().decode("utf8")
        informacion = json.loads(label)
        res = informacion['results']
        return res

    def do_GET(self):


        list_recurso = self.path.split("?")
        if len(list_recurso) > 1:
            parametros = list_recurso[1]
        else:
            parametros = ""

        if parametros:
            print("El usuario ha introducido parámetros")
        else:
            print("El usuario no ha introducido parámetros")


        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            web = self.app_principal()
            self.wfile.write(bytes(web, "utf8"))



        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_nombres = []
            limit = self.path.split('=')[1]
            if limit == "":
                limit = 22
            res = self.resultados(limit)
            for resultado in res:
                if ('generic_name' in resultado['openfda']):
                    lista_nombres.append(resultado['openfda']['generic_name'][0])
                else:
                    lista_nombres.append('Nombre desconocido')
            resultado_final = self.app_secundaria(lista_nombres)
            self.wfile.write(bytes(resultado_final, "utf8"))

        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            componente = self.path.split('=')[1]
            limit = 10

            try:
                lista_nombre = []
                lista_encontrados = []
                conexion = http.client.HTTPSConnection(self.URL)

                conexion.request("GET",self.LABEL + "?limit=" + str(limit) + self.ACTIVE_INGREDIENT + componente)
                r1 = conexion.getresponse()
                label1 = r1.read().decode("utf8")
                info1 = json.loads(label1)

                buscador_componente = info1['results']

                for resultado in buscador_componente:
                    if ('generic_name' in resultado['openfda']):
                        lista_nombre.append(resultado['openfda']['generic_name'][0])

                    else:
                        lista_nombre.append('Nombre desconocido')


                resultado_final = self.app_secundaria(lista_nombre)
                self.wfile.write(bytes(resultado_final, "utf8"))

            except KeyError:
                if componente == "":
                    resultado_final = self.resultado_vacio()
                    self.wfile.write(bytes(resultado_final, "utf8"))
                else:
                    resultado_final = self.resultado_incorrecto()
                    self.wfile.write(bytes(resultado_final, "utf8"))


        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_empresas = []
            limit = self.path.split('=')[1]
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    lista_empresas.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    lista_empresas.append('Empresa desconocida')
            resultado_final = self.app_secundaria(lista_empresas)
            self.wfile.write(bytes(resultado_final, "utf8"))

        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            empresa = self.path.split('=')[1]
            limit = 10
            try:
                lista_empresa = []
                lista_encontrados1 = []
                conexion = http.client.HTTPSConnection(self.URL)

                conexion.request("GET",self.LABEL + "?limit=" + str(limit) + self.COMPANY + empresa)
                r1 = conexion.getresponse()
                label1 = r1.read().decode("utf8")
                info1 = json.loads(label1)

                buscador_empresa = info1['results']

                for resultado in buscador_empresa:
                    if ('manufacturer_name' in resultado['openfda']):
                        lista_empresa.append(resultado['openfda']['manufacturer_name'][0])

                    else:
                        lista_empresa.append('Nombre desconocido')


                resultado_final = self.app_secundaria(lista_empresa)
                self.wfile.write(bytes(resultado_final, "utf8"))

            except KeyError:
                if empresa == "" or limit == "":
                    resultado_final = self.resultado_vacio()
                    self.wfile.write(bytes(resultado_final, "utf8"))
                else:
                    resultado_final = self.resultado_incorrecto()
                    self.wfile.write(bytes(resultado_final, "utf8"))
        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_advertencias = []
            limit =self.path.split('=')[1]
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    lista_advertencias.append(resultado['warnings'][0])
                else:
                    lista_advertencias.append('Adevertencia desconocida')
            resultado_final = self.app_secundaria(lista_advertencias)
            self.wfile.write(bytes(resultado_final, "utf8"))

        elif 'redirect' in self.path:
            self.send_response(301)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Recurso no encontrado '{}'.".format(self.path).encode())
        return


socketserver.TCPServer.allow_reuse_address = True

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto:", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("El usuario ha interrumpido la conexión en el puerto", PORT)


print("Servidor parado")
