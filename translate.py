import requests
from bs4 import BeautifulSoup
import sys
args = sys.argv

languages = ['All', 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

def single_translation():
    sub1 = f'{languages[your_lan].lower()}-{languages[dest_lan].lower()}'
    url = f'https://context.reverso.net/translation/{sub1}/{t_word}'

    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code:
        print(r.status_code, 'OK')

    soup = BeautifulSoup(r.content, 'html.parser')

    words = soup.find_all('a', {'class': 'translation'})
    phrases = soup.find_all('span', {'class': 'text'})
    words_list = [i.text.strip('\n ') for i in words]
    phrases_list = [i.text.strip('\n ') for i in phrases if '\n ' in i.text]
    if words_list == ['Translation']:
        print(f"Sorry, unable to find {t_word}")
    else:
        print()
        print(f'{languages[dest_lan]} Translations:')
        for word in words_list[1:6]:
            print(word)

        print()
        print(f'{languages[dest_lan]} Examples:')
        for i in range(0, 10, 2):
            print(phrases_list[i])
            print(phrases_list[i+1])
            print()
    

def translate_all():
    print()
    my_lan = languages[your_lan]
    out = open(f'{t_word.upper()}.txt', 'a', encoding='utf-8')

    for lan in languages:
        if lan in ('All', my_lan):
            continue
        
        sub1 = f'{my_lan.lower()}-{lan.lower()}'
        url = f'https://context.reverso.net/translation/{sub1}/{t_word}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html.parser')
        words = soup.find_all('a', {'class': 'translation'})
        phrases = soup.find_all('span', {'class': 'text'})
        words_list = [i.text.strip('\n ') for i in words]
        phrases_list = [i.text.strip('\n ') for i in phrases if '\n ' in i.text]
        
        if words_list == ['Translation']:
            print(f"Sorry, unable to find {t_word}")
            out.close()
            break
        else:
            print(f'{lan} Translations:', file=out, flush=True)
            print(words_list[1], file=out, flush=True)
            print('', file=out, flush=True)
    
            print(f'{lan} Examples:', file=out, flush=True)
            print(phrases_list[0], file=out, flush=True)
            print(phrases_list[1], file=out, flush=True)
            print('', file=out, flush=True)
    
            print(f'{lan} Translations:')
            print(words_list[1])
            print()
    
            print(f'{lan} Examples:')
            print(phrases_list[0])
            print(phrases_list[1])
            print()

    out.close()

try:
    your_lan = languages.index(args[1].capitalize())
except ValueError:
    print(f"Sorry, the program doesn't support {args[1]}")
else:
    try:
        dest_lan = languages.index(args[2].capitalize())
    except ValueError:
        print(f"Sorry, the program doesn't support {args[2]}")
    else:
        t_word = args[3]

        if requests.get("https://context.reverso.net/translation", headers={'User-Agent': 'Mozilla/5.0'}).status_code == False:
            print("Something wrong with your internet connection")
        else:
            if dest_lan == 0:
                translate_all()
            else:
                single_translation()


