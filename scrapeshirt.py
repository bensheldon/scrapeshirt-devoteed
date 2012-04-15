 #!/usr/bin/python

from BeautifulSoup import BeautifulSoup
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import re
import urllib2
import base64, urllib

# set the variables
USERNAME = 'SideOfBacon'
PASSWORD = '?????????'
STATUS_URL = 'http://shirtsonsale.shoutem.com/api/twitter/1.0/statuses/update.json'

if __name__ == '__main__': 
	main()

def main():
	## Woot
	woot = scrape_woot()
	status = 'Woot! ' + woot['title'] + '. ' + woot['url']
	update_status(status, get_image(woot['image']))

  ## TeeFury
	teefury = scrape_teefury()
	status = 'TeeFury: ' + teefury['title'] + '. ' + teefury['url']
	update_status(status, get_image(teefury['image']))

  ## RIPT
	ript = scrape_ript()
	status = 'RIPT Apparel: ' + ript['title'] + '. ' + ript['url']
	update_status(status, get_image(ript['image']))
	
	## Tilteed /BROKEN
  # 	tilteed = scrape_tilteed()
  # 	status = 'Tilteed: ' +tilteed['title'] + '. ' + tilteed['url']
  # 	update_status(status, get_image(tilteed['image']))
	
	
##
# Update the status
##
def update_status (status, imagepath):

	# Register the streaming http handlers with urllib2
	register_openers()

	# Encode the parameters
	datagen, headers = multipart_encode({'status' : status,
																			 'include_shoutem_fields' : 'true',
																			 'file_attachment' : open(imagepath)})

	# Create the Request object
	request = urllib2.Request(STATUS_URL, datagen, headers)
	# Add the authorization (there is probably a better way to do this
	request.headers['Authorization'] = 'Basic %s' % ( base64.b64encode(USERNAME + ':' + PASSWORD),)
	# Actually do t he request, and return the response
	return urllib2.urlopen(request).read()	

##
# Get the image (stores in memory)
##
def get_image(url):
	opener = urllib2.build_opener()
	page = opener.open(url)
	imagedata = page.read()

	filepath = 'images/' + url.split("/")[-1]
	fout = open(filepath, "wb")
	fout.write(imagedata)
	fout.close()

	return filepath


## 
# WOOT!
## 
def scrape_woot():
	response = urllib2.urlopen("http://shirt.woot.com/")
	html = response.read()
	soup = BeautifulSoup(html)
	
	product = soup.find("div", { "class" : "hproduct clearfix" })
	
	image = product.find('a')['href']
	
	#find a string between single quotes
	search = re.compile("(?:[^\\']+|\\.)*")
	
	image = search.findall(image)[0]
		
	title = product.find("h2", { "class" : "fn" }).find(text=True)
	
	url = product.find('a', { "class" : "url" })['href']
	
	return {"url":url, "title":title, "image":image}



##
# Tilteed
##
def scrape_tilteed():
	response = urllib2.urlopen("http://www.tilteed.com/")
	html = response.read()
	soup = BeautifulSoup(html)
	
	product = soup.find("div", { "id" : "mainshirt" })
	
	url = product.find('a')['href']
	
	image = product.find('img')['src']
	
	title = soup.find("div",{"id" : "maininfo"}).find("span", { "class" : "shirtname"}).find("a", text=True)
	
	return {"url":url, "title":title, "image":image}
	
##
# Tee Fury
##
def scrape_teefury():
	response = urllib2.urlopen("http://www.teefury.com/")
	html = response.read()
	soup = BeautifulSoup(html)
	
	url = "http://teefury.com" #doesn't change
	
	# Awful html for teefury
	image = soup.find('td', {"colspan": "3"}).find('img')['src']
		
	image = "http://www.teefury.com/" + image

	title = soup.find("div", {"id" : "product_title"}).find(text=True)
	
	return {"url":url, "title":title, "image":image}

##
# RIPT Apparel
##
def scrape_ript():
	response = urllib2.urlopen("http://www.riptapparel.com/")
	html = response.read()
	soup = BeautifulSoup(html)
	
	url = soup.find("h1",{"class" : "postTitle"}).find('a')['href']
	title = soup.find("h1",{"class" : "postTitle"}).find('a')['title']
	image = soup.find('div', {"class": "detailView"}).find('img')['src']
		
	return {"url":url, "title":title, "image":image}


	

	
	