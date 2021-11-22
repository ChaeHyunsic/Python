import pygame
import os
import random
import math

class bubble(pygame.sprite.Sprite):     # bubble의 rect 정보를 class로 관리
    def __init__(self, image, color, position=(0,0), row_index=-1, col_index=-1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18
        self.row_index = row_index
        self.col_index = col_index

    def set_rect(self, position):   # rect 정보를 갱신해야할 때 사용
        self.rect = self.image.get_rect(center = position)

    def draw(self, screen, x_pos = None):   # group과 같이 draw 메소드를 사용하기 위해 사용
        if x_pos:   # 움직이는 객체일 경우 이를 반영
            screen.blit(self.image, (self.rect.x + x_pos, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

    def set_angle(self, angle):     # angle 정보를 갱신해야할 때 사용
        self.angle = angle
        self.rad_angle = math.radians(self.angle)

    def move(self):     # bubble을 fire했을 때의 움직임 구현
        x_pos = self.radius * math.cos(self.rad_angle)
        y_pos = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += x_pos
        self.rect.y += y_pos

        if self.rect.left < 0 or self.rect.right > screen_width:    # 화면 밖으로 나가지 않도록 설정
            self.set_angle(180 - self.angle)

    def set_index(self, row_index, col_index):  # index 정보를 갱신해야할 때 사용
        self.row_index = row_index
        self.col_index = col_index
        
    def drop(self, height): # 화면 밖에 존재하고 있는 벽을 점차 화면에 등장시킬 때 화면 상의 bubble들을 이에 맞게 조정하기 위해 사용
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + height))

class pointer(pygame.sprite.Sprite):    # pointer의 rect 정보를 class로 관리
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.position = position
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.origin_image = image

    def draw(self, screen):     # group과 같이 draw 메소드를 사용하기 위해 사용
        screen.blit(self.image, self.rect)

    def rotate(self, angle_move):   # pointer가 회전을 통해 조준 할 수 있도록 하기 위해 사용
        self.angle += angle_move

        # pointer의 angle 회전 제한 설정
        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)

def setup():    # 게임을 시작하기 전 필요한 기본 정보 구축
    global map

    level = choice_level()  # 게임 난이도 설정

    if level == 1:
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
    elif level == 2:
        map = [
            list("...YY..."),
            list("...G.../"),
            list("...R...."),
            list("...B.../"),
            list("...R...."),
            list("...G.../"),
            list("...P...."),
            list("...P.../"),
            list("........"),
            list("......./"),
            list("........")
        ]
    elif level == 3:
        map = [
            list("G......G"),
            list("RGBYRGB/"),
            list("Y......Y"),
            list("BYRGBYR/"),
            list("...R...."),
            list("...G.../"),
            list("...R...."),
            list("......./"),
            list("........"),
            list("......./"),
            list("........")
        ] 

    # 선택된 맵에 맞는 정보 불러오기
    for row_index, row in enumerate(map):
        for col_index, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_position(row_index, col_index)
            image = get_image(col)
            bubble_group.add(bubble(image, col, position, row_index, col_index))


def get_position(row_index, col_index):     # 상황에 따라 bubble들이 올바른 위치를 찾게 하기 위해 사용
    x_pos = col_index * cell_size + bubble_width // 2
    y_pos = row_index * cell_size + bubble_height // 2 + wall_height
    if row_index % 2 == 1:
        x_pos += cell_size // 2
    
    return x_pos, y_pos

def get_image(color):   # 맵에 지정된 bubble의 이미지를 불러오기 위해 사용
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
        return bubble_images[-1]    # 마지막 이미지 bubble은 게임 종료시 출현

