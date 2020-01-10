from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

days = 30

d = datetime.datetime.today()
d_x = d + datetime.timedelta(days=days)

#print(str(d.year)+"-"+str(d.month)+"-"+str(d.day))
start_date = str(d.year)+"-"+str(d.month)+"-"+str(d.day)
end_date = str(d_x.year)+"-"+str(d_x.month)+"-"+str(d_x.day)

banned_words = ['Oxford Housing','Bursley Hall','South Quad','South Quadrangle','North Quad','North Quadrangle','East Quad','East Quadrangle','Mosher-Jordan Hall', "Mary Markley Hall"]
url = "https://events.umich.edu/list?filter=tags:Food,&range="+start_date+"to"+end_date
print(url)

#acceses the page from the url as a html
client = uReq(url)
#stores the page
page = client.read()
#closes the url
client.close()

page_soup = soup(page, "html.parser")
title = page_soup.findAll("div", {"class":"event-title"})
locations = page_soup.findAll("div", {"class":"event-info"})
date_time = page_soup.findAll("div", {"class":"event-listing-grid"})

size = len(locations)
date = []

for i in range(size):
	date.append(date_time[i].time["datetime"])

file = open("events.txt", "w") 
file.write("Subject,Start date,Start Time,End date,End Time,Location\n")

for i in range(size):
	if locations[i].ul.li.a["title"] not in banned_words:

		date_time = date[i].split(" ")
		hour = date_time[1].split(":")
		hour_int = int(hour[0])
		if(hour_int > 22):
			hour_int = hour_int - 22;
		hour_int = hour_int + 2;
		end_str = str(hour_int)+":"+hour[1]

		file.write(title[i].h3.a["title"]+","+date_time[0]+","+date_time[1]+","+date_time[0]+","+end_str+","+locations[i].ul.li.a["title"]+"\n") 

file.close()
