import pygame
import cv2
import numpy as np
import random
import os
import sys

# אתחול Pygame ומודול המוזיקה
pygame.init()
try:
    pygame.mixer.init()
    print("pygame.mixer מאותחל בהצלחה")
except Exception as e:
    print("שגיאה באתחול המיקסר:", e)

# רשימת קבצי וידאו
video_files = ["video.mp4", "video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4"]

# משתנה לניהול הווידאו
video = None

# משתנה גלובלי לשמירת שם הסרטון האחרון
last_video_file = None

def load_next_video():
    global video, video_files, last_video_file
    new_video_file = random.choice(video_files)
    # אם יש יותר מאחד בסרטונים, וודא שהסרטון החדש שונה מהקודם
    if last_video_file is not None and len(video_files) > 1:
        while new_video_file == last_video_file:
            new_video_file = random.choice(video_files)
    print("מעבר לסרטון:", new_video_file)
    if video is not None:
        video.release()
    video = cv2.VideoCapture(new_video_file)
    if not video.isOpened():
        print("לא ניתן לפתוח את הסרטון:", new_video_file)
    last_video_file = new_video_file

# אתחול וידאו ראשוני
load_next_video()

# רשימת קבצי מוזיקה (ודאו שהקבצים קיימים בתיקיה)
music_files = ["song.mp3", "song2.mp3", "song3.mp3", "song4.mp3"]
for mf in music_files:
    if not os.path.exists(mf):
        print("קובץ מוזיקה לא נמצא:", mf)

# משתנה לניהול מצב ניגון המוזיקה
is_music_playing = False

def toggle_music():
    global is_music_playing
    if is_music_playing:
        print("מפסיקים מוזיקה")
        pygame.mixer.music.stop()
        is_music_playing = False
    else:
        music_file = random.choice(music_files)
        print("מנסה לטעון ולהשמיע:", music_file)
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            is_music_playing = True
            print("המוזיקה מופעלת:", music_file)
        except Exception as e:
            print("שגיאה בהפעלת המוזיקה:", e)

# רשימת דמויות עם דירוגי חוזק
strength_ratings = {
    "Naruto Uzumaki": 1100,
    "Itachi Uchiha": 950,
    "Minato Namikaze": 950,
    "Third Raikage": 800,
    "Ay": 740,
    "Killer Bee": 730,
    "Sasuke Uchiha": 720,
    "Nagato (Pain)": 710,
    "Jiraiya": 700,
    "Kakashi Hatake": 670,
    "Kisame Hoshigaki": 670,
    "Tsunade Senju": 670,
    "Konan": 650,
    "Gaara": 650,
    "Second Mizukage": 640,
    "Danzo Shimura": 630,
    "Darui": 610,
    "Rasa (Gaara's Father)": 580,
    "Deidara": 580,
    "Hiruzen Sarutobi": 560,
    "Hanzo": 550,
    "Orochimaru": 540,
    "Neji Hyuga": 535,
    "Kakuzu": 535,
    "Jugo": 530,
    "Suigetsu Hozuki": 530,
    "Hidan": 525,
    "Zabuza Momochi": 525,
    "Sasori": 520,
    "Shikamaru Nara": 500,
    "Yamato": 470,
    "Rock Lee": 470,
    "Choji Akimichi": 460,
    "Asuma Sarutobi": 450,
    "Kankuro": 430,
    "Sai": 420,
    "Ino Yamanaka": 415,
    "Karin Uzumaki": 410,
    "Chiyo": 400,
    "Temari": 370,
    "Hinata Hyuga": 360,
    "Kimimaro": 350,
    "Sakura Haruno": 340,
    "Shino Aburame": 320,
    "Kiba Inuzuka": 300,
    "Konomaru Sarutobi": 270,
    "Iruka Umino": 250,
}

naruto_characters = list(strength_ratings.keys())

# הגדרת חלון וגודל המסך
width = 1080
height = 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("עומרי מטומטם")
font = pygame.font.Font(None, 36)

# טעינת תמונת img.png
try:
    img = pygame.image.load("img.png")
    img = pygame.transform.scale(img, (int(img.get_width() * 0.5), int(img.get_height() * 0.5)))
