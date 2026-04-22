import pygame
import random
from PIL import Image 

class Card: # Lớp đại diện cho một lá bài trong trò chơi
    def __init__(self, name, card_type, element, image_path, stat_atk=0, stat_def=0, stat_hp=0, stat_cri=0, stat_eva=0, stat_spd=0, description=""):
        self.name = name # Tên lá bài
        self.card_type = card_type # Loại bài 
        self.element = element # Hệ nguyên tố 

        self.base_atk = stat_atk # Tấn công gốc
        self.base_def = stat_def # Phòng thủ gốc
        self.base_hp = stat_hp # Máu gốc
        self.base_spd = stat_spd # Tốc độ gốc
        self.base_cri = stat_cri # Chí mạng gốc
        self.base_eva = stat_eva # Né tránh gốc

        self.stat_atk = stat_atk # Tấn công hiện tại
        self.stat_def = stat_def # Phòng thủ hiện tại
        self.stat_hp = stat_hp # Máu hiện tại
        self.stat_cri = stat_cri # Chí mạng hiện tại
        self.stat_eva = stat_eva # Né tránh hiện tại
        self.stat_spd = stat_spd # Tốc độ hiện tại
        self.description = description # Mô tả nội dung của bài

        try:
            # SỬ DỤNG PILLOW ĐỂ RESIZE VỚI THUẬT TOÁN LANCZOS (CỰC NÉT)
            pil_img = Image.open(image_path).convert("RGBA")
            
            # Kích thước cho bài trên tay (Nhỏ gọn để dễ quản lý)
            hand_res = pil_img.resize((130, 180), Image.LANCZOS)
            # Kích thước cho bài trên bàn cờ (Lớn hơn để nhìn rõ chi tiết)
            board_res = pil_img.resize((160, 210), Image.LANCZOS)
            
            # Chuyển ngược lại Pygame Surface để render
            # FIX: Sửa fromstring thành frombuffer để tương thích với Pygame 2.2+
            self.image_hand = pygame.image.frombuffer(hand_res.tobytes(), hand_res.size, hand_res.mode).convert_alpha()
            self.image_board = pygame.image.frombuffer(board_res.tobytes(), board_res.size, board_res.mode).convert_alpha()
            
            self.image_path = image_path 
            
        except Exception as e:
            print(f"Lỗi load ảnh {name}: {e}")
            # Fallback: Tạo mặt bài trống nếu không load được ảnh
            self.image_hand = pygame.Surface((130, 180))
            self.image_hand.fill((200, 100, 100))
            self.image_board = pygame.Surface((160, 210))
            self.image_board.fill((200, 100, 100))

class Player: # Lớp quản lý thông tin và hành động của người chơi (HP, Deck, Hand)
    def __init__(self, deck_data): # Khởi tạo thông tin ban đầu của người chơi
        self.hp = 100 # Khởi tạo lượng máu ban đầu của người chơi là 100
        self.deck = list(deck_data) # Khởi tạo bộ bài ban đầu
        self.hand = [] # Khởi tạo số lượng bài trên tay là rỗng
        random.shuffle(self.deck) # Xáo bài ngay khi bắt đầu trận

    def draw_card(self): # Rút 1 lá bài từ bộ bài lên tay
        if self.deck and len(self.hand) < 6: # Giới hạn số lá bài tối đa trên tay là 6
            return self.deck.pop()
        return None

class Board: # Lớp quản lý khu vực bàn cờ
    def __init__(self): # Khởi tạo bàn cờ với 4 ô trống và các khu vực phụ trợ
        self.slots = [None] * 4 # Tối đa 4 đơn vị trên sân
        self.env_buffs = []     # Danh sách các hiệu ứng môi trường đang kích hoạt
        self.graveyard = []     # Nơi chứa các lá bài đã bị tiêu diệt hoặc đã sử dụng
