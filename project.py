from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint
from math import sin, cos, sqrt, radians
from math import degrees, atan2
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18, GLUT_BITMAP_HELVETICA_12
import time


camra_angl = 0         
camra_radius = 700     
camra_height = 500      

plyr_pos = [0, 0, 0]
plyr_angl = 0
plyr_life = 5
plyr_ammo = 20  # New: player ammo count

len_grid = 600

camera_pos = [0, 300, 400]

fovY = 110

score = 0

missed_bullets = 0
game_over = False
game_paused = False  # New: flag for game pause state

auto_follow = False
cheating_on = False
cheating_speed = 0.25    
cheat_threashold = 4    

frst_prsn = False

cheating_vision = False

# Button dimensions and positions
button_width = 100
button_height = 30
pause_button = {"x": 850, "y": 750, "width": button_width, "height": button_height, "text": "PAUSE"}
resume_button = {"x": 850, "y": 700, "width": button_width, "height": button_height, "text": "RESUME"}
reset_button = {"x": 850, "y": 650, "width": button_width, "height": button_height, "text": "RESET"}


bullets = []
enemies = []
count_enemy = 8  # Changed from 5 to 8 total enemies

# New: Ammo and health pickups
ammo_pickup = {
    "pos": [200, 200, 0],
    "active": True,
    "last_pickup_time": 0,
    "cooldown": 10  # seconds
}

health_pickup = {
    "pos": [-200, -200, 0],
    "active": True,
    "last_pickup_time": 0,
    "cooldown": 15  # seconds
}

