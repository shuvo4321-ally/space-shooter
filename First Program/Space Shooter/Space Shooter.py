
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import random
import math
import time

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

score = 0
lives = 3

game_over_lives = False
game_over_blocks = False
difficulty = None


stars = []
num_stars = 130

spaceship_x = WINDOW_WIDTH // 2
spaceship_y = 50
spaceship_width = 40
spaceship_height = 30
spaceship_speed = 13

invincible = False
invincible_start = 0

bullets = []
bullet_speed = 15
three_way_shoot = False
three_way_shoot_start = 0

blocks = []
block_sizes = [20, 30, 40]

falling_hearts = []
heart_size = 17

falling_arrows = []
arrow_size = 18

power_ups = []
power_up_size = 18


difficulty_settings = {
    "Easy": {"heart_speed": 3, "heart_spawn_rate": 0.003, "arrow_speed": 3, "arrow_spawn_rate": 0.03},
    "Medium": {"heart_speed": 5, "heart_spawn_rate": 0.002, "arrow_speed": 5, "arrow_spawn_rate": 0.07},
    "Hard": {"heart_speed": 6, "heart_spawn_rate": 0.001, "arrow_speed": 7, "arrow_spawn_rate": 0.1}
}

def draw_pixel(x, y):
    GL.glBegin(GL.GL_POINTS)
    GL.glVertex2f(x, y)
    GL.glEnd()

