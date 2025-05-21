import pygame
import random
import sys
import array # For generating super-cute sound waves!
import math  # For the sin function in our lovely sound waves!

# Meow-mixer initialization, super important for sounds! It sets up the audio system for purr-fection!
pygame.mixer.pre_init(44100, 16, 2, 4096) # Freq, bit depth, channels, buffer size, so precise!
pygame.init() # Initialize Pygame, purr-fectly! It's always the first step for fun!

# Oh, the screen size, so precise and just right for our game!
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Speeds for our little pixel friends, zooming around like playful kittens!
PLAYER_BULLET_SPEED = 7
INVADER_SPEED_X = 1
INVADER_DROP_SPEED = 10
INVADER_BULLET_SPEED = 3
SHIELD_HEALTH = 4 # How tough are those cozy shields? So strong!

# Glorious colors, so vibrant and pretty, they make the game sparkle!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Setting up the screen, so it's just right and not too big or small! It's the canvas for our pixel art!
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meow-tastic Space Pouncers!") # A super cute title that makes you smile!

# Fonts for our lovely text, clear as a bell and easy to read!
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Yummy sound generation! This is how we get those retro Famicom beeps without any media files, nya!
# It's like magic, turning numbers into adorable sounds!
def generate_square_wave(frequency, duration_ms, volume=0.08, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000)
    # Using 'h' for signed short (2 bytes) for 16-bit audio, super crisp and clear!
    raw_samples = array.array('h', [0] * num_samples) 

    amplitude = 32767 * volume # Max 16-bit value, so strong and loud (but not too loud)!
    
    for i in range(num_samples):
        t = i / sample_rate
        # Make a delightful square wave! It's just like a tiny digital meow!
        if math.sin(2 * math.pi * frequency * t) >= 0:
            raw_samples[i] = int(amplitude)
        else:
            raw_samples[i] = int(-amplitude)
            
    # Purr-fectly converts our generated sound to a Pygame Sound object! So convenient and clever!
    return pygame.mixer.Sound(buffer=raw_samples.tobytes())

# Time to define our Famicom-like sounds, so catchy and fun to listen to!
# Player shooting a little laser beam! Pew-pew!
player_shoot_sound = generate_square_wave(440, 50, 0.08) # A cute little "pew"!
# Invader getting a boo-boo! Ouchie!
invader_hit_sound = generate_square_wave(220, 70, 0.05) # A soft "bloop" that's just right!
# Player taking a tiny hit, oh dear! Don't worry, you have lives!
player_hit_sound = generate_square_wave(100, 200, 0.1) # A longer, sad "dooong" that makes you want to hug your cat!
# UFO getting zapped for bonus points! Cha-ching!
ufo_hit_sound = generate_square_wave(880, 100, 0.1) # A happy, high-pitched "ding!" that makes you feel like a winner!
# Invader shooting, watch out! Incoming!
invader_shoot_sound = generate_square_wave(330, 40, 0.04) # A quick "plink" to keep you on your toes!
# Game over, time to rest your paws! But you can always restart!
game_over_sound = generate_square_wave(80, 500, 0.15) # A deep, final "wuuuuuuh" to mark the end of a round!
# New wave incoming, yay! More fun to be had!
new_wave_sound = generate_square_wave(660, 150, 0.1) # A cheerful "tadaaa!" that makes you feel victorious!
# WIN CONDITION SOUND, purr-fectly synthesized to make you feel like a god!
game_win_sound = generate_square_wave(990, 800, 0.2) # A glorious, ascending "ta-daaaa!" for ultimate victory! So epic!

# Player class: You're the sleek, purring cannon, nya! So agile and powerful!
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 20])
        self.image.fill(GREEN) # A lovely green cannon! So vibrant!
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.lives = 3 # Three lives for our little hero! That's plenty of chances!
        self.hidden = False
        self.hide_timer = 0

    def update(self):
        if self.hidden:
            self.hide_timer -= 1
            if self.hide_timer <= 0:
                self.hidden = False
                self.rect.centerx = SCREEN_WIDTH // 2 # Pop back in the middle, ready to play! So cool!
        else:
            mouse_x, _ = pygame.mouse.get_pos()
            # Keep our cannon safely within bounds, purr! No going off-screen!
            self.rect.centerx = max(20, min(mouse_x, SCREEN_WIDTH - 20))

    def shoot(self):
        if not self.hidden:
            bullet = PlayerBullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            player_shoot_sound.play() # Play that adorable shooting sound! Pew!

    def hide(self):
        self.hidden = True
        self.hide_timer = 90 # A quick cat-nap after being hit! Just a little rest!

