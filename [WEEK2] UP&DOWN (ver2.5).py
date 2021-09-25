##############################
# SWING 파이썬 스터디 2주차 과제 #
#     *   딕셔너리 버전     *   #
##############################

import random
import time

global record # append(record_dic)
record = []

pointer = 0
chance = 1

with open("record2.txt", "r", encoding='UTF-8') as f:
    record_dic={}
    while True:
        line = f.readline()
        if line:
            line.replace('\n', '')
            line.split('\t')
            record_dic['chance'] = line[0]
            record_dic['nickname'] = line[1]
            record_dic['time'] = line[2]

            record.append(record_dic)
        else:
            break

def recording(chance_):
    global record
    nickname = input("닉네임을 입력하세요 >> ")
    record_dic = {}  # {"날짜정보","닉네임","기록"}
    record_dic['time'] = time.strftime('%Y-%m-%d')
    record_dic['chance'] = chance_
    record_dic['nickname'] = nickname
    record.insert(0,record_dic)
    # 최고기록을 맨 앞에 기록되게 코딩하면, sort 과정이 필요 없다.
    # record.append(record_dic)
    # record = sorted(record, key=(lambda x:int(x['chance'])))


while True :
    print("********************************")
    print("UP & DOWN 게임에 오신 걸 환영합니다~")
    print("1. 게임시작 2. 기록확인 3. 게임종료")
    pointer = int(input(">> "))
    # 1. 게임시작
    if pointer == 1:
        min_ = 1
        max_ = 100
        collect = random.randrange(1, 100)
        print(f"이번정답: {collect}") # test용 코드

        while chance < 11:
            try:
                number = int(input(f"{chance}번째 숫자 입력({min_}~{max_}) : "))
                if number > 100 or number < 1:
                    print("1-100까지의 숫자를 입력하세요.")
                    continue
            except:
                print("1-100까지의 숫자를 입력하세요.")
                continue

            if number == collect:
                print("정답입니다!!")
                print(f"{chance}번째만에 맞추셨습니다.")
                if record:
                    best = int(record[0]['chance'])
                    if chance < best:
                        print("최고기록 갱신~!")
                        recording(chance)
                else:
                    print("최초로 플레이하셨습니다!")
                    recording(chance)
                chance = 1

                break

            elif number < collect:
                if number > min_:
                    min_ = number+1
                print("UP")
                chance = chance + 1

            elif number > collect:
                if number < max_:
                    max_ = number - 1
                print("DOWN")
                chance = chance + 1

            if chance == 11:
                print("기회를 모두 소진하였습니다. 게임오버!")
                break



    # 2. 기록확인
    elif pointer == 2:
        for rank in range(len(record)):
            print(f"{rank+1}위: {record[rank]['chance']}\t{record[rank]['nickname']}\t{record[rank]['time']}")

    # 3. 게임종료
    elif pointer == 3:
        with open("record2.txt", "w", encoding="UTF-8") as f:
            for record_ in record:
                f.write(f"{record_['chance']}\t{record_['nickname']}\t{record_['time']}\n")
        break

    # 예외. 1-3이 아닌 다른 수를 입력했을 경우
    else :
        "올바른 번호를 선택해주세요."
