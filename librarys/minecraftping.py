import socket
import struct
import time

class MinecraftScan:
    def __encode_varint(self, val):
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

    def __encode_string(self, text:str):
        encode = text.encode("utf-8")
        return self.__encode_varint(len(encode)) + encode


    def client(self, HOST:str, PORT:int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)    

        packet_id = self.__encode_varint(0x00)
        protocol_version = self.__encode_varint(-1)
        server_address = self.__encode_string(HOST)
        server_PORT = struct.pack(">H", PORT)
        next_state = self.__encode_varint(1)

        data_package = packet_id + protocol_version + server_address + server_PORT + next_state
        full_package = self.__encode_varint(len(data_package)) + data_package

        try:

            print("Conectando")
            sock.connect((HOST,PORT))

            sock.sendall(full_package)
            print("Enviado", str(time.ctime()))


            status_request_packet = self.__encode_varint(1) + self.__encode_varint(0x00)
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
