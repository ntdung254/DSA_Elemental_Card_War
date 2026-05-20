"""
Mô đun cơ sở dữ liệu thẻ bài.
Định nghĩa và khởi tạo toàn bộ kho thẻ (Card pool) của hệ thống bao gồm: 
Thẻ Quái vật (Monster), Thẻ Phép thuật (Spell), và Thẻ Môi trường (Environment) 
được phân loại theo ngũ hành nguyên tố (Fire, Water, Lightning, Wind, Earth).
"""
from models import Card

# Monster Cards
FIRE_MONSTERS = [
    Card("Sasuke Uchiha", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/sasuke_uchiha.png", stat_atk=30, stat_hp=15, stat_def=12, stat_spd=25, stat_eva=10, stat_cri=8),
    Card("Portgas D. Ace", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/portgas_d_ace.png", stat_atk=32, stat_hp=18, stat_def=10, stat_spd=20, stat_eva=10, stat_cri=10),
    Card("Kyojuro Rengoku", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/kyojuro_rengoku.png", stat_atk=36, stat_hp=16, stat_def=12, stat_spd=18, stat_eva=3, stat_cri=15),
    Card("Mereoleona Vermillion", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/mereoleona_vermillion.png", stat_atk=38, stat_hp=20, stat_def=10, stat_spd=22, stat_eva=5, stat_cri=5),
    Card("Natsu Dragneel", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/natsu_dragneel.png", stat_atk=33, stat_hp=20, stat_def=15, stat_spd=15, stat_eva=10, stat_cri=7),
    Card("Endeavor", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/endeavor.png", stat_atk=37, stat_hp=18, stat_def=15, stat_spd=15, stat_eva=5, stat_cri=10),
    Card("Feitan", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/feitan.png", stat_atk=30, stat_hp=12, stat_def=8, stat_spd=30, stat_eva=10, stat_cri=10),
    Card("Genryusai Yamamoto", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/genryusai_yamamoto.png", stat_atk=40, stat_hp=18, stat_def=15, stat_spd=10, stat_eva=2, stat_cri=15),
    Card("BoBoiBoy Blaze", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/boboiboy_blaze.png", stat_atk=31, stat_hp=16, stat_def=10, stat_spd=23, stat_eva=12, stat_cri=8),
    Card("Genos", "Monster", "Fire", "assets/cards_list/monster_cards/fire_monster/genos.png", stat_atk=35, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=10, stat_cri=5)
]

WATER_MONSTERS = [
    Card("Kisame Hoshigaki", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/kisame_hoshigaki.png", stat_atk=25, stat_hp=35, stat_def=20, stat_spd=10, stat_eva=5, stat_cri=5),
    Card("Jinbe", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/jinbe.png", stat_atk=24, stat_hp=30, stat_def=25, stat_spd=10, stat_eva=6, stat_cri=5),
    Card("Tanjiro Kamado", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/tanjiro_kamado.png", stat_atk=22, stat_hp=24, stat_def=18, stat_spd=18, stat_eva=12, stat_cri=6),
    Card("Noelle Silva", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/noelle_silva.png", stat_atk=28, stat_hp=20, stat_def=15, stat_spd=17, stat_eva=15, stat_cri=5),
    Card("Juvia Lockser", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/juvia_lockser.png", stat_atk=18, stat_hp=26, stat_def=15, stat_spd=16, stat_eva=20, stat_cri=5),
    Card("Tsuyu Asui", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/tsuyu_asui.png", stat_atk=15, stat_hp=22, stat_def=12, stat_spd=18, stat_eva=28, stat_cri=5),
    Card("Morel Mackernasey", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/morel_mackernasey.png", stat_atk=20, stat_hp=28, stat_def=22, stat_spd=12, stat_eva=15, stat_cri=3),
    Card("Toshiro Hitsugaya", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/toshiro_hitsugaya.png", stat_atk=26, stat_hp=18, stat_def=15, stat_spd=22, stat_eva=12, stat_cri=7),
    Card("BoBoiBoy Water", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/boboiboy_water.png", stat_atk=18, stat_hp=25, stat_def=18, stat_spd=14, stat_eva=20, stat_cri=5),
    Card("Silver Fang", "Monster", "Water", "assets/cards_list/monster_cards/water_monster/silver_fang.png", stat_atk=30, stat_hp=28, stat_def=20, stat_spd=12, stat_eva=5, stat_cri=5)
]

LIGHTNING_MONSTERS = [
    Card("Kakashi Hatake", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/kakashi_hatake.png", stat_atk=25, stat_hp=15, stat_def=15, stat_spd=25, stat_eva=10, stat_cri=10),
    Card("Enel", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/enel.png", stat_atk=30, stat_hp=15, stat_def=10, stat_spd=30, stat_eva=10, stat_cri=5),
    Card("Zenitsu Agatsuma", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/zenitsu_agatsuma.png", stat_atk=20, stat_hp=12, stat_def=8, stat_spd=35, stat_eva=5, stat_cri=20),
    Card("Luck Voltia", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/luck_voltia.png", stat_atk=24, stat_hp=15, stat_def=11, stat_spd=32, stat_eva=10, stat_cri=8),
    Card("Laxus Dreyar", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/laxus_dreyar.png", stat_atk=30, stat_hp=20, stat_def=15, stat_spd=20, stat_eva=5, stat_cri=10),
    Card("Denki Kaminari", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/denki_kaminari.png", stat_atk=22, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=8, stat_cri=20),
    Card("Killua Zoldyck", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/killua_zoldyck.png", stat_atk=22, stat_hp=15, stat_def=10, stat_spd=40, stat_eva=8, stat_cri=5),
    Card("Chojiro Sasakibe", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/chojiro_sasakibe.png", stat_atk=25, stat_hp=15, stat_def=15, stat_spd=25, stat_eva=10, stat_cri=10),
    Card("BoBoiBoy Lightning", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/boboiboy_lightning.png", stat_atk=23, stat_hp=16, stat_def=12, stat_spd=30, stat_eva=12, stat_cri=7),
    Card("Child Emperor", "Monster", "Lightning", "assets/cards_list/monster_cards/lightning_monster/child_emperor.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=35, stat_eva=15, stat_cri=5)
]

WIND_MONSTERS = [
    Card("Temari", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/temari.png", stat_atk=22, stat_hp=18, stat_def=12, stat_spd=20, stat_eva=23, stat_cri=5),
    Card("Monkey D. Dragon", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/monkey_d_dragon.png", stat_atk=25, stat_hp=20, stat_def=15, stat_spd=20, stat_eva=20, stat_cri=0),
    Card("Sanemi Shinazugawa", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/sanemi_shinazugawa.png", stat_atk=28, stat_hp=15, stat_def=12, stat_spd=22, stat_eva=18, stat_cri=5),
    Card("Yuno Grinberryall", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/yuno_grinberryall.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=25, stat_cri=5),
    Card("Wendy Marvell", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/wendy_marvell.png", stat_atk=15, stat_hp=25, stat_def=15, stat_spd=20, stat_eva=20, stat_cri=5),
    Card("Inasa Yoarashi", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/inasa_yoarashi.png", stat_atk=24, stat_hp=18, stat_def=13, stat_spd=20, stat_eva=25, stat_cri=0),
    Card("Neferpitou", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/neferpitou.png", stat_atk=30, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=20, stat_cri=0),
    Card("Kensei Muguruma", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/kensei_muguruma.png", stat_atk=26, stat_hp=18, stat_def=12, stat_spd=24, stat_eva=20, stat_cri=0),
    Card("BoBoiBoy Cyclone", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/boboiboy_cyclone.png", stat_atk=20, stat_hp=15, stat_def=10, stat_spd=25, stat_eva=25, stat_cri=5),
    Card("Tatsumaki", "Monster", "Wind", "assets/cards_list/monster_cards/wind_monster/tatsumaki.png", stat_atk=35, stat_hp=10, stat_def=10, stat_spd=20, stat_eva=25, stat_cri=0)
]

EARTH_MONSTERS = [
    Card("Onoki", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/onoki.png", stat_atk=15, stat_hp=25, stat_def=35, stat_spd=10, stat_eva=10, stat_cri=5),
    Card("Pica", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/pica.png", stat_atk=15, stat_hp=30, stat_def=40, stat_spd=5, stat_eva=5, stat_cri=5),
    Card("Gyomei Himejima", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/gyomei_himejima.png", stat_atk=25, stat_hp=30, stat_def=30, stat_spd=10, stat_eva=2, stat_cri=3),
    Card("Sol Marron", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/sol_marron.png", stat_atk=18, stat_hp=28, stat_def=35, stat_spd=12, stat_eva=5, stat_cri=2),
    Card("Gajeel Redfox", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/gajeel_redfox.png", stat_atk=24, stat_hp=26, stat_def=35, stat_spd=10, stat_eva=3, stat_cri=2),
    Card("Cementoss", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/cementoss.png", stat_atk=15, stat_hp=25, stat_def=40, stat_spd=12, stat_eva=8, stat_cri=0),
    Card("Uvogin", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/uvogin.png", stat_atk=30, stat_hp=30, stat_def=30, stat_spd=5, stat_eva=2, stat_cri=3),
    Card("Sajin Komamura", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/sajin_komamura.png", stat_atk=25, stat_hp=35, stat_def=25, stat_spd=10, stat_eva=2, stat_cri=3),
    Card("BoBoiBoy Earth", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/boboiboy_earth.png", stat_atk=20, stat_hp=30, stat_def=35, stat_spd=10, stat_eva=5, stat_cri=0),
    Card("Superalloy Darkshine", "Monster", "Earth", "assets/cards_list/monster_cards/earth_monster/superalloy_darkshine.png", stat_atk=25, stat_hp=25, stat_def=45, stat_spd=5, stat_eva=0, stat_cri=0)
]

# Environment Cards
ENVIRONMENT_CARDS = [
    Card("Inferno Forge", "Environment", "Fire", 
         "assets/cards_list/environment_cards/fire_environment.png",
         description="Basic: +10 ATK. Fire Resonance: +15 CRI."),

    Card("Abyssal Tide Basin", "Environment", "Water", 
         "assets/cards_list/environment_cards/water_environment.png",
         description="Basic: Heal 8 HP/turn. Water Resonance: +15 EV."),

    Card("Thunderbolt Reactor", "Environment", "Lightning", 
         "assets/cards_list/environment_cards/lightning_environment.png",
         description="Basic: +10 SPD. Electric Resonance: 30% Stun chance."),

    Card("Hurricane Eye Plateau", "Environment", "Wind", 
         "assets/cards_list/environment_cards/wind_environment.png",
         description="Basic: +20 EV. Wind Resonance: Ignore 20% DEF."),

    Card("Diamond Crag Fortress", "Environment", "Earth", 
         "assets/cards_list/environment_cards/earth_environment.png",
         description="Basic: +20 DEF. Earth Resonance: Status Immune.")
]

# Spell Cards
FIRE_SPELLS = [
    Card("Flame Rage", "Spell", "Fire", "assets/cards_list/spell_cards/fire_spell/flame_rage.png", description="+15 ATK to 1 allied monster for 2 turns"),
    Card("Inferno Shot", "Spell", "Fire", "assets/cards_list/spell_cards/fire_spell/inferno_shot.png", description="Deal 30 damage to 1 enemy monster"),
    Card("Burning Spirit", "Spell", "Fire", "assets/cards_list/spell_cards/fire_spell/burning_spirit.png", description="Heal 25 HP to 1 allied monster. +10 ATK for 1 turn"),
    Card("Meteor Collapse", "Spell", "Fire", "assets/cards_list/spell_cards/fire_spell/meteor_collapse.png", description="Deal 15 damage to all enemy monsters"),
    Card("Phoenix Rebirth", "Spell", "Fire", "assets/cards_list/spell_cards/fire_spell/phoenix_rebirth.png", description="Revive 1 allied monster with 50% HP")
]

WATER_SPELLS = [
    Card("Aqua Shield", "Spell", "Water", "assets/cards_list/spell_cards/water_spell/aqua_shield.png", description="+20 DEF to 1 allied monster for 2 turns"),
    Card("Tidal Impact", "Spell", "Water", "assets/cards_list/spell_cards/water_spell/tidal_impact.png", description="Deal 25 damage to 1 enemy monster"),
    Card("Healing Rain", "Spell", "Water", "assets/cards_list/spell_cards/water_spell/healing_rain.png", description="Heal 20 HP to all allied monsters"),
    Card("Frozen Heart", "Spell", "Water", "assets/cards_list/spell_cards/water_spell/frozen_heart.png", description="Reduce 15 ATK and 15 SPD of 1 enemy monster"),
    Card("Ocean Blessing", "Spell", "Water", "assets/cards_list/spell_cards/water_spell/ocean_blessing.png", description="Draw 2 cards. Heal player by 20 LP")
]

LIGHTNING_SPELLS = [
    Card("Thunder Strike", "Spell", "Lightning", "assets/cards_list/spell_cards/lightning_spell/thunder_strike.png", description="Deal 30 damage to 1 enemy monster"),
    Card("Overcharge", "Spell", "Lightning", "assets/cards_list/spell_cards/lightning_spell/overcharge.png", description="+20 SPD and +10 ATK to 1 allied monster"),
    Card("Chain Lightning", "Spell", "Lightning", "assets/cards_list/spell_cards/lightning_spell/chain_lightning.png", description="Deal 15 damage to all enemy monsters"),
    Card("Electric Drain", "Spell", "Lightning", "assets/cards_list/spell_cards/lightning_spell/electric_drain.png", description="Reduce 20 DEF of 1 enemy monster"),
    Card("Final Judgement", "Spell", "Lightning", "assets/cards_list/spell_cards/lightning_spell/final_judgement.png", description="Deal 50 damage to enemy player")
]

WIND_SPELLS = [
    Card("Sonic Speed", "Spell", "Wind", "assets/cards_list/spell_cards/wind_spell/sonic_speed.png", description="+25 SPD to 1 allied monster"),
    Card("Air Cutter", "Spell", "Wind", "assets/cards_list/spell_cards/wind_spell/air_cutter.png", description="Deal 25 damage to 1 enemy monster"),
    Card("Sky Dance", "Spell", "Wind", "assets/cards_list/spell_cards/wind_spell/sky_dance.png", description="+20 EVA to all allied monsters"),
    Card("Storm Pressure", "Spell", "Wind", "assets/cards_list/spell_cards/wind_spell/storm_pressure.png", description="Reduce 15 SPD of all enemy monsters"),
    Card("Wind Blessing", "Spell", "Wind", "assets/cards_list/spell_cards/wind_spell/wind_blessing.png", description="Draw 2 cards")
]

EARTH_SPELLS = [
    Card("Stone Armor", "Spell", "Earth", "assets/cards_list/spell_cards/earth_spell/stone_armor.png", description="+25 DEF to 1 allied monster"),
    Card("Earth Crusher", "Spell", "Earth", "assets/cards_list/spell_cards/earth_spell/earth_crusher.png", description="Deal 30 damage to 1 enemy monster"),
    Card("Gaia Blessing", "Spell", "Earth", "assets/cards_list/spell_cards/earth_spell/gaia_blessing.png", description="Heal 30 HP to 1 allied monster"),
    Card("Mountain Pressure", "Spell", "Earth", "assets/cards_list/spell_cards/earth_spell/mountain_pressure.png", description="Reduce 20 ATK of all enemy monsters"),
    Card("Ancient Revival", "Spell", "Earth", "assets/cards_list/spell_cards/earth_spell/ancient_revival.png", description="Revive 1 allied monster with 40% HP")
]

NEUTRAL_SPELLS = []

# All Data
ALL_MONSTERS = FIRE_MONSTERS + WATER_MONSTERS + LIGHTNING_MONSTERS + WIND_MONSTERS + EARTH_MONSTERS
ALL_SPELLS = FIRE_SPELLS + WATER_SPELLS + LIGHTNING_SPELLS + WIND_SPELLS + EARTH_SPELLS + NEUTRAL_SPELLS
FULL_DATABASE = ALL_MONSTERS + ENVIRONMENT_CARDS + ALL_SPELLS
