import urllib.request
from bs4 import BeautifulSoup

url = "http://www.swu.ac.kr/www/swuniversity.html"
web = urllib.request.urlopen(url)
soup = BeautifulSoup(web, "html.parser")

print("*** 서울여자대학교 학과 및 홈페이지 정보 ***\n")
print("학과\t\t\t\t\t\t홈페이지")

uls = soup.findAll("ul", {"class":"col_list0"})

for ul in uls:
    lis = ul.findAll("li")
    for li in lis:
        name = li.a.text
        if ("학과" in name) or ("학부" in name) or ("전공" in name):
            url = "http://www.swu.ac.kr" + li.a["href"]
            web = urllib.request.urlopen(url)
            soup = BeautifulSoup(web, "html.parser")

            try:
                link = soup.find("span", text="홈페이지 바로가기").parent["href"]
                print(f"{name}\t\t\t{link}")

            except:
                print(f"{name}\t\t\t홈페이지가 존재하지 않음")
                pass
"""

"""