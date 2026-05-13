"""
Mô đun quản lý các hiệu ứng hoạt hình (animations) trong trò chơi.
Cung cấp bộ máy xử lý các trạng thái đồ họa chuyển động như tấn công, nhấp nháy, hy sinh, triệu hồi và rung lắc màn hình/thực thể.
"""
import random
import math

class AnimationManager:
    """
    Lớp quản lý tập trung các tiến trình và trạng thái hiệu ứng hoạt hình.
    Lưu trữ và cập nhật liên tục các thông số đồ họa cho từng thực thể (thẻ bài) và toàn cục (màn hình).
    """
    def __init__(self):
        """
        Khởi tạo bộ quản lý hiệu ứng. Thiết lập các từ điển (dictionary) lưu trữ 
        trạng thái của các loại hiệu ứng khác nhau và các biến kiểm soát toàn cục.
        """
        self.combat_anims = {} 
        self.flash_anims = {}  
        self.death_anims = {}
        self.entity_shakes = {}
        
        self.summon_anims = {}
        self.global_shake = {'timer': 0, 'intensity': 0}
        self.red_flash_alpha = 0
        
    def start_attack_bump(self, entity, target_entity, target_y_dir):
        """
        Khởi động hiệu ứng va chạm khi tấn công cho một thực thể cụ thể.
        Ghi nhận tiến trình, hướng tấn công và mục tiêu để tính toán tọa độ nội suy.
        """
        self.combat_anims[entity] = {'progress': 0, 'dir': target_y_dir, 'target': target_entity, 'impacted': False}

    def start_flash(self, entity):
        """
        Kích hoạt hiệu ứng nhấp nháy (flash) cho một thực thể, thường dùng khi nhận sát thương hoặc hiệu ứng đặc biệt.
        """
        self.flash_anims[entity] = 1.0

    def start_death(self, entity):
        """
        Khởi tạo hiệu ứng tan biến (hy sinh) cho thực thể khi lượng máu (HP) bằng 0.
        """
        self.death_anims[entity] = 1.0

    def start_summon(self, entity):
        """
        Bắt đầu hiệu ứng triệu hồi thực thể lên bàn cờ với tiến trình từ 0.0 đến 1.0.
        """
        self.summon_anims[entity] = 0.0

    def start_entity_shake(self, entity, duration=15, intensity=8):
        """
        Thiết lập hiệu ứng rung lắc cục bộ cho một thực thể (thường do chịu tác động vật lý).
        """
        self.entity_shakes[entity] = {'timer': duration, 'intensity': intensity}

    # Đã thêm cờ flash_red để chỉ báo nháy đỏ khi bị tấn công
    def start_global_shake(self, duration=20, intensity=15, flash_red=True):
        """
        Kích hoạt hiệu ứng rung lắc toàn màn hình (global shake) kèm cảnh báo nhấp nháy đỏ (nếu được chỉ định).
        Dùng cho các sự kiện sát thương lớn hoặc đánh trực tiếp vào người chơi.
        """
        self.global_shake = {'timer': duration, 'intensity': intensity}
        if flash_red:
            self.red_flash_alpha = 150 

    def update(self):
        """
        Cập nhật toàn bộ trạng thái hiệu ứng theo mỗi khung hình (frame).
        Xử lý tăng/giảm các biến số tiến trình và dọn dẹp các hiệu ứng đã hoàn tất.
        Trả về danh sách các va chạm (impacts) được ghi nhận trong khung hình hiện tại.
        """
        impacts = []
        for ent, an in list(self.combat_anims.items()):
            an['progress'] += 0.04 # GIẢM TỐC ĐỘ TẤN CÔNG GẤP ĐÔI (Từ 0.08 xuống 0.04)
            if an['progress'] >= 0.45 and not an['impacted']:
                an['impacted'] = True
                impacts.append((ent, an['target'])) 
            if an['progress'] >= 1.0:
                del self.combat_anims[ent]

        for ent, alpha in list(self.flash_anims.items()):
            self.flash_anims[ent] -= 0.05
            if self.flash_anims[ent] <= 0: del self.flash_anims[ent]

        for ent, alpha in list(self.death_anims.items()):
            self.death_anims[ent] -= 0.04
            if self.death_anims[ent] <= 0: del self.death_anims[ent]
            
        for ent, prog in list(self.summon_anims.items()):
            self.summon_anims[ent] += 0.05 
            if self.summon_anims[ent] >= 1.0: del self.summon_anims[ent]

        for ent, sh in list(self.entity_shakes.items()):
            if sh['timer'] > 0: sh['timer'] -= 1
            else: del self.entity_shakes[ent]
            
        if self.global_shake['timer'] > 0:
            self.global_shake['timer'] -= 1
            
        if self.red_flash_alpha > 0:
            self.red_flash_alpha -= 5 
            if self.red_flash_alpha < 0: self.red_flash_alpha = 0

        return impacts

    def get_attack_offset(self, entity):
        """
        Tính toán và trả về độ lệch tọa độ Y của thực thể dựa trên tiến trình của hoạt ảnh tấn công.
        Sử dụng hàm lượng giác để tạo độ cong mượt mà cho chuyển động.
        """
        if entity in self.combat_anims:
            p = self.combat_anims[entity]['progress']
            dir_y = self.combat_anims[entity]['dir']
            if p < 0.3: offset = -(math.sin((p / 0.3) * math.pi / 2)) * 30 * dir_y
            elif p < 0.5: offset = (-30 + 110 * ((p - 0.3) / 0.2)) * dir_y
            elif p < 0.8: offset = (80 - 40 * ((p - 0.5) / 0.3)) * dir_y
            else: offset = (40 - 40 * ((p - 0.8) / 0.2)) * dir_y
            return int(offset)
        return 0

    def get_entity_shake(self, entity):
        """
        Lấy giá trị ngẫu nhiên độ lệch tọa độ (X, Y) để tạo hiệu ứng rung cục bộ cho thực thể.
        """
        if entity in self.entity_shakes:
            sh = self.entity_shakes[entity]
            if sh['timer'] > 0:
                return random.randint(-sh['intensity'], sh['intensity']), random.randint(-sh['intensity'], sh['intensity'])
        return 0, 0
        
    def get_global_shake_offset(self):
        """
        Lấy giá trị ngẫu nhiên độ lệch tọa độ (X, Y) để tạo hiệu ứng rung toàn màn hình.
        """
        if self.global_shake['timer'] > 0:
            i = self.global_shake['intensity']
            return random.randint(-i, i), random.randint(-i, i)
        return 0, 0

    def get_death_alpha(self, entity):
        """
        Lấy giá trị độ mờ (alpha channel, 0-255) cho hoạt ảnh hy sinh của thực thể.
        """
        return int(self.death_anims.get(entity, 0) * 255)
        
    def get_summon_progress(self, entity):
        """
        Trả về tiến trình triệu hồi (từ 0.0 đến 1.0) của một thực thể.
        """
        return self.summon_anims.get(entity, 1.0) 

    def get_flash_alpha(self, entity):
        """
        Lấy giá trị độ mờ (alpha channel, 0-255) cho hoạt ảnh nhấp nháy của thực thể.
        """
        return int(self.flash_anims.get(entity, 0) * 255)

    def get_blink(self, current_time, speed=0.005):
        """
        Tính toán hệ số nhấp nháy nhịp nhàng theo thời gian thực dựa trên hàm sin.
        Dùng cho các chỉ báo nổi bật hoặc viền chọn mục tiêu.
        """
        return (math.sin(current_time * speed) + 1) / 2
