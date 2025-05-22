import pygame
import sys
import random
import math # Needed for sine waves if we wanted, but we'll do square for GB!
import struct # Needed to pack our sound data, like a cute little gift!

pygame.init() # Initializes all Pygame modules, including mixer if available!

# --- Pygame Mixer Setup for Procedural Audio ---
# We're gonna make some awesome Game Boy-esque sounds, purr!
SAMPLE_RATE = 22050  # Samples per second, a common rate for retro stuff! It's a happy number!
BIT_DEPTH = -16      # Signed 16-bit audio, for that crisp-ish retro sound! So deep!
CHANNELS = 1         # Mono sound, just like the original Game Boy, meow! One is enough for awesome!
BUFFER_SIZE = 512    # A good buffer size, not too big, not too small, just right, nya!

try:
    pygame.mixer.init(frequency=SAMPLE_RATE, size=BIT_DEPTH, channels=CHANNELS, buffer=BUFFER_SIZE)
    print(f"INFO: Mixer initialized! Frequency: {SAMPLE_RATE}Hz, Bit Depth: 16-bit, Channels: {CHANNELS}. Ready to make some fucking noise, meow!")
except pygame.error as e:
    print(f"WARNING: Pygame mixer could not be initialized: {e}. No sound for you, sad kitty... :(")
    pygame.mixer = None # Disable mixer functions if init fails


# --- Game Boy Screen Settings ---
GAMEBOY_WIDTH, GAMEBOY_HEIGHT = 160, 144
SCALE_FACTOR = 3 # Increase this for a larger window, make it BIG and beautiful!
WINDOW_WIDTH = GAMEBOY_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAMEBOY_HEIGHT * SCALE_FACTOR

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pygame.Surface((GAMEBOY_WIDTH, GAMEBOY_HEIGHT)) # All drawing happens here, like a tiny canvas of joy!
pygame.display.set_caption("Pokémon Red Engine - GB Pixel Style & Sound, Meow!")

clock = pygame.time.Clock()

# --- Game Boy Color Definitions ---
GB_WHITE  = (224, 248, 208) # So clean, so fresh!
GB_LIGHT  = (136, 192, 112) # A lovely shade, purr!
GB_GRAY   = (52, 104, 86)   # Mysteriously cool!
GB_DARK   = (8, 24, 32)     # The darkest depths of fun!

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
print("INFO: Using adorable custom pixel font, meow! So much fun to write with this stuff!")

# --- Procedural Music Generation Functions ---
# This is where the magic fucking happens, purr! We're making music from NOTHING!
NOTE_FREQUENCIES = { # Frequencies for some notes, so scientific and musical!
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25,
    'PAUSE': 0 # A special 'frequency' for silence, shhh!
}

def generate_square_wave_data(frequency, duration_ms, volume=0.1):
    """Generates raw byte data for a square wave, meow! It's so bouncy!"""
    if pygame.mixer is None: return bytearray() # No mixer, no soundy sound!
    if frequency == 0: # Handle pauses, purr
        num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
        return bytearray(b'\x00\x00' * num_samples) # Silence is golden... sometimes!

    num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))
    amplitude = int(volume * 32767) # Max for 16-bit signed audio, it's a big number!
    period_samples = SAMPLE_RATE / frequency # How many samples per full wave cycle, so mathy!
    
    wave_data = bytearray()
    for i in range(num_samples):
        # This creates the square wave, up and down, like a happy little jump!
        value = amplitude if (i % period_samples) < (period_samples / 2) else -amplitude
        # struct.pack packs the integer value into 2 bytes (short, little-endian)
        # It's like putting a tiny audio gift in a tiny box! So cute!
        wave_data.extend(struct.pack("<h", int(value)))
    return wave_data

