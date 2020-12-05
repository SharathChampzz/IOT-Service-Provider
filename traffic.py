import urllib.request
from time import sleep
import random

jsonids = ['covid-warriors-ed9ec-firebase-adminsdk-amphh-677a486534', 'fyp-healthapp-project-firebase-adminsdk-40qfo-f8fc938674']

while True:
	for id in jsonids:
		url = 'http://127.0.0.1:4555/' + id + '/' + str(random.randint(0,100))
		contents = urllib.request.urlopen(url).read()
		sleep(3)