import datetime
import os
import time

while True:
	with open("/tmp/log", "a") as f:
		f.write(str(datetime.datetime.now())+ "\n")
	time.sleep(1)