def prepare_bubbles():  # pointer에 의해 fire되는 bubble과 그 다음 fire될 bubble에 대한 정의를 하기 위해 사용
    global current_bubble
    global next_bubble

    if next_bubble:
        current_bubble = next_bubble
    else:
        current_bubble = create_bubble()

    current_bubble.set_rect((screen_width //2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

def create_bubble():    # bubble 객체를 생성해야할 때 사용
    color = get_color()
    image = get_image(color)
    return bubble(image, color)

def get_color():    # 현재 화면 상 표시되어 있는 bubble들의 color 중에서 fire될 bubble의 color를 선택할 수 있게 하기 위해 사용
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    
    return random.choice(colors)

def collision():    # bubble끼리 충돌했을 때와 bubble이 천장에 충돌했을 때의 충돌 현상을 처리 하기 위해 사용
    global current_bubble, fire, fire_count

    col_bubble = pygame.sprite.spritecollideany(current_bubble, bubble_group, pygame.sprite.collide_mask)
    if col_bubble or current_bubble.rect.top <= wall_height:
        row_index, col_index = get_index(*current_bubble.rect.center)   # tuple 형태가 아닌 분리된 변수를 parameter로 넘겨줌
        place_bubble(current_bubble, row_index, col_index)
        remove_bubbles(row_index, col_index, current_bubble.color)
        current_bubble = None   # 이미 fire된 current bubble 정보 초기화
        
        # fire되었음으로 이에 따른 상태 반영
        fire = False
        fire_count -= 1

def get_index(x, y):    # 상황에 따라 bubble들이 올바른 위치를 찾게 하기 위해 사용
    row_index = (y - wall_height) // cell_size
    col_index = x // cell_size

    if row_index % 2 == 1:
        col_index = (x - cell_size // 2) // cell_size
        if col_index < 0:
            col_index = 0
        elif col_index > 6:
            col_index = 6

    return row_index, col_index

def place_bubble(current_bubble, row_index, col_index):     # fire된 bubble이 올바른 자리에 place되고 해당 bubble을 bubble group에 추가하기 위해 사용
    map[row_index][col_index] = current_bubble.color
    position = get_position(row_index, col_index)
    current_bubble.set_rect(position)
    current_bubble.set_index(row_index, col_index)
    bubble_group.add(current_bubble)

def remove_bubbles(row_index, col_index, color):    # place된 bubble이 bubble pop 조건에 만족한다면 remove 시키기 위해 사용
    visited.clear() # 이전 visited 정보 초기화
    visit(row_index, col_index, color)
    if len(visited) >= 3:   # 같은 color의 bubble이 3개 이상 겹친다면 pop 조건을 만족하도록 설정
        remove_visited()
        remove_alone()

def visit(row_index, col_index, color=None):    # place 된 bubble이 bubble pop 조건에 만족하는지 확인 하기 위해 사용
    if row_index < 0 or row_index >= 11 or col_index < 0 or col_index >= 8:     # 화면 밖은 탐색하지 않도록 설정
        return

    if color and map[row_index][col_index] != color:    # color에 대한 정보가 확실한지 확인하도록 설정
        return

    if map[row_index][col_index] in [".", "/"]:     # 비어있거나 존재할 수 없는 cell은 아닌지 확인하도록 설정
        return

    if (row_index, col_index) in visited:   # 이미 한번 탐색한 cell은 더이상 탐색하지 않도록 설정
        return

    visited.append((row_index, col_index))

    # cell을 기준으로 존재하는 모든 방향의 bubble을 탐색하도록 설정
    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]
    if row_index % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]

    for i in range(len(rows)):
        visit(row_index + rows[i], col_index + cols[i], color)

def remove_visited():   # bubble pop 조건을 만족하여 해당 bubble을 remove 하기 위해 사용
    remove_bubble = [i for i in bubble_group if (i.row_index, i.col_index) in visited]
    for j in remove_bubble:
        map[j.row_index][j.col_index] = "."
        bubble_group.remove(j)

def remove_alone(): # 어떠한 상황에 의해 천장과의 연결고리가 끊어진 bubble이 있는지 탐색
    visited.clear()
    for col_index in range(8):
        if map[0][col_index] != ".":
            visit(0, col_index)

    remove_visited_alone()

def remove_visited_alone():     # 어떠한 상황에 의해 천장과의 연결고리가 끊어진 bubble을 정리하기 위해 사용
    remove_bubble = [i for i in bubble_group if (i.row_index, i.col_index) not in visited]
    for j in remove_bubble:
        map[j.row_index][j.col_index] = "."
        bubble_group.remove(j)

def draw_bubbles():     # bubble group에 속해있는 bubble들을 화면 상에 그리기 위해 사용
    # fire count에 따라 화면 흔들림 기능 설정
    x_pos = None
    if fire_count == 2:
        x_pos = random.randint(-1, 1)
    elif fire_count == 1:
        x_pos = random.randint(-4, 4)

    for bubble in bubble_group:
        bubble.draw(screen, x_pos)

def drop_wall():    # fire count에 따라 벽이 내려오는 기능 설정
    global wall_height, fire_count

    wall_height += cell_size
    for bubble in bubble_group:
        bubble.drop(cell_size)

    fire_count = max_fire_count # fire count 초기화

def get_bottom_bubble():    # 가장 아래에 위치하고 있는 bubble의 rect 정보를 얻기 위해 사용
    bottom_bubbles = [bubble.rect.bottom for bubble in bubble_group]

    return max(bottom_bubbles)

def change_bubble(image):   # game over 되었을 때 화면 상의 모든 bubble들을 회색으로 변경하기 위해 사용
    for bubble in bubble_group:
        bubble.image  = image

def display_result():   # 게임 result 출력
    text = font.render(result, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(text, text_rect)

def choice_level():     # 게임 난이도 선택 기능 설정
    screen.blit(background, (0, 0))  # 배경 설정 임시 활성화
    pygame.display.update()  # 변경사항 반영

    msg = font.render("Choose the level to play : ", True, (255, 255, 255))
    msg_rect = msg.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)))
    
    screen.blit(msg, msg_rect)  # 난이도 선택 기능 활성화
    pygame.display.update()  # 변경사항 반영

    waiting = True  # 사용자가 난이도를 선택할 때까지 대기하도록 하기 위해 사용
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:     
                    waiting = False
                    return 1
                elif event.key == pygame.K_2:   
                    waiting = False
                    return 2
                elif event.key == pygame.K_3:   
                    waiting = False
                    return 3

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

