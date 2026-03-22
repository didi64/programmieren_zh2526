import threading
from ipywidgets import Output, Image
from ipycanvas import Canvas, hold_canvas
from IPython.display import display
import random

random.seed()

score = 0
highscore = 0
counter = 0
game_over_pos_y = 400
game_state = 'init_screen'
total_enemies_alive = 50

cur_anim_frame = 0
emenies_move_dir = 1
enemies_move_offset_x = 0
enemies_move_offset_y = 50

enemies_attack_chance = 50   # spawn laser every n farmes
enemies_attack_chance_default = 50
enemies_attack_chance_step = 10
enemies_laser_speed = 5 # move laser every n frames
enemies_laser_speed_default = 5
enemies_laser_speed_step = 1
enemies_start_speed = 10
enemies_start_speed_default = 10
enemies_start_speed_step = 1
enemies_draw_hitbox = False
enemies_width = 400
enemies_move_padding = 0
enemies_num_x = 10
game_scale = 3
enemies_first_row_hight = 50
enemies_row_spacing = 40
enemies_num_y = 5
enemie_type_per_row = ('squid', 'cuttlefish', 'squid', 'crab', 'octopus')
enemie_width = {
    "squid": 8,
    "cuttlefish": 8,
    "crab": 11,
    "octopus": 12
}
enemie_points = {
    "squid": 30,
    "cuttlefish": 30,
    "crab": 20,
    "octopus": 10
}


layout = {'border': '1px solid green',}
canvas = Canvas(width=500, height=500, layout=layout)
canvas.fill_style = "black"
canvas.fill_rect(0, 0, canvas.width, canvas.height)
canvas.image_smoothing_enabled = False

out = Output()


@out.capture()
def on_keyboard_event(key, *flags):
    ''' interrupt handler for keyboard inputs '''
    global game_state
    if game_state == 'playing':
        if key == 'a' and (player.pos_x - 1*game_scale - (player.hitbox_x*game_scale)/2) > 0:
            player.pos_x -= 1*game_scale
        elif key == 'd' and (player.pos_x + 1*game_scale + (player.hitbox_x*game_scale)/2) < 500:
            player.pos_x += 1*game_scale
        elif key == 'w' and laser[0].alive == False:
            laser[0].speed_y = 6
            laser[0].speed_x = 0
            laser[0].pos_x = player.pos_x + laser[0].speed_x * game_scale
            laser[0].pos_y = player.pos_y + laser[0].speed_y * game_scale
            laser[0].alive = True
    elif game_state == 'game_over':
        if key == ' ':
            game_state = 'init_screen'
            draw_init_screen()
            out.clear_output()
            event_loop()

    elif game_state == 'init_screen':
        if key == ' ':
            reset_game()
            game_state = 'playing'
            event_loop()


class Player:
    def __init__(self):
        self.pos_x = 250
        self.pos_y = 420
        self.hitbox_x = 11
        self.hitbox_y = 8
        self.hit = 0
        self.retrys = 3


player = Player()


class Enemy:
    def __init__(self):
        self.type = 'crab'
        self.points = 10
        self.alive = True
        self.pos_x = 0
        self.pos_y = 0
        self.hitbox_x = 11
        self.hitbox_y = 8
        self.lowest = False


enemie = []
for y in range(enemies_num_y):
    row = []
    for x in range(enemies_num_x):
        row.append(Enemy())
    enemie.append(row)


def int_enemie():
    ''' initializes every enemie '''
    for y in range(enemies_num_y):
        for x in range(enemies_num_x):
            enemie[y][x].type = enemie_type_per_row[y]
            enemie[y][x].hitbox_x = enemie_width[enemie[y][x].type]
            enemie[y][x].pos_x = (canvas.width-enemies_width)/2 + (enemies_width/(enemies_num_x-1))*x - (enemie[y][x].hitbox_x*game_scale)/2
            enemie[y][x].pos_y = enemies_first_row_hight + y*enemies_row_spacing
            enemie[y][x].points = enemie_points[enemie[y][x].type]
            enemie[y][x].alive = True


int_enemie()


class Laser:
    def __init__(self):
        self.type = 'player'
        self.alive = False
        self.pos_x = 250
        self.pos_y = 400
        self.speed_x = 0
        self.speed_y = 0
        self.length = 10
        self.hitbox_length = 3
        self.width = 3


