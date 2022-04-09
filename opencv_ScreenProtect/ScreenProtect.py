import numpy as np  # numpy package import
import cv2          # opencv package import
import random       # random module import
import os           # os module import

# '조건 2. 화면 보호기 영상 출력창의 제목(title)은 “ScreenProtect_학번"으로 설정' 구현
title = 'ScreenProtect'
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)     # 지정한 title을 제목으로 한 윈도우 생성 (윈도우의 크기는 윈도우에 출력될 영상에 맞게 조정)

name = 'ChaeHyunsic'       # 영문 이름 정의

# 제공된 컬러 영상 불러오기
image = cv2.imread("color.jpg", cv2.IMREAD_COLOR)
if image is None:                                       # 만에 하나 제공된 컬러 영상이 경로에 없을 경우를 대비하여 exception처리 정의
    raise Exception("해당 이미지 파일이 존재하지 않습니다.")
image_height, image_weight = image.shape[:2]            # 불러온 컬러 영상의 size 정보(height, weight)를 나누어 저장

# 첫 영상 프레임에서 이름 구문이 위치할 좌표 정의
start_point = [random.randrange(0, image_weight+1), random.randrange(0, image_height+1)]        # 0부터 각각의 weight, height 범위 내에서 랜덤하게 생성
next_point = start_point        # 다음 프레임에서 이름 구문이 위치할 좌표를 첫 영상 프레임에서 이름 구문이 위치할 좌표로 초기화

font = cv2.FONT_HERSHEY_SIMPLEX        # 사용할 font 정의
WHITE = (255, 255, 255)                # 흰색 RGB 정보 정의

# '조건 4-2. 첫 영상 프레임에서 이름 구문의 이동 방향 또한 랜덤하게 설정' 구현
dir = random.randint(0, 3)      # 이름 구문의 이동 방향 정의 ( 첫 이동 방향은 랜덤하게 선택 )

fps = 29.97                                 # 초당 프레임 정의
delay = round(1000/fps)                     # 딜레이 정의
size = (image_weight, image_height)         # 화면 출력 및 저장 영상 크기 정의
fourcc = cv2.VideoWriter_fourcc(*'DX50')    # 코덱 종류 정의

file_index = 0      # imwrite를 통해 저장될 영상 갯수 정의
frame = []          # imread를 통해 읽어올 img를 연속적으로 append할 list 정의

