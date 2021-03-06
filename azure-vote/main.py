#!/usr/bin/env python

import os
from random import randrange, seed
from datetime import datetime, timedelta
from flask import Flask, request, render_template, Response
import csv

app = Flask(__name__)


def read_values(file_path):
    result = {}
    db = {}
    # checking whether file exists or not
    if not os.path.exists(file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
            # file not found message
            print("Created directory")
        #db = read_values(file_path)
        db[button1_name] = 0
        db[button2_name] = 0
        print("Intital db values %s." % db)
        write_values(file_path,db)

    #print("Reading file")
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            result = row

            
    return result


def write_values(file_path, values):
    with open(file_path, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=values.keys())
        writer.writeheader()
        writer.writerow(values)


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
            
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


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

read_values(db_file)

if __name__ == "__main__":
    app.run()