except Exception as e:
    print("שגיאה בטעינת img.png:", e)
    img = None

# רשימת תמונות לעין השארינגן
sharingan_images = ["sharingan.png", "sharingan1.png", "sharingan2.png", "sharingan3.png", "sharingan4.png"]
try:
    b = random.randint(0, len(sharingan_images)-1)
    local_sharingan = pygame.image.load(sharingan_images[b])
    local_sharingan = pygame.transform.scale(local_sharingan, (50, 50))
except Exception as e:
    print("שגיאה בטעינת sharingan:", e)
    local_sharingan = None

# משתנים לניקוד ובחירות השחקנים
player1_score = 0
player2_score = 0
player1_selection = []
player2_selection = []
used_options = []

def get_video_frame():
    """
    קורא פריים מהווידאו וממיר אותו ל-Surface של Pygame.
    במידה והווידאו הסתיים, נעשה מעבר לסרטון חדש מהרשימה.
    """
    global video
    ret, frame = video.read()
    if not ret:
        load_next_video()
        ret, frame = video.read()
        if not ret:
            return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame_surface = pygame.surfarray.make_surface(frame)
    frame_surface = pygame.transform.scale(frame_surface, (int(frame_surface.get_width() * 0.5), int(frame_surface.get_height() * 0.5)))
    return frame_surface

def get_character_options(used_options):
    all_options = list(set(naruto_characters))
    available_options = list(set(all_options) - set(used_options))
    selected_options = random.sample(available_options, min(9, len(available_options)))
    return selected_options

