##############################
# SWING 파이썬 스터디 1주차 과제 #
##############################

# detail1. 예외처리: 숫자 외 입력 불가(선택지 및 게임 내 숫자 입력)
# detail2. max, min을 더 크게 입력해도 조정X (1~30일때 40 입력해도 1~40으로 조정되지 않음)
# detail3. __위: __ 로 표시함
### 테스트결과는 같은 폴더 내 png 파일로 첨부하였습니다. (정답 알려주는 test용 코드 포함하여 테스트함)

import random

pointer = 0 # 선택지의 번호를 담을 변수 선언
chance = 1 # 기회를 담을 변수 선언
record = [] # record를 담을 변수 미리 선언

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

        # feedback1: 범위가 아닌 수를 입력한 경우는 입력 카운트 안되게 하기
        # for을 while문으로 변경하고 chance변수를 따로 선언하여 정상 입력에서만 카운트되도록 하기
        while chance < 11:
            try:
                number = int(input(f"{chance}번째 숫자 입력({min_}~{max_}) : "))
                if number > 100 or number < 1:
                    print("1-100까지의 숫자를 입력하세요.")
                    continue
            except:
                print("1-100까지의 숫자를 입력하세요.")
                continue

            if number == collect: # 정답을 맞췄을 경우,
                print("정답입니다!!")
                print(f"{chance}번째만에 맞추셨습니다.") # 몇번만에 맞췄는지 알려주고
                if record:
                    best = min(record) # 현재 record 내 최솟값(best)와 비교해서
                    if chance < best:
                        print("최고기록 갱신~!") # 최고기록인지 알려주기
                        record.append(chance)  # 그 후! record에 추가하기
                else: # feedback2: 최고기록만 기록에 추가하기
                    # record가 없는 첫번째 기록이 문제라 if문 아래에 두지 못했는데,
                    # else를 추가하여 해당 경우에도 핸들링 되도록 함
                    record.append(chance) #

                chance = 1 # chance를 1로 초기화하여 다음 게임을 준비함

                break

            elif number < collect: # 정답보다 작은 수를 입력했을 경우,
                if number > min_: # 최솟값 범위 조정
                    min_ = number+1
                print("UP")
                chance = chance + 1  # 정상 입력, 실패했을 때만 카운트가 올라감

            elif number > collect: # 정답보다 큰 수를 입력했을 경우,
                if number < max_: # 최댓값 범위 조정
                    max_ = number-1
                print("DOWN")
                chance = chance + 1  # 정상 입력, 실패했을 때만 카운트가 올라감

    # 2. 기록확인
    elif pointer == 2:
        record.sort()
        for i,j in zip(range(len(record)),record): # 기록 확인 시 편의를 위해 zip 사용
            print(f"{i+1}위: {j}")

    # 3. 게임종료
    elif pointer == 3:
        break

    # 예외. 1-3이 아닌 다른 수를 입력했을 경우
    else :
        "올바른 번호를 선택해주세요."
