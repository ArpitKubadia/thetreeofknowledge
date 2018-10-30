import flask
import libgenapi
import json
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as soup

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


def url_opener(mirror):
	url=mirror
	uClient=uReq(url)
	page_html=uClient.read()
	uClient.close()
	page_soup=soup(page_html,"html.parser")
	containers=page_soup.find("div",{"class":"book-info"})
	name=containers.find("div",{"class":"book-info__title"}).text
	download_class=containers.find("div",{"class":"book-info__download"})
	link=download_class.find('a').get("href")
	#print(name)
	#print(link)
	magic_no=link[10:]
	#print(magic_no)
	dowloader_url="https://libgen.pw/download/book/"+magic_no
	return (name,dowloader_url)
#	r=requests.get(dowloader_url,stream=True)
#	with open(name+".pdf","wb") as pdf: 
#	    for chunk in r.iter_content(chunk_size=1024): 
#	        # writing one chunk at a time to pdf file 
#	        if chunk: 
#	            pdf.write(chunk) 

@app.route('/search/<name>', methods=['GET'])
def api_id(name):

	lg=libgenapi.Libgenapi(["http://libgen.io/","http://gen.lib.rus.ec"]) 
	#name=input("Enter the name of the book: ")
	output=lg.search(name);
	#json_output=json.load(output)
	json_output=json.dumps (output, sort_keys=True,indent=4)
	#print(json_output)
	loaded_data=json.loads(json_output)
	result=[]
	for data in loaded_data:
		if(data["mirrors"]!=None):# and (data["extension"]=="pdf" or data["extension"]=="epub")):
			for mirror in data["mirrors"]:
				if(mirror.startswith("http://libgen.pw")):
					print(mirror)
					name,url=url_opener(mirror)
					print(name)
					print(url)
					result.append({"name":name,
									"url":url})
					print("\n\n")
	result=json.dumps(result,indent=2)
	return (result)



app.run()