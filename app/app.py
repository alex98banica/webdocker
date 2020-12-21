import os
import json
import datetime
from flask import request
from flask import Response
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', 'passwd'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(80), unique=True, nullable=False)
    lat = db.Column(db.String(80))
    lon = db.Column(db.String(80))

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTara = db.Column(db.Integer)
    nume = db.Column(db.String(80), unique=True, nullable=False)
    lat = db.Column(db.String(80))
    lon = db.Column(db.String(80))

class Temperatures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idOras = db.Column(db.Integer)
    valoare = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/api/countries", methods=["POST"])
def insert_countries():
    try:
        req_data = request.json
        numee = req_data['nume']
        latt = req_data['lat']
        lonn = req_data['lon']
    except:
        return Response(status=400)

    try:
        row = Country(nume = numee, lat = 25.124,lon = float(lonn))
        db.session.add(row)
        db.session.commit()

        select = Country.query.filter_by(nume=numee).first()
        return Response(json.dumps(select.id), status=201)
    except:
        return Response(status = 409)

@app.route("/api/countries", methods=["GET"])
def get_countries():

        res = Country.query.all()
        y = []
        for country in res:
            ret={
                "id" : country.id,
                "nume" : country.nume,
                "lat" : float(country.lat),
                "lon" : float(country.lon)
            }
            y.append(ret)
        return Response(json.dumps(y),status = 200)

@app.route("/api/countries/<id>", methods=["PUT"])
def put_countries(id):
    try:
        req_data = request.json
        numee = req_data['nume']
        latt = req_data['lat']
        lonn = req_data['lon']
    except:
        return Response(status=400)
    try:
        Country.query.filter(Country.id == id).delete()
        db.session.commit()
        row = Country(id = id, nume = numee, lat = latt,lon = lonn)
        db.session.add(row)
        db.session.commit()
        return Response(status=200)
    except:
        return Response(status=404)


@app.route("/api/countries/<id>", methods=["DELETE"])
def del_countries(id):
    try:
        sterg = Country.query.filter(Country.id == id).first()
        if sterg is not None:
            Country.query.filter(Country.id == id).delete()
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=404)

@app.route("/api/cities", methods=["POST"])
def insert_city():
    try:
        req_data = request.json
        idTaraa = req_data['idTara']
        numee = req_data['nume']
        latt = req_data['lat']
        lonn = req_data['lon']
    except:
        return Response(status=400)


    res = Country.query.all()
    t = 0
    for country in res:
        if int(idTaraa) == int(country.id):
            t = 1
    if t == 0:
        return Response(status=409)


    try:
        row = City(idTara = idTaraa, nume = numee, lat = float(latt), lon = float(lonn))
        db.session.add(row)
        db.session.commit()

        select = City.query.filter_by(nume=numee).first()
        return Response(json.dumps(select.id), status=201)
    except:
        return Response(status = 409)


@app.route("/api/cities", methods=["GET"])
def get_cities():

        res = City.query.all()
        y = []
        for city in res:
            ret={
                "id" : city.id,
                "idTara" : city.idTara,
                "nume" : city.nume,
                "lat" : float(city.lat),
                "lon" : float(city.lon)
            }
            y.append(ret)
        return Response(json.dumps(y),status = 200)


@app.route("/api/cities/country/<idTara>", methods=["GET"])
def get_cities_id(idTara):

        res = City.query.filter_by(idTara = idTara).all()
        y = []
        for city in res:
            ret={
                "id" : city.id,
                "idTara" : city.idTara,
                "nume" : city.nume,
                "lat" : float(city.lat),
                "lon" : float(city.lon)
            }
            y.append(ret)
        return Response(json.dumps(y),status = 200)

@app.route("/api/cities/<id>", methods=["PUT"])
def put_cities(id):
    try:
        req_data = request.json
        idTaraa = req_data['idTaraa']
        numee = req_data['nume']
        latt = req_data['lat']
        lonn = req_data['lon']
    except:
        return Response(status=400)
    try:
        db.session.commit()
        res = Country.query.all()
        t = 0
        for country in res:
            if int(idTaraa) == int(country.id):
                City.query.filter(City.id == id).delete()
                row = City(id = id, idTara = idTaraa, nume = numee, lat = latt,lon = lonn)
                db.session.add(row)
                db.session.commit()
                t = 1

        if t == 1:
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=404)

@app.route("/api/cities/<id>", methods=["DELETE"])
def del_cities(id):
    try:
        sterg = City.query.filter(City.id == id).first()
        if sterg is not None:
            City.query.filter(City.id == id).delete()
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=404)


