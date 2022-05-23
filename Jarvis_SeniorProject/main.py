import speech_recognition as sr
import pyttsx3
import pywhatkit
import subprocess
import wikipedia
# import sports
from tkinter import *
import tkinter.scrolledtext as st
import requests
from bs4 import BeautifulSoup
from opencage.geocoder import OpenCageGeocode
import imdb
from rotten_tomatoes_scraper.rt_scraper import MovieScraper
from googlesearch import search
from PIL import Image, ImageTk
from PyDictionary import PyDictionary

import datetime
import os
import time
import threading
from playsound import playsound

import smtplib
import config

# voice and voice recognizer

voiceRep = pyttsx3.init()
voiceRate = 145
voiceRep.setProperty('rate', voiceRate)

# GUI variables----------------------------------------------------------------


root = Tk()
root.title("Virtual Assistant")


# frame = LabelFrame(root, text="", padx=200, pady=100)
# frame = Frame(root)

# gui


def user_gui():
    global text_box
    canvas = Canvas(root, width=600, height=300)
    canvas.grid(columnspan=3, rowspan =4)

    logo = Image.open('logoblack.png')
    logo = logo.resize((150,150), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column = 1, row = 0)
    instructions = Label(root, text="Welcome to Jarvis, Virtual Assistant. Please press the button below to give commands.")
    instructions.grid(columnspan=3, column = 0, row=1)
    # frame.grid()
    talkPhoto = Image.open('microphone.png')
    talkPhoto = talkPhoto.resize((70, 70), Image.ANTIALIAS)
    talkPhoto = ImageTk.PhotoImage(talkPhoto)
    # button = Button(canvas, image=talkPhoto, padx=15, pady=15, command=talk)
    button = Button(root, image=talkPhoto, command=talk)
    button.grid(column=1, row=2)
    # root.resizable(False , False)
    #canvas = Canvas(root, width=600, height=75)
    #canvas.grid(columnspan=6)
    #texter = Label(root, text="Jarvis")
    #texter.grid(column=0, row=3)

    canvas = Canvas(root, width=600, height=250)

    canvas.grid(columnspan=3)
    texter = Label(root, text='JARVIS                                                                    USER', anchor=CENTER)
    texter.grid(columnspan =3, column = 0, row =3)
    text_box = st.ScrolledText(root, height=10, width=50, padx=15, pady=15)

    text_box.grid(column=1, row=4)
    # gui.text_box.insert(INSERT, 'tester\n')
    # gui.text_box.insert(INSERT, 'tester\n')
    # gui.text_box.insert(INSERT, 'tester\n','alignment')
    # gui.text_box.tag_configure('alignment',justify='right')
    # gui.text_box.insert(INSERT, 'tester')

    text_box.configure(state = 'disable')

    #root.update()
    root.mainloop()


# GUI handling ------------------------------------------------------------------

# printInGUI
def printTextJarvis(line):
    text_box.configure(state='normal')
    print(line)
    line = line + '\n'
    text_box.insert(INSERT , line)
    text_box.configure(state='disable')
    root.update()

def printTextUser(line):
    text_box.configure(state='normal')
    print(line)
    line = line + '\n'
    text_box.insert(INSERT, line, 'right_align')
    text_box.tag_configure('right_align', justify='right')
    text_box.configure(state='disable')
    root.update()


def talk():
    command_check()


# Jarvis funtions:
# greet
def greet():
    voiceRep.say('Hello, it is me, Jarvis')
    printTextJarvis('Hello, it is me, Jarvis')
    voiceRep.say('How can I help you?')
    printTextJarvis('How can I help you?')
    voiceRep.runAndWait()


#greet()

# JarvisTalk
def jarvis_say(line):
    voiceRep.say(line)
    voiceRep.runAndWait()
    return line


