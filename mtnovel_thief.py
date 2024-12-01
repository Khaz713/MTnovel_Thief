import json
import os
import re
import time
from random import random, randint

import requests
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import cloudscraper

with open('list.json', 'r', encoding='utf-8') as f:
    novels = json.load(f)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.70',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Request Line': 'GET / HTTP/1.1',
    'Accept-Encoding': 'gzip, deflate'
}

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth) # at the end novel gets sent to google drive for ease of access on mobile

i = 0
novels_list = []
for novel in novels:
    # get all the novels on the list and checks if they are any new chapters of them
    i += 1
    flag = True
    while flag:
        try:

            scraper = cloudscraper.create_scraper()
            soup = BeautifulSoup(scraper.get(novels[novel]["url"]).text, 'html.parser')

            # every website has different layout so had to make a separate commands for all of them
            if "mtnovel" in novels[novel]["url"]:
                latest_chapters = soup.find('div', class_='l-chapter').find('a', href=True)
                latest_url = 'https://mtnovel.com' + latest_chapters['href']
                try:
                    latest_number = int(latest_chapters['title'].split('-')[0].split(' ')[1].strip())
                except Exception as e:
                    try:
                       latest_number = int(latest_chapters['title'].split(':')[0].split(' ')[1].strip())
                    except Exception as es:
                       latest_number = int(latest_chapters['title'].split(' ')[0])
            elif "allnovelfull" in novels[novel]["url"]:
                latest_chapters = soup.find('div', class_='l-chapter').find('a', href=True)
                latest_url = 'https://allnovelfull.com' + latest_chapters['href']
                try:
                    latest_number = int(latest_chapters['title'].split('-')[0].split(' ')[1].strip())
                except Exception as e:
                    latest_number = int(latest_chapters['title'].split(':')[0].split(' ')[1].strip())
            elif "readlightnovel" in novels[novel]["url"]:
                latest_chapters = soup.findAll('div', class_='novel-detail-body')[-1].find('a', href=True)
                latest_url = latest_chapters['href']
                latest_number = int(latest_chapters.text.strip().split(' ')[1])
            elif "noveltop1" in novels[novel]["url"]:
                latest_chapters = soup.find('div', class_='l-chapter').find('a', href=True)
                latest_url = latest_chapters['href']
                try:
                    latest_number = int(latest_chapters.text.strip().split(' ')[1])
                except ValueError:
                    latest_number = int(latest_chapters.text.strip().split(' ')[1].split('-')[0])
            elif "lightnovelpub" in novels[novel]["url"]:

                latest_chapters = soup.findAll('a', href=True)
                latest_url = "https://www.lightnovelpub.com" + latest_chapters[10]['href']
                try:
                    latest_number = int(latest_chapters[10].text.strip().split(' ')[1].split(':')[0])
                except ValueError:
                    latest_number = 0
            elif "novel84" in novels[novel]["url"]:
                latest_chapters = soup.find('div', class_='item').find('a', href=True)
                latest_url = latest_chapters['href']
                latest_number = int(latest_chapters.text.strip().split(' ')[1])
            elif "wuxiaz" in novels[novel]["url"]:
                latest_chapters = soup.find('div', class_='intro').find('a', href=True)
                latest_url = "https://www.wuxiaz.com" + latest_chapters['href']
                latest_number = int(latest_chapters.text.strip().split(' ')[1])
            novels_list.append([novel, latest_url, latest_number])

            flag = False
        except Exception as es:
            flag = True


    if novels[novel]['chapter'] < latest_number:
        new = f'<---NEW {latest_number - novels[novel]["chapter"]}!'
        print(f'{i}. {novel} {novels[novel]["chapter"]}/{latest_number} {new}')
    else:
        print(f'{i}. {novel} {novels[novel]["chapter"]}/{latest_number}')

selects = []
print('====================================================')
print('CHOOSE NOVELS, 0 TO START:')
while True:
    selects.append([int(x) for x in input().split()])
    if selects[-1][0] == 0:
        break
