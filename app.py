# %%
import json
from librarys.minecraftping import MinecraftScan

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


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

import pandas as pd

df = pd.read_csv("./servers/ips.csv", header=None, names=["hostname","port"],)
df["port"] = 25565
df.head()
# %%
minecraftPing = MinecraftScan()

for HOST, PORT in zip(df["hostname"], df["port"]):
    resp = minecraftPing.client(HOST, PORT)
    if resp != None:
        to_txt(HOST, PORT, resp)
    

# %%
