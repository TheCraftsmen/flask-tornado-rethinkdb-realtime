"""Flasknado! - A simple example of using Flask and Tornado
together.

"""

from __future__ import print_function
from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.websocket import WebSocketHandler
import rethinkdb as r
from tornado import gen
from tornado.ioloop import IOLoop

CONNECTED_CLIENTS = list()

class WebSocket(WebSocketHandler):
    def open(self):
        CONNECTED_CLIENTS.append(self)
        print("Socket opened.")

    def on_message(self, message):
        #self.write_message("Received: " + message)

        print("Received message: " + message)
        self.broadcast("Received: " + message)
        print(CONNECTED_CLIENTS)

    def broadcast(self, msj):
        for c in CONNECTED_CLIENTS:
            c.write_message(msj)

    def on_close(self):
        print("Socket closed.")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



r.set_loop_type("tornado")

@gen.coroutine
def print_changes():
    conn = yield r.connect(host="localhost", port=28015)
    feed = yield r.table("autores").changes().run(conn)
    while (yield feed.fetch_next()):
        change = yield feed.next()
        print(change)
        for c in CONNECTED_CLIENTS:
            c.write_message(change)


if __name__ == "__main__":
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])
    server.listen(8090)
    IOLoop.current().add_callback(print_changes)
    IOLoop.instance().start()
