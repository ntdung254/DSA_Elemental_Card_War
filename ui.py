"""
Mô đun Render đồ họa và Giao diện Người dùng (UI Graphics Engine).
Cung cấp toàn bộ các hàm tiện ích hỗ trợ thao tác dựng hình, đổ màu, căn chỉnh văn bản,
phác họa bàn cờ, khu vực chứa thẻ, hiệu ứng công nghệ và kết xuất các cửa sổ (Modal/Panel).
"""
import pygame
import math
import os
from PIL import Image
from constants import *

CARD_W_UI = 130; CARD_H_UI = 180

ELEMENT_COLORS = {
    "Fire": (255, 50, 50), "Water": (50, 150, 255), "Wind": (50, 255, 100),
    "Earth": (180, 100, 50), "Lightning": (255, 220, 50), None: (80, 80, 80)
}
MILESTONE_COLORS = {0: (150, 150, 150), 1: (205, 127, 50), 2: (192, 192, 192), 3: (255, 215, 0), 4: (185, 242, 255)}
ALL_ELEMENTS = ["Fire", "Water", "Lightning", "Wind", "Earth"]

_ASSETS = {}
def get_asset(name, size=None, radius=0):
    """
    Truy xuất tài nguyên hình ảnh (Asset Manager). 
    Triển khai cấu trúc Lazy Loading và Caching để giảm tối đa chi phí file I/O.
    Hỗ trợ thay đổi kích thước và tạo mặt nạ bo góc (rounded corner mask) linh hoạt.
    """
    key = (name, size, radius)
    if key not in _ASSETS:
        try:
            img = pygame.image.load(f"assets/graphic/{name}.png").convert_alpha()
            if size: img = pygame.transform.smoothscale(img, size)
            if radius > 0:
                mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
                result = img.copy()
                result.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
                _ASSETS[key] = result
            else: _ASSETS[key] = img
        except: _ASSETS[key] = None
    return _ASSETS[key]

