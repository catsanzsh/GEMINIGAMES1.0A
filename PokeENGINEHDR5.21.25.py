import pygame
import sys
import random

pygame.init()

# --- Game Boy Screen Settings ---
GAMEBOY_WIDTH, GAMEBOY_HEIGHT = 160, 144
SCALE_FACTOR = 3 # Increase this for a larger window
WINDOW_WIDTH = GAMEBOY_WIDTH * SCALE_FACTOR
WINDOW_HEIGHT = GAMEBOY_HEIGHT * SCALE_FACTOR

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pygame.Surface((GAMEBOY_WIDTH, GAMEBOY_HEIGHT)) # All drawing happens here
pygame.display.set_caption("Pokémon Red Engine - GB Pixel Style, Meow!")

clock = pygame.time.Clock()

# --- Game Boy Color Definitions ---
GB_WHITE  = (224, 248, 208)
GB_LIGHT  = (136, 192, 112)
GB_GRAY   = (52, 104, 86)
GB_DARK   = (8, 24, 32)

# --- Game Boy Pixel Font Settings ---
# This is our super cute, custom-made pixel font, purr!
GB_PIXEL_FONT_CHAR_WIDTH = 5  # Width of one character image
GB_PIXEL_FONT_CHAR_HEIGHT = 7 # Height of one character image (most GB fonts are 8px tall, but 7 for data here + 1px space below)
GB_PIXEL_FONT_DRAW_WIDTH = 6 # Actual width to advance cursor (char_width + spacing)
GB_PIXEL_FONT_DRAW_HEIGHT = 8 # Actual height for lines (char_height + spacing)
GB_PIXEL_FONT_TEXT_COLOR = GB_DARK

# You can expand this font with more characters, it's super fun to design them! Meow!
# Each character is 5 pixels wide and 7 pixels tall. '1' is a drawn pixel, '0' is empty.
GB_PIXEL_FONT_DATA = {
    'A': ["01000", "10100", "10100", "11100", "10100", "10100", "00000"],
    'B': ["11000", "10100", "11000", "10100", "10100", "11000", "00000"],
    'C': ["01100", "10000", "10000", "10000", "10000", "01100", "00000"],
    'D': ["11000", "10100", "10100", "10100", "10100", "11000", "00000"],
    'E': ["11100", "10000", "11000", "10000", "10000", "11100", "00000"],
    'F': ["11100", "10000", "11000", "10000", "10000", "10000", "00000"],
    'G': ["01100", "10000", "10000", "10110", "10010", "01110", "00000"],
    'H': ["10100", "10100", "11100", "10100", "10100", "10100", "00000"],
    'I': ["01000", "01000", "01000", "01000", "01000", "01000", "00000"],
    'K': ["10100", "10100", "11000", "10100", "10100", "10100", "00000"], # Simplified K
    'L': ["10000", "10000", "10000", "10000", "10000", "11100", "00000"],
    'M': ["10100", "11100", "10100", "10100", "10100", "10100", "00000"],
    'N': ["10100", "11100", "10100", "10100", "10100", "10100", "00000"], # Same as M for now
    'O': ["01000", "10100", "10100", "10100", "10100", "01000", "00000"],
    'P': ["11000", "10100", "10100", "11000", "10000", "10000", "00000"],
    'Q': ["01000", "10100", "10100", "10100", "01010", "00010", "00000"], # Q with tail
    'R': ["11000", "10100", "10100", "11000", "10100", "10100", "00000"],
    'S': ["01100", "10000", "01000", "00100", "10000", "01100", "00000"],
    'T': ["11100", "01000", "01000", "01000", "01000", "01000", "00000"],
    'U': ["10100", "10100", "10100", "10100", "10100", "01100", "00000"],
    'V': ["10100", "10100", "10100", "10100", "01000", "01000", "00000"], # Simplified V
    'W': ["10100", "10100", "10100", "10100", "11100", "10100", "00000"], # Simplified W
    'Y': ["10100", "10100", "01000", "01000", "01000", "01000", "00000"],
    '0': ["01000", "10100", "10100", "10100", "10100", "01000", "00000"], # Same as O
    '1': ["01000", "11000", "01000", "01000", "01000", "11100", "00000"],
    '2': ["01100", "10100", "00100", "01000", "10000", "11100", "00000"],
    '3': ["11000", "00100", "01000", "00100", "00100", "11000", "00000"],
    '4': ["10100", "10100", "11100", "00100", "00100", "00100", "00000"],
    '5': ["11100", "10000", "11000", "00100", "00100", "11000", "00000"],
    '6': ["01100", "10000", "11000", "10100", "10100", "01000", "00000"],
    '7': ["11100", "00100", "00100", "01000", "01000", "01000", "00000"],
    '8': ["01000", "10100", "01000", "10100", "10100", "01000", "00000"],
    '9': ["01000", "10100", "10100", "01100", "00100", "01000", "00000"],
    '!': ["01000", "01000", "01000", "01000", "00000", "01000", "00000"],
    '?': ["01000", "10100", "00100", "01000", "00000", "01000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01000", "00000"],
    ':': ["00000", "01000", "00000", "01000", "00000", "00000", "00000"],
    '/': ["00100", "00100", "01000", "01000", "10000", "10000", "00000"],
    '>': ["00000", "01000", "01100", "01110", "01100", "01000", "00000"], # Menu Cursor
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '$': ["01000", "11100", "10100", "11100", "01100", "11100", "01000"], # Basic $
    '_': ["00000", "00000", "00000", "00000", "00000", "00000", "11111"], # Underscore
    # This is our fallback character if we don't have a specific one, purr!
    'UNKNOWN': ["11100", "10100", "10100", "10100", "10100", "10100", "11100"] # A little box
}
print("INFO: Using adorable custom pixel font, meow! So much fun!")