os.system('cls')
for select_2 in selects:
    if select_2[0] == 0:
        print('ALL DONE')
        break
    novel_name = novels_list[select_2[0] - 1][0]
    url = novels_list[select_2[0] - 1][1]
    latest_number = novels_list[select_2[0] - 1][2]
    current_number = latest_number - novels[novel_name]['chapter']

    chapters = []
    for i in range(current_number):
        flag = True
        while flag:
            scraper = cloudscraper.create_scraper()
            soup = BeautifulSoup(scraper.get(url).text, 'html.parser')
            try:
                if "mtnovel" in url:
                    chapter_title = soup.find('span', class_='chapter-text').text
                    chapter_raw = soup.find('div', class_='chapter-c').find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "allnovelfull" in url:
                    chapter_title = soup.find('span', class_='chapter-text').text
                    chapter_raw = soup.find('div', class_='chapter-c').find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "readlightnovel" in url:
                    chapter_title = soup.find('div', class_='desc').text.strip().splitlines()[0].strip()
                    chapter_raw = soup.find('div', class_='desc').find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "noveltop1" in url:
                    chapter_title = soup.find('a', class_='chr-title')['title']
                    chapter_raw = soup.find('div', class_='chr-c').find_all('p')
                    chapter_raw.pop(0)
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "lightnovelpub" in url:
                    chapter_title = soup.find('span', class_='chapter-title').text
                    chapter_raw = soup.find('div', id='chapter-container').find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "novel84" in url:
                    chapter_title = soup.find('a', class_='chr-title')['title']
                    chapter_raw = soup.find('div', class_='chr-c').find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                elif "wuxiaz" in url:
                    chapter_title = soup.find('div', class_='titles').find('h2').text
                    chapter_raw = soup.find('div', class_="chapter-content").find_all('p')
                    chapter = ['# ' + chapter_title + '\n\n']
                flag = False
            except Exception as es:
                os.system('cls')
                print('====================================================')
                sleep = randint(10, 30)
                for j in range(sleep):
                    loading = ''
                    percent = int(((j + 1) / sleep) * 100)
                    filled = int(percent / 10)
                    empty = 10 - int(percent / 10)
                    for k in range(filled):
                        loading += '\u25a0'
                    for k in range(empty):
                        loading += '\u25a1'
                    print(f'Waiting: [{loading}] {percent}%', end='\r', flush=True)
                    time.sleep(1)
                os.system('cls')
                print('====================================================')
                flag = True

        hidden_words = ['readlightnovel.me', 'lightno​velpub', 'lightno​velpub.com', 'lightno­', 'velpub.c',
                        'ʟɪɢʜᴛɴᴏᴠᴇʟᴘᴜʙ', 'Webnovel']
        hidden_words = re.compile("|".join(hidden_words))   # some websites insert their watermark between paragraphs

        for line in chapter_raw:
            try:
                line = line.text
            except Exception as e:
                pass
            # replacing some symbols for css escape sequence
            line = line.replace('<', '\\<')
            line = line.replace('>', '\\>')
            line = line.replace('[', '\\[')
            line = line.replace(']', '\\]')
            line = line.replace('~', '\\~')
            line = line.replace('…', '...')
            line = line.replace('-----', ' ')
            line = line.replace('----', ' ')
            line = line.replace('---', ' ')
            if not hidden_words.search(line):
                chapter.append(line + '\n\n')
        chapters.insert(0, chapter)

        # getting url for next chapter
        if "mtnovel" in url:
            url = 'https://mtnovel.com' + soup.find('div', class_='btn-group').find('a', href=True)['href']
        elif "allnovelfull" in url:
            url = 'https://allnovelfull.com' + soup.find('div', class_='btn-group').find('a', href=True)['href']
        elif "readlightnovel" in url:
            try:
                url = soup.find('a', href=True, class_='prev prev-link')['href']
            except Exception as e:
                pass
        elif "noveltop1" in url:
            url = soup.find('a', href=True, class_='btn btn-success')['href']
        elif "lightnovelpub" in url:
            url = "https://www.lightnovelpub.com" + \
                  soup.find('div', class_='chapternav skiptranslate').find('a', href=True)['href']
        elif "novel84" in url:
            url = soup.find('a', href=True, class_='btn btn-success')['href']
        elif "wuxiaz" in url:
            url = "https://www.wuxiaz.com" + soup.find('div', class_='action-select').find('a', href=True)['href']
        loading = ''
        percent = int(((i + 1) / current_number) * 100)
        filled = int(percent / 10)
        empty = 10 - int(percent / 10)
        for j in range(filled):
            loading += '\u25a0'
        for j in range(empty):
            loading += '\u25a1'
        print(f'{novel_name}: {i + 1}/{current_number} [{loading}] {percent}%', end='\r', flush=True)

    if novels[novel_name]['chapter'] + 1 == latest_number:
        name = novel_name.replace(' ', '_') + '_' + str(latest_number)
    else:
        name = novel_name.replace(' ', '_') + '_' + str(novels[novel_name]['chapter'] + 1) + '-' + str(latest_number)
    chapters.insert(0, '% ' + name + '\n\n')
    with open('novels/' + name + '.txt', 'w', encoding='utf-8') as f:
        for chapter in chapters:
            for line in chapter:
                f.write(line)

    os.system(f'pandoc novels/{name}.txt -o novels/{name}.epub --quiet')
    # using pandoc to convert txt into epub, there is a lib in python for that but it was not working
    upload = drive.CreateFile({"mimeType": "application/epub+zip",
                               "parents": [
                                   {"kind": "drive#fileLink", "id": 'XXX', }],
                               "title": "{}.epub".format(name)})
    # uploads the epub file into private google drive
    upload.SetContentFile("novels/{}.epub".format(name))
    upload.Upload()

    novels[novel_name]['chapter'] = latest_number

    with open('list.json', 'w', encoding='utf-8') as f:
        json.dump(novels, f)

    print(f'UPLOAD {name} DONE              ')

input()
