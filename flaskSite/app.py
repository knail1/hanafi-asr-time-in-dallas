from flask import Flask
from flask import render_template
import requests
import tempfile
import PyPDF2
from tabula import wrapper
import json

#import os

FILENAME = 'pdf.pdf'

app = Flask(__name__)

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
    df = wrapper.read_pdf(pdfFile)
    return(df)





@app.route('/')
def hello_world():
    aprilUri = 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf'
    pdfFileName = pullPdf(aprilUri)
    df_output = pdfParser(pdfFileName)

    #parsed = json.loads(df_output)
    #parsed = json.load(df)
    #print(parsed)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    return render_template('index.html', title='PrayerSched', table=df_output)


if __name__ == '__main__':

    app.run()
