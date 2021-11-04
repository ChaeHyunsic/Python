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

# 화면 타이틀 설정
pygame.display.set_caption("pygame_pang")

# 게임 진행 루프
running = True
while running:
    for event in pygame.event.get():  # 사용자의 이벤트 입력 확인
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))  # 배경 설정 활성화
    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 설정 활성화

    pygame.display.update()  # 변경사항 적용

pygame.quit()  # pygame 종료
