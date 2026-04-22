# card_data.py
# Sinh viên thực hiện: Nguyễn Tấn Dũng - 25520368
# Môn học: IT003.Q21.CTTN - Đồ án: ELEMENTAL CARD WARS

from models import Card

# ==========================================
# 1. DANH SÁCH BÀI QUÁI VẬT (MONSTER CARDS)
# ==========================================

FIRE_MONSTERS = [
    Card("Sasuke Uchiha", "Monster", "Fire", "cards_list/fire_monster/sasuke_uchiha.png", stat_atk=30, stat_hp=15, stat_def=12, stat_spd=25, stat_eva=10, stat_cri=8),
    Card("Portgas D. Ace", "Monster", "Fire", "cards_list/fire_monster/portgas_d_ace.png", stat_atk=32, stat_hp=18, stat_def=10, stat_spd=20, stat_eva=10, stat_cri=10),
    Card("Kyojuro Rengoku", "Monster", "Fire", "cards_list/fire_monster/kyojuro_rengoku.png", stat_atk=36, stat_hp=16, stat_def=12, stat_spd=18, stat_eva=3, stat_cri=15),
    Card("Mereoleona Vermillion", "Monster", "Fire", "cards_list/fire_monster/mereoleona_vermillion.png", stat_atk=38, stat_hp=20, stat_def=10, stat_spd=22, stat_eva=5, stat_cri=5),
    Card("Natsu Dragneel", "Monster", "Fire", "cards_list/fire_monster/natsu_dragneel.png", stat_atk=33, stat_hp=20, stat_def=15, stat_spd=15, stat_eva=10, stat_cri=7),
    Card("Endeavor", "Monster", "Fire", "cards_list/fire_monster/endeavor.png", stat_atk=37, stat_hp=18, stat_def=15, stat_spd=15, stat_eva=5, stat_cri=10),
    Card("Feitan", "Monster", "Fire", "cards_list/fire_monster/feitan.png", stat_atk=30, stat_hp=12, stat_def=8, stat_spd=30, stat_eva=10, stat_cri=10),
    Card("Genryusai Yamamoto", "Monster", "Fire", "cards_list/fire_monster/genryusai_yamamoto.png", stat_atk=40, stat_hp=18, stat_def=15, stat_spd=10, stat_eva=2, stat_cri=15),
    Card("BoBoiBoy Blaze", "Monster", "Fire", "cards_list/fire_monster/boboiboy_blaze.png", stat_atk=31, stat_hp=16, stat_def=10, stat_spd=23, stat_eva=12, stat_cri=8),
    Card("Genos", "Monster", "Fire", "cards_list/fire_monster/genos.png", stat_atk=35, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=10, stat_cri=5)
]

WATER_MONSTERS = [
    Card("Kisame Hoshigaki", "Monster", "Water", "cards_list/water_monster/kisame_hoshigaki.png", stat_atk=25, stat_hp=35, stat_def=20, stat_spd=10, stat_eva=5, stat_cri=5),
    Card("Jinbe", "Monster", "Water", "cards_list/water_monster/jinbe.png", stat_atk=24, stat_hp=30, stat_def=25, stat_spd=10, stat_eva=6, stat_cri=5),
    Card("Tanjiro Kamado", "Monster", "Water", "cards_list/water_monster/tanjiro_kamado.png", stat_atk=22, stat_hp=24, stat_def=18, stat_spd=18, stat_eva=12, stat_cri=6),
    Card("Noelle Silva", "Monster", "Water", "cards_list/water_monster/noelle_silva.png", stat_atk=28, stat_hp=20, stat_def=15, stat_spd=17, stat_eva=15, stat_cri=5),
    Card("Juvia Lockser", "Monster", "Water", "cards_list/water_monster/juvia_lockser.png", stat_atk=18, stat_hp=26, stat_def=15, stat_spd=16, stat_eva=20, stat_cri=5),
    Card("Tsuyu Asui", "Monster", "Water", "cards_list/water_monster/tsuyu_asui.png", stat_atk=15, stat_hp=22, stat_def=12, stat_spd=18, stat_eva=28, stat_cri=5),
    Card("Morel Mackernasey", "Monster", "Water", "cards_list/water_monster/morel_mackernasey.png", stat_atk=20, stat_hp=28, stat_def=22, stat_spd=12, stat_eva=15, stat_cri=3),
    Card("Toshiro Hitsugaya", "Monster", "Water", "cards_list/water_monster/toshiro_hitsugaya.png", stat_atk=26, stat_hp=18, stat_def=15, stat_spd=22, stat_eva=12, stat_cri=7),
    Card("BoBoiBoy Water", "Monster", "Water", "cards_list/water_monster/boboiboy_water.png", stat_atk=18, stat_hp=25, stat_def=18, stat_spd=14, stat_eva=20, stat_cri=5),
    Card("Silver Fang", "Monster", "Water", "cards_list/water_monster/silver_fang.png", stat_atk=30, stat_hp=28, stat_def=20, stat_spd=12, stat_eva=5, stat_cri=5)
]

