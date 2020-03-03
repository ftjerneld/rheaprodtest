from flask import Flask, jsonify, request, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
  return 'Correct path: 192.168.4.1/rheaserver'

@app.route('/log')
def log():
  cf = open('log/testlog.csv','r')
  with cf:
    record = csv.DictReader(cf)
    columnNames=['MAC','Firmware','RSSI']
    return render_template('log.html', records=record, colnames=columnNames)

@app.route('/rheaserver/', methods=['GET'])
def rheaserver():
  if request.method == 'GET':
    mac = request.args.get('mac', default='NA')
    rssi = request.args.get('rssi', default='0')
    fw = request.args.get('fw', default='NA')
    plid = request.args.get('plid', default='NA') 

    f=open("log/testlog.csv","a+")
    with f:
      writer = csv.writer(f)
      writer.writerow([mac,fw,rssi])

  return jsonify(isError= False, 
                 message= "Success", 
                 statusCode= 200, 
                 mac= mac,
                 rssi= rssi,
                 fw= fw,
                 plid= plid), 200

if __name__ == '__main__':
  app.run(debug=True, port=80, host='0.0.0.0')

