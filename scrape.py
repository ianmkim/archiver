import pyautogui
import pyperclip
import time
import json

import pickle
import csv

from bs4 import BeautifulSoup

from pynput.keyboard import Controller

def write(text):
	pyperclip.copy(text)
	pyautogui.hotkey('ctrl', 'v')
	pyperclip.copy('')

def read():
	pyautogui.hotkey('ctrl', 'c')
	return pyperclip.paste()

def fill_url(last_name):
	url = "https://home.dartmouth.edu/directory/ajax/search?type=student&last-name=" + last_name + "&_wrapper_format=drupal_ajax"
	return url

def process_entry(entry):
	name = entry.find_all("div", {"class": "directory-item__person-name"})[0].text
	email = entry.find_all("div", {"class": "directory-item__person-email"})[0].text
	try:
		number = entry.find_all("div", {"class": "directory-item__person-phone"})[0].text
	except:
		number = ""
	try:
		mailbox = entry.find_all("div", {"class": "directory-item__person-mailbox"})[0].text
	except:
		mailbox = ""
	return {
		"name": name,
		"mail": mailbox,
		"email": email,
		"number": number,
	}

def construct_bruteforce_prompt():
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	out = []
	for char in alphabet:
		for char2 in alphabet:
			out.append(char + char2)
	return out

# name_list = construct_bruteforce_prompt()

with open("detailed_list.pickle", 'rb') as handle:
    name_list = pickle.load(handle)
keyboard = Controller()
email_dict = {}

for i, name in enumerate(name_list):
	print("=======", (i/len(name_list)) * 100, "% =======")
	pyautogui.click(180, 63)
	time.sleep(0.5)
	pyautogui.hotkey('ctrl', 'a')
	print(fill_url(name))
	write(fill_url(name))
	pyautogui.write("\n")
	time.sleep(1)

	pyautogui.click(19,98)
	pyautogui.hotkey('ctrl', 'a')
	out = read()
	try:
		parsed = json.loads(out)[0]["content"]

		soup = BeautifulSoup(parsed, 'html.parser')
		items = soup.find_all("div", {"class": "directory-item"})

		with open("scraped.csv", "a") as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for entry in items:
				out_dict = process_entry(entry)
				if out_dict['name'] not in email_dict:
					print(out_dict['name'], out_dict['email'])
					email_dict[out_dict['name']] = {
						'mail': out_dict['mail'],
						'number': out_dict['number'],
						'email': out_dict['email'],
					}
					writer.writerow([
						out_dict['name'],
						out_dict['email'],
						out_dict['mail'].replace("\\n", "").strip(),
						out_dict['email'],
					])
				else:
					print("skipped")
	except Exception as ex:
		print(ex)

	time.sleep(2)

print("writing to pickle file")
with open("scraped.pickle", 'wb') as handle:
	pickle.dump(email_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
