import threading 
import socket
import time
import selectors

clients = {}


host = "0.0.0.0"
port = 8000


TIMEOUT = 60
selector = selectors.DefaultSelector()

def handle_clients(conn, addr):
    try:
        while True:
            global clients
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by (addr)")
                break
            else:
                clients[conn]["data"] = data.decode("utf-8")
            clients[conn] = time.time()
    except ConnectionResetError:
        print(f"Connnection reset by {addr}")
    finally:
        selector.unregister(conn)
        del clients[conn]
        conn.close()

def update():
    while True:
        global clients
        for client in clients:
            try:
                client.send(clients.encode("utf-8"))
            except:
                print("FAILED to send update to "+str(clients[client]["address"]))


def main():
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.bind((host, port))
     s.listen(5)
     s.setblocking(False)

     selector.register(s, selectors.EVENT_READ)
     
     print("Server started, listening for connections...")

    while True:
        global clients, TIMEOUT
        events = selector.select(timeout=1)
        for key, mask in events:
            if key.fillobj == s:
                connection, address = s.accept()
                print(f"New connection from {address}")
                connection.setblocking(False)
                selector.register(connection, selectors.EVENT_READ)
                clients[connection] = {"connection":connection,"address":address,"time":time.time()}
                client_thread = threading.Thread(target=handle_client,  args=(connection,address,))
            elif mask & selectors.EVENT_READ:
                connection = key.fileobj



        current_time = time.time()
        for conneciton, last_activity_time in list(connection.items()):
            if current_time - last_activity_time > TIMEOUT:
                print(f"Connection timed out")
                selector.unregistor(connection)
                del clients[connection]
                connection.close()


if __name__ == "__main__":
    update_thread = threading.Thread(target=update, args=(,))
    update_thread.start()
    main()

