from flask import Flask, make_response, request, send_file,render_template
import os
import pandas as pd
import SentimentAnalysis
app = Flask(__name__)


@app.route('/')
@app.route('/test')
def test():
   return render_template('test.html')

@app.route('/excel.html')
def excel():
   return render_template('excel.html')

@app.route('/keyword.html', methods=['GET', 'POST'])
def keyword():
	if request.method == "POST":
		SentimentAnalysis.fetch_tweets(request.form['fetch_tweet'],10)
		return render_template('keyword.html')
	else:
		return render_template("keyword.html")


@app.route('/upload.html',methods=['GET', 'POST'])
def upload_route_summary():
	if request.method == 'POST':

		# Create variable for uploaded file
		f = request.files['fileupload']
		print(f)
		THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		filename_path = os.path.join(THIS_FOLDER, f.filename)
		SentimentAnalysis.uploaded_file(filename_path)
		return render_template('excel.html')



if __name__ == '__main__':
   app.run(debug = True)