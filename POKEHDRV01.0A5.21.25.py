import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Red Engine - Rival Battle!")
font = pygame.font.SysFont('Consolas', 18) # A nice retro-ish font
font_small = pygame.font.SysFont('Consolas', 16)
clock = pygame.time.Clock()

# --- Color Definitions ---
GB_WHITE  = (232, 232, 232)
GB_LIGHT  = (180, 180, 180)
GB_GRAY   = (110, 110, 110)
GB_DARK   = (36, 36, 36)
GB_ORANGE = (254, 165, 61) # Charmander body
GB_BLUE   = (100, 180, 255) # Squirtle body
GB_BROWN  = (87, 47, 8)   # Shading/details
GB_BLACK  = (20, 20, 20)
HP_GREEN = (48, 200, 48)
HP_YELLOW = (248, 224, 48)
HP_RED = (248, 72, 56)


# --- Sprite Grids ---
CHARMANDER_GRID = [
    "0000001111000000",
    "0000111222110000",
    "0001112222211000",
    "0011122111221100",
    "0111121111121110",
    "1111111121111111",
    "1111111121111111",
    "0111111222111110",
    "0111111222111110",
    "0011111111111100",
    "0011111111111100",
    "0001111111111000",
    "0000111111110000",
    "0000011111100000",
    "0000001111000000",
    "0000000000000000",
]
SQUIRTLE_GRID = [
    "0000011221000000",
    "0001122222110000",
    "0011222222211000",
    "0112221122221100",
    "1122221112222111",
    "1222211122222211",
    "1222211112222211",
    "0122222222222210",
    "0122222222222210",
    "0012222222222100",
    "0012222222222100",
    "0001222222221000",
    "0000112222110000",
    "0000011111100000",
    "0000001111000000",
    "0000000000000000",
]
CHARMANDER_COLORS = {1: GB_ORANGE, 2: GB_BROWN}
SQUIRTLE_COLORS = {1: GB_BLUE, 2: GB_BROWN}

# --- Sprite Cache ---
SPRITE_GRIDS = {
    "CHARMANDER": (CHARMANDER_GRID, CHARMANDER_COLORS),
    "SQUIRTLE": (SQUIRTLE_GRID, SQUIRTLE_COLORS),
}
SPRITE_CACHE = {}

def render_gb_sprite(grid, color_map, pixel_size=6, outline=True):
    size = len(grid) * pixel_size
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            idx = int(val)
            if idx == 0:
                continue
            color = color_map.get(idx, GB_GRAY)
            rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(surf, color, rect)
    if outline:
        mask = pygame.mask.from_threshold(surf, (0,0,0,0), (1,1,1,255))
        outline_mask = mask.outline()
        if outline_mask: # Check if outline_mask is not empty
             # The thickness of 2 for outline might be a bit much for 6x scale, 1 might be better
            pygame.draw.lines(surf, GB_BLACK, True, outline_mask, 1) # Changed to 1 for finer outline
    return surf

def get_sprite_surface(name, pixel_size=6, outline=True):
    key = (name, pixel_size, outline)
    if key in SPRITE_CACHE:
        return SPRITE_CACHE[key]
    grid, cmap = SPRITE_GRIDS[name]
    surf = render_gb_sprite(grid, cmap, pixel_size, outline)
    SPRITE_CACHE[key] = surf
    return surf

def blit_gb_sprite(dest, x, y, name, pixel_size=6, outline=True):
    surf = get_sprite_surface(name, pixel_size, outline)
    dest.blit(surf, (x, y))

# --- Pokémon Data and Battle Logic ---
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
        self.moves = moves # List of move dictionaries
        self.fainted = False
        self.attack_stage = 0 # For Growl/Tail Whip effects
        self.defense_stage = 0 # For Growl/Tail Whip effects

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.fainted = True
        return self.fainted

    def get_stat_modifier(self, stage):
        if stage >= 0:
            return (2 + stage) / 2
        else:
            return 2 / (2 - stage)

    def get_effective_attack(self):
        return int(self.attack * self.get_stat_modifier(self.attack_stage))

    def get_effective_defense(self):
        return int(self.defense * self.get_stat_modifier(self.defense_stage))

    def change_attack_stage(self, amount):
        self.attack_stage += amount
        self.attack_stage = max(-6, min(6, self.attack_stage)) # Stages cap at -6 and +6

    def change_defense_stage(self, amount):
        self.defense_stage += amount
        self.defense_stage = max(-6, min(6, self.defense_stage))


