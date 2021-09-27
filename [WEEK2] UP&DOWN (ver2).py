##############################
# SWING 파이썬 스터디 2주차 과제 #
##############################
import os.path
import random
import time

record = []
pointer = 0
chance = 1

# feedback: 파일 없을 때 핸들링하기 (빈 파일을 만듦)
if not os.path.isfile('record.txt'):
    print("기록을 저장하는 데 필요한 record파일이 없습니다. record 파일을 생성합니다.")
    # sys.exit()
    f = open("record.txt", "w")
    f.close()

with open("record.txt", "r", encoding='UTF-8') as f:
    while True:
        line = f.readline()
        if line:
            record.append(line.replace('\n',''))
        else:
            break

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
                    best = int(record[0][0])
                    if chance < best:
                        ### (1) 최고기록을 깬 경우 기록, 닉네임, 날짜정보 함께 저장하기
                        print("최고기록 갱신~!")
                        nickname = input("닉네임을 입력하세요 >> ")
                        record.insert(0, f"{chance}\t{nickname}\t{time.strftime('%Y-%m-%d')}")
                        # 최고기록을 맨 앞에 기록되게 코딩하면, sort 과정이 필요 없다.
                        # record.append(f"{chance}\t{nickname}\t{time.strftime('%Y-%m-%d')}")
                        # record.sort(key=lambda x: x[0])

                else:
                    print("최초로 플레이하셨습니다!")
                    nickname = input("닉네임을 입력하세요 >> ")
                    record.append(f"{chance}\t{nickname}\t{time.strftime('%Y-%m-%d')}")

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
        print(len(record))
        for rank in range(len(record)):
            print(f"{rank+1}위: {record[rank]}")

    # 3. 게임종료
    elif pointer == 3:
        with open("record.txt", "w", encoding='UTF-8') as f:
            for record_ in record:
                f.write(f"{record_}\n")
        break

    # 예외. 1-3이 아닌 다른 수를 입력했을 경우
    else :
        "올바른 번호를 선택해주세요."