def jarvis_listen():
    try:
        with sr.Microphone() as source:
            jarvis_say('Jarvis is listening')
            # print('Jarvis is listening........')
            printTextJarvis('Jarvis is listening........')
            listener = sr.Recognizer()
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if command == 'stop':
                return None
            # command = command.title()
            return command
    except:
        jarvis_say('I did not hear you, please say that again')
        return jarvis_listen()


# getUserCommand
def get_user_command():
    try:
        with sr.Microphone() as source:

            jarvis_say('Jarvis is listening')
            # print('Jarvis is listening........')
            printTextJarvis('Jarvis is listening........')
            listener = sr.Recognizer()
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'jarvis' in command:
                voiceRep.say('Your command has been recorded, please give me a moment to process')
                voiceRep.runAndWait()
                # printText('Jarvis: Your command has been recorded')
                # print(command)
                printTextUser(command)
                return command
    except:
        pass
    # return 'Jarvis could not hear you'


# Jarvis funtions


def play_song(user_command):
    if 'play' in user_command:
        song_name = user_command.replace('play ', '')
        jarvis_say('playing' + song_name)
        pywhatkit.playonyt(song_name)
        # print('playing')
        printTextJarvis('playing' + song_name)

#play_song('play lady gaga')
def open_application(user_command):
    if 'open' in user_command:
        application_name = user_command.replace('open ', '')
       # print(config.application)
       # print(application_name)
        jarvis_say('opening ' + application_name)
        printTextJarvis('opening ' + application_name)
       # print(config.application.get(application_name))
        subprocess.call(config.application.get(application_name))
        #application.update({'google chrome': r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"})
        #application.update({'microsoft edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'})
        #application.update({"photoshop" : r"D:\NguyenLeMinh\Adobe Photoshop 2020\Photoshop.exe"})

#open_application('open google chrome')

def close_application(user_command):
    if 'close' in user_command:
        #print(user_command)
        application_name = user_command.replace('close ', '')
        #print(application_name)
        jarvis_say('closing ' + application_name)
        printTextJarvis('closing ' + application_name)

        #print(config.application.get(application_name).rpartition( "\\" )[2])
        #print(config.application.get(application_name))
        subprocess.call(["taskkill", "/F", "/IM", config.application.get(application_name).rpartition( "\\" )[2]])

#user_gui()
#close_application('close google chrome')

def google_search(user_command):
    if 'search' in user_command:
        searching = user_command.replace('search ', '')
        jarvis_say('searching' + searching)
        pywhatkit.search(searching)
        # print('searching')
        printTextJarvis('Jarvis: searching' + searching)


def weather_check(user_command):
    if ('weather today in' in user_command) or ('weather today at' in user_command):
        if ' in ' in user_command:
            index = user_command.find(' in ') + 4
            var = 'in '
        else:
            index = user_command.find(' at ') + 4
            var = 'at '
        user_command = user_command[index:]
        # city = user_command.replace('how is the weather today in','')
        city = user_command
        print(city)
        print(get_location(city))
        latitude, longitude = get_location(city)
        weather = get_weather(latitude, longitude)
        a = 'It is '
        if weather == 'Mist':
            weather = 'foggy'
        elif weather == 'Rain':
            weather = 'rainy'
        elif weather == 'Clear':
            weather = 'very clear'
            a = 'The sky is '
        elif weather == 'Clouds':
            weather = 'cloudy'
        jarvis_say(a + weather + ' today ' + var + city)
        printTextJarvis(a + weather + ' today ' + var + city)

    if ('weather today' in user_command) and (' in ' not in user_command) and (' at ' not in user_command):
        city, country, latitude, longitude = get_location_current_place()
        weather = get_weather(latitude, longitude)
        a = 'It is '
        if weather == 'Mist':
            weather = 'foggy'
        elif weather == 'Rain':
            weather = 'rainy'
        elif weather == 'Clear':
            weather = 'very clear'
            a = 'The sky is '
        elif weather == 'Clouds':
            weather = 'cloudy'
        jarvis_say(a + weather + ' today in ' + city + ' ' + country)
        printTextJarvis(a + weather + ' today in ' + city + ' ' + country)


