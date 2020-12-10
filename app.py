import os
from flask import Flask, request, render_template, url_for, redirect
from os import listdir
import json
import re
from sql import adduser, getusers, clear, geturl, getfirebasetomcu
from werkzeug.utils import secure_filename

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_name = ''

def getprojectname(url):
	p = r'//(.*)\.firebaseio'
	x = re.findall(p, url)
	return x[0]

@app.route("/")
def index():
	print('/')
	return render_template("uploader.html") # upload to uploader


@app.route('/takeurl')
def take(): # calling this function and changing url
	return render_template('takeurl.html') # /takeinput to /takeurl

@app.route('/takeurl', methods=["GET", "POST"]) # /takeinput to /takeurl
def takk(): # to accept url of firebase
	print('/takeurl')
	global file_name
	url = request.form['firebaseurl']

	print(f'Filename or JSOn Name : {file_name}')
	print(f'URL  : {url}')

	print(file_name + '\n' + url)
	adduser(getprojectname(url), file_name.split('.')[0], url, 'Added Just Now!')
	# print(getusers())
	# return '<h1 style="color:green">Added Successfully..!</h1>'
	return render_template('sucess.html')

@app.route("/upload", methods=["GET", "POST"])
def upload():  # to accept json file | file uploader
	print('/upload')
	global file_name

	target = os.path.join(APP_ROOT, 'static')
	# print(f'Target : {target}')

	if not os.path.isdir(target):
		os.mkdir(target)
	
	if request.method =='POST':
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			print(filename)
			file_name = filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			return redirect(url_for('take'))
	return 'Some thing Wrong Happened File not found may be'


@app.route('/<jsonno>/<path>/<readings>') 
def mcutopython(jsonno, path,readings):
	try:
		s = jsonno + '/' + path + '/' + readings
		print(f'Requesting URL : {s}')
		json_path = os.path.join(os.path.join(APP_ROOT, 'static'), jsonno + '.json')
		# url = 'https://fyp-healthapp-project.firebaseio.com/'
		url = geturl(jsonno)
		if url:
			from fb import addtofirebase
			addtofirebase(json_path, url, readings, path)
		else:
			print('User Not Found!')
		# print(getusers())
		# print(geturl(jsonno))
		# return '<h1 style="color:green">Added to firebase Successfully..!</h1>'
		return getfirebasetomcu(getprojectname(url))
	except Exception as e:
		return e


if __name__ == "__main__":
    app.run(port=4555, debug=True, threaded=True)

#this will execute on app close
# conn.commit()
# conn.close()