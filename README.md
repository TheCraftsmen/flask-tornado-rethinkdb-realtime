Implementacion de changesfeed de rethinkdb usando websocket
de tornado con el microframework Flask


como funciona?

lo que hacer la corutine de tornado es enviar un mensaje en broadcast cada vez
que se ejecuta un cambio en la base de datos

primero instalar rethinkdb 2.3.0

despues la libreria para python

correr la base de datos

y crear la tabla autores como en el tutorial de get started de rethinkdb

conn = r.connect(host="localhost", port=28015)

r.db("test").table_create("autores").run(conn)

ahora ejecuten en una terminal

windows
C:\> python app.py

linux
$ python app.py

y dejar corriendo

en otra terminal abrir el interprete python 

>>> import rethinkdb as r

>>> conn = r.connect(host="localhost", port=28015)

>>> r.table("autores").insert([
	{"nombre": "lionel", "apellido": "messi"}
]).run(conn)

y van a ver como se ejecuta el change en la terminal que tiene flask con tornado corriendo