# --- Helper function to draw text with our pixel font ---
def draw_pixel_text(surface, text, start_x, start_y, color):
    current_x = start_x
    current_y = start_y
    char_actual_width = GB_PIXEL_FONT_CHAR_WIDTH # The visual width of the character glyph
    # char_advance_width is GB_PIXEL_FONT_DRAW_WIDTH (includes spacing)

    for char_code in text.upper(): # Make sure we use uppercase for lookup!
        char_grid = GB_PIXEL_FONT_DATA.get(char_code, GB_PIXEL_FONT_DATA['UNKNOWN'])
        
        for r_idx, row_str in enumerate(char_grid):
            for c_idx, pixel_val in enumerate(row_str):
                if pixel_val == '1':
                    pygame.draw.rect(surface, color,
                                     (current_x + c_idx,
                                      current_y + r_idx,
                                      1, 1)) # Each '1' is a 1x1 pixel on game_surface
        current_x += GB_PIXEL_FONT_DRAW_WIDTH
    return current_x # Return end x for any calculation needs

def get_pixel_text_width(text_content):
    return len(text_content) * GB_PIXEL_FONT_DRAW_WIDTH

# --- Sprite Grids (Remain the same definition-wise) ---
CHARMANDER_GRID = [ 
    "0000001111000000", "0000112222110000", "0001222112221000", "0012211111221000",
    "0122111111122100", "1121111111112210", "1121111121112210", "0121111222112100",
    "0112111222111100", "0011221111221100", "0011112222111000", "0001111111110000",
    "0000111001100000", "0000011001100000", "0000011001100000", "0000000000000000",
]
SQUIRTLE_GRID = [ 
    "0000011110000000", "0000122221000000", "0001221122100000", "0012211112210000",
    "0122111111221000", "1221111111122100", "1221111111122100", "0122222222221000",
    "0012222222211000", "0001222222210000", "0000112221100000", "0000011111000000",
    "0000001110000000", "0000011111000000", "0000110000110000", "0000000000000000",
]
CHARMANDER_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY}
SQUIRTLE_COLORS_GB = {1: GB_LIGHT, 2: GB_GRAY}

