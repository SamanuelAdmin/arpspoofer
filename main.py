import requests
from bs4 import BeautifulSoup

import random

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem



API_URL = 'https://www.1secmail.com/api/v1/'


# user agent randomizer configs
uarSoftwareNames = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.ANDROID.value]
uarOperatingSystems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
userAgentRandomizer = UserAgent(software_names=uarSoftwareNames, operating_systems=uarOperatingSystems)

def getRandomUserAgent():
    return userAgentRandomizer.get_random_user_agent()


def ask2api(**kwargs) -> requests.Response:
    customHeaders = {
        'User-Agent': getRandomUserAgent(),
    }

    customParams = {}

    for key, value in kwargs.items():
        customParams[key] = str(value)

    return requests.get( API_URL, params=customParams, headers=customHeaders )


def getRandomMails(count=10) -> list[str]:
    r = ask2api(action="genRandomMailbox", count=count)

    if r.status_code == 200:
        return r.json()


def getMessages(mail: str) -> list[dict]|int:
    username, domain = mail.split('@')
    r = ask2api(action="getMessages", login=username, domain=domain)

    if r.status_code == 200:
        return r.json()
    return r.status_code

def readMessage(mail: str, _id: int) -> dict|int:
    username, domain = mail.split('@')
    r = ask2api(action="readMessage", login=username, domain=domain, id=_id)

    if r.status_code == 200:
        return r.json()

    return r.status_code


def authAccount(authCode: str) -> bool:
    r = requests.get(
        f'https://socialgrowthsmm.com/auth/activation/{authCode}',
            headers={
                'user-agent': getRandomUserAgent(),
            }
    )

    if r.status_code == 200:
        if 'Congratulations! Your Registration is Now Complete' in r.text:
            return True


def getRandomString(letters = 'abcdefghijklmnopqrstuvwxyz', length=24):
    return ''.join(random.choice(letters) for i in range(length))


def main():
    mails = getRandomMails(count=1000)

    for mail in mails:
        userAgent = getRandomUserAgent()

        # create account details
        username = getRandomString()
        lastname = getRandomString()
        password = getRandomString()
        token = 'e5344d48cae7be4ff8389be1b4049f46'

        session = requests.Session()
        session.headers.update(
            {
                'user-agent': userAgent,
            }
        )

        getCsrfR = session.get(
            'https://socialgrowthsmm.com/auth/signup',
            headers={'user-agent': userAgent}
        )
        if getCsrfR.status_code != 200:
            continue

        token = getCsrfR.cookies['token']
        csrfToken = getCsrfR.cookies['csrfToken']

        session.cookies.set('token', token)
        session.cookies.set('csrfToken', csrfToken)

        # request for generate account
        r = session.post(
            'https://socialgrowthsmm.com/auth/ajax_sign_up',
            data={
                'first_name': username,
                'last_name': lastname,
                'email': mail,
                'password': password,
                're_password': password,
                'timezone': random.choice(['Europe/Kyiv', 'Pacific/Niue', 'Pacific/Honolulu', 'America/Menominee', 'America/Mexico_City', 'America/Atikokan']),
                'terms': 'on',
                'token': token,
            },
            headers={
                'user-agent': userAgent,
                'referer': 'https://socialgrowthsmm.com/auth/signup',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Connection': 'keep-alive',
                'Host': 'socialgrowthsmm.com',
                'Origin': 'https://socialgrowthsmm.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Alt-Used': 'socialgrowthsmm.com'
            }
        )
        if r.status_code != 200:
            continue

        if r.json()['status'] != 'success': continue


        # read last message for verif an account
        messages = getMessages(mail)

        if type(messages) != int:
            message = readMessage(mail, messages[0]['id'])
            authCode = message['body'].split('https://socialgrowthsmm.com/auth/activation/')[1].split(' ')[0]

            if authAccount(authCode):
                print(f'Created account with {mail} : {password}')


if __name__ == '__main__': main()