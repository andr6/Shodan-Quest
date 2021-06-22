# -*- coding: utf-8 -*-

# Author:   Samy Younsi (RuptureFarm 1029) <samyyounsi@hotmail.fr>
# License:  MIT License (http://www.opensource.org/licenses/mit-license.php)
# Docs:     https://github.com/ShinoNuma/Shodan-Quest
# Website:  http://samy.ga
# Linkedin: https://www.linkedin.com/in/samy-younsi/
# Note:     FOR EDUCATIONAL PURPOSE ONLY.

from __future__ import print_function, unicode_literals
from PyInquirer import Separator, Token, prompt, style_from_dict
from termcolor import cprint
import shodan
import random
import time
import csv
import os

def banner():
  shodanQuest = """
    ____  _               _                ___                  _   
   / ___|| |__   ___   __| | __ _ _ __    / _ \ _   _  ___  ___| |_ 
   \___ \| '_ \ / _ \ / _` |/ _` | '_ \  | | | | | | |/ _ \/ __| __|
    ___) | | | | (_) | (_| | (_| | | | | | |_| | |_| |  __/\__ \ |_ 
   |____/|_| |_|\___/ \__,_|\__,_|_| |_|  \__\_\\__,_|\___||___/\__|
   Author: Naqwada, RuptureFarms 1029                        v1.0.2

                      FOR EDUCATIONAL PURPOSE ONLY.   
  """
  txtColors = ['red', 'yellow', 'green', 'blue', 'cyan']
  return cprint(shodanQuest, random.choice(txtColors), attrs=['bold'])

def getSavedAPIKey():
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    return open(filename, 'r').read()
  else:
    return open(filename, 'w+').read()

def checkShodanAPIKey(apiKey):
  try:
    print('[⏳] Checking if the Shodan API key is valid...')
    api = shodan.Shodan(apiKey)
    api.search('0_0')
    cprint('[✔️] API Key Authentication: SUCCESS..!', 'green', attrs=['bold'])
    saveAPIKey(apiKey)
    cprint('[📑] The API Key has been saved.', 'blue', attrs=['bold'])
    return apiKey
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])
    exit()

def findShoddanAPIKeyOnGit(boolean):
  if boolean == True:
    cprint('[👻] Here is a list of GitHub dorks to help you find a Shodan API Key', 'green', attrs=['bold'])
    print('[+] \033[1;32m Dork 1:\033[1;m shodan_api_key language:python')
    print('[+] \033[1;32m Dork 2:\033[1;m shodan_api_key language:php')
    print('[+] \033[1;32m Dork 3:\033[1;m shodan_api_key language:javascript')
    print('[+] \033[1;32m Dork 4:\033[1;m shodan_key language:python')
    print('[+] \033[1;32m Dork 5:\033[1;m shodan_key language:php')
    print('[+] \033[1;32m Dork 6:\033[1;m shodan_key language:javascript')
    cprint('[👀] Insert the following dorks in the GitHub search bar, select the "Code" tab, and look carefully for Shodan API keys in the code.', 'green', attrs=['bold'])
    cprint('[✏️] You can also modify the dorks by changing the language for example to get more results.', 'green', attrs=['bold'])
  print('\n[👹] See you soon for a new adventure!\n')  
  exit()

def shodanSearch(apiKey, params):
  try:
    api = shodan.Shodan(apiKey)

    if params['needDorks'] == True:
      for dork in params['dorks']:
        params['keywords'] += ' {} '.format(dork)
    print(params['keywords'])
    results = []
    counter = 1
    for response in api.search_cursor(params['keywords']):
      print('[+] \033[1;32m IP:\033[1;m {}'.format((response['ip_str'])))
      print('[+] \033[1;32m Port:\033[1;m {}'.format(str(response['port'])))
      print('[+] \033[1;32m Organization:\033[1;m {}'.format(str(response['org'])))
      print('[+] \033[1;32m Location:\033[1;m {}'.format(str(response['location'])))
      print('[+] \033[1;32m Layer:\033[1;m {}'.format((response['transport'])))
      print('[+] \033[1;32m Domains:\033[1;m {}'.format(str(response['domains'])))
      print('[+] \033[1;32m Hostnames:\033[1;m {}'.format(str(response['hostnames'])))

      print('\n[👾] \033[1;32m Result:\033[1;m {}. \033[1;32m Search query:\033[1;m {}'.format(str(counter), str(params['keywords'])))
      results.append(response) 
      time.sleep(0.5)
      print('\n')


      counter += 1
      if counter >= 999:
        break
    return results
  except shodan.APIError as errorMessage:
    cprint('[🚫] Error: {}. Please, try again.'.format(errorMessage), 'red', attrs=['bold'])

