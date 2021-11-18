import pygame
import os

pygame.init()   # pygame 시작

# 화면 크기 설정
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("pygame_bobble")

# fps 설정
fps = pygame.time.Clock()

# 이미지 파일 경로 설정
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 게임 진행 루프
running = True
while running:
    fps.tick(60)    # fps 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
            running = False

    screen.blit(background, (0,0))  # 게임 배경 지정
    pygame.display.update() # 변동사항 반영

pygame.quit()   # pygame 종료