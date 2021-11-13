import pygame
import os

class gemstone(pygame.sprite.Sprite):   # 4가지 종류 보석의 rect 정보를 class로 관리
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)

def gemstone_setup():   # 4가지 종류 보석 그룹화
    gemstone_group.add(gemstone(gemstone_images[0], (200, 380)))
    gemstone_group.add(gemstone(gemstone_images[1], (300, 500)))
    gemstone_group.add(gemstone(gemstone_images[2], (300, 380)))
    gemstone_group.add(gemstone(gemstone_images[3], (900, 420)))

pygame.init()   # pygame 시작

# 화면 크기 설정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# 타이틀 설정
pygame.display.set_caption("pygame_goldminer")

# fps 설정
fps = pygame.time.Clock()

# 이미지 파일 경로 설정
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.jpg"))

gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.jpg")),
    pygame.image.load(os.path.join(current_path, "big_gold.jpg")),
    pygame.image.load(os.path.join(current_path, "stone.jpg")),
    pygame.image.load(os.path.join(current_path, "diamond.jpg"))
]

# 보석 그룹 생성
gemstone_group = pygame.sprite.Group()
gemstone_setup()

# 게임 진행 루프
running = True
while running:
    fps.tick(30)    # fps를 30으로 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
            running = False

    screen.blit(background, (0, 0)) # 게임 배경 지정
    gemstone_group.draw(screen) # 보석 그룹 노출

    pygame.display.update() # 변동사항 반영

pygame.quit()   # pygame 종료