import pygame
import os


def game(version):   # pang 게임 출력
    # 화면 크기 설정
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    if version == 1:    # original version
        # 타이틀 설정
        pygame.display.set_caption("original_ver")

        # 이미지 파일 경로 설정
        current_path = os.path.dirname(__file__)
        images_path = os.path.join(current_path, "original_image")

    elif version == 2:  # soccer version
        # 타이틀 설정
        pygame.display.set_caption("soccer_ver")

        # 이미지 파일 경로 설정
        current_path = os.path.dirname(__file__)
        images_path = os.path.join(current_path, "soccer_image")

    # 배경 설정
    background = pygame.image.load(os.path.join(images_path, "background.jpg"))

    # 스테이지 설정
    stage = pygame.image.load(os.path.join(images_path, "stage.jpg"))
    stage_size = stage.get_rect().size
    stage_height = stage_size[1]    # 스테이지 위에서 캐릭터가 움직이게 하기 위해 사용

    # 캐릭터 설정
    character = pygame.image.load(os.path.join(images_path, "character.jpg"))
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = screen_width / 2 - character_width / 2    # 캐릭터의 위치 조작을 위해 사용
    character_y_pos = screen_height - character_height - \
        stage_height    # 캐릭터의 위치 조작을 위해 사용
    character_speed = 0.6   # fps와 함께 캐릭터 고유 이동속도 설정

    # 캐릭터 이동 설정
    current_x_pos = 0

    # 무기 설정
    weapon = pygame.image.load(os.path.join(images_path, "weapon.jpg"))
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]
    weapon_speed = 8    # 무기 고유 이동 속도 설정
    weapon_remove = -1  # 무기가 기능을 다했을 때 소멸작용을 하기 위해 사용
    weapons = []    # 무기 연발 기능 설정을 위해 사용

    # 보스 캐릭터 설정
    boss_images = [
        pygame.image.load(os.path.join(images_path, "boss1.jpg")),
        pygame.image.load(os.path.join(images_path, "boss2.jpg")),
        pygame.image.load(os.path.join(images_path, "boss3.jpg")),
        pygame.image.load(os.path.join(images_path, "boss4.jpg"))
    ]
    boss_y_speed = [-18, -15, -12, -9]  # 보스의 상태에 따라 다른 고유 이동속도 설정을 하기 위해 사용
    boss = []   # 보스의 상태값이 많은 관계로 이를 저장하기 위해 사용
    boss.append({
        "current_x_pos": 50,
        "current_y_pos": 50,
        "current_boss": 0,
        "boss_x_pos": 3,
        "boss_y_pos": -6,
        "init_boss_y_speed": boss_y_speed[0]
    })
    boss_remove = -1    # 보스가 데미지를 입었을때 소멸작용을 하기 위해 사용

    # FPS 설정
    clock = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.Font(None, 50)

    # 최대 플레이 시간 설정
    maximum_playtime = 50
    start_playtime = pygame.time.get_ticks()

    # 최종 게임 상태 설정 (Mission Complete, Game over, Time out)
    result = "Game over"

    # 게임 진행 루프
    running = True  # 게임 진행 여부를 알기 위해 사용
    while running:
        fps = clock.tick(60)    # fps를 60으로 설정
        for event in pygame.event.get():  # 사용자의 이벤트 입력 확인
            if event.type == pygame.QUIT:   # 창닫기 이벤트 발생
                running = False

            if event.type == pygame.KEYDOWN:    # 키 눌림 이벤트 발생
                if event.key == pygame.K_LEFT:  # 왼쪽으로 이동하는 경우
                    current_x_pos -= character_speed
                elif event.key == pygame.K_RIGHT:   # 오른쪽으로 이동하는 경우
                    current_x_pos += character_speed
                elif event.key == pygame.K_SPACE:   # 무기로 공격하는 경우
                    weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])

            if event.type == pygame.KEYUP:  # 키 눌림 이벤트 종료
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    current_x_pos = 0   # 키 눌림 이벤트가 끝나면 더이상 움직이지 않도록 설정

        # 키 눌림 이벤트 반영
        character_x_pos += current_x_pos * fps

        # 캐릭터 이동가능범위 설정
        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 무기 이동범위 설정
        weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
        weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

        # 보스 이동범위 설정
        for index, value in enumerate(boss):
            boss_x_pos = value["current_x_pos"]
            boss_y_pos = value["current_y_pos"]
            boss_index = value["current_boss"]
            boss_size = boss_images[boss_index].get_rect().size
            boss_width = boss_size[0]
            boss_height = boss_size[1]

            # 보스가 벽에 부딪혔을 때 다시 튕겨져 나오도록 설정
            if boss_x_pos < 0 or boss_x_pos > screen_width - boss_width:
                value["boss_x_pos"] *= -1
            if boss_y_pos >= screen_height - stage_height - boss_height:
                value["boss_y_pos"] = value["init_boss_y_speed"]
            else:
                value["boss_y_pos"] += 0.5

            # 설정한 보스의 이동범위를 반영
            value["current_x_pos"] += value["boss_x_pos"]
            value["current_y_pos"] += value["boss_y_pos"]

        # 데미지 기능 설정
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for b_index, b_value in enumerate(boss):
            boss_x_pos = b_value["current_x_pos"]
            boss_y_pos = b_value["current_y_pos"]
            boss_index = b_value["current_boss"]
            boss_rect = boss_images[boss_index].get_rect()
            boss_rect.left = boss_x_pos
            boss_rect.top = boss_y_pos

            # 캐릭터가 보스에게 데미지를 입었을 경우 활성화
            if character_rect.colliderect(boss_rect):
                running = False
                break

            # 보스가 캐릭터에게 데미지를 입었을 경우 활성화
            for w_index, w_value in enumerate(weapons):
                weapon_x_pos = w_value[0]
                weapon_y_pos = w_value[1]
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_x_pos
                weapon_rect.top = weapon_y_pos

                if weapon_rect.colliderect(boss_rect):
                    weapon_remove = w_index  # 데미지를 입힌 무기를 소멸처리하기 위해 사용
                    boss_remove = b_index   # 데미지를 입은 보스를 소멸처리하기 위해 사용

                    if boss_index < 3:  # 보스의 최종 상태가 아니라면 실행
                        boss_width = boss_rect.size[0]
                        boss_height = boss_rect.size[1]
                        seperate_boss_rect = boss_images[boss_index + 1].get_rect()
                        seperate_boss_width = seperate_boss_rect.size[0]
                        seperate_boss_height = seperate_boss_rect.size[1]

                        # 데미지를 입은 보스는 두 개로 분열되어 좌우로 흩어지는 것을 반영
                        boss.append({
                            "current_x_pos": boss_x_pos + boss_width / 2 - seperate_boss_width / 2,
                            "current_y_pos": boss_y_pos + boss_height / 2 - seperate_boss_height / 2,
                            "current_boss": boss_index + 1,
                            "boss_x_pos": -3,
                            "boss_y_pos": -6,
                            "init_boss_y_speed": boss_y_speed[boss_index + 1]
                        })

                        boss.append({
                            "current_x_pos": boss_x_pos + boss_width / 2 - seperate_boss_width / 2,
                            "current_y_pos": boss_y_pos + boss_height / 2 - seperate_boss_height / 2,
                            "current_boss": boss_index + 1,
                            "boss_x_pos": 3,
                            "boss_y_pos": -6,
                            "init_boss_y_speed": boss_y_speed[boss_index + 1]
                        })
                    break
            else:   # 데미지 기능이 발생하지 않았다면 for문을 계속 진행하게 설정
                continue
            break   # 데미지 기능이 발생했다면 이중 for문 탈출하게 설정

        # 데미지를 입은 보스와 데미지를 입힌 무기가 있을 경우 이를 소멸하기 위해 사용
        if boss_remove > -1:
            del boss[boss_remove]
            boss_remove = -1

        if weapon_remove > -1:
            del weapons[weapon_remove]
            weapon_remove = -1

        # 보스의 최종 상태에 데미지를 입힌 경우 활성화
        if len(boss) == 0:
            result = "Mission Complete"
            running = False
            break

        # 시간 제한 설정
        playtime = (pygame.time.get_ticks() - start_playtime) / 1000
        timer = font.render(
            str(int(maximum_playtime - playtime)), True, (255, 255, 255))
        if maximum_playtime - playtime <= 0:
            result = "Timeout"
            running = False
            break

        screen.blit(background, (0, 0))  # 배경 설정 활성화

        for weapon_x_pos, weapon_y_pos in weapons:  # 무기 설정 활성화
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

        for index, value in enumerate(boss):    # 보스 설정 활성화
            boss_x_pos = value["current_x_pos"]
            boss_y_pos = value["current_y_pos"]
            boss_index = value["current_boss"]
            screen.blit(boss_images[boss_index], (boss_x_pos, boss_y_pos))

        screen.blit(stage, (0, screen_height - stage_height))   # 스테이지 설정 활성화
        screen.blit(character, (character_x_pos,
                    character_y_pos))  # 캐릭터 설정 활성화
        screen.blit(timer, (10, 10))    # 시간 제한 설정 활성화

        pygame.display.update()  # 변경사항 반영

    # 최종 게임 상태 출력
    msg = font.render(result, True, (0, 0, 0))
    msg_rect = msg.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()  # 변경사항 반영
    pygame.time.delay(2000)

