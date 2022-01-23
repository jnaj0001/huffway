import socket, asyncio
from datetime import datetime


class FLchat:
    def __init__(self):
        print("""
        Welcome to FLchat!

        Please choose one of the following 2 options:
            1. Server - Setup a socket and be a server
            2. Client - Connect to a server and be a client

        Type your choice below (tip: you can also enter single digits):
            """)
        self.user_input = input()
        msg_time = datetime.now(tz=None)
        try:
            if int(self.user_input):
                self.user_input = int(self.user_input)
        except:
            self.user_input = self.user_input.lower()
        if self.user_input in ["server", 1]:
            self.user_input = 1
            print(msg_time.strftime("(%d-%b-%Y %H:%M) ") + "Server connected.")
            self.server_chat()
        elif self.user_input in ["client", 2]:
            self.user_input = 2
            print(msg_time.strftime("(%d-%b-%Y %H:%M) ") + "Client connected.")
            self.client_chat()


    def server_chat(self):
        async def handle_client(reader, writer):
            request = None
            while request != 'quit':
                request = (await reader.read(255)).decode('utf8')
                msg_time = datetime.now(tz=None)
                print(msg_time.strftime("(%d-%b-%Y %H:%M) ") + "Received: " + request)
                response = str(input('>> ')) + '\n'
                writer.write(response.encode('utf8'))
                await writer.drain()
            writer.close()

        async def run_server():
            server = await asyncio.start_server(handle_client, 'localhost', 6767)
            async with server:
                await server.serve_forever()

        asyncio.run(run_server())

    def client_chat(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 6767))
        request = None

        try:
            while request != 'quit':
                request = input('>> ')
                if request:
                    client.send(request.encode('utf8'))
                    response = client.recv(255).decode('utf8')
                    msg_time = datetime.now(tz=None)
                    print(msg_time.strftime("(%d-%b-%Y %H:%M) ") + "Received: " + response)
        except KeyboardInterrupt:
            client.close()

