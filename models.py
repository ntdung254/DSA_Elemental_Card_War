import pygame
import random
from PIL import Image 

class Card:
    """
    Lớp đại diện cho một lá bài trong trò chơi.
    
    Lớp này không chỉ lưu trữ các thông số chiến đấu (ATK, DEF, HP...) mà còn
    xử lý hình ảnh bằng Pillow để đảm bảo độ sắc nét (anti-aliasing) khi hiển thị 
    trên các kích thước khác nhau (trên tay vs. trên bàn cờ).
    """
    def __init__(self, name, card_type, element, image_path, stat_atk=0, stat_def=0, stat_hp=0, stat_cri=0, stat_eva=0, stat_spd=0, description=""):
        """
        Khởi tạo một thực thể Card mới.

        Args:
            name (str): Tên lá bài.
            card_type (str): Loại bài (ví dụ: Unit, Spell, Trap).
            element (str): Hệ nguyên tố (Fire, Water, Earth, Lightning, Wind).
            image_path (str): Đường dẫn đến file ảnh gốc.
            stat_atk (int): Chỉ số tấn công cơ bản.
            stat_def (int): Chỉ số phòng thủ.
            stat_hp (int): Chỉ số máu.
            stat_cri (int): Tỷ lệ chí mạng.
            stat_eva (int): Tỷ lệ né tránh.
            stat_spd (int): Tốc độ hành động.
            description (str): Nội dung mô tả kỹ năng hoặc lore của bài.
        """
        self.name = name # Tên lá bài
        self.card_type = card_type # Loại bài (ví dụ: Unit, Spell, Trap)
        self.element = element # Hệ nguyên tố (Fire, Water, Earth, Lightning, Wind)

        self.base_atk = stat_atk
        self.base_def = stat_def
        self.base_hp = stat_hp # Máu tối đa gốc
        self.base_spd = stat_spd
        self.base_cri = stat_cri
        self.base_eva = stat_eva

        self.stat_atk = stat_atk
        self.stat_def = stat_def # Chỉ số phòng thủ
        self.stat_hp = stat_hp # Chỉ số máu
        self.stat_cri = stat_cri # Chỉ số  chí mạng
        self.stat_eva = stat_eva # Chỉ số  né tránh
        self.stat_spd = stat_spd # Chỉ số  tốc độ
        self.description = description # Nội dung mô tả kỹ năng của bài

        try:
            # SỬ DỤNG PILLOW ĐỂ RESIZE VỚI THUẬT TOÁN LANCZOS (CỰC NÉT)
            pil_img = Image.open(image_path).convert("RGBA")
            
            # Kích thước cho bài trên tay (Nhỏ gọn để dễ quản lý)
            hand_res = pil_img.resize((130, 180), Image.LANCZOS)
            # Kích thước cho bài trên bàn cờ (Lớn hơn để nhìn rõ chi tiết)
            board_res = pil_img.resize((160, 210), Image.LANCZOS)
            
            # Chuyển ngược lại Pygame Surface để render
            self.image_hand = pygame.image.fromstring(hand_res.tobytes(), hand_res.size, hand_res.mode).convert_alpha()
            self.image_board = pygame.image.fromstring(board_res.tobytes(), board_res.size, board_res.mode).convert_alpha()
            
            self.image_path = image_path 
            
        except Exception as e:
            print(f"Lỗi load ảnh {name}: {e}")
            # Fallback: Tạo mặt bài trống nếu không load được ảnh
            self.image_hand = pygame.Surface((130, 180))
            self.image_hand.fill((200, 100, 100))
            self.image_board = pygame.Surface((160, 210))
            self.image_board.fill((200, 100, 100))

class Player:
    """
    Lớp quản lý thông tin và hành động của người chơi.
    
    Bao gồm việc quản lý lượng máu (HP), bộ bài (Deck) và các lá bài đang cầm trên tay (Hand).
    """
    def __init__(self, deck_data):
        """
        Khởi tạo người chơi với một bộ bài cho trước.

        Args:
            deck_data (list): Danh sách các đối tượng Card cấu thành bộ bài.
        """
        self.hp = 1000
        self.deck = deck_data 
        self.hand = []
        random.shuffle(self.deck) # Xáo bài ngay khi bắt đầu trận

    def draw_card(self):
        """
        Rút một lá bài từ bộ bài lên tay.

        Returns:
            Card: Đối tượng lá bài vừa rút nếu thành công, ngược lại trả về None.
            Giới hạn bài trên tay tối đa là 5 lá.
        """
        if self.deck and len(self.hand) < 5:
            return self.deck.pop()
        return None

class Board:
    """
    Lớp quản lý khu vực bàn cờ và logic môi trường chiến đấu.
    
    Chịu trách nhiệm quản lý các quân bài đang tham chiến, tính toán buff 
    nguyên tố dựa trên sự tương tác giữa các lá bài và môi trường xung quanh.
    """
    def __init__(self):
        """Khởi tạo bàn cờ với 4 ô trống và các khu vực phụ trợ."""
        self.slots = [None] * 4 # Tối đa 4 đơn vị trên sân
        self.env_buffs = []     # Danh sách các hiệu ứng môi trường đang kích hoạt
        self.graveyard = []     # Nơi chứa các lá bài đã bị tiêu diệt hoặc đã sử dụng

    def update_environment(self):
        """
        Cập nhật chỉ số của các lá bài dựa trên cơ chế cộng hưởng nguyên tố.
        
        Thuật toán:
        1. Đếm tổng số lượng nguyên tố xuất hiện từ bài trên sân và buff môi trường.
        2. So sánh với các mốc kích hoạt:
           - Mốc 2 đơn vị cùng hệ: Tăng 10 ATK.
           - Mốc 4 đơn vị cùng hệ: Tăng 30 ATK.
        """
        element_counts = {"Fire": 0, "Water": 0, "Earth": 0, "Lightning": 0, "Wind": 0}
        
        # Đếm nguyên tố từ buff môi trường
        for env in self.env_buffs: 
            element_counts[env.element] += 1
            
        # Đếm nguyên tố từ các lá bài đang nằm trong slot
        for card in self.slots:
            if card: 
                element_counts[card.element] += 1

        # Áp dụng buff chỉ số (Reset về base trước khi cộng dồn mới)
        for card in self.slots:
            if card:
                card.stat_atk = card.base_atk
                count = element_counts.get(card.element, 0)
                if count >= 4: 
                    card.stat_atk += 30
                elif count >= 2: 
                    card.stat_atk += 10