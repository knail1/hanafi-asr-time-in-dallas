from flask import Flask
from flask import render_template
import requests
import tempfile
import PyPDF2
from tabula import wrapper
import pandas as pd
#from config import Config
from flask_bootstrap import Bootstrap
import datetime

from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
import json

#import os

FILENAME = 'pdf.pdf'
DAILY_TIME_LOCAL_STORAGE_DIRECTORY = 'localFiles'
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
                          # (top,left,bottom,right).
                          #area = (136.43, 58.64, 602.63, 554.93))
                          area = (129.52, 59.99, 602.63, 553.13))
    #top, left, bottom, right
    df = pd.DataFrame(data=df)
    return(df)



def selectURI(x):
    return {
        'January': 'http://masjidyaseen.org/wp-content/uploads/2019/01/January-2020.pdf',
        'Febuary': 'http://masjidyaseen.org/wp-content/uploads/2019/02/Febuary-2020.pdf',
        'March': 'http://masjidyaseen.org/wp-content/uploads/2019/03/March-2020.pdf',
        'April': 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2020.pdf',
        'May': 'http://masjidyaseen.org/wp-content/uploads/2019/05/May-2019.pdf',
        'June': 'http://masjidyaseen.org/wp-content/uploads/2019/06/June-2019.pdf',
        'July': 'http://masjidyaseen.org/wp-content/uploads/2019/07/July-2019.pdf',
        'August': 'http://masjidyaseen.org/wp-content/uploads/2019/08/August-2019.pdf',
        'September': 'http://masjidyaseen.org/wp-content/uploads/2019/09/September-2019.pdf',
        'October': 'http://masjidyaseen.org/wp-content/uploads/2019/10/October-2019.pdf',
        'November': 'http://masjidyaseen.org/wp-content/uploads/2019/11/November-2019.pdf',
        'December': 'http://masjidyaseen.org/wp-content/uploads/2019/12/December-2019.pdf',

        }[x]

def writeTodaysPrayerTimes(currentDT, df):
    day = currentDT.strftime("%d")
    month = currentDT.strftime("%B")
    year = currentDT.strftime("%Y")
    fileName = month + "-" + day + "-" + year
    fullFilePath = DAILY_TIME_LOCAL_STORAGE_DIRECTORY + "/" +fileName
    exists = os.path.isfile(fullFilePath)
    if exists:
        pass
    else:
        df.to_csv(path_or_buf=fullFilePath)

    return(fullFilePath)



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
        fajrTiming = df_output.iloc[currentDay][3]
        sunRise = df_output.iloc[currentDay][4]
        duhrTiming = df_output.iloc[currentDay][5]
        asrTiming = df_output.iloc[currentDay][6]
        maghribTiming = df_output.iloc[currentDay][7]
        ishaTiming = df_output.iloc[currentDay][8]


    return render_template('index.html',
                           title='PrayerSched',
                           fajrTiming = fajrTiming,
                           sunRise = sunRise,
                           duhrTiming = duhrTiming,
                           asrTiming = asrTiming,
                           maghribTiming = maghribTiming,
                           ishaTiming = ishaTiming,
                           table=df_output.to_html(index=False))


@app.route('/ramadan')
def ramadan_todaysPrayerTimes():
    currentDT = datetime.datetime.now()

    ramadanURI = 'http://masjidyaseen.org/wp-content/uploads/2019/05/Ramadan-1440.pdf'
    #aprilUri = 'http://masjidyaseen.org/wp-content/uploads/2019/04/April-2019.pdf'
    #mayUri = 'http://masjidyaseen.org/wp-content/uploads/2019/05/May-2019.pdf'
    #theUri = selectURI(currentDT.strftime("%B"))
    theUri = ramadanURI
    pdfFileName = pullPdf(theUri)
    df_output = pdfParser(pdfFileName)
    print(df_output)
    print("---")

    currentDay = int(currentDT.strftime("%d")) + 25 # fixing index of the new cut table
    print(df_output.iloc[currentDay][3])

    #~~~~~NEW CODE FOR LOCAL CACHE READ IN
    fileWithTodaysTimings = writeTodaysPrayerTimes(currentDT,df_output.iloc[currentDay])
    df_output_back = pd.DataFrame.from_csv(fileWithTodaysTimings)
    df_dict = df_output_back.to_dict()

    #~~~~~

    #if df_output.columns[1] == 'May/June':
    #    fajrTiming = df_output.iloc[currentDay][3]
    #    sunRise = df_output.iloc[currentDay][4]
    #    duhrTiming = df_output.iloc[currentDay][5]
    #    asrTiming = df_output.iloc[currentDay][6]
    #    maghribTiming = df_output.iloc[currentDay][7]
    #    ishaTiming = df_output.iloc[currentDay][8]
    fajrTiming = df_dict['AMADAN']['Fajr']
    sunRise = df_dict['AMADAN']['Sunrise']
    duhrTiming = df_dict['AMADAN']['Dhuhr']
    asrTiming = df_dict['AMADAN']['Asr']
    maghribTiming = df_dict['AMADAN']['Maghrib']
    ishaTiming = df_dict['AMADAN']['Isha']


    return render_template('index.html',
                           title='PrayerSched',
                           fajrTiming = fajrTiming,
                           sunRise = sunRise,
                           duhrTiming = duhrTiming,
                           asrTiming = asrTiming,
                           maghribTiming = maghribTiming,
                           ishaTiming = ishaTiming,
                           table=df_output.to_html(index=False))

if __name__ == '__main__':
    app.run(debug=True)