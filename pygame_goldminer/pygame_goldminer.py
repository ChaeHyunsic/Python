import pygame
import os


class gemstone(pygame.sprite.Sprite):   # 4가지 종류 보석의 rect 정보를 class로 관리
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)


class claw(pygame.sprite.Sprite):   # 집게 rect 정보를 class로 관리
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(40, 0)   # 집게의 pivot을 중심으로 움직이는 값
        self.position = position  # 집게의 pivot

        self.direction = -1  # 집게의 이동 방향
        self.angle_speed = 2.5  # 집게의 좌우 이동 속도
        self.angle = 10  # 집게의 각도

    def draw(self, screen):  # group이 아닌 객체에서 draw 메소드를 사용하기 위해 선언
        pygame.draw.line(screen, (0, 0, 0), self.position,
                         self.rect.center, 5)   # 집게가 움직이는 동선 표시
        screen.blit(self.image, self.rect)

    def update(self, x_pos):   # 집게의 설정 반영
        if self.direction == -1:    # 집게가 왼쪽으로 이동하고 있는 경우
            self.angle += self.angle_speed
        elif self.direction == 1:   # 집게가 오른쪽으로 이동하고 있는 경우
            self.angle -= self.angle_speed

        if self.angle > 170:    # 집게가 왼쪽 끝에 도달한 경우
            self.angle = 170
            self.set_direction(1)
        elif self.angle < 10:   # 집게가 오른쪽 끝에 도달한 경우
            self.angle = 10
            self.set_direction(-1)

        self.offset.x += x_pos

        self.rotate()

    def rotate(self):   # 각도에 따라 집게 회전
        self.image = pygame.transform.rotozoom(
            self.original_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position + offset_rotated)
   
    def set_direction(self, direction):
        self.direction = direction

    def init_setting(self):
        self.offset.x = 40
        self.angle = 10
        self.direction = -1


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

# 집게 생성
claw_image = pygame.image.load(os.path.join(current_path, "claw.jpg"))
claw_group = claw(claw_image, (screen_width // 2, 110))

# 집게 이동 설정
x_pos = 0
claw_speed = 12
claw_return_speed = 20

# 게임 진행 루프
running = True
while running:
    fps.tick(30)    # fps를 30으로 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:    # 마우스 클릭 이벤트 발생시 실행
            claw_group.set_direction(0)
            x_pos = claw_speed

    # 집게 이동범위 지정
    if claw_group.rect.left < 0 or claw_group.rect.right > screen_width or claw_group.rect.bottom > screen_height:
        x_pos = -claw_return_speed

    if claw_group.offset.x < 40:
        x_pos = 0
        claw_group.init_setting()

    screen.blit(background, (0, 0))  # 게임 배경 지정
    gemstone_group.draw(screen)  # 보석 그룹 생성
    claw_group.update(x_pos)  # 집게 설정 반영
    claw_group.draw(screen)  # 집게 생성

    pygame.display.update()  # 변동사항 반영

pygame.quit()   # pygame 종료
