from __future__ import print_function
import sys, time
import requests, urllib
import demjson, shelve
import os.path


		
class Archiver:
	def __init__(self):
                """
                A class for archiving URLS into the wayback machine
                """
		self._machine = "http://archive.org/wayback/available?url="
		self._arch = "https://web.archive.org/save/"
		self.archived_urls = []
		
		# load data
		if os.path.isfile("archived_urls.dat"):
			self.archived_urls = self.load_data()

	def available(self, url, silent=False):
                """
                :param: url
                :param: silent=False
                Checks if the given URL exists in the wayback machine.
                The silent argument if set True does not print anything to the console
                """
		print("[Checking]: %s\n" % url) if silent == False else 0
		data = demjson.decode(requests.get(self._machine+url).text)["archived_snapshots"]
		if "closest" in data: 
			print(self.print_item(data)) if silent == False else 0
			return (data["closest"])["available"]
		return False
	
	def load_data(self):
                """
                Loads the archived URLS from a file called archived_urls.dat
                """
		return shelve.open("archived_urls.dat")["main"]
	def out_text(self, filename):
                """
                :param: filename
                Outputs a list of archived urls into text format
                """
		map(open(filename, 'w').write, map(lambda x : x+"\n",self.archived_urls))
		print("Done.")
	def save_data(self):
                """
                Saves the archived urls into archived_urls.dat
                """
		shelve.open("archived_urls.dat")["main"] = self.archived_urls
	def archive(self, url):
                """
                :param: url
                Archves a url into the wayback machine.
                """
		l = requests.get(self._arch+url)
		print("Archiving...")
		self.archived_urls.append(url)
		self.save_data()
			
	def print_item(self, data):
                """
                :param: data
                Print function for json data for archive data
                """
		dat = data["closest"]
		stamp = "Archived:%s\nAvailable:%s\nURL:%s\nStatus:%s" % (dat["timestamp"], dat['available'], dat['url'], dat['status'])
		return stamp
		
	def save_webpage(self, url, filename):
                """
                :param: url
                :param: filename
                Saves a webpage 
                """
		print("[OK]: Saving webpage..")
		if not os.path.isdir(os.getcwd()+"\\saved_webpages"): os.mkdir("saved_webpages")
		open(os.getcwd()+"\\saved_webpages\\"+filename, 'w').write((requests.get(url).text).encode("utf-8"))
		if os.path.isfile(os.getcwd()+"\\saved_webpages\\"+filename): print("Done.")


Help = \
" \
Usage: archive.py [option] [option2]\n \
\
Options:\n \
        -CH/ch [url] - Check if a URL already exists in the wayback machine and return it's information if it does\n \
        -ARCH/arch [url] - Archive a URL\n \
        -CHARCH/charch [url] - Archive a url if it doesn't already exists\n \
        -OUTT/outt [filename] - Output a list of archived urls in text format\n \
        -H/h - Print this help message\n \
        -LARCH/larch - print out a list of urls you archived\n \
        -SAVE/save [url] [filename] - Save a url into a file"

def main():
        global Help
        A = Archiver()
        args = map(lambda x : x.lower(), sys.argv[1:len(sys.argv)])
        print(args)
        if len(args) == 2:
                print(args[0])
                if args[0] == "-ch":
                        if A.available(args[1]) is True:
                                print("URL found.")
                        else:
                                print("URL not found in wayback machine.")
                        sys.exit(0)
                elif args[0] == "-arch":
                        A.archive(args[1])
                        if A.available(args[1], True) is True:
                                print("[Success]: Archiving is successful")
                        else:
                                print("[Error]: Archiving failed!")
                        sys.exit(0)
                elif args[0] == "-charch":
                        main = A.available(args[1])
                        if main is True or main == "True":
                                print("URL exists.")
                        elif main is False:
                                print("URL does not exist.")
                                A.archive(args[1])
                        sys.exit(0)
                elif args[0] == "-outt":
                        A.out_text(args[1])
                        sys.exit(0)
        elif len(args) == 3:
                if args[0] == "-save":
                        A.save_webpage(args[1], args[2])
                        sys.exit(0)
        
        elif len(args) == 1:
                if args[0] == "-h":
                        print("-h")
                        print(Help)
                        sys.exit(0)
                elif args[0] == "-larch":
                        print("-larch")
                        map(lambda x : print(x), A.archived_urls)
                        sys.exit(0)
                else:
                        print("[Error]: Unknown argument \'%s\'" % args[0])
                        sys.exit(0)
        else:
                print("Archiver: No arguments found.\n Type '-h' for help")
                sys.exit(0)
		
if __name__ == "__main__":
        main()
