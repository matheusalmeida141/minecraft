import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# Configurações do Alvo
SUBNET = "201.168.2.1/24"  # Defina a faixa de rede (CIDR)
PORT = 25565                 # Defina a porta única que deseja escanear
TIMEOUT = 1.0              # Tempo de espera por resposta (em segundos)
MAX_WORKERS = 100          # Número de testes em paralelo

def scan_ip(ip):
    ip_str = str(ip)
    try:
        # Cria o socket para IPv4 e TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            # Tenta conectar no IP atual e na porta fixa
            if s.connect_ex((ip_str, PORT)) == 0:
                print(f"[+] {ip_str} está com a porta {PORT} ABERTA")
                # with open("ips.csv", mode="a") as arquivo:
                #     arquivo.write(ip_str + ',\n')
    except Exception:
        pass

def ips(ips):
    try:
        # Converte a string da sub-rede em uma lista de hosts válidos
        network = ipaddress.ip_network(ips, strict=False)
        hosts = list(network.hosts())
        #print(f"Iniciando varredura na rede {ips} procurando a porta {PORT}...")
        #print(f"Total de IPs a testar: {len(hosts)}")
        #print("-" * 50)

        # Executa a varredura em paralelo usando Threads
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(scan_ip, hosts)
            
        #print("-" * 50)
        #print("Varredura concluída.")
        
    except ValueError:
        print("Erro: Formato de sub-rede inválido. Use o formato CIDR (Ex: 192.168.1.0/24).")


print("Iniciando...")

for i in range(0,255):
    for j in range(0,255):
        ips(f"200.{j}.{i}.0/24")