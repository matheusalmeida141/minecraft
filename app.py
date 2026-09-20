# %%
from librarys.minecraftping import MinecraftScan
from librarys.portscanner import portScan
from librarys.crud import database
import multiprocessing
import time


#CONFIG
SUBNET = "200"
PORT = "25565"
TIMEOUT = 5
MAX_WORKERS = 100

#DATABASE
db = database()

# %%

# def setup():
#     with open("./servers/minecraft.txt", "w", encoding="utf-8") as file:
#         print("Create minecraft txt")

def scan_ips():
    print("Iniciando o scan de ips e portas")
    pScan = portScan(SUBNET,PORT, TIMEOUT, MAX_WORKERS)
    address = pScan.start()
    db.create(address[0], address[1])

def ping_ips():
    ping = MinecraftScan()
    while(1):
        data = db.select()
        print(data)
        for x in data:
            print(x["_id"],x["ip"], x["port"])
            res = ping.client(x["ip"], x["port"])
            if res != None:
                with open("./servers/minecraft.txt", "a") as fl:
                    fl.write(res + "\n")
            db.delete(x["_id"])
        time.sleep(2)


if __name__ == "__main__":
    print("Iniciando Script")
    p1 = multiprocessing.Process(target=scan_ips)
    p2 = multiprocessing.Process(target=ping_ips)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
# %%
