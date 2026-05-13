"""
Mô đun định nghĩa các cấu trúc dữ liệu cốt lõi (Models) cho hệ thống trò chơi.
Bao gồm các lớp biểu diễn Thẻ bài (Card), Người chơi (Player) và trạng thái Bàn cờ (Board),
hỗ trợ quản lý logic và nạp trước dữ liệu hình ảnh tối ưu nhờ cơ chế caching.
"""
import pygame
import random
from PIL import Image, ImageDraw

_IMAGE_CACHE = {}

class Card:
    """
    Lớp cấu trúc đại diện cho một thẻ bài vật lý ảo.
    Chứa toàn bộ thông số cơ bản (HP, ATK, DEF...), nguyên tố, đường dẫn hình ảnh.
    Cung cấp các cơ chế tiền xử lý ảnh (bo góc, đa độ phân giải) để tối ưu hiệu suất đồ họa.
    """
    def __init__(self, name, card_type, element, image_path, stat_atk=0, stat_def=0, stat_hp=0, stat_cri=0, stat_eva=0, stat_spd=0, description=""):
        """
        Khởi tạo đối tượng thẻ bài dựa trên bộ chỉ số truyền vào.
        Thực hiện áp dụng Cache hình ảnh, xử lý bộ nhớ đệm để tránh tải lại file I/O liên tục,
        và tạo ba phiên bản hình ảnh (Hand, Board, Zoom) bằng thư viện PIL (Pillow).
        """
        self.name = name
        self.card_type = card_type
        self.element = element
        self.stat_atk, self.stat_def, self.stat_hp = stat_atk, stat_def, stat_hp
        self.current_hp = stat_hp  
        self.stat_cri, self.stat_eva, self.stat_spd = stat_cri, stat_eva, stat_spd
        self.description = description
        self.image_path = image_path 

        cache_key = (image_path, name)
        if cache_key in _IMAGE_CACHE:
            cached_data = _IMAGE_CACHE[cache_key]
            self.image_hand = cached_data['hand']
            self.image_board = cached_data['board']
            self.image_zoom = cached_data['zoom']
        else:
            try:
                pil_img = Image.open(image_path).convert("RGBA")
                
                def apply_rounded_corners(im, rad):
                    circle = Image.new('L', (rad * 2, rad * 2), 0)
                    draw = ImageDraw.Draw(circle)
                    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
                    alpha = Image.new('L', im.size, 255)
                    w, h = im.size
                    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
                    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
                    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
                    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
                    im.putalpha(alpha)
                    return im

                h_res = apply_rounded_corners(pil_img.resize((130, 180), Image.Resampling.LANCZOS), 15)
                b_res = apply_rounded_corners(pil_img.resize((160, 210), Image.Resampling.LANCZOS), 18)
                z_res = apply_rounded_corners(pil_img.resize((400, 530), Image.Resampling.LANCZOS), 35)

                self.image_hand = pygame.image.frombuffer(h_res.tobytes(), h_res.size, h_res.mode).convert_alpha()
                self.image_board = pygame.image.frombuffer(b_res.tobytes(), b_res.size, b_res.mode).convert_alpha()
                self.image_zoom = pygame.image.frombuffer(z_res.tobytes(), z_res.size, z_res.mode).convert_alpha()

                _IMAGE_CACHE[cache_key] = {'hand': self.image_hand, 'board': self.image_board, 'zoom': self.image_zoom}
            except:
                self.image_hand = pygame.Surface((130, 180), pygame.SRCALPHA); pygame.draw.rect(self.image_hand, (100,100,100), (0,0,130,180), 0, 15)
                self.image_board = pygame.Surface((160, 210), pygame.SRCALPHA); pygame.draw.rect(self.image_board, (100,100,100), (0,0,160,210), 0, 18)
                self.image_zoom = pygame.Surface((400, 530), pygame.SRCALPHA); pygame.draw.rect(self.image_zoom, (100,100,100), (0,0,400,530), 0, 35)

    def get_current_stats(self, milestones, board_env=None):
        """
        Tính toán và trả về toàn bộ bộ chỉ số theo cấu trúc từ điển (Dictionary) của thẻ bài ở thời điểm hiện tại.
        Cho phép cộng gộp các hiệu ứng tăng cường từ cấp độ cộng hưởng nguyên tố (milestones) 
        và môi trường tương ứng đang được thiết lập trên bàn cờ.
        """
        stats = {
            "atk": {"base": self.stat_atk, "current": self.stat_atk},
            "def": {"base": self.stat_def, "current": self.stat_def},
            "hp": {"base": self.stat_hp, "current": self.current_hp, "max": self.stat_hp},
            "spd": {"base": self.stat_spd, "current": self.stat_spd},
            "eva": {"base": self.stat_eva, "current": self.stat_eva},
            "cri": {"base": self.stat_cri, "current": self.stat_cri},
        }
        if self.card_type != "Monster": return stats

        if board_env == "Fire": stats["atk"]["current"] += 10
        elif board_env == "Lightning": stats["spd"]["current"] += 10
        elif board_env == "Wind": stats["eva"]["current"] += 20
        elif board_env == "Earth": stats["def"]["current"] += 20
        elif board_env == "Water": stats["hp"]["max"] += 0 

        boost_map = {"Fire": ["atk", "cri"], "Water": ["hp", "eva"], "Lightning": ["spd", "cri"], "Wind": ["eva", "spd"], "Earth": ["def", "hp"]}
        pct_map = {0: 0.0, 1: 0.2, 2: 0.5, 3: 1.0, 4: 2.0}

        if board_env == self.element:
            lvl = milestones.get(self.element, 0)
            if lvl > 0 and self.element in boost_map:
                pct = pct_map[lvl]
                for stat in boost_map[self.element]:
                    bonus = stats[stat]["base"] * pct
                    if stat == "hp": stats[stat]["max"] += bonus
                    else: stats[stat]["current"] += bonus
        return stats

