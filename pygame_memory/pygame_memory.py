import pygame
from random import *


def display_level_screen():    # 게임 난이도를 표시
    pygame.draw.circle(screen, (255, 255, 255), ind_level.center, 60, 5)

    msg = font.render("{0}".format(current_level), True, (255, 255, 255))
    msg_rect = msg.get_rect(center=ind_level.center)
    screen.blit(msg, msg_rect)


def display_game_screen():  # memory 게임 실행
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time > maximum_display_time:
            hidden = True

    for index, value in enumerate(answer, start=1):
        if hidden:
            pygame.draw.rect(screen, (50, 50, 50), value)
        else:
            show_cell = font.render(str(index), True, (255, 255, 255))
            show_cell_rect = show_cell.get_rect(center=value.center)
            screen.blit(show_cell, show_cell_rect)


def check_start(pos):   # 사용자가 게임 시작을 하고자하는지 확인
    global start, start_ticks

    if start:
        check_answer(pos)
    elif ind_level.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()


def check_answer(pos):  # 사용자가 선택한 것이 정답인지 확인
    global hidden, start, current_level

    for button in answer:
        if button.collidepoint(pos):
            if button == answer[0]:
                del answer[0]
                if not hidden:
                    hidden = True
            else:
                game_over()
            break

    if len(answer) == 0:
        start = False
        hidden = False
        current_level += 1
        reflect_level(current_level)


def reflect_level(level):   # 게임 난이도에 맞는 게임 출력
    global maximum_display_time

    # 게임 난이도에 따라 cell의 최대 노출 시간 조정
    maximum_display_time = 5 - (level // 3)
    maximum_display_time = max(maximum_display_time, 1)

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

            center_x = screen_left_margin + col_index * \
                total_cell_size + total_cell_size / 2
            center_y = screen_top_margin + row_index * total_cell_size + total_cell_size / 2

            cell = pygame.Rect(0, 0, real_cell_size, real_cell_size)
            cell.center = (center_x, center_y)

            answer.append(cell)


def game_over():
    global running

    running = False

    msg = font.render("Your final level is {0}.".format(
        current_level), True, (255, 255, 255))
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))
    screen.fill((0, 0, 0))
    screen.blit(msg, msg_rect)


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
hidden = False  # cell의 노출 여부를 정하기 위해 사용

# cell의 최대 노출 시간 지정
maximum_display_time = None
start_ticks = None

# 초기 게임 난이도 반영
current_level = 1
reflect_level(current_level)

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

pygame.time.delay(5000)
pygame.quit()   # pygame 종료