# Enemy types: 0=sphere, 1=cube, 2=cone, 3=torus
def start_game():
    global enemies
    
    enemies = []
    
    # Add 2 sphere-type enemies (original type)
    for i in range(2):
        enemies.append({
            "pos": [randint(-len_grid//2, len_grid//2),
                    randint(-len_grid//2, len_grid//2),
                    0],
            "size": 25,
            "growing": True,
            "shot": False,
            "type": 0  # Sphere enemy
        })
    
    # Add 2 cube-type enemies
    for i in range(2):
        enemies.append({
            "pos": [randint(-len_grid//2, len_grid//2),
                    randint(-len_grid//2, len_grid//2),
                    0],
            "size": 20,
            "growing": True,
            "shot": False,
            "type": 1  # Cube enemy
        })
    
    # Add 2 cone-type enemies
    for i in range(2):
        enemies.append({
            "pos": [randint(-len_grid//2, len_grid//2),
                    randint(-len_grid//2, len_grid//2),
                    0],
            "size": 22,
            "growing": True,
            "shot": False,
            "type": 2  # Cone enemy
        })
    
    # Add 2 torus-type enemies
    for i in range(2):
        enemies.append({
            "pos": [randint(-len_grid//2, len_grid//2),
                    randint(-len_grid//2, len_grid//2),
                    0],
            "size": 18,
            "growing": True,
            "shot": False,
            "type": 3  # Torus enemy
        })


def game_reset():
    global plyr_pos, plyr_angl, plyr_life, missed_bullets, game_over, score, bullets, plyr_ammo, game_paused
    
    plyr_pos = [0, 0, 0]
    plyr_angl = 0
    plyr_life = 5
    plyr_ammo = 20  # Reset ammo
    
    game_over = False
    game_paused = False  # Make sure game is not paused after reset
    missed_bullets = 0
    
    bullets = []
    score = 0
    
    # Reset pickups
    ammo_pickup["active"] = True
    health_pickup["active"] = True
    ammo_pickup["last_pickup_time"] = 0
    health_pickup["last_pickup_time"] = 0

    start_game()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    if text == "GAME OVER! Press R to restart":
        glColor3f(1.0, 0.0, 0.0)
    elif text == "PAUSED":
        glColor3f(1.0, 0.5, 0.0)  # Orange for pause message
    else:
        glColor3f(1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)            

    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
# Draw button with text
def draw_button(button):
    # Set up for 2D drawing
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw button background
    glColor3f(0.2, 0.2, 0.2)  # Dark gray background
    glBegin(GL_QUADS)
    glVertex2f(button["x"], button["y"])
    glVertex2f(button["x"] + button["width"], button["y"])
    glVertex2f(button["x"] + button["width"], button["y"] + button["height"])
    glVertex2f(button["x"], button["y"] + button["height"])
    glEnd()
    
    # Draw button border
    glColor3f(0.5, 0.5, 0.5)  # Light gray border
    glBegin(GL_LINE_LOOP)
    glVertex2f(button["x"], button["y"])
    glVertex2f(button["x"] + button["width"], button["y"])
    glVertex2f(button["x"] + button["width"], button["y"] + button["height"])
    glVertex2f(button["x"], button["y"] + button["height"])
    glEnd()
    
    # Draw button text
    glColor3f(1.0, 1.0, 1.0)  # White text
    text_x = button["x"] + (button["width"] - len(button["text"]) * 40) / 2
    text_y = button["y"] + (button["height"] - 12) / 2
    glRasterPos2f(text_x, text_y + button["height"]/2)
    
    for ch in button["text"]:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    

def grid_floor():
    glBegin(GL_QUADS)

    for i in range(-len_grid, len_grid, 100):         
        for j in range(-len_grid, len_grid, 100):     
            # Alternating colors for checkerboard pattern
            if (i//100 + j//100) % 2 == 0:                  
                glColor3f(0.7, 0.5, 0.95)  # Purple                
            else:
                glColor3f(0.5, 0.7, 0.9)  # Changed to blue                                          
            glVertex3f(i, j, 0)
            glVertex3f(i+100, j, 0)
            glVertex3f(i+100, j+100, 0)
            glVertex3f(i, j+100, 0)
    glEnd()


def walls():
    glBegin(GL_QUADS)
    # North wall - white
    glColor3f(1, 1, 1)                      
    glVertex3f(-len_grid, +len_grid, 0)
    glVertex3f(-len_grid, +len_grid, 70)
    glVertex3f(+len_grid, +len_grid, 70)     
    glVertex3f(+len_grid, +len_grid, 0)     
    glEnd()
    
    glBegin(GL_QUADS)
    # South wall - white
    glColor3f(1, 1, 1)
    glVertex3f(+len_grid, -len_grid, 0) 
    glVertex3f(+len_grid, -len_grid, 70) 
    glVertex3f(-len_grid, -len_grid, 70)    
    glVertex3f(-len_grid, -len_grid, 0)
    glEnd()

    glBegin(GL_QUADS)
    # West wall - gold
    glColor3f(1.0, 0.84, 0.0)          
    glVertex3f(-len_grid, -len_grid, 0)
    glVertex3f(-len_grid, -len_grid, 70)
    glVertex3f(-len_grid, +len_grid, 70)       
    glVertex3f(-len_grid, +len_grid, 0)
    glEnd()
    
    glBegin(GL_QUADS)
    # East wall - gold
    glColor3f(1.0, 0.84, 0.0)                  
    glVertex3f(+len_grid, +len_grid, 0)
    glVertex3f(+len_grid, +len_grid, 70)
    glVertex3f(+len_grid, -len_grid, 70)
    glVertex3f(+len_grid, -len_grid, 0)
    glEnd()


def player_drawing():
    glPushMatrix()

    glTranslatef(plyr_pos[0], plyr_pos[1], plyr_pos[2])   
    glRotatef(plyr_angl, 0, 0, 1)                            

    # Body
    glColor3f(0.3, 0.5, 0.2)          
    glPushMatrix()
    glScalef(20, 10, 30)                                    
    glutSolidCube(1)         
    glPopMatrix()

    # Head
    glColor3f(0, 0, 0)            
    glPushMatrix()
    glTranslatef(0, 0, 30 + 10)    
    glutSolidSphere(10, 16, 16)  
    glPopMatrix()

    # Arms
    glColor3f(0, 0, 0)  

    for hand_x in (-15, +15):            
        glPushMatrix()
        glTranslatef(hand_x, 0, 10)  
        glRotatef(90, 0, 1, 0)         
        gluCylinder(gluNewQuadric(), 3, 3, 10, 12, 4)    
       
        if hand_x > 0:
            glTranslatef(0, 0, 10)        
            glColor3f(0.3, 0.3, 0.9)      
            gluCylinder(gluNewQuadric(), 2, 2, 30, 12, 4)
        glPopMatrix()

    if game_over:  
        glColor3f(0.3, 0.3, 0.9)
        for leg_x in (-8, +8):
            glPushMatrix()
            glTranslatef(leg_x, 0, 0)  
            glRotatef(90, 1, 0, 0)        
            gluCylinder(gluNewQuadric(), 4, 4, 30, 12, 4)
            glPopMatrix()          

    glPopMatrix()


def bullet_drawing():
    glColor3f(1.0, 0.5, 0.0)
    
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet["pos"][0], bullet["pos"][1], bullet["pos"][2])
        glutSolidCube(6)
        glPopMatrix()


def enemy_drawing():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy["pos"][0], enemy["pos"][1], enemy["pos"][2])
        
        # Different enemy types have different colors and shapes
        if enemy["type"] == 0:  # Sphere enemy (original)
            glColor3f(1, 0, 0)  # Red
            glutSolidSphere(enemy["size"], 10, 10)
            
            # Eyes
            glColor3f(0, 0, 0)
            glTranslatef(0, 0, enemy["size"] + 5)
            glutSolidSphere(enemy["size"]/2, 10, 10)
            
        elif enemy["type"] == 1:  # Cube enemy
            glColor3f(0, 0, 1)  # Blue
            glutSolidCube(enemy["size"] * 1.5)
            
            # Cube eyes
            glColor3f(1, 1, 0)  # Yellow eyes
            glTranslatef(-enemy["size"]/2, -enemy["size"]/2, enemy["size"])
            glutSolidCube(enemy["size"]/3)
            glTranslatef(enemy["size"], 0, 0)
            glutSolidCube(enemy["size"]/3)
            
        elif enemy["type"] == 2:  # Cone enemy
            glColor3f(0, 1, 0)  # Green
            glRotatef(-90, 1, 0, 0)  # Rotate to point upward
            glutSolidCone(enemy["size"]/1.5, enemy["size"]*2, 12, 12)
            
            # Cone eyes
            glColor3f(1, 0, 1)  # Purple eyes
            glRotatef(90, 1, 0, 0)  # Rotate back
            glTranslatef(-enemy["size"]/4, enemy["size"]/2, enemy["size"]/2)
            glutSolidSphere(enemy["size"]/5, 8, 8)
            glTranslatef(enemy["size"]/2, 0, 0)
            glutSolidSphere(enemy["size"]/5, 8, 8)
            
        elif enemy["type"] == 3:  # Torus enemy
            glColor3f(1, 0.5, 0)  # Orange
            glutSolidTorus(enemy["size"]/3, enemy["size"], 12, 12)
            
            # Torus center
            glColor3f(0, 0.5, 0.5)  # Teal center
            glutSolidSphere(enemy["size"]/2, 8, 8)
        
        glPopMatrix()


# New: Draw ammo and health pickups
def draw_pickups():
    # Draw ammo pickup
    if ammo_pickup["active"]:
        glPushMatrix()
        glTranslatef(ammo_pickup["pos"][0], ammo_pickup["pos"][1], ammo_pickup["pos"][2])
        
        # Draw ammo box
        glColor3f(1.0, 1.0, 0.0)  # Yellow
        glutSolidCube(15)
        
        # Draw ammo symbol
        glColor3f(0, 0, 0)
        glTranslatef(0, 0, 15)
        glutSolidCube(5)
        glTranslatef(0, 0, 5)
        glutSolidCube(5)
        
        glPopMatrix()
    
    # Draw health pickup
    if health_pickup["active"]:
        glPushMatrix()
        glTranslatef(health_pickup["pos"][0], health_pickup["pos"][1], health_pickup["pos"][2])
        
        # Draw health box
        glColor3f(0.0, 1.0, 0.0)  # Green
        glutSolidCube(15)
        
        # Draw plus symbol for health
        glColor3f(1, 1, 1)  # White plus
        glPushMatrix()
        glTranslatef(0, 0, 15)
        glScalef(10, 3, 3)
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0, 15)
        glScalef(3, 10, 3)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()


def keyboardListener(key, x, y):
    global plyr_pos, plyr_angl, cheating_on, cheating_vision, game_over, auto_follow, game_paused

    if game_over and key == b'r':
        game_reset()
        return
        
    # Allow p key to toggle pause
    if key == b'p':
        game_paused = not game_paused
        return

    if key == b'c':
        cheating_on = not cheating_on

    if key == b'v' and cheating_on:
        if cheating_on and frst_prsn:
            auto_follow = not auto_follow
       
    # Only process movement if game is not paused and not over
    if not game_paused and not game_over:
        speed = 3
        
        if key == b'w':
                plyr_pos[0] += speed * cos(radians(plyr_angl))
                plyr_pos[1] += speed * sin(radians(plyr_angl))
                

        if key == b's':
            
                plyr_pos[0] -= speed * cos(radians(plyr_angl))
                plyr_pos[1] -= speed * sin(radians(plyr_angl))
              
        plyr_pos[0] = max(-550, min(plyr_pos[0], 550))
        plyr_pos[1] = max(-550, min(plyr_pos[1], 550))

        if key == b'a':
            plyr_angl += 5
        if key == b'd':
            plyr_angl -= 5


def specialKeyListener(key, x, y):
    global camra_angl, camra_radius

    if key == GLUT_KEY_LEFT:
        camra_angl += 2
    elif key == GLUT_KEY_RIGHT:
        camra_angl -= 2
    elif key == GLUT_KEY_UP:
        camra_radius = max(-600, camra_radius - 10)  # Zoom in
    elif key == GLUT_KEY_DOWN:
        camra_radius = max(+600, camra_radius + 10) # Zoom out


def mouseListener(button, state, x, y):
    global frst_prsn, bullets, plyr_ammo, game_paused, game_over

    # UI buttons handling
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert window coordinates to match our orthographic projection
        # GLUT has y=0 at the top, our UI coordinate system has y=0 at the bottom
        y = 800 - y
        
        # Check if clicked on pause button
        if (pause_button["x"] <= x <= pause_button["x"] + pause_button["width"] and
            pause_button["y"] <= y <= pause_button["y"] + pause_button["height"]):
            game_paused = True
            return
            
        # Check if clicked on resume button
        if (resume_button["x"] <= x <= resume_button["x"] + resume_button["width"] and
            resume_button["y"] <= y <= resume_button["y"] + resume_button["height"]):
            game_paused = False
            return
            
        # Check if clicked on reset button
        if (reset_button["x"] <= x <= reset_button["x"] + reset_button["width"] and
            reset_button["y"] <= y <= reset_button["y"] + reset_button["height"]):
            game_reset()
            game_paused = False
            return
        
        # Regular shooting functionality - only if not paused and not game over
        if not game_paused and not game_over:
            # Check if player has ammo
            if plyr_ammo > 0:
                bullet_speed = 4
                
                bullet_pos = [plyr_pos[0], plyr_pos[1], plyr_pos[2]+10]
                
                bullet_dir = [                       
                    cos(radians(plyr_angl)),
                    sin(radians(plyr_angl)),
                    0
                ]
                
                bullets.append({
                    "pos": bullet_pos,
                    "dir": bullet_dir,
                    "speed": bullet_speed
                })
                
                # Decrease ammo
                plyr_ammo -= 1

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_paused and not game_over:
        frst_prsn = not frst_prsn


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    global frst_prsn, bullets, plyr_ammo
    if frst_prsn:
        gluLookAt(
            plyr_pos[0], plyr_pos[1], plyr_pos[2] + 30,
            plyr_pos[0] + 0.05,                              
            plyr_pos[1] + 0.05,        
            plyr_pos[2] + 30,
            0, 0, 1
        )
        
        if auto_follow:                                                
            cam_x = plyr_pos[0] - cos(radians(plyr_angl))
            cam_y = plyr_pos[1] - sin(radians(plyr_angl))
            cam_z = plyr_pos[2] + 90

            look_x = plyr_pos[0] + 2 * cos(radians(plyr_angl))
            look_y = plyr_pos[1] + 2 * sin(radians(plyr_angl))
            look_z = plyr_pos[2] + 30

            gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)
    else:
        cam_x = camra_radius * cos(radians(camra_angl))
        cam_y = camra_radius * sin(radians(camra_angl))
        cam_z = camra_height  

        gluLookAt(
            cam_x, cam_y, cam_z,  
            0, 0, 0,              
            0, 0, 1               
        )


def check_pickup_collisions():
    global plyr_ammo, plyr_life, ammo_pickup, health_pickup
    
    current_time = time.time()
    
    # Check ammo pickup collision
    if ammo_pickup["active"]:
        dx = plyr_pos[0] - ammo_pickup["pos"][0]
        dy = plyr_pos[1] - ammo_pickup["pos"][1]
        dist = sqrt(dx*dx + dy*dy)
        
        if dist < 30:  # Player is close enough to pickup
            plyr_ammo += 30  # Add 30 ammo
            ammo_pickup["active"] = False
            ammo_pickup["last_pickup_time"] = current_time
    
    # Check health pickup collision
    if health_pickup["active"]:
        dx = plyr_pos[0] - health_pickup["pos"][0]
        dy = plyr_pos[1] - health_pickup["pos"][1]
        dist = sqrt(dx*dx + dy*dy)
        
        if dist < 30:  # Player is close enough to pickup
            plyr_life += 2  # Add 2 health
            health_pickup["active"] = False
            health_pickup["last_pickup_time"] = current_time
    
    # Check if pickups should be reactivated
    if not ammo_pickup["active"] and current_time - ammo_pickup["last_pickup_time"] > ammo_pickup["cooldown"]:
        ammo_pickup["active"] = True
        # Randomize new position
        ammo_pickup["pos"] = [randint(-len_grid//2 + 100, len_grid//2 - 100), 
                              randint(-len_grid//2 + 100, len_grid//2 - 100), 
                              0]
    
    if not health_pickup["active"] and current_time - health_pickup["last_pickup_time"] > health_pickup["cooldown"]:
        health_pickup["active"] = True
        # Randomize new position
        health_pickup["pos"] = [randint(-len_grid//2 + 100, len_grid//2 - 100), 
                                randint(-len_grid//2 + 100, len_grid//2 - 100), 
                                0]


def collision_finding():
    global bullets, enemies, plyr_life, missed_bullets, game_over, score

    # Bullet-enemy collision
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dx = bullet["pos"][0] - enemy["pos"][0]
            dy = bullet["pos"][1] - enemy["pos"][1]
            dz = bullet["pos"][2] - enemy["pos"][2]
            dist = sqrt(dx*dx + dy*dy + dz*dz)
            
            if dist < enemy["size"] + 10:  
                bullets.remove(bullet)
                enemies.remove(enemy)

                # Create a new enemy of the same type to replace the one that was destroyed
                enemy_type = enemy["type"]
                enemies.append({
                    "pos": [randint(-len_grid//2, len_grid//2), 
                            randint(-len_grid//2, len_grid//2), 
                            0],
                    "size": 15 + randint(5, 10),  # Vary size
                    "growing": True,
                    "shot": False,
                    "type": enemy_type
                })

                score += 10
                break

    # Check for missed bullets
    for bullet in bullets[:]:
        if (abs(bullet["pos"][0]) > len_grid or 
            abs(bullet["pos"][1]) > len_grid):
            bullets.remove(bullet)
            missed_bullets += 1

    # Check for player-enemy collision
    for enemy in enemies:
        dx = plyr_pos[0] - enemy["pos"][0]
        dy = plyr_pos[1] - enemy["pos"][1]
        dist = sqrt(dx*dx + dy*dy)

        if dist < enemy["size"] + 20 and not game_over:
            plyr_life -= 1
            enemy["pos"][0] = randint(-len_grid//2, len_grid//2)
            enemy["pos"][1] = randint(-len_grid//2, len_grid//2)

            if plyr_life <= 0:
                game_over = True

    # Check for game over from too many missed shots
    if missed_bullets >= 30 and not game_over:
        game_over = True


def updating_enemies():
    for enemy in enemies:
        # Move towards player
        dx = plyr_pos[0] - enemy["pos"][0]
        dy = plyr_pos[1] - enemy["pos"][1]
        dist = sqrt(dx*dx + dy*dy)

        if dist > 0:
            # Different enemy types move at different speeds
            speed_factor = 0.05
            if enemy["type"] == 1:  # Cube moves slower
                speed_factor = 0.03
            elif enemy["type"] == 2:  # Cone moves faster
                speed_factor = 0.06
            elif enemy["type"] == 3:  # Torus moves at medium speed
                speed_factor = 0.04
                
            enemy["pos"][0] += dx / dist * speed_factor
            enemy["pos"][1] += dy / dist * speed_factor

        # Pulsate size
        if enemy["growing"]:
            enemy["size"] += 0.1
            if enemy["size"] > 30:
                enemy["growing"] = False
        else:
            enemy["size"] -= 0.1
            
            if enemy["size"] < 15:
                enemy["growing"] = True


def updating_bullets():
    for bullet in bullets:
        bullet["pos"][0] += bullet["dir"][0] * bullet["speed"]
        bullet["pos"][1] += bullet["dir"][1] * bullet["speed"]
        bullet["pos"][2] += bullet["dir"][2] * bullet["speed"]  


def idle():                                      
    global plyr_angl, bullets, plyr_ammo

    # Only update game state if not paused and not game over
    if not game_paused and not game_over:
        if cheating_on:
            plyr_angl = (plyr_angl + cheating_speed) % 360

            for enemy in enemies:
                if enemy["shot"]:                        
                    continue

                dx = enemy["pos"][0] - plyr_pos[0]
                dy = enemy["pos"][1] - plyr_pos[1]
                dz = enemy["pos"][2] - (plyr_pos[2] + 20)

                angle_to_enemy = degrees(atan2(dy, dx)) % 360             
                diff = (angle_to_enemy - plyr_angl) % 360 

                if abs(diff) <= cheat_threashold and plyr_ammo > 0:
                    bullet_speed = 4
                    bullet_pos = [plyr_pos[0], plyr_pos[1], plyr_pos[2] + 20]
                    dist = sqrt(dx*dx + dy*dy + dz*dz)
                    
                    bullet_dir = [dx/dist, dy/dist, dz/dist]          

                    bullets.append({
                        "pos": bullet_pos,
                        "dir": bullet_dir,
                        "speed": bullet_speed
                    })
                    
                    plyr_ammo -= 1  # Use ammo even in cheat mode
                    enemy["shot"] = True                                   
                    break

        updating_enemies()
        updating_bullets()
        collision_finding()
        check_pickup_collisions()  # Check for pickups

    # Always redisplay to ensure UI updates even when paused
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    grid_floor()
    walls()  
    player_drawing()

    enemy_drawing()
    bullet_drawing()
    draw_pickups()  # Draw the pickups

    # HUD Information
    draw_text(10, 770, f"Score: {score}")
    draw_text(10, 740, f"Remaining Lives: {plyr_life}")
    draw_text(10, 710, f"Missed: {missed_bullets}/30")
    draw_text(10, 680, f"Ammo: {plyr_ammo}")  # Display ammo count

    # Display cooldown timers for pickups
    current_time = time.time()
    if not ammo_pickup["active"]:
        time_left = int(ammo_pickup["cooldown"] - (current_time - ammo_pickup["last_pickup_time"]))
        draw_text(10, 650, f"Ammo Pickup: {time_left}s")
    
    if not health_pickup["active"]:
        time_left = int(health_pickup["cooldown"] - (current_time - health_pickup["last_pickup_time"]))
        draw_text(10, 620, f"Health Pickup: {time_left}s")

    # Draw UI buttons
    draw_button(pause_button)
    draw_button(resume_button)
    draw_button(reset_button)

    # Game status messages
    if game_over:
        draw_text(350, 400, "GAME OVER! Press R to restart", GLUT_BITMAP_HELVETICA_18)
    
    if game_paused:
        draw_text(450, 400, "PAUSED", GLUT_BITMAP_HELVETICA_18)
    
    if cheating_on:
        draw_text(10, 590, "CHEAT MODE IS ON", GLUT_BITMAP_HELVETICA_12)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)

    glutCreateWindow(b"3D Game with Multiple Enemy Types")
    
    # Enable depth testing for 3D rendering
    glEnable(GL_DEPTH_TEST)
    
    # Setup initial game state
    start_game()

    # Register GLUT callbacks
    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    # Instructions
    print("Game Controls:")
    print("  W,A,S,D - Move player")
    print("  Left Mouse - Shoot")
    print("  Right Mouse - Toggle first/third person view")
    print("  P - Toggle pause")
    print("  UI Buttons: PAUSE, RESUME, RESET")
    print("  R - Restart after game over")

    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()