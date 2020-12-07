import os
from flask import Flask, request, render_template, url_for, redirect
from os import listdir
import json
import re
from sql import adduser, getusers, clear, geturl, getfirebasetomcu

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def getprojectname(url):
	p = r'//(.*)\.firebaseio'
	x = re.findall(p, url)
	return x[0]

@app.route("/")
def index():
	print('/')
	return render_template("upload.html")


@app.route('/takeinput')
def take(): # calling this function and changing url
	return render_template('takeinput.html')

@app.route('/takeinput', methods=["GET", "POST"])
def takk():
	print('/takeinput')
	global file_name
	url = request.form['firebaseurl']
	# print(file_name + '\n' + url)
	adduser(getprojectname(url), file_name.split('.')[0], url, 'Added Just Now!')
	# print(getusers())
	return '<h1 style="color:green">Added Successfully..!</h1>'

@app.route("/upload", methods=["GET", "POST"])
def upload():
	print('/upload')
	global file_name
	try:
		url = request.form['firebaseurl']
		# print(f'Firebase URL : {url}')
	except Exception as e:
		print(e)
	target = os.path.join(APP_ROOT, 'static')
	# print(f'Target : {target}')

	if not os.path.isdir(target):
		os.mkdir(target)
            
	for file in request.files.getlist("file"):
		filename = file.filename
		# print(f'File : {filename}')
		file_name = filename
		file.save(os.path.join(target, filename))
	return redirect(url_for('take'))

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