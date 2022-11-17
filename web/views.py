from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from sqlalchemy import create_engine

from web.models import Connections


def index(request):
    print(Connections.objects.all())
    return render(request, 'index.html')


class ConnectionPage(View):
    template_name = "index.html"

    def get(self, request):
        # user = request.user
        conn_list = Connections.objects.all()
        return render(request, self.template_name, {'list': conn_list})

    def post(self, request):
        action = request.POST["action"]
        if action == 'delete':
            conn_id = request.POST["conn-id"]
            conn = Connections.objects.filter(connection_id=conn_id).delete()
        elif action == 'test':
            dbtype = request.POST["dbtype"]
            username = request.POST["username"]
            password = request.POST["password"]
            host = request.POST["host"]
            port = request.POST["port"]
            schema = request.POST["schema"]
            if len(password):
                con_string = dbtype + '://' + username + ':' + password + '@' + host + ':' + port + '/' + schema
            else:
                con_string = dbtype + '://' + username + '@' + host + ':' + port + '/' + schema
            print(con_string)
            try:
                engine = create_engine(con_string, echo=True)
                print(engine.connect())
            except Exception as e:
                print(e)
                try:
                    return HttpResponse(str(e.orig.args[1]))
                except:
                    return HttpResponse(str(e))
            return HttpResponse("Success")
        elif action == 'add':
            dbtype = request.POST["dbtype"]
            connectionname = request.POST["name"]
            username = request.POST["username"]
            password = request.POST["password"]
            host = request.POST["host"]
            port = request.POST["port"]
            schema = request.POST["schema"]
            Connections.objects.create(dbtype=dbtype, connection_name=connectionname, username=username,
                                       password=password, host=host, port=port, schema=schema)
        return redirect("/")


class Tables(View):
    template_name = "tables.html"

    def get(self, request, conn_id):
        # conn_id = request.GET['id']
        conn = Connections.objects.get(connection_id=conn_id)
        if len(conn.password):
            con_string = conn.dbtype + '://' + conn.username + ':' + conn.password + '@' + conn.host + ':' + str(conn.port) + '/' + conn.schema
        else:
            con_string = conn.dbtype + '://' + conn.username + '@' + conn.host + ':' + str(conn.port) + '/' + conn.schema
        print(con_string)
        engine = create_engine(con_string, echo=True)
        request.session['conn_id'] = conn_id
        request.session['con_string'] = con_string
        return render(request, self.template_name, {'list': engine.table_names()})

    def post(self, request):
        action = request.POST["action"]
        if action == 'delete':
            conn_id = request.POST["id"]
            conn = Connections.objects.filter(connection_id=conn_id).delete()
        elif action == 'test':
            dbtype = request.POST["dbtype"]
            username = request.POST["username"]
            password = request.POST["password"]
            host = request.POST["host"]
            port = request.POST["port"]
            schema = request.POST["schema"]
        return redirect("/")
