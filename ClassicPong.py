import pygame as py
import webcolors
import winsound
import threading
#Inits
py.init()
py.font.init()


# Fenstergröße festlegen
width, height = 800, 600
screen = py.display.set_mode((width, height), py.DOUBLEBUF)  # Doublebuffering Flag activated
py.display.set_caption("Pong")
screen.fill(webcolors.name_to_hex("Grey"))

# Center Coords
center_x = screen.get_width() // 2
center_y = screen.get_height() // 2

# Coords Ball
x_ball = 400
y_ball = 300
ball_size = 10  # Größe des Balls

# Speed
speed_x = 4
speed_y = 4

# Set Player1
x_player1 = 20
y_player1 = center_y
height_player = 80
width_player = 10

# Set Player2
x_player2 = 760
y_player2 = center_y

#ScoreBoard
score_player1 = 0
score_player2 = 0

# V für Verschieben Player
move = 5  # Geschwindigkeit der Spielerbewegung

#Flag für Counter
score = False

#Beep Sound auf weiteren Thread damit spiel nicht stoppt: 
def play_beep(frequency=300, duration=200):
    threading.Thread(target=winsound.Beep, args=(frequency, duration), daemon=True).start()

# Clock
clock = py.time.Clock()

# Haupt-Schleife, um das Fenster offen zu halten
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Tastenzustand abfragen
    keys = py.key.get_pressed()

    # Bewegung von Player 1 (W und S)
    if keys[py.K_w]:  # Hoch
        y_player1 -= move
    if keys[py.K_s]:  # Runter
        y_player1 += move

    # Bewegung von Player 2 (Pfeil hoch und Pfeil runter)
    if keys[py.K_UP]:  # Hoch
        y_player2 -= move
    if keys[py.K_DOWN]:  # Runter
        y_player2 += move

    # Begrenze die Spieler innerhalb des Bildschirms
    y_player1 = max(0, min(y_player1, height - height_player// 2))  # Player 1
    y_player2 = max(0, min(y_player2, height - height_player // 2))  # Player 2

    # Spielfeld löschen
    screen.fill(webcolors.name_to_hex("Black"))

    # ___________________________DrawingMap____________________________________________
    strich_hight = 20  # Höhe eines Strichs
    gap_height = 10  # Höhe der Lücke zwischen den Strichen
    strich_width = 8  # Breite eines Strichs

    y = 0  # Startposition Y
    while y < height:  # // 2 für true Mid
        py.draw.rect(screen, webcolors.name_to_hex("White"), [center_x - (strich_hight // 2), y, strich_width, strich_hight])
        y += strich_hight + gap_height  # nächster Strich

    # ____________________________Moving Pong__________________________________________
    pong = py.Rect(x_ball, y_ball, ball_size, ball_size)  #Ball als Rechteck
    py.draw.rect(screen, webcolors.name_to_hex("Red"), pong)
    x_ball += speed_x
    y_ball += speed_y

    # Kollision mit Wänden
    if x_ball >= width or x_ball <= 0:  # Logik Hitting Wall
        speed_x = speed_x * -1
    if y_ball >= height or y_ball <= 0:
        speed_y = speed_y * -1

    # ____________________________Moving Bars___________________________________________
    # Draw Player 1
    player1 = py.Rect(x_player1, y_player1 - (height_player // 2), width_player, height_player)
    py.draw.rect(screen, webcolors.name_to_hex("White"), player1)

    # Draw Player 2
    player2 = py.Rect(x_player2, y_player2 - (height_player // 2), width_player, height_player)
    py.draw.rect(screen, webcolors.name_to_hex("White"), player2)

    if pong.colliderect(player1):
        x_ball = x_player1 + width_player  #Ball leicht nach Rechts setzen um erneuten hit zu vermeiden
        speed_x = abs(speed_x)  #Make safe to move right
        play_beep()  # 800 Hz für 200 ms

    if pong.colliderect(player2):
        x_ball = x_player2 - ball_size  
        speed_x = -abs(speed_x) 
        play_beep()  # 800 Hz für 200 ms


    #Draw Score Board
    font = py.font.Font(None, 36)  # Standard-Schriftart, Größe 36
    score_text = font.render(f"{score_player1} - {score_player2}", True, (webcolors.name_to_hex("White")))
    screen.blit(score_text, (width // 2 - 30, 10))


    #Logik Point for hitting Borders left/ right
    if x_ball < 5 and score == False:
        score_player2 += 1
        score = True
        x_ball, y_ball = center_x, center_y
    elif x_ball > 755 and score == False:
        score_player1 += 1
        score = True
        x_ball, y_ball = center_x, center_y
        
    # Nach der Punktezählung zurücksetzen
    if x_ball > 5 and x_ball < 755:
        score = False

    # Fenster aktualisieren
    py.display.flip()

    # Framerate auf 60 FPS begrenzen
    clock.tick(60)

py.quit()