def choose_characters(player_selection, used_options):
    global local_sharingan
    character_options = get_character_options(used_options)
    clock = pygame.time.Clock()
    # אתחול מיקום ותנועה לעין השארינגן
    sharingan_offset = 0
    sharingan_direction = 1
    choosing = True

    big_image_x = 400
    big_image_y = 50

    while choosing:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(character_options):
                        character_name = character_options[index]
                        if character_name not in player_selection:
                            player_selection.append(character_name)
                            if len(player_selection) == 3:
                                choosing = False
                elif event.key == pygame.K_m:
                    toggle_music()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i, character in enumerate(character_options):
                        text_surface = font.render(f"{i + 1}. {character}", True, (0, 0, 255))
                        rect = text_surface.get_rect(topleft=(10, 100 + i * 40))
                        if rect.collidepoint(pos):
                            if character not in player_selection:
                                player_selection.append(character)
                                if len(player_selection) == 3:
                                    choosing = False
                            break

        # עדכון תנועת עין השארינגן
        max_offset = big_image_x - 50
        sharingan_offset += sharingan_direction * 2
        if sharingan_offset <= 0:
            sharingan_offset = 0
            sharingan_direction = 1
            # שינוי תמונה בעת שינוי כיוון
            b = random.randint(0, len(sharingan_images)-1)
            try:
                local_sharingan = pygame.image.load(sharingan_images[b])
                local_sharingan = pygame.transform.scale(local_sharingan, (50, 50))
            except:
                local_sharingan = None
        elif sharingan_offset >= max_offset:
            sharingan_offset = max_offset
            sharingan_direction = -1
            # שינוי תמונה בעת שינוי כיוון
            b = random.randint(0, len(sharingan_images)-1)
            try:
                local_sharingan = pygame.image.load(sharingan_images[b])
                local_sharingan = pygame.transform.scale(local_sharingan, (50, 50))
            except:
                local_sharingan = None

        screen.fill((255, 0, 0))

        # הצגת רשימת האפשרויות והבחירות
        for i, character in enumerate(character_options):
            text = font.render(f"{i + 1}. {character}", True, (0, 0, 255))
            screen.blit(text, (10, 100 + i * 40))
        for i, name in enumerate(player_selection):
            choice_text = font.render(f"Chosen: {name}", True, (0, 255, 0))
            screen.blit(choice_text, (10, 20 + i * 30))
        score_text = font.render(f"Player 1: {player1_score}   Player 2: {player2_score}", True, (255, 255, 0))
        screen.blit(score_text, (width // 2 - 100, 20))

        if img:
            screen.blit(img, (big_image_x, big_image_y))

        # הצגת הווידאו במקום התמונה הקבועה
        video_frame = get_video_frame()
        if video_frame:
            screen.blit(video_frame, (735, -40))

        if local_sharingan:
            eye_x = max(0, min(sharingan_offset, big_image_x - 50))
            eye_y = height - local_sharingan.get_height() - 5
            screen.blit(local_sharingan, (eye_x, eye_y))

        pygame.display.flip()

def restart_game():
    global player1_selection, player2_selection, used_options
    player1_selection = []
    player2_selection = []
    used_options = []

# בחירת דמויות לשחקן הראשון
choose_characters(player1_selection, used_options)
used_options += player1_selection
try:
    b = random.randint(0, len(sharingan_images)-1)
    local_sharingan = pygame.image.load(sharingan_images[b])
    local_sharingan = pygame.transform.scale(local_sharingan, (50, 50))
except:
    local_sharingan = None
screen.fill((255, 0, 0))
for i, name in enumerate(player1_selection):
    choice_text = font.render(f"Player 1 chose: {name}", True, (0, 255, 0))
    screen.blit(choice_text, (100, 50 + i * 30))
pygame.display.flip()
pygame.time.wait(2000)

# בחירת דמויות לשחקן השני
choose_characters(player2_selection, used_options)

# לולאת המשחק העיקרית
show_choices = True
clock = pygame.time.Clock()

while show_choices:
    clock.tick(60)
    if is_music_playing and not pygame.mixer.music.get_busy():
        print("המוזיקה הסתיימה באופן טבעי")
        is_music_playing = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_choices = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                choose_characters(player1_selection, used_options)
                used_options += player1_selection
                choose_characters(player2_selection, used_options)
            elif event.key == pygame.K_1:
                player1_score += 1
                winner_text = font.render("Player 1 won the game!", True, (0, 255, 0))
                screen.fill((255, 0, 0))
                screen.blit(winner_text, (400, 250))
                pygame.display.flip()
                pygame.time.wait(2000)
                restart_game()
                choose_characters(player1_selection, used_options)
                used_options += player1_selection
                choose_characters(player2_selection, used_options)
            elif event.key == pygame.K_2:
                player2_score += 1
                winner_text = font.render("Player 2 won the game!", True, (0, 255, 0))
                screen.fill((255, 0, 0))
                screen.blit(winner_text, (400, 250))
                pygame.display.flip()
                pygame.time.wait(2000)
                restart_game()
                choose_characters(player1_selection, used_options)
                used_options += player1_selection
                choose_characters(player2_selection, used_options)
            elif event.key == pygame.K_w:
                player1_strength = sum(strength_ratings[char] for char in player1_selection)
                player2_strength = sum(strength_ratings[char] for char in player2_selection)
                if player1_strength > player2_strength:
                    player1_score += 1
                    winner_text = font.render("Player 1 won the game!", True, (0, 255, 0))
                elif player2_strength > player1_strength:
                    player2_score += 1
                    winner_text = font.render("Player 2 won the game!", True, (0, 255, 0))
                else:
                    winner_text = font.render("It's a tie!", True, (255, 255, 0))
                screen.fill((255, 0, 0))
                screen.blit(winner_text, (400, 250))
                pygame.display.flip()
                pygame.time.wait(2000)
                restart_game()
                choose_characters(player1_selection, used_options)
                used_options += player1_selection
                choose_characters(player2_selection, used_options)
            elif event.key == pygame.K_m:
                toggle_music()

    screen.fill((255, 0, 0))
    for i, name in enumerate(player1_selection):
        choice_text = font.render(f"Player 1 chose: {name}", True, (0, 255, 0))
        screen.blit(choice_text, (10, 50 + i * 30))
    for i, name in enumerate(player2_selection):
        choice_text = font.render(f"Player 2 chose: {name}", True, (0, 255, 0))
        screen.blit(choice_text, (10, 200 + i * 30))
    score_text = font.render(f"Player 1: {player1_score}   Player 2: {player2_score}", True, (255, 255, 0))
    screen.blit(score_text, (width // 2 - 100, 20))
    if img:
        screen.blit(img, (400, 50))
    video_frame = get_video_frame()
    if video_frame:
        screen.blit(video_frame, (735, -40))
    pygame.display.flip()

pygame.quit()
video.release()
