import threading
import socket
import time
import selectors
import json

class Server:
    def __init__(self):
        self.clients = {}
        self.host = "0.0.0.0"
        self.port = 8066
        self.TIMEOUT = 60
        self.selector = selectors.DefaultSelector()

    def handle_clients(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Connection closed by {addr}")
                    break
                else:
                    self.clients[conn]["data"] = data.decode("utf-8")
                    self.clients[conn]["time"] = time.time()
        except BlockingIOError:
            # No data available to read, continue waiting
            pass
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
        finally:
            self.selector.unregister(conn)
            del self.clients[conn]
            conn.close()

    def prep_data(self):
        data = {}
        for count, (client, info) in enumerate(self.clients.items()):
            try:
                data[count] = info["data"]
            except Exception as e:
                print(f"FAILED to prep data for {info['address']}: {e}")
        return json.dumps(data)

    def update(self):
        while True:
            d = self.prep_data()
            for client, info in list(self.clients.items()):
                try:
                    client.send(d.encode("utf-8"))
                except Exception as e:
                    print(f"FAILED to send update to {info['address']}: {e}")

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        s.setblocking(False)

        self.selector.register(s, selectors.EVENT_READ)
        print("Server started, listening for connections...")

        while True:
            events = self.selector.select(timeout=1)
            for key, mask in events:
                if key.fileobj == s:
                    connection, address = s.accept()
                    print(f"New connection from {address}")
                    connection.setblocking(False)
                    self.selector.register(connection, selectors.EVENT_READ)
                    self.clients[connection] = {"connection": connection, "address": address, "time": time.time()}
                    client_thread = threading.Thread(target=self.handle_clients, args=(connection, address,))
                    client_thread.start()
                elif mask & selectors.EVENT_READ:
                    connection = key.fileobj
                    self.handle_clients(connection, self.clients[connection]["address"])

            current_time = time.time()
            for connection, info in list(self.clients.items()):
                if current_time - info["time"] > self.TIMEOUT:
                    print(f"Connection timed out with {info['address']}")
                    self.selector.unregister(connection)
                    del self.clients[connection]
                    connection.close()

if __name__ == "__main__":
    server = Server()
    update_thread = threading.Thread(target=server.update)
    update_thread.start()
    server.main()
