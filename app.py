from flask import Flask
from flask import render_template
import requests
import tempfile
import PyPDF2
from tabula import wrapper
#from config import Config
from flask_bootstrap import Bootstrap
import datetime

from flask import Flask, render_template, request
from werkzeug import secure_filename

import json

#import os

FILENAME = 'pdf.pdf'

app = Flask(__name__)
bootstrap = Bootstrap(app)
#app.config.from_object(Config)

def pullPdf(uri):
    r = requests.get(uri)
    handle, filepath = tempfile.mkstemp()
    with open(FILENAME, 'wb') as f:
        f.write(r.content)
    return(FILENAME)

def pdfParser(pdfFile):
    df = wrapper.read_pdf(pdfFile,
                          spreadsheet = True,
                          area = (136.43, 58.64, 602.63, 554.93))
    #top, left, bottom, right

    return(df)



@app.route('/asr')
def todaysPrayerTimes():
    aprilUri = 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf'
    pdfFileName = pullPdf(aprilUri)
    df_output = pdfParser(pdfFileName)
    print(df_output)

    currentDT = datetime.datetime.now()
    currentDay = int(currentDT.strftime("%d"))

    if df_output.columns[1] == currentDT.strftime("%B"):
        asrTiming = df_output.iloc[21][6]


    return render_template('index.html', title='PrayerSched', asrTiming = asrTiming, table=df_output.to_html(index=False))


@app.route('/')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'



#app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)