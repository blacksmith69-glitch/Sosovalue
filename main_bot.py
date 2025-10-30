import requests
import base64
import mail
import time
import os
import random
import string

logo = f"""

█████╗ ██████╗  █████╗ ███████╗ █████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
███████║██████╔╝███████║█████╗  ███████║   ██║
██╔══██║██╔══██╗██╔══██║██╔══╝  ██╔══██║   ██║
██║  ██║██║  ██║██║  ██║██║     ██║  ██║   ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝
----------------------------------------------------
> TG CHANNEL :  @cryptowitharyanog
> YouTube    :  @cryptowitharyan
\033[1;34m------------------------------------------\033[0m"""

os.system('clear')
print(logo)
base_url = input('> Input base url : ')
refcode = input('> Referral code : ')
print('\033[1;34m------------------------------------------\033[0m')

def generate_password(length=8):
    if length < 8:
        length = 8

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("@#$&")

    remaining = ''.join(random.choices(string.ascii_letters + string.digits + "@#$&", k=length - 4))

    password = upper + lower + digit + special + remaining
    encoded_password = base64.b64encode(password.encode()).decode()
    return encoded_password

used_proxies = []

def get_random_proxy():
    global used_proxies
    with open('proxy.txt', 'r') as file:
        proxies = file.read().splitlines()
    total_proxies = len(proxies)
    if len(used_proxies) >= total_proxies:
        return 'All proxies used from `proxy.txt`'

    while True:
        proxy = random.choice(proxies)
        if proxy not in used_proxies:
            used_proxies.append(proxy)
            return {'http': proxy, 'https': proxy}

def create_account(captcha_token, password, email, proxy):
    headers = {
        'Host': 'm.sosovalue.com',
        'sec-ch-ua-platform': 'Android',
        'user-device': 'Chrome/131.0.6778.260#Android/15',
        'accept-language': 'en',
        'sec-ch-ua': 'Android',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15; 23129RAA4G Build/AQ3A.240829.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.260 Mobile Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://m.sosovalue.com',
        'x-requested-with': 'mark.via.gp',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.sosovalue.com/',
        'priority': 'u=1, i'
    }
    json_data = {
        'password': password,
        'rePassword': password,
        'username': 'NEW_USER_NAME_02',
        'email': email
    }
    params = {
        'cf-turnstile-response': captcha_token,
    }
    response = requests.post(
        'https://gw.sosovalue.com/usercenter/email/anno/sendRegisterVerifyCode/V2',
        params=params,
        headers=headers,
        json=json_data,
        proxies=proxy
    ).json()
    return response

def verify_email(password, email, code, refcode, proxy):
    headers = {
        'Host': 'gw.sosovalue.com',
        'sec-ch-ua-platform': 'Android',
        'user-device': 'Chrome/131.0.6778.260#Android/15',
        'accept-language': 'en',
        'sec-ch-ua': 'Android',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 15; 23129RAA4G Build/AQ3A.240829.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.260 Mobile Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://m.sosovalue.com',
        'x-requested-with': 'mark.via.gp',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.sosovalue.com/',
        'priority': 'u=1, i',
    }
    json_data = {
        'password': password,
        'rePassword': password,
        'username': 'NEW_USER_NAME_02',
        'email': email,
        'verifyCode': code,
        'invitationCode': refcode,
        'invitationFrom': 'null'
    }
    response = requests.post(
        'https://gw.sosovalue.com/usercenter/user/anno/v3/register',
        headers=headers,
        json=json_data,
        proxies=proxy
    ).json()
    return response

def console(mail, password, code):
    return 'ok'

def get_captcha():
    global base_url
    while True:
        token = requests.get(f'{base_url}/get').text
        if token != "No tokens available":
            return token
        else:
            time.sleep(0.3)

while True:
    try:
        email = mail.getmails()
        print('> \033[1;32mNew email :', email)
        password = generate_password()
        decpass = str(base64.b64decode(password.encode())).replace("b'", '').replace("'", '')
        print('\033[0m> \033[1;32mPassword :', decpass)
        captcha_token = get_captcha()
        proxy = get_random_proxy()
        if 'All proxies used' in proxy:
            print('\033[1;31mAll proxies used now! Ending.')
            break
        create_account_response = create_account(captcha_token, password, email, proxy)
        if create_account_response['code'] == 0:
            print(f'\033[0m>\033[1;32m Email sent successfully \033[0m')
        username, domain = email.split('@')
        code = mail.get_verification_link(email, domain)
        verify_response = verify_email(password, email, code, refcode, proxy)
        with open('accounts.txt', 'a') as file:
            file.write(f"Email : {email} \nPassword : {decpass} \nToken : {verify_response['data']['token']}\nRefresh Token : {verify_response['data']['refreshToken']}\n--------------------------------\n")
        if verify_response['code'] == 0:
            print(f'>\033[1;32m Email verified successfully \033[0m')
        print(f"\033[1;34m{'-' * 42}\033[0m")
    except Exception as e:
        print('\033[0m> \033[1;31mError :', str(e) + '\033[1;34m------------------------------------------\033[0m')
