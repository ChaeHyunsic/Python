import pygame


def display_level_screen():    # 게임 난이도를 표시
    pygame.draw.circle(screen, (255, 255, 255), ind_level.center, 60, 5)


def display_game_screen():  # memory 게임 실행
    pass


def check_start(pos):   # 사용자가 게임 시작을 하고자하는지 확인
    global start

    if ind_level.collidepoint(pos):
        start = True


pygame.init()   # pygame 시작

# 화면 크기 설정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("pygame_memory")

# 게임 난이도 표시 기능
ind_level = pygame.Rect(0, 0, 120, 120)
ind_level.center = (120, screen_height - 120)
start = False   # 게임 시작 여부 확인을 위해 사용

# 게임 진행 루프
running = True
while running:
    click_pos = None    # 마우스 클릭한 좌표를 기억하기 위해 사용

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONUP:    # 마우스 클릭 이벤트 발생시 실행
            click_pos = pygame.mouse.get_pos()

    screen.fill((0, 0, 0))    # 게임 배경 지정

    if start:
        display_game_screen()
    else:
        display_level_screen()  # 게임 난이도 표시 기능 활성화

    if click_pos:
        check_start(click_pos)

    pygame.display.update()  # 변동 사항 반영

pygame.quit()   # pygame 종료
