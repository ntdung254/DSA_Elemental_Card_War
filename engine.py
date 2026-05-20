"""
Mô đun Engine xử lý logic cốt lõi của trò chơi.
Chịu trách nhiệm thực thi các phép toán giao tranh, tác dụng của thẻ bài, cập nhật chỉ số,
cũng như ra quyết định tự động cho đối thủ máy (Bot AI).
"""
import random

SPELL_TYPES = {
    "Inferno Shot": "ENEMY", "Tidal Impact": "ENEMY", "Thunder Strike": "ENEMY", "Air Cutter": "ENEMY", "Earth Crusher": "ENEMY",
    "Flame Rage": "ALLY", "Aqua Shield": "ALLY", "Overcharge": "ALLY", "Sonic Speed": "ALLY", "Stone Armor": "ALLY", "Burning Spirit": "ALLY", "Gaia Blessing": "ALLY",
    "Frozen Heart": "ENEMY", "Electric Drain": "ENEMY",
    "Meteor Collapse": "GLOBAL", "Chain Lightning": "GLOBAL", "Healing Rain": "GLOBAL", "Sky Dance": "GLOBAL", "Storm Pressure": "GLOBAL", "Mountain Pressure": "GLOBAL",
    "Final Judgement": "GLOBAL", "Ocean Blessing": "GLOBAL", "Wind Blessing": "GLOBAL",
    "Ancient Revival": "GRAVE_ALLY",
    "Phoenix Rebirth": "GRAVE_ALLY"
}

