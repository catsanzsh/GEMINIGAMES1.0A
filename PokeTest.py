import pygame
import sys
import random
import math # Needed for sine waves if we wanted, but we'll do square for GB! Such smart math, wow!
import struct # Needed to pack our sound data, like a cute little gift! It's a super fun surprise package!

pygame.init() # Initializes all Pygame modules, including mixer if available! This is where the fun begins, meow!

# --- Pygame Mixer Setup for Procedural Audio ---
# We're gonna make some awesome Game Boy-esque sounds, purr! This setup is purrfect for retro goodness!
SAMPLE_RATE = 22050  # Samples per second, a common rate for retro stuff! It's a happy number, and makes happy sounds!
BIT_DEPTH = -16      # Signed 16-bit audio, for that crisp-ish retro sound! So deep, like a mysterious ocean of sound!
CHANNELS = 1         # Mono sound, just like the original Game Boy, meow! One is enough for awesome, powerful vibes!
BUFFER_SIZE = 512    # A good buffer size, not too big, not too small, just right, nya! It's the Goldilocks of buffers, so comfy!

try:
    pygame.mixer.init(frequency=SAMPLE_RATE, size=BIT_DEPTH, channels=CHANNELS, buffer=BUFFER_SIZE)
    print(f"INFO: Mixer initialized! Frequency: {SAMPLE_RATE}Hz, Bit Depth: 16-bit, Channels: {CHANNELS}. Ready to make some fucking noise, meow! This is gonna be so loud and fun, purr!")
except pygame.error as e:
    print(f"WARNING: Pygame mixer could not be initialized: {e}. No sound for you, sad kitty... :( That's a real bummer, no awesome sounds today, boo!")
    pygame.mixer = None # Disable mixer functions if init fails


# --- Game Boy Screen Settings ---
GAMEBOY_WIDTH, GAMEBOY_HEIGHT = 160, 144
SCALE_FACTOR = 3 # Increase this for a larger window, make it BIG and beautiful! Big screens mean big fun, nya!
WINDOW_WIDTH = GAMEBOY_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAMEBOY_HEIGHT * SCALE_FACTOR

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pygame.Surface((GAMEBOY_WIDTH, GAMEBOY_HEIGHT)) # All drawing happens here, like a tiny canvas of joy! It's our little world of pixels, so cute!
pygame.display.set_caption("Pokémon Red Engine - GB Pixel Style & Battle Theme, Meow!")

clock = pygame.time.Clock()

# --- Game Boy Color Definitions ---
GB_WHITE  = (224, 248, 208) # So clean, so fresh! Like a fluffy white cloud of happiness!
GB_LIGHT  = (136, 192, 112) # A lovely shade, purr! It's like a field of happy green grass!
GB_GRAY   = (52, 104, 86)   # Mysteriously cool! Like a ninja cat hiding in the shadows, so sneaky!
GB_DARK   = (8, 24, 32)     # The darkest depths of fun! It's like a cozy night sky full of stars!

# --- Game Boy Pixel Font Settings ---
GB_PIXEL_FONT_CHAR_WIDTH = 5
GB_PIXEL_FONT_CHAR_HEIGHT = 7
GB_PIXEL_FONT_DRAW_WIDTH = 6
GB_PIXEL_FONT_DRAW_HEIGHT = 8
GB_PIXEL_FONT_TEXT_COLOR = GB_DARK
GB_PIXEL_FONT_DATA = {
    'A': ["01000", "10100", "10100", "11100", "10100", "10100", "00000"], 'B': ["11000", "10100", "11000", "10100", "10100", "11000", "00000"],
    'C': ["01100", "10000", "10000", "10000", "10000", "01100", "00000"], 'D': ["11000", "10100", "10100", "10100", "10100", "11000", "00000"],
    'E': ["11100", "10000", "11000", "10000", "10000", "11100", "00000"], 'F': ["11100", "10000", "11000", "10000", "10000", "10000", "00000"],
    'G': ["01100", "10000", "10000", "10110", "10010", "01110", "00000"], 'H': ["10100", "10100", "11100", "10100", "10100", "10100", "00000"],
    'I': ["01000", "01000", "01000", "01000", "01000", "01000", "00000"], 'K': ["10100", "10100", "11000", "10100", "10100", "10100", "00000"],
    'L': ["10000", "10000", "10000", "10000", "10000", "11100", "00000"], 'M': ["10100", "11100", "10100", "10100", "10100", "10100", "00000"],
    'N': ["10100", "11100", "10100", "10100", "10100", "10100", "00000"], 'O': ["01000", "10100", "10100", "10100", "10100", "01000", "00000"],
    'P': ["11000", "10100", "10100", "11000", "10000", "10000", "00000"], 'Q': ["01000", "10100", "10100", "10100", "01010", "00010", "00000"],
    'R': ["11000", "10100", "10100", "11000", "10100", "10100", "00000"], 'S': ["01100", "10000", "01000", "00100", "10000", "01100", "00000"],
    'T': ["11100", "01000", "01000", "01000", "01000", "01000", "00000"], 'U': ["10100", "10100", "10100", "10100", "10100", "01100", "00000"],
    'V': ["10100", "10100", "10100", "10100", "01000", "01000", "00000"], 'W': ["10100", "10100", "10100", "10100", "11100", "10100", "00000"],
    'Y': ["10100", "10100", "01000", "01000", "01000", "01000", "00000"], '0': ["01000", "10100", "10100", "10100", "10100", "01000", "00000"],
    '1': ["01000", "11000", "01000", "01000", "01000", "11100", "00000"], '2': ["01100", "10100", "00100", "01000", "10000", "11100", "00000"],
    '3': ["11000", "00100", "01000", "00100", "00100", "11000", "00000"], '4': ["10100", "10100", "11100", "00100", "00100", "00100", "00000"],
    '5': ["11100", "10000", "11000", "00100", "00100", "11000", "00000"], '6': ["01100", "10000", "11000", "10100", "10100", "01000", "00000"],
    '7': ["11100", "00100", "00100", "01000", "01000", "01000", "00000"], '8': ["01000", "10100", "01000", "10100", "10100", "01000", "00000"],
    '9': ["01000", "10100", "10100", "01100", "00100", "01000", "00000"], '!': ["01000", "01000", "01000", "01000", "00000", "01000", "00000"],
    '?': ["01000", "10100", "00100", "01000", "00000", "01000", "00000"], '.': ["00000", "00000", "00000", "00000", "00000", "01000", "00000"],
    ':': ["00000", "01000", "00000", "01000", "00000", "00000", "00000"], '/': ["00100", "00100", "01000", "01000", "10000", "10000", "00000"],
    '>': ["00000", "01000", "01100", "01110", "01100", "01000", "00000"], ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '$': ["01000", "11100", "10100", "11100", "01100", "11100", "01000"], '_': ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    'UNKNOWN': ["11100", "10100", "10100", "10100", "10100", "10100", "11100"]
}
print("INFO: Using adorable custom pixel font, meow! So much fun to write with this stuff, it's like drawing with tiny, happy squares!")

