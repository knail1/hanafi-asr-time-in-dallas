from flask import Flask
from flask import render_template
import requests
import tempfile
import PyPDF2
from tabula import wrapper
#from config import Config
from flask_bootstrap import Bootstrap
import datetime

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
    pdfFileObj = open(pdfFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pageObj = pdfReader.getPage(0)
    #print(pageObj.extractText())
    #print(pdfReader.numPages
    #df = wrapper.read_pdf(pdfFile, output_format = "json")
    df = wrapper.read_pdf(pdfFile,
                          spreadsheet = True,
                          area = (136.43, 58.64, 602.63, 554.93))
    #top, left, bottom, right
    #csvTimes = wrapper.convert_into(FILENAME, "output.csv", output_format="csv", pages='all')

    return(df)
    #return((csvTimes, df))





@app.route('/')
def todaysPrayerTimes():
    aprilUri = 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf'
    pdfFileName = pullPdf(aprilUri)
    df_output = pdfParser(pdfFileName)

    #parsed = json.loads(df_output)
    #parsed = json.load(df)
    #print(parsed)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    print(df_output)

    currentDT = datetime.datetime.now()
    currentDay = int(currentDT.strftime("%d"))

    if df_output.columns[1] == currentDT.strftime("%B"):
        asrTiming = df_output.iloc[21][6]


    return render_template('index.html', title='PrayerSched', asrTiming = asrTiming, table=df_output.to_html(index=False))


if __name__ == '__main__':
    app.run()