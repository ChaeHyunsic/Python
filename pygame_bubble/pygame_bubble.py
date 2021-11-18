import pygame
import os

class bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

def setup():
    global map

    map = [
        list("RRYYBBGG"),
        list("RRYYBBG/"),
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")
    ]

    for row_index, row in enumerate(map):
        for col_index, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_position(row_index, col_index)
            image = get_image(col)
            bubble_group.add(bubble(image, col, position))


def get_position(row_index, col_index):
    x_pos = col_index * cell_size + bubble_width // 2
    y_pos = row_index * cell_size + bubble_height // 2
    if row_index % 2 == 1:
        x_pos += cell_size // 2
    
    return x_pos, y_pos

def get_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[-1]


pygame.init()   # pygame 시작

# 화면 크기 설정
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("pygame_bubble")

# fps 설정
fps = pygame.time.Clock()

# 이미지 파일 경로 설정
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

# 게임 맵 설정
map = []
cell_size = 56
bubble_width = 56
bubble_height = 62
bubble_group = pygame.sprite.Group()

setup()
# 게임 진행 루프
running = True
while running:
    fps.tick(60)    # fps 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
            running = False

    screen.blit(background, (0,0))  # 게임 배경 지정
    bubble_group.draw(screen)

    pygame.display.update() # 변동사항 반영

pygame.quit()   # pygame 종료