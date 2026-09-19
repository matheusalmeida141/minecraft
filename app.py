# %%
import json
from librarys.minecraftping import MinecraftScan
from librarys.portscanner import portScan


#%%
def to_json(HOST, PORT, resp):
    #data = json.loads('{' + "\"server_info\": {" + f"\"ip\": \"{HOST}\", \"port\": {str(PORT)}" + "}," + resp[1:105] + '}')
    data = json.loads(resp)

    with open("./servers/ips.json", "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(data, indent=2, ensure_ascii=False) + ',\n')

def to_txt(HOST:str, PORT:int, resp):
    data = f"{HOST}:{PORT} : " + resp[:resp.find("favicon")]
    with open("./servers/minecraft.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(data + ',\n')
# %%
lines = []
with open("./servers/ips.csv", "r") as fl:
    lines  = fl.readlines()

for i in range(len(lines)):
    lines[i] = lines[i].replace('\n', '').replace(',','')

lines
# %%
minecraftPing = MinecraftScan()
PORT = 25565
for HOST in (lines):
    resp = minecraftPing.client(HOST, PORT)
    if resp != None:
        to_txt(HOST, PORT, resp)
    

# %%
# Configurações do Alvo
SUBNET = "200"  # Defina a faixa de rede (CIDR)
PORT = 25565                 # Defina a porta única que deseja escanear
TIMEOUT = 1.0              # Tempo de espera por resposta (em segundos)
MAX_WORKERS = 100          # Número de testes em paralelo
