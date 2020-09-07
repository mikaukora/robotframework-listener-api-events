from websocket import create_connection
import json


class ListenerApi2Events():
    ROBOT_LISTENER_API_VERSION = 2

    def send_message(self, event, name=None, attrs=None, message=None, path=None):
        ws = create_connection("ws://localhost:5678/")
        info = {}
        info["event"] = event
        if name:
            info["name"] = name
        if path:
            info["path"] = path
        if message:
            info.update(message)
        if attrs:
            info.update(attrs)
        ws.send(json.dumps(info))
        ws.close()

    def start_suite(self, name, attrs):
        self.send_message("start_suite", name, attrs)

    def end_suite(self, name, attrs):
        self.send_message("end_suite", name, attrs)

    def start_test(self, name, attrs):
        self.send_message("start_test", name, attrs)

    def end_test(self, name, attrs):
        self.send_message("end_test", name, attrs)

    def start_keyword(self, name, attrs):
        self.send_message("start_keyword", name, attrs)

    def end_keyword(self, name, attrs):
        self.send_message("end_keyword", name, attrs)

    def log_message(self, message):
        self.send_message("log_message", message=message)

    def message(self, message):
        self.send_message("message", message=message)

    def library_import(self, name, attrs):
        self.send_message("library_import", name, attrs)

    def resource_import(self, name, attrs):
        self.send_message("resource_import", name, attrs)

    def variables_import(self, name, attrs):
        self.send_message("variables_import", name, attrs)

    def output_file(self, path):
        self.send_message("output_file", path=path)

    def log_file(self, path):
        self.send_message("log_file", path=path)

    def report_file(self, path):
        self.send_message("report_file", path=path)

    def xunit_file(self, path):
        self.send_message("xunit_file", path=path)

    def debug_file(self, path):
        self.send_message("debug_file", path=path)

    def close(self):
        self.send_message("close")


if __name__ == "__main__":
    from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

    clients = []
    class SimpleServ(WebSocket):

        def handleMessage(self):
          for client in clients:
            if client != self and not client.closed:
                client.sendMessage(self.data)

        def handleConnected(self):
            clients.append(self)

        def handleClose(self):
            clients.remove(self)

    server = SimpleWebSocketServer('', 5678, SimpleServ)
    server.serveforever()
