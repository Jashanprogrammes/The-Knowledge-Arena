# 🎮 Quiz Royale - The Battle-Style Quiz Game

Welcome to **Quiz Royale**, an epic battle-style quiz game where knowledge is your weapon and strategy is your shield!

## 🏰 Game Features

### ⚔️ Battle Mechanics

- **Health Points (HP)**: Start with 100 HP
- **Experience Points (XP)**: Earn 10 XP for correct answers
- **Streak System**: Get 3 correct in a row for a "🔥 Combo Heal" (+15 HP)
- **Time Pressure**: 10-15 seconds per question (varies by round)
- **Penalties**: -10 HP for timeout, -20 HP for wrong answers

### 🛡️ Power-ups

- **Shield**: Ignore 1 wrong answer (earned after each round)
- **Heal**: Regain 20 HP (earned after each round)

### 🎯 Game Structure

- **3 Rounds**: Each with 5 questions
- **Round 1**: Easy Geography questions (15s timer)
- **Round 2**: Medium Science questions (12s timer)
- **Round 3**: Hard History questions (10s timer)
- **Final Showdown**: Epic conclusion with leaderboard

### 🎨 Visual Features

- Animated health bars with color-coded status
- Real-time timer with pulsing animation
- Gradient backgrounds and modern UI
- Player avatars and status cards
- Streak indicators with glow effects

## 🚀 How to Play

### Installation

1. Install Python 3.7+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
streamlit run quiz_royale.py
```

### Gameplay

1. **Setup**: Enter your name and choose an avatar
2. **Battle**: Answer questions within the time limit
3. **Strategy**: Use power-ups wisely to survive
4. **Victory**: Compete for the highest final score!

## 🎮 Game Rules

### Scoring System

- **Correct Answer**: +10 XP
- **Wrong Answer**: -20 HP (unless shielded)
- **Timeout**: -10 HP
- **3-Correct Streak**: +15 HP (Combo Heal)
- **Final Score**: XP + (HP × 2)

### Elimination

- Players are eliminated when HP reaches 0
- Eliminated players cannot continue to next rounds
- Power-ups are awarded to survivors after each round

### Power-up Usage

- **Shield**: Automatically activates on wrong answers
- **Heal**: Can be used anytime (restores 20 HP)
- **Acquisition**: 1 of each power-up per round for survivors

## 🏆 Victory Conditions

The game ends after 3 rounds, and the winner is determined by:

1. **Final Score** (XP + HP × 2)
2. **Survival** (must not be eliminated)
3. **Total XP** (tiebreaker)

## 🎨 Customization

The game uses the existing `questions.json` file with the following structure:

- **Categories**: Geography, Science, History, Literature, Art, Technology, Sports, Mathematics
- **Difficulties**: Easy, Medium, Hard
- **Format**: Multiple choice with 4 options

## 🔧 Technical Details

- **Framework**: Streamlit
- **Styling**: Custom CSS with animations
- **Data**: JSON-based question system
- **State Management**: Streamlit session state
- **Responsive**: Works on desktop and mobile

## 🎵 Sound Effects (Future Enhancement)

The game is designed to support sound effects for:

- Correct/incorrect answers
- Power-up activations
- Eliminations
- Round transitions
- Final showdown

## 🏰 Ready for Battle?

Launch the game and prove your knowledge in the ultimate quiz arena! May the best warrior win! ⚔️🏆