def saveResultsAs(questName, fileFormat, results):
  savePath = 'quests/'
  filename = '{}-{}.{}'.format(str(questName), time.strftime('%Y-%m-%d-%H:%M'), fileFormat)
  fullPath = os.path.join(savePath, filename) 
  counter = 1
  if fileFormat == 'csv':
    csvColumns = ['#', 'IP', 'Port', 'Organization', 'Location', 'Layer', 'Domains', 'Hostnames', 'Service Information']
    try:
      with open(fullPath, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvColumns)
        writer.writeheader()
        for result in results:
          writer.writerow({'#': counter, 'IP': result['ip_str'], 'Port': result['port'], 'Organization': result['org'], 'Location': result['location'], 'Layer': result['transport'], 'Domains': result['domains'], 'Hostnames': str(result['hostnames'])})
          counter += 1
    except IOError:
      print(IOError)
  else:
    try:
      file = open(fullPath, 'w+')
      counter = counter + 1
      for result in results:
        file.write('[+] IP: {}\n'.format(result['ip_str'])) 
        file.write('[+] Port: {}\n'.format(result['port']))
        file.write('[+] Organization: {}\n'.format(result['org']))
        file.write('[+] Location: {}\n'.format(result['location']))
        file.write('[+] Layer: {}\n'.format(result['transport']))
        file.write('[+] Domains {}\n'.format(result['domains']))
        file.write('[+] Hostnames: {}\n'.format(result['hostnames']))
        file.write('[+] Service information: {}\n'.format(str(result['data'])))
        file.write('\n[✓] Result: {}. Search query: {}\n'.format(str(counter), str(questName)))
        counter += 1
    except IOError:
      print("I/O error")
  return filename

def saveAPIKey(apiKey):
  filename = 'shodan_key.txt'
  file_exists = os.path.isfile(filename) 
  if file_exists:
    file = open(filename, 'w')
    file.write(apiKey) 
    file.close()
  else:
    file = open(filename, 'w+')
    file.write(apiKey) 
    file.close()
  return True

def main():
  banner()

  shodanAPIKey = getSavedAPIKey()
  results = ''
  
  if len(shodanAPIKey) == 0: 
    print('[🙂] Hi, welcome to Shodan Quest!\n')
  else:
    print('[🤠] Welcome back, ready for a new quest?!\n')

  answers = prompt(initQuestions, style=promptStyle)

  if answers.get('findNewKey') == False or answers.get('findNewKey') == True:
    findShoddanAPIKeyOnGit(answers.get('findNewKey'))

  if len(answers) and answers.get('usePreviousKey') == True: 
    shodanAPIKey = checkShodanAPIKey(shodanAPIKey)
  
  if len(answers) and answers.get('haveOwnKey') == True:
    shodanAPIKey = checkShodanAPIKey(answers.get('useNewKey'))

  if len(answers) > 0:   
    answers = prompt(searchQuestions, style=promptStyle)

  if len(answers) and len(answers['keywords']) > 0 or len(answers['dorks']) > 0:
    questName = answers['keywords']
    results = shodanSearch(shodanAPIKey, answers)

  if len(results) > 0:
    answers = prompt(saveResultsQuestion, style=promptStyle) 
    if answers.get('fileFormat'):
      file = saveResultsAs(questName, answers.get('fileFormat'), results)
      if len(file) > 0:
        print('[📝] Your file {} has been successfully saved!\n'.format(file))
  else:
    cprint('[😓] No result found. Please try again using another keywords or dorks combo.', 'yellow', attrs=['bold'])   
  
  print('\n[👹] See you soon for a new adventure!\n')