def draw_text_centered(surface, text, font, color, rect):
    """
    Hỗ trợ xuất văn bản nhiều dòng và tự động tính toán, căn giữa vị trí 
    (theo cả trục ngang và dọc) tương đối bên trong một khu vực khung chữ nhật xác định.
    """
    lines = str(text).split('\n')
    total_h = len(lines) * font.get_linesize()
    start_y = rect[1] + (rect[3] - total_h) // 2
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, color)
        text_rect = text_surf.get_rect(center=(rect[0] + rect[2]//2, start_y + i * font.get_linesize() + font.get_linesize()//2))
        surface.blit(text_surf, text_rect)

def draw_background(surface, bg_image=None):
    """
    Render phông nền cơ bản của ứng dụng. Cung cấp cơ chế dự phòng (fallback) tự động 
    vẽ mô hình lưới vector trong trường hợp không tải được file ảnh nền gốc.
    """
    if bg_image: surface.blit(bg_image, (0, 0))
    else:
        surface.fill((10, 12, 18))
        for x in range(0, WIDTH, 100): pygame.draw.line(surface, (20, 25, 40), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 100): pygame.draw.line(surface, (20, 25, 40), (0, y), (WIDTH, y), 1)

def draw_endturn_button(surface, center, turn, mouse_pos):
    """
    Vẽ nút bấm tương tác đa hình thái "End Turn" / "Waiting" tùy thuộc vào pha trận đấu hiện tại.
    Thay đổi màu sắc và lớp ảnh phủ (overlay) dựa trên trạng thái con trỏ chuột.
    """
    btn_w, btn_h = 160, 160
    rect = pygame.Rect(0, 0, btn_w, btn_h)
    rect.center = center
    
    is_hover = False
    if turn == "PLAYER_SETUP":
        is_hover = rect.collidepoint(mouse_pos)
        img = get_asset('endturn_hover', (btn_w, btn_h)) if is_hover else get_asset('endturn_normal', (btn_w, btn_h))
    else:
        img = get_asset('wait', (btn_w, btn_h))
        
    if img: surface.blit(img, rect.topleft)
    else:
        fill_color = (255, 200, 50) if is_hover else (180, 140, 30)
        if turn != "PLAYER_SETUP": fill_color = (60, 60, 60)
        pygame.draw.rect(surface, fill_color, rect, 0, 15)
        
    return is_hover

def draw_hand(surface, player, ui_state, fonts, is_bot=False):
    """
    Dựng khu vực bài trên tay (Hand). Tự động phân bổ khoảng cách nội suy giữa các thẻ bài 
    và đáp ứng các hiệu ứng trượt dọc (hover_offsets) khi di chuột vào đối với Người chơi, 
    cũng như che giấu mặt thẻ bằng ảnh lật úp đối với đối thủ Máy.
    """
    num = len(player.hand)
    if num == 0: return
    spacing = 120; start_x = (WIDTH - ((num - 1) * spacing + CARD_W_UI)) // 2
    base_y = 920 if not is_bot else -60 

    for i, card in enumerate(player.hand):
        hx = start_x + i * spacing; curr_y = base_y
        
        if not is_bot:
            offset = ui_state.get('hover_offsets', {}).get(i, 0)
            curr_y -= int(offset)

        if is_bot:
            back_img = get_asset('back', (CARD_W_UI, CARD_H_UI), radius=15)
            if back_img: surface.blit(pygame.transform.rotate(back_img, 180), (hx, curr_y))
            else: pygame.draw.rect(surface, (30, 45, 75), (hx, curr_y, CARD_W_UI, CARD_H_UI), 0, 15)
            pygame.draw.rect(surface, (0, 0, 0), (hx, curr_y, CARD_W_UI, CARD_H_UI), 1, 15)
        else:
            surface.blit(card.image_hand, (hx, curr_y))
            pygame.draw.rect(surface, (0, 0, 0), (hx, curr_y, CARD_W_UI, CARD_H_UI), 1, 15)
            if ui_state['selected_idx'] == i: pygame.draw.rect(surface, (0, 255, 255), (hx-2, curr_y-2, CARD_W_UI+4, CARD_H_UI+4), 3, 15)

def draw_flip_card(surface, draw_info):
    """
    Kết xuất cấu trúc giả 3D mô phỏng hiệu ứng thẻ lật mở (Flip Animation).
    Tính toán biến dạng kích thước ngang của thẻ thông qua hàm quỹ đạo nội suy bậc ba (cubic interpolation).
    """
    p = draw_info['prog']; t = 1 - pow(1 - p, 3) 
    sx, sy = draw_info['start']; ex, ey = draw_info['end']
    cx, cy = sx + (ex - sx) * t, sy + (ey - sy) * t
    
    if p < 0.5:
        w = int(CARD_W_UI * (1 - p/0.5))
        if w > 0:
            back_img = get_asset('back', (w, CARD_H_UI), radius=15)
            if back_img:
                if draw_info['side'] == 'BOT': back_img = pygame.transform.rotate(back_img, 180)
                surface.blit(back_img, (cx - w//2, cy))
            else:
                rect = pygame.Rect(cx - w//2, cy, w, CARD_H_UI)
                pygame.draw.rect(surface, (30, 45, 75), rect, 0, 15)
                pygame.draw.rect(surface, (0, 0, 0), rect, 2, 15)
    else:
        w = int(CARD_W_UI * ((p - 0.5)/0.5))
        if w > 0:
            img = pygame.transform.smoothscale(draw_info['card'].image_hand, (w, CARD_H_UI))
            if draw_info['side'] == 'BOT': img = pygame.transform.rotate(img, 180)
            surface.blit(img, (cx - w//2, cy))

def draw_spell_activation(surface, card, progress, fonts):
    """
    Render chuỗi hiệu ứng kỹ năng toàn màn hình cực đại (Cinematic Activation).
    Mô phỏng mặt nạ bán trong suốt cường độ dao động và vầng sáng ánh hào quang tỏa ra từ trung tâm.
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, int(150 * math.sin(progress * math.pi))))
    surface.blit(overlay, (0, 0))
    
    glow_size = int(350 + 50 * math.sin(progress * math.pi * 2))
    glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
    c_color = (100, 255, 100, 100) if card.card_type == "Environment" else (100, 200, 255, 100)
    pygame.draw.circle(glow, c_color, (glow_size//2, glow_size//2), glow_size//2)
    surface.blit(glow, (WIDTH//2 - glow_size//2, HEIGHT//2 - glow_size//2))
    
    s = 1.0 + math.sin(progress * math.pi) * 0.4
    w, h = int(160 * s), int(210 * s)
    surface.blit(pygame.transform.smoothscale(card.image_board, (w, h)), (WIDTH//2 - w//2, HEIGHT//2 - h//2))
    draw_text_centered(surface, "ACTIVATING...", fonts['huge'], (255, 255, 255), (0, HEIGHT//2 + h//2 + 20, WIDTH, 100))

def draw_text_with_outline(surface, text, font, color, outline_color, rect, y_offset=0):
    """
    Render phông chữ có viền bọc sắc nét (Outline Text) nhằm gia tăng độ tương phản.
    Thực hiện bằng kỹ thuật vẽ offset lặp 8 hướng (diagonal & orthogonal).
    """
    for ox, oy in [(-1,-1), (-1,1), (1,-1), (1,1), (0,-1), (0,1), (-1,0), (1,0)]:
        outline_surf = font.render(text, True, outline_color)
        surface.blit(outline_surf, outline_surf.get_rect(center=(rect.centerx + ox, rect.centery + oy + y_offset)))
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, text_surf.get_rect(center=(rect.centerx, rect.centery + y_offset)))

def draw_hud(surface, player_hp, bot_hp, fonts):
    """
    Xây dựng lớp phủ (Heads-Up Display - HUD) ở vị trí các góc màn hình để hiển thị 
    thông số điểm sinh mệnh (HP) cập nhật thời gian thực cho cả hai phe.
    """
    p_rect = pygame.Rect(20, HEIGHT - 110, 260, 90)
    b_rect = pygame.Rect(WIDTH - 280, 20, 260, 90)
    
    hp_img = get_asset('hp_bar', (260, 90))
    if hp_img:
        surface.blit(hp_img, p_rect.topleft)
        surface.blit(hp_img, b_rect.topleft)

    COLOR_HP_TEXT = (231, 215, 165)
    COLOR_HP_OUTLINE = (58, 43, 26)
    
    draw_text_with_outline(surface, f"HP: {int(player_hp)}", fonts['hp'], COLOR_HP_TEXT, COLOR_HP_OUTLINE, p_rect, y_offset=2)
    draw_text_with_outline(surface, f"HP: {int(bot_hp)}", fonts['hp'], COLOR_HP_TEXT, COLOR_HP_OUTLINE, b_rect, y_offset=2)

def draw_milestones(surface, is_player, milestones, fonts, icons, mouse_pos, tooltips_out):
    """
    Dựng bảng thống kê tiến trình độ phân giải Môi trường (Environment Milestones).
    Mã hóa màu các cấp độ, vẽ trực quan hóa các khung icon, đồng thời tự động chèn chú thích
    (tooltips) nếu con trỏ chuột dừng vào giới hạn đối tượng.
    """
    line_height, box_w, icon_size, text_off_y = 38, 260, 26, 4
    total_h = len(ALL_ELEMENTS) * line_height
    start_x = 20 if is_player else WIDTH - 280
    start_y = (HEIGHT - 110) - total_h - 15 if is_player else 20 + 90 + 15
    
    ms_bg = pygame.Surface((box_w, total_h + 0), pygame.SRCALPHA); ms_bg.fill((40, 40, 40, 80)); surface.blit(ms_bg, (start_x, start_y - 5))
    pygame.draw.rect(surface, (200, 200, 200, 150), (start_x, start_y - 5, box_w, total_h + 0), 2, 8)

    col_icon_x, col_text_x, col_count_x = start_x + 30, start_x + 70, start_x + 195
    pct_map = {1: 20, 2: 50, 3: 100, 4: 200}
    boost_text = {"Fire": "ATK & CRI", "Water": "HP & EV", "Lightning": "SPD & CRI", "Wind": "EV & SPD", "Earth": "DEF & HP"}

    for idx, el in enumerate(ALL_ELEMENTS):
        level = milestones.get(el, 0); curr_y = start_y + idx * line_height
        color = MILESTONE_COLORS.get(level, (200, 200, 200))
        if el.lower() in icons:
            surface.blit(pygame.transform.scale(icons[el.lower()], (icon_size, icon_size)), (col_icon_x, curr_y))
            if pygame.Rect(start_x, curr_y, box_w, line_height).collidepoint(mouse_pos):
                tooltips_out.append((mouse_pos, f"{el} Boost: +{pct_map[level]}% {boost_text[el]}" if level > 0 else f"{el} Boost: 0% {boost_text[el]}"))

        surface.blit(fonts['small'].render(el.capitalize(), True, color), (col_text_x, curr_y + text_off_y))
        surface.blit(fonts['small'].render(f"{level}/4", True, color), (col_count_x, curr_y + text_off_y))

def draw_deck_grave_zone(surface, player, is_player, fonts, deck_angle):
    """
    Bố cục và render khu vực chức năng gồm Bộ bài lưu trữ (Deck) và Mộ bài (Graveyard).
    Sử dụng tham số góc quay (deck_angle) để giả lập hình thái thực tế của tập giấy.
    """
    slot_x_start, slot_gap_x, slot_w, slot_h = 550, 222, 170, 220
    grave_w, grave_h, custom_gap = 126, 177, 30
    
    if is_player:
        slot_y = 622
        grave_x = slot_x_start - custom_gap - grave_w 
        grave_y = slot_y + (slot_h // 2) - (grave_h // 2)
        deck_center = (WIDTH - 348, HEIGHT - 118)
        grave_center = (grave_x + grave_w // 2, grave_y + grave_h // 2)
    else:
        slot_y = 200
        grave_x = (slot_x_start + 3 * slot_gap_x + slot_w) + custom_gap
        grave_y = slot_y + (slot_h // 2) - (grave_h // 2)
        deck_center = (436, 60)
        grave_center = (grave_x + grave_w // 2, grave_y + grave_h // 2)

    deck_img = get_asset('deck', (126, 177), radius=12)
    if deck_img:
        rotated_d = pygame.transform.rotate(deck_img, deck_angle)
        surface.blit(rotated_d, rotated_d.get_rect(center=deck_center))
    else: draw_rotated_rect(surface, (30, 45, 80), deck_center, 126, 177, deck_angle, 0, 10)

    g_rect = pygame.Rect(0, 0, grave_w, grave_h)
    g_rect.center = grave_center
    grave_img = get_asset('graveyard', (grave_w, grave_h), radius=12)
    if grave_img:
        if not is_player: grave_img = pygame.transform.rotate(grave_img, 180)
        surface.blit(grave_img, g_rect.topleft)
    else:
        pygame.draw.rect(surface, (50, 30, 30), g_rect, 0, 10); pygame.draw.rect(surface, (255, 100, 100), g_rect, 2, 10)
    
    return g_rect

def draw_board(surface, board, targeting_mode, blink_val, icons, anim, attacking_entity=None):
    """
    Render tổng thể trạng thái bàn cờ khu vực giao tranh 4x2 grid (Các slot thẻ bài).
    Khối lượng công việc bao gồm: đổ viền highlight theo luật targeting, pha trộn (blend) sprite, 
    xử lý các hoạt ảnh con của thẻ bài (độ mờ, rung lắc, trượt lên/xuống) và icon nguyên tố đi kèm.
    """
    card_w, card_h = 160, 210
    slot_w, slot_h = 170, 220
    border_w = 4
    board_img = get_asset('board', (slot_w + 20, slot_h + 20), radius=15)

    def render_slot(i, slots, envs, base_x, base_y, entity_prefix):
        """
        Nhiệm vụ đồ họa cục bộ tại một ô riêng biệt. Cập nhật vị trí bị dịch chuyển
        bởi engine animation và kiểm tra các điều kiện phát quang tương tác của ô cờ này.
        """
        shake_x, shake_y = anim.get_entity_shake(f'{entity_prefix}{i}')
        bump_y = anim.get_attack_offset(f'{entity_prefix}{i}')
        card_fx = base_x + 5 + shake_x
        card_fy = base_y + 5 + bump_y + shake_y

        outer_color = ELEMENT_COLORS[envs[i]] if envs[i] else ELEMENT_COLORS[None]
        pygame.draw.rect(surface, outer_color, (base_x - border_w, base_y - border_w, slot_w + border_w*2, slot_h + border_w*2), border_w, 15)
        
        if board_img:
            b_render = pygame.transform.rotate(board_img, 180) if entity_prefix == 'b' else board_img
            surface.blit(b_render, (base_x - 10, base_y - 10))
        else: pygame.draw.rect(surface, (30, 35, 45), (base_x, base_y, slot_w, slot_h), 0, 12)
            
        overlay = pygame.Surface((card_w, card_h), pygame.SRCALPHA); overlay.fill((220, 220, 220, 60)) 
        surface.blit(overlay, (base_x + 5, base_y + 5))

        if envs[i] and envs[i].lower() in icons:
            icon_img = pygame.transform.scale(icons[envs[i].lower()], (40, 40))
            icon_y = base_y + slot_h + 20 if entity_prefix == 'b' else base_y - 60
            if entity_prefix == 'b': icon_img = pygame.transform.rotate(icon_img, 180)
            surface.blit(icon_img, (base_x + 65, icon_y))

        is_valid = False
        if targeting_mode:
            if targeting_mode == "ENEMY" and entity_prefix == 'b' and slots[i]: is_valid = True
            elif targeting_mode == "ALLY" and entity_prefix == 'p' and slots[i]: is_valid = True
            elif targeting_mode == "EMPTY_ALLY" and entity_prefix == 'p' and not slots[i]: is_valid = True
            elif targeting_mode == "SUMMON" and entity_prefix == 'p' and not slots[i]: is_valid = True
            elif targeting_mode == "ENV" and entity_prefix == 'p': is_valid = True
            
        if is_valid: 
            pygame.draw.rect(surface, (40, 150*blink_val + 50, 200), (base_x - border_w, base_y - border_w, slot_w + border_w*2, slot_h + border_w*2), 4, 15)

        if attacking_entity == f'{entity_prefix}{i}':
            pulse = int(100 * blink_val + 155) 
            pygame.draw.rect(surface, (pulse, 30, 30), (base_x - border_w - 4, base_y - border_w - 4, slot_w + border_w*2 + 8, slot_h + border_w*2 + 8), 4, 15)

        card = slots[i]
        if card:
            summon_prog = anim.get_summon_progress(f'{entity_prefix}{i}')
            d_alpha = anim.get_death_alpha(f'{entity_prefix}{i}')
            
            if summon_prog < 1.0:
                s = max(0.1, summon_prog)
                w, h = int(card_w * s), int(card_h * s)
                img = pygame.transform.smoothscale(card.image_board, (w, h))
                if entity_prefix == 'b': img = pygame.transform.rotate(img, 180)
                img.set_alpha(int(255 * summon_prog))
                surface.blit(img, (base_x + 5 + (card_w-w)//2, base_y + 5 + (card_h-h)//2))
                
            elif f'{entity_prefix}{i}' in anim.death_anims:
                s = max(0.1, d_alpha / 255.0)
                w, h = int(card_w * s), int(card_h * s)
                img = pygame.transform.smoothscale(card.image_board, (w, h))
                if entity_prefix == 'b': img = pygame.transform.rotate(img, 180)
                img.set_alpha(d_alpha)
                surface.blit(img, (base_x + 5 + (card_w-w)//2, base_y + 5 + (card_h-h)//2 - (255-d_alpha)//3))
            else:
                img_render = pygame.transform.rotate(card.image_board, 180) if entity_prefix == 'b' else card.image_board
                surface.blit(img_render, (card_fx, card_fy))

        flash_alpha = anim.get_flash_alpha(f'{entity_prefix}{i}')
        if flash_alpha > 0:
            fs = pygame.Surface((slot_w, slot_h), pygame.SRCALPHA); fs.fill((255, 255, 255, flash_alpha))
            surface.blit(fs, (base_x, base_y))

        spell_ov = anim.get_spell_overlay(f'{entity_prefix}{i}')
        if spell_ov:
            ov_type, ov_alpha = spell_ov
            ov_img = get_asset(ov_type, (slot_w, slot_h))
            if ov_img:
                ov_render = ov_img.copy()
                ov_render.set_alpha(ov_alpha)
                surface.blit(ov_render, (base_x, base_y))
            else:
                ov_color = (80, 255, 80, ov_alpha) if ov_type == 'plus' else (255, 80, 80, ov_alpha)
                ov_surf = pygame.Surface((slot_w, slot_h), pygame.SRCALPHA)
                ov_surf.fill(ov_color)
                surface.blit(ov_surf, (base_x, base_y))

    for i in range(4):
        render_slot(i, board.bot_slots, board.bot_env, 550 + i*222, 200, 'b')
        render_slot(i, board.player_slots, board.player_env, 550 + i*222, 622, 'p')


def draw_zoom_panel(surface, inspect_data, x, y, fonts, panel_w=880, panel_h=2700, badge_w=220, badge_h=120,
                    badge_dx=0, badge_dy=0,       # Dịch chuyển nhãn (badge)
                    card_dx=0, card_dy=0,         # Dịch chuyển ảnh lá bài
                    name_dx=0, name_dy=0,         # Dịch chuyển chữ Tên lá bài
                    stats_dx=0, stats_dy=0,       # Dịch chuyển bảng chỉ số/mô tả
                    num_columns=2, col_gap=40, row_gap=65):
    """
    Cửa sổ Thông tin chi tiết (Inspect Panel). 
    """
    if isinstance(inspect_data, dict):
        card, milestones, board_env = inspect_data['card'], inspect_data.get('milestones', {}), inspect_data.get('board_env', None)
    else:
        card, milestones, board_env = inspect_data, {}, None

    px, py = x, y

    # --- Background panel: graphic/info.png ---
    info_bg = get_asset('info', (panel_w, panel_h))
    if info_bg:
        surface.blit(info_bg, (px, py))
    else:
        pygame.draw.rect(surface, (15, 18, 25), (px, py, panel_w, panel_h), 0, 20)
        pygame.draw.rect(surface, (100, 100, 120), (px, py, panel_w, panel_h), 2, 20)

    # --- Các tọa độ gốc mặc định (Base Coordinates) ---
    base_badge_y = py + 20
    base_img_y = base_badge_y + badge_h + 30
    IMG_W, IMG_H = 400, 530
    base_name_y = base_img_y + IMG_H + 30
    base_stats_y = base_name_y + 48 + 30

    # --- Type badge (Áp dụng dịch chuyển badge_dx, badge_dy) ---
    badge_x = px + (panel_w - badge_w) // 2 + badge_dx
    badge_y = base_badge_y + badge_dy
    badge_name = card.card_type.lower()
    badge_img = get_asset(badge_name, (badge_w, badge_h))
    
    if badge_img:
        surface.blit(badge_img, (badge_x, badge_y))
    else:
        type_colors = {"Monster": (180, 50, 50), "Spell": (50, 100, 180), "Environment": (50, 150, 50)}
        badge_rect = pygame.Rect(badge_x, badge_y, badge_w, badge_h)
        pygame.draw.rect(surface, type_colors.get(card.card_type, (100, 100, 100)), badge_rect, 0, 12)
        pygame.draw.rect(surface, (255, 255, 255), badge_rect, 2, 12)
        draw_text_centered(surface, card.card_type.upper(), fonts['small'], (255, 255, 255), badge_rect)

    # --- Card image (Áp dụng dịch chuyển card_dx, card_dy) ---
    img_x = px + (panel_w - IMG_W) // 2 + card_dx
    img_y = base_img_y + card_dy
    surface.blit(card.image_zoom, (img_x, img_y))
    pygame.draw.rect(surface, (200, 200, 200), (img_x, img_y, IMG_W, IMG_H), 2, 35)

    # --- Card name (Áp dụng dịch chuyển name_dx, name_dy) ---
    COLOR_HP_TEXT = (231, 215, 165)
    COLOR_HP_OUTLINE = (58, 43, 26)
    name_rect = pygame.Rect(px + name_dx, base_name_y + name_dy, panel_w, 48)  
    draw_text_with_outline(surface, card.name.upper(), fonts['hp'], COLOR_HP_TEXT, COLOR_HP_OUTLINE, name_rect)

    # --- Stats / Description (Áp dụng dịch chuyển stats_dx, stats_dy) ---
    start_y = base_stats_y + stats_dy
    if card.card_type == "Monster":
        stats = card.get_current_stats(milestones, board_env)
        stat_names = [("ATK", "atk"), ("DEF", "def"), ("HP", "hp"), ("SPD", "spd"), ("EVA", "eva"), ("CRI", "cri")]
        
        # BẢN FIX: Cố định độ rộng mỗi ô chứa chữ để col_gap hoạt động rõ ràng
        # 160 pixel là độ rộng vừa vặn cho các chỉ số
        cell_w = 160  
        total_grid_w = num_columns * cell_w + (num_columns - 1) * col_gap
        
        # Tính điểm bắt đầu X để căn giữa toàn bộ khối chỉ số
        grid_start_x = px + (panel_w - total_grid_w) // 2 + stats_dx
        
        for i, (label, key) in enumerate(stat_names):
            col_idx = i % num_columns
            row_idx = i // num_columns
            
            # Vị trí X giờ phụ thuộc hoàn toàn vào col_gap và cell_w cố định
            sx = grid_start_x + col_idx * (cell_w + col_gap)
            sy = start_y + row_idx * row_gap
            
            stat_rect = pygame.Rect(sx, sy, cell_w, 60)
            
            if key == "hp":
                txt = f"HP: {int(stats['hp']['current'])}/{int(stats['hp']['max'])}"
                draw_text_with_outline(surface, txt, fonts['hp'], COLOR_HP_TEXT, COLOR_HP_OUTLINE, stat_rect)
            else:
                base, curr = stats[key]['base'], stats[key]['current']
                if curr > base:   val_color = (100, 255, 100)
                elif curr < base: val_color = (255, 100, 100)
                else:             val_color = COLOR_HP_TEXT
                txt = f"{label}: {int(curr)}"
                draw_text_with_outline(surface, txt, fonts['hp'], val_color, COLOR_HP_OUTLINE, stat_rect)
    else:
        # Spell/Environment description
        desc_rect = pygame.Rect(px + stats_dx, start_y, panel_w, 200)
        lines = card.description.split('. ') if card.description else []
        line_y = desc_rect.y
        for line in lines:
            if not line: continue
            txt_surf = fonts['small'].render(line.strip(), True, COLOR_HP_TEXT)
            cx = px + (panel_w - txt_surf.get_width()) // 2 + stats_dx
            for ox, oy in [(-1,-1), (-1,1),(1,-1),(1,1)]:
                o_surf = fonts['small'].render(line.strip(), True, COLOR_HP_OUTLINE)
                surface.blit(o_surf, (cx + ox, line_y + oy))
            surface.blit(txt_surf, (cx, line_y))
            line_y += fonts['small'].get_linesize() + 10

def draw_grave_viewer(surface, graveyard, fonts, scale=1.0):
    """
    Render một khung pop-up nội bộ chiếm tỷ lệ lớn để liệt kê toàn bộ các thẻ bài đã nằm dưới mộ.
    Cung cấp hiệu ứng phóng to động (Zoom Animation) với hệ số scale điều chỉnh kích thước tổng quan.
    """
    if scale <= 0.01: return
    
    dim_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim_overlay.fill((0, 0, 0, int(180 * scale)))
    surface.blit(dim_overlay, (0, 0))

    base_w, base_h = 800, 1000
    panel_w, panel_h = int(base_w * scale), int(base_h * scale)
    px, py = (WIDTH - panel_w) // 2, (HEIGHT - panel_h) // 2
    
    table_img = get_asset('graveyard_table', size=(base_w, base_h))
    if table_img:
        if scale < 1.0: table_img = pygame.transform.scale(table_img, (panel_w, panel_h))
        surface.blit(table_img, (px, py))
        
    if scale < 0.2: return 
    
    c_w, c_h = max(1, int(CARD_W_UI * scale)), max(1, int(CARD_H_UI * scale))
    gap = max(1, int(2 * scale))
    
    card_row_w = (4 * c_w) + (3 * gap)
    start_x = px + (panel_w - card_row_w) // 2
    start_y = py + int(150 * scale)
    
    for i, card in enumerate(graveyard[:16]):
        gx = start_x + (i % 4) * (c_w + gap)
        gy = start_y + (i // 4) * (c_h + gap)
        scaled_card = pygame.transform.scale(card.image_hand, (c_w, c_h)) if scale < 1.0 else card.image_hand
        surface.blit(scaled_card, (gx, gy))

def draw_rotated_rect(surface, color, center, width, height, angle, border_width=0, border_radius=10):
    """
    Hàm vẽ nguyên thủy bổ trợ (Helper graphic method) để vẽ cấu trúc hình khối (Rectangle) 
    nhưng có khả năng tùy chỉnh góc xoay linh hoạt tự do xung quanh điểm trung tâm (pivot).
    """
    target_rect = pygame.Rect(0, 0, width, height)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, (0, 0, width, height), border_width, border_radius)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=center))
    
def draw_endgame_screen(surface, is_victory, fonts, scale=1.0):
    """
    Dựng kết quả Tổng kết Ván đấu (Defeat/Victory) ở giai đoạn cuối ứng dụng.
    Bao gồm làm tối nền, dựng đồ họa cảnh báo theo chu kỳ mở dần (scaling fade-in overlay).
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) 
    surface.blit(overlay, (0, 0))
    
    img_name = 'victory' if is_victory else 'defeat'
    img = get_asset(img_name)
    
    if img:
        w, h = int(img.get_width() * scale), int(img.get_height() * scale)
        if w > 0 and h > 0:
            scaled_img = pygame.transform.smoothscale(img, (w, h))
            img_rect = scaled_img.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            surface.blit(scaled_img, img_rect)
        y_text = HEIGHT//2 + img.get_height()//2 - 10
    else:
        y_text = HEIGHT//2 + 50

    if scale >= 0.9:
        draw_text_centered(surface, "Click anywhere to exit", fonts['large'], (255, 255, 255), (0, y_text, WIDTH, 50))
