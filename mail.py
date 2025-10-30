import names
import random
import string,time
from bs4 import BeautifulSoup
import requests as curl_requests
from fake_useragent import UserAgent
def get_fake_chrome_ua(): return UserAgent().chrome


def get_headers(token=None):
    headers = {
        'accept': '/',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp',
        'priority': 'u=1, i',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': get_fake_chrome_ua()
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers
    
def get_random_domain():
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    keyword = random.choice(consonants) + random.choice(vowels)
    
    retry_count = 0
    MAX_RETRIES = 5
    while retry_count < MAX_RETRIES:
        try:
            response = curl_requests.get(
                f'https://generator.email/search.php?key={keyword}',
                headers=get_headers(),
                timeout=120
            )
            domains = response.json()
            valid_domains = [d for d in domains if all(ord(c) < 128 for c in d)]
            
            if valid_domains:
                selected_domain = random.choice(valid_domains)
                return selected_domain
            return None
            
        except Exception as e:
            return str(e)

def generate_email(domain):
    first_name = names.get_first_name().lower()
    last_name = names.get_last_name().lower()
    random_nums = ''.join(random.choices(string.digits, k=3))
    
    separator = random.choice(['', '.'])
    email = f"{first_name}{separator}{last_name}{random_nums}@{domain}"
    return email

def get_verification_link(email, domain):
    cookies = {
        'embx': f'[%22{email}%22]',
        'surl': f'{domain}/{email.split("@")[0]}'
    }
    
    max_attempts = 15
    retry_count = 0
    
    while retry_count < max_attempts:
        try:
            response = curl_requests.get(
                'https://generator.email/inbox1/',
                headers=get_headers(),
                cookies=cookies,
                timeout=120
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            code = False
            try:
               code = str(soup).split('SoSoValue - ')[1].split(' ')[0]
            except:
                pass
            if code:
                return code
            retry_count += 1
            
        except Exception as e:
            retry_count += 1
    return None

def getmails():
    while True:
      domi = get_random_domain()
      if domi:
         mail = generate_email(domi)
         return mail