class Player: 
    """
    Lớp quản lý thông tin và dữ liệu vòng đời của một đấu thủ (Người hoặc Máy).
    Giám sát điểm sinh mệnh (HP), trạng thái Rút bài (Deck), bài trên tay (Hand), 
    mộ bài (Graveyard) và tiến trình nâng cấp nguyên tố (milestones).
    """
    def __init__(self, full_card_pool):
        """
        Khởi tạo đấu thủ với lượng điểm sinh mệnh tiêu chuẩn. Trộn (shuffle) danh sách thẻ truyền vào 
        để tạo lập bộ bài ngẫu nhiên, sẵn sàng cho việc phân phối thẻ.
        """
        self.hp = 200
        self.display_hp = 200.0 # Thêm biến máu hiển thị để tạo animation
        self.deck = list(full_card_pool)
        random.shuffle(self.deck)
        self.hand, self.graveyard = [], []
        self.env_milestones = {"Fire": 0, "Water": 0, "Lightning": 0, "Wind": 0, "Earth": 0}

    def draw_card(self):
        """
        Rút một thẻ bài ở vị trí trên cùng của Bộ bài (Deck). Trả về None nếu bộ bài đã rỗng.
        """
        return self.deck.pop() if self.deck else None

class Board:
    """
    Lớp dữ liệu biểu diễn tình trạng tổng quan trên bề mặt giao tranh (Bàn cờ).
    Bao gồm 4 ô không gian cho Người chơi và 4 ô cho Máy, quản lý sự hiện diện của Thẻ quái vật
    cùng với nguyên tố môi trường tương ứng đang được áp đặt tại các ô.
    """
    def __init__(self):
        """
        Khởi tạo Bàn cờ ở trạng thái trống không, phân bổ đồng đều các ô slot bằng giá trị None.
        """
        self.player_slots, self.bot_slots = [None] * 4, [None] * 4
        self.player_env, self.bot_env = [None] * 4, [None] * 4
