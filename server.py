from http.server import BaseHTTPRequestHandler, HTTPServer


PORT = 8000



# Define o que o servidor fará quando receber uma requisição
class MeuHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Envia o código de status HTTP 200 (Sucesso)
        self.send_response(200)
        
        # 2. Define o tipo de conteúdo como texto/HTML
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # 3. Cria a mensagem que vai aparecer na página
        with open("./servers/ips.csv", 'r') as aq:
            for i in aq:
                msg  = f"<p>{i}<p>"
            #mensagem += f"<p>{i}</p>"
        # 4. Envia a mensagem convertida em bytes para o navegador
            
                self.wfile.write(bytes(msg, "utf-8"))

# Configura e inicia o servidor
with HTTPServer(("", PORT), MeuHandler) as server:
    print(f"Servidor rodando em http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado.")
