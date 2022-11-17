from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

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

    def get(self, request, conn_id=None):
        try:
            con_string = None
            if not conn_id:
                con_string = request.session.get('con_string')
                if not con_string:
                    return redirect("/")
            if not con_string:
                conn = Connections.objects.get(connection_id=conn_id)
                if len(conn.password):
                    con_string = conn.dbtype + '://' + conn.username + ':' + conn.password + '@' + conn.host + ':' + str(conn.port) + '/' + conn.schema
                else:
                    con_string = conn.dbtype + '://' + conn.username + '@' + conn.host + ':' + str(conn.port) + '/' + conn.schema
            print(con_string)
            engine = create_engine(con_string, echo=True)
            request.session['conn_id'] = conn_id
            request.session['con_string'] = con_string
            metadata = MetaData()
            metadata.reflect(engine)
            base = automap_base(metadata=metadata)
            base.prepare()
            tables_list = []
            for table_name in engine.table_names():
                constraints = ''
                for i in base.classes[table_name].__table__.constraints:
                    constraints += str(i).split("(")[0] + " : "
                    for j in i.columns:
                        constraints += j.name + " | "
                tables_list.append({
                    'name': table_name,
                    'constraints': constraints
                })
            return render(request, self.template_name, {'list': tables_list})
        except Exception as e:
            print(e)
            return redirect("/")

    def post(self, request):
        return redirect("/")


class Table(View):
    template_name = "columns.html"

    def get(self, request, conn_id, table_name):
        con_string = request.session.get('con_string')
        if con_string:
            print(con_string)
            engine = create_engine(con_string, echo=True)
            session = Session(engine)
            metadata = MetaData()
            metadata.reflect(engine)
            base = automap_base(metadata=metadata)
            base.prepare()
            columns = []
            row_count = session.query(base.classes[table_name]).count()
            for column in base.classes[table_name].__table__.columns:
                name = column.key
                column_type = str(column.type)
                columns.append({'name': name, 'type': column_type})
            return render(request, self.template_name, {'list': columns, 'col': len(columns), 'row': row_count})
        else:
            return redirect("/")

    def post(self, request):
        return redirect("/")
