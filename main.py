"""
Mô đun thực thi chính (Entry Point) của ứng dụng trò chơi.
Quản lý vòng lặp hệ thống, khởi tạo môi trường, điều phối các pha (phases) của trận đấu,
và xử lý Cỗ máy trạng thái (State Machine) bao gồm Menu chính, Chế độ Online và Màn hình Chơi.
"""
import pygame, sys, os, random, copy
from constants import *
from network import GameNetwork

os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '2'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("ELEMENTAL CARD WARS")

from engine import GameEngine
import ui
from animations import AnimationManager
from models import Player, Board
from card_data import (
    FIRE_MONSTERS, WATER_MONSTERS, LIGHTNING_MONSTERS, WIND_MONSTERS, EARTH_MONSTERS, 
    FIRE_SPELLS, WATER_SPELLS, LIGHTNING_SPELLS, WIND_SPELLS, EARTH_SPELLS, ENVIRONMENT_CARDS
)

def build_custom_deck():
    """
    Tạo và cấu hình một bộ bài hoàn chỉnh ngẫu nhiên cho người chơi, 
    đảm bảo sự cân bằng về số lượng giữa các nguyên tố và loại thẻ bài.
    """
    deck = []
    deck.extend([copy.copy(c) for c in random.sample(FIRE_MONSTERS, 6)])
    deck.extend([copy.copy(c) for c in random.sample(WATER_MONSTERS, 6)])
    deck.extend([copy.copy(c) for c in random.sample(LIGHTNING_MONSTERS, 6)])
    deck.extend([copy.copy(c) for c in random.sample(WIND_MONSTERS, 6)])
    deck.extend([copy.copy(c) for c in random.sample(EARTH_MONSTERS, 6)])
    for env in ENVIRONMENT_CARDS:
        for _ in range(4): deck.append(copy.copy(env))
        
    spell_pools = [FIRE_SPELLS, WATER_SPELLS, LIGHTNING_SPELLS, WIND_SPELLS, EARTH_SPELLS]
    for pool in spell_pools:
        deck.extend([copy.copy(c) for c in random.sample(pool, 3)])
        
    random.shuffle(deck)
    return deck

def clone_board(original_board):
    """
    Sao chép sâu (deep copy) trạng thái bàn cờ hiện tại. 
    Hỗ trợ cơ chế dự đoán trạng thái và phân tách dữ liệu đồ họa (display_board) khỏi dữ liệu logic cốt lõi.
    """
    new_board = Board()
    new_board.player_slots = [copy.copy(card) if card else None for card in original_board.player_slots]
    new_board.bot_slots = [copy.copy(card) if card else None for card in original_board.bot_slots]
    new_board.player_env = list(original_board.player_env)
    new_board.bot_env = list(original_board.bot_env)
    return new_board

