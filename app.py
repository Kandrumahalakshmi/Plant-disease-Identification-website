from flask import Flask, render_template, jsonify, request, Markup
from model import predict_image
import utils
import serial_rx_tx
import _thread
import os
import time
import urllib.request

str_message=''
serialPort = serial_rx_tx.SerialPort()
app = Flask(__name__)

def OpenCommand():

        comport = 'COM5'
        baudrate = '9600'
        serialPort.Open(comport,baudrate)
        #serialPort.Close()


def SendDataCommand(cmd):
    message = str(cmd)
    if serialPort.IsOpen():
        #message += '\r\n'
        serialPort.Send(message)

OpenCommand()
time.sleep(2)
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print('Res:'+ prediction)

            SendDataCommand(prediction)

            res = Markup(utils.disease_dic[prediction])
            return render_template('display.html', status=200, result=res)
        except:
            pass
    return render_template('index.html', status=500, res="Internal Server Error")


if __name__ == "__main__":
    app.run(debug=False)