SPRITE_GRIDS = {
    "CHARMANDER": (CHARMANDER_GRID, CHARMANDER_COLORS_GB),
    "SQUIRTLE": (SQUIRTLE_GRID, SQUIRTLE_COLORS_GB),
}
SPRITE_CACHE = {}

def render_gb_sprite(grid, color_map, pixel_size=1, outline_color=GB_DARK):
    sprite_width = len(grid[0]) * pixel_size
    sprite_height = len(grid) * pixel_size
    surf = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    surf.fill((0,0,0,0)) 

    for y, row in enumerate(grid):
        for x, val_char in enumerate(row):
            val = int(val_char)
            if val == 0: continue
            color = color_map.get(val, GB_GRAY)
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(surf, color, rect)

    if outline_color:
        mask = pygame.mask.from_surface(surf, 127)
        outline_pixels = mask.outline()
        if outline_pixels:
            for point_x, point_y in outline_pixels:
                pygame.draw.rect(surf, outline_color, (point_x, point_y, pixel_size, pixel_size))
    return surf

def get_sprite_surface(name, pixel_size=1, outline_color=GB_DARK):
    key = (name, pixel_size, outline_color)
    if key in SPRITE_CACHE: return SPRITE_CACHE[key]
    
    grid_data = SPRITE_GRIDS.get(name)
    if not grid_data:
        print(f"ERROR: Sprite '{name}' not found! Oh noes! :( Returning a placeholder, purr.")
        placeholder = pygame.Surface((16*pixel_size, 16*pixel_size))
        placeholder.fill(GB_GRAY)
        pygame.draw.rect(placeholder, GB_DARK, placeholder.get_rect(),1)
        return placeholder

    grid, cmap = grid_data
    surf = render_gb_sprite(grid, cmap, pixel_size, outline_color)
    SPRITE_CACHE[key] = surf
    return surf

def blit_gb_sprite(dest_surface, x, y, name, gb_pixel_size=1, outline_color=GB_DARK):
    surf = get_sprite_surface(name, gb_pixel_size, outline_color)
    dest_surface.blit(surf, (x, y))

class PokemonInstance:
    def __init__(self, name, level, sprite_name, max_hp, attack, defense, speed, moves):
        self.name = name
        self.level = level
        self.sprite_name = sprite_name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves
        self.fainted = False
        self.attack_stage = 0
        self.defense_stage = 0

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.fainted = True
        return self.fainted

    def get_stat_modifier(self, stage): 
        multipliers = {-6:0.25,-5:0.28,-4:0.33,-3:0.40,-2:0.50,-1:0.66,0:1.0,1:1.5,2:2.0,3:2.5,4:3.0,5:3.5,6:4.0}
        return multipliers[stage]

    def get_effective_attack(self): return int(self.attack * self.get_stat_modifier(self.attack_stage))
    def get_effective_defense(self): return int(self.defense * self.get_stat_modifier(self.defense_stage))
    def change_attack_stage(self, amount): self.attack_stage = max(-6, min(6, self.attack_stage + amount))
    def change_defense_stage(self, amount): self.defense_stage = max(-6, min(6, self.defense_stage + amount))

