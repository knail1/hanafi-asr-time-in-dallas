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



def selectURI(x):
    return {
        'January': 'http://masjidyaseen.org/wp-content/uploads/2019/04/January-2020.pdf',
        'Febuary': 'http://masjidyaseen.org/wp-content/uploads/2019/04/Febuary-2020.pdf',
        'March': 'http://masjidyaseen.org/wp-content/uploads/2019/04/March-2020.pdf',
        'April': 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf',
        'May': 'http://masjidyaseen.org/wp-content/uploads/2019/05/May-2019.pdf',
        'June': 'http://masjidyaseen.org/wp-content/uploads/2019/05/June-2019.pdf',
        'July': 'http://masjidyaseen.org/wp-content/uploads/2019/05/July-2019.pdf',
        'August': 'http://masjidyaseen.org/wp-content/uploads/2019/05/August-2019.pdf',
        'September': 'http://masjidyaseen.org/wp-content/uploads/2019/05/September-2019.pdf',
        'October': 'http://masjidyaseen.org/wp-content/uploads/2019/05/October-2019.pdf',
        'November': 'http://masjidyaseen.org/wp-content/uploads/2019/05/November-2019.pdf',
        'December': 'http://masjidyaseen.org/wp-content/uploads/2019/05/December-2019.pdf',

        }[x]

@app.route('/')
def todaysPrayerTimes():
    currentDT = datetime.datetime.now()

    #aprilUri = 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf'
    #mayUri = 'http://masjidyaseen.org/wp-content/uploads/2019/05/May-2019.pdf'
    theUri = selectURI(currentDT.strftime("%B"))
    pdfFileName = pullPdf(theUri)
    df_output = pdfParser(pdfFileName)
    print(df_output)

    currentDay = int(currentDT.strftime("%d"))

    if df_output.columns[1] == currentDT.strftime("%B"):
        asrTiming = df_output.iloc[21][6]


    return render_template('index.html', title='PrayerSched', asrTiming = asrTiming, table=df_output.to_html(index=False))


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        # os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(secure_filename(f.filename))
        #return 'file uploaded successfully'
        return render_template('postUpload.html', fileName = f.filename)



#app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)