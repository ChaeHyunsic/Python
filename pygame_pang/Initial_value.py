import pygame

pygame.init()  # pygame 초기화

# 화면 크기 설정
screen_width = 480
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 배경 설정
background = pygame.image.load(
    "D:\\작업\\Python\\pygame_pang\\background_color.png")

# 캐릭터 설정
character = pygame.image.load("D:\\작업\\Python\\pygame_pang\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height
character_speed = 0.6

# 캐릭터 이동 설정
current_x_pos = 0
current_y_pos = 0

# 보스 캐릭터 설정
boss = pygame.image.load("D:\\작업\\Python\\pygame_pang\\boss.png")
boss_size = boss.get_rect().size
boss_width = boss_size[0]
boss_height = boss_size[1]
boss_x_pos = screen_width / 2 - boss_width / 2
boss_y_pos = screen_height / 2 - boss_height / 2

# FPS 설정
clock = pygame.time.Clock()

# 폰트 설정
font = pygame.font.Font(None, 40)

# 최대 플레이 시간 설정
maximum_playtime = 10
start_playtime = pygame.time.get_ticks()

# 화면 타이틀 설정
pygame.display.set_caption("pygame_pang")

# 게임 진행 루프
running = True
while running:
    fps = clock.tick(60)    # fps를 60으로 설정
    for event in pygame.event.get():  # 사용자의 이벤트 입력 확인
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생
            running = False

        if event.type == pygame.KEYDOWN:    # 키 눌림 이벤트 발생
            if event.key == pygame.K_LEFT:
                current_x_pos -= character_speed
            elif event.key == pygame.K_RIGHT:
                current_x_pos += character_speed
            elif event.key == pygame.K_UP:
                current_y_pos -= character_speed
            elif event.key == pygame.K_DOWN:
                current_y_pos += character_speed

        if event.type == pygame.KEYUP:  # 키 눌림 이벤트 종료
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                current_x_pos = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                current_y_pos = 0

    # 키 눌림 이벤트 반영
    character_x_pos += current_x_pos * fps
    character_y_pos += current_y_pos * fps

    # 캐릭터 이동가능범위 설정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 데미지 기능 설정
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    boss_rect = boss.get_rect()
    boss_rect.left = boss_x_pos
    boss_rect.top = boss_y_pos

    # 데미지 기능 활성화
    if character_rect.colliderect(boss_rect):
        running = False

    # 시간 제한 설정
    playtime = (pygame.time.get_ticks() - start_playtime) / 1000
    timer = font.render(
        str(int(maximum_playtime - playtime)), True, (255, 255, 255))
    if maximum_playtime - playtime <= 0:
        running = False

    screen.blit(background, (0, 0))  # 배경 설정 활성화
    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 설정 활성화
    screen.blit(boss, (boss_x_pos, boss_y_pos))  # 보스 캐릭터 설정 활성화
    screen.blit(timer, (10, 10))    # 시간 제한 설정 활성화

    pygame.display.update()  # 변경사항 반영

pygame.quit()  # pygame 종료
