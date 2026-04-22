import pygame, sys, os
from constants import *
import ui
from animations import AnimationManager

# Khổi tạo hệ thống (Display trước)
os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '2'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("ELEMENTAL CARD WARS - Nguyễn Tấn Dũng (25520368)")

# Import Data
from models import Player, Board
from card_data import FULL_DATABASE

def main():
    # Vòng lặp chính quản lý trạng thái Game
    clock = pygame.time.Clock()
    anim = AnimationManager()
    player = Player(FULL_DATABASE.copy())
    board = Board()
    
    fonts = {
        'small': pygame.font.SysFont("Verdana", 20, bold=True),
        'stats': pygame.font.SysFont("Verdana", 18, bold=True),
        'large': pygame.font.SysFont("Verdana", 32, bold=True),
        'count': pygame.font.SysFont("Verdana", 40, bold=True)
    }

    ui_state = {
        'inspecting': None, 'selected_idx': -1, 'show_menu_idx': -1,
        'is_targeting': False, 'draw_anim': None, 'draw_pos': [1550.0, 850.0],
        'summon_anim': None, 'summon_progress': 0.0, 'summon_target_idx': -1
    }

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        offset = anim.get_shake_offset()
        screen.fill(COLOR_BG)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_smth = False
                
                # Logic Deck
                if 1550 <= mx <= 1680 and 850 <= my <= 1030 and not ui_state['draw_anim']:
                    card = player.draw_card(); clicked_smth = True
                    if card: ui_state['draw_anim'] = card; ui_state['draw_pos'] = [1550.0, 850.0]

                # Logic Summon Button
                if ui_state['show_menu_idx'] != -1:
                    hx, hy = 250 + ui_state['show_menu_idx'] * 170, 850
                    if hx <= mx <= hx + 120 and hy - 60 <= my <= hy - 10:
                        ui_state['is_targeting'] = True; ui_state['show_menu_idx'] = -1; clicked_smth = True

                # Logic Board Slots
                if not clicked_smth:
                    for i in range(4):
                        bx, by = 400 + i * 220, 420
                        if bx <= mx <= bx + 150 and by <= my <= by + 200:
                            if ui_state['is_targeting'] and not board.slots[i]:
                                ui_state['summon_anim'] = player.hand.pop(ui_state['selected_idx'])
                                ui_state['summon_target_idx'] = i; ui_state['summon_progress'] = 0.0
                                ui_state['is_targeting'] = False; ui_state['inspecting'] = None; clicked_smth = True
                            elif board.slots[i]: ui_state['inspecting'] = board.slots[i]; clicked_smth = True
                            break

                # Logic Hand Cards
                if not clicked_smth:
                    for i, card in enumerate(player.hand):
                        hx, hy = 250 + i * 170, 850
                        if hx <= mx <= hx + 120 and hy <= my <= hy + 180:
                            ui_state['selected_idx'], ui_state['inspecting'] = i, card
                            if card.card_type == "Monster": ui_state['show_menu_idx'] = i
                            else: 
                                player.hand.pop(i); ui_state['selected_idx'] = -1; ui_state['inspecting'] = None
                            clicked_smth = True; break

                if not clicked_smth: # CLick vào vùng trống để thoát khỏi nội dung
                    ui_state['selected_idx'] = -1; ui_state['inspecting'] = None; ui_state['show_menu_idx'] = -1

        # Update
        if ui_state['draw_anim']:
            tx = 250 + len(player.hand) * 170
            ui_state['draw_pos'][0] += (tx - ui_state['draw_pos'][0]) * 0.15
            if abs(ui_state['draw_pos'][0] - tx) < 2: player.hand.append(ui_state['draw_anim']); ui_state['draw_anim'] = None

        if ui_state['summon_anim']:
            ui_state['summon_progress'] += 0.04
            if ui_state['summon_progress'] >= 1.0:
                board.slots[ui_state['summon_target_idx']] = ui_state['summon_anim']
                ui_state['summon_anim'] = None; anim.start_shake()

        # Hiển thị
        # Deck
        pulse = anim.get_pulse(current_time)
        pygame.draw.rect(screen, (50, 80, 200 * pulse + 50), (1545+offset[0], 845+offset[1], 140, 190), 4, 12)
        pygame.draw.rect(screen, (30, 35, 60), (1550+offset[0], 850+offset[1], 130, 180), 0, 10)
        ui.draw_text(screen, f"{len(player.deck)}", 1605+offset[0], 915+offset[1], fonts['count'])

        ui.draw_board(screen, board, ui_state['is_targeting'], anim.get_blink(current_time), offset)
        ui.draw_hand(screen, player, ui_state, fonts, offset)

        if ui_state['summon_anim']:
            ui.draw_slam_effect(screen, ui_state['summon_anim'], ui_state['summon_target_idx'], ui_state['summon_progress'], offset)
        if ui_state['draw_anim']:
            screen.blit(ui_state['draw_anim'].image_hand, (int(ui_state['draw_pos'][0])+offset[0], int(ui_state['draw_pos'][1])+offset[1]))
        if ui_state['inspecting']:
            ui.draw_zoom_panel(screen, ui_state['inspecting'], 1480, 40, fonts, offset)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": main()
