import sys, time
import requests, urllib
import demjson
import shelve
import os.path
import mechanize


		
class Archiver:
	def __init__(self):
		self._machine = "http://archive.org/wayback/available?url="
		self._arch = "https://web.archive.org/save/"
		self.archived_urls = []
		
		# load data
		if os.path.isfile("archived_urls.dat"):
			self.archived_urls = self.load_data()
		
	def available(self, url):
		print "[Checking]: %s\n" % url
		archive = requests.get(self._machine+url)
		ds = demjson.decode(archive.text)
		if "closest" in ds["archived_snapshots"]:
			ac = ds["archived_snapshots"]
			cs = ac["closest"]
			check_ = cs["available"]
			print self.print_item(ds)
			return True
		return False
	
	def load_data(self):
		p = shelve.open("archived_urls.dat")
		ar = p["main"]
		p.close()
		return ar
		
	def out_text(self, filename):
		o = open(filename, 'w')
		for y in self.archived_urls:
			o.write(y+"\n")
		o.close()
		print "Done."
		
	def save_data(self):
		output = shelve.open("archived_urls.dat")
		output["main"] = self.archived_urls
		output.close()
		
	def archive(self, url):
		if url != None:
			response = requests.get(self._arch+url)
			print "Archiving..."
			self.archived_urls.append(url)
			self.save_data()
			
	def print_item(self, data):
		dat = data["archived_snapshots"]
		dat = dat["closest"]
		stamp = "Archived:%s\nAvailable:%s\nURL:%s\nStatus:%s" % (dat["timestamp"], dat['available'], dat['url'], dat['status'])
		return stamp
		
	def save_webpage(self, url, filename):
		print "[OK]: Saving webpage..\n"
		web = mechanize.Browser()
		response = br.open(url)
		if not os.path.isdir(os.getcwd()+"\\saved_webpages"):
			mkdir("saved_webpages")
		wp = open(os.getcwd()+"\\saved_webpages\\"+filename, 'w')
		wp.write(response)
		wp.close()
		@property
	def last(self):
		return self.last
	@property
	def first(self):
		return self.archived_urls[0]
		
	@property
	def last_item(self):
		return archived_urls[len(self.archived_urls)-1]
	@property
	def first_item(self):
		return archived_urls[0]

		

if __name__ == "__main__":
	A = Archiver()
	arg = sys.argv[1:len(sys.argv)]

	if len(arg) == 0:
		print "press -h for a list of commands"
		sys.exit(0)
		
	elif len(arg) == 1:
		if arg[0] == "-list_arch":
			for x in A.archived_urls:
				print x+"\n"
			sys.exit(0)
	if len(arg) > 1:
		print arg[0]
		if arg[0] == '-ch':
			result = A.available(arg[1])
			if result == True:
				print "Already exists.\n"
			elif result == False:
				print "Does not exist."
			sys.exit(0)
		elif arg[0] == '-arch':
			A.last_url = arg[1]
			A.archive(arg[1])
			sys.exit(0)
		if arg[0] == "-outt":
			A.out_text(arg[1])
			sys.exit(0)
		elif arg[0] == '-char':
			response = A.available(arg[1])
			if response == False:
				A.archive()
			else: print "[OK]: Already exists.\n"
			sys.exit(0)
		if arg[0] == "-save":
			A.save_webpage(arg[1], arg[2])
		else:
			print "Unknown symbol %s" % arg[0]
			sys.exit()
	elif len(arg) <= 1 and len(arg) != 0:
		if arg[0] == "-h":
			help = "Syntax: [options] [url]\n-h A list of commands\n-ch Check if a url exists\n-arch Archive a url\n-char Check and archive a url\n-list_arch List all the urls you archived\n-outt [filename] Out put the list of archived urls into a text file\n-save [url] [filename] Saves a webpage"
			print help
			sys.exit(0)