def pang_version():  # pang 게임에서 version 선택하는 화면 출력
    # 화면 크기 설정
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 타이틀 설정
    pygame.display.set_caption("pygame_pang")

    # 이미지 파일 경로 설정
    current_path = os.path.dirname(__file__)
    images_path = os.path.join(current_path, "pang_image")

    # 배경 설정
    background = pygame.image.load(os.path.join(images_path, "background.jpg"))

    # 폰트 설정
    font = pygame.font.Font(None, 50)

    screen.blit(background, (0, 0))  # 배경 설정 활성화
    pygame.display.update()  # 변경사항 반영

    # version 선택창 출력
    msg = font.render("Choose the version to play : ", True, (0, 0, 255))
    msg_rect = msg.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)-50))
    choice = font.render("1: original, 2: soccer, 3: quit", True, (0, 0, 255))
    choice_rect = choice.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)+50))
    
    screen.blit(msg, msg_rect)
    screen.blit(choice, choice_rect)
    pygame.display.update()  # 변경사항 반영


pygame.init()  # pygame 시작

pang_version()  # pang 게임에서 version 선택하는 화면 출력

waiting = True  # quit를 선택하기 전까지 계속 시도할 수 있도록 하기 위해 사용
while waiting:
    for event in pygame.event.get():  # 사용자의 이벤트 입력 확인
        if event.type == pygame.QUIT:   # 창닫기 이벤트 발생
            waiting = False
            break

        if event.type == pygame.KEYDOWN:    # 키 눌림 이벤트 발생
            if event.key == pygame.K_1:     # version 1을 선택한 경우
                game(1)
                pang_version()
            elif event.key == pygame.K_2:   # version 2를 선택한 경우
                game(2)
                pang_version()
            elif event.key == pygame.K_3:   # quit를 선택한경우
                waiting = False
                break

pygame.quit()   # pygame 종료
