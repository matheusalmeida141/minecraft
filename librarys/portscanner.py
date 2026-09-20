import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import time

class portScan:

    def __init__(self, SUBNET, PORT, TIMEOUT, MAX_WORKERS):
        self.SUBNET = SUBNET
        self.PORT = PORT
        self.TIMEOUT = TIMEOUT
        self.MAX_WORKERS = MAX_WORKERS

    def scan_ip(self):
        ip_str = str(self.IP)
        try:
            # Cria o socket para IPv4 e TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT)
                # Tenta conectar no IP atual e na porta fixa
                if s.connect_ex((ip_str, self.PORT)) == 0:
                    print(f"[+] {ip_str} está com a porta {self.PORT} ABERTA")
                    return(ip_str, self.PORT)
        except Exception:
            pass

    def ips(self, ips):
        try:
            #Converte a string da sub-rede em uma lista de hosts válidos
            network = ipaddress.ip_network(ips, strict=False)
            hosts = list(network.hosts())
            print(f"{time.ctime()} - Iniciando varredura na rede {ips} procurando a porta {self.PORT}...")
            print(f"Total de IPs a testar: {len(hosts)}")
            print("-" * 50)

            # Executa a varredura em paralelo usando Threads
            with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                executor.map(self.scan_ip, hosts)
                
            print("-" * 50)
            print("Varredura concluída.")
            
        except ValueError:
            print("Erro: Formato de sub-rede inválido. Use o formato CIDR (Ex: 192.168.1.0/24).")

    def start(self):
        print("Iniciando...")

        for i in range(0,255):
            for j in range(0,255):
                self.ips(f"{self.SUBNET}.{j}.{i}.0/24")