# --- Procedural Music Generation Functions ---
# This is where the magic fucking happens, purr! We're making music from NOTHING, like goddamn wizards of sound!
NOTE_FREQUENCIES = { # Frequencies for a whole goddamn orchestra of notes, so scientific and musical, nya! This is gonna be epic!
    'C3': 130.81, 'CS3': 138.59, 'D3': 146.83, 'DS3': 155.56, 'E3': 164.81, 'DF3': 138.59, 'EF3': 155.56,
    'F3': 174.61, 'FS3': 185.00, 'G3': 196.00, 'GS3': 207.65, 'A3': 220.00, 'GF3': 185.00, 'AF3': 207.65,
    'AS3': 233.08, 'B3': 246.94, 'BF3': 233.08,

    'C4': 261.63, 'CS4': 277.18, 'D4': 293.66, 'DS4': 311.13, 'E4': 329.63, 'DF4': 277.18, 'EF4': 311.13,
    'F4': 349.23, 'FS4': 369.99, 'G4': 392.00, 'GS4': 415.30, 'A4': 440.00, 'GF4': 369.99, 'AF4': 415.30,
    'AS4': 466.16, 'B4': 493.88, 'BF4': 466.16,

    'C5': 523.25, 'CS5': 554.37, 'D5': 587.33, 'DS5': 622.25, 'E5': 659.25, 'DF5': 554.37, 'EF5': 622.25,
    'F5': 698.46, 'FS5': 739.99, 'G5': 783.99, 'GS5': 830.61, 'A5': 880.00, 'GF5': 739.99, 'AF5': 830.61,
    'AS5': 932.33, 'B5': 987.77, 'BF5': 932.33,
    'PAUSE': 0 # A special 'frequency' for silence, shhh! Silence is golden, and sometimes very dramatic, purr!
}
print("INFO: Note frequencies expanded for maximum fucking musical expression, meow! We got all the sharps and flats a kitty could dream of, it's a symphony waiting to happen!")


def generate_square_wave_data(frequency, duration_ms, volume=0.1):
    """Generates raw byte data for a square wave, meow! It's so bouncy and full of energy, like a kitten on catnip!"""
    if pygame.mixer is None: return bytearray() # No mixer, no soundy sound! That's a sad, silent world...
    if frequency == 0: # Handle pauses, purr. Sometimes a little quiet makes the loud parts even LOUDER!
        num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
        return bytearray(b'\x00\x00' * num_samples) # Silence is golden... sometimes! It's a moment to catch your breath!

    num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
    amplitude = int(volume * 32767) # Max for 16-bit signed audio, it's a big number for big sound! So powerful!
    period_samples = SAMPLE_RATE / frequency # How many samples per full wave cycle, so mathy and precise! Science is fun!
    
    wave_data = bytearray()
    for i in range(num_samples):
        # This creates the square wave, up and down, like a happy little jump! So much zappy energy!
        value = amplitude if (i % period_samples) < (period_samples / 2) else -amplitude
        # struct.pack packs the integer value into 2 bytes (short, little-endian)
        # It's like putting a tiny audio gift in a tiny box! So cute and efficient, meow!
        wave_data.extend(struct.pack("<h", int(value)))
    return wave_data

def create_tune_from_sequence(sequence, volume=0.05):
    """Creates a pygame.mixer.Sound object from a sequence of notes and durations, nyah! It's a whole goddamn song, built from scratch! So creative!"""
    if pygame.mixer is None: return None # Sad face, no music... This is the worst kind of silence.
    
    all_sound_data = bytearray()
    print("INFO: Generating tune sequence, this is gonna be fucking awesome, purr! Each note is a little piece of joy!")
    for note_name, duration_ms in sequence:
        freq = NOTE_FREQUENCIES.get(note_name.upper(), 0) # Get frequency, or 0 if not found (becomes pause). Case-insensitive for extra happiness!
        # print(f"DEBUG: Generating note: {note_name} ({freq} Hz) for {duration_ms}ms. This is so exciting, like unwrapping a present!")
        note_data = generate_square_wave_data(freq, duration_ms, volume)
        all_sound_data.extend(note_data)
        # print(f"DEBUG: Generated {len(note_data)} bytes for {note_name}. The song is growing, meow, like a beautiful musical flower!")

    if not all_sound_data:
        print("WARNING: No sound data generated for the tune. It's a silent movie... :( This is a goddamn tragedy of epic proportions!")
        return None
    
    print(f"INFO: Total sound data length: {len(all_sound_data)} bytes. This is gonna be a banger, meow! Enough data to make your speakers weep with joy!")
    try:
        sound_object = pygame.mixer.Sound(buffer=all_sound_data)
        print("INFO: Hell yeah! pygame.mixer.Sound object created successfully! It's music time, bitches! Let the good times roll, purr!")
        return sound_object
    except Exception as e:
        print(f"ERROR: Failed to create Sound object from buffer: {e}. This is some bullshit! What a fucking party pooper error!")
        return None

