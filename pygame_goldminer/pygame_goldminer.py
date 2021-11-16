import pygame
import os
import math

def game(): # 게임 난이도를 반영한 게임 실행
    global level

    class gemstone(pygame.sprite.Sprite):   # 4가지 종류 보석의 rect 정보를 class로 관리
        def __init__(self, image, position, price, weight):
            super().__init__()
            self.image = image
            self.rect = image.get_rect(center=position)
            self.price = price
            self.weight = weight

        # 정지 상태일때, 혹은 집게에 의해 이동하는 상태일때의 보석 위치 설정
        def set_position(self, position, angle):
            rad_angle = math.radians(angle)
            x_pos = self.rect.size[0] // 2 * math.cos(rad_angle)
            y_pos = self.rect.size[0] // 2 * math.sin(rad_angle)

            self.rect.center = (position[0] + x_pos, position[1] + y_pos)


    class claw(pygame.sprite.Sprite):   # 집게의 rect 정보를 class로 관리
        def __init__(self, image, position):
            super().__init__()
            self.image = image
            self.original_image = image
            self.rect = image.get_rect(center=position)
            self.offset = pygame.math.Vector2(40, 0)   # 집게의 pivot을 중심으로 움직이는 값
            self.position = position
            self.direction = -1  # 집게의 이동 방향 (-1: LEFT, 1:RIGHT)
            self.angle_speed = 2.5  # 집게의 좌우 이동 속도
            self.angle = 10  # pivot을 기준으로 집게의 각도

        def draw(self, screen):  # group이 아닌 객체에서 draw 메소드를 사용하기 위해 선언
            pygame.draw.line(screen, (0, 0, 0), self.position,
                            self.rect.center, 5)   # 집게가 움직이는 동선 표시
            screen.blit(self.image, self.rect)

        def update(self, x_pos):   # 집게의 이동 설정
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

            self.rotate()   # 각도에 따라 집게 회전

        def rotate(self):   # 각도에 따라 집게 회전
            self.image = pygame.transform.rotozoom(
                self.original_image, -self.angle, 1)    # 부드러운 회전을 위해 bilt이 아닌 rotozoom 사용
            offset_rotated = self.offset.rotate(self.angle)
            self.rect = self.image.get_rect(center=self.position + offset_rotated)

        def set_direction(self, direction): # 집게 이동 방향 지정
            self.direction = direction

        def init_setting(self): # 초기 설정으로 초기화 해야할 때 사용
            self.offset.x = 40
            self.angle = 10
            self.direction = -1


    def gemstone_setup():   # 4가지 종류 보석 그룹화
        small_gold_price, small_gold_weight = 100, 5
        big_gold_price, big_gold_weight = 300, 2
        stone_price, stone_weight = 10, 2
        diamond_price, diamond_weight = 600, 7

        gemstone_group.add(
            gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_weight))
        gemstone_group.add(
            gemstone(gemstone_images[0], (400, 400), small_gold_price, small_gold_weight))
        gemstone_group.add(
            gemstone(gemstone_images[0], (600, 450), small_gold_price, small_gold_weight))
        gemstone_group.add(
            gemstone(gemstone_images[0], (800, 400), small_gold_price, small_gold_weight))
        gemstone_group.add(
            gemstone(gemstone_images[0], (1150, 380), small_gold_price, small_gold_weight))

        gemstone_group.add(
            gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_weight))
        gemstone_group.add(
            gemstone(gemstone_images[1], (800, 500), big_gold_price, big_gold_weight))

        gemstone_group.add(
            gemstone(gemstone_images[2], (300, 380), stone_price, stone_weight))
        gemstone_group.add(
            gemstone(gemstone_images[2], (700, 330), stone_price, stone_weight))
        gemstone_group.add(
            gemstone(gemstone_images[2], (1000, 480), stone_price, stone_weight))

        gemstone_group.add(
            gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_weight))
        gemstone_group.add(
            gemstone(gemstone_images[3], (150, 500), diamond_price, diamond_weight))

    def display_score():    # 현재 난이도와 점수, 목표점수 출력
        level_text = font.render(f"Current level : {level}", True, (0, 0, 0))
        screen.blit(level_text, (50, 20))

        current_text = font.render(f"Current score : {current_score:,}", True, (0, 0, 0))
        screen.blit(current_text, (50, 60))

        goal_text = font.render(f"Goal score : {goal:,}", True, (0, 0, 0))
        screen.blit(goal_text, (50, 100))

    def display_time(time): # 남은 시간 출력
        text = font.render(f"Time : {time}", True, (0, 0, 0))
        screen.blit(text, (1100, 40))

    def display_result():   # 결과 출력
        font = pygame.font.SysFont("arialrounded", 60)  # 좀 더 큰 크기로 출력하기 위해 font 재정의
        text = font.render(result, True, (0, 0, 0))
        text_rect = text.get_rect(center=(int(screen_width/2), int(screen_height / 2)))
        screen.blit(text, text_rect)

    # 화면 크기 설정
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 타이틀 설정
    pygame.display.set_caption("pygame_goldminer")

    # fps 설정
    fps = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.SysFont("arialrounded", 30)

    # 이미지 파일 경로 설정
    current_path = os.path.dirname(__file__)
    background = pygame.image.load(os.path.join(current_path, "background.jpg"))

    gemstone_images = [
        pygame.image.load(os.path.join(current_path, "small_gold.png")).convert_alpha(),
        pygame.image.load(os.path.join(current_path, "big_gold.png")).convert_alpha(),
        pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(),
        pygame.image.load(os.path.join(current_path, "diamond.png")).convert_alpha()
    ]

    # 보석 그룹 생성
    gemstone_group = pygame.sprite.Group()
    gemstone_setup()
    gemstone_caught = None

    # 집게 생성
    claw_image = pygame.image.load(os.path.join(current_path, "claw.png")).convert_alpha()
    claw_group = claw(claw_image, (screen_width // 2, 5))

    # 집게 이동 설정
    x_pos = 0
    claw_speed = 12
    claw_return_speed = 20

    # 점수 기능 설정
    if level > 20:
        goal = 2000
    else:
        goal = level * 100
    current_score = 0

    # 제한 시간 설정
    result = None
    if level > 20:
        total_time = 100 - (level % 10)
    else:
        total_time = 100
    start_time = pygame.time.get_ticks()

    # 게임 진행 루프
    running = True
    while running:
        fps.tick(30)    # fps를 30으로 설정
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # 창닫기 이벤트 발생시 실행
                running = False
                level = 0

            if event.type == pygame.MOUSEBUTTONDOWN:    # 마우스 클릭 이벤트 발생시 실행
                if claw_group.direction != 0:   # 집게가 좌우 이동 상태라면 멈춤
                    claw_group.set_direction(0)
                    x_pos = claw_speed

        # 집게 이동범위 지정
        if claw_group.rect.left < 0 or claw_group.rect.right > screen_width or claw_group.rect.bottom > screen_height:
            x_pos = -claw_return_speed

        # 집게가 발사되었다가 원위치로 돌아왔을때 처리 과정 설정
        if claw_group.offset.x < 40:
            x_pos = 0
            claw_group.init_setting()

            if gemstone_caught: # 집게가 보석을 집어온 경우 그에 대한 점수 반영
                current_score += gemstone_caught.price
                gemstone_group.remove(gemstone_caught)
                gemstone_caught = None

        # 집게가 보석을 잡는 과정 설정
        if not gemstone_caught:
            for gemstone in gemstone_group:
                if pygame.sprite.collide_mask(claw_group, gemstone):
                    gemstone_caught = gemstone
                    x_pos = -gemstone.weight
                    break

        # 집게가 보석을 잡아가는 과정 설정
        if gemstone_caught:
            gemstone_caught.set_position(claw_group.rect.center, claw_group.angle)

        screen.blit(background, (0, 0))  # 게임 배경 지정
        gemstone_group.draw(screen)  # 보석 그룹 생성
        claw_group.update(x_pos)  # 집게 설정 반영
        claw_group.draw(screen)  # 집게 생성
        display_score() # 현재 난이도와 점수, 목표 점수 출력

        if current_score >= goal:
            level += 1
            running = False
            if level == 30:
                result = "All Mission Complete"
                display_result()    # 결과 출력 기능 활성
            else:
                result = "Mission Complete"
                display_result()    # 결과 출력 기능 활성화

        # 시간 제한 설정 활성화
        elapsed_time = int((pygame.time.get_ticks() - start_time) / 1000)
        display_time(total_time - elapsed_time)

        if total_time - elapsed_time <= 0:
            level = 0
            running = False
            result = "Game Over"
            display_result()    # 결과 출력 기능 활성화

        pygame.display.update()  # 변동사항 반영

    pygame.time.delay(2000)

pygame.init()   # pygame 시작

level = 1

while 30 > level > 0:   # 지정된 난이도 안에서 순차적으로 게임이 계속 실행되도록 설정 (게임을 포기하거나 게임오버가 된 경우에는 종료)
    game()


pygame.quit()   # pygame 종료
