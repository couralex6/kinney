# Copyright Year(s) program was created VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

from flask import Flask, request
import cp
from constants import DEBUG, SUCCESS
import json
import logging

app = Flask(__name__)
SUCCESS = "100"


@app.route("/api/v1/load/<id>")
def get_load(id):
    """
    Get current load
    Note id will be parsed to extract a group of stations if specified
    or a station, or a port on a station
    """
    res = cp.get_load(id)
    if (res['responseCode'] == SUCCESS):
        if DEBUG:
            print("Successful: get_load(" + id + ")")
        return json.dumps(cp.process_load(res))
    else:
        logging.error("Error: get_load(" + id + ") "  + res['responseText'])
        return res['responseText']


@app.route("/api/v1/curtail/<id>", methods=['POST'])
def curtail(id):
    """
    Curtail a port given:
    - ID in URL  (could be a station-group, or a station, or a station with port) 
    - curtail amount as either absolute_amount or percentage_amount in POST body (defaults to 0, no charging)
    - curtail duration as time_interval in POST body  (defaults to 0, signifying endless)
    {
        percentage: None,
        absolute: 0
        time_interval: 0
    }
    """
    if request.method == 'POST':
        amount = request.form['amount']
        percentage = request.form['percentage']
        time_interval = request.form['time_interval']
    
    res = cp.shed_load(id, absolute_amount=amount, time_interval=time_interval)
    if (res['responseCode'] == SUCCESS):
        return "Success: Curtail on " + str(id)
    else:
        logging.error("Error: Curtail id: " + id + " " + res['responseText'])
        return res['responseText']



@app.route("/api/v1/clear/<id>")
def clear(id):
    """
    Clear curtail given ID in URL 
    Note id will be parsed to extract a group of stations if specified
    or a station, or a port on a station
    """
   
    res = cp.clear_shed(id)
    if (res['responseCode'] == SUCCESS):
        return "Successful: Clear on " + id 
    else:
        logging.error("Error: Clear shed id: " + id + " " + res['responseText'])
        return res['responseText'] 


