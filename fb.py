import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import re

from sql import updatefirebasetomcu
objects = []
count = 0
details = dict()

class ListenerClass:
	def __init__(self, appname):
		self.appname = appname

	def listener(self, event):
	    # print(event.event_type)  # can be 'put' or 'patch'
	    # print(event.path)  # relative to the reference, it seems
	    # print(event.data)  # new data at /reference/event.path. None if deleted
	    # print(self.appname) # Extra data related to change add your own member variable

	    path = str(event.path)
	    data = str(event.data)
	    if '{' not in data:
	    	result = "{'" + path[1:] + "': '" + data + "'}"
	    	# print(f'Updating this one : {result}')
	    	updatefirebasetomcu(self.appname, result)
	    else:
	    	updatefirebasetomcu(self.appname, data)
	    	# print(f'Updating this on First time : ')
	    	# print(data)
# /:{'motor': 'on', 'n0': 'hello MCU'}
# /motor:off   # after one data change
def update(appname,data, path):
	path = path.replace('-','/')
	ref = db.reference('/',app= appname).child(path)
	value = dict()
	n = 0
	for i in data.split('_'):
		key = 'n' + str(n)
		n += 1
		value[key] = i
	ref.update(value)

def addtofirebase(json_path, url, data, path):
	global objects, count, details
	# print(f'JSON PATH : {json_path}')
	# print(f'URL : {url}')
	# print(f'Readings : {data}')
	
	p = r'//(.*)\.firebaseio'
	x = re.findall(p, url)
	# print(x[0])
	my_app_name = x[0]
	xyz = {'databaseURL': 'https://{}.firebaseio.com'.format(my_app_name),'storageBucket': '{}.appspot.com'.format(my_app_name)}
	# print(f'No of Objects : {len(objects)}')
	if my_app_name not in firebase_admin._apps:
		cred = credentials.Certificate(json_path)        
		obj = firebase_admin.initialize_app(cred,xyz , name=my_app_name)
		objects.append(obj)
		details[my_app_name] = count
		count += 1
		update(objects[details[my_app_name]], data, path)
		listenerObject = ListenerClass(my_app_name)
		db.reference('sendbacktomcu', app= obj).listen(listenerObject.listener)
		# print('reference sucess!')
	else:
		update(objects[details[my_app_name]], data, path)

	print(f'No of Existing Connections : {len(objects)}')	