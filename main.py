# -*- coding: cp1251 -*-
import flask
from db_cnxn import db_connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@db_connector()
def getvalues(cursor, number):
    if number < 5:
        return None
    code = str(number)[1:4]
    sub_num = str(number)[4:]

    cursor.execute(""" select * from phone_codes where code_id = %s and %s between range_s and range_e """, (code, sub_num))
    cdata = cursor.fetchone()
    return cdata


@app.route('/', methods=['GET'])
def home():
    """стартовая страница"""
    return "<h1>Check a phone number</h1><p>This site is a prototype API to check a phone number.</p>"

@app.route('/api/v1/number', methods=['GET'])
def api_id():
    #проверяем введен ли id
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    cdata = getvalues(number=id)

    result = {"Number: ": id, "Operator: ": cdata[5], "Region: ": cdata[6]} if cdata else "Enter existing number"
    return flask.jsonify(result)

app.run()