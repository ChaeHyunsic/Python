import pygame
from random import *

def display_level_screen():    # 게임 난이도를 표시
    pygame.draw.circle(screen, (255, 255, 255), ind_level.center, 60, 5)


def display_game_screen():  # memory 게임 실행
    for index, value in enumerate(answer, start=1):
        pygame.draw.rect(screen, (50, 50, 50), value)

        show_cell = font.render(str(index), True, (255, 255, 255))
        show_cell_rect = show_cell.get_rect(center =value.center)
        screen.blit(show_cell, show_cell_rect)

def check_start(pos):   # 사용자가 게임 시작을 하고자하는지 확인
    global start

    if ind_level.collidepoint(pos):
        start = True

def reflect_level(level):   # 게임 난이도에 맞는 게임 출력
    total_count = (level // 3) + 5
    total_count = min(total_count, 20)

    shuffle_grid(total_count)

def shuffle_grid(total_count):
    rows = 5
    columns = 9
    number = 1
    total_cell_size = 130
    real_cell_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    grid = [[0 for col in range(columns)] for row in range(rows)]
    while number <= total_count:
        row_index = randrange(0, rows)
        col_index = randrange(0, columns)

        if grid[row_index][col_index] == 0:
            grid[row_index][col_index] = number
            number += 1

            center_x = screen_left_margin + col_index * total_cell_size + total_cell_size / 2
            center_y = screen_top_margin + row_index * total_cell_size + total_cell_size / 2

            cell = pygame.Rect(0, 0, real_cell_size, real_cell_size)
            cell.center = (center_x, center_y)

            answer.append(cell)


pygame.init()   # pygame 시작

# 화면 크기 설정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("pygame_memory")

# 폰트 설정
font = pygame.font.Font(None, 120)

# 게임 난이도 표시 기능
ind_level = pygame.Rect(0, 0, 120, 120)
ind_level.center = (120, screen_height - 120)
start = False   # 게임 시작 여부 확인을 위해 사용
answer = []     # 게임의 정답을 저장해두어 사용자의 답변과 비교하기 위해 사용

# 초기 게임 난이도 반영
reflect_level(1)

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
