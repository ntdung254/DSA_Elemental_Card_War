"""
Mô đun khai báo các hằng số cấu hình.
Bao gồm các thông số khởi tạo màn hình, cài đặt tốc độ khung hình (FPS), 
mã màu mặc định và tọa độ tĩnh dùng cho hệ thống giao diện UI.
"""
import pygame

# Screen Configuration
WIDTH, HEIGHT = 1920, 1080
FPS = 60


# Colors
COLOR_BG = (10, 12, 18)
COLOR_PANEL = (15, 20, 30)
COLOR_BORDER = (200, 200, 200)
COLOR_TEXT_BASE = (255, 255, 255)
COLOR_SUMMON = (34, 139, 34)

# Default Coordinates
DECK_POS = (1550, 850)
GRAVE_POS = (1700, 850)
HAND_START_X = 250
BOARD_START_X = 400
BOARD_Y = 420