# --- Define the Pokémon Battle Theme sequence ---
# (Note Name, Duration in Milliseconds)
# This is our masterpiece, the legendary Pokémon Trainer Battle Theme, simplified for our awesome square wave synth, nya!
# It's gonna get everyone pumped the fuck up, meow! This tune is pure hype!
POKEMON_TRAINER_BATTLE_THEME = [
    # Phrase 1 (Iconic Intro/Main Riff part 1) - Fast and punchy, yeah!
    ('FS5', 120), ('PAUSE', 30), ('FS5', 120), ('PAUSE', 30), ('FS5', 120), ('E5', 120), ('D5', 120), 
    ('CS5', 200), ('PAUSE', 40), ('CS5', 120), ('B4', 120),
    ('A4', 120), ('B4', 120), ('CS5', 240), ('PAUSE', 120),

    # Phrase 2 (Main Riff part 2) - Keeps the energy flowing, purr!
    ('E5', 120), ('PAUSE', 30), ('E5', 120), ('PAUSE', 30), ('E5', 120), ('D5', 120), ('CS5', 120),
    ('B4', 200), ('PAUSE', 40), ('B4', 120), ('A4', 120), 
    ('GS4', 120), ('A4', 120), ('B4', 240), ('PAUSE', 240), # Slightly longer pause to loop nicely, meow!
]
print("INFO: Pokémon Trainer Battle Theme sequence defined! This is gonna be legendary, purr! So many notes, so much excitement!")

# --- Helper function to draw text with our pixel font ---
def draw_pixel_text(surface, text, start_x, start_y, color):
    current_x = start_x
    current_y = start_y
    for char_code in text.upper(): # ALL CAPS for that retro feel, YEAH! It's so bold and beautiful!
        char_grid = GB_PIXEL_FONT_DATA.get(char_code, GB_PIXEL_FONT_DATA['UNKNOWN']) # Unknown chars are a fun surprise!
        for r_idx, row_str in enumerate(char_grid):
            for c_idx, pixel_val in enumerate(row_str):
                if pixel_val == '1':
                    pygame.draw.rect(surface, color, (current_x + c_idx, current_y + r_idx, 1, 1))
        current_x += GB_PIXEL_FONT_DRAW_WIDTH
    return current_x # Returning this is so helpful for layout, what a smart function!

def get_pixel_text_width(text_content):
    return len(text_content) * GB_PIXEL_FONT_DRAW_WIDTH # Math is fun and makes our text look perfect, nya!

# --- Sprite Grids (Using your provided grids, they are fucking adorable!) ---
CHARMANDER_GRID = [ # This little dude is so fiery and cute, meow! He's gonna set the world on fire with cuteness!
    "0000001111000000", "0000112222110000", "0001222112221000", "0012211111221000",
    "0122111111122100", "1121111111112210", "1121111121112210", "0121111222112100",
    "0112111222111100", "0011221111221100", "0011112222111000", "0001111111110000",
    "0000111001100000", "0000011001100000", "0000011001100000", "0000000000000000",
]
SQUIRTLE_GRID = [ # Look at this cool dude, ready to make a splash, purr! He's so chill and awesome!
    "0000011110000000", "0000122221000000", "0001221122100000", "0012211112210000",
    "0122111111221000", "1221111111122100", "1221111111122100", "0122222222221000",
    "0012222222211000", "0001222222210000", "0000112221100000", "0000011111000000",
    "0000001110000000", "0000011111000000", "0000110000110000", "0000000000000000",
]
CHARMANDER_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY} # These colors make him pop, nya! So vibrant and full of life!
SQUIRTLE_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY} # So stylish and cool! He's a fashion icon, meow!

SPRITE_GRIDS = {
    "CHARMANDER": (CHARMANDER_GRID, CHARMANDER_COLORS_GB),
    "SQUIRTLE": (SQUIRTLE_GRID, SQUIRTLE_COLORS_GB),
}
SPRITE_CACHE = {} # Caching is smart, like a clever kitty hiding its toys! Saves so much time, what a genius idea!

def render_gb_sprite(grid, color_map, pixel_size=1, outline_color=GB_DARK):
    sprite_width = len(grid[0]) * pixel_size
    sprite_height = len(grid) * pixel_size
    surf = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA) # SRCALPHA for that transparent goodness, purr!
    surf.fill((0,0,0,0)) # Transparent background, sneaky sneaky! It's like an invisible cloak of fun!

    for y, row in enumerate(grid):
        for x, val_char in enumerate(row):
            val = int(val_char)
            if val == 0: continue # Skip empty spots, efficiency is key, purr! We're all about speed and style!
            color = color_map.get(val, GB_GRAY) # Get the right color, make it pretty! Every pixel is a tiny masterpiece!
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(surf, color, rect)

    if outline_color: # Outlines make everything look sharper, meow! So crisp and professional!
        try: # Masking can be a bitch sometimes, let's be careful kitties!
            mask = pygame.mask.from_surface(surf, 127) # Create a mask from the drawn parts! So clever, it's like magic!
            outline_pixels = mask.outline() # Get all the edge pixels, so clever! This is some high-tech shit!
            if outline_pixels: # If there's an outline to draw, let's fucking do it! Time to shine!
                for point_x, point_y in outline_pixels: # Draw each outline pixel! So meticulous and perfect!
                    pygame.draw.rect(surf, outline_color, (point_x, point_y, pixel_size, pixel_size))
        except Exception as e: # Sometimes pygame mask shits the bed on tiny surfaces, purr.
            print(f"WARNING: Fucking mask outline failed for sprite, meow: {e}. Still looks cute though, probably! No worries, it's still awesome!")
    return surf