class GameEngine:
    """
    Lớp bao bọc các phương thức tĩnh (static methods) xử lý nghiệp vụ, 
    nhằm đảm bảo tính độc lập của logic trò chơi với các thành phần đồ họa (UI).
    """
    @staticmethod
    def get_spell_type(name):
        """
        Xác định phân loại mục tiêu của thẻ phép thuật dựa trên tên thẻ bài.
        Trả về các kiểu như: ENEMY, ALLY, GLOBAL, GRAVE_ALLY.
        """
        return SPELL_TYPES.get(name, "ENEMY")

    @staticmethod
    def calculate_stats(card, board_env, milestones):
        """
        Tính toán các chỉ số thực tế của thẻ bài Quái vật dựa trên trạng thái môi trường 
        bàn cờ và các mốc cộng hưởng (milestones) nguyên tố hiện tại.
        """
        stats_dict = card.get_current_stats(milestones, board_env)
        return {
            "atk": stats_dict["atk"]["current"], "def": stats_dict["def"]["current"],
            "hp": stats_dict["hp"]["current"], "spd": stats_dict["spd"]["current"],
            "eva": stats_dict["eva"]["current"], "cri": stats_dict["cri"]["current"]
        }

    @staticmethod
    def execute_combat(atk_card, def_card, atk_stats, def_stats):
        """
        Thực thi quy trình tính toán giao tranh giữa hai thực thể.
        Bao gồm kiểm tra tỷ lệ né tránh (evasion), tỷ lệ chí mạng (critical hit), 
        và tính toán lượng sát thương cuối cùng sau khi đã giảm trừ bởi giáp (defense).
        Trả về tuple: (Sát thương thực tế, cờ báo chí mạng, cờ báo trượt).
        """
        if random.randint(1, 100) <= def_stats["eva"]: return 0, False, True 
        is_crit = random.randint(1, 100) <= atk_stats["cri"]
        base_dmg = atk_stats["atk"] * 2 if is_crit else atk_stats["atk"]
        def_reduction = min(def_stats["def"], 80) / 100.0
        return max(1, int(base_dmg * (1 - def_reduction))), is_crit, False

    @staticmethod
    def execute_spell(card, target_card=None, caster_player=None, enemy_player=None, board=None, caster_side="PLAYER"):
        """
        Thực thi hiệu ứng của thẻ bài phép thuật lên các mục tiêu được chỉ định.
        Hỗ trợ đa dạng các loại hiệu ứng: Gây sát thương, Hồi phục, Buff chỉ số, 
        Debuff, sát thương diện rộng (AOE) và ảnh hưởng trực tiếp đến người chơi.
        """
        name = card.name
        ally_slots = board.player_slots if caster_side == "PLAYER" else board.bot_slots
        enemy_slots = board.bot_slots if caster_side == "PLAYER" else board.player_slots
        
        # 1. Gây sát thương
        if name in ["Inferno Shot", "Thunder Strike", "Earth Crusher"] and target_card: target_card.current_hp -= 30
        elif name in ["Tidal Impact", "Air Cutter"] and target_card: target_card.current_hp -= 25
        
        # 2. Hồi máu / Buff Đơn
        elif name == "Burning Spirit" and target_card:
            target_card.current_hp = min(target_card.stat_hp, target_card.current_hp + 25); target_card.stat_atk += 10
        elif name == "Gaia Blessing" and target_card:
            target_card.current_hp = min(target_card.stat_hp, target_card.current_hp + 30)
        elif name == "Flame Rage" and target_card: target_card.stat_atk += 15
        elif name == "Aqua Shield" and target_card: target_card.stat_def += 20
        elif name == "Overcharge" and target_card: target_card.stat_spd += 20; target_card.stat_atk += 10
        elif name == "Sonic Speed" and target_card: target_card.stat_spd += 25
        elif name == "Stone Armor" and target_card: target_card.stat_def += 25
            
        # 3. Debuff
        elif name == "Frozen Heart" and target_card: target_card.stat_atk -= 15; target_card.stat_spd -= 15
        elif name == "Electric Drain" and target_card: target_card.stat_def -= 20
            
        # 4. Kỹ năng diện rộng (AOE)
        elif name in ["Meteor Collapse", "Chain Lightning"]:
            for c in enemy_slots: 
                if c: c.current_hp -= 15
        elif name == "Healing Rain":
            for c in ally_slots:
                if c: c.current_hp = min(c.stat_hp, c.current_hp + 20)
        elif name == "Sky Dance":
            for c in ally_slots:
                if c: c.stat_eva += 20
        elif name == "Storm Pressure":
            for c in enemy_slots:
                if c: c.stat_spd -= 15
        elif name == "Mountain Pressure":
            for c in enemy_slots:
                if c: c.stat_atk -= 20
                    
        # 5. Tác dụng thẳng lên người chơi & Rút bài
        if name == "Final Judgement" and enemy_player: enemy_player.hp -= 50
        if name == "Ocean Blessing" and caster_player: caster_player.hp += 20
        
        # Ghi chú: Việc rút bài (Ocean Blessing, Wind Blessing) được xử lý trong main.py
        # với animation draw card, không xử lý ở đây nữa.

    @staticmethod
    def bot_ai_turn(bot, board):
        """
        Mô phỏng trí tuệ nhân tạo (AI) ra quyết định cho đối thủ máy trong lượt đi.
        Quy trình bao gồm: Triển khai thẻ môi trường, đánh quái vật vào các vị trí trống, 
        và sử dụng phép thuật lên các mục tiêu khả thi theo kịch bản tuyến tính.
        Trả về danh sách các hành động (actions) đã lên kế hoạch.
        """
        actions = []
        playable_monsters = [c for c in bot.hand if c.card_type == "Monster"]
        playable_envs = [c for c in bot.hand if c.card_type == "Environment"]
        playable_spells = [c for c in bot.hand if c.card_type == "Spell"]

        for env in playable_envs:
            empty_slots = [i for i in range(4) if not board.bot_env[i]]
            if empty_slots:
                slot = empty_slots[0]
                actions.append({"type": "ENV", "card": env, "target": slot, "side": "BOT"})
                board.bot_env[slot] = env.element
                bot.hand.remove(env)
                bot.pending_spells.append(env)

        for mon in playable_monsters:
            empty_slots = [i for i in range(4) if not board.bot_slots[i]]
            if empty_slots:
                slot = empty_slots[0]
                actions.append({"type": "SUMMON", "card": mon, "target": slot, "side": "BOT"})
                board.bot_slots[slot] = mon
                bot.hand.remove(mon)
                
        for spell in playable_spells:
            t_type = GameEngine.get_spell_type(spell.name)
            if t_type == "GLOBAL":
                actions.append({"type": "SPELL", "card": spell, "side": "BOT", "target_side": "GLOBAL"})
                bot.hand.remove(spell)
                bot.pending_spells.append(spell)
            elif t_type == "ENEMY":
                targets = [i for i in range(4) if board.player_slots[i]]
                if targets:
                    actions.append({"type": "SPELL", "card": spell, "target": targets[0], "side": "BOT", "target_side": "PLAYER"})
                    bot.hand.remove(spell)
                    bot.pending_spells.append(spell)
            elif t_type == "ALLY":
                targets = [i for i in range(4) if board.bot_slots[i]]
                if targets:
                    actions.append({"type": "SPELL", "card": spell, "target": targets[0], "side": "BOT", "target_side": "BOT"})
                    bot.hand.remove(spell)
                    bot.pending_spells.append(spell)
            elif t_type == "GRAVE_ALLY":
                dead_mons = [c for c in bot.graveyard if c.card_type == "Monster"]
                empty_slots = [i for i in range(4) if not board.bot_slots[i]]
                if dead_mons and empty_slots:
                    revived = dead_mons[0]
                    bot.graveyard.remove(revived)
                    revive_pct = 0.5 if spell.name == "Phoenix Rebirth" else 0.4
                    revived.current_hp = max(1, int(revived.stat_hp * revive_pct))
                    actions.append({"type": "SPELL", "card": spell, "target": empty_slots[0], "side": "BOT", "target_side": "BOT", "revived_card": revived})
                    bot.hand.remove(spell)
                    bot.pending_spells.append(spell)

        return actions