class Enemie_Laser:
    def __init__(self):
        self.type = 'enemie'
        self.alive = True
        self.pos_x = 250
        self.pos_y = 400
        self.speed_x = 0
        self.speed_y = 0
        self.length = 10
        self.hitbox_length = 3
        self.width = 3


laser = []
# for x in range(5):
laser.append(Laser())



class Barrier:
    def __init__(self):
        self.pos_x = 250
        self.pos_y = 400
        self.width = 50
        self.thiccc = 10


barrier = []
for x in range(4):
    barrier.append(Barrier())
    barrier[x].pos_x = 500/5 * (x + 1)



# Import Images
ufo = Image.from_file("Images/ufo.png")
cannon = Image.from_file("Images/cannon.png")
cannon_hit = Image.from_file("Images/cannon_hit.png")
anim_frame_1 = {
    "squid": Image.from_file("Images/squid_1.png"),
    "cuttlefish": Image.from_file("Images/cuttlefish_1.png"),
    "crab": Image.from_file("Images/crab_1.png"),
    "octopus": Image.from_file("Images/octopus_1.png")
}
anim_frame_2 = {
    "squid": Image.from_file("Images/squid_2.png"),
    "cuttlefish": Image.from_file("Images/cuttlefish_2.png"),
    "crab": Image.from_file("Images/crab_2.png"),
    "octopus": Image.from_file("Images/octopus_2.png")
}
anim_frame = []
anim_frame.append(anim_frame_1)
anim_frame.append(anim_frame_2)

# enemie[0][0].alive = False
# enemie[3][5].alive = False
# enemie[4][9].alive = False


# -------------------------------- Helper --------------------------------


def get_max_anim_range_left():
    ''' calculates how many pixels the enemies chan shift to the left '''
    largest_enemie_left = 0
    dead_col_left = 0

    for x in range(enemies_num_x):
        for y in range(enemies_num_y):
            if enemie[y][x].alive == True:
                largest_enemie_left = enemie[y][x].hitbox_x
        if largest_enemie_left == 0:
            dead_col_left += 1
        else:
            break

    return (canvas.width-enemies_width)/2 - (largest_enemie_left*game_scale)/2 + (enemies_width/(enemies_num_x-1))*dead_col_left - enemies_move_padding


def get_max_anim_range_right():
    ''' calculates how many pixels the enemies chan shift to the right '''
    largest_enemie_right = 0
    dead_col_right = 0

    for x in reversed(range(enemies_num_x)):
        for y in range(enemies_num_y):
            if enemie[y][x].alive == True:
                largest_enemie_right = enemie[y][x].hitbox_x
        if largest_enemie_right == 0:
            dead_col_right += 1
        else:
            break

    return (canvas.width-enemies_width)/2 - (largest_enemie_right*game_scale)/2 + (enemies_width/(enemies_num_x-1))*dead_col_right - enemies_move_padding


def dir(input):
    ''' checks if input ist negative or positive, used for laser direction '''
    if input < 0:
        return -1
    elif input > 0:
        return 1
    else:
        return 0


def larger(input_1, input_2):
    ''' returns the larger absolute number '''
    if abs(input_1) > abs(input_2):
        return abs(input_1)
    else:
        return abs(input_2)


# -------------------------------- Draw Screen --------------------------------


def clear_screen():
    ''' clears the schreen '''
    canvas.fill_style = "black"
    canvas.fill_rect(0, 0, canvas.width, canvas.height)


def draw_init_screen():
    ''' draws the initial screen '''
    clear_screen()
    canvas.fill_style = "white"
    canvas.font = "70px serif"
    canvas.text_align = "center"
    canvas.fill_text("Space Invaders", 250, 125)

    canvas.font = "20px serif"
    canvas.fill_text(f"HIGHSCORE: {highscore}", 125, 200)
    canvas.fill_text(f"SCORE: {score}", (500-125), 200)

    canvas.fill_style = "green"
    canvas.text_align = "center"
    canvas.font = "25px serif"
    canvas.fill_text("Press \'SPACE\' to play",250, 450)


def draw_game():
    ''' draws the game infos (score, revives... ) '''
    clear_screen()
    canvas.fill_style = "white"
    canvas.text_align = "center"
    canvas.font = "20px serif"
    canvas.fill_text(f"HIGHSCORE: {highscore}", 125, 25)
    canvas.fill_text(f"SCORE: {score}", (500-125), 25)

    canvas.stroke_style = "green"
    canvas.line_width = 5
    canvas.stroke_line(0, 450, 500, 450)

    canvas.draw_image(cannon, 50, 460, 13*3, 8*3)
    if player.retrys > 1:
        canvas.draw_image(cannon, 50+(13*3)+10, 460, 13*3, 8*3)
    canvas.text_align = "left"
    canvas.font = "20px serif"
    canvas.fill_text(f"{player.retrys}x", 15, 480)