initQuestions = [
    {
        'type': 'confirm',
        'name': 'usePreviousKey',
        'qmark': '[❓]',
        'message': 'Saved Shodan API key detected, do you want to use the following key: {} for your current quest?'.format(getSavedAPIKey()),
        'default': True,
        'when': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(getSavedAPIKey()) > 30 else False
    },
   {
        'type': 'confirm',
        'name': 'haveOwnKey',
        'qmark': '[❓]',
        'message': 'Do you have a Shodan API key?',
        'default': True,
        'when': lambda answers: answers.get('usePreviousKey') == False or len(getSavedAPIKey()) < 30,
    },
    {
        'type': 'input',
        'name': 'useNewKey',
        'message': 'Enter your Shodan API key:',
        'qmark': '[🔑]',
        'when': lambda answers: answers.get('haveOwnKey') == True,
        'validate': lambda answer: 'The length of the API key should be at least 30 characters.' \
            if len(answer) < 30 else True
    },
    {
        'type': 'confirm',
        'name': 'findNewKey',
        'qmark': '[❓]',
        'message': 'You can try to find a valid API key for free using GitHub dork. Are you interested?',
        'default': False,
        'when': lambda answers: answers.get('haveOwnKey') == False,
    }
]

searchQuestions = [
    {
        'type': 'input',
        'name': 'keywords',
        'qmark': '[💬]',
        'message': 'Enter what you are looking for:',
        # 'validate': lambda answer: 'Are you really looking for something?' \
        #     if len(answer) == 0 else True
    },
    {
        'type': 'confirm',
        'name': 'needDorks',
        'qmark': '[❓]',
        'message': 'Do you need to combine your query with Shodan dorks?',
        'default': False
    },
    {
        'type': 'checkbox',
        'qmark': '[🤖]',
        'message': 'Dorks selection',
        'name': 'dorks',
        'choices': [ 
            Separator('= Databases ='),
            {
                'name': '"MongoDB Server Information" port:27017 -authentication',
            },
            {
                'name': '"Set-Cookie: mongo-express=" "200 OK"',
            },
            {
                'name': 'mysql port:"3306"'
            },
            {
                'name': 'port:"9200" all:"elastic indices"'
            },
            {
                'name': 'port:5432 PostgreSQL'
            },
            Separator('= Exposed ports ='),
            {
                'name': 'proftpd port:21',
            },
            {
                'name': '"220" "230 Login successful." port:21'
            },
            {
                'name': 'openssh port:22'
            },
            {
                'name': 'port:"23"'
            },
            {
                'name': '"Polycom Command Shell" -failed port:23'
            },
            {
                'name': 'port:"25" product:"exim"'
            },
            {
                'name': 'port:"11211" product:"Memcached"'
            },
            {
                'name': '"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"'
            },
            {
                'name': '"Docker Containers:" port:2375'
            },
            {
                'name': '"Docker-Distribution-Api-Version: registry" "200 OK" -gitlab'
            },
            {
                'name': '"dnsmasq-pi-hole" "Recursion: enabled"'
            },
            {
                'name': 'http.favicon.hash:"1485257654" "200"'
            },
            Separator('= DNS servers ='),
            {
                'name': '"port: 53" Recursion: Enabled'
            },
            Separator('= Network infrastructure ='),
            {
                'name': 'port:8291 os:"MikroTik RouterOS 6.45.9"'
            },
            Separator('= Web servers ='),
            {
                'name': 'product:"Apache httpd" port:"80"'
            },
            {
                'name': 'product:"Microsoft IIS httpd"'
            },
            {
                'name': 'product:"nginx"',
            },
            {
                'name': '"port: 8080" product:"nginx"'
            },
            Separator('= North Korea Server ='),
            {
                'name': 'net:175.45.176.0/22,210.52.109.0/24,77.94.35.0/24'
            },
            Separator('= Operating systems ='),
            {
                'name': 'os:"windows 7"'
            },
            {
                'name': 'os:"Windows 10 Home 19041"',
            },
            {
                'name': 'os:"Linux"'
            },
            Separator('= Android Root Bridge ='),
            {
                'name': '"Android Debug Bridge" "Device" port:5555'
            },
            Separator('= Webcams ='),
            {
                'name': 'Server: SQ-WEBCAM'
            },
            {
                'name': '"Server: yawcam" "Mime-Type: text/html"',
            },
            {
                'name': 'title:"xzeres wind"'
            },
            {
                'name': 'port:5006,5007 product:mitsubishi',
            },
            {
                'name': '"Server: IP Webcam Server" "200 OK"'
            },
            {
                'name': '("webcam 7" OR "webcamXP") http.component:"mootools" -401'
            },
            Separator('= Home Devices ='),
            {
                'name': '"Server: AV_Receiver" "HTTP/1.1 406"'
            },
            {
                'name': '"\x08_airplay" port:5353',
            },
            {
                'name': '"Chromecast:" port:8008',
            },
            {
                'name': '"Model: PYNG-HUB"',
            },
            Separator('= Remote Desktop ='),
            {
                'name': 'remote desktop "port:3389"'
            },
            {
                'name': '"authentication disabled" "RFB 003.008"',
            },
            Separator('= NAS accesses ='),
            {
                'name': '"Authentication: disabled" port:445'
            },
            {
                'name': '"X-Plex-Protocol" "200 OK" port:32400',
            },
            {
                'name': '"220" "230 Login successful." port:21'
            },
            {
                'name': '"Set-Cookie: iomega=" -"manage/login.html" -http.title:"Log In"'
            },
            {
                'name': 'Redirecting sencha port:9000'
            },
            {
                'name': '"Authentication: disabled" port:445'
            },
            Separator('= Printers and copiers ='),
            {
                'name': '"Serial Number:" "Built:" "Server: HP HTTP"'
            },
            {
                'name': '"SERVER: EPSON_Linux UPnP" "200 OK"',
            },
            {
                'name': '"Server: EPSON-HTTP" "200 OK"'
            },
            {
                'name': '"Serial Number:" "Built:" "Server: HP HTTP"'
            },
            {
                'name': 'ssl:"Xerox Generic Root"',
            },
            {
                'name': '"Server: KS_HTTP" "200 OK"'
            },
            {
                'name': '"Server: CANON HTTP Server"'
            },
            Separator('= Industrial Control Systems ='),
            {
                'name': '"Server: Prismview Player"'
            },
            {
                'name': '"in-tank inventory" port:10001',
            },
            {
                'name': 'P372 "ANPR enabled"'
            },
            {
                'name': 'mikrotik streetlight'
            },
            {
                'name': '"voter system serial" country:US',
            },
            {
                'name': '"Cisco IOS" "ADVIPSERVICESK9_LI-M"'
            },
            {
                'name': '"[2J[H Encartele Confidential"'
            },
            {
                'name': 'http.title:"Tesla PowerPack System" http.component:"d3" -ga3ca4f2'
            },
            {
                'name': '"Server: gSOAP/2.8" "Content-Length: 583"'
            },
            {
                'name': '"Cobham SATCOM" OR ("Sailor" "VSAT")'
            },
            {
                'name': 'title:"Slocum Fleet Mission Control"'
            },
            {
                'name': '"Server: CarelDataServer" "200 Document follows"'
            },
            {
                'name': 'http.title:"Nordex Control" "Windows 2000 5.0 x86" "Jetty/3.1 (JSP 1.1; Servlet 2.2; java 1.6.0_14)"'
            },
            {
                'name': '"[1m[35mWelcome on console"'
            },
            {
                'name': '"DICOM Server Response" port:104'
            },
            {
                'name': '"Server: EIG Embedded Web Server" "200 Document follows"'
            },
            {
                'name': '"Siemens, SIMATIC" port:161'
            },
            {
                'name': '"Server: Microsoft-WinCE" "Content-Length: 12581"'
            },
            {
                'name': '"HID VertX" port:4070'
            }
        ],
        'when': lambda answers: answers.get('needDorks') == True,
        'validate': lambda answer: 'You must choose at least one Shodan dork.' \
            if len(answer) == 0 else True
    }
]

saveResultsQuestion = [
    {
        'type': 'confirm',
        'name': 'wantSaveResults',
        'qmark': '[❓]',
        'message': 'Do you want to save the result of your quest?',
        'default': True,
    },    
    {
        'type': 'list',
        'name': 'fileFormat',
        'qmark': '[❓]',
        'message': 'What type of format do you need?',
        'choices': ['TXT', 'CSV'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers.get('wantSaveResults') == True,
    },
]

promptStyle = style_from_dict({
    Token.Separator: '#b41e44 bold',
    Token.QuestionMark: '#4b7bec',
    Token.Selected: '#2ecc71',
    Token.Pointer: '#45aaf2 bold',
    Token.Instruction: '', 
    Token.Answer: '#3498db bold',
    Token.Question: '#fff bold',
})

if __name__ == "__main__":
  main()