MOVE_SCRATCH = {"name": "Scratch", "power": 40, "accuracy": 100, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_GROWL = {"name": "Growl", "power": 0, "accuracy": 100, "pp": 40, "type": "Normal", "effect_type": "stat_change", "stat": "attack", "target": "enemy", "stages": -1}
MOVE_TACKLE = {"name": "Tackle", "power": 40, "accuracy": 100, "pp": 35, "type": "Normal", "effect_type": "damage"}
MOVE_TAIL_WHIP = {"name": "Tail Whip", "power": 0, "accuracy": 100, "pp": 30, "type": "Normal", "effect_type": "stat_change", "stat": "defense", "target": "enemy", "stages": -1}

player_pokemon = PokemonInstance(
    name="CHARMANDER", level=5, sprite_name="CHARMANDER",
    max_hp=19, attack=12, defense=11, speed=13,
    moves=[MOVE_SCRATCH, MOVE_GROWL]
)

rival_pokemon = PokemonInstance(
    name="SQUIRTLE", level=5, sprite_name="SQUIRTLE",
    max_hp=20, attack=11, defense=13, speed=11,
    moves=[MOVE_TACKLE, MOVE_TAIL_WHIP]
)

# --- Battle UI and State ---
SPRITE_PIXEL_SIZE = 6
PLAYER_SPRITE_X = 40
PLAYER_SPRITE_Y = HEIGHT - (16 * SPRITE_PIXEL_SIZE) - 70  # 16 is sprite height, 70 is bottom margin
RIVAL_SPRITE_X = WIDTH - (16 * SPRITE_PIXEL_SIZE) - 40
RIVAL_SPRITE_Y = 30

HP_BAR_WIDTH = 100
HP_BAR_HEIGHT = 8

# Player info box (top left for opponent, bottom right for player)
RIVAL_INFO_BOX = pygame.Rect(20, 20, 180, 50)
PLAYER_INFO_BOX = pygame.Rect(WIDTH - 200, HEIGHT - 130, 180, 50)

MESSAGE_BOX_RECT = pygame.Rect(10, HEIGHT - 60, WIDTH - 20, 50)
ACTION_MENU_RECT = pygame.Rect(WIDTH - 160, HEIGHT - 60 - 85, 150, 80) # Above message box
MOVE_MENU_RECT = pygame.Rect(10, HEIGHT - 60 - 85, 150, 80) # Temp, dynamic later

current_dialog_text = ""
battle_phase = "INTRO_1" # INTRO_1, INTRO_2, INTRO_3, PLAYER_PROMPT, ACTION_SELECT, MOVE_SELECT, PLAYER_ATTACK_MSG, PLAYER_ATTACK_ANIM, ENEMY_FAINT_CHECK, ENEMY_ATTACK_MSG, ENEMY_ATTACK_ANIM, PLAYER_FAINT_CHECK, BATTLE_END
intro_message_idx = 0
action_cursor_pos = 0
move_cursor_pos = 0
ACTION_MENU_ITEMS = ["FIGHT", "PKMN"] # PKMN not implemented

selected_player_move = None
selected_enemy_move = None

def display_dialog(text):
    global current_dialog_text
    current_dialog_text = text

def draw_text_wrapped(surface, text, rect, font, color=GB_BLACK):
    words = [word.split(' ') for word in text.splitlines()] # Handle newlines
    space = font.size(' ')[0]
    max_width, max_height = rect.width - 10, rect.height - 10 # Padding
    x, y = rect.x + 5, rect.y + 5
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= rect.x + max_width:
                x = rect.x + 5 # Reset x
                y += word_height # Start on new line
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = rect.x + 5 # Reset x for new lines in original text
        y += word_height


def draw_info_box(surface, pokemon, rect, is_player_side):
    pygame.draw.rect(surface, GB_WHITE, rect)
    pygame.draw.rect(surface, GB_BLACK, rect, 2)
    
    name_text = font.render(f"{pokemon.name} Lv{pokemon.level}", True, GB_BLACK)
    surface.blit(name_text, (rect.x + 5, rect.y + 5))

    # HP Bar
    hp_bar_outline_rect = pygame.Rect(rect.x + 5, rect.y + 25, HP_BAR_WIDTH, HP_BAR_HEIGHT + 4) # Little border
    pygame.draw.rect(surface, GB_DARK, hp_bar_outline_rect, 1) # Outer border for HP bar
    
    hp_text = font_small.render("HP:", True, GB_BLACK) # Small "HP:" label
    surface.blit(hp_text, (rect.x + 8, rect.y + 26))

    hp_bar_inner_bg_rect = pygame.Rect(rect.x + 30, rect.y + 27, HP_BAR_WIDTH - 25 , HP_BAR_HEIGHT) # Actual bar BG
    pygame.draw.rect(surface, GB_GRAY, hp_bar_inner_bg_rect) # Background for the bar fill

    hp_ratio = pokemon.current_hp / pokemon.max_hp
    current_hp_width = int((HP_BAR_WIDTH - 25) * hp_ratio)
    hp_color = HP_GREEN
    if hp_ratio < 0.2: hp_color = HP_RED
    elif hp_ratio < 0.5: hp_color = HP_YELLOW
    
    current_hp_rect = pygame.Rect(rect.x + 30, rect.y + 27, current_hp_width, HP_BAR_HEIGHT)
    pygame.draw.rect(surface, hp_color, current_hp_rect)

    if is_player_side: # Show numerical HP for player
        hp_val_text = font_small.render(f"{pokemon.current_hp}/{pokemon.max_hp}", True, GB_BLACK)
        surface.blit(hp_val_text, (rect.x + 5 + HP_BAR_WIDTH - 20, rect.y + rect.height - 20))


def calculate_damage_cute(attacker, defender, move):
    if move["effect_type"] != "damage" or move["power"] == 0:
        return 0
    
    # Adorable Gen 1-ish formula! Nya~
    # ((2 * Level / 5 + 2) * Power * Atk/Def / 50 + 2) * Modifier
    level_factor = (2 * attacker.level / 5) + 2
    atk_stat = attacker.get_effective_attack()
    def_stat = defender.get_effective_defense()
    
    # Prevent division by zero if defense is somehow 0 after extreme stat drops
    if def_stat == 0: def_stat = 1

    damage = (((level_factor * move["power"] * (atk_stat / def_stat)) / 50) + 2)
    
    # Random modifier (0.85 to 1.0 in Gen 1)
    random_mod = random.uniform(0.85, 1.0)
    final_damage = int(damage * random_mod)
    
    return max(1, final_damage) # Always at least 1 damage, purr!

def apply_stat_change_move(attacker, target, move):
    stat_to_change = move["stat"]
    stages = move["stages"]
    change_text = "rose" if stages > 0 else "fell"
    
    if stat_to_change == "attack":
        if (stages < 0 and target.attack_stage == -6) or \
           (stages > 0 and target.attack_stage == 6):
            display_dialog(f"{target.name}'s Attack won't go any {'higher' if stages > 0 else 'lower'}!")
        else:
            target.change_attack_stage(stages)
            display_dialog(f"{attacker.name} used {move['name']}! {target.name}'s Attack {change_text}!")
    elif stat_to_change == "defense":
        if (stages < 0 and target.defense_stage == -6) or \
           (stages > 0 and target.defense_stage == 6):
            display_dialog(f"{target.name}'s Defense won't go any {'higher' if stages > 0 else 'lower'}!")
        else:
            target.change_defense_stage(stages)
            display_dialog(f"{attacker.name} used {move['name']}! {target.name}'s Defense {change_text}!")
    # Add other stats if needed (Speed, Special etc.)
    # For this battle, Attack and Defense are primary.

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Quick exit
                running = False

            if current_dialog_text and event.key == pygame.K_z: # 'A' button to advance dialog
                current_dialog_text = "" # Clear current dialog to proceed
                # --- State transitions after dialog dismissal ---
                if battle_phase == "INTRO_1": battle_phase = "INTRO_2"
                elif battle_phase == "INTRO_2": battle_phase = "INTRO_3"
                elif battle_phase == "INTRO_3": battle_phase = "PLAYER_PROMPT"
                elif battle_phase == "PLAYER_ATTACK_MSG": battle_phase = "PLAYER_ATTACK_EFFECT"
                elif battle_phase == "PLAYER_STAT_EFFECT_MSG": battle_phase = "ENEMY_FAINT_CHECK" # after player's status move
                elif battle_phase == "PLAYER_DAMAGE_MSG": battle_phase = "ENEMY_FAINT_CHECK"
                elif battle_phase == "ENEMY_FAINT_MSG": battle_phase = "BATTLE_END_WIN"
                elif battle_phase == "ENEMY_ATTACK_MSG": battle_phase = "ENEMY_ATTACK_EFFECT"
                elif battle_phase == "ENEMY_STAT_EFFECT_MSG": battle_phase = "PLAYER_FAINT_CHECK" # after enemy's status move
                elif battle_phase == "ENEMY_DAMAGE_MSG": battle_phase = "PLAYER_FAINT_CHECK"
                elif battle_phase == "PLAYER_FAINT_MSG": battle_phase = "BATTLE_END_LOSE"
                elif battle_phase == "BATTLE_END_WIN" or battle_phase == "BATTLE_END_LOSE":
                    running = False # End game after final message

            elif battle_phase == "ACTION_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP:
                    action_cursor_pos = (action_cursor_pos - 1) % len(ACTION_MENU_ITEMS)
                elif event.key == pygame.K_DOWN:
                    action_cursor_pos = (action_cursor_pos + 1) % len(ACTION_MENU_ITEMS)
                elif event.key == pygame.K_z: # Select action
                    if ACTION_MENU_ITEMS[action_cursor_pos] == "FIGHT":
                        battle_phase = "MOVE_SELECT"
                        move_cursor_pos = 0
                    elif ACTION_MENU_ITEMS[action_cursor_pos] == "PKMN":
                        display_dialog("Can't switch yet, nya~!") # Placeholder
                        # battle_phase = "PLAYER_PROMPT" # or stay in ACTION_SELECT
            
            elif battle_phase == "MOVE_SELECT" and not current_dialog_text:
                if event.key == pygame.K_UP:
                    move_cursor_pos = (move_cursor_pos - 1) % len(player_pokemon.moves)
                elif event.key == pygame.K_DOWN:
                    move_cursor_pos = (move_cursor_pos + 1) % len(player_pokemon.moves)
                elif event.key == pygame.K_x: # 'B' button to go back
                    battle_phase = "ACTION_SELECT"
                    action_cursor_pos = 0
                elif event.key == pygame.K_z: # Select move
                    selected_player_move = player_pokemon.moves[move_cursor_pos]
                    battle_phase = "PLAYER_ATTACK_MSG"

    # --- Battle Logic ---
    if not current_dialog_text: # Only process phases if no dialog is blocking
        if battle_phase == "INTRO_1":
            display_dialog("Rival GARY wants to fight!")
        elif battle_phase == "INTRO_2":
            display_dialog(f"GARY sent out {rival_pokemon.name}!")
        elif battle_phase == "INTRO_3":
            display_dialog(f"Go! {player_pokemon.name}!")
        elif battle_phase == "PLAYER_PROMPT":
            display_dialog(f"What will {player_pokemon.name} do?")
            battle_phase = "ACTION_SELECT" # Transition to show menu
            action_cursor_pos = 0
        
        # Player's Turn Logic
        elif battle_phase == "PLAYER_ATTACK_MSG":
            display_dialog(f"{player_pokemon.name} used {selected_player_move['name']}!")
            # Next state set by 'Z' press dismissing dialog

        elif battle_phase == "PLAYER_ATTACK_EFFECT":
            if selected_player_move["effect_type"] == "damage":
                damage = calculate_damage_cute(player_pokemon, rival_pokemon, selected_player_move)
                rival_pokemon.take_damage(damage)
                display_dialog(f"It's a hit! {rival_pokemon.name} took {damage} damage!")
                battle_phase = "PLAYER_DAMAGE_MSG" # Wait for Z press
            elif selected_player_move["effect_type"] == "stat_change":
                apply_stat_change_move(player_pokemon, rival_pokemon, selected_player_move)
                battle_phase = "PLAYER_STAT_EFFECT_MSG" # Dialog set by apply_stat_change_move
            # Next state (ENEMY_FAINT_CHECK) set by 'Z' press dismissing subsequent dialog

        elif battle_phase == "ENEMY_FAINT_CHECK":
            if rival_pokemon.fainted:
                display_dialog(f"{rival_pokemon.name} fainted!")
                battle_phase = "ENEMY_FAINT_MSG" # Wait for Z press
            else:
                # If enemy not fainted, proceed to enemy's turn
                selected_enemy_move = random.choice(rival_pokemon.moves) # Simple AI
                battle_phase = "ENEMY_ATTACK_MSG"

        # Enemy's Turn Logic
        elif battle_phase == "ENEMY_ATTACK_MSG":
            display_dialog(f"{rival_pokemon.name} used {selected_enemy_move['name']}!")
            # Next state set by 'Z' press

        elif battle_phase == "ENEMY_ATTACK_EFFECT":
            if selected_enemy_move["effect_type"] == "damage":
                damage = calculate_damage_cute(rival_pokemon, player_pokemon, selected_enemy_move)
                player_pokemon.take_damage(damage)
                display_dialog(f"Ouch! {player_pokemon.name} took {damage} damage!")
                battle_phase = "ENEMY_DAMAGE_MSG" # Wait for Z press
            elif selected_enemy_move["effect_type"] == "stat_change":
                apply_stat_change_move(rival_pokemon, player_pokemon, selected_enemy_move)
                battle_phase = "ENEMY_STAT_EFFECT_MSG" # Dialog set by apply_stat_change_move
            # Next state (PLAYER_FAINT_CHECK) set by 'Z' press

        elif battle_phase == "PLAYER_FAINT_CHECK":
            if player_pokemon.fainted:
                display_dialog(f"{player_pokemon.name} fainted!")
                battle_phase = "PLAYER_FAINT_MSG" # Wait for Z press
            else:
                # If player not fainted, back to player's turn prompt
                battle_phase = "PLAYER_PROMPT"
        
        # Battle End States
        elif battle_phase == "BATTLE_END_WIN":
            display_dialog("You defeated GARY! Yay! 🎉")
            # Next state set by Z press to end game
        elif battle_phase == "BATTLE_END_LOSE":
            display_dialog("Oh no! You lost to GARY...😿")
            # Next state set by Z press to end game


    # --- Drawing ---
    screen.fill(GB_WHITE)

    # Draw Pokémon Sprites
    blit_gb_sprite(screen, PLAYER_SPRITE_X, PLAYER_SPRITE_Y, player_pokemon.sprite_name, SPRITE_PIXEL_SIZE)
    blit_gb_sprite(screen, RIVAL_SPRITE_X, RIVAL_SPRITE_Y, rival_pokemon.sprite_name, SPRITE_PIXEL_SIZE)

    # Draw Info Boxes (HP bars are inside these)
    draw_info_box(screen, rival_pokemon, RIVAL_INFO_BOX, False)
    draw_info_box(screen, player_pokemon, PLAYER_INFO_BOX, True)
    
    # Draw Message Box and Dialog Text
    if current_dialog_text or battle_phase == "ACTION_SELECT" or battle_phase == "MOVE_SELECT":
        pygame.draw.rect(screen, GB_WHITE, MESSAGE_BOX_RECT)
        pygame.draw.rect(screen, GB_BLACK, MESSAGE_BOX_RECT, 2)
        if current_dialog_text:
            draw_text_wrapped(screen, current_dialog_text, MESSAGE_BOX_RECT, font)
            # Draw a little indicator to press Z
            if battle_phase not in ["ACTION_SELECT", "MOVE_SELECT"]: # Don't show if menu is up
                indicator_x = MESSAGE_BOX_RECT.right - 15
                indicator_y = MESSAGE_BOX_RECT.bottom - 15
                pygame.draw.polygon(screen, GB_BLACK, [(indicator_x, indicator_y), (indicator_x + 5, indicator_y - 5), (indicator_x + 10, indicator_y)])


    # Draw Action Menu
    if battle_phase == "ACTION_SELECT" and not current_dialog_text :
        pygame.draw.rect(screen, GB_WHITE, ACTION_MENU_RECT)
        pygame.draw.rect(screen, GB_BLACK, ACTION_MENU_RECT, 2)
        for i, item in enumerate(ACTION_MENU_ITEMS):
            text_surf = font.render(item, True, GB_BLACK)
            text_pos_x = ACTION_MENU_RECT.x + 20
            if i == action_cursor_pos:
                cursor_surf = font.render(">", True, GB_BLACK)
                screen.blit(cursor_surf, (ACTION_MENU_RECT.x + 5, ACTION_MENU_RECT.y + 10 + i * 30))
            screen.blit(text_surf, (text_pos_x, ACTION_MENU_RECT.y + 10 + i * 30))

    # Draw Move Menu
    if battle_phase == "MOVE_SELECT" and not current_dialog_text:
        # Dynamic move menu box
        max_move_name_width = 0
        for move in player_pokemon.moves:
            w, _ = font.size(move["name"])
            if w > max_move_name_width: max_move_name_width = w
        
        move_menu_w = max_move_name_width + 40 # padding
        move_menu_h = len(player_pokemon.moves) * 25 + 15 # padding
        
        actual_move_menu_rect = pygame.Rect(10, HEIGHT - 60 - move_menu_h - 5, move_menu_w, move_menu_h)

        pygame.draw.rect(screen, GB_WHITE, actual_move_menu_rect)
        pygame.draw.rect(screen, GB_BLACK, actual_move_menu_rect, 2)
        for i, move in enumerate(player_pokemon.moves):
            text_surf = font.render(move["name"], True, GB_BLACK)
            text_pos_x = actual_move_menu_rect.x + 20
            if i == move_cursor_pos:
                cursor_surf = font.render(">", True, GB_BLACK)
                screen.blit(cursor_surf, (actual_move_menu_rect.x + 5, actual_move_menu_rect.y + 5 + i * 25))
            screen.blit(text_surf, (text_pos_x, actual_move_menu_rect.y + 5 + i * 25))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