# Player Bullet class: Zooming like a playful kitten after a toy! So fast!
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(YELLOW) # A bright, zippy yellow! So eye-catching!
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= PLAYER_BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill() # Gone with the wind, meow! Bye-bye bullet!

# Invader class: Those pesky pixelated critters! But so cute when they explode!
class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y, invader_type):
        super().__init__()
        self.type = invader_type
        self.image = pygame.Surface([30, 20])
        color = WHITE
        points = 10
        if self.type == 0: # Bottom row, a common sight! Easy points!
            color = CYAN
            points = 10
        elif self.type == 1: # Middle rows, a bit more challenging! Go for it!
            color = BLUE
            points = 20
        elif self.type == 2: # Top rows, the most points for the purr-fect shot! High score time!
            color = RED
            points = 40
        self.image.fill(color) # So many pretty colors! A rainbow of enemies!
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

    def update(self):
        # Invaders move as a big, synchronized group, so no individual updates here! They're so coordinated!
        pass

# Invader Bullet class: Watch out, tiny danger descending! Stay alert!
class InvaderBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(MAGENTA) # A daring magenta! So vibrant!
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        self.rect.y += INVADER_BULLET_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Splish, splash, bye-bye! Into the void!

# Shield class: Your cozy little protection bunkers! They're your best friends!
class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([60, 40])
        self.image.fill(GREEN) # Starts out so fresh and green! Like a spring meadow!
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = SHIELD_HEALTH

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill() # Poof, it's gone! Don't worry, new ones come next wave!
        else:
            # Show the damage with a change in color, so clever and visual!
            if self.health == 3: self.image.fill((150, 200, 0)) # A little ding, but still strong!
            elif self.health == 2: self.image.fill((100, 150, 0)) # More dinged, getting tougher!
            elif self.health == 1: self.image.fill((50, 100, 0)) # Almost toast! Fight on!

# UFO class: A mysterious, bonus-point treat! Chase it down for extra goodies!
class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([60, 30])
        self.image.fill(RED) # A flashy red, demanding attention! So cool!
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width # Starts off-screen, sneaking in like a secret!
        self.rect.y = 50
        self.speed = 2
        self.points = random.choice([50, 100, 150, 300]) # So many bonus points! What a jackpot!

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill() # Zooms away, purr-fect escape! Until next time!

