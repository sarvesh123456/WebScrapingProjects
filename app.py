from flask import Flask,render_template,request,jsonify,send_file
import FutureBridgeScraping
import time
import os

app=Flask(__name__)

@app.route('/',methods=['GET'])
def start():
    return render_template('index.html')

@app.route('/fileDownload/<downloadLink>',methods=['GET'])
def fileDownload(downloadLink):
    return send_file(downloadLink,attachment_filename=downloadLink)

@app.route('/send',methods=['GET','POST'])
def startScraping():
    if request.method=='POST':
        fileName=request.form['fileName']+str(time.time())+'.xlsx'
        try:
            if request.form['link']=='Future Bridge':
                FutureBridgeScraping.scrapeData1(1,1,fileName,request.form['ImagePrefix'])
            else:
                FutureBridgeScraping.scrapeData2(1,1,fileName,request.form['ImagePrefix'])
            return fileName
        except:
            return ''

if __name__=='__main__':
    app.run(debug=True,host='149.28.144.146')