while True:
    # '조건 6. 키보드 입력키 ‘q’ 누르면 종료. 그 전까지는 무한반복' 구현
    # '조건 7-1. 동영상 및 화면 설정' 구현 (딜레이(delay) = round(1000/fps))
    return_key = cv2.waitKey(delay)     # 딜레이동안 key 입력을 받기 위해 대기
    if return_key == ord('q'):
        break                           # 키보드 입력키 'q'를 누르면 무한 반복되는 while문 탈출

    # '조건 1. 자신의 영문 이름이 대각선 방향으로 이동하면서 화면 보호기처럼 동작' 구현
    # '조건 4. 이름 구문(text)은 대각선 방향으로 이동, 이동 크기는 자유' 구현
    # '조건 5. 이름 구문이 영상의 경계선을 만나면 90도 회전하여 이동(이름 구문의 시작 좌표가 경계선을 만나는 것을 기준)' 구현
    if dir == 0:    # 우측 하향 대각선 방향인 경우
        next_point = [next_point[0] + 1, next_point[1] + 1]     # x좌표 1px, y좌표 1px 증가
        if next_point[0] >= image_weight:   # 우측 경계선을 만났을 경우
           next_point[0] = image_weight     # 우측 경계선 이상의 값을 가지지 못하도록 제한
           next_point[1] -= 1               # 우측 경계선을 만났을 당시의 값으로 롤백
           dir = 2                          # 90도 회전하여 좌측 하향 대각선 방향으로 지정
        elif next_point[1] >= image_height:     # 하단 경계선을 만났을 경우
             next_point[0] -= 1                 # 하단 경계선을 만났을 당시의 값으로 롤백
             next_point[1] = image_height       # 하단 경계선 이상의 값을 가지지 못하도록 제한
             dir = 1                            # 90도 회전하여 우측 상향 대각선 방향으로 지정
    elif dir == 1:  # 우측 상향 대각선 방향인 경우
        next_point = [next_point[0] + 1, next_point[1] - 1]     # x좌표 1px 증가, y좌표 1px 감소
        if next_point[0] >= image_weight:   # 우측 경계선을 만났을 경우
           next_point[0] = image_weight     # 우측 경계선 이상의 값을 가지지 못하도록 제한
           next_point[1] += 1               # 우측 경계선을 만났을 당시의 값으로 롤백
           dir = 3                          # 90도 회전하여 좌측 상향 대각선 방향으로 지정
        elif next_point[1] <= 0:    # 상단 경계선을 만났을 경우
             next_point[0] -= 1     # 상단 경계선을 만났을 당시의 값으로 롤백
             next_point[1] = 0      # 상단 경계선 이하의 값을 가지지 못하도록 제한
             dir = 0                # 90도 회전하여 우측 하향 대각선 방향으로 지정
    elif dir == 2:  # 좌측 하향 대각선 방향인 경우
        next_point = [next_point[0] - 1, next_point[1] + 1]     # x좌표 1px 감소, y좌표 1px 증가
        if next_point[0] <= 0:      # 좌측 경계선을 만났을 경우
           next_point[0] = 0        # 좌측 경계선 이하의 값을 가지지 못하도록 제한
           next_point[1] -= 1       # 좌측 경계선을 만났을 당시의 값으로 롤백
           dir = 0                  # 90도 회전하여 우측 하향 대각선 방향으로 지정
        elif next_point[1] >= image_height:     # 하단 경계선을 만났을 경우
             next_point[0] += 1                 # 하단 경계선을 만났을 당시의 값으로 롤백
             next_point[1] = image_height       # 하단 경계선 이상의 값을 가지지 못하도록 제한
             dir = 3                            # 90도 회전하여 좌측 상향 대각선 방향으로 지정
    elif dir == 3:  # 좌측 상향 대각선 방향인 경우
        next_point = [next_point[0] - 1, next_point[1] - 1]     # x좌표 1px 감소, y좌표 1px 감소
        if next_point[0] <= 0:      # 좌측 경계선을 만났을 경우
           next_point[0] = 0        # 좌측 경계선 이하의 값을 가지지 못하도록 제한
           next_point[1] += 1       # 좌측 경계선을 만났을 당시의 값으로 롤백
           dir = 1                  # 90도 회전하여 우측 상향 대각선 방향으로 지정
        elif next_point[1] <= 0:        # 상단 경계선을 만났을 경우
             next_point[0] += 1         # 상단 경계선을 만났을 당시의 값으로 롤백
             next_point[1] = 0          # 상단 경계선 이하의 값을 가지지 못하도록 제한
             dir = 2                    # 90도 회전하여 좌측 하향 대각선 방향으로 지정

    # '조건 3. 제공된 영상(‘color.jpg’)이 배경이 되고, 본인의 이름 구문(text) 부분만 마스킹(masking) 되어 보이도록 함' 구현
    # '조건 4-1. 첫 영상 프레임에서 이름 구문의 위치는 랜덤하게 설정' 구현 (첫 영상 프레임에서 next_point에는 start_point의 정보가 들어있다)
    text = np.zeros_like(image)                                 # image와 같은 형식을 zero로 초기화하여 text 정의
    cv2.putText(text, name, next_point, font, 1.5, WHITE, 6)    # name을 next_point 위치에 font로 1.5배율 크기, 6굵기의 흰색으로 text에 이름 구문 출력
    mask = cv2.bitwise_and(image, text)                         # image에 이름 구문 마스킹
    cv2.imshow(title, mask)                                     # 마스킹한 영상 출력
    cv2.imwrite(str(file_index)+".jpg", mask)                   # 출력된 영상 frame 캡처 후 저장
    file_index += 1                                             # frame 캡처할 때마다 count

cv2.destroyAllWindows()         # 활성화 되어 있는 모든 윈도우 파괴

# 종료되기 전까지 캡처된 모든 frame을 순서대로 list에 append
for i in range(file_index):
        img = cv2.imread(str(i)+".jpg", cv2.IMREAD_COLOR)
        frame.append(img)

# '조건 7. 종료후 ‘ScreenProtect_본인학번.avi’로 동작 화면을 동영상으로 1분 내외 저장' 구현
# '조건 7-1. 동영상 및 화면 설정' 구현
# '초당 프레임 (fps) = 29.97'
# '화면 출력 및 저장 영상 크기(size) = ‘color.jpg’ 크기와 동일'
# '코덱종류(fourcc) = cv2.VideoWriter_fourcc(*'DX50')'
result = cv2.VideoWriter("ScreenProtect.avi", fourcc, fps, size)   # 'DX50' 코딩 방식, 29.97fps, (480, 360)size로 녹화할 동영상을 지정된 이름과 형식으로 생성
for i in range(len(frame)):
    result.write(frame[i])      # 종료되기 전까지 캡처된 모든 frame을 순서대로 동영상에 출력

result.release()    # 녹화 종료

# 캡처된 모든 frame 파일 제거
for i in range(file_index):
    os.remove(str(i)+".jpg")