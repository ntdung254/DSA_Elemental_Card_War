import pygame
from PIL import Image
from constants import *

def draw_text(surface, text, x, y, font, color=COLOR_TEXT_BASE): #Vẽ văn bản lên bề mặt hiển thị với tọa độ số nguyên
    img = font.render(str(text), True, color)
    surface.blit(img, (int(x), int(y)))

def draw_zoom_panel(surface, card, x, y, fonts, offset): #Hiển thị bảng thông tin chi tiết của lá bài đang được chọn
    if not card: return
    off_x, off_y = offset
    px, py = x + off_x, y + off_y
    
    pygame.draw.rect(surface, (10, 12, 18), (px, py, 420, 950), 0, 20)
    pygame.draw.rect(surface, COLOR_BORDER, (px, py, 420, 950), 2, 20)
    
    try:
        pil_img = Image.open(card.image_path).convert("RGBA")
        zoom_res = pil_img.resize((370, 495), Image.LANCZOS)
        zoom_surface = pygame.image.fromstring(zoom_res.tobytes(), zoom_res.size, zoom_res.mode).convert_alpha()
        surface.blit(zoom_surface, (int(px + 25), int(py + 25)))
    except:
        surface.blit(card.image_board, (int(px + 25), int(py + 25)))

    draw_text(surface, card.name.upper(), px + 25, py + 540, fonts['large'], (0, 255, 255))
    
    stats = [
        (f"ATK: {card.stat_atk}", (255, 100, 100)), (f"DEF: {card.stat_def}", (100, 255, 100)),
        (f"HP: {card.stat_hp}", (255, 255, 100)), (f"SPD: {card.stat_spd}", (100, 150, 255)),
        (f"CRI: {card.stat_cri}%", (255, 100, 255)), (f"EVA: {card.stat_eva}%", (150, 255, 200))
    ]
    for i, (text, color) in enumerate(stats):
        draw_text(surface, text, px + 25 + (i % 2 * 180), py + 640 + (i // 2 * 50), fonts['stats'], color)

def draw_board(surface, board, is_targeting, blink_val, offset): #Vẽ bàn cờ và các quái vật trên sân
    off_x, off_y = offset
    for i in range(4):
        bx, by = 400 + i * 220 + off_x, 420 + off_y
        slot_color = (60, 60, 65)
        if is_targeting and not board.slots[i]:
            slot_color = (40, 100 * blink_val + 40, 40)
            pygame.draw.rect(surface, (0, 255, 0), (bx-4, by-4, 158, 208), 2, 12)
        
        pygame.draw.rect(surface, slot_color, (bx, by, 150, 200), 0, 10)
        if board.slots[i]:
            surface.blit(board.slots[i].image_board, (bx, by))

def draw_hand(surface, player, ui_state, fonts, offset): #Vẽ các lá bài trên tay và menu Summon
    off_x, off_y = offset
    for i, card in enumerate(player.hand):
        hx, hy = 250 + i * 170 + off_x, 850 + off_y
        if i == ui_state['selected_idx']:
            pygame.draw.rect(surface, (0, 255, 180), (hx-5, hy-5, 140, 190), 4, 10)
        surface.blit(card.image_hand, (hx, hy))

        if ui_state['show_menu_idx'] == i:
            pygame.draw.rect(surface, COLOR_SUMMON, (hx, hy - 60, 120, 40), 0, 5)
            pygame.draw.rect(surface, (255, 255, 255), (hx, hy - 60, 120, 40), 1, 5)
            draw_text(surface, "SUMMON", hx + 10, hy - 50, fonts['small'])

def draw_slam_effect(surface, card, target_idx, progress, offset): #Hiệu ứng lá bài đập mạnh từ trên cao xuống
    if not card: return
    off_x, off_y = offset
    bx, by = 400 + target_idx * 220, 420
    
    scale_val = 1.0 + (1.0 - progress) * 2.0 
    temp_w, temp_h = int(150 * scale_val), int(200 * scale_val)
    
    slam_img = pygame.transform.smoothscale(card.image_board, (temp_w, temp_h))
    slam_img.set_alpha(int(255 * progress))
    
    draw_x = bx - (temp_w - 150) // 2 + off_x
    draw_y = by - (temp_h - 200) // 2 + off_y
    surface.blit(slam_img, (draw_x, draw_y))
