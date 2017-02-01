from __future__ import print_function
import sys, time
import requests, urllib
import demjson, shelve
import os.path, mechanize


		
class Archiver:
	def __init__(self):
		self._machine = "http://archive.org/wayback/available?url="
		self._arch = "https://web.archive.org/save/"
		self.archived_urls = []
		
		# load data
		if os.path.isfile("archived_urls.dat"):
			self.archived_urls = self.load_data()
		
	def available(self, url):
		print("[Checking]: %s\n" % url)
		data = demjson.decode(requests.get(self._machine+url).text)["archived_snapshots"]
		if "closest" in data: 
			print(self.print_item(data)) 
			return (data["closest"])["available"]
		return False
	
	def load_data(self):
		return shelve.open("archived_urls.dat")["main"]
	def out_text(self, filename):
		map(open(filename, 'w').write, map(lambda x : x+"\n",self.archived_urls))
		print("Done.")
	def save_data(self):
		shelve.open("archived_urls.dat")["main"] = self.archived_urls
	def archive(self, url):
		requests.get(self._arch+url)
		print("Archiving...")
		self.archived_urls.append(url)
		self.save_data()
			
	def print_item(self, data):
		dat = data["closest"]
		stamp = "Archived:%s\nAvailable:%s\nURL:%s\nStatus:%s" % (dat["timestamp"], dat['available'], dat['url'], dat['status'])
		return stamp
		
	def save_webpage(self, url, filename):
		print("[OK]: Saving webpage..")
		if not os.path.isdir(os.getcwd()+"\\saved_webpages"): os.mkdir("saved_webpages")
		open(os.getcwd()+"\\saved_webpages\\"+filename, 'w').write(requests.get(url).text)
		if os.path.isfile(os.getcwd()+"\\saved_webpages\\"+filename): print("Done.")
	@property
	def last(self):
		return self.last[len(self.archived_urls)-1]
	@property
	def first(self):
		return self.archived_urls[0]
		
def main():
	A = Archiver()
	command_terms = ["-list_arch", "-ch", "-arch", "-outt", "-char", "-save", "-h"]
	args = sys.argv[1:len(sys.argv)]
	if args[0] in command_terms and len(args) == 1:
		if len(args) == 1:
			if args[0] == command_terms[6]:
				print("Syntax: [options] [url]\n-h A list of commands\n-ch Check if a url exists\n-arch Archive a url\n-char Check and archive a url\n-list_arch List all the urls you archived\n-outt [filename] Out put the list of archived urls into a text file\n-save [url] [filename] Saves a webpage")
				return
			elif args[0] == command_terms[0]:
				map(lambda x: print(x), A.archived_urls)
				return
		elif len(args) > 1:
			if args[0] == command_terms[1]:
				if A.available(args[1]) == True: 
					print("Already exists.\n")
					return
				else: 
					print("Does not exist.")
					return
			elif args[0] == command_terms[2]:
				A.archive(args[1])
				return
			if args[0] == command_terms[3]:
				A.out_text(args[1])
				return
			elif args[0] == command_terms[4]:
				if A.available(args[1]) == False:
					A.archive(args[1])
					return
				else: 
					print("[Error]: Already exists.\n")
					return
			if args[0] == command_terms[5]:
						if args[1] == "first":
							A.save_webpage(A.first, args[2])
							return
						elif args[1] == "last": 
							A.save_webpage(A.last, args[2])
							return
				
	else:
		print("[Error]: Unknown symbol \'%s\'" % args[0])
		return 0
		
if __name__ == "__main__":
	main()