def midpoint_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_pixel(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        draw_pixel(xc + x, yc + y)
        draw_pixel(xc - x, yc + y)
        draw_pixel(xc + x, yc - y)
        draw_pixel(xc - x, yc - y)
        draw_pixel(xc + y, yc + x)
        draw_pixel(xc - y, yc + x)
        draw_pixel(xc + y, yc - x)
        draw_pixel(xc - y, yc - x)

        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

def draw_heart(x, y, size):
    GL.glColor3f(1.0, 0.0, 0.0)  

    # top of the heart
    midpoint_circle(x - size // 4, y, size // 4)
    midpoint_circle(x + size // 4, y, size // 4)

    # bottom of the heart
    midpoint_line(x - size // 2, y, x, y - size // 2)
    midpoint_line(x + size // 2, y, x, y - size // 2)

def draw_arrow(x, y, size):
    # Arrow body
    GL.glColor3f(1.0, 1.0, 0.0)  
    midpoint_line(x, y, x - size // 2, y - size // 2)  
    midpoint_line(x, y, x + size // 2, y - size // 2)  
    midpoint_line(x - size // 2, y - size // 2, x, y - size)  
    midpoint_line(x + size // 2, y - size // 2, x, y - size)  

    # Cockpit
    GL.glColor3f(0.0, 1.0, 1.0)  
    midpoint_circle(x, y - size // 3, size // 6)

    # Thrusters
    GL.glColor3f(1.0, 0.0, 0.0) 
    midpoint_circle(x - size // 4, y + size // 6, size // 8)
    midpoint_circle(x + size // 4, y + size // 6, size // 8)

    # Flames
    GL.glColor3f(1.0, 0.5, 0.0)  
    midpoint_line(x - size // 4, y + size // 6, x - size // 4, y + size // 4)
    midpoint_line(x + size // 4, y + size // 6, x + size // 4, y + size // 4)

    GL.glColor3f(1.0, 1.0, 0.0) 
    midpoint_line(x - size // 5, y + size // 4, x - size // 4, y + size // 6)
    midpoint_line(x + size // 5, y + size // 4, x + size // 4, y + size // 6)
    
def init_stars():
    global stars
    stars = [{'x': random.randint(0, WINDOW_WIDTH), 'y': random.randint(0, WINDOW_HEIGHT)} for _ in range(num_stars)]

def init_game():
    global blocks, falling_hearts, falling_arrows, power_ups
    init_stars()

    min_distance_between_blocks = 50  # Minimum distance of not overlapping

    for _ in range(20):
        block_size = random.choice(block_sizes)

        while True:
            block_x = random.randint(0, WINDOW_WIDTH - block_size)
            block_y = random.randint(WINDOW_HEIGHT // 2, WINDOW_HEIGHT - block_size)

            overlap = False
            for block in blocks:
                dist_x = abs(block['x'] - block_x)
                dist_y = abs(block['y'] - block_y)
                if dist_x < block_size + min_distance_between_blocks and dist_y < block_size + min_distance_between_blocks:
                    overlap = True
                    break  # Exit the loop if overlap

            if not overlap:
                blocks.append({'x': block_x, 'y': block_y, 'size': block_size})
                break  # move to next block

def check_collisions():
    global score, lives, game_over_lives, game_over_blocks, invincible, invincible_start

    # bullet-block collisions
    for bullet in bullets[:]:
        for block in blocks[:]:
            if (block['x'] < bullet['x'] < block['x'] + block['size'] and
                block['y'] < bullet['y'] < block['y'] + block['size']):
                bullets.remove(bullet)
                blocks.remove(block)
                score += 1 
                if not blocks:
                    game_over_blocks = True

    # spaceship-heart collisions
    for heart in falling_hearts[:]:
        if (spaceship_x < heart['x'] < spaceship_x + spaceship_width and
            spaceship_y < heart['y'] < spaceship_y + spaceship_height):
            falling_hearts.remove(heart)
            lives += 1  

    # spaceship-power-up collisions
    for power_up in power_ups[:]:
        if (spaceship_x < power_up['x'] < spaceship_x + spaceship_width and
            spaceship_y < power_up['y'] < spaceship_y + spaceship_height):
            power_ups.remove(power_up)
            apply_power_up()

    # spaceship-arrow collisions
    for arrow in falling_arrows[:]:
        if invincible:
            shield_radius = spaceship_width + 10
            shield_center_x = spaceship_x + spaceship_width // 2
            shield_center_y = spaceship_y + spaceship_height // 2
            distance = math.sqrt((arrow['x'] - shield_center_x) ** 2 + (arrow['y'] - shield_center_y) ** 2)
            if distance < shield_radius:
                falling_arrows.remove(arrow)
        else:
            if (spaceship_x < arrow['x'] < spaceship_x + spaceship_width and
                spaceship_y < arrow['y'] < spaceship_y + spaceship_height):
                falling_arrows.remove(arrow)
                lives -= 1
                if lives <= 0:
                    game_over_lives = True

    
    
def restart_game():
    global score, lives, three_way_shoot, three_way_shoot_start, game_over_lives, game_over_blocks
    score = 0
    lives = 3
    game_over_lives = False
    game_over_blocks = False
    three_way_shoot = False
    three_way_shoot_start = 0
    init_game()

def update_game_objects():
    global three_way_shoot, three_way_shoot_start, invincible, invincible_start
    
    # Update star positions
    for star in stars:
        star['y'] -= 2
        if star['y'] < 0:
            star['y'] = WINDOW_HEIGHT
            star['x'] = random.randint(0, WINDOW_WIDTH)
            
    # Update bullet positions
    for bullet in bullets:
        angle_rad = math.radians(bullet['angle'])
        bullet['x'] += math.sin(angle_rad) * bullet_speed
        bullet['y'] += math.cos(angle_rad) * bullet_speed

    # Update falling heart positions
    for heart in falling_hearts:
        heart['y'] -= difficulty_settings[difficulty]["heart_speed"]

    # Update falling arrow positions
    for arrow in falling_arrows:
        arrow['y'] -= difficulty_settings[difficulty]["arrow_speed"]

    # Update power-up positions
    for power_up in power_ups:
        power_up['y'] -= 5

    # Remove off-screen objects
    bullets[:] = [b for b in bullets if b['y'] < WINDOW_HEIGHT]
    falling_hearts[:] = [h for h in falling_hearts if h['y'] > 0]
    falling_arrows[:] = [a for a in falling_arrows if a['y'] > 0]
    power_ups[:] = [p for p in power_ups if p['y'] > 0]

    # if three-way shoot should end
    if three_way_shoot and time.time() - three_way_shoot_start > 10:
        three_way_shoot = False
        
    # if invincibility should
    if invincible and time.time() - invincible_start > 10:
        invincible = False

def spawn_falling_hearts():
    if random.random() < difficulty_settings[difficulty]["heart_spawn_rate"]:
        falling_hearts.append({
            'x': random.randint(0, WINDOW_WIDTH),
            'y': WINDOW_HEIGHT
        })

def spawn_falling_arrows():
    if random.random() < difficulty_settings[difficulty]["arrow_spawn_rate"]:
        falling_arrows.append({
            'x': random.randint(0, WINDOW_WIDTH),
            'y': WINDOW_HEIGHT
        })

def spawn_power_ups():
    if random.random() < 0.003:
        power_ups.append({
            'x': random.randint(0, WINDOW_WIDTH),
            'y': WINDOW_HEIGHT
        })

def check_game_over():
    global game_over_lives, game_over_blocks
    if lives <= 0:
        game_over_lives = True

    if not blocks:
        game_over_blocks = True

def update_score_and_lives():
    global score, lives
    GL.glColor3f(1.0, 1.0, 1.0)

    #the heart icon beside health bar
    heart_x = 10
    heart_y = WINDOW_HEIGHT - 20  
    draw_heart(heart_x, heart_y, 15)  

    # Draw the health bar segments to the right of the heart
    segment_width = 30  
    segment_height = 10  
    segment_gap = 5  
    start_x = heart_x + 13  
    start_y = heart_y  

    # Determine the number of filled segments based on remaining lives
    for i in range(lives):
        segment_x = start_x + i * (segment_width + segment_gap)

        if i < lives:
            GL.glColor3f(1.0, 0.0, 0.0)

        # Draw the segment as individual points using GL_POINTS
        for y in range(start_y - segment_height // 2, start_y + segment_height // 2):
            for x in range(segment_x, segment_x + segment_width):
                draw_pixel(x, y)

    # the score
    GL.glColor3f(1.0, 1.0, 1.0) 
    score_x = WINDOW_WIDTH - 150  
    score_y = WINDOW_HEIGHT - 25  
    GL.glRasterPos2f(score_x, score_y)
    for char in f"Score: {score}":
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    # active power-up indicator
    power_up_x = score_x - 100
    power_up_y = 15
    GL.glRasterPos2f(power_up_x, power_up_y)
    if invincible:
        power_up_text = "Power-Up: Invincible"
    elif three_way_shoot:
        power_up_text = "Power-Up: Bullet Spread"
    else:
        power_up_text = "Power-Up: None"
    
    for char in power_up_text:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


def draw_game_objects():
    
    GL.glColor3f(1.0, 1.0, 1.0)
    for star in stars:
        draw_pixel(star['x'], star['y'])
    
    # spaceship
    GL.glColor3f(0.7, 0.7, 0.7)  # Light Gray

    # body
    midpoint_line(spaceship_x + spaceship_width // 2, spaceship_y + spaceship_height, spaceship_x + spaceship_width // 2, spaceship_y)

    # Cockpit
    GL.glColor3f(1.0, 1.0, 1.0)
    midpoint_circle(spaceship_x + spaceship_width // 2, spaceship_y + 3 * spaceship_height // 4, 5)

    # Wings
    GL.glColor3f(0.7, 0.7, 0.7)
    midpoint_line(spaceship_x, spaceship_y + spaceship_height // 2, spaceship_x + spaceship_width // 4, spaceship_y)
    midpoint_line(spaceship_x + spaceship_width, spaceship_y + spaceship_height // 2, spaceship_x + 3 * spaceship_width // 4, spaceship_y)

    # wings texture
    GL.glColor3f(0.3, 0.3, 0.3)
    midpoint_line(spaceship_x, spaceship_y + spaceship_height // 2, spaceship_x + spaceship_width // 4, spaceship_y + spaceship_height // 4)
    midpoint_line(spaceship_x + spaceship_width, spaceship_y + spaceship_height // 2, spaceship_x + 3 * spaceship_width // 4, spaceship_y + spaceship_height // 4)

    # Thrusters
    GL.glColor3f(0.3, 0.3, 0.3) 
    midpoint_circle(spaceship_x + spaceship_width // 3, spaceship_y - 5, 3)
    midpoint_circle(spaceship_x + 2 * spaceship_width // 3, spaceship_y - 5, 3)

    # Flames
    GL.glColor3f(1.0, 0.0, 0.0)  
    midpoint_circle(spaceship_x + spaceship_width // 3, spaceship_y - 10, 2)
    midpoint_circle(spaceship_x + 2 * spaceship_width // 3, spaceship_y - 10, 2)
    GL.glColor3f(1.0, 0.5, 0.0)  
    midpoint_circle(spaceship_x + spaceship_width // 3, spaceship_y - 12, 1)
    midpoint_circle(spaceship_x + 2 * spaceship_width // 3, spaceship_y - 12, 1)
    GL.glColor3f(1.0, 1.0, 0.0) 
    draw_pixel(spaceship_x + spaceship_width // 3, spaceship_y - 14)
    draw_pixel(spaceship_x + 2 * spaceship_width // 3, spaceship_y - 14)
    
    if invincible:
        GL.glColor3f(0.0, 1.0, 1.0)  
        midpoint_circle(spaceship_x + spaceship_width // 2, spaceship_y + spaceship_height // 2, spaceship_width)
    
    # bullets
    GL.glColor3f(1.0, 1.0, 0.0)
    for bullet in bullets:
        midpoint_line(bullet['x'], bullet['y'], bullet['x'], bullet['y'] + 5)

    GL.glColor3f(0.8, 0.3, 0.1)
    for block in blocks:
        # Loop filling
        for y in range(block['y'], block['y'] + block['size'] + 1):
            # horizontal line
            midpoint_line(block['x'], y, block['x'] + block['size'], y)

    # falling hearts
    for heart in falling_hearts:
        draw_heart(heart['x'], heart['y'], heart_size)

    # falling arrows
    for arrow in falling_arrows:
        draw_arrow(arrow['x'], arrow['y'], arrow_size)

    # power-ups
    for power_up in power_ups:
        #outer deep pink circle
        GL.glColor3f(1.0, 0.4, 0.7)
        midpoint_circle(power_up['x'], power_up['y'], power_up_size // 2)

        #lighter pink hue
        GL.glColor3f(1.0, 0.6, 0.8)  
        midpoint_circle(power_up['x'], power_up['y'], power_up_size // 3)

        #center of the ball, a very light pink
        GL.glColor3f(1.0, 0.8, 0.9)
        midpoint_circle(power_up['x'], power_up['y'], power_up_size // 4)

        # reflective shine
        GL.glColor3f(1.0, 1.0, 1.0)  # White Highlight
        midpoint_circle(power_up['x'] - power_up_size // 8, power_up['y'] + power_up_size // 8, power_up_size // 8)
 
def apply_power_up():
    global three_way_shoot, three_way_shoot_start, invincible, invincible_start
    power_up = random.choice(["three_way_shoot", "invincible"])
    if power_up == "three_way_shoot":
        three_way_shoot = True
        three_way_shoot_start = time.time()
    elif power_up == "invincible":
        invincible = True
        invincible_start = time.time()

def shoot_bullet():
    global three_way_shoot
    if three_way_shoot:
        bullets.append({'x': spaceship_x + spaceship_width // 2, 'y': spaceship_y + spaceship_height, 'angle': 0})
        bullets.append({'x': spaceship_x + spaceship_width // 2, 'y': spaceship_y + spaceship_height, 'angle': -15})
        bullets.append({'x': spaceship_x + spaceship_width // 2, 'y': spaceship_y + spaceship_height, 'angle': 15})
    else:
        bullets.append({'x': spaceship_x + spaceship_width // 2, 'y': spaceship_y + spaceship_height, 'angle': 0})

def keyboard(key, x, y):
    global spaceship_x, game_over_lives, game_over_blocks, difficulty

    if difficulty is None:
        if key == b'1':
            difficulty = "Easy"
            init_game()
        elif key == b'2':
            difficulty = "Medium"
            init_game()
        elif key == b'3':
            difficulty = "Hard"
            init_game()
    else:
        if key == b'a' and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        elif key == b'd' and spaceship_x < WINDOW_WIDTH - spaceship_width:
            spaceship_x += spaceship_speed
        elif key == b' ':
            shoot_bullet()
        elif key == b'r' and (game_over_lives or game_over_blocks):
            restart_game()

def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    if difficulty is None:
        draw_difficulty_menu()
    elif not game_over_lives and not game_over_blocks:
        update_game_objects()
        spawn_falling_hearts()
        spawn_falling_arrows()
        spawn_power_ups()
        check_collisions()
        check_game_over()
        draw_game_objects()
        update_score_and_lives()
    else:
        draw_game_over()

    GLUT.glutSwapBuffers()

def draw_difficulty_menu():
    GL.glColor3f(1.0, 1.0, 1.0)

    menu_items = [
        "   Space Shooter Game",'',
        "Select Difficulty:",
        "1. Easy",
        "2. Medium",
        "3. Hard",
        "Press 1, 2, or 3 to start"
    ]

    for i, item in enumerate(menu_items):
        GL.glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100 - i * 30)
        for char in item:
            GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def draw_game_over():
    if game_over_lives:
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
        for char in "Game Over":
            GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    elif game_over_blocks:
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
        for char in "You Win!":
            GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
            
    GL.glColor3f(1.0, 1.0, 1.0)
    GL.glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30)
    for char in f"Final Score: {score}":
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(char))
    
    GL.glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 60)
    for char in "Press 'R' to restart":
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(char))

def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutCreateWindow(b"Space Shoot Game")
    GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, -1.0, 1.0)

    GLUT.glutDisplayFunc(display)
    GLUT.glutKeyboardFunc(keyboard)
    GLUT.glutIdleFunc(display)
    GLUT.glutMainLoop()

if __name__ == "__main__":
    main()

