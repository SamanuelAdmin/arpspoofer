import scapy.all as scapy

import threading
import time
import os

# from colorama import init
# init(autoreset=True)
# from colorama import Fore, Back, Style
from tabulate import tabulate


foundedHosts = []

def scan(ip):
	global foundedHosts

	arpPacket = scapy.ARP( # arp request WHO HAS (1) (as default)
			pdst = ip 
		)

	# print(Fore.YELLOW + "[INFO] " + arpPacket.summary())

	broadcast = scapy.Ether(
		dst="ff:ff:ff:ff:ff:ff" # destination (who will take)
	) # outer shell for sending pack
	# print(Fore.YELLOW + "[INFO] " + broadcast.summary())

	arpPush = broadcast / arpPacket
	# print(Fore.YELLOW + "[INFO] " + arpPush.summary())

	aliveHosts = scapy.srp(arpPush, timeout=10, verbose=False)[0]

	for host in aliveHosts:
		if host not in foundedHosts: foundedHosts.append(host)


def printHosts():
	global foundedHosts

	while True:
		tableData = []
		for hostId in range(len(foundedHosts)):
			tableData.append([hostId, foundedHosts[hostId].answer.psrc, foundedHosts[hostId].answer.hwsrc])

		print(tabulate(tableData, headers=["ID", "IP", "MAC"], tablefmt="grid"))

		time.sleep(10)
		os.system("clear")



def main():
	threading.Thread(target=printHosts, daemon=True).start()

	while True:
		scan("192.168.0.0/24")
		time.sleep(1)

if __name__ == '__main__': 
	try: main()
	except KeyboardInterrupt: exit()