def movie_info(user_command):
    if 'rating' in user_command:
        index = user_command.find(' of ') + 4
        user_command = user_command[index:]
        movie_title = check_movie_exist(user_command)
        imdb = imdb_score(movie_title)
        tomatoes = movie_score(movie_title)
        jarvis_say('According to the IMDB, the critics rate the movie ' + movie_title + ' ' + str(
            imdb) + ' over 10. The audience give the movie ' + str(tomatoes) + ' over 100 ')
        printTextJarvis('According to the IMDB, the critics rate the movie ' + movie_title + ' ' + str(
            imdb) + ' over 10. The audience give the movie ' + str(tomatoes) + ' over 100 ')
        if imdb >= 8:
            jarvis_say('It is a very good movie')
            printTextJarvis('It is a very good movie')
        elif (imdb < 8) and (imdb > 6):
            jarvis_say('The movie is not so bad')
            printTextJarvis('The movie is not so bad')
        else:
            jarvis_say('This is a bad movie. Do not waste your time for this')
            printTextJarvis('This is a bad movie. Do not waste your time for this')


def check_wikipedia(user_command):
    if 'look up wikipedia for' in user_command:

        objectSearch = user_command.replace('look up wikipedia for', '')
        # print(objectSearch)
        jarvis_say('looking up wikipedia for' + objectSearch)
        try:
            info = wikipedia.summary(objectSearch, 3)
        except:
            info = 'No information found on Wikipedia for' + objectSearch
        printTextJarvis(info)
        jarvis_say(info)


def get_word_definition(user_command):
    if 'define' in user_command:
        word = user_command.replace('define ', '')
        print(word)
        # print(len(word) == 0)
        if not word:
            printTextJarvis('I did not hear any word from you')
            jarvis_say('I did not hear any word from you')
        else:
            definition = word_meaning(word)
            if definition == None:
                printTextJarvis('I can only define nouns, verbs, and adjectives')
                jarvis_say('I can only define nouns, verbs, and adjectives')
            else:
                # print(definition)
                types = list(definition.keys())
                # print(types[0])
                if len(definition) == 1:
                    number_of_meaning = len(definition.get(types[0]))
                    if number_of_meaning == 1:
                        printTextJarvis('This word has one meaning: ' + definition.get(types[0])[0])
                        jarvis_say('This word has one meaning: ')
                        jarvis_say(definition.get(types[0])[0])
                    else:
                        printTextJarvis('This word has ' + str(number_of_meaning) + ' meanings:')
                        jarvis_say('This word has ' + str(number_of_meaning) + ' meanings:')
                        counter = 1
                        print(definition.get(types[0]))
                        for i in definition.get(types[0]):
                            printTextJarvis('Definition number ' + str(counter) + ': ' + i)
                            jarvis_say('Definition number ' + str(counter) + ':')
                            jarvis_say(i)

                            counter += 1
                            if counter > 4:
                                printTextJarvis('Do you want to hear the rest?')
                                jarvis_say('Do you want to hear the rest?')
                                user_answer = jarvis_listen()
                                if 'no' in user_answer:
                                    printTextJarvis('Ok then')
                                    jarvis_say('Ok then')
                                    break

                else:
                    # print(definition)

                    jarvis_say('This word has a few types defining its meanings, including')
                    printTextJarvis('This word has a few types defining its meanings, including')
                    for i in types:
                        printTextJarvis(i)
                        jarvis_say(i)
                    meanings = word_type(definition)
                    counter = 1
                    if len(meanings) == 1:
                        printTextJarvis('Definition: ' + str(meanings[0]))
                        jarvis_say('This word means ')
                        jarvis_say(str(meanings[0]))
                    else:
                        for i in meanings:
                            printTextJarvis('Definition number ' + str(counter) + ' is ' + i)
                            jarvis_say('Definition number ' + str(counter) + ' is ')
                            jarvis_say(i)

                            counter += 1
                            if counter > 4:
                                printTextJarvis('Do you want to hear the rest? There are: ' + str(len(meanings) - counter) + ' meanings left.')
                                jarvis_say('Do you want to hear the rest?  There are: ' + str(len(meanings) - counter) + ' meanings left.')
                                user_answer = jarvis_listen()
                                if 'no' in user_answer:
                                    printTextJarvis('Ok then')
                                    jarvis_say('Ok then')
                                    break


