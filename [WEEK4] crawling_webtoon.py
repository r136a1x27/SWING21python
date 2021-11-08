import urllib.request
import os
from bs4 import BeautifulSoup

def filenamePreprocessing(file_name):
    file_name = file_name.replace('/', '／').replace('\\', '').replace(':', '：').replace('*', '＊').replace('"', '″') \
                         .replace('?', '？').replace('|', '｜').replace('<', '[').replace('>', '>')
    return file_name

url = "https://comic.naver.com/webtoon/list?titleId=726214"
web = urllib.request.urlopen(url)
soup = BeautifulSoup(web, "html.parser")


subject = soup.find("head").find("title").text  # 웹툰명
print(f"*** 웹툰 {subject} 크롤링 시작 ***")
p_subject = filenamePreprocessing(subject)
os.mkdir(p_subject)
os.chdir(p_subject)

tis = soup.findAll("td", {"class":"title"})

for ti in tis:
    lis = ti.findAll("a")
    for li in lis:
        title = li.text # 회차별 제목 받아오기
        print(f"[+] {title} 크롤링 중...")
        # 회차별 제목 전처리
        p_title = filenamePreprocessing(title)
        # 회차별 제목 폴더 생성하기
        os.mkdir(p_title)
        os.chdir(p_title)

        # 해당 회차로 이동하기
        link = li['href']
        url = "https://comic.naver.com" + link
        web = urllib.request.urlopen(url)
        soup = BeautifulSoup(web, "html.parser")

        # 이미지 정보 불러오기
        imgs = soup.find("div", {"class":"wt_viewer"}).findAll("img")

        i = 0
        for img in imgs:
            # 오프너 세팅
            opener = urllib.request.build_opener()
            opener.addheaders=[('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")]
            urllib.request.install_opener(opener)

            img_url = img['src'] # 이미지 url 불러오기
            number = str(i).zfill(2)
            urllib.request.urlretrieve(img_url, f'./{number}.jpg')
            i = i+1
        os.chdir("../")
        # 이미지 저장하기

print("** 크롤링이 완료되었습니다 **")
