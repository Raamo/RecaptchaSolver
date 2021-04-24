from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
import pydub
import urllib
from speech_recognition import Recognizer, AudioFile
import os

path = os.path.abspath(os.getcwd())

driver = webdriver.Chrome("chromedriver.exe")

driver.get("https://www.google.com/recaptcha/api2/demo")

frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
sleep(randint(2, 4))

driver.find_element_by_class_name("recaptcha-checkbox-border").click()

driver.switch_to.default_content()

frames = driver.find_element_by_xpath(
    "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")

sleep(randint(2, 4))

driver.switch_to.default_content()

frames = driver.find_elements_by_tag_name("iframe")

driver.switch_to.frame(frames[-1])

driver.find_element_by_id("recaptcha-audio-button").click()

driver.switch_to.default_content()

frames = driver.find_elements_by_tag_name("iframe")

driver.switch_to.frame(frames[-1])

sleep(randint(2, 4))

driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

try:
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print(src)
    urllib.request.urlretrieve(src, path+"\\audio.mp3")

    sound = pydub.AudioSegment.from_mp3(
        path+"\\audio.mp3").export(path+"\\audio.wav", format="wav")

    recognizer = Recognizer()

    recaptcha_audio = AudioFile(path+"\\audio.wav")

    with recaptcha_audio as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio, language="de-DE")

    print(text)

    inputfield = driver.find_element_by_id("audio-response")
    inputfield.send_keys(text.lower())

    inputfield.send_keys(Keys.ENTER)

    sleep(10)
    print("Success")
    driver.quit()
except NameError:
    print("Failed")
    print(NameError)
    driver.quit()