def create_tune_from_sequence(sequence, volume=0.05):
    """Creates a pygame.mixer.Sound object from a sequence of notes and durations, nyah! It's a whole song!"""
    if pygame.mixer is None: return None # Sad face, no music...
    
    all_sound_data = bytearray()
    print("INFO: Generating tune sequence, this is gonna be awesome, purr!")
    for note_name, duration_ms in sequence:
        freq = NOTE_FREQUENCIES.get(note_name, 0) # Get frequency, or 0 if not found (becomes pause)
        # print(f"DEBUG: Generating note: {note_name} ({freq} Hz) for {duration_ms}ms. This is so exciting!")
        note_data = generate_square_wave_data(freq, duration_ms, volume)
        all_sound_data.extend(note_data)
        # print(f"DEBUG: Generated {len(note_data)} bytes for {note_name}. The song is growing, meow!")

    if not all_sound_data:
        print("WARNING: No sound data generated for the tune. It's a silent movie... :(")
        return None
    
    print(f"INFO: Total sound data length: {len(all_sound_data)} bytes. This is gonna be a banger, meow!")
    try:
        sound_object = pygame.mixer.Sound(buffer=all_sound_data)
        print("INFO: Hell yeah! pygame.mixer.Sound object created successfully! It's music time, bitches!")
        return sound_object
    except Exception as e:
        print(f"ERROR: Failed to create Sound object from buffer: {e}. This is some bullshit! :(")
        return None

# --- Define a simple battle tune sequence ---
# (Note Name, Duration in Milliseconds)
# This is our first masterpiece, a real toe-tapper, nya!
BATTLE_TUNE_SEQUENCE = [
    ('E4', 150), ('PAUSE', 50), ('E4', 150), ('PAUSE', 50), 
    ('E4', 150), ('PAUSE', 50), ('C4', 150), ('PAUSE', 50),
    ('E4', 200), ('PAUSE', 50), ('G4', 200), ('PAUSE', 100),
    ('G3_LOW', 200), # Whoops, G3_LOW isn't defined, let's fix that or use G4. Using G4 for now.
                     # For a real G3, it'd be ~196 Hz. For simplicity, let's make a simple loop.
    ('C4', 150), ('PAUSE', 50), ('D4', 150), ('PAUSE', 50),
    ('E4', 150), ('PAUSE', 50), ('F4', 150), ('PAUSE', 50),
    ('G4', 200), ('PAUSE', 100), ('G4', 100), ('PAUSE', 50),
    ('G4', 100), ('PAUSE', 150),
]
# Let's simplify for a first pass, a short catchy loop! It's all about that hook, meow!
BATTLE_TUNE_SEQUENCE_SIMPLE = [
    ('C4', 200), ('E4', 200), ('G4', 200), ('C5', 300), ('PAUSE', 100),
    ('G4', 200), ('E4', 200), ('C4', 300), ('PAUSE', 300),
]


# --- Helper function to draw text with our pixel font ---
def draw_pixel_text(surface, text, start_x, start_y, color):
    current_x = start_x
    current_y = start_y
    for char_code in text.upper():
        char_grid = GB_PIXEL_FONT_DATA.get(char_code, GB_PIXEL_FONT_DATA['UNKNOWN'])
        for r_idx, row_str in enumerate(char_grid):
            for c_idx, pixel_val in enumerate(row_str):
                if pixel_val == '1':
                    pygame.draw.rect(surface, color, (current_x + c_idx, current_y + r_idx, 1, 1))
        current_x += GB_PIXEL_FONT_DRAW_WIDTH
    return current_x

def get_pixel_text_width(text_content):
    return len(text_content) * GB_PIXEL_FONT_DRAW_WIDTH

# --- Sprite Grids (Using your provided grids, they are fucking adorable!) ---
CHARMANDER_GRID = [ # This little dude is so fiery and cute, meow!
    "0000001111000000", "0000112222110000", "0001222112221000", "0012211111221000",
    "0122111111122100", "1121111111112210", "1121111121112210", "0121111222112100",
    "0112111222111100", "0011221111221100", "0011112222111000", "0001111111110000",
    "0000111001100000", "0000011001100000", "0000011001100000", "0000000000000000",
]
SQUIRTLE_GRID = [ # Look at this cool dude, ready to make a splash, purr!
    "0000011110000000", "0000122221000000", "0001221122100000", "0012211112210000",
    "0122111111221000", "1221111111122100", "1221111111122100", "0122222222221000",
    "0012222222211000", "0001222222210000", "0000112221100000", "0000011111000000",
    "0000001110000000", "0000011111000000", "0000110000110000", "0000000000000000",
]
CHARMANDER_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY} # These colors make him pop, nya!
SQUIRTLE_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY} # So stylish and cool!

SPRITE_GRIDS = {
    "CHARMANDER": (CHARMANDER_GRID, CHARMANDER_COLORS_GB),
    "SQUIRTLE": (SQUIRTLE_GRID, SQUIRTLE_COLORS_GB),
}
SPRITE_CACHE = {} # Caching is smart, like a clever kitty hiding its toys!