LIGHTNING_MONSTERS = [
    Card("Kakashi Hatake", "Monster", "Lightning", "cards_list/lightning_monster/kakashi_hatake.png", stat_atk=25, stat_hp=15, stat_def=15, stat_spd=25, stat_eva=10, stat_cri=10),
    Card("Enel", "Monster", "Lightning", "cards_list/lightning_monster/enel.png", stat_atk=30, stat_hp=15, stat_def=10, stat_spd=30, stat_eva=10, stat_cri=5),
    Card("Zenitsu Agatsuma", "Monster", "Lightning", "cards_list/lightning_monster/zenitsu_agatsuma.png", stat_atk=20, stat_hp=12, stat_def=8, stat_spd=35, stat_eva=5, stat_cri=20),
    Card("Luck Voltia", "Monster", "Lightning", "cards_list/lightning_monster/luck_voltia.png", stat_atk=24, stat_hp=15, stat_def=11, stat_spd=32, stat_eva=10, stat_cri=8),
    Card("Laxus Dreyar", "Monster", "Lightning", "cards_list/lightning_monster/laxus_dreyar.png", stat_atk=30, stat_hp=20, stat_def=15, stat_spd=20, stat_eva=5, stat_cri=10),
    Card("Denki Kaminari", "Monster", "Lightning", "cards_list/lightning_monster/denki_kaminari.png", stat_atk=22, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=8, stat_cri=20),
    Card("Killua Zoldyck", "Monster", "Lightning", "cards_list/lightning_monster/killua_zoldyck.png", stat_atk=22, stat_hp=15, stat_def=10, stat_spd=40, stat_eva=8, stat_cri=5),
    Card("Chojiro Sasakibe", "Monster", "Lightning", "cards_list/lightning_monster/chojiro_sasakibe.png", stat_atk=25, stat_hp=15, stat_def=15, stat_spd=25, stat_eva=10, stat_cri=10),
    Card("BoBoiBoy Lightning", "Monster", "Lightning", "cards_list/lightning_monster/boboiboy_lightning.png", stat_atk=23, stat_hp=16, stat_def=12, stat_spd=30, stat_eva=12, stat_cri=7),
    Card("Child Emperor", "Monster", "Lightning", "cards_list/lightning_monster/child_emperor.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=35, stat_eva=15, stat_cri=5)
]

WIND_MONSTERS = [
    Card("Temari", "Monster", "Wind", "cards_list/wind_monster/temari.png", stat_atk=22, stat_hp=18, stat_def=12, stat_spd=20, stat_eva=23, stat_cri=5),
    Card("Monkey D. Dragon", "Monster", "Wind", "cards_list/wind_monster/monkey_d_dragon.png", stat_atk=25, stat_hp=20, stat_def=15, stat_spd=20, stat_eva=20, stat_cri=0),
    Card("Sanemi Shinazugawa", "Monster", "Wind", "cards_list/wind_monster/sanemi_shinazugawa.png", stat_atk=28, stat_hp=15, stat_def=12, stat_spd=22, stat_eva=18, stat_cri=5),
    Card("Yuno Grinberryall", "Monster", "Wind", "cards_list/wind_monster/yuno_grinberryall.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=25, stat_cri=5),
    Card("Wendy Marvell", "Monster", "Wind", "cards_list/wind_monster/wendy_marvell.png", stat_atk=15, stat_hp=25, stat_def=15, stat_spd=20, stat_eva=20, stat_cri=5),
    Card("Inasa Yoarashi", "Monster", "Wind", "cards_list/wind_monster/inasa_yoarashi.png", stat_atk=24, stat_hp=18, stat_def=13, stat_spd=20, stat_eva=25, stat_cri=0),
    Card("Neferpitou", "Monster", "Wind", "cards_list/wind_monster/neferpitou.png", stat_atk=30, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=20, stat_cri=0),
    Card("Kensei Muguruma", "Monster", "Wind", "cards_list/wind_monster/kensei_muguruma.png", stat_atk=26, stat_hp=18, stat_def=12, stat_spd=24, stat_eva=20, stat_cri=0),
    Card("BoBoiBoy Cyclone", "Monster", "Wind", "cards_list/wind_monster/boboiboy_cyclone.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=25, stat_cri=5),
    Card("Tatsumaki", "Monster", "Wind", "cards_list/wind_monster/tatsumaki.png", stat_atk=35, stat_hp=10, stat_def=10, stat_spd=20, stat_eva=25, stat_cri=0)
]

EARTH_MONSTERS = [
    Card("Onoki", "Monster", "Earth", "cards_list/earth_monster/onoki.png", stat_atk=15, stat_hp=25, stat_def=35, stat_spd=10, stat_eva=10, stat_cri=5),
    Card("Pica", "Monster", "Earth", "cards_list/earth_monster/pica.png", stat_atk=15, stat_hp=30, stat_def=40, stat_spd=5, stat_eva=5, stat_cri=5),
    Card("Gyomei Himejima", "Monster", "Earth", "cards_list/earth_monster/gyomei_himejima.png", stat_atk=25, stat_hp=30, stat_def=30, stat_spd=10, stat_eva=2, stat_cri=3),
    Card("Sol Marron", "Monster", "Earth", "cards_list/earth_monster/sol_marron.png", stat_atk=18, stat_hp=28, stat_def=35, stat_spd=12, stat_eva=5, stat_cri=2),
    Card("Gajeel Redfox", "Monster", "Earth", "cards_list/earth_monster/gajeel_redfox.png", stat_atk=24, stat_hp=26, stat_def=35, stat_spd=10, stat_eva=3, stat_cri=2),
    Card("Cementoss", "Monster", "Earth", "cards_list/earth_monster/cementoss.png", stat_atk=15, stat_hp=25, stat_def=40, stat_spd=12, stat_eva=8, stat_cri=0),
    Card("Uvogin", "Monster", "Earth", "cards_list/earth_monster/uvogin.png", stat_atk=30, stat_hp=30, stat_def=30, stat_spd=5, stat_eva=2, stat_cri=3),
    Card("Sajin Komamura", "Monster", "Earth", "cards_list/earth_monster/sajin_komamura.png", stat_atk=25, stat_hp=35, stat_def=25, stat_spd=10, stat_eva=2, stat_cri=3),
    Card("BoBoiBoy Earth", "Monster", "Earth", "cards_list/earth_monster/boboiboy_earth.png", stat_atk=20, stat_hp=30, stat_def=35, stat_spd=10, stat_eva=5, stat_cri=0),
    Card("Superalloy Darkshine", "Monster", "Earth", "cards_list/earth_monster/superalloy_darkshine.png", stat_atk=25, stat_hp=25, stat_def=45, stat_spd=5, stat_eva=0, stat_cri=0)
]

# 2. DANH SÁCH BÀI PHÉP THUẬT (SPELL CARDS)

FIRE_SPELLS = [
]

WATER_SPELLS = [
]

LIGHTNING_SPELLS = [
]

WIND_SPELLS = [
]

EARTH_SPELLS = [
]

NEUTRAL_SPELLS = [
]

# ==========================================
# 3. TỔNG HỢP TOÀN BỘ DATA
# ==========================================
ALL_MONSTERS = FIRE_MONSTERS + WATER_MONSTERS + LIGHTNING_MONSTERS + WIND_MONSTERS + EARTH_MONSTERS
# ALL_SPELLS = FIRE_SPELLS + WATER_SPELLS + LIGHTNING_SPELLS + WIND_SPELLS + EARTH_SPELLS + NEUTRAL_SPELLS
FULL_DATABASE = ALL_MONSTERS #+ ALL_SPELLS