def get_alarm_time(user_command):
    if 'set alarm' in user_command:
        user_command = user_command.replace('set alarm', '')
        user_command = user_command.replace('at', '')
        alarm(user_command)


# checkCommand
def command_check():
    try:
        user_command = get_user_command()
        if 'hello jarvis' in user_command:
            greet()
        if 'jarvis' in user_command:
            user_command = user_command.replace('jarvis ', '')
        play_song(user_command)
        open_application(user_command)
        close_application(user_command)
        google_search(user_command)
        weather_check(user_command)
        movie_info(user_command)
        check_wikipedia(user_command)
        get_word_definition(user_command)
        get_alarm_time(user_command)
        sending_email(user_command)
    except Exception as e:
        print(e)
        jarvis_say('I could not hear you, please try again.')
        printTextJarvis('I could not hear you, please try again.')


# send emails functions


def sending_email(user_command):
    if 'send email' in user_command:
        user_command = user_command.replace('send email ', '')
        user_command = user_command.replace('to ', '')
        #user_command = user_command.replace(' ', '')
        receiver = get_receiver(user_command)
        subject = get_subject()
        body = get_body()
        send_mail(subject, body, receiver)
        jarvis_say("Email has been sent")
        printTextJarvis("Email has been sent")


def send_mail(subject, body, receiver):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.email, config.password)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(config.email, receiver, message)
    server.quit()


# send_mail('TEST', 'TESTINGBODY', 'minhnguyen_2021@depauw.edu')

def get_receiver(user_command):
    # receiver = jarvis_listen()
    # print(receiver)
    #name = email_collector(user_command)
    print(user_command)
    email = config.email_addresses.get(user_command)
    return email


def email_collector(user_command):
    if ' ' in user_command:
        user_command = user_command.replace(' ', '')
    # if 'at' in user_command:
    #    user_command = user_command.replace('at', '@')
    return user_command


# get_receiver()

def get_subject():
    jarvis_say('What is the subject')
    printTextJarvis('What is the subject?')
    subject = jarvis_listen()
    return subject


def get_body():
    try:
        with sr.Microphone() as source:
            jarvis_say('What should I say in the email')
            # print('Jarvis is listening........')
            printTextJarvis('What should I say in the email?')
            listener = sr.Recognizer()
            voice = listener.record(source, duration=10)
            command = listener.recognize_google(voice)
            command = command.lower()
            if command == 'stop':
                return None
            # command = command.title()
            #printTextUser(command)
            return command
    except:
        jarvis_say('Come again please')
        return jarvis_listen()


import re