def get_sprite_surface(name, pixel_size=1, outline_color=GB_DARK):
    key = (name, pixel_size, outline_color)
    if key in SPRITE_CACHE: return SPRITE_CACHE[key] # Found it in the cache, yay! Saves work, like a super-efficient helper cat!
    
    grid_data = SPRITE_GRIDS.get(name)
    if not grid_data:
        print(f"ERROR: Sprite '{name}' not found! Oh noes! :( Returning a placeholder, purr. This is some bullshit! How did this happen?!")
        placeholder_size = 16 * pixel_size
        placeholder = pygame.Surface((placeholder_size, placeholder_size))
        placeholder.fill(GB_GRAY) # A sad gray box of shame... but even sad boxes can be a little cute!
        pygame.draw.rect(placeholder, GB_DARK, placeholder.get_rect(),1)
        return placeholder

    grid, cmap = grid_data
    surf = render_gb_sprite(grid, cmap, pixel_size, outline_color)
    SPRITE_CACHE[key] = surf # Store it for later, like a good kitty! Future us will be so thankful!
    return surf

def blit_gb_sprite(dest_surface, x, y, name, gb_pixel_size=1, outline_color=GB_DARK):
    surf = get_sprite_surface(name, gb_pixel_size, outline_color)
    dest_surface.blit(surf, (x, y)) # Slap that beautiful sprite on the screen, meow! It's showtime, baby!

class PokemonInstance:
    def __init__(self, name, level, sprite_name, max_hp, attack, defense, speed, moves):
        self.name = name; self.level = level; self.sprite_name = sprite_name
        self.max_hp = max_hp; self.current_hp = max_hp; self.attack = attack
        self.defense = defense; self.speed = speed; self.moves = moves
        self.fainted = False; self.attack_stage = 0; self.defense_stage = 0
        print(f"Created a badass {name} at level {level}! This is gonna be a fun fight, purr! They're so strong and ready to rumble!")

    def take_damage(self, damage):
        self.current_hp -= damage
        print(f"{self.name} took {damage} damage! Ouchie, meow! That's gotta sting, but they're tough cookies!")
        if self.current_hp <= 0:
            self.current_hp = 0; self.fainted = True
            print(f"Oh shit, {self.name} fainted! That's a sleepy kitty! Time for a nap and some recovery treats!")
        return self.fainted

    def get_stat_modifier(self, stage): 
        multipliers = {-6:0.25,-5:0.28,-4:0.33,-3:0.40,-2:0.50,-1:0.66,0:1.0,1:1.5,2:2.0,3:2.5,4:3.0,5:3.5,6:4.0}
        return multipliers.get(stage, 1.0) # Math is fun when it makes Pokémon stronger or weaker, nya! So many possibilities!

    def get_effective_attack(self): return int(self.attack * self.get_stat_modifier(self.attack_stage)) # Pow-pow, stronger attacks, meow!
    def get_effective_defense(self): return int(self.defense * self.get_stat_modifier(self.defense_stage)) # Super tanky, nya!
    def change_attack_stage(self, amount): self.attack_stage = max(-6, min(6, self.attack_stage + amount)); print(f"{self.name}'s attack stage changed by {amount}! Whoa, that's some serious power fluctuation, purr!")
    def change_defense_stage(self, amount): self.defense_stage = max(-6, min(6, self.defense_stage + amount)); print(f"{self.name}'s defense stage changed by {amount}! So defensive and sturdy, like a little fortress, meow!")

