import os
import sys
import threading
import time


if __name__ == '__main__':
	ipBase = sys.argv[1]
	addIpStr = '.'.join(ipBase.split('.')[:3])

	print("Starting...")
	for i in range(255):
		threading.Thread(target=os.system, args=(f"ping {addIpStr}.{i}",)).start()

	while True: time.sleep(1)