# get_email()
def check_valid(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


# alarm functions
def alarm(alarm_time):
    # print(alarm_time[:2])
    now = datetime.datetime.now()
    print(now)
    hour, minute = time_extractor(alarm_time)
    # if len(alarm_time) == 5:

    wakeup_time = datetime.datetime.combine(now.date(), datetime.time(hour, minute, 0))
    # print(wakeup_time)
    # time.sleep((wakeup_time - now).total_seconds())
    second = (wakeup_time - now).total_seconds()
    # print('run it now')
    jarvis_say("Alarm has been set")
    printTextJarvis("Alarm has been set")
    if __name__ == '__main__':
        threading.Thread(target=wake_me_up, args=(second,)).start()
        # threading.Thread(target=run).start()
    # print("DONE BEFORE 10 Second")


def wake_me_up(second_to_wake_up):
    time.sleep(second_to_wake_up)
    playsound('morning_alarm.mp3')


def time_extractor(alarm_time):
    daytime = True
    daytimeset = False
    minute = 0
    if ':' in alarm_time:
        alarm_time = alarm_time.replace(':', '')
    if '.' in alarm_time:
        alarm_time = alarm_time.replace('.', '')
    if ' ' in alarm_time:
        alarm_time = alarm_time.replace(' ', '')
    print(alarm_time)
    if 'am' in alarm_time:
        daytimeset = True
        alarm_time = alarm_time.replace('am', '')
        daytime = True
    elif 'pm' in alarm_time:
        daytimeset = True
        alarm_time = alarm_time.replace('pm', '')
        daytime = False
    # wake me up at:
    # 6
    if len(alarm_time) == 1:
        hour = int(alarm_time)
        if not daytime:
            hour = hour + 12
    # 11
    if len(alarm_time) == 2:
        hour = int(alarm_time)
        if not daytime:
            hour = hour + 12
            if hour == 24:
                hour = 0
    # 605
    elif len(alarm_time) == 3:
        hour = int(alarm_time[0])
        minute = int(alarm_time[1:])
        if not daytime:
            hour = hour + 12
    # 1800
    elif len(alarm_time) == 4:
        hour = int(alarm_time[:2])
        minute = int(alarm_time[2:])
        if daytimeset:
            if not daytime:
                hour = hour + 12
    # elif len(alarm_time) ==
    print(hour, minute)
    return hour, minute


# time_extractor("  20   ")
# alarm("605 pm")
# print('am I late')
# weather helper functions
def get_location_current_place():
    try:
        webpage = 'https://iplocation.com/'
        page = requests.get(webpage)
        data = BeautifulSoup(page.content, 'html.parser')
        city = data.find(class_='city').get_text()
        country = data.find(class_='country_name').get_text()
        latitude = data.find(class_='lat').get_text()
        longitude = data.find(class_='lng').get_text()
        return city, country, latitude, longitude
        # return latitude, longitude
    except Exception as e:
        printTextJarvis('Error, location could not be retrieved')
        jarvis_say('Error, location could not be retrieved')


def get_location(city):
    try:
        key = '8348941949744f989032e0a3dc4d97a5'
        geocoder = OpenCageGeocode(key)

        # query = city+','+country
        query = city
        results = geocoder.geocode(query)
        lat = results[0]['geometry']['lat']

        lng = results[0]['geometry']['lng']

        return lat, lng
    except Exception as e:
        return None


def get_weather(latitude, longitude):
    try:
        api_key = "7577b77a75f7d55304f2adde85b33230"
        base_url = 'http://api.openweathermap.org/data/2.5/weather?'
        complete_url = base_url + "lat=" + \
                       str(latitude) + "&lon=" + str(longitude) + "&appid=" + api_key
        response = requests.get(complete_url)
        x = response.json()
    except Exception as e:
        printTextJarvis("An error occurred while retrieving weather information")
        jarvis_say("An error occurred while retrieving weather information")
    if x["cod"] != "404":
        return x.get('weather')[0].get('main')
    else:
        return False


# search query that returns search link
def google_query(query):
    link = []
    for j in search(query, tld="ca", lang="en", num=10, stop=10, pause=2):
        link.append(j)
    return link


# movie ratings helper functions
# check movie existence in IMDB the database
def check_movie_exist(movie_name):
    try:
        movie_name += ' IMDB'
        webpage = google_query(movie_name)[0]  # return first link search result
        page = requests.get(webpage)
        content = page.text
        data = BeautifulSoup(content, 'lxml')
        # print(data)
        title = str(data.findAll(attrs={"property": "og:title"}))
        # title = data.title.string
        title = title[16:-31]
        # print(title)
        # translator = Translator()
        # title = translator.translate(title)
        # print(title)
        return title
    except Exception as e:
        printTextJarvis('Movie not found')


def imdb_score(movie_name):
    movie = imdb.IMDb().search_movie(movie_name)
    movieID = movie[0].getID()
    rating = imdb.IMDb().get_movie(movieID)['rating']
    # print(rating)
    return rating


# get the movie score from rottentomatoes
def movie_score(movie_name):
    name = movie_name[0:-6]
    # print(name)
    movie_scraper = MovieScraper(movie_title=name)
    movie_scraper.extract_metadata()

    # print(movie_scraper.metadata.get('Score_Audience'))
    return movie_scraper.metadata.get('Score_Audience')


# get sport match info
'''
def scores(sport_name, team_1, team_2):
    valid_sport = ['baseball', 'basketball', 'football','soccer', 'tennis']
    if sport_name not in valid_sport:
        print('I do not care about this sport, sorry')
    else:
        matches = check_sport_name(sport_name)
        try:
            result = []
            all_matches = sports.all_matches()
            print(all_matches)
            keys = list(all_matches.keys())
            for j in range(len(keys)):
                temp = all_matches[keys[j]]
                matches = []
                for i in range(len(temp)):
                    matches.append((str(temp[i])).lower())
                for text in matches:
                    if query in text:
                        result.append(True)
                        print(f'{keys[j]} : The last updated score was {text}')
                        #speak('The last updated score was {text} : {keys[j]}')
                    else:
                        result.append(False)
            if True not in result:
                print('Could not retrieve game scores')
                #speak('Could not retrieve game scores')
        except Exception as e:
            print(e)
            print('An error occurred, please try again')
            #speak('An error occurred, please try again')

#'baseball', 'basketball', 'cricket', 'football', 'handball', 'hockey', 'soccer', 'tennis', 'volleyball'
def check_sport_name(sport_name):
    if sport_name == 'baseball':
        return sports.get_sport(sports.BASEBALL)
    elif sport_name == 'basketball':
        return sports.get_sport(sports.BASKETBALL)
    elif sport_name == 'football':
        return sports.get_sport(sports.FOOTBALL)
    elif sport_name == 'soccer':
        return sports.get_sport(sports.SOCCER)
    elif sport_name == 'tennis':
        return sports.get_sport(sports.TENNIS)
    return None
'''


# words definitions helper
def word_meaning(word):
    try:
        meaning = PyDictionary().meaning(word)
        print(meaning)
    except:
        meaning = None
    return meaning


def word_type(definition):
    jarvis_say('Which type of this word are you refering to?')
    # print('Jarvis is listening........')
    printTextJarvis('Which type of this word are you refering to?')
    command = jarvis_listen()
    # print(command)
    command = type_checker(definition, command)
    # command = command.title()
    meaning = definition.get(command)
    # meaning = definition.get('Noun')
    # jarvis_say(meaning)
    # printText(command)
    return meaning


def type_checker(definition, command):
    if 'pronoun' in command:
        command = command.replace(command, 'pronoun')
    elif 'adjective' in command:
        command = command.replace(command, 'adjective')
    elif 'adverb' in command:
        command = command.replace(command, 'adverb')
    elif 'preposition' in command:
        command = command.replace(command, 'preposition')
    elif 'noun' in command:
        command = command.replace(command, 'noun')
    elif 'verb' in command:
        command = command.replace(command, 'verb')
    elif 'interjection' in command:
        command = command.replace(command, 'interjection')
    elif 'conjunction' in command:
        command = command.replace(command, 'conjunction')
    elif 'determiner' in command:
        command = command.replace(command, 'determiner')
    command = command.title()
    if command not in definition.keys():
        printTextJarvis('There is no type called ' + command + '. Please try again!')
        jarvis_say('There is no type called ' + command + '. Please try again!')
        command = jarvis_listen()

        # command.title()
        return type_checker(definition, command)
    else:
        return command


# print(word_meaning('unless'))
user_gui()
# print(wikipedia.summary('tony stark'),3)
