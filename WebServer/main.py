from threading import Thread

import mysql.connector
from flask import Flask, render_template, session, request, redirect, url_for, make_response, json, jsonify

from Queues import solarObject, eolicObject, chargeTime, requests, rules
from time import time
from EnergyManagement import runEnergyManagement
from ServerRequests import runRequests
from ServerResponses import runResponses
from Rules import runRules
import socket

host = 'localhost'
FLASK_PORT = 12345
SOCKET_PORT = 8000
dbhost = "localhost"
user = "python"
password = "python"
dbname = "dbsensores"

db = mysql.connector.connect(
    host=dbhost,
    user=user,
    password=password,
    database=dbname
)
cursor = db.cursor()

s = socket.socket()
s.connect((host, SOCKET_PORT))


def RequestsToServer():
    runRequests(s)


def ResponsesFromServer():
    runResponses(s)


def RulesSetup():
    runRules()


def EnergyManagement():
    runEnergyManagement()


app = Flask(__name__)
app.secret_key = "encode_key"


@app.route('/')
def index():
    try:
        return render_template('dashboard.html', username=session['username'])
    except:
        return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if session['username'] == None:
        return render_template('login.html')
    else:
        return render_template('dashboard.html', username=session['username'])

@app.route('/actuators')
def actuators():
    if session['username'] == None:
        return render_template('login.html')
    else:
        return render_template('actuators.html', username=session['username'])


@app.route('/login ', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("CALL login_user('" + username + "','" + password + "')")
        record = cursor.fetchone()
        while (db.next_result()):
            print()
        if str(record[0]) == "1":
            session['loggedin'] = True
            session['username'] = record[0]
            return redirect(url_for('dashboard'))
        else:
            msg = "Invalid Credentials"
    return render_template('index.html', msg=msg)

@app.route('/logout ', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/data', methods=["GET", "POST"])
def data():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL last_light_value()")
    light = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.execute("CALL last_wind_value()")
    wind = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.close()
    dbconn.close()

    consumption = solarObject.consume + eolicObject.consume

    #SEND JAVASCRIPT
    data = [time() * 1000, int(light[0]), int(wind[0]), solarObject.storage, eolicObject.storage, consumption, chargeTime.usage, chargeTime.solar, chargeTime.eolic]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/triggers', methods=["GET", "POST"])
def triggers():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL get_actuator_state('city_lights')")
    clights = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.execute("CALL get_actuator_state('solar')")
    solar = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.execute("CALL get_actuator_state('eolic')")
    eolic = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.execute("CALL get_actuator_state('passive')")
    passive = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.execute("CALL get_actuator_state('watering')")
    watering = c.fetchone()
    while (dbconn.next_result()):
        print()

    c.close()
    dbconn.close()

    #SEND JAVASCRIPT
    return jsonify({"clights": clights[0], "solar":solar[0] , "eolic":eolic[0], "watering":watering[0], "passive":passive[0]})

@app.route('/rulesvalues', methods=["GET", "POST"])
def rulesvalues():
    #SEND JAVASCRIPT
    return jsonify({"citylightstrigger":int(rules['city_lights']), "eolictrigger":int(rules['eolic']), "solartrigger":int(rules['solar']), "wattrigger":int(rules['watering'])})

@app.route('/citylights', methods=["GET", "POST"])
def citylights():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL get_actuator_state('city_lights')")
    clights = c.fetchone()
    while (dbconn.next_result()):
        print()

    if clights[0]=='on':
        requests.insert(0,"usercloff")
    else:
        requests.insert(0, "userclon")

    c.close()
    dbconn.close()

    data = []
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/watering', methods=["GET", "POST"])
def watering():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL get_actuator_state('watering')")
    watering = c.fetchone()
    while (dbconn.next_result()):
        print()

    if watering[0]=='off':
        requests.insert(0,"userwatering")

    c.close()
    dbconn.close()

    data = []
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/energy', methods=["GET", "POST"])
def energy():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL get_actuator_state('solar')")
    sol = c.fetchone()
    while (dbconn.next_result()):
        print()

    if sol[0]=='on':
        requests.insert(0, "usereolic")
    else:
        requests.insert(0, "usersolar")

    c.close()
    dbconn.close()

    data = []
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/passivemode', methods=["GET", "POST"])
def passivemode():
    dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
    c = dbconn.cursor()
    c.execute("CALL get_actuator_state('passive')")
    passive = c.fetchone()
    while (dbconn.next_result()):
        print()

    if passive[0]=='on':
        requests.insert(0, "passiveOff")
    else:
        requests.insert(0, "passiveOn")

    c.close()
    dbconn.close()

    data = []
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/updatetriggers ', methods=['GET', 'POST'])
def updatetriggers():
    if request.method == 'POST':
        citylights = request.form['cltrigger']
        solar = request.form['solartrigger']
        eolic = request.form['eolictrigger']
        watering = request.form['wattrigger']


        if (int(citylights) <= 100 and int(citylights) >= 0) and (int(solar) <= 100 and int(solar) >= 0) and (int(eolic) <= 100 and int(eolic) >= 0) :
            dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
            c = dbconn.cursor()
            c.execute("CALL update_trigger('city_lights','" + str(citylights)+ "')")
            c.execute("CALL update_trigger('solar','" + str(solar) + "')")
            c.execute("CALL update_trigger('eolic','" + str(eolic) + "')")
            c.execute("CALL update_trigger('watering','" + str(watering) + "')")
            dbconn.commit()

            c.close()
            dbconn.close()

        RulesSetup()

    data = []
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':

    RulesSetup()
    t1 = Thread(target=RequestsToServer)
    t2 = Thread(target=ResponsesFromServer)
    t3 = Thread(target=EnergyManagement)
    t1.start()
    t2.start()
    t3.start()


    app.run(host='0.0.0.0', port=FLASK_PORT)
