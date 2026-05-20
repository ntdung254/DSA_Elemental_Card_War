# ⚔️ ELEMENTAL CARD WARS

> A turn-based elemental card strategy game built with **Python + Pygame**, featuring:
>
> 🔥 Tactical combat  
> 🌎 Elemental resonance system  
> 🤖 AI opponent  
> 🌐 LAN multiplayer mode  
> ✨ Cinematic animations and visual effects  

---

# 📌 Overview

**Elemental Card Wars** is a strategic card battle game where two players compete on a battlefield using monsters, spells, and elemental environments.

The game combines:
- Turn-based tactics
- Simultaneous action reveal
- Elemental synergy
- Real-time visual effects
- Multiplayer networking

Each player starts with **200 HP**, and the objective is simple:

> 💀 Reduce the opponent’s HP to 0 before yours reaches zero.

---

# 🎮 Core Gameplay

## 🃏 Card Types

The game contains 3 major card categories:

### ⚔️ Monster Cards
Main combat units with elemental attributes:
- 🔥 Fire
- 💧 Water
- ⚡ Lightning
- 🌪 Wind
- 🌍 Earth

Each monster has:
- ATK — Attack
- DEF — Damage Reduction
- HP — Health
- SPD — Attack Speed
- EVA — Evasion Rate
- CRI — Critical Hit Rate

---

### ✨ Spell Cards
One-time use cards that can:
- Deal damage
- Heal allies
- Buff stats
- Debuff enemies
- Revive monsters
- Affect the entire battlefield

---

### 🌎 Environment Cards
Special terrain cards that create elemental resonance.

Monsters standing on matching environments gain bonus stats.

---

# 🧠 Elemental Resonance System

One of the game's main mechanics is the **Milestone Resonance System**.

Each time an Environment Card is activated:
- The corresponding elemental milestone increases
- Bonus stats scale higher and higher

### Resonance Levels
| Level | Bonus |
|---|---|
| 1 | +20% |
| 2 | +50% |
| 3 | +100% |
| 4 | +200% |

This system encourages:
- Element specialization
- Strategic deck building
- Long-term battlefield control

---

# ⚙️ Turn Structure

Each round is divided into 4 phases:

## 1️⃣ Setup Phase
Players secretly:
- Summon monsters
- Place environment cards
- Prepare spells

---

## 2️⃣ Reveal Phase
Both players reveal actions simultaneously.

Spells and environments activate first.

---

## 3️⃣ Battle Phase
Combat occurs lane by lane.

Rules:
- Higher SPD attacks first
- Empty opposing slots allow direct HP attacks
- Critical hits and evasion are calculated dynamically

---

## 4️⃣ Cleanup Phase
The system:
- Removes defeated monsters
- Sends them to the graveyard
- Draws new cards
- Updates board states

---

# 🤖 AI System (Bot Opponent)

The game includes a built-in AI opponent using:

## 🧠 Rule-Based Greedy Algorithm

The bot:
1. Scans cards in hand
2. Evaluates predefined priorities
3. Instantly performs the best available action

### Why Greedy AI?

✅ Extremely fast  
✅ Low computational cost  
✅ No frame drops  
✅ Works smoothly with real-time animations  

### Tradeoff
The AI is not always perfectly optimal like Minimax or MCTS systems, but it provides:
- Smooth gameplay
- Fast decision-making
- Lightweight processing

---

# 🌐 Online LAN Multiplayer

The game supports local multiplayer over LAN using:

## 🔌 TCP Socket Networking

Players can:
- Host a game
- Join using IP address

---

## 📡 Networking Architecture

Implemented in `network.py` using:
- Python sockets
- Peer-to-peer communication
- Multithreading
- Pickle serialization

---

## 📦 Length-Prefixed TCP Framing

To avoid:
- TCP sticky packets
- Broken serialization
- Data corruption

The system sends:
1. Packet length (4 bytes)
2. Serialized game data

before transmitting the actual payload.

This ensures stable synchronization between players.

---

# 🎞 Animation System

The game contains a dedicated animation engine:
- Attack bump effects
- Flash effects
- Summon animations
- Death dissolves
- Global screen shake
- Spell overlays

Implemented in:
```python
animations.py
