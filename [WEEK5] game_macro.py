import time

from selenium import webdriver # selenium 설치 후, webdriver import

# ▶ 셀레니움 사용 준비하기
driver = webdriver.Chrome('chromedriver.exe') # chromedriver파일은 따로 미리 다운받아서 저장해놓기
driver.get("http://zzzscore.com/1to50/") # 게임 사이트로 접속

# ▶ 객체 찾기
"""
* element를 elements로만 바꾸면, 모든 객체를 받아온다.

1. driver.find_element_by_name("name값“)
    → 현재 페이지에서 용이하지 않음

2. driver.find_element_by_class_name("class값“)
    → class값 box로 탐색

3. driver.find_element_by_xapth("xpath_개발자모드에서 오른쪽 클릭으로 받아올 수 있음”)
    → 규칙 찾기 
    (주의: <div style="opacity: 1;"><span class="box" style="z-index:89"></span>11</div>
            에서 div를 선택해야 함 - 잘 보면 div에 속한 텍스트임, 클릭도 div에서 하면 됨(클릭은 span으로 해도 됨))
        //*[@id="grid"]/div[1]/span
        //*[@id="grid"]/div[2]/span
        //*[@id="grid"]/div[3]/span
        ...
        //*[@id="grid"]/div[25]/span
    → 탐색과 저장에서 빠른지는 모르겠지만, 코드의 가독성은 좋은 것 같다. 
"""

# (1) Algorithm: 
# 1 to 50 이므로, 외부반복문 1~50 / 버튼 25개: 중첩 for문을 통해 반복하기
## 쉬운 방법이지만, 아주 단순히 생각해보면 50*25번의 탐색을 수행해야 해서 느릴 것이라 생각
### 실제 성능 측정: 4.701 + 4.601 + 4.501
"""
for i in range(1, 51):
    for j in range(1,26):
        btn = driver.find_element_by_xpath(f'//*[@id="grid"]/div[{j}]')
        if btn.text == str(i): # i를 그대로 쓰면 str과 int의 비교가 일어나 항상 false가 되었습니다.
            btn.click()
            break
"""
# (2) Algorithm: half & half
# 첫 번째 생각: 1 to 50이고 한 번에 25개가 뜨니까, 저장해놓고 클릭할 때 마다 갱신하고 찾고를 반복, selenium find보다 index가 빠를 것이라 생각   
## 성능개선1: 하나 발견하면 앞에 탐색한 것들 저장해놓고, 앞에 있으면 그거 클릭 없으면 뒤 탐색 -> delay때문에, 매번 0.1로 기다리느니 아래 방법을 사용하였습니다.
# 두 번째 생각: 위의 방법 문제점이 클릭 시 다음 문자로 변하는 delay이므로 25개씩 리스트 한 번에 갱신
## 성능개선2: 1단계 25개, 2단계 25개
### 실제 성능 측정: 1.2, 1.002, 1.101, 1.054, 1.1

#### 게임 시작 전 정보 파악
texts = []
boxes = driver.find_elements_by_class_name("box") # 화면 상 25개의 객체를 한번에 받아오기에는 class가 편했다.
for box in boxes:
    texts.append(box.find_element_by_xpath('..').text) # 재탐색하기보다 현재 객체의 부모를 찾도록 함

for i in range(1, 26):
    btn_index = texts.index(str(i)) # 1~25을 찾은 index를 통해 boxes에 찾을 수 있음(순서가 똑같기 때문)
    boxes[btn_index].click()

    """
    # 바뀐 값을 다시 text에 갱신 # box의 xpath 배열은 1부터 시작하므로 +1 
    ## --> 시도했는데 바뀌는 데까지 딜레이가 좀 있어서 new가 이전 값 그대로임
    new = driver.find_element_by_xpath(f'//*[@id="grid"]/div[{btn_index + 1}]').text  # 바로 넣어줘도 되는데 가독성을 위해
    texts[btn_index] = new
    """

# 결국 2단계에 나눠서 한번 더 받아오고 수행하는 걸로...
try:
    time.sleep(0.1) # stale element reference: element is not attached to the page document. 위에서 말한 딜레이 때문. implicit_wait로는 해결X
    # 게임 개발자가 딜레이 0.1로 설정해놨는지 더 작은 값을 설정하면 같은 오류 발생: 즉, 최소값이 0.1

    texts = []
    boxes = driver.find_elements_by_class_name("box") # 화면 상 25개의 객체를 한번에 받아오기에는 class가 편했다.
    for box in boxes:
        texts.append(box.find_element_by_xpath('..').text) # 재탐색하기보다 현재 객체의 부모를 찾도록 함

except:
    print("오류발생")
    time.sleep(0.05) # 위에서 딜레이 줘도 가끔 오류 뜨는 경우가 있었습니다. 이 경우 딜레이를 더 줍니다.

    texts = []
    boxes = driver.find_elements_by_class_name("box")  # 화면 상 25개의 객체를 한번에 받아오기에는 class가 편했다.
    for box in boxes:
        texts.append(box.find_element_by_xpath('..').text)  # 재탐색하기보다 현재 객체의 부모를 찾도록 함

for i in range(26, 51):
    btn_index = texts.index(str(i)) # 26~50을 찾은 index를 통해 boxes에 찾을 수 있음(순서가 똑같기 때문)
    boxes[btn_index].click()
    
## 그냥 느낌적으로만 두 번째 알고리즘이 빠르겠다~ 싶었는데 체감하니까 감회가 남다르다.