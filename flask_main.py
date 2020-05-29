from flask import Flask, make_response, request, send_file,render_template,redirect,url_for
import os
import pandas as pd
import SentimentAnalysis
from multiprocessing import Process
import os
app = Flask(__name__)
SIZE=0

@app.route('/')
@app.route('/test.html')
def test():
   return render_template('test.html')

@app.route('/excel.html')
def excel():
   return render_template('excel.html')

@app.route('/keyword.html', methods=['GET', 'POST'])
def keyword():
	data={'username':"23"}
	if request.method == "POST":
		global SIZE
		print(SIZE)
		if len(request.form['fetch_tweet'])==0:
			return render_template('keyword.html',data=data)
		SentimentAnalysis.fetch_tweets(request.form['fetch_tweet'],SIZE)
		return render_template('keyword.html',data=data)
	else:
		return render_template("keyword.html")


@app.route('/excel.html',methods=['GET', 'POST'])
def upload_route_summary():
	if request.method == 'POST':
		f = request.files['fileupload']
		print(f)
		THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		filename_path = os.path.join(THIS_FOLDER, f.filename)
		SentimentAnalysis.uploaded_file(filename_path)
		data={'username':"1"}
		return render_template('excel.html',data=data)


@app.route('/tweet.html',methods=['GET', 'POST'])
def tweets_number():
	if request.method == 'POST':
		global SIZE
		# Create variable for uploaded file
		f = request.form['fetch_tweet_num']
		SIZE=f
		print(SIZE)
		data={'username':"2"}
		return render_template('excel.html',data=data)

@app.route('/button.html',methods=['GET', 'POST'])
def button_click():
	print('button_file_upload' in request.form)
	#input()
	if request.method == 'POST':
		if 'button_file_upload' in request.form:
			data={'username':"1"}
			return render_template('excel.html',data=data)
		elif 'twitter_num_button' in request.form:
			data={'username':"2"}
			return render_template('excel.html',data=data)


@app.route('/pastdata.html')
def past_data():
	return render_template('pastdata.html')

@app.route('/dataanalysis.html')
def data_analysis():
	return render_template('dataanalysis.html')

@app.route('/contact.html')
def contact():
	return render_template('contact.html')

@app.route('/graph.html')
def graph():
	return render_template('graph.html')
	
if __name__ == '__main__':
   app.run(debug = True)