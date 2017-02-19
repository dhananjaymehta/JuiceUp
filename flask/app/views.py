from app import app
from flask import render_template 
from flask import request, jsonify
import json, datetime
from elasticsearch import Elasticsearch

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("stations.html",title='Juice Up')

@app.route('/email')
def email():
 return render_template("email.html")

@app.route('/getNearestStations', methods=['GET'])
def getNearestStations():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    latlon = str(lat) + "," + str(lon)
    print " In here ==> lat : " +  lat + "   lon : " + lon
    es = Elasticsearch("http://ec2-52-36-245-111.us-west-2.compute.amazonaws.com:9200", http_auth=('elastic', 'changeme'), verify_certs=False)
    INDEX_NAME = 'geo_charging_stn_loc'

    q = '{"query":{"bool":{"must" : {"match_all" : {}},"filter":{"geo_distance":{"distance":"10km","location":"'+ latlon +'"}}}}}'
    #q = '{"query": {"match_all": {} } }'
    #, "filter":{"geo_distance": {"distance":"10km", "location" : ' + latlon + ' }}}'    
    print " Query  === " + q 
    result = es.search(index = INDEX_NAME, size=10, body=q)
    lines = json.dumps(result['hits']['hits'])
    print lines
    return lines
    #return render_template("stations.html", data=lines)
    

@app.route('/realtime')
def realtime():
 return render_template("realtime.html")

if __name__ == "__main__":
    app.run(debug=True)
