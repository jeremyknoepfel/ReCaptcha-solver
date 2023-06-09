# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:03:52 2020

Löst Googles Recaptcha.

@author: Jeremy
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pydub
import urllib
import speech_recognition

data_path = "D:\Python-Scripts"
driver_path = 'C:\Program Files (x86)\chromedriver.exe'
browser = webdriver.Chrome(driver_path)

browser.get("https://www.google.com/recaptcha/api2/demo")
frames = browser.find_elements_by_tag_name("iframe")
browser.switch_to.frame(frames[0])
time.sleep(random.randint(2,4))
browser.find_element_by_class_name("recaptcha-checkbox-border").click()
browser.switch_to.default_content()

frames = browser.find_element_by_xpath(
    "/html/body/div[2]/div[4]"
    ).find_elements_by_tag_name("iframe")
browser.switch_to.frame(frames[0])
time.sleep(random.randint(2,4))
browser.find_element_by_id("recaptcha-audio-button").click()
browser.switch_to.default_content()
frames = browser.find_elements_by_tag_name("iframe")
browser.switch_to.frame(frames[-1])
time.sleep(random.randint(2,4))
browser.find_element_by_xpath(
    "/html/body/div/div/div[3]/div/button"
    ).click()

src = browser.find_element_by_id("audio-source").get_attribute("src")
urllib.request.urlretrieve(src, data_path + "\\audio.mp3")
sound = pydub.AudioSegment.from_mp3(
    data_path + "\\audio.mp3"
    ).export(data_path + "\\audio.wav", format="wav")
recognizer = speech_recognition.Recognizer()
google_audio = speech_recognition.AudioFile(data_path + "\\audio.wav")

with google_audio as source:
    audio= recognizer.record(source)
text = recognizer.recognize_google(audio, language='de-DE')
inputfield = browser.find_element_by_id("audio-response")
inputfield.send_keys(text.lower())
inputfield.send_keys(Keys.ENTER)