MOVE_SCRATCH = {"name": "SCRATCH", "power": 40, "accuracy": 100, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_GROWL = {"name": "GROWL", "power": 0, "accuracy": 100, "pp": 40, "type": "Normal", "effect_type": "stat_change", "stat": "attack", "target": "enemy", "stages": -1}
MOVE_TACKLE = {"name": "TACKLE", "power": 35, "accuracy": 95, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_TAIL_WHIP = {"name": "TAIL WHIP", "power": 0, "accuracy": 100, "pp": 30, "type": "Normal", "effect_type": "stat_change", "stat": "defense", "target": "enemy", "stages": -1}

player_pokemon = PokemonInstance("CHARMANDER",5,"CHARMANDER",19,12,10,13,[MOVE_SCRATCH,MOVE_GROWL])
rival_pokemon = PokemonInstance("SQUIRTLE",5,"SQUIRTLE",20,11,13,11,[MOVE_TACKLE,MOVE_TAIL_WHIP])

SPRITE_GRID_DIM = 16
GB_SPRITE_PIXEL_SIZE = 1
PLAYER_SPRITE_X = 8
PLAYER_SPRITE_Y = GAMEBOY_HEIGHT - (SPRITE_GRID_DIM * GB_SPRITE_PIXEL_SIZE) - 48
RIVAL_SPRITE_X = GAMEBOY_WIDTH - (SPRITE_GRID_DIM * GB_SPRITE_PIXEL_SIZE) - 8
RIVAL_SPRITE_Y = 8

RIVAL_INFO_BOX_W, RIVAL_INFO_BOX_H = 76, 30
RIVAL_INFO_BOX = pygame.Rect(6, 6, RIVAL_INFO_BOX_W, RIVAL_INFO_BOX_H)
PLAYER_INFO_BOX_W, PLAYER_INFO_BOX_H = 76, 36
PLAYER_INFO_BOX_Y_OFFSET = 40
PLAYER_INFO_BOX = pygame.Rect(GAMEBOY_WIDTH - PLAYER_INFO_BOX_W - 6, GAMEBOY_HEIGHT - PLAYER_INFO_BOX_H - PLAYER_INFO_BOX_Y_OFFSET, PLAYER_INFO_BOX_W, PLAYER_INFO_BOX_H)
HP_BAR_W_INFOBOX = 48
HP_BAR_H_INFOBOX = 4
MESSAGE_BOX_H = 38
MESSAGE_BOX_RECT = pygame.Rect(4, GAMEBOY_HEIGHT - MESSAGE_BOX_H - 4, GAMEBOY_WIDTH - 8, MESSAGE_BOX_H)
ACTION_MENU_W, ACTION_MENU_H = 68, 36 # Adjusted for pixel font
ACTION_MENU_RECT = pygame.Rect(GAMEBOY_WIDTH - ACTION_MENU_W - 4, MESSAGE_BOX_RECT.y - ACTION_MENU_H - 2, ACTION_MENU_W, ACTION_MENU_H)
MOVE_MENU_Y_OFFSET = MESSAGE_BOX_RECT.y - 2

current_dialog_text = ""
battle_phase = "INTRO_1"
action_cursor_pos = 0
move_cursor_pos = 0
ACTION_MENU_ITEMS = ["FIGHT", "PKMN"]
selected_player_move = None
selected_enemy_move = None
UI_BORDER_COLOR = GB_DARK
UI_FILL_COLOR = GB_WHITE
UI_SHADOW_COLOR = GB_GRAY

def draw_gb_box(surface, rect, border_color=UI_BORDER_COLOR, fill_color=UI_FILL_COLOR, shadow_color=UI_SHADOW_COLOR, border_width=1, shadow_offset=1):
    if shadow_color:
        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(surface, shadow_color, shadow_rect)
    pygame.draw.rect(surface, fill_color, rect)
    pygame.draw.rect(surface, border_color, rect, border_width)

def display_dialog(text):
    global current_dialog_text
    current_dialog_text = text.upper() 

def draw_text_wrapped_pixel(surface, text, rect, color):
    # This is our new wrapped text function, meow! It's so clever!
    words = text.upper().split(' ')
    lines = []
    current_line = ""
    rect_inner_width = rect.width - 8 # Padding for text inside the box
    line_height_px = GB_PIXEL_FONT_DRAW_HEIGHT # Includes line spacing

    for word in words:
        test_line_candidate = current_line + word + " "
        # Calculate width using our pixel font's metrics, yay!
        if get_pixel_text_width(test_line_candidate.strip()) <= rect_inner_width:
            current_line = test_line_candidate
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    y_text_start = rect.y + 4 # Padding from top of box
    for i, line_text in enumerate(lines):
        if i >= 2: break # Max 2 lines for standard dialog
        draw_pixel_text(surface, line_text, rect.x + 4, y_text_start + (i * line_height_px), color)

def draw_info_box(surface, pokemon, rect, is_player_side):
    draw_gb_box(surface, rect)
    
    name_text_x = rect.x + 4
    name_text_y = rect.y + 2
    draw_pixel_text(surface, f"{pokemon.name.upper()}", name_text_x, name_text_y, GB_PIXEL_FONT_TEXT_COLOR)
    
    # Calculate width of name to position level text, so cute!
    name_width = get_pixel_text_width(pokemon.name.upper())
    level_text_x = name_text_x + name_width + 2 # Small space
    draw_pixel_text(surface, f":L{pokemon.level}", level_text_x, name_text_y + 1, GB_PIXEL_FONT_TEXT_COLOR)

    hp_label_text_x = rect.x + 6
    hp_label_text_y = rect.y + 12 
    draw_pixel_text(surface, "HP:", hp_label_text_x, hp_label_text_y, GB_PIXEL_FONT_TEXT_COLOR)
    hp_label_width = get_pixel_text_width("HP:")

    hp_bar_bg_rect = pygame.Rect(hp_label_text_x + hp_label_width + 2, hp_label_text_y + 1, HP_BAR_W_INFOBOX, HP_BAR_H_INFOBOX)
    pygame.draw.rect(surface, GB_LIGHT, hp_bar_bg_rect)
    
    hp_ratio = pokemon.current_hp / pokemon.max_hp
    current_hp_width = int(HP_BAR_W_INFOBOX * hp_ratio)
    current_hp_rect = pygame.Rect(hp_bar_bg_rect.x, hp_bar_bg_rect.y, current_hp_width, HP_BAR_H_INFOBOX)
    pygame.draw.rect(surface, GB_DARK, current_hp_rect)
    pygame.draw.rect(surface, GB_DARK, hp_bar_bg_rect, 1)

    if is_player_side:
        hp_val_str = f"{pokemon.current_hp: >3}/{pokemon.max_hp: >3}".replace(" ","0") # Pad with 0 for GB look
        hp_val_width = get_pixel_text_width(hp_val_str)
        hp_val_text_x = rect.x + rect.width - hp_val_width - 6 
        hp_val_text_y = rect.y + 12 + GB_PIXEL_FONT_DRAW_HEIGHT + 1 
        draw_pixel_text(surface, hp_val_str, hp_val_text_x, hp_val_text_y, GB_PIXEL_FONT_TEXT_COLOR)

def calculate_damage_cute(attacker, defender, move):
    if move["effect_type"] != "damage" or move["power"] == 0: return 0
    level_factor = ((attacker.level * 2 / 5) + 2)
    atk_stat = attacker.get_effective_attack()
    def_stat = max(1, defender.get_effective_defense())
    damage = (((level_factor * move["power"] * (atk_stat / def_stat)) / 50) + 2)
    random_mod = random.uniform(0.85, 1.0)
    final_damage = int(damage * random_mod)
    return max(1, final_damage) # Always a little boop of damage, purr!

def apply_stat_change_move(attacker, target, move):
    stat_to_change = move["stat"]
    stages = move["stages"]
    change_text = "ROSE" if stages > 0 else "FELL"
    prefix = f"{attacker.name.upper()} USED {move['name'].upper()}!"
    suffix = ""
    if stat_to_change == "attack":
        if (stages < 0 and target.attack_stage == -6) or (stages > 0 and target.attack_stage == 6):
            suffix = f"{target.name.upper()}'S ATTACK WON'T GO ANY {'HIGHER' if stages > 0 else 'LOWER'}!"
        else:
            target.change_attack_stage(stages); suffix = f"{target.name.upper()}'S ATTACK {change_text}!"
    elif stat_to_change == "defense":
        if (stages < 0 and target.defense_stage == -6) or (stages > 0 and target.defense_stage == 6):
            suffix = f"{target.name.upper()}'S DEFENSE WON'T GO ANY {'HIGHER' if stages > 0 else 'LOWER'}!"
        else:
            target.change_defense_stage(stages); suffix = f"{target.name.upper()}'S DEFENSE {change_text}!"
    display_dialog(f"{prefix} {suffix}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if current_dialog_text and event.key == pygame.K_z:
                current_dialog_text = ""
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
                elif battle_phase == "BATTLE_END_WIN" or battle_phase == "BATTLE_END_LOSE": running = False
            elif battle_phase == "ACTION_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: action_cursor_pos = (action_cursor_pos - 1) % len(ACTION_MENU_ITEMS)
                elif event.key == pygame.K_DOWN: action_cursor_pos = (action_cursor_pos + 1) % len(ACTION_MENU_ITEMS)
                elif event.key == pygame.K_z:
                    if ACTION_MENU_ITEMS[action_cursor_pos] == "FIGHT": battle_phase = "MOVE_SELECT"; move_cursor_pos = 0
                    elif ACTION_MENU_ITEMS[action_cursor_pos] == "PKMN": display_dialog("PKMN OPTION ISN'T CODED YET, NYA~!")
            elif battle_phase == "MOVE_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP: move_cursor_pos = (move_cursor_pos - 1) % len(player_pokemon.moves)
                elif event.key == pygame.K_DOWN: move_cursor_pos = (move_cursor_pos + 1) % len(player_pokemon.moves)
                elif event.key == pygame.K_x: battle_phase = "ACTION_SELECT"; action_cursor_pos = 0
                elif event.key == pygame.K_z: selected_player_move = player_pokemon.moves[move_cursor_pos]; battle_phase = "PLAYER_ATTACK_MSG"

    if not current_dialog_text:
        if battle_phase == "INTRO_1": display_dialog("RIVAL GARY WANTS TO FIGHT!")
        elif battle_phase == "INTRO_2": display_dialog(f"GARY SENT OUT {rival_pokemon.name.upper()}!")
        elif battle_phase == "INTRO_3": display_dialog(f"GO! {player_pokemon.name.upper()}!")
        elif battle_phase == "PLAYER_PROMPT": display_dialog(f"WHAT WILL {player_pokemon.name.upper()} DO?"); battle_phase = "ACTION_SELECT"; action_cursor_pos = 0
        elif battle_phase == "PLAYER_ATTACK_MSG": display_dialog(f"{player_pokemon.name.upper()} USED {selected_player_move['name'].upper()}!")
        elif battle_phase == "PLAYER_ATTACK_EFFECT":
            if selected_player_move["effect_type"] == "damage":
                damage = calculate_damage_cute(player_pokemon, rival_pokemon, selected_player_move)
                rival_pokemon.take_damage(damage); display_dialog(f"IT'S A HIT!"); battle_phase = "PLAYER_DAMAGE_MSG"
            elif selected_player_move["effect_type"] == "stat_change":
                apply_stat_change_move(player_pokemon, rival_pokemon, selected_player_move); battle_phase = "PLAYER_STAT_EFFECT_MSG"
        elif battle_phase == "ENEMY_FAINT_CHECK":
            if rival_pokemon.fainted: display_dialog(f"{rival_pokemon.name.upper()} FAINTED!"); battle_phase = "ENEMY_FAINT_MSG"
            else: selected_enemy_move = random.choice(rival_pokemon.moves); battle_phase = "ENEMY_ATTACK_MSG"
        elif battle_phase == "ENEMY_ATTACK_MSG": display_dialog(f"ENEMY {rival_pokemon.name.upper()} USED {selected_enemy_move['name'].upper()}!")
        elif battle_phase == "ENEMY_ATTACK_EFFECT":
            if selected_enemy_move["effect_type"] == "damage":
                damage = calculate_damage_cute(rival_pokemon, player_pokemon, selected_enemy_move)
                player_pokemon.take_damage(damage); display_dialog(f"OUCH! IT HIT YOUR POKEMON!"); battle_phase = "ENEMY_DAMAGE_MSG"
            elif selected_enemy_move["effect_type"] == "stat_change":
                apply_stat_change_move(rival_pokemon, player_pokemon, selected_enemy_move); battle_phase = "ENEMY_STAT_EFFECT_MSG"
        elif battle_phase == "PLAYER_FAINT_CHECK":
            if player_pokemon.fainted: display_dialog(f"{player_pokemon.name.upper()} FAINTED!"); battle_phase = "PLAYER_FAINT_MSG"
            else: battle_phase = "PLAYER_PROMPT"
        elif battle_phase == "BATTLE_END_WIN": display_dialog(f"PLAYER DEFEATED RIVAL GARY! YOU WON $200, MEOW!")
        elif battle_phase == "BATTLE_END_LOSE": display_dialog("PLAYER BLACKED OUT! OH NOES...😿")

    game_surface.fill(GB_WHITE)
    player_sprite_render_y = PLAYER_SPRITE_Y + (16 * GB_SPRITE_PIXEL_SIZE) / 4
    blit_gb_sprite(game_surface, PLAYER_SPRITE_X, player_sprite_render_y, player_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    rival_sprite_render_y = RIVAL_SPRITE_Y - (16*GB_SPRITE_PIXEL_SIZE) /8
    blit_gb_sprite(game_surface, RIVAL_SPRITE_X, rival_sprite_render_y, rival_pokemon.sprite_name, GB_SPRITE_PIXEL_SIZE)
    draw_info_box(game_surface, rival_pokemon, RIVAL_INFO_BOX, False)
    draw_info_box(game_surface, player_pokemon, PLAYER_INFO_BOX, True)
    
    if battle_phase == "ACTION_SELECT" and not current_dialog_text:
        draw_gb_box(game_surface, ACTION_MENU_RECT)
        item_y_offset = 4 
        for i, item in enumerate(ACTION_MENU_ITEMS):
            text_pos_x = ACTION_MENU_RECT.x + 12
            if i == action_cursor_pos:
                draw_pixel_text(game_surface, ">", ACTION_MENU_RECT.x + 4, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, item.upper(), text_pos_x, ACTION_MENU_RECT.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
    
    elif battle_phase == "MOVE_SELECT" and not current_dialog_text:
        max_move_name_width_px = 0
        for move in player_pokemon.moves:
            w = get_pixel_text_width(move["name"].upper())
            if w > max_move_name_width_px: max_move_name_width_px = w
        
        move_menu_w = max_move_name_width_px + 20 
        move_menu_h = len(player_pokemon.moves) * GB_PIXEL_FONT_DRAW_HEIGHT + 8 
        actual_move_menu_rect = pygame.Rect(4, MOVE_MENU_Y_OFFSET - move_menu_h, move_menu_w, move_menu_h)
        draw_gb_box(game_surface, actual_move_menu_rect)
        
        item_y_offset = 4
        for i, move in enumerate(player_pokemon.moves):
            text_pos_x = actual_move_menu_rect.x + 12
            if i == move_cursor_pos:
                draw_pixel_text(game_surface, ">", actual_move_menu_rect.x + 4, actual_move_menu_rect.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
            draw_pixel_text(game_surface, move["name"].upper(), text_pos_x, actual_move_menu_rect.y + item_y_offset + i * GB_PIXEL_FONT_DRAW_HEIGHT, GB_PIXEL_FONT_TEXT_COLOR)
    
    if current_dialog_text or battle_phase == "PLAYER_PROMPT":
        draw_gb_box(game_surface, MESSAGE_BOX_RECT)
        if current_dialog_text:
            draw_text_wrapped_pixel(game_surface, current_dialog_text, MESSAGE_BOX_RECT, GB_PIXEL_FONT_TEXT_COLOR)
            if pygame.time.get_ticks() // 400 % 2 == 0:
                indicator_x = MESSAGE_BOX_RECT.right - 8
                indicator_y = MESSAGE_BOX_RECT.bottom - 8
                pygame.draw.polygon(game_surface, GB_PIXEL_FONT_TEXT_COLOR, 
                                    [(indicator_x, indicator_y), (indicator_x + 3, indicator_y - 3), (indicator_x - 3, indicator_y - 3)]) # Smaller triangle

    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