def queue_card_draw(card, side, hand_len):
    """
    Tính toán quỹ đạo và lưu trữ thông tin cần thiết để khởi tạo hiệu ứng Rút bài (Draw Card animation) 
    từ bộ bài (Deck) về tay người chơi (Hand).
    """
    if side == 'PLAYER':
        start_pos = (WIDTH - 348, HEIGHT - 118)
        end_pos = ((WIDTH - (hand_len * 120 + 130)) // 2 + hand_len * 120, 920)
    else:
        start_pos = (436, 60)
        end_pos = ((WIDTH - (hand_len * 120 + 130)) // 2 + hand_len * 120, -60)
    return {'card': card, 'side': side, 'start': start_pos, 'end': end_pos, 'prog': 0.0}

def process_board_deaths(board, player, bot, anim):
    """
    Quét liên tục trạng thái trên bàn cờ để phát hiện các thực thể có HP <= 0.
    Kích hoạt hoạt ảnh tan biến (Death animation) và xử lý việc di chuyển thẻ bài vào Mộ bài (Graveyard).
    Trả về cờ (boolean) báo hiệu xem có đang xử lý hoạt ảnh tan biến nào không.
    """
    animating = False
    for i in range(4):
        c_p = board.player_slots[i]
        if c_p and c_p.current_hp <= 0:
            if f'p{i}' not in anim.death_anims and not getattr(c_p, 'dying', False):
                anim.start_death(f'p{i}'); c_p.dying = True; animating = True
            elif f'p{i}' in anim.death_anims: animating = True
            elif getattr(c_p, 'dying', False):
                player.graveyard.append(c_p); board.player_slots[i] = None

        c_b = board.bot_slots[i]
        if c_b and c_b.current_hp <= 0:
            if f'b{i}' not in anim.death_anims and not getattr(c_b, 'dying', False):
                anim.start_death(f'b{i}'); c_b.dying = True; animating = True
            elif f'b{i}' in anim.death_anims: animating = True
            elif getattr(c_b, 'dying', False):
                bot.graveyard.append(c_b); board.bot_slots[i] = None
    return animating

def menu_state(clock):
    """
    Quản lý vòng lặp sự kiện và kết xuất đồ họa cho màn hình Menu chính (Main Menu).
    Xử lý các thao tác điều hướng sang chế độ chơi Solo, trực tuyến (Online), hoặc Thoát ứng dụng.
    """
    try: bg_menu = pygame.transform.scale(pygame.image.load('assets/menu_bg.png').convert(), (WIDTH, HEIGHT))
    except: bg_menu = None
    
    BTN_W, BTN_H = 600, 140 
    def load_btn_img(path):
        try: return pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(), (BTN_W, BTN_H))
        except: 
            surf = pygame.Surface((BTN_W, BTN_H)); surf.fill((150, 50, 50))
            return surf

    img_s_n = load_btn_img('assets/solo_normal.png')
    img_s_h = load_btn_img('assets/solo_hover.png')
    img_o_n = load_btn_img('assets/online_normal.png')
    img_o_h = load_btn_img('assets/online_hover.png')
    img_q_n = load_btn_img('assets/quit_normal.png')
    img_q_h = load_btn_img('assets/quit_hover.png')
    
    start_x = WIDTH // 2 - (BTN_W // 2)
    solo_r = pygame.Rect(start_x, 480, BTN_W, BTN_H)
    onl_r  = pygame.Rect(start_x, 630, BTN_W, BTN_H)
    quit_r = pygame.Rect(start_x, 780, BTN_W, BTN_H)
    
    while True:
        mx, my = pygame.mouse.get_pos()
        if bg_menu: screen.blit(bg_menu, (0, 0))
        else: screen.fill((10, 12, 18))
        
        try: screen.blit(img_s_h if solo_r.collidepoint(mx, my) else img_s_n, solo_r.topleft)
        except: pass
        try: screen.blit(img_o_h if onl_r.collidepoint(mx, my) else img_o_n, onl_r.topleft)
        except: pass
        try: screen.blit(img_q_h if quit_r.collidepoint(mx, my) else img_q_n, quit_r.topleft)
        except: pass
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "QUIT", None
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if solo_r.collidepoint(mx, my): return "PLAYING", None
                if onl_r.collidepoint(mx, my): return "ONLINE_MENU", None
                if quit_r.collidepoint(mx, my): return "QUIT", None
        pygame.display.flip(); clock.tick(FPS)

def online_menu_state(clock):
    """
    Quản lý vòng lặp tương tác cho Chế độ trực tuyến (Online Multiplayer).
    Cho phép nhập IP cấu hình kết nối mạng thông qua TCP socket (Đóng vai trò Host hoặc Client).
    """
    font_sys = pygame.font.SysFont("Verdana", 40, bold=True)
    try: font_ip = pygame.font.Font("assets/FrizQuadrata.ttf", 32)
    except: font_ip = pygame.font.SysFont("Arial", 32, bold=True)
    
    try: bg_online = pygame.transform.scale(pygame.image.load('assets/menu_online.png').convert(), (WIDTH, HEIGHT))
    except: bg_online = None

    def load_btn(name, w, h):
        try: return pygame.transform.smoothscale(pygame.image.load(f'assets/{name}.png').convert_alpha(), (w, h))
        except: 
            s = pygame.Surface((w, h)); s.fill((150, 50, 50))
            return s

    host_n = load_btn('hostgame_normal', 400, 80)
    host_h = load_btn('hostgame_hover', 400, 80)
    join_n = load_btn('joingame_normal', 400, 80)
    join_h = load_btn('joingame_hover', 400, 80)
    back_n = load_btn('back_normal', 150, 60)
    back_h = load_btn('back_hover', 150, 60)
    
    ip_text = ""
    input_active = False
    net = GameNetwork()
    
    while True:
        mx, my = pygame.mouse.get_pos()
        if bg_online: screen.blit(bg_online, (0, 0))
        else: screen.fill((15, 20, 30))
        
        host_r = pygame.Rect(WIDTH//2 - 200, 350, 400, 80)
        screen.blit(host_h if host_r.collidepoint(mx, my) else host_n, host_r.topleft)
        
        join_r = pygame.Rect(WIDTH//2 - 200, 480, 400, 80)
        screen.blit(join_h if join_r.collidepoint(mx, my) else join_n, join_r.topleft)
        
        input_r = pygame.Rect(WIDTH//2 - 200, 580, 400, 60)
        pygame.draw.rect(screen, (30, 40, 50), input_r, 0, 10)
        pygame.draw.rect(screen, (200,200,200) if input_active else (100,100,100), input_r, 2, 10)
        
        COLOR_TEXT = (231, 215, 165)
        COLOR_OUTLINE = (58, 43, 26)
        blink_cursor = "|" if input_active and (pygame.time.get_ticks() % 1000 < 500) else ""
        display_text = ip_text + blink_cursor if ip_text or input_active else "Enter Host IP ..."
        ui.draw_text_with_outline(screen, display_text, font_ip, COLOR_TEXT, COLOR_OUTLINE, input_r, y_offset=2)
        
        back_r = pygame.Rect(50, 50, 150, 60)
        screen.blit(back_h if back_r.collidepoint(mx, my) else back_n, back_r.topleft)
        
        if net.is_host and not net.connected:
            ui.draw_text_centered(screen, "Waiting for opponent...", font_sys, (255, 255, 0), (0, 700, WIDTH, 50))
            
        if net.connected:
            return "PLAYING", net

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "QUIT", None
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if back_r.collidepoint(mx, my): return "MENU", None
                if input_r.collidepoint(mx, my): input_active = True
                else: input_active = False
                
                if host_r.collidepoint(mx, my) and not net.is_host:
                    net.host_game()
                if join_r.collidepoint(mx, my) and ip_text:
                    success = net.join_game(ip_text.strip())
                    if not success: ip_text = "Connection Failed"
                    
            if e.type == pygame.KEYDOWN and input_active:
                if ip_text == "Connection Failed": ip_text = ""
                if e.key == pygame.K_RETURN: pass
                elif e.key == pygame.K_BACKSPACE: ip_text = ip_text[:-1]
                else: ip_text += e.unicode

        pygame.display.flip(); clock.tick(FPS)

def play_state(clock, net=None):
    """
    Vòng lặp nghiệp vụ chính (Main Game Loop).
    Quản lý luồng thực thi liên tục thông qua Cỗ máy trạng thái trận đấu (Game Phases) bao gồm: 
    Rút bài đầu game (INIT_DRAW), Người chơi bố trí (PLAYER_SETUP), 
    Máy bố trí (BOT_SETUP), Tiết lộ hành động (REVEAL), Giao tranh (BATTLE) và Dọn dẹp (CLEANUP).
    Xử lý đồng bộ hóa logic Engine và hệ thống UI/Animation.
    """
    anim = AnimationManager()
    main_surface = pygame.Surface((WIDTH, HEIGHT))
    
    if net and net.is_host:
        p_deck, b_deck = build_custom_deck(), build_custom_deck()
        net.send_data({'type': 'init_decks', 'p1': p_deck, 'p2': b_deck})
        player, bot = Player(p_deck), Player(b_deck)
    elif net and not net.is_host:
        player, bot = Player([]), Player([])
        waiting_decks = True
        while waiting_decks:
            data = net.get_data()
            if data and data.get('type') == 'init_decks':
                player.deck = data['p2']
                bot.deck = data['p1'] 
                waiting_decks = False
    else:
        player, bot = Player(build_custom_deck()), Player(build_custom_deck())
        
    board = Board()
    player.pending_spells, bot.pending_spells = [], [] 
    display_board = clone_board(board) 

    fonts = {'small': pygame.font.SysFont("Verdana", 18, bold=True), 'large': pygame.font.SysFont("Verdana", 32, bold=True), 'huge': pygame.font.SysFont("Verdana", 80, bold=True)}
    try: fonts['hp'] = pygame.font.Font("assets/FrizQuadrata.ttf", 32)
    except: fonts['hp'] = pygame.font.SysFont("Arial", 32, bold=True)
    
    ICONS = {}
    for el in ui.ALL_ELEMENTS:
        try:
            if os.path.exists(f'assets/{el.lower()}.png'): ICONS[el.lower()] = pygame.image.load(f'assets/{el.lower()}.png').convert_alpha()
            else: ICONS[el.lower()] = pygame.image.load(f'cards_list/element_icon/{el.lower()}.png').convert_alpha()
        except: 
            t = pygame.Surface((30, 30)); t.fill((100,100,100)); ICONS[el.lower()] = t

    try:
        bg_img = pygame.transform.scale(pygame.image.load('assets/background.png').convert(), (WIDTH, HEIGHT))
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.fill((0, 0, 0)); overlay.set_alpha(100); bg_img.blit(overlay, (0,0))
    except: bg_img = None

    ui_state = {
        'inspecting': None, 'selected_idx': -1, 'show_menu_idx': -1, 'is_targeting': False, 
        'viewing_grave': None, 'revival_card': None, 'is_discarding': False,
        'draw_queue': [], 'current_draw': None, 'spell_anim': None, 'setup_anim': None,
        'hover_offsets': {}, 'endgame_scale': 0.0, 'grave_scale': 0.0
    }

    game_phase = "INIT_DRAW"
    player_actions_queue, bot_actions_queue, reveal_queue = [], [], []
    init_draw_count, hex_center = 0, (WIDTH - 420, 625)
    combat_state = {'slot': 0, 'step': 0, 'timer': 0, 'order': []}
    action_timer = endgame_timer = 0

    while True:
        curr_time = pygame.time.get_ticks(); mx, my = pygame.mouse.get_pos()
        ui.draw_background(main_surface, bg_img)
        
        if player.display_hp > player.hp:
            player.display_hp -= max(0.2, (player.display_hp - player.hp) * 0.05)
        elif player.display_hp < player.hp: player.display_hp = player.hp
        
        if bot.display_hp > bot.hp:
            bot.display_hp -= max(0.2, (bot.display_hp - bot.hp) * 0.05)
        elif bot.display_hp < bot.hp: bot.display_hp = bot.hp

        impacts = anim.update()
        for atk_ent, def_ent in impacts:
            anim.start_entity_shake(atk_ent, 15, 8)
            if def_ent: anim.start_entity_shake(def_ent, 15, 8)

        if game_phase not in ["ENDGAME", "INIT_DRAW"] and (player.hp <= 0 or bot.hp <= 0):
            game_phase = "ENDGAME"; endgame_timer = curr_time
            ui_state['endgame_scale'] = 0.0

        if ui_state['current_draw']:
            d = ui_state['current_draw']; d['prog'] += 0.04
            if d['prog'] >= 1.0:
                if d['side'] == 'PLAYER': player.hand.append(d['card'])
                else: bot.hand.append(d['card'])
                ui_state['current_draw'] = None
        elif ui_state['draw_queue']: ui_state['current_draw'] = ui_state['draw_queue'].pop(0)

        if net:
            net_data = net.get_data()
            if net_data:
                if net_data['type'] == 'turn_actions' and game_phase == "WAITING_OPPONENT":
                    bot_actions_queue = net_data['actions']
                    for a in bot_actions_queue:
                        a["side"] = "BOT"
                        if "target_side" in a:
                            if a["target_side"] == "BOT": a["target_side"] = "PLAYER"
                            elif a["target_side"] == "PLAYER": a["target_side"] = "BOT"
                            
                    reveal_queue = player_actions_queue + bot_actions_queue
                    
                    for a in reveal_queue[:]:
                        if a["type"] == "SUMMON":
                            side_char = 'p' if a.get("side", "PLAYER") == "PLAYER" else 'b'
                            t_idx = a["target"]
                            if side_char == 'p': board.player_slots[t_idx] = a["card"]
                            else: board.bot_slots[t_idx] = a["card"]
                            anim.start_summon(f'{side_char}{t_idx}')
                            reveal_queue.remove(a)
                            
                    game_phase = "REVEAL"; action_timer = curr_time
                    display_board = clone_board(board)

        if game_phase == "ENDGAME":
            if ui_state.get('endgame_scale', 0.0) < 1.0:
                ui_state['endgame_scale'] = min(1.0, ui_state.get('endgame_scale', 0.0) + 0.04)

            ui.draw_endgame_screen(main_surface, bot.hp <= 0, fonts, ui_state.get('endgame_scale', 1.0))
            screen.blit(main_surface, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    if net: net.close()
                    return "QUIT"
                if event.type == pygame.MOUSEBUTTONDOWN and curr_time - endgame_timer > 1500: 
                    if net: net.close()
                    return "MENU"
            pygame.display.flip(); clock.tick(FPS); continue 

        elif game_phase == "INIT_DRAW":
            if init_draw_count < 5:
                c1, c2 = player.draw_card(), bot.draw_card()
                if c1: ui_state['draw_queue'].append(queue_card_draw(c1, 'PLAYER', init_draw_count))
                if c2: ui_state['draw_queue'].append(queue_card_draw(c2, 'BOT', init_draw_count))
                init_draw_count += 1
            elif not ui_state['draw_queue'] and not ui_state['current_draw']:
                game_phase = "PLAYER_SETUP"; display_board = clone_board(board)
                
        elif game_phase == "PLAYER_SETUP" and ui_state['setup_anim']:
            ui_state['setup_anim']['prog'] += 0.02 
            if ui_state['setup_anim']['prog'] >= 1.0:
                action = ui_state['setup_anim']['action']
                player_actions_queue.append(action)
                if action["type"] == "ENV":
                    display_board.player_env[action["target"]] = action["card"].element
                    player.env_milestones[action["card"].element] = min(4, player.env_milestones[action["card"].element]+1)
                ui_state['setup_anim'] = None

        elif game_phase == "BOT_SETUP":
            if net:
                net.send_data({'type': 'turn_actions', 'actions': player_actions_queue})
                game_phase = "WAITING_OPPONENT"
            else:
                bot_actions_queue = GameEngine.bot_ai_turn(bot, board)
                for a in bot_actions_queue: a["side"] = "BOT"
                reveal_queue = player_actions_queue + bot_actions_queue
                
                for a in reveal_queue[:]:
                    if a["type"] == "SUMMON":
                        side_char = 'p' if a.get("side", "PLAYER") == "PLAYER" else 'b'
                        t_idx = a["target"]
                        if side_char == 'p': board.player_slots[t_idx] = a["card"]
                        else: board.bot_slots[t_idx] = a["card"]
                        anim.start_summon(f'{side_char}{t_idx}')
                        reveal_queue.remove(a)
                        
                game_phase = "REVEAL"; action_timer = curr_time
                display_board = clone_board(board)

        elif game_phase == "WAITING_OPPONENT":
            ui.draw_text_centered(main_surface, "WAITING FOR OPPONENT...", fonts['large'], (255, 255, 0), (WIDTH//2 - 250, 150, 500, 50))

        elif game_phase == "REVEAL":
            if ui_state['spell_anim']:
                ui_state['spell_anim']['prog'] += 0.01 
                if ui_state['spell_anim']['prog'] >= 1.0:
                    action = ui_state['spell_anim']['action']
                    t_idx = action.get("target")
                    c_side = action.get("side")
                    
                    if action["type"] == "SPELL":
                        c_player = player if c_side == "PLAYER" else bot
                        e_player = bot if c_side == "PLAYER" else player
                        t_card = None
                        if t_idx is not None:
                            t_card = board.player_slots[t_idx] if action.get("target_side") == "PLAYER" else board.bot_slots[t_idx]
                            
                        GameEngine.execute_spell(action["card"], target_card=t_card, caster_player=c_player, enemy_player=e_player, board=board, caster_side=c_side)
                        
                        if "revived_card" in action:
                            if c_side == "PLAYER": board.player_slots[t_idx] = action["revived_card"]
                            else: board.bot_slots[t_idx] = action["revived_card"]
                            action["revived_card"].current_hp = max(1, int(action["revived_card"].stat_hp * 0.4))
                            
                        c = action["card"]
                        if c_side == "PLAYER" and c in player.pending_spells:
                            player.pending_spells.remove(c); player.graveyard.append(c)
                        elif c_side == "BOT" and c in bot.pending_spells:
                            bot.pending_spells.remove(c); bot.graveyard.append(c)
                    
                    elif action["type"] == "ENV" and c_side == "BOT":
                        old_env = board.bot_env[t_idx]
                        if old_env: bot.env_milestones[old_env] = max(0, bot.env_milestones[old_env]-1)
                        board.bot_env[t_idx] = action["card"].element
                        bot.env_milestones[action["card"].element] = min(4, bot.env_milestones.get(action["card"].element, 0)+1)
                        anim.start_flash(f'b{t_idx}')
                        c = action["card"]
                        if c in bot.pending_spells:
                            bot.pending_spells.remove(c); bot.graveyard.append(c)

                    process_board_deaths(board, player, bot, anim)
                    ui_state['spell_anim'] = None; display_board = clone_board(board); action_timer = curr_time

            elif not process_board_deaths(board, player, bot, anim):
                if curr_time - action_timer > 600:
                    if reveal_queue:
                        action = reveal_queue.pop(0)
                        
                        if net:
                            side_char = 'p' if action in player_actions_queue else 'b'
                            if side_char == 'b':
                                if action.get("target_side") == "BOT": action["target_side"] = "PLAYER"
                                elif action.get("target_side") == "PLAYER": action["target_side"] = "BOT"
                        else:
                            side_char = 'p' if action.get("side") == "PLAYER" or action in player_actions_queue else 'b'
                            
                        action["side"] = "PLAYER" if side_char == 'p' else "BOT"

                        if action["type"] == "ENV" and side_char == 'p':
                            board.player_env[action["target"]] = action["card"].element
                            c = action["card"]
                            if c in player.pending_spells:
                                player.pending_spells.remove(c)
                                player.graveyard.append(c)
                            action_timer = curr_time
                            
                        elif action["type"] == "ENV" and side_char == 'b':
                            ui_state['spell_anim'] = {'card': action['card'], 'prog': 0, 'action': action}

                        elif action["type"] == "SPELL":
                            ui_state['spell_anim'] = {'card': action['card'], 'prog': 0, 'action': action}
                            
                        display_board = clone_board(board) 
                    else:
                        game_phase = "BATTLE"; combat_state = {'slot': 0, 'step': 0, 'timer': curr_time, 'order': []}
            else:
                display_board = clone_board(board) 

        elif game_phase == "BATTLE":
            if not process_board_deaths(board, player, bot, anim):
                if curr_time - combat_state['timer'] > 800:
                    slot = combat_state['slot']
                    if slot > 3: game_phase = "CLEANUP"
                    else:
                        p_card, b_card = board.player_slots[slot], board.bot_slots[slot]
                        if not p_card and not b_card: combat_state['slot'] += 1; combat_state['timer'] = curr_time
                        else:
                            if combat_state['step'] == 0:
                                p_stats = GameEngine.calculate_stats(p_card, board.player_env[slot], player.env_milestones) if p_card else None
                                b_stats = GameEngine.calculate_stats(b_card, board.bot_env[slot], bot.env_milestones) if b_card else None
                                if p_card and b_card:
                                    if p_stats['spd'] >= b_stats['spd']: combat_state['order'] = [('p', p_card, p_stats, b_card, b_stats), ('b', b_card, b_stats, p_card, p_stats)]
                                    else: combat_state['order'] = [('b', b_card, b_stats, p_card, p_stats), ('p', p_card, p_stats, b_card, b_stats)]
                                elif p_card: combat_state['order'] = [('p_direct', p_card, p_stats)]
                                elif b_card: combat_state['order'] = [('b_direct', b_card, b_stats)]
                                combat_state['step'] = 1

                            if combat_state['step'] > 0:
                                idx = combat_state['step'] - 1
                                if idx < len(combat_state['order']):
                                    atk_data = combat_state['order'][idx]
                                    if "direct" not in atk_data[0] and getattr(atk_data[1], 'dying', False): pass 
                                    else:
                                        if atk_data[0] in ['p', 'b']:
                                            atk_c, atk_s, def_c, def_s = atk_data[1], atk_data[2], atk_data[3], atk_data[4]
                                            dmg, is_crit, is_miss = GameEngine.execute_combat(atk_c, def_c, atk_s, def_s)
                                            def_c.current_hp -= dmg
                                            anim.start_attack_bump(f'{atk_data[0]}{slot}', f'{"b" if atk_data[0]=="p" else "p"}{slot}', -1 if atk_data[0]=='p' else 1)
                                        elif atk_data[0] == 'p_direct':
                                            bot.hp -= atk_data[2]['atk']; anim.start_attack_bump(f'p{slot}', None, -1)
                                            anim.start_global_shake(20, 15, flash_red=False)
                                        elif atk_data[0] == 'b_direct':
                                            player.hp -= atk_data[2]['atk']; anim.start_attack_bump(f'b{slot}', None, 1)
                                            anim.start_global_shake(20, 15, flash_red=True)
                                    combat_state['step'] += 1; combat_state['timer'] = curr_time
                                else:
                                    combat_state['slot'] += 1; combat_state['step'] = 0; combat_state['timer'] = curr_time
            display_board = clone_board(board)

        elif game_phase == "CLEANUP":
            if not process_board_deaths(board, player, bot, anim):
                c_p, c_b = player.draw_card(), bot.draw_card()
                if c_p: ui_state['draw_queue'].append(queue_card_draw(c_p, 'PLAYER', len(player.hand)))
                if c_b: ui_state['draw_queue'].append(queue_card_draw(c_b, 'BOT', len(bot.hand)))
                
                if len(player.hand) > 6: ui_state['is_discarding'] = True
                if len(bot.hand) > 6: bot.graveyard.append(bot.hand.pop(random.randint(0, len(bot.hand)-1)))
                
                player_actions_queue.clear(); bot_actions_queue.clear()
                display_board = clone_board(board); game_phase = "WAIT_CLEANUP_DRAW"

        elif game_phase == "WAIT_CLEANUP_DRAW":
            if not ui_state['draw_queue'] and not ui_state['current_draw']: game_phase = "PLAYER_SETUP"

        attacking_entity = None
        if game_phase == "BATTLE" and combat_state['step'] > 0:
            idx = combat_state['step'] - 1
            if idx < len(combat_state['order']):
                atk_data = combat_state['order'][idx]
                slot = combat_state['slot']
                if atk_data[0] in ['p', 'p_direct']: attacking_entity = f'p{slot}'
                elif atk_data[0] in ['b', 'b_direct']: attacking_entity = f'b{slot}'

        b_grave_rect = ui.draw_deck_grave_zone(main_surface, bot, False, fonts, 19.4)
        p_grave_rect = ui.draw_deck_grave_zone(main_surface, player, True, fonts, 23.2)
        hex_hover = ui.draw_endturn_button(main_surface, hex_center, game_phase, (mx, my))

        hovered_idx = -1
        if game_phase == "PLAYER_SETUP" and not ui_state['viewing_grave'] and not ui_state['inspecting']:
            start_x = (WIDTH - ((len(player.hand) - 1) * 120 + 130)) // 2
            for i in range(len(player.hand)):
                if pygame.Rect(start_x + i * 120, 890, 130, 210).collidepoint(mx, my): hovered_idx = i; break

        for i in range(len(player.hand)):
            target_offset = 30 if (i == hovered_idx or i == ui_state['show_menu_idx']) else 0
            current_offset = ui_state['hover_offsets'].get(i, 0)
            ui_state['hover_offsets'][i] = current_offset + (target_offset - current_offset) * 0.15

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                if net: net.close()
                return "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                if net: net.close()
                return "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                if ui_state['viewing_grave']:
                    if ui_state.get('grave_scale', 0.0) >= 0.9:
                        clicked_grave_card = False 
                        scaled_size = (800, 1000) 
                        p_w, p_h = scaled_size
                        px, py = (WIDTH - p_w) // 2, (HEIGHT - p_h) // 2
                        c_row_w = (4 * 130) + (3 * 2)
                        s_x = px + (p_w - c_row_w) // 2
                        s_y = py + 30
                        gv = player.graveyard if ui_state['viewing_grave'] == "PLAYER" else bot.graveyard
                        for i, g_card in enumerate(gv[:16]):
                            gx = s_x + (i % 4) * (130 + 2); gy = s_y + (i // 4) * (180 + 2)
                            if pygame.Rect(gx, gy, 130, 180).collidepoint(mx, my):
                                clicked_grave_card = True
                                if ui_state['is_targeting'] == "SELECT_GRAVE_CARD" and g_card.card_type == "Monster":
                                    ui_state['revival_card'] = g_card; ui_state['is_targeting'] = "EMPTY_ALLY"; ui_state['viewing_grave'] = None
                                else: ui_state['inspecting'] = g_card
                                break
                        if not clicked_grave_card and not pygame.Rect(px, py, p_w, p_h).collidepoint(mx, my):
                            ui_state['viewing_grave'] = None
                    else:
                        ui_state['viewing_grave'] = None
                    continue

                prev_viewing_grave = ui_state['viewing_grave']
                ui_state['viewing_grave'] = None; ui_state['inspecting'] = None
                
                if p_grave_rect.collidepoint(mx, my): 
                    if prev_viewing_grave != "PLAYER": 
                        ui_state['viewing_grave'] = "PLAYER"
                        ui_state['grave_scale'] = 0.0
                    continue
                if b_grave_rect.collidepoint(mx, my): 
                    if prev_viewing_grave != "BOT": 
                        ui_state['viewing_grave'] = "BOT"
                        ui_state['grave_scale'] = 0.0
                    continue
                
                if game_phase == "PLAYER_SETUP" and not ui_state['setup_anim']:
                    if ui_state['is_discarding']:
                        start_x = (WIDTH - ((len(player.hand) - 1) * 120 + 130)) // 2
                        for i, card in enumerate(player.hand):
                            if pygame.Rect(start_x + i * 120, 920, 130, 180).collidepoint(mx, my):
                                player.graveyard.append(player.hand.pop(i)); ui_state['is_discarding'] = False; break
                        continue
                        
                    if hex_hover:
                        game_phase = "BOT_SETUP"; ui_state['show_menu_idx'] = -1; continue
                    
                    if ui_state['show_menu_idx'] != -1:
                        idx = ui_state['show_menu_idx']
                        start_x = (WIDTH - ((len(player.hand) - 1) * 120 + 130)) // 2
                        if pygame.Rect(start_x + idx * 120 - 10, 825, 150, 55).collidepoint(mx, my):
                            card = player.hand[idx]
                            if card.card_type == "Spell":
                                t_type = GameEngine.get_spell_type(card.name)
                                if t_type == "GLOBAL":
                                    action = {"type": "SPELL", "card": card, "target_side": "BOT", "side": "PLAYER"}
                                    ui_state['setup_anim'] = {'card': card, 'prog': 0, 'action': action}
                                    player.pending_spells.append(player.hand.pop(idx))
                                elif t_type == "GRAVE_ALLY":
                                    ui_state['is_targeting'] = "SELECT_GRAVE_CARD"; ui_state['viewing_grave'] = "PLAYER"; ui_state['grave_scale'] = 0.0
                                else: ui_state['is_targeting'] = t_type
                            elif card.card_type == "Environment": ui_state['is_targeting'] = "ENV"
                            elif card.card_type == "Monster": ui_state['is_targeting'] = "SUMMON"
                            ui_state['show_menu_idx'] = -1; ui_state['selected_idx'] = idx; continue

                    if ui_state['is_targeting']:
                        t_mode = ui_state['is_targeting']
                        for i in range(4):
                            if pygame.Rect(550 + i*222, 200, 160, 210).collidepoint(mx, my):
                                if t_mode == "ENEMY" and display_board.bot_slots[i]:
                                    card = player.hand[ui_state['selected_idx']]
                                    action = {"type": "SPELL", "card": card, "target_side": "BOT", "side": "PLAYER", "target": i}
                                    ui_state['setup_anim'] = {'card': card, 'prog': 0, 'action': action}
                                    player.pending_spells.append(player.hand.pop(ui_state['selected_idx']))
                                    ui_state['is_targeting'] = False
                                break

                            elif pygame.Rect(550 + i*222, 622, 160, 210).collidepoint(mx, my):
                                if t_mode == "ALLY" and display_board.player_slots[i]:
                                    card = player.hand[ui_state['selected_idx']]
                                    action = {"type": "SPELL", "card": card, "target_side": "PLAYER", "side": "PLAYER", "target": i}
                                    ui_state['setup_anim'] = {'card': card, 'prog': 0, 'action': action}
                                    player.pending_spells.append(player.hand.pop(ui_state['selected_idx']))
                                    ui_state['is_targeting'] = False
                                elif t_mode == "EMPTY_ALLY" and not display_board.player_slots[i]:
                                    card = player.hand[ui_state['selected_idx']]
                                    revived = ui_state['revival_card']
                                    player.graveyard.remove(revived)
                                    action = {"type": "SPELL", "card": card, "target_side": "PLAYER", "side": "PLAYER", "target": i, "revived_card": revived}
                                    ui_state['setup_anim'] = {'card': card, 'prog': 0, 'action': action}
                                    player.pending_spells.append(player.hand.pop(ui_state['selected_idx']))
                                    ui_state['is_targeting'] = False; ui_state['revival_card'] = None
                                elif t_mode == "SUMMON" and not display_board.player_slots[i]:
                                    card = player.hand[ui_state['selected_idx']]
                                    action = {"type": "SUMMON", "card": card, "target": i, "side": "PLAYER"}
                                    player_actions_queue.append(action)
                                    display_board.player_slots[i] = action["card"]
                                    player.hand.pop(ui_state['selected_idx']); ui_state['is_targeting'] = False
                                elif t_mode == "ENV":
                                    card = player.hand[ui_state['selected_idx']]
                                    action = {"type": "ENV", "card": card, "target": i, "side": "PLAYER"}
                                    ui_state['setup_anim'] = {'card': card, 'prog': 0, 'action': action}
                                    player.pending_spells.append(player.hand.pop(ui_state['selected_idx']))
                                    ui_state['is_targeting'] = False
                                break
                        continue
                    
                    clicked_something = False
                    start_x = (WIDTH - ((len(player.hand) - 1) * 120 + 130)) // 2
                    for i, card in enumerate(player.hand):
                        if pygame.Rect(start_x + i * 120, 920, 130, 180).collidepoint(mx, my):
                            ui_state['selected_idx'] = i
                            ui_state['inspecting'] = {'card': card, 'milestones': player.env_milestones, 'board_env': None}
                            ui_state['show_menu_idx'] = i; clicked_something = True; break
                            
                    if not clicked_something and not ui_state['is_targeting']:
                        for i in range(4):
                            if pygame.Rect(550 + i*222, 622, 160, 210).collidepoint(mx, my) and display_board.player_slots[i]:
                                ui_state['inspecting'] = {'card': display_board.player_slots[i], 'milestones': player.env_milestones, 'board_env': display_board.player_env[i]}; clicked_something = True; break
                            if pygame.Rect(550 + i*222, 200, 160, 210).collidepoint(mx, my) and display_board.bot_slots[i]:
                                ui_state['inspecting'] = {'card': display_board.bot_slots[i], 'milestones': bot.env_milestones, 'board_env': display_board.bot_env[i]}; clicked_something = True; break
                    if not clicked_something: ui_state['show_menu_idx'] = -1

        ui.draw_hud(main_surface, player.display_hp, bot.display_hp, fonts)
        tooltips = []
        ui.draw_milestones(main_surface, True, player.env_milestones, fonts, ICONS, (mx, my), tooltips)
        ui.draw_milestones(main_surface, False, bot.env_milestones, fonts, ICONS, (mx, my), tooltips)
        
        ui.draw_board(main_surface, display_board, ui_state['is_targeting'], anim.get_blink(curr_time), ICONS, anim, attacking_entity)
        ui.draw_hand(main_surface, player, ui_state, fonts, False)
        ui.draw_hand(main_surface, bot, ui_state, fonts, True)

        if ui_state['current_draw']: ui.draw_flip_card(main_surface, ui_state['current_draw'])
            
        if ui_state['is_discarding']:
            warn_rect = pygame.Rect(WIDTH//2 - 250, 840, 500, 45)
            pygame.draw.rect(main_surface, (200, 50, 50), warn_rect, 0, 10); pygame.draw.rect(main_surface, (255, 200, 200), warn_rect, 2, 10)
            ui.draw_text_centered(main_surface, "HAND IS FULL! CLICK A CARD TO DISCARD", fonts['small'], (255,255,255), warn_rect)
        
        if ui_state['show_menu_idx'] != -1 and not ui_state['is_targeting'] and not ui_state['is_discarding'] and not ui_state['setup_anim']:
            start_x = (WIDTH - ((len(player.hand) - 1) * 120 + 130)) // 2
            card = player.hand[ui_state['show_menu_idx']]
            btn_rect = pygame.Rect(start_x + ui_state['show_menu_idx'] * 120 - 10, 825, 150, 55)
            pygame.draw.rect(main_surface, (255, 200, 80) if btn_rect.collidepoint(mx, my) else (200, 150, 50), btn_rect, 0, 8)
            pygame.draw.rect(main_surface, (255, 255, 255), btn_rect, 2, 8) 
            ui.draw_text_centered(main_surface, "SUMMON" if card.card_type == "Monster" else "ACTIVATE", fonts['small'], (255,255,255), btn_rect)
            
        if ui_state['viewing_grave']:
            if ui_state.get('grave_scale', 0.0) < 1.0:
                ui_state['grave_scale'] = min(1.0, ui_state.get('grave_scale', 0.0) + 0.08)
            ui.draw_grave_viewer(main_surface, player.graveyard if ui_state['viewing_grave'] == "PLAYER" else bot.graveyard, fonts, ui_state.get('grave_scale', 1.0))
            
        if ui_state['inspecting']: ui.draw_zoom_panel(main_surface, ui_state['inspecting'], 1480, 250, fonts)

        for (tx, ty), text in tooltips:
            tt_surf = fonts['small'].render(text, True, (255, 255, 255))
            bg_rect = tt_surf.get_rect(topleft=(tx + 15, ty + 15)); bg_rect.inflate_ip(16, 10)
            if bg_rect.right > WIDTH: bg_rect.right = WIDTH - 10
            pygame.draw.rect(main_surface, (20, 20, 30), bg_rect, 0, 5); pygame.draw.rect(main_surface, (100, 200, 255), bg_rect, 1, 5)
            main_surface.blit(tt_surf, tt_surf.get_rect(center=bg_rect.center))
            
        if ui_state.get('spell_anim'):
            ui.draw_spell_activation(main_surface, ui_state['spell_anim']['card'], ui_state['spell_anim']['prog'], fonts)
        elif ui_state.get('setup_anim'):
            ui.draw_spell_activation(main_surface, ui_state['setup_anim']['card'], ui_state['setup_anim']['prog'], fonts)
        elif game_phase == "REVEAL": ui.draw_text_centered(main_surface, "OPPONENT ACTIONS REVEAL...", fonts['large'], (255, 200, 0), (WIDTH//2 - 250, 150, 500, 50))
        
        shake_x, shake_y = anim.get_global_shake_offset()
        screen.blit(main_surface, (shake_x, shake_y))
        
        if anim.red_flash_alpha > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 0, 0, anim.red_flash_alpha))
            screen.blit(flash_surf, (0,0))
            
        pygame.display.flip(); clock.tick(FPS)

def main():
    """
    Điểm truy cập chính của chương trình.
    Thiết lập xung nhịp (clock rate) và quản lý vòng đời chuyển đổi trạng thái của ứng dụng.
    """
    clock = pygame.time.Clock(); state = "MENU"
    net_conn = None
    while state != "QUIT":
        if state == "MENU": state, net_conn = menu_state(clock)
        elif state == "ONLINE_MENU": state, net_conn = online_menu_state(clock)
        elif state == "PLAYING": state = play_state(clock, net_conn)
    pygame.quit(); sys.exit()

if __name__ == "__main__": main()
