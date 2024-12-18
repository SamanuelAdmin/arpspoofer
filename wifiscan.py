from prettytable import PrettyTable
import wifi
import sys

def getCellView(cell):
    return {
        'ssid': cell.ssid,
        'encrypted': bool(cell.encrypted),
        'encryption_type': cell.encryption_type,
        'mode': cell.mode,
        'quality': cell.quality,
        'signal': cell.signal,
        'noise': cell.noise,
        'address': cell.address,
        'channel': cell.channel,
    }

def scan(adapterName:str):
    wifiNetworksScanResult = []

    wifi_scanner = wifi.Cell.all(adapterName)

    for cell in wifi_scanner:
        wifiNetworksScanResult.append(
            getCellView(cell)
        )

    return wifiNetworksScanResult

def sortBy(l: list[dict], sortname="signal"):
    return list(sorted(l, key=lambda x: int(x[sortname]) * -1))


def transformSsid(ssid):
    if ssid.strip("\x00") == "" or ssid == '':
        return '<HIDDEN SSID>'


def makeTable(info):
    table = PrettyTable()

    table.field_names = [
        "Encryption",
        "SSID", "Address", "Channel",
        "Quality", "Signal"
    ]

    for cellInfo in info:
        table.add_row(
            [
                cellInfo['encryption_type'] if cellInfo['encrypted'] else ' - ',
                cellInfo['ssid'] if cellInfo['ssid'].strip("\x00") != "" and cellInfo['ssid'] != '' else '<HIDDEN SSID>',
                cellInfo['address'], cellInfo['channel'],
                cellInfo['quality'], cellInfo['signal']
            ]
        )

    return table

def cellIsUninque(list, cell, checkname='address'):
    for el in list:
        if el[checkname] == cell[checkname]:
            return False

    return True

def main():
    args = sys.argv[1:]
    adapterName = args[0]

    networks = []
    scancount = 10

    for _ in range(10):
        print(f'Scanning [{_ + 1}/{scancount}]')
        scanResult = scan(adapterName)

        for cell in scanResult:
            if cellIsUninque(networks, cell):
                networks.append(cell)

        print(f'Found: {len(networks)}')

    result = sortBy(networks)

    print( makeTable(result) )
    print(f'Found network: {len(result)}')

if __name__ == '__main__': main()