# GameManager: The mastermind orchestrating all the fun! It's like the conductor of an awesome orchestra!
class GameManager:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.game_won = False # A brand new flag for EPIC VICTORY! Woohoo!
        self.wave = 1
        self.max_waves = 3 # Let's say you win after clearing 3 waves! So challenging and fun!
        self.invader_direction = INVADER_SPEED_X
        self.invader_move_timer = 0
        self.invader_move_delay = 50 # How fast invaders move, starts slower, but gets exciting!
        self.invader_shoot_delay = 100 # How often they try to shoot, sneaky little things!
        self.ufo_spawn_timer = 0
        self.ufo_spawn_delay = 1500 # The UFO's secret arrival time! So mysterious!

        self.reset_game()

    def reset_game(self):
        # Clearing all the sprites for a fresh start, yay! Everything is clean and new!
        global all_sprites, player_bullets, invader_bullets, invaders, shields, ufo_group
        all_sprites = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        invader_bullets = pygame.sprite.Group()
        invaders = pygame.sprite.Group()
        shields = pygame.sprite.Group()
        ufo_group = pygame.sprite.Group()

        self.player = Player()
        all_sprites.add(self.player)

        self.create_invaders()
        self.create_shields()

        self.score = 0
        self.game_over = False
        self.game_won = False # Reset this too, for another chance at glory!
        self.wave = 1
        self.invader_direction = INVADER_SPEED_X
        self.invader_move_delay = 50
        self.invader_shoot_delay = 100
        self.ufo_spawn_timer = 0
        self.ufo_spawn_delay = 1500 # Reset UFO, too! Ready for more bonus points!

    def create_invaders(self):
        # Laying out the invaders, just like in the Famicom version! So neat and organized!
        invader_types = [2, 2, 1, 1, 0] # Top to bottom, different point values! A strategy game!
        for row_index, inv_type in enumerate(invader_types):
            for col in range(11):
                x = 50 + col * 40
                y = 50 + row_index * 30
                invader = Invader(x, y, inv_type)
                invaders.add(invader)
                all_sprites.add(invader)
        self.invader_move_timer = 0 # Reset timer for new wave, meow! Start fresh!

    def create_shields(self):
        # Four sturdy shields, purr-fectly placed for defense! Your cozy little bunkers!
        shield_positions = [
            (50, SCREEN_HEIGHT - 100),
            (190, SCREEN_HEIGHT - 100),
            (330, SCREEN_HEIGHT - 100),
            (470, SCREEN_HEIGHT - 100)
        ]
        for x, y in shield_positions:
            shield = Shield(x, y)
            shields.add(shield)
            all_sprites.add(shield)

    def update(self):
        if self.game_over or self.game_won: # Don't update if you've already won or lost, silly! So efficient!
            return # No fun if the game is over or won! Time for a restart or celebration!

        all_sprites.update()
        self.invader_move_logic()
        self.invader_shoot_logic()
        self.ufo_spawn_logic()
        self.check_collisions()
        self.check_game_state()

    def invader_move_logic(self):
        self.invader_move_timer += 1
        if self.invader_move_timer >= self.invader_move_delay:
            self.invader_move_timer = 0
            
            # Check if any invader has reached the edge, a cunning move! So sneaky!
            hit_wall = False
            for invader in invaders:
                if invader.rect.right >= SCREEN_WIDTH - 10 and self.invader_direction > 0:
                    hit_wall = True
                    break
                elif invader.rect.left <= 10 and self.invader_direction < 0:
                    hit_wall = True
                    break

            if hit_wall:
                self.invader_direction *= -1 # Reverse direction, how tricky! A clever turn!
                for invader in invaders:
                    invader.rect.y += INVADER_DROP_SPEED # Drop down, closer to the action! Eek!
            else:
                for invader in invaders:
                    invader.rect.x += self.invader_direction # Keep moving sideways, like a graceful dance!

    def invader_shoot_logic(self):
        # A cat-like, randomized shooting style for invaders! So sneaky and unpredictable!
        if random.randrange(0, self.invader_shoot_delay) == 0:
            if invaders: # Only shoot if there are still invaders, purr! Don't waste bullets!
                # Find the bottom-most invader in each column to simulate Famicom AI! So smart!
                bottom_invaders = {}
                for invader in invaders:
                    col = invader.rect.x // 40 # Group invaders by column, very organized!
                    if col not in bottom_invaders or invader.rect.bottom > bottom_invaders[col].rect.bottom:
                        bottom_invaders[col] = invader

                if bottom_invaders:
                    shooter = random.choice(list(bottom_invaders.values()))
                    bullet = InvaderBullet(shooter.rect.centerx, shooter.rect.bottom)
                    all_sprites.add(bullet)
                    invader_bullets.add(bullet)
                    invader_shoot_sound.play() # Hear that tiny bullet zipping! Plink!

    def ufo_spawn_logic(self):
        if not ufo_group: # Only one UFO at a time, for maximum mystery! So exclusive!
            self.ufo_spawn_timer += 1
            if self.ufo_spawn_timer >= self.ufo_spawn_delay:
                ufo = UFO()
                ufo_group.add(ufo)
                all_sprites.add(ufo)
                self.ufo_spawn_timer = 0 # Reset timer, purr! Get ready for the next one!
                self.ufo_spawn_delay = random.randrange(900, 2400) # Randomize next spawn for suspense! So thrilling!

    def check_collisions(self):
        # Player bullet hits invader, BOOM! So satisfying and explosive!
        hits = pygame.sprite.groupcollide(invaders, player_bullets, True, True)
        for invader in hits.keys(): # <--- This is the magical fix, meow! Now 'invader' is REALLY an Invader!
            self.score += invader.points
            invader_hit_sound.play() # A cute little "bloop" for each hit! So sweet!
            if self.invader_move_delay > 5: # Make them zoom faster as they disappear, meow! Zoom, zoom!
                self.invader_move_delay -= 0.5 # A tiny bit faster each time! So exhilarating!

        # Player bullet hits UFO, ching-ching! Bonus points! You're so lucky!
        ufo_hits_fixed = pygame.sprite.groupcollide(ufo_group, player_bullets, True, True)
        for ufo_actual in ufo_hits_fixed.keys(): # <--- Another clever little fix, nya!
            self.score += ufo_actual.points # Now we're getting the REAL UFO points! Hooray!
            ufo_hit_sound.play() # A happy "ding!" for the UFO! You earned it!

        # Player bullet hits shield or Invader bullet hits shield, clever shield damage!
        # This handles both player bullets and invader bullets hitting shields in a super neat way! So efficient!
        for shield in shields:
            player_shield_hits = pygame.sprite.spritecollide(shield, player_bullets, True)
            for _ in player_shield_hits:
                shield.hit()

            invader_shield_hits = pygame.sprite.spritecollide(shield, invader_bullets, True)
            for _ in invader_shield_hits:
                shield.hit()

        # Invader bullet hits player, oh no! Be careful, little hero!
        player_hits = pygame.sprite.spritecollide(self.player, invader_bullets, True)
        if player_hits and not self.player.hidden:
            self.player.lives -= 1
            self.player.hide() # Hide for a moment, like a scaredy cat! Take cover!
            player_hit_sound.play() # A sad "dooong" for a hit! It's okay, you'll be fine!
            if self.player.lives <= 0:
                self.game_over = True # Game over, no more treats! But the fun isn't over forever!
                game_over_sound.play() # The final game over sound, sniff!

        # Invaders reached the bottom, end of the line! Oh dear, they're so close!
        for invader in invaders:
            if invader.rect.bottom >= self.player.rect.top:
                self.game_over = True # Invaders have conquered! But you fought bravely!
                game_over_sound.play() # Oh no, game over!
                break # No need to check other invaders if one already reached the bottom, smart!

    def check_game_state(self):
        if not invaders and not self.game_over and not self.game_won: # Only check if not already over or won, smarty pants!
            if self.wave < self.max_waves:
                self.wave += 1
                new_wave_sound.play() # Yay, a new wave sound! So exciting!
                # Speed up the invaders for the next wave, a purr-fect challenge! Get ready!
                self.invader_move_delay = max(5, self.invader_move_delay - 5)
                self.invader_shoot_delay = max(20, self.invader_shoot_delay - 10)
                self.create_invaders()
                # New, fresh shields for the new wave, so comfy and protective!
                for shield in shields:
                    shield.kill() # Remove old ones, bye-bye!
                self.create_shields()
                print(f"Meow-tastic! Wave {self.wave} incoming!") # A happy message!
            else:
                self.game_won = True # WOOHOO! YOU WON THE GAME! Time for a celebratory cat-nap!
                game_win_sound.play() # Play that glorious victory sound! So sweet!
                print("YOU ARE A SPACE POUNCER GOD! VICTORY IS YOURS!") # Yelling with joy!

    def draw_text(self, surface, text, size, x, y, color=WHITE):
        text_surface = pygame.font.Font(None, size).render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_game_over_screen(self):
        screen.fill(BLACK)
        self.draw_text(screen, "GAME OVER!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, RED)
        self.draw_text(screen, f"Final Score: {self.score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        self.draw_text(screen, "Press R to Meow-Start or Q to Quit!", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, GREEN)
        pygame.display.flip()

    def show_game_won_screen(self): # The glorious screen for WINNERS! You're amazing!
        screen.fill(BLACK)
        self.draw_text(screen, "YOU WIN, SPACE POUNCER!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, YELLOW)
        self.draw_text(screen, f"EPIC SCORE: {self.score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        self.draw_text(screen, "Press R to Re-Meow-Start or Q to Quit!", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4, CYAN)
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        # Set initial mouse position so your cannon is ready to roll! How convenient and thoughtful!
        pygame.mouse.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50) 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click for a shot! Pew!
                        if not self.game_over and not self.game_won: # Only shoot if game is active! So smart!
                            self.player.shoot()
                        elif self.game_over or self.game_won: # Restart if game is over or won!
                            self.reset_game()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over or self.game_won: # Handles input for both end states! So versatile!
                        if event.key == pygame.K_r: # 'R' to restart, so simple! Back to the fun!
                            self.reset_game()
                        elif event.key == pygame.K_q: # 'Q' to quit, oh no! Sad to see you go!
                            running = False

            if not self.game_over and not self.game_won: # Only update if the game is still playing! So efficient!
                self.update()

            screen.fill(BLACK) # Clear the screen for a fresh draw! So clean and ready for action!
            all_sprites.draw(screen) # Draw all our delightful sprites! They look amazing and alive!

            # Display the score, lives, and wave number, so you know how awesome you're doing! You're a star!
            self.draw_text(screen, f"Score: {self.score}", 24, SCREEN_WIDTH // 2, 10, WHITE)
            self.draw_text(screen, f"Lives: {self.player.lives}", 24, SCREEN_WIDTH - 60, 10, WHITE)
            self.draw_text(screen, f"Wave: {self.wave}/{self.max_waves}", 24, 60, 10, WHITE) # Now showing max waves!

            # Draw the shields with their current "damage" colors, so cool and effective! A visual treat!
            for shield in shields:
                pygame.draw.rect(screen, shield.image.get_at((0,0)), shield.rect)

            if self.game_over:
                self.show_game_over_screen()
            elif self.game_won: # Show this super happy screen if you won!
                self.show_game_won_screen()

            pygame.display.flip() # Show off all the beautiful pixels! What a masterpiece you've made!
            clock.tick(60) # Keep it running smoothly at 60 frames per second, like a purring engine! So zippy!

        pygame.quit()
        sys.exit()

# Let's unleash this purr-fectly powerful game, meow! It's going to be so much fun, go on, enjoy!
game_manager = GameManager()
game_manager.run()