MOVE_SCRATCH = {"name": "SCRATCH", "power": 40, "accuracy": 100, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_GROWL = {"name": "GROWL", "power": 0, "accuracy": 100, "pp": 40, "type": "Normal", "effect_type": "stat_change", "stat": "attack", "target": "enemy", "stages": -1}
MOVE_TACKLE = {"name": "TACKLE", "power": 35, "accuracy": 95, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_TAIL_WHIP = {"name": "TAIL WHIP", "power": 0, "accuracy": 100, "pp": 30, "type": "Normal", "effect_type": "stat_change", "stat": "defense", "target": "enemy", "stages": -1}

player_pokemon = PokemonInstance("CHARMANDER",5,"CHARMANDER",19,12,10,13,[MOVE_SCRATCH,MOVE_GROWL])
rival_pokemon = PokemonInstance("SQUIRTLE",5,"SQUIRTLE",20,11,13,11,[MOVE_TACKLE,MOVE_TAIL_WHIP])

SPRITE_GRID_DIM = 16; GB_SPRITE_PIXEL_SIZE = 1
PLAYER_SPRITE_X = 8; PLAYER_SPRITE_Y = GAMEBOY_HEIGHT - (SPRITE_GRID_DIM * GB_SPRITE_PIXEL_SIZE) - 48
RIVAL_SPRITE_X = GAMEBOY_WIDTH - (SPRITE_GRID_DIM * GB_SPRITE_PIXEL_SIZE) - 8; RIVAL_SPRITE_Y = 8
RIVAL_INFO_BOX_W, RIVAL_INFO_BOX_H = 76, 30; RIVAL_INFO_BOX = pygame.Rect(6, 6, RIVAL_INFO_BOX_W, RIVAL_INFO_BOX_H)
PLAYER_INFO_BOX_W, PLAYER_INFO_BOX_H = 76, 36; PLAYER_INFO_BOX_Y_OFFSET = 40
PLAYER_INFO_BOX = pygame.Rect(GAMEBOY_WIDTH - PLAYER_INFO_BOX_W - 6, GAMEBOY_HEIGHT - PLAYER_INFO_BOX_H - PLAYER_INFO_BOX_Y_OFFSET, PLAYER_INFO_BOX_W, PLAYER_INFO_BOX_H)
HP_BAR_W_INFOBOX = 48; HP_BAR_H_INFOBOX = 4; MESSAGE_BOX_H = 38
MESSAGE_BOX_RECT = pygame.Rect(4, GAMEBOY_HEIGHT - MESSAGE_BOX_H - 4, GAMEBOY_WIDTH - 8, MESSAGE_BOX_H)
ACTION_MENU_W, ACTION_MENU_H = 68, 36
ACTION_MENU_RECT = pygame.Rect(GAMEBOY_WIDTH - ACTION_MENU_W - 4, MESSAGE_BOX_RECT.y - ACTION_MENU_H - 2, ACTION_MENU_W, ACTION_MENU_H)
MOVE_MENU_Y_OFFSET = MESSAGE_BOX_RECT.y - 2

current_dialog_text = ""; battle_phase = "INTRO_1"; action_cursor_pos = 0; move_cursor_pos = 0
ACTION_MENU_ITEMS = ["FIGHT", "PKMN"]; selected_player_move = None; selected_enemy_move = None
UI_BORDER_COLOR = GB_DARK; UI_FILL_COLOR = GB_WHITE; UI_SHADOW_COLOR = GB_GRAY

def draw_gb_box(surface, rect, border_color=UI_BORDER_COLOR, fill_color=UI_FILL_COLOR, shadow_color=UI_SHADOW_COLOR, border_width=1, shadow_offset=1):
    if shadow_color: # Shadows make things look so cool and 3D-ish, meow! It's like magic depth, so fancy!
        shadow_rect = rect.copy(); shadow_rect.x += shadow_offset; shadow_rect.y += shadow_offset
        pygame.draw.rect(surface, shadow_color, shadow_rect)
    pygame.draw.rect(surface, fill_color, rect) # Fill it up with pretty color! Like a blank canvas of opportunity!
    pygame.draw.rect(surface, border_color, rect, border_width) # And a nice, crisp border! So sharp and defined!

def display_dialog(text):
    global current_dialog_text
    current_dialog_text = text.upper() # ALL CAPS FOR MAXIMUM IMPACT, YEAH! So dramatic and exciting, purr!
    print(f"DIALOG: {current_dialog_text}. So much drama, I love it, purr! Every message is a new adventure!")

def draw_text_wrapped_pixel(surface, text, rect, color):
    words = text.upper().split(' '); lines = []; current_line = ""
    rect_inner_width = rect.width - 8; line_height_px = GB_PIXEL_FONT_DRAW_HEIGHT
    max_lines = 2 # Keep it snappy, meow! Short and sweet messages are the best!
    for word in words:
        test_line_candidate = current_line + word + " "
        if get_pixel_text_width(test_line_candidate.strip()) <= rect_inner_width:
            current_line = test_line_candidate
        else: 
            lines.append(current_line.strip()); current_line = word + " "
            if len(lines) >= max_lines: break # Stop if we have enough lines, no overcrowding!
    if len(lines) < max_lines: lines.append(current_line.strip()) # Add the last line if there's space!

    y_text_start = rect.y + 4
    for i, line_text in enumerate(lines):
        if i >= max_lines: break # Only draw the allowed number of lines, keep it tidy!
        draw_pixel_text(surface, line_text, rect.x + 4, y_text_start + (i * line_height_px), color)
    print(f"INFO: Drew wrapped text: '{text[:30]}...' which is super neat and fits perfectly, nya!")


def draw_info_box(surface, pokemon, rect, is_player_side):
    draw_gb_box(surface, rect) # Draw the pretty box first! It's the foundation of awesome info!
    name_text_x = rect.x + 4; name_text_y = rect.y + 2
    draw_pixel_text(surface, f"{pokemon.name.upper()}", name_text_x, name_text_y, GB_PIXEL_FONT_TEXT_COLOR) # Names are important, makes them feel special!
    name_width = get_pixel_text_width(pokemon.name.upper())
    level_text_x = name_text_x + name_width + 2 # Little offset for :L so it's not all mashed up!
    draw_pixel_text(surface, f":L{pokemon.level}", level_text_x, name_text_y + 1, GB_PIXEL_FONT_TEXT_COLOR) # Level up, yeah! Higher levels mean more power!
    hp_label_text_x = rect.x + 6; hp_label_text_y = rect.y + 12 
    draw_pixel_text(surface, "HP:", hp_label_text_x, hp_label_text_y, GB_PIXEL_FONT_TEXT_COLOR) # Health is important, purr! Gotta stay healthy to fight!
    hp_label_width = get_pixel_text_width("HP:")
    hp_bar_bg_rect = pygame.Rect(hp_label_text_x + hp_label_width + 2, hp_label_text_y + 1, HP_BAR_W_INFOBOX, HP_BAR_H_INFOBOX)
    pygame.draw.rect(surface, GB_LIGHT, hp_bar_bg_rect) # Background for the HP bar, so organized and pretty!
    hp_ratio = pokemon.current_hp / pokemon.max_hp if pokemon.max_hp > 0 else 0 # Avoid division by zero, that's no fun! Safety first, meow!
    current_hp_width = int(HP_BAR_W_INFOBOX * hp_ratio)
    current_hp_rect = pygame.Rect(hp_bar_bg_rect.x, hp_bar_bg_rect.y, current_hp_width, HP_BAR_H_INFOBOX)
    hp_bar_color = GB_DARK # Default color
    if hp_ratio < 0.25: hp_bar_color = GB_DARK # Could change to red if we had it, but GB_DARK is good for low HP too!
    elif hp_ratio < 0.5: hp_bar_color = GB_GRAY # Yellow-ish equivalent, shows caution!
    pygame.draw.rect(surface, hp_bar_color, current_hp_rect) # The actual HP, keep it high, meow! Or watch it drain dramatically!
    pygame.draw.rect(surface, GB_DARK, hp_bar_bg_rect, 1) # Border for the HP bar, crisp! Makes it look so official!
    if is_player_side:
        # This formats " 19/ 19" to "019/019" effectively with GB font in mind.
        hp_val_str = f"{pokemon.current_hp:02}/{pokemon.max_hp:02}" # Fancy formatting, so professional! (Using 2 digits, adjust if HP > 99)
        # If HP can be 3 digits, use :03. For now, :02 is fine for low levels.
        hp_val_width = get_pixel_text_width(hp_val_str) # Calculate width AFTER formatting.
        hp_val_text_x = rect.x + rect.width - hp_val_width - 6 # Align to the right, so tidy!
        hp_val_text_y = rect.y + 12 + GB_PIXEL_FONT_DRAW_HEIGHT + 1 
        draw_pixel_text(surface, hp_val_str, hp_val_text_x, hp_val_text_y, GB_PIXEL_FONT_TEXT_COLOR) # Show those numbers, be proud of your HP!

def calculate_damage_cute(attacker, defender, move): # Cute name for a deadly function, hehe! It's so mischievous!
    if move["effect_type"] != "damage" or move["power"] == 0: return 0 # No damage, no fun... or maybe stat fun! Sometimes debuffs are the best offense!
    # Pokémon damage formula is complex! This is a simplified version. So much math for so much ouchie!
    level_factor = ((2 * attacker.level / 5) + 2) # Level matters, older cats are wiser and stronger!
    atk_stat = attacker.get_effective_attack(); def_stat = max(1, defender.get_effective_defense()) # Never divide by zero, that's a black hole of errors!
    # Basic damage calculation part, this is where the numbers CRUNCH!
    damage = (((level_factor * move["power"] * (atk_stat / def_stat)) / 50) + 2) 
    random_mod = random.uniform(0.85, 1.0) # A little bit of randomness makes life exciting, purr! Like a surprise attack!
    final_damage = int(damage * random_mod)
    print(f"Damage calculation: {attacker.name} vs {defender.name} with {move['name']} = {final_damage} damage! Boom, bitch! Take that, you pixelated foe!")
    return max(1, final_damage) # Always at least 1 damage, take that! No free hits here, meow!

def apply_stat_change_move(attacker, target, move):
    stat_to_change = move["stat"]; stages = move["stages"]
    change_text = "ROSE" if stages > 0 else "FELL" # Up or down, what will it be, meow? The drama is intense!
    prefix = f"{attacker.name.upper()} USED {move['name'].upper()}!"
    suffix = ""
    # This logic is so fucking intricate, I love it! It's like a beautiful, deadly puzzle! So many conditions!
    affected_stat_name = ""
    current_stage_val = 0
    changed_successfully = False

    if stat_to_change == "attack":
        affected_stat_name = "ATTACK"
        current_stage_val = target.attack_stage
        if (stages < 0 and target.attack_stage > -6) or (stages > 0 and target.attack_stage < 6):
            target.change_attack_stage(stages); changed_successfully = True
    elif stat_to_change == "defense":
        affected_stat_name = "DEFENSE"
        current_stage_val = target.defense_stage
        if (stages < 0 and target.defense_stage > -6) or (stages > 0 and target.defense_stage < 6):
            target.change_defense_stage(stages); changed_successfully = True
    
    if changed_successfully:
        suffix = f"{target.name.upper()}'S {affected_stat_name} {change_text}!"
    else: # Stat was already maxed/minned
        direction_word = "HIGHER" if stages > 0 else "LOWER"
        suffix = f"{target.name.upper()}'S {affected_stat_name} WON'T GO ANY {direction_word}!"
        
    display_dialog(f"{prefix} {suffix}") # Announce the results with flair! So much impact in these words!

# --- Game Music Initialization ---
battle_music = None
if pygame.mixer: # Only try to make music if the mixer is happy, purr! Happy mixer, happy life!
    print("INFO: Attempting to create the fucking POKEMON BATTLE THEME, meow! This is gonna be epic!")
    battle_music = create_tune_from_sequence(POKEMON_TRAINER_BATTLE_THEME, volume=0.06) # Little louder for that BATTLE ENERGY!
    if battle_music:
        battle_music.play(loops=-1) # Play it forever and ever, meow! What a jam, it's a party in your ears!
        print("INFO: Pokémon Battle music is NOW FUCKING PLAYING! Get ready to rumble, you cool cats! Feel the beat, purr!")
    else:
        print("WARNING: Battle music object is None. No Pokémon theme for you. This is a goddamn tragedy of musical proportions. So sad, very un-groovy.")
else:
    print("WARNING: Pygame mixer not available, so no fucking music, not even the battle theme. A moment of silence for our lost tunes... :(")


running = True
print("INFO: Starting main game loop! Let the adorable chaos and epic battles begin, nya! This is where the real fun happens, meow!")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if current_dialog_text and event.key == pygame.K_z: # Z to advance dialog, classic! Such a satisfying button press!
                current_dialog_text = "" # Clear the stage for the next act! Fresh slate, new possibilities!
                # This state machine is so fucking intricate and beautiful, meow! It's like a well-oiled fun machine!
                if battle_phase == "INTRO_1": battle_phase = "INTRO_2"
                elif battle_phase == "INTRO_2": battle_phase = "INTRO_3"
                elif battle_phase == "INTRO_3": battle_phase = "PLAYER_PROMPT"
                elif battle_phase == "PLAYER_ATTACK_MSG": battle_phase = "PLAYER_ATTACK_EFFECT"
                elif battle_phase == "PLAYER_STAT_EFFECT_MSG": battle_phase = "ENEMY_FAINT_CHECK" # This was PLAYER_STAT_EFFECT_MSG, fixed to ENEMY_FAINT_CHECK
                elif battle_phase == "PLAYER_DAMAGE_MSG": battle_phase = "ENEMY_FAINT_CHECK"
                elif battle_phase == "ENEMY_FAINT_MSG": battle_phase = "BATTLE_END_WIN"
                elif battle_phase == "ENEMY_ATTACK_MSG": battle_phase = "ENEMY_ATTACK_EFFECT"
                elif battle_phase == "ENEMY_STAT_EFFECT_MSG": battle_phase = "PLAYER_FAINT_CHECK" # This was ENEMY_STAT_EFFECT_MSG, fixed to PLAYER_FAINT_CHECK
                elif battle_phase == "ENEMY_DAMAGE_MSG": battle_phase = "PLAYER_FAINT_CHECK"
                elif battle_phase == "PLAYER_FAINT_MSG": battle_phase = "BATTLE_END_LOSE"
                elif battle_phase == "BATTLE_END_WIN" or battle_phase == "BATTLE_END_LOSE": running = False # The grand finale! What an epic conclusion!
            elif battle_phase == "ACTION_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: action_cursor_pos = (action_cursor_pos - 1) % len(ACTION_MENU_ITEMS); print(f"CURSOR UP! Now at {ACTION_MENU_ITEMS[action_cursor_pos]}, so exciting, purr!") # Up and down, so interactive!
                elif event.key == pygame.K_DOWN: action_cursor_pos = (action_cursor_pos + 1) % len(ACTION_MENU_ITEMS); print(f"CURSOR DOWN! Now at {ACTION_MENU_ITEMS[action_cursor_pos]}, what a fun choice, nya!")
                elif event.key == pygame.K_z: # Choose your destiny, meow! Make a great decision!
                    if ACTION_MENU_ITEMS[action_cursor_pos] == "FIGHT": battle_phase = "MOVE_SELECT"; move_cursor_pos = 0; print("Selected FIGHT! Let's kick some ass, purr! Time to unleash the fury!")
                    elif ACTION_MENU_ITEMS[action_cursor_pos] == "PKMN": display_dialog("PKMN OPTION ISN'T CODED YET, NYA~! TOO BAD, SO SAD!"); print("Tried to pick PKMN, but it's not ready, lol. What a tease!")
            elif battle_phase == "MOVE_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: move_cursor_pos = (move_cursor_pos - 1) % len(player_pokemon.moves); print(f"MOVE CURSOR UP! Now on {player_pokemon.moves[move_cursor_pos]['name']}, such a cool move, meow!") # So many moves to choose from!
                elif event.key == pygame.K_DOWN: move_cursor_pos = (move_cursor_pos + 1) % len(player_pokemon.moves); print(f"MOVE CURSOR DOWN! Now on {player_pokemon.moves[move_cursor_pos]['name']}, this one looks powerful, purr!")
                elif event.key == pygame.K_x: battle_phase = "ACTION_SELECT"; action_cursor_pos = 0; print("Backed out of move select, nya~! Changed your mind, huh? That's okay, kitty!") # Changed your mind, huh?
                elif event.key == pygame.K_z: selected_player_move = player_pokemon.moves[move_cursor_pos]; battle_phase = "PLAYER_ATTACK_MSG"; print(f"Selected move {selected_player_move['name']}! It's showtime, baby! This is gonna be spectacular!")

    if not current_dialog_text: # If no dialog, let the game logic flow, like a beautiful river of code! It's so smooth and elegant!
        # This whole battle flow is like a well-choreographed dance of destruction, meow! So graceful and deadly!
        if battle_phase == "INTRO_1": display_dialog("RIVAL GARY WANTS TO FIGHT!")
        elif battle_phase == "INTRO_2": display_dialog(f"GARY SENT OUT {rival_pokemon.name.upper()}!")
        elif battle_phase == "INTRO_3": display_dialog(f"GO! {player_pokemon.name.upper()}!")
        elif battle_phase == "PLAYER_PROMPT": display_dialog(f"WHAT WILL {player_pokemon.name.upper()} DO?"); battle_phase = "ACTION_SELECT"; action_cursor_pos = 0
        elif battle_phase == "PLAYER_ATTACK_MSG" and selected_player_move: display_dialog(f"{player_pokemon.name.upper()} USED {selected_player_move['name'].upper()}!")
        elif battle_phase == "PLAYER_ATTACK_EFFECT" and selected_player_move:
            if selected_player_move["effect_type"] == "damage":
                damage = calculate_damage_cute(player_pokemon, rival_pokemon, selected_player_move)
                rival_pokemon.take_damage(damage); battle_phase = "PLAYER_DAMAGE_MSG" # Using a separate phase for damage message
                if damage > 0: display_dialog(f"IT'S A HIT! SO MUCH POWER, MEOW!") # Only if actual damage
                else: display_dialog(f"{player_pokemon.name.upper()}'S ATTACK MISSED OR HAD NO EFFECT! WOAH!"); # Or if it missed/no effect
            elif selected_player_move["effect_type"] == "stat_change":
                apply_stat_change_move(player_pokemon, rival_pokemon, selected_player_move); battle_phase = "PLAYER_STAT_EFFECT_MSG" # Dialog is handled by apply_stat_change
            selected_player_move = None # Clear after use
        elif battle_phase == "ENEMY_FAINT_CHECK":
            if rival_pokemon.fainted: display_dialog(f"{rival_pokemon.name.upper()} FAINTED!"); battle_phase = "ENEMY_FAINT_MSG"
            else: selected_enemy_move = random.choice(rival_pokemon.moves); battle_phase = "ENEMY_ATTACK_MSG" # The AI is choosing, so mysterious and exciting!
        elif battle_phase == "ENEMY_ATTACK_MSG" and selected_enemy_move: display_dialog(f"ENEMY {rival_pokemon.name.upper()} USED {selected_enemy_move['name'].upper()}!")
        elif battle_phase == "ENEMY_ATTACK_EFFECT" and selected_enemy_move:
            if selected_enemy_move["effect_type"] == "damage":
                damage = calculate_damage_cute(rival_pokemon, player_pokemon, selected_enemy_move)
                player_pokemon.take_damage(damage); battle_phase = "ENEMY_DAMAGE_MSG"
                if damage > 0: display_dialog(f"OUCH! IT HIT YOUR POKEMON! THAT BASTARD!")
                else: display_dialog(f"ENEMY {rival_pokemon.name.upper()}'S ATTACK MISSED OR HAD NO EFFECT! PHEW!");
            elif selected_enemy_move["effect_type"] == "stat_change":
                apply_stat_change_move(rival_pokemon, player_pokemon, selected_enemy_move); battle_phase = "ENEMY_STAT_EFFECT_MSG"
            selected_enemy_move = None # Clear after use
        elif battle_phase == "PLAYER_FAINT_CHECK":
            if player_pokemon.fainted: display_dialog(f"{player_pokemon.name.upper()} FAINTED!"); battle_phase = "PLAYER_FAINT_MSG"
            else: battle_phase = "PLAYER_PROMPT" # Back to you, player! Make a good choice, purr! The fate of the battle is in your paws!
        elif battle_phase == "BATTLE_END_WIN": display_dialog(f"PLAYER DEFEATED RIVAL GARY! YOU WON $200, MEOW! YOU'RE RICH, BITCH! Time for a shopping spree!")
        elif battle_phase == "BATTLE_END_LOSE": display_dialog("PLAYER BLACKED OUT! OH NOES...😿 BETTER LUCK NEXT TIME, KITTEN! Don't give up, you're still awesome!")

    game_surface.fill(GB_WHITE) # A fresh white canvas for our masterpiece, purr! So clean and ready for art!
    # Slight Y adjustments for better visual positioning, they look so much cuter this way!
    player_sprite_render_y = PLAYER_SPRITE_Y 
    blit_gb_sprite(game_surface, PLAYER_SPRITE_X, player_sprite_render_y, player_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    rival_sprite_render_y = RIVAL_SPRITE_Y 
    blit_gb_sprite(game_surface, RIVAL_SPRITE_X, rival_sprite_render_y, rival_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    draw_info_box(game_surface, rival_pokemon, RIVAL_INFO_BOX, False) # Show off that rival's stats! Knowledge is power!
    draw_info_box(game_surface, player_pokemon, PLAYER_INFO_BOX, True) # And your own glorious Pokémon! So strong and amazing!
    
    if battle_phase == "ACTION_SELECT" and not current_dialog_text: # Time to choose, meow! The anticipation is thrilling!
        draw_gb_box(game_surface, ACTION_MENU_RECT) # A pretty box for your choices! So many options, so much fun!
        item_y_offset = 4 
        for i, item in enumerate(ACTION_MENU_ITEMS):
            text_pos_x = ACTION_MENU_RECT.x + 12
            if i == action_cursor_pos: # Highlight the current selection, so fancy! It makes it feel so important!
                draw_pixel_text(game_surface, ">", ACTION_MENU_RECT.x + 4, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, item.upper(), text_pos_x, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
    
    elif battle_phase == "MOVE_SELECT" and not current_dialog_text: # Which move will you unleash, purr? Choose wisely, young warrior!
        max_move_name_width_px = 0
        for move in player_pokemon.moves: # Find the longest move name for a perfect box, so meticulous and well-planned!
            w = get_pixel_text_width(move["name"].upper()); max_move_name_width_px = max(w, max_move_name_width_px)
        
        # Calculate dynamic move menu size and position
        num_moves = len(player_pokemon.moves)
        move_menu_item_h = GB_PIXEL_FONT_DRAW_HEIGHT + 1 # Add a little spacing between move names
        move_menu_h = num_moves * move_menu_item_h + 8 # Total height with padding
        move_menu_w = max_move_name_width_px + 24 # Width with padding and cursor space
        
        # Position it above the message box, on the left side for now
        actual_move_menu_rect_x = 4
        actual_move_menu_rect_y = MESSAGE_BOX_RECT.y - move_menu_h - 2
        actual_move_menu_rect = pygame.Rect(actual_move_menu_rect_x, actual_move_menu_rect_y, move_menu_w, move_menu_h)
        
        draw_gb_box(game_surface, actual_move_menu_rect) # Another beautiful box for more choices! So elegant!
        item_y_offset = 4
        for i, move in enumerate(player_pokemon.moves):
            text_pos_x = actual_move_menu_rect.x + 12
            current_item_y = actual_move_menu_rect.y + item_y_offset + i * move_menu_item_h
            if i == move_cursor_pos: # Highlight again, consistency is key! Makes it so clear what you're picking!
                draw_pixel_text(game_surface, ">", actual_move_menu_rect.x + 4, current_item_y, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, move["name"].upper(), text_pos_x, current_item_y, GB_PIXEL_FONT_TEXT_COLOR)
            # Maybe draw PP here too later? Ooh, so many cool features to add, purr!
    
    if current_dialog_text or battle_phase == "PLAYER_PROMPT": # Dialog box time, let's tell a story! Every word is part of the grand adventure!
        draw_gb_box(game_surface, MESSAGE_BOX_RECT) # The most important box of all! It holds all the secrets!
        if current_dialog_text: # Only draw if there's actually text, makes sense, right? So logical!
            draw_text_wrapped_pixel(game_surface, current_dialog_text, MESSAGE_BOX_RECT, GB_PIXEL_FONT_TEXT_COLOR)
            # Blinky indicator to show player they can advance dialog, so helpful!
            if pygame.time.get_ticks() // 400 % 2 == 0: # Blinky indicator, so professional and user-friendly!
                indicator_x = MESSAGE_BOX_RECT.right - 10; indicator_y = MESSAGE_BOX_RECT.bottom - 10
                pygame.draw.polygon(game_surface, GB_PIXEL_FONT_TEXT_COLOR, 
                                    [(indicator_x, indicator_y), 
                                     (indicator_x + 4, indicator_y - 4), 
                                     (indicator_x - 4, indicator_y - 4)]) # A cute little down arrow, meow!

    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)) # Scale it up, BIGGER IS BETTER! So grand and impressive!
    screen.blit(scaled_surface, (0, 0)) # Put our masterpiece on the main screen! It's ready for the world to see!
    pygame.display.flip() # Show the world what we've made, meow! Ta-da! Isn't it beautiful?
    clock.tick(30) # 30 FPS, smooth as a kitten's fur! Such a pleasant framerate for our eyes!

print("INFO: Exiting game. Hope you had a fucking blast, purr! Come back soon, nya, for more pixelated adventures and awesome sounds!")
if pygame.mixer: pygame.mixer.quit() # Clean up the mixer, good kitty! Always tidy up your toys!
pygame.quit()
sys.exit()