def draw_enemies():
    ''' draws the enemies '''
    global total_enemies_alive
    total_enemies_alive = 0
    for y in range(enemies_num_y):
        for x in range(enemies_num_x):
            this_enemie = enemie[y][x]
            if this_enemie.alive:
                total_enemies_alive += 1
                canvas.draw_image(anim_frame[cur_anim_frame][this_enemie.type],
                                  this_enemie.pos_x + enemies_move_offset_x,
                                  this_enemie.pos_y + enemies_move_offset_y,
                                  this_enemie.hitbox_x*game_scale,
                                  this_enemie.hitbox_y*game_scale)
                global enemies_draw_hitbox
                if enemies_draw_hitbox == True:
                    canvas.stroke_style = "red"
                    canvas.line_width = 1
                    canvas.stroke_rect(this_enemie.pos_x + enemies_move_offset_x,
                                       this_enemie.pos_y + enemies_move_offset_y,
                                       this_enemie.hitbox_x*game_scale,
                                       this_enemie.hitbox_y*game_scale)


def draw_player():
    ''' draws the player (cannon) '''
    if player.hit == 0:
        canvas.draw_image(cannon, player.pos_x-(player.hitbox_x*game_scale)/2, player.pos_y, player.hitbox_x*game_scale, player.hitbox_y*game_scale)
    else:
        canvas.draw_image(cannon_hit, player.pos_x-(player.hitbox_x*game_scale)/2, player.pos_y, player.hitbox_x*game_scale, player.hitbox_y*game_scale)
        player.hit -= 1


def draw_lasers():
    ''' draws the laserbeams '''
    for x in range(len(laser)):
        if laser[x].alive == True:
            laser_dir_factor_x = laser[x].speed_x/(laser[x].speed_x + laser[x].speed_y)
            laser_dir_factor_y = laser[x].speed_y/(laser[x].speed_x + laser[x].speed_y)
            canvas.stroke_style = "blue"
            canvas.line_width = laser[x].width
            canvas.stroke_line(laser[x].pos_x, laser[x].pos_y, laser[x].pos_x+laser_dir_factor_x*laser[x].length, laser[x].pos_y+laser_dir_factor_y*laser[x].length)


def draw_barriers():
    ''' draws the barriers '''
    for x in range(len(barrier)):
        if barrier[x].thiccc >= 2:
            canvas.stroke_style = "green"
            canvas.line_width = barrier[x].thiccc
            canvas.stroke_line(barrier[x].pos_x - barrier[x].width/2, barrier[x].pos_y, barrier[x].pos_x + barrier[x].width/2, barrier[x].pos_y)


def draw_game_over_screen():
    ''' draws the GAME OVER screen '''
    canvas.fill_style = "red"
    canvas.fill_rect(0, 100, canvas.width, 70)
    canvas.fill_rect(0, 425, canvas.width, 35)

    canvas.fill_style = "black"
    canvas.text_align = "center"
    canvas.font = "50px serif"
    canvas.fill_text("GAME OVER", 250, 150)

    canvas.fill_style = "black"
    canvas.text_align = "center"
    canvas.font = "25px serif"
    canvas.fill_text("Press \'SPACE\' to reset",250, 450)


# -------------------------------- Move / Modify --------------------------------