# 게임 맵, cell 설정
map = []
cell_size = 56
bubble_width = 56
bubble_height = 62
visited = []

# 버블 그룹 생성
bubble_group = pygame.sprite.Group()

# 포인터 설정
pointer_group = pointer(pointer_image, (screen_width // 2, 624), 90)
angle_left = 0
angle_right = 0
angle_speed = 1.5
current_bubble = None
next_bubble = None
fire = False    # 포인터에서 버블이 연사되지 않도록 하기 위해 사용

# 시도 횟수 제한 설정
max_fire_count = 7
fire_count = max_fire_count
wall = pygame.image.load(os.path.join(current_path, "wall.png"))
wall_height = 0

# 게임 종료 여부 (게임 결과 정보 포함)
result = None

# 폰트 설정
font = pygame.font.SysFont("arialrounded", 40)

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
            elif event.key == pygame.K_SPACE:
                if current_bubble and not fire:
                    fire = True
                    current_bubble.set_angle(pointer_group.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                angle_left = 0
            elif event.key == pygame.K_RIGHT:
                angle_right = 0

    # fire관련 기능 활성화
    if not current_bubble:
        prepare_bubbles()

    if fire:
        collision()

    if fire_count == 0:
        drop_wall()

    if not bubble_group:    # 화면 상의 모든 bubble이 remove되었을 때 발생
        result = "Mission Complete"
    elif get_bottom_bubble() > len(map) * cell_size:    # 가장 아래의 bubble이 기준선을 넘어갔을 때 발생
        result = "Game Over"
        change_bubble(bubble_images[-1])

    screen.blit(background, (0, 0))  # 게임 배경 지정
    screen.blit(wall, (0, wall_height - screen_height))  # 벽 기능 활성화
    draw_bubbles()
    pointer_group.draw(screen)  # pointer 기능 활성화
    pointer_group.rotate(angle_left + angle_right)  # pointer 회전 기능 활성화

    # current bubble, next bubble을 화면 상에 노출
    if current_bubble:
        if fire:
            current_bubble.move()
        current_bubble.draw(screen)

    if next_bubble:
        next_bubble.draw(screen)

    if result != None:      # 게임 종료 발생
        display_result()
        running = False

    pygame.display.update() # 변동사항 반영

pygame.time.delay(2000)
pygame.quit()   # pygame 종료