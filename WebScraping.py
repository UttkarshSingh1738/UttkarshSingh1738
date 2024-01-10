import urllib.request
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import ast
import json
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
String ="";
number_of_chapters = 1
for k in tqdm(range(1,number_of_chapters+1)):
    url = "https://novelfull.com/warriors-promise/chapter-" + str(k) + ".html"
    headers={'User-Agent':user_agent,}
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    html = data.decode("utf-8")
    pattern = "<title.*?>.*?</title.*?>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    title = match_results.group()
    title = re.sub("<.*?>", "", title)
    title = title[5:35] + "\n"
    soup = BeautifulSoup(html, "html.parser")
    AH = soup.get_text()
    print(AH)
    index1 = AH.find("Transn") + 22
    index = AH.find("If you find any errors")
    AH = AH[index1:index] + "\n"
    String += (title + AH )
#print(String)
#f= open("Warriors's Promise.txt","w+")
#f.write(String)
