import random
import math

class AnimationManager: # Quản lý các trạng thái rung màn hình và các hiệu ứng chuyển động.
    def __init__(self): # Khởi tạo ban đầu
        self.shake_timer = 0
        self.shake_intensity = 0

    def start_shake(self, duration=15, intensity=15): # Thiết lập thời gian và cường độ rung
        self.shake_timer = duration
        self.shake_intensity = intensity

    def get_shake_offset(self): # Tính toán tọa độ lệch ngẫu nhiên dựa trên cường độ rung hiện tại
        if self.shake_timer > 0:
            self.shake_timer -= 1
            return random.randint(-self.shake_intensity, self.shake_intensity), \
                   random.randint(-self.shake_intensity, self.shake_intensity)
        return 0, 0

    def get_pulse(self, current_time, speed=0.003): # Tính toán giá trị nhịp đập (hiện tại chưa dùng)
        return (math.sin(current_time * speed) + 1) / 2

    def get_blink(self, current_time, speed=0.005): # Tính toán giá trị nhấp nháy cho ô cờ (Khi summon)
        return (math.sin(current_time * speed) + 1) / 2