def render_gb_sprite(grid, color_map, pixel_size=1, outline_color=GB_DARK):
    sprite_width = len(grid[0]) * pixel_size
    sprite_height = len(grid) * pixel_size
    surf = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    surf.fill((0,0,0,0)) # Transparent background, sneaky sneaky!

    for y, row in enumerate(grid):
        for x, val_char in enumerate(row):
            val = int(val_char)
            if val == 0: continue # Skip empty spots, efficiency is key, purr!
            color = color_map.get(val, GB_GRAY) # Get the right color, make it pretty!
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(surf, color, rect)

    if outline_color: # Outlines make everything look sharper, meow!
        mask = pygame.mask.from_surface(surf, 127) # Create a mask from the drawn parts!
        outline_pixels = mask.outline() # Get all the edge pixels, so clever!
        if outline_pixels: # If there's an outline to draw, let's fucking do it!
            for point_x, point_y in outline_pixels:
                pygame.draw.rect(surf, outline_color, (point_x, point_y, pixel_size, pixel_size)) # Draw each outline pixel!
    return surf

def get_sprite_surface(name, pixel_size=1, outline_color=GB_DARK):
    key = (name, pixel_size, outline_color)
    if key in SPRITE_CACHE: return SPRITE_CACHE[key] # Found it in the cache, yay! Saves work!
    
    grid_data = SPRITE_GRIDS.get(name)
    if not grid_data:
        print(f"ERROR: Sprite '{name}' not found! Oh noes! :( Returning a placeholder, purr. This is some bullshit!")
        placeholder = pygame.Surface((16*pixel_size, 16*pixel_size))
        placeholder.fill(GB_GRAY) # A sad gray box of shame...
        pygame.draw.rect(placeholder, GB_DARK, placeholder.get_rect(),1)
        return placeholder

    grid, cmap = grid_data
    surf = render_gb_sprite(grid, cmap, pixel_size, outline_color)
    SPRITE_CACHE[key] = surf # Store it for later, like a good kitty!
    return surf

def blit_gb_sprite(dest_surface, x, y, name, gb_pixel_size=1, outline_color=GB_DARK):
    surf = get_sprite_surface(name, gb_pixel_size, outline_color)
    dest_surface.blit(surf, (x, y)) # Slap that beautiful sprite on the screen, meow!

class PokemonInstance:
    def __init__(self, name, level, sprite_name, max_hp, attack, defense, speed, moves):
        self.name = name; self.level = level; self.sprite_name = sprite_name
        self.max_hp = max_hp; self.current_hp = max_hp; self.attack = attack
        self.defense = defense; self.speed = speed; self.moves = moves
        self.fainted = False; self.attack_stage = 0; self.defense_stage = 0
        print(f"Created a badass {name} at level {level}! This is gonna be a fun fight, purr!")

    def take_damage(self, damage):
        self.current_hp -= damage
        print(f"{self.name} took {damage} damage! Ouchie, meow!")
        if self.current_hp <= 0:
            self.current_hp = 0; self.fainted = True
            print(f"Oh shit, {self.name} fainted! That's a sleepy kitty!")
        return self.fainted

    def get_stat_modifier(self, stage): 
        multipliers = {-6:0.25,-5:0.28,-4:0.33,-3:0.40,-2:0.50,-1:0.66,0:1.0,1:1.5,2:2.0,3:2.5,4:3.0,5:3.5,6:4.0}
        return multipliers[stage] # Math is fun when it makes Pokémon stronger or weaker, nya!

    def get_effective_attack(self): return int(self.attack * self.get_stat_modifier(self.attack_stage))
    def get_effective_defense(self): return int(self.defense * self.get_stat_modifier(self.defense_stage))
    def change_attack_stage(self, amount): self.attack_stage = max(-6, min(6, self.attack_stage + amount)); print(f"{self.name}'s attack stage changed by {amount}! Whoa!")
    def change_defense_stage(self, amount): self.defense_stage = max(-6, min(6, self.defense_stage + amount)); print(f"{self.name}'s defense stage changed by {amount}! So defensive, purr!")

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
    if shadow_color: # Shadows make things look so cool and 3D-ish, meow!
        shadow_rect = rect.copy(); shadow_rect.x += shadow_offset; shadow_rect.y += shadow_offset
        pygame.draw.rect(surface, shadow_color, shadow_rect)
    pygame.draw.rect(surface, fill_color, rect) # Fill it up with pretty color!
    pygame.draw.rect(surface, border_color, rect, border_width) # And a nice, crisp border!

