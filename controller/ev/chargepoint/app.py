from flask import Flask, request
import cp

app = Flask(__name__)

@app.route("/api/v1/load/<id>")
def get_load(id):
    """
    Get current load
    Note id will be parsed to extract a group of stations if specified
    or a station, or a port on a station
    """
    cp.get_load(id)
    return "Get load called on: " + id


@app.route("/api/v1/curtail/<id>", methods=['POST'])
def curtail(id):
    """
    Curtail a port given ID in URL and curtail type/amount in POST body.
    Note id will be parsed to extract a group of stations if specified
    or a station, or a port on a station
    {
        percentage: None,
        absolute: 50
    }
    """
    if request.method == 'POST':
        absolute_amount = request.form['absolute_amount']
        #percentage_amount = request.form['percentage_amount']
    
    cp.shed_load(id, absolute_amount = absolute_amount)
    return "Shed Load called on: " + id


@app.route("/api/v1/clear/<id>")
def clear(id):
    """
    Clear curtail given ID in URL 
    Note id will be parsed to extract a group of stations if specified
    or a station, or a port on a station
    """
   
    cp.clear_shed(id)
    return "Clear Shed called on: " + id