def move_lasers():
    ''' moves the laser positions and checks for hits '''
    for l in range(len(laser)):
        if (laser[l].alive == True and l == 0) or (laser[l].alive == True and counter % enemies_laser_speed == 0):
            for a in range(larger(laser[l].speed_x, laser[l].speed_y)):
                laser[l].pos_x -= dir(laser[l].speed_x)*game_scale
                laser[l].pos_y -= dir(laser[l].speed_y)*game_scale
                # print(f"larger number is:{larger(laser[l].speed_x, laser[l].speed_y)}")

                # check laser out of game area
                if laser[l].pos_y < 0 or laser[l].pos_y > 500 or laser[l].pos_x < 0 or laser[l].pos_x > 500:
                    laser[l].alive = False
                    print(f"killed laser_nr_{l}")

                # check laser hit barrier
                for x in range(len(barrier)):
                        # canvas.stroke_style = "yellow"
                        # canvas.line_width = 1
                        # canvas.stroke_line(barrier[x].pos_x + barrier[x].width/2, barrier[x].pos_y + barrier[x].thiccc/2, barrier[x].pos_x - barrier[x].width/2, barrier[x].pos_y - barrier[x].thiccc/2)
                        if(laser[l].pos_x <= barrier[x].pos_x + barrier[x].width/2 and
                        laser[l].pos_x >= barrier[x].pos_x - barrier[x].width/2 and
                        laser[l].pos_y <= barrier[x].pos_y + barrier[x].thiccc/2 and
                        laser[l].pos_y >= barrier[x].pos_y - barrier[x].thiccc/2 and
                        laser[l].alive == True and barrier[x].thiccc >= 1):
                            laser[l].alive = False
                            barrier[x].thiccc -= 1


                if laser[l].type == 'player' and laser[l].alive == True:
                    for y in range(enemies_num_y):
                        for x in range(enemies_num_x):
                            # canvas.stroke_style = "yellow"
                            # canvas.line_width = 1
                            # canvas.stroke_line(enemie[y][x].pos_x + enemies_move_offset_x, enemie[y][x].pos_y + enemies_move_offset_y, enemie[y][x].pos_x + enemies_move_offset_x + enemie[y][x].hitbox_x*game_scale, enemie[y][x].pos_y + enemies_move_offset_y + enemie[y][x].hitbox_y*game_scale)
                            if (laser[l].pos_x >= enemie[y][x].pos_x + enemies_move_offset_x  and
                            laser[l].pos_y >= enemie[y][x].pos_y + enemies_move_offset_y and
                            laser[l].pos_x <= enemie[y][x].pos_x + enemies_move_offset_x + enemie[y][x].hitbox_x*game_scale and
                            laser[l].pos_y <= enemie[y][x].pos_y + enemies_move_offset_y + enemie[y][x].hitbox_y*game_scale  and
                            laser[l].alive == True and enemie[y][x].alive == True):
                                enemie[y][x].alive = False
                                laser[l].alive = False
                                global score
                                global highscore
                                score += enemie[y][x].points
                                if highscore < score:
                                    highscore = score

                if laser[l].type == 'enemie' and laser[l].alive == True and player.hit == 0:
                    if (laser[l].pos_x >= player.pos_x-(player.hitbox_x*game_scale)/2 and
                    laser[l].pos_y >= player.pos_y and
                    laser[l].pos_x <= player.pos_x + (player.hitbox_x*game_scale)/2 and
                    laser[l].pos_y <= player.pos_y + player.hitbox_y*game_scale  and
                    laser[l].alive == True):
                        player.retrys -= 1
                        player.hit = 3
                        laser[l].alive = False

    # remove dead enemie lasers
    for q in reversed(range(1, len(laser))):
        if laser[q].alive == False:
            laser.pop(q)


def animate_enemies():
    ''' toggles the enemie design '''
    global cur_anim_frame
    if cur_anim_frame > 0:
        cur_anim_frame = 0
    else:
        cur_anim_frame = 1


def move_enemies():
    ''' moves the emenies (left right and down) '''
    global emenies_move_dir
    global emenies_move_offset
    global enemie_scale
    global enemies_move_offset_x
    global enemies_move_offset_y
    if emenies_move_dir > 0:
        max_range = get_max_anim_range_right()
    else:
        max_range = get_max_anim_range_left()

    if (enemies_move_offset_x + game_scale*emenies_move_dir) * emenies_move_dir < max_range:
        enemies_move_offset_x += game_scale * emenies_move_dir
    else:
        emenies_move_dir *= -1
        enemies_move_offset_x += game_scale * emenies_move_dir
        enemies_move_offset_y += 10


# -------------------------------- Miscellaneous --------------------------------


def reset_game():
    ''' completely resets the game for a new player'''
    global score
    global counter
    global enemies_move_offset_x
    global enemies_move_offset_y
    global enemies_attack_chance
    global enemies_laser_speed
    global enemies_start_speed

    score = 0
    counter = 0
    enemies_move_offset_x = 0
    enemies_move_offset_y = 50
    player.pos_x = 250
    player.retrys = 3
    enemies_attack_chance = enemies_attack_chance_default
    enemies_laser_speed = enemies_laser_speed_default
    enemies_start_speed = enemies_start_speed_default

    for y in range(enemies_num_y):
        for x in range(enemies_num_x):
            enemie[y][x].alive = True

    for x in range(4):
        barrier[x].thiccc = 10

    kill_all_laser()