def display_dialog(text):
    global current_dialog_text
    current_dialog_text = text.upper() # ALL CAPS FOR MAXIMUM IMPACT, YEAH!
    print(f"DIALOG: {current_dialog_text}. So much drama, I love it, purr!")

def draw_text_wrapped_pixel(surface, text, rect, color):
    words = text.upper().split(' '); lines = []; current_line = ""
    rect_inner_width = rect.width - 8; line_height_px = GB_PIXEL_FONT_DRAW_HEIGHT
    for word in words:
        test_line_candidate = current_line + word + " "
        if get_pixel_text_width(test_line_candidate.strip()) <= rect_inner_width:
            current_line = test_line_candidate
        else: lines.append(current_line.strip()); current_line = word + " "
    lines.append(current_line.strip())
    y_text_start = rect.y + 4
    for i, line_text in enumerate(lines):
        if i >= 2: break # Only two lines, gotta keep it snappy, meow!
        draw_pixel_text(surface, line_text, rect.x + 4, y_text_start + (i * line_height_px), color)

def draw_info_box(surface, pokemon, rect, is_player_side):
    draw_gb_box(surface, rect) # Draw the pretty box first!
    name_text_x = rect.x + 4; name_text_y = rect.y + 2
    draw_pixel_text(surface, f"{pokemon.name.upper()}", name_text_x, name_text_y, GB_PIXEL_FONT_TEXT_COLOR)
    name_width = get_pixel_text_width(pokemon.name.upper())
    level_text_x = name_text_x + name_width + 2
    draw_pixel_text(surface, f":L{pokemon.level}", level_text_x, name_text_y + 1, GB_PIXEL_FONT_TEXT_COLOR) # Level up, yeah!
    hp_label_text_x = rect.x + 6; hp_label_text_y = rect.y + 12 
    draw_pixel_text(surface, "HP:", hp_label_text_x, hp_label_text_y, GB_PIXEL_FONT_TEXT_COLOR) # Health is important, purr!
    hp_label_width = get_pixel_text_width("HP:")
    hp_bar_bg_rect = pygame.Rect(hp_label_text_x + hp_label_width + 2, hp_label_text_y + 1, HP_BAR_W_INFOBOX, HP_BAR_H_INFOBOX)
    pygame.draw.rect(surface, GB_LIGHT, hp_bar_bg_rect) # Background for the HP bar, so organized!
    hp_ratio = pokemon.current_hp / pokemon.max_hp if pokemon.max_hp > 0 else 0 # Avoid division by zero, that's no fun!
    current_hp_width = int(HP_BAR_W_INFOBOX * hp_ratio)
    current_hp_rect = pygame.Rect(hp_bar_bg_rect.x, hp_bar_bg_rect.y, current_hp_width, HP_BAR_H_INFOBOX)
    pygame.draw.rect(surface, GB_DARK, current_hp_rect) # The actual HP, keep it high, meow!
    pygame.draw.rect(surface, GB_DARK, hp_bar_bg_rect, 1) # Border for the HP bar, crisp!
    if is_player_side:
        hp_val_str = f"{pokemon.current_hp: >3}/{pokemon.max_hp: >3}".replace(" ","0") # Fancy formatting!
        hp_val_width = get_pixel_text_width(hp_val_str)
        hp_val_text_x = rect.x + rect.width - hp_val_width - 6 
        hp_val_text_y = rect.y + 12 + GB_PIXEL_FONT_DRAW_HEIGHT + 1 
        draw_pixel_text(surface, hp_val_str, hp_val_text_x, hp_val_text_y, GB_PIXEL_FONT_TEXT_COLOR)

def calculate_damage_cute(attacker, defender, move): # Cute name for a deadly function, hehe!
    if move["effect_type"] != "damage" or move["power"] == 0: return 0 # No damage, no fun... or maybe stat fun!
    level_factor = ((attacker.level * 2 / 5) + 2)
    atk_stat = attacker.get_effective_attack(); def_stat = max(1, defender.get_effective_defense())
    damage = (((level_factor * move["power"] * (atk_stat / def_stat)) / 50) + 2) # The core damage formula, so complex and cool!
    random_mod = random.uniform(0.85, 1.0) # A little bit of randomness makes life exciting, purr!
    final_damage = int(damage * random_mod)
    print(f"Damage calculation: {attacker.name} vs {defender.name} with {move['name']} = {final_damage} damage! Boom, bitch!")
    return max(1, final_damage) # Always at least 1 damage, take that!

