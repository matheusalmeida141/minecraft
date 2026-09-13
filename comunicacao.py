# %%
import socket
import struct
import json
import time

def encode_varint(val):
    total = b""

    if val < 0:
        val = (1 << 32) + val

    while True:
        byte = val & 0x7F
        val >>= 7
        if val != 0:
            byte |= 0x80
        total += struct.pack("B", byte)
        if val == 0:
            break

    return total

def encode_string(text:str):
    encode = text.encode("utf-8")
    return encode_varint(len(encode)) + encode


def cliente(host:str, port:int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)    

    packet_id = encode_varint(0x00)
    protocol_version = encode_varint(-1)
    server_address = encode_string(host)
    server_port = struct.pack(">H", port)
    next_state = encode_varint(1)

    data_package = packet_id + protocol_version + server_address + server_port + next_state
    full_package = encode_varint(len(data_package)) + data_package

    try:

        print("Conectando")
        sock.connect((host,port))

        print("Enviando...")
        sock.sendall(full_package)
        print("Enviado")


        status_request_packet = encode_varint(1) + encode_varint(0x00)
        sock.sendall(status_request_packet)

        resp = sock.recv(4096)
        print("Recebido")
        
        if resp.find(b'{') != -1:
            resp = resp[resp.find(b'{'):].decode("utf-8")
            return resp

    except Exception as e:
        print("Deu algo errado!", e)
    
    except sock.timeout:
        print("Servidor lento")

    finally:
        sock.close()


#%%
def to_json(HOST, PORT, resp):
    #data = json.loads('{' + "\"server_info\": {" + f"\"ip\": \"{HOST}\", \"port\": {str(PORT)}" + "}," + resp[1:105] + '}')
    data = json.loads(resp)

    with open("./servers/ips.json", "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(data, indent=2, ensure_ascii=False) + ',\n')

def to_txt(HOST:str, PORT:int, resp):
    data = f"{HOST}:{PORT} : " + resp[:resp.find("favicon")]
    with open("./servers/ips.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(data + ',\n')
# %%

import pandas as pd

df = pd.read_csv("dados.csv")

# %%
for HOST, PORT in zip(df["hostname"], df["port"]):
    PORT = int(PORT)
    resp = cliente(HOST, PORT)
    if resp != None:
        to_txt(HOST, PORT, resp)
    
# %%
cliente('200.168.222.50',25565)
# %%