@app.route("/api/temperatures", methods=["POST"])
def insert_temperatures():
    try:
        req_data = request.json
        idOrass = req_data['idOras']
        valoaree = req_data['valoare']
    except:
        return Response(status=400)


    res = City.query.all()
    t = 0
    for city in res:
        if int(idOrass) == int(city.id):
            t = 1
    if t == 0:
        return Response(status=409)


    try:
        row = Temperatures(idOras = idOrass, valoare = valoaree, timestamp = datetime.datetime.utcnow()+datetime.timedelta(hours=2))
        db.session.add(row)
        db.session.commit()

        select = Temperatures.query.filter_by(idOras = idOrass , valoare = valoaree).order_by(Temperatures.id.desc()).first()
        return Response(json.dumps(select.id), status=201)
    except:
        return Response(status = 409)


@app.route("/api/temperatures/<id>", methods=["PUT"])
def put_temperatures(id):
    try:
        req_data = request.json
        idOrass = req_data['idOras']
        valoaree = req_data['valoare']
    except:
        return Response(status=400)

    try:
        db.session.commit()
        res = City.query.all()
        t = 0
        for city in res:
            if int(idOrass) == int(city.id):
                Temperatures.query.filter(Temperatures.id == id).delete()
                db.session.commit()
                row = Temperatures(id = id, idOras = idOrass, valoare = valoaree, timestamp = datetime.datetime.utcnow()+datetime.timedelta(hours=2))
                db.session.add(row)
                db.session.commit()
                t = 1
        if t == 1:
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=404)

@app.route("/api/temperatures/<id>", methods=["DELETE"])
def del_temepratures(id):
    try:
        sterg = Temperatures.query.filter(Temperatures.id == id).first()
        if sterg is not None:
            Temperatures.query.filter(Temperatures.id == id).delete()
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=404)


@app.route("/api/temperatures", methods=["GET"])
def get_temp1():
    try:
        latt = request.args.get('lat')
        lonn = request.args.get('lon')
        fromm = request.args.get('from')
        untill = request.args.get('until')
        udate = datetime.datetime.strptime(untill, '%Y-%m-%d')
        fdate = datetime.datetime.strptime(fromm, '%Y-%m-%d')
    except:
        return Response(status = 400)

    try:
        res = Temperatures.query.all()
        y = []
        for temp in res:
            if temp.timestamp.date() >= fdate.date() and temp.timestamp.date() <= udate.date() :
                ret={
                    "id" : temp.id,
                    "valoare" : temp.valoare,
                    "timestamp" : temp.timestamp.date().strftime('%Y-%m-%d')
                }
                y.append(ret)
        return Response(json.dumps(y),status = 200)
    except:
        return Response(status = 409)

@app.route("/api/temperatures/cities/<idOras>", methods=["GET"])
def get_tem2(idOras):
    y = []
    try:
        fromm = request.args.get('from')
        untill = request.args.get('until')
        udate = datetime.datetime.strptime(untill, '%Y-%m-%d')
        fdate = datetime.datetime.strptime(fromm, '%Y-%m-%d')
    except:
        return Response(json.dumps(y),status = 200)

    try:
        res = Temperatures.query.all()
        for temp in res:
            if temp.timestamp.date() >= fdate.date() and temp.timestamp.date() <= udate.date() and int(idOras) == int(temp.idOras) :
                ret={
                    "id" : temp.id,
                    "valoare" : temp.valoare,
                    "timestamp" : temp.timestamp.date().strftime('%Y-%m-%d')
                }
                y.append(ret)
        return Response(json.dumps(y),status = 200)
    except:
        return Response(json.dumps(y),status = 200)

@app.route("/api/temperatures/countries/<idTara>", methods=["GET"])
def get_tem3(idTara):
    y = []
    try:
        fromm = request.args.get('from')
        untill = request.args.get('until')
        udate = datetime.datetime.strptime(untill, '%Y-%m-%d')
        fdate = datetime.datetime.strptime(fromm, '%Y-%m-%d')
    except:
        return Response(json.dumps(y),status = 200)
    try:
        res = Temperatures.query.all()
        res2 = City.query.all()
        for city in res2:
            for temp in res:
                if temp.timestamp.date() >= fdate.date() and temp.timestamp.date() <= udate.date() and int(city.id) == int(temp.idOras) and int(idTara) == int(city.idTara):
                    ret={
                        "id" : temp.id,
                        "valoare" : temp.valoare,
                        "timestamp" : temp.timestamp.date().strftime('%Y-%m-%d')
                    }
                    y.append(ret)
        return Response(json.dumps(y),status = 200)
    except:
        return Response(json.dumps(y),status = 200)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