def apply_stat_change_move(attacker, target, move):
    stat_to_change = move["stat"]; stages = move["stages"]
    change_text = "ROSE" if stages > 0 else "FELL" # Up or down, what will it be, meow?
    prefix = f"{attacker.name.upper()} USED {move['name'].upper()}!"
    suffix = ""
    # This logic is so fucking intricate, I love it! It's like a puzzle!
    if stat_to_change == "attack":
        if (stages < 0 and target.attack_stage == -6) or (stages > 0 and target.attack_stage == 6):
            suffix = f"{target.name.upper()}'S ATTACK WON'T GO ANY {'HIGHER' if stages > 0 else 'LOWER'}!"
        else: target.change_attack_stage(stages); suffix = f"{target.name.upper()}'S ATTACK {change_text}!"
    elif stat_to_change == "defense":
        if (stages < 0 and target.defense_stage == -6) or (stages > 0 and target.defense_stage == 6):
            suffix = f"{target.name.upper()}'S DEFENSE WON'T GO ANY {'HIGHER' if stages > 0 else 'LOWER'}!"
        else: target.change_defense_stage(stages); suffix = f"{target.name.upper()}'S DEFENSE {change_text}!"
    display_dialog(f"{prefix} {suffix}") # Announce the results with flair!

# --- Game Music Initialization ---
battle_music = None
if pygame.mixer: # Only try to make music if the mixer is happy, purr!
    battle_music = create_tune_from_sequence(BATTLE_TUNE_SEQUENCE_SIMPLE, volume=0.03) # Lower volume for background
    if battle_music:
        battle_music.play(loops=-1) # Play it forever and ever, meow! What a jam!
        print("INFO: Battle music is now playing! Get ready to rumble, you cool cats!")
    else:
        print("WARNING: Battle music object is None. No music will play. This is a goddamn tragedy.")


