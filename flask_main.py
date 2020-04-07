from flask import Flask, make_response, request, send_file,render_template
import os
import pandas as pd
import SentimentAnalysis
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
	if request.method == "POST":
		global SIZE
		print(SIZE)
		input("skjvnksdjvn")
		SentimentAnalysis.fetch_tweets(request.form['fetch_tweet'],SIZE)
		return render_template('keyword.html')
	else:
		return render_template("keyword.html")


@app.route('/excel.html',methods=['GET', 'POST'])
def upload_route_summary():
	if request.method == 'POST':
		f = request.files['fileupload']
		print(f)
		input()
		THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
		filename_path = os.path.join(THIS_FOLDER, f.filename)
		SentimentAnalysis.uploaded_file(filename_path)
		return render_template('excel.html')


@app.route('/tweet.html',methods=['GET', 'POST'])
def tweets_number():
	if request.method == 'POST':
		global SIZE
		# Create variable for uploaded file
		f = request.form['fetch_tweet_num']
		SIZE=f
		print(SIZE)
		return render_template('excel1.html')

@app.route('/pastdata.html')
def contact():
	return "hello world"



if __name__ == '__main__':
   app.run(debug = True)