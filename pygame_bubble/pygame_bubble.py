import pygame
import os

class bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

class pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.position = position
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.origin_image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, angle_move):
        self.angle += angle_move

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)

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

pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))

# 게임 맵 설정
map = []
cell_size = 56
bubble_width = 56
bubble_height = 62

# 버블 그룹 생성
bubble_group = pygame.sprite.Group()

# 포인터 설정
pointer_group = pointer(pointer_image, (screen_width // 2, 624), 90)
angle_left = 0
angle_right = 0
angle_speed = 1.5

setup()
# 게임 진행 루프
running = True
while running:
    fps.tick(60)    # fps 60으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                angle_right -= angle_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                angle_left = 0
            elif event.key == pygame.K_RIGHT:
                angle_right = 0

    screen.blit(background, (0,0))  # 게임 배경 지정
    bubble_group.draw(screen)
    pointer_group.rotate(angle_left + angle_right)
    pointer_group.draw(screen)

    pygame.display.update() # 변동사항 반영

pygame.quit()   # pygame 종료