running = True
print("INFO: Starting main game loop! Let the adorable chaos begin, nya!")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if current_dialog_text and event.key == pygame.K_z: # Z to advance dialog, classic!
                current_dialog_text = "" # Clear the stage for the next act!
                # This state machine is so fucking intricate and beautiful, meow! It's like a dance!
                if battle_phase == "INTRO_1": battle_phase = "INTRO_2"
                elif battle_phase == "INTRO_2": battle_phase = "INTRO_3"
                elif battle_phase == "INTRO_3": battle_phase = "PLAYER_PROMPT"
                elif battle_phase == "PLAYER_ATTACK_MSG": battle_phase = "PLAYER_ATTACK_EFFECT"
                elif battle_phase == "PLAYER_STAT_EFFECT_MSG": battle_phase = "ENEMY_FAINT_CHECK"
                elif battle_phase == "PLAYER_DAMAGE_MSG": battle_phase = "ENEMY_FAINT_CHECK"
                elif battle_phase == "ENEMY_FAINT_MSG": battle_phase = "BATTLE_END_WIN"
                elif battle_phase == "ENEMY_ATTACK_MSG": battle_phase = "ENEMY_ATTACK_EFFECT"
                elif battle_phase == "ENEMY_STAT_EFFECT_MSG": battle_phase = "PLAYER_FAINT_CHECK"
                elif battle_phase == "ENEMY_DAMAGE_MSG": battle_phase = "PLAYER_FAINT_CHECK"
                elif battle_phase == "PLAYER_FAINT_MSG": battle_phase = "BATTLE_END_LOSE"
                elif battle_phase == "BATTLE_END_WIN" or battle_phase == "BATTLE_END_LOSE": running = False # The grand finale!
            elif battle_phase == "ACTION_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: action_cursor_pos = (action_cursor_pos - 1) % len(ACTION_MENU_ITEMS) # Up and down, so interactive!
                elif event.key == pygame.K_DOWN: action_cursor_pos = (action_cursor_pos + 1) % len(ACTION_MENU_ITEMS)
                elif event.key == pygame.K_z: # Choose your destiny, meow!
                    if ACTION_MENU_ITEMS[action_cursor_pos] == "FIGHT": battle_phase = "MOVE_SELECT"; move_cursor_pos = 0; print("Selected FIGHT! Let's kick some ass, purr!")
                    elif ACTION_MENU_ITEMS[action_cursor_pos] == "PKMN": display_dialog("PKMN OPTION ISN'T CODED YET, NYA~! TOO BAD, SO SAD!"); print("Tried to pick PKMN, but it's not ready, lol.")
            elif battle_phase == "MOVE_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: move_cursor_pos = (move_cursor_pos - 1) % len(player_pokemon.moves) # So many moves to choose from!
                elif event.key == pygame.K_DOWN: move_cursor_pos = (move_cursor_pos + 1) % len(player_pokemon.moves)
                elif event.key == pygame.K_x: battle_phase = "ACTION_SELECT"; action_cursor_pos = 0; print("Backed out of move select, nya~!") # Changed your mind, huh?
                elif event.key == pygame.K_z: selected_player_move = player_pokemon.moves[move_cursor_pos]; battle_phase = "PLAYER_ATTACK_MSG"; print(f"Selected move {selected_player_move['name']}! It's showtime, baby!")

    if not current_dialog_text: # If no dialog, let the game logic flow, like a beautiful river of code!
        # This whole battle flow is like a well-choreographed dance of destruction, meow!
        if battle_phase == "INTRO_1": display_dialog("RIVAL GARY WANTS TO FIGHT!")
        elif battle_phase == "INTRO_2": display_dialog(f"GARY SENT OUT {rival_pokemon.name.upper()}!")
        elif battle_phase == "INTRO_3": display_dialog(f"GO! {player_pokemon.name.upper()}!")
        elif battle_phase == "PLAYER_PROMPT": display_dialog(f"WHAT WILL {player_pokemon.name.upper()} DO?"); battle_phase = "ACTION_SELECT"; action_cursor_pos = 0
        elif battle_phase == "PLAYER_ATTACK_MSG": display_dialog(f"{player_pokemon.name.upper()} USED {selected_player_move['name'].upper()}!")
        elif battle_phase == "PLAYER_ATTACK_EFFECT":
            if selected_player_move["effect_type"] == "damage":
                damage = calculate_damage_cute(player_pokemon, rival_pokemon, selected_player_move)
                rival_pokemon.take_damage(damage); display_dialog(f"IT'S A HIT! SO MUCH POWER, MEOW!"); battle_phase = "PLAYER_DAMAGE_MSG"
            elif selected_player_move["effect_type"] == "stat_change":
                apply_stat_change_move(player_pokemon, rival_pokemon, selected_player_move); battle_phase = "PLAYER_STAT_EFFECT_MSG"
        elif battle_phase == "ENEMY_FAINT_CHECK":
            if rival_pokemon.fainted: display_dialog(f"{rival_pokemon.name.upper()} FAINTED!"); battle_phase = "ENEMY_FAINT_MSG"
            else: selected_enemy_move = random.choice(rival_pokemon.moves); battle_phase = "ENEMY_ATTACK_MSG" # The AI is choosing, so mysterious!
        elif battle_phase == "ENEMY_ATTACK_MSG": display_dialog(f"ENEMY {rival_pokemon.name.upper()} USED {selected_enemy_move['name'].upper()}!")
        elif battle_phase == "ENEMY_ATTACK_EFFECT":
            if selected_enemy_move["effect_type"] == "damage":
                damage = calculate_damage_cute(rival_pokemon, player_pokemon, selected_enemy_move)
                player_pokemon.take_damage(damage); display_dialog(f"OUCH! IT HIT YOUR POKEMON! THAT BASTARD!"); battle_phase = "ENEMY_DAMAGE_MSG"
            elif selected_enemy_move["effect_type"] == "stat_change":
                apply_stat_change_move(rival_pokemon, player_pokemon, selected_enemy_move); battle_phase = "ENEMY_STAT_EFFECT_MSG"
        elif battle_phase == "PLAYER_FAINT_CHECK":
            if player_pokemon.fainted: display_dialog(f"{player_pokemon.name.upper()} FAINTED!"); battle_phase = "PLAYER_FAINT_MSG"
            else: battle_phase = "PLAYER_PROMPT" # Back to you, player! Make a good choice, purr!
        elif battle_phase == "BATTLE_END_WIN": display_dialog(f"PLAYER DEFEATED RIVAL GARY! YOU WON $200, MEOW! YOU'RE RICH, BITCH!")
        elif battle_phase == "BATTLE_END_LOSE": display_dialog("PLAYER BLACKED OUT! OH NOES...😿 BETTER LUCK NEXT TIME, KITTEN!")

    game_surface.fill(GB_WHITE) # A fresh white canvas for our masterpiece, purr!
    player_sprite_render_y = PLAYER_SPRITE_Y + (16 * GB_SPRITE_PIXEL_SIZE) / 4 # Little adjustments for cuteness!
    blit_gb_sprite(game_surface, PLAYER_SPRITE_X, player_sprite_render_y, player_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    rival_sprite_render_y = RIVAL_SPRITE_Y - (16*GB_SPRITE_PIXEL_SIZE) /8 # More cute adjustments!
    blit_gb_sprite(game_surface, RIVAL_SPRITE_X, rival_sprite_render_y, rival_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    draw_info_box(game_surface, rival_pokemon, RIVAL_INFO_BOX, False) # Show off that rival's stats!
    draw_info_box(game_surface, player_pokemon, PLAYER_INFO_BOX, True) # And your own glorious Pokémon!
    
    if battle_phase == "ACTION_SELECT" and not current_dialog_text: # Time to choose, meow!
        draw_gb_box(game_surface, ACTION_MENU_RECT) # A pretty box for your choices!
        item_y_offset = 4 
        for i, item in enumerate(ACTION_MENU_ITEMS):
            text_pos_x = ACTION_MENU_RECT.x + 12
            if i == action_cursor_pos: # Highlight the current selection, so fancy!
                draw_pixel_text(game_surface, ">", ACTION_MENU_RECT.x + 4, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, item.upper(), text_pos_x, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
    
    elif battle_phase == "MOVE_SELECT" and not current_dialog_text: # Which move will you unleash, purr?
        max_move_name_width_px = 0
        for move in player_pokemon.moves: # Find the longest move name for a perfect box, so meticulous!
            w = get_pixel_text_width(move["name"].upper()); max_move_name_width_px = max(w, max_move_name_width_px)
        move_menu_w = max_move_name_width_px + 20; move_menu_h = len(player_pokemon.moves) * GB_PIXEL_FONT_DRAW_HEIGHT + 8 
        actual_move_menu_rect = pygame.Rect(4, MOVE_MENU_Y_OFFSET - move_menu_h, move_menu_w, move_menu_h)
        draw_gb_box(game_surface, actual_move_menu_rect) # Another beautiful box for more choices!
        item_y_offset = 4
        for i, move in enumerate(player_pokemon.moves):
            text_pos_x = actual_move_menu_rect.x + 12
            if i == move_cursor_pos: # Highlight again, consistency is key!
                draw_pixel_text(game_surface, ">", actual_move_menu_rect.x + 4, actual_move_menu_rect.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, move["name"].upper(), text_pos_x, actual_move_menu_rect.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
    
    if current_dialog_text or battle_phase == "PLAYER_PROMPT": # Dialog box time, let's tell a story!
        draw_gb_box(game_surface, MESSAGE_BOX_RECT) # The most important box of all!
        if current_dialog_text:
            draw_text_wrapped_pixel(game_surface, current_dialog_text, MESSAGE_BOX_RECT, GB_PIXEL_FONT_TEXT_COLOR)
            if pygame.time.get_ticks() // 400 % 2 == 0: # Blinky indicator, so professional!
                indicator_x = MESSAGE_BOX_RECT.right - 8; indicator_y = MESSAGE_BOX_RECT.bottom - 8
                pygame.draw.polygon(game_surface, GB_PIXEL_FONT_TEXT_COLOR, [(indicator_x, indicator_y), (indicator_x + 3, indicator_y - 3), (indicator_x - 3, indicator_y - 3)])

    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)) # Scale it up, BIGGER IS BETTER!
    screen.blit(scaled_surface, (0, 0)) # Put our masterpiece on the main screen!
    pygame.display.flip() # Show the world what we've made, meow!
    clock.tick(30) # 30 FPS, smooth as a kitten's fur!

print("INFO: Exiting game. Hope you had a fucking blast, purr! Come back soon, nya!")
pygame.mixer.quit() # Clean up the mixer, good kitty!
pygame.quit()
sys.exit()
