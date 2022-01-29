#!/usr/bin/env python

import os
from random import randrange, seed
from datetime import datetime, timedelta
from flask import Flask, request, render_template, Response


app = Flask(__name__)


def read_values(file_path):
    result = {}

    if not os.path.exists(file_path):
        return result

    with open(file_path) as database:
        for line in database:
            name, var = line.partition("=")[::2]
            result[name.strip()] = var

    return result


def write_values(file_path, values):
    with open(file_path, "w+") as database:
        for key, value in values.items():
            if key == '':
                continue
            database.write("%s=%s\n" % (key, value))


@app.route('/health')
def health():
    global failure_time

    if datetime.now() > failure_time:
        return Response("Failure", status=500)

    return Response("OK", status=200)


@app.route('/', methods=['GET', 'POST'])
def index():
    global failure_time

    if datetime.now() > failure_time:
        return Response("Failure", status=500)

    if request.method == 'GET':

        db = read_values(db_file)

        return render_template(
            "index.html",
            value1=int(db[button1_name]),
            value2=int(db[button2_name]),
            button1=button1_name,
            button2=button2_name,
            title=title
        )

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':

            db = { button1_name: 0, button2_name: 0 }
            write_values(db_file, db)

            return render_template(
                "index.html",
                value1=int(db[button1_name]),
                value2=int(db[button2_name]),
                button1=button1_name,
                button2=button2_name,
                title=title
            )

        else:

            db = read_values(db_file)

            button_name = request.form['vote']
            db[button_name] = int(db[button_name]) + 1
            write_values(db_file, db)

            return render_template(
                "index.html",
                value1=int(db[button1_name]),
                value2=int(db[button2_name]),
                button1=button1_name,
                button2=button2_name,
                title=title
            )


app.config.from_pyfile('config_file.cfg')
button1_name = app.config['VOTE1VALUE']
button2_name = app.config['VOTE2VALUE']
db_file = app.config['DB_PATH']
timeout_min = int(app.config['FAIL_TIMEOUT_MIN'])
timeout_max = max(int(app.config['FAIL_TIMEOUT_MAX']) - timeout_min, 1)
title = app.config['TITLE']

seed(datetime.now())
random_timeout = timeout_min + randrange(timeout_max)
failure_time = datetime.now() + timedelta(minutes=random_timeout)
print("The application will fail at %s." % failure_time)

if not os.path.exists(os.path.dirname(db_file)):
    os.makedirs(os.path.dirname(db_file))
db = read_values(db_file)
if button1_name not in db:
    db[button1_name] = 0
if button2_name not in db:
    db[button2_name] = 0
write_values(db_file, db)

if __name__ == "__main__":
    app.run()
