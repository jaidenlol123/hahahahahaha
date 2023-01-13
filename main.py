import requests
from bs4 import BeautifulSoup
import random
import string
import colorama
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
colorama.init()


def check_url(url, count):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        songtitle = soup.find('div', {'class': 'songtitle'})
        if songtitle:
            if 'mp3' in songtitle.text:
                with open("mp3_files.txt", "a") as file:
                    file.write(f"{songtitle.text} - {url}\n")
                print(Fore.GREEN + "[+] " + Style.RESET_ALL, f"{songtitle.text} - {url} - mp3 file found and written to file", f"({count})")
            else:
                with open("no_file_found.txt", "a") as file:
                    file.write(f"{url}\n")
                print(Fore.RED + "[-] " + Style.RESET_ALL, f"{songtitle.text} - {url} - No File Found", f"({count})")
    except:
        with open("error_occured.txt", "a") as file:
            file.write(f"{url}\n")
        print(Fore.RED + "[-] " + Style.RESET_ALL, f"{url} - Error Occurred", f"({count})")


count = 0
generated_strings = set()
lowercase_chars = string.ascii_lowercase + string.digits
with ThreadPoolExecutor(max_workers=500) as executor:
    while True:
        random_string = ''.join(random.choices(lowercase_chars, k=32))
        if random_string in generated_strings:
            continue
        generated_strings.add(random_string)
        url = f"https://onlyfiles.io/f/{random_string}"
        count += 1
        executor.submit(check_url, url, count)