def next_level():
    ''' partially resets the game and increases the difficulty '''
    global counter
    global enemies_move_offset_x
    global enemies_move_offset_y
    global enemies_attack_chance
    global enemies_laser_speed
    global enemies_start_speed

    counter = 0
    enemies_move_offset_x = 0
    enemies_move_offset_y = 50
    player.pos_x = 250
    player.retrys = 3

    enemies_attack_chance -= enemies_attack_chance_step
    enemies_laser_speed -= enemies_laser_speed_step
    enemies_start_speed -= enemies_start_speed_step

    for y in range(enemies_num_y):
        for x in range(enemies_num_x):
            enemie[y][x].alive = True

    for x in range(4):
        barrier[x].thiccc = 10

    kill_all_laser()


def spawn_enemie_lasers():
    ''' randomly spawns a laser moving downward from a random enemies position (must be lowest in collumn) '''
    lowest_enemie_col = [['NaN' for _ in range(2)] for _ in range(enemies_num_x)]
    active_enemie_cols = 0
    if random.randrange(0, enemies_attack_chance) == 0:

        for x in range(enemies_num_x):
            found = False
            for y in reversed(range(enemies_num_y)):
                if enemie[y][x].alive == True and found == False:
                    lowest_enemie_col[x][0] = y
                    lowest_enemie_col[x][1] = x
                    active_enemie_cols += 1
                    found = True

        for i in reversed(range(len(lowest_enemie_col))):
            if lowest_enemie_col[i][0] == 'NaN':
                lowest_enemie_col.pop(i)

        if active_enemie_cols > 0:
            sel_enemie = random.randrange(0, active_enemie_cols)
            this_enemie = enemie[lowest_enemie_col[sel_enemie][0]][lowest_enemie_col[sel_enemie][1]]

            laser.append(Enemie_Laser())
            laser[len(laser)-1].pos_x = this_enemie.pos_x + (this_enemie.hitbox_x*game_scale)/2 + enemies_move_offset_x
            laser[len(laser)-1].pos_y = this_enemie.pos_y + this_enemie.hitbox_y*game_scale + enemies_move_offset_y
            laser[len(laser)-1].speed_y = -10


def kill_all_laser():
    ''' removes or disables all lasers '''
    for l in reversed(range(len(laser))):
        if(l != 0):
            laser.pop(l)
        else:
            laser[l].alive = False


def check_game_over():
    ''' check for game over conditions '''
    global game_state
    lowest_enemie_y = 0
    lowest_enemie_height = 0
    for x in range(enemies_num_x):
        for y in range(enemies_num_y):
            if enemie[y][x].alive == True and enemie[y][x].pos_y > lowest_enemie_y:
                lowest_enemie_y = enemie[y][x].pos_y
                lowest_enemie_height = enemie[y][x].hitbox_y
    # print(f"lowest enemie:{lowest_enemie_y} + move_y_offset:{enemies_move_offset_y} = {lowest_enemie_y + enemies_move_offset_y}")

    if (lowest_enemie_y + lowest_enemie_height*game_scale + enemies_move_offset_y >= game_over_pos_y or player.retrys <= 0):
        game_state = 'game_over'


def event_loop():
    ''' the main loop '''
    global player
    global counter
    global game_state
    global enemies_start_speed

    if game_state == 'init_screen':
        draw_init_screen()

    elif game_state == 'playing':
        anim_thread = threading.Timer(0.05, event_loop)
        anim_thread.name = 'MyThread'
        anim_thread.start()

        counter += 1

        inv_speed = (enemies_start_speed - enemies_move_offset_y/20)
        if inv_speed < 1:
            inv_speed = 1

        if counter % inv_speed == 0:
            animate_enemies()
            move_enemies()

        spawn_enemie_lasers()
        move_lasers()
        check_game_over()

        with hold_canvas(canvas):
            draw_game()
            draw_barriers()
            draw_player()
            draw_enemies()
            draw_lasers()
        pass

        if total_enemies_alive == 0:
            next_level()

    elif game_state == 'game_over':
        draw_game_over_screen()


    # display(canvas)


canvas.on_key_down(on_keyboard_event)

display(canvas, out)
event_loop()
