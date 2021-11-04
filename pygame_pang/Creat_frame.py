import pygame

pygame.init()  # pygame 초기화

# 화면 크기 설정
screen_width = 480
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("pygame_pang")

# 게임 진행 루프
running = True
while running:
    for event in pygame.event.get():  # 사용자의 이벤트 입력 확인
        if event.type == pygame.QUIT:
            running = False

pygame.quit()  # pygame 종료
