import streamlit as st
import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="🎮 THE KNOWLEDGE ARENA",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #000000;
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-align: center;
        color: #ff0000;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    }
    
    .stButton > button {
        background: #000000;
        border: 1px solid #ffffff;
        border-radius: 4px;
        color: #ffffff;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    
    .stButton > button:hover {
        background: #1a1a1a;
        border-color: #ff0000;
    }
    
    .stTextInput > div > div > input {
        background: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 4px;
        color: #ffffff !important;
        padding: 10px 12px;
        font-size: 14px;
    }
    
    .stSelectbox > div > div {
        background: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 4px;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-size: 14px;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #000000;
    }
    
    .css-1d391kg {
        background-color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
    
# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
if 'players' not in st.session_state:
    st.session_state.players = []
if 'current_round' not in st.session_state:
    st.session_state.current_round = 1
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'questions_per_round' not in st.session_state:
    st.session_state.questions_per_round = 5
if 'max_rounds' not in st.session_state:
    st.session_state.max_rounds = 3
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'leaderboard_data' not in st.session_state:
    st.session_state.leaderboard_data = []
if 'round_completed' not in st.session_state:
    st.session_state.round_completed = False

def load_questions():
    """Load questions from JSON file with better error handling"""
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
            
        # Validate question structure
        for i, q in enumerate(questions):
            required_fields = ['id', 'question', 'options', 'answer_index', 'category', 'difficulty']
            for field in required_fields:
                if field not in q:
                    st.error(f"Question {i+1} missing required field: {field}")
                    return []
            
            # Validate answer_index is within options range
            if q['answer_index'] >= len(q['options']) or q['answer_index'] < 0:
                st.error(f"Question {i+1} has invalid answer_index: {q['answer_index']}")
                return []
                
        return questions
        
    except FileNotFoundError:
        st.error("❌ questions.json file not found! Please ensure the file exists.")
        return []
    except json.JSONDecodeError as e:
        st.error(f"❌ Error parsing questions.json: {e}")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected error loading questions: {e}")
        return []

def load_leaderboard():
    """Load leaderboard from JSON file"""
    try:
        with open('leaderboard.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create empty leaderboard if file doesn't exist
        return []
    except json.JSONDecodeError:
        # If JSON is corrupted, return empty list
        return []

def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file"""
    try:
        with open('leaderboard.json', 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving leaderboard: {e}")

def add_to_leaderboard(player_name, final_score, avatar):
    """Add player score to leaderboard"""
    leaderboard = load_leaderboard()
    
    # Add new score
    leaderboard.append({
        'name': player_name,
        'score': final_score,
        'avatar': avatar,
        'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Sort by score (highest first) and keep top 10
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:10]
    
    # Save updated leaderboard
    save_leaderboard(leaderboard)
    
    # Debug: Show what was saved
    st.success(f"✅ {player_name}'s score ({final_score}) saved to leaderboard!")
    
    return leaderboard

def get_questions_by_difficulty_and_topic(questions, difficulty, topic_categories):
    """Filter questions by difficulty and topic categories"""
    filtered = [q for q in questions if q['difficulty'] == difficulty and q['category'] in topic_categories]
    return filtered

def create_player(name, avatar):
    """Create a new player with initial stats"""
    return {
        'name': name,
        'avatar': avatar,
        'hp': 100,
        'max_hp': 100,
        'xp': 0,
        'streak': 0,
        'powerups': {'shield': 0, 'heal': 0},
        'eliminated': False,
        'final_score': 0
    }

def update_player_hp(player, change, reason=""):
    """Update player HP with animations"""
    old_hp = player['hp']
    player['hp'] = max(0, min(player['max_hp'], player['hp'] + change))
    
    if change < 0:
        st.session_state.last_damage = {
            'player': player['name'],
            'damage': abs(change),
            'reason': reason
        }
    elif change > 0:
        st.session_state.last_heal = {
            'player': player['name'],
            'heal': change,
            'reason': reason
        }
    
    return old_hp != player['hp']

def check_elimination(player):
    """Check if player is eliminated"""
    if player['hp'] <= 0 and not player['eliminated']:
        player['eliminated'] = True
        return True
    return False

def apply_powerup(player, powerup_type):
    """Apply power-up to player"""
    if powerup_type == 'shield' and player['powerups']['shield'] > 0:
        player['powerups']['shield'] -= 1
        return True
    elif powerup_type == 'heal' and player['powerups']['heal'] > 0:
        player['powerups']['heal'] -= 1
        update_player_hp(player, 20, "Heal Power-up")
        return True
    return False

def get_round_config(round_num):
    """Get configuration for each round with 3 specific topics"""
    # The 3 specific topics
    topics = ['Hollywood/Bollywood', 'History/GK', 'Sports']
    
    # Initialize round topic if not already done
    if f'round_{round_num}_topic' not in st.session_state:
        # Get available topics (not used in previous rounds)
        used_topics = []
        for i in range(1, round_num):
            if f'round_{i}_topic' in st.session_state:
                used_topics.append(st.session_state[f'round_{i}_topic'])
        
        # Choose from remaining topics
        available_topics = [topic for topic in topics if topic not in used_topics]
        if available_topics:
            st.session_state[f'round_{round_num}_topic'] = random.choice(available_topics)
        else:
            # If all topics used, pick randomly
            st.session_state[f'round_{round_num}_topic'] = random.choice(topics)
    
    # Map topics to categories for question filtering
    topic_to_categories = {
        'Hollywood/Bollywood': ['Hollywood', 'Bollywood'],
        'History/GK': ['History'],
        'Sports': ['Sports']
    }
    
    current_topic = st.session_state[f'round_{round_num}_topic']
    configs = {
        1: {'difficulty': 'easy', 'topic': current_topic, 'categories': topic_to_categories[current_topic]},
        2: {'difficulty': 'medium', 'topic': current_topic, 'categories': topic_to_categories[current_topic]},
        3: {'difficulty': 'hard', 'topic': current_topic, 'categories': topic_to_categories[current_topic]}
    }
    return configs.get(round_num, configs[3])


def render_player_setup():
    """Render player setup interface"""
    # Hero section with 70% height
    st.markdown("""
    <div style="height: 70vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <h1 class="main-header" style="font-size: 4rem; margin-bottom: 2rem;">THE KNOWLEDGE ARENA</h1>
        <p style="font-size: 1.5rem; color: #ffffff; margin-bottom: 3rem;">Test your knowledge in the ultimate quiz battle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Leaderboard section
    leaderboard = load_leaderboard()
    if leaderboard:
        st.markdown("### LEADERBOARD")
        for i, entry in enumerate(leaderboard[:5]):
            col1, col2, col3 = st.columns([0.1, 3, 2])
            with col1:
                st.write(f"**{i+1}.**")
            with col2:
                st.write(f"{entry['avatar']} {entry['name']}")
            with col3:
                st.write(f"{entry['score']} pts")
            st.markdown("---")
    
    st.markdown("### PLAYER SETUP")
    
    player_name = st.text_input("NAME", placeholder="Enter name")
    
    if player_name:
        leaderboard = load_leaderboard()
        player_scores = [entry for entry in leaderboard if entry['name'].lower() == player_name.lower()]
        if player_scores:
            best_score = max(player_scores, key=lambda x: x['score'])
            st.caption(f"Best: {best_score['score']} pts")
    
    avatar_options = ["⚔️", "🛡️", "🏹", "🗡️", "⚡", "🔥", "❄️", "🌟"]
    selected_avatar = st.selectbox("AVATAR", avatar_options)
    
    if st.button("ADD PLAYER", type="primary"):
        if player_name:
            new_player = create_player(player_name, selected_avatar)
            st.session_state.players.append(new_player)
            st.rerun()
        else:
            st.error("Please enter your name!")
    
    if st.session_state.players:
        for i, player in enumerate(st.session_state.players):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"{player['avatar']} **{player['name']}**")
            with col2:
                if st.button("✕", key=f"remove_{i}"):
                    st.session_state.players.pop(i)
                    st.rerun()
        
        st.markdown("---")
        if st.button("START", type="primary", use_container_width=True):
                st.session_state.game_state = 'playing'
                st.session_state.game_started = True
                st.session_state.round_completed = False
                for i in range(1, 4):
                    if f'round_{i}_topic' in st.session_state:
                        del st.session_state[f'round_{i}_topic']
                st.rerun()
        
        if st.button("VIEW LEADERBOARD"):
                st.session_state.show_full_leaderboard = True
                st.rerun()
    
    if st.session_state.get('show_full_leaderboard', False):
        st.markdown("### COMPLETE LEADERBOARD")
        leaderboard = load_leaderboard()
        
        if leaderboard:
            for i, entry in enumerate(leaderboard):
                col1, col2, col3, col4 = st.columns([0.2, 3, 2, 2])
                with col1:
                    st.write(f"**{i+1}.**")
                with col2:
                    st.write(f"{entry['avatar']} {entry['name']}")
                with col3:
                    st.write(f"{entry['score']} pts")
                with col4:
                    st.caption(entry['date'][:10])
                st.markdown("---")
        else:
            st.info("No scores yet")
        
        if st.button("BACK"):
            st.session_state.show_full_leaderboard = False
            st.rerun()

def render_game_interface():
    """Render main game interface"""
    # Check if we're in round completion state
    if st.session_state.get('round_completed', False):
        end_round()
        return
    
    questions = load_questions()
    if not questions:
        st.error("No questions available!")
        return
    
    # Get current round configuration
    round_config = get_round_config(st.session_state.current_round)
    round_questions = get_questions_by_difficulty_and_topic(
        questions, round_config['difficulty'], round_config['categories']
    )
    
    # Validate we have enough questions
    if len(round_questions) < st.session_state.questions_per_round:
        st.error(f"Not enough {round_config['difficulty']} {round_config['topic']} questions available!")
        st.info(f"Need {st.session_state.questions_per_round} questions, but only found {len(round_questions)}")
        st.info(f"Looking for: {round_config['categories']} with difficulty: {round_config['difficulty']}")
        
        # Show available questions for debugging
        if round_questions:
            st.write("Available questions:")
            for q in round_questions:
                st.write(f"- {q['question']} ({q['category']})")
        
        return
    
    # Initialize round questions if not already done
    if f'round_{st.session_state.current_round}_questions' not in st.session_state:
        # Shuffle questions for this round
        shuffled_questions = round_questions.copy()
        random.shuffle(shuffled_questions)
        st.session_state[f'round_{st.session_state.current_round}_questions'] = shuffled_questions
        st.session_state[f'round_{st.session_state.current_round}_used_questions'] = []
    
    # Get the current question from the shuffled list
    round_questions_list = st.session_state[f'round_{st.session_state.current_round}_questions']
    used_questions = st.session_state[f'round_{st.session_state.current_round}_used_questions']
    
    # Find next unused question
    if st.session_state.current_question < len(round_questions_list):
        current_question_data = round_questions_list[st.session_state.current_question]
        # Mark this question as used
        if current_question_data['id'] not in used_questions:
            used_questions.append(current_question_data['id'])
    else:
        # If we run out of questions, cycle through unused ones
        available_questions = [q for q in round_questions_list if q['id'] not in used_questions]
        if available_questions:
            current_question_data = available_questions[0]
            used_questions.append(current_question_data['id'])
        else:
            # If all questions used, reset and start over
            used_questions.clear()
            current_question_data = round_questions_list[0]
            used_questions.append(current_question_data['id'])
    
    st.markdown(f"### Round {st.session_state.current_round} - {round_config['topic']} ({round_config['difficulty'].upper()})")
    st.caption(f"Question {st.session_state.current_question + 1} / {st.session_state.questions_per_round}")
    st.markdown("---")
    
    # Players status will be shown at the bottom
    
    # Initialize answer state for new question
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    
    st.markdown(f"**{current_question_data['question']}**")
    
    if st.session_state.get('answer_submitted', False):
        if 'last_answer_result' in st.session_state:
            result = st.session_state.last_answer_result
            if result['is_correct']:
                st.success("✓ Correct")
            else:
                st.error("✗ Wrong")
            st.info(f"Answer: {result['correct_answer']}")
            
            if st.button("NEXT", key="next_question_btn"):
                next_question()
    else:
        cols = st.columns(2)
        for i, option in enumerate(current_question_data['options']):
            with cols[i % 2]:
                if st.button(option, key=f"option_{i}", use_container_width=True):
                    handle_answer(i, current_question_data, round_config)
    
    st.markdown("---")
    if len(st.session_state.players) > 0:
        player = st.session_state.players[0]
        hp_percentage = (player['hp'] / player['max_hp']) * 100
        hp_color = "#ff0000" if hp_percentage < 50 else "#ffffff"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**{player['avatar']} {player['name']}**")
        with col2:
            st.metric("HP", f"{player['hp']}/{player['max_hp']}")
        with col3:
            st.metric("XP", player['xp'])
        with col4:
            st.metric("Streak", player['streak'])
        
        st.progress(hp_percentage / 100)
        st.caption(f"🛡 {player['powerups']['shield']}  💉 {player['powerups']['heal']}")

def handle_answer(selected_index, question_data, round_config):
    """Handle player's answer"""
    st.session_state.answer_submitted = True
    
    correct_index = question_data['answer_index']
    is_correct = selected_index == correct_index
    
    # Process the single player's answer
    player = st.session_state.players[0]  # Single player game
    
    if is_correct:
        # Correct answer
        player['xp'] += 10
        player['streak'] += 1
        
        # Combo heal for streak of 3
        if player['streak'] >= 3:
            update_player_hp(player, 15, "Combo Heal!")
            player['streak'] = 0  # Reset streak
    else:
        # Wrong answer
        if player['powerups']['shield'] > 0:
            # Use shield
            apply_powerup(player, 'shield')
        else:
            # Take damage
            update_player_hp(player, -20, "Wrong answer")
            player['streak'] = 0
            check_elimination(player)
    
    # Store result for display
    st.session_state.last_answer_result = {
        'is_correct': is_correct,
        'correct_answer': question_data['options'][correct_index]
    }
    
    # Refresh to show result
    st.rerun()

def next_question():
    """Move to next question or round"""
    st.session_state.current_question += 1
    st.session_state.answer_submitted = False
    
    # Clear previous answer result
    if 'last_answer_result' in st.session_state:
        del st.session_state.last_answer_result
    
    # Check if round is complete
    if st.session_state.current_question >= st.session_state.questions_per_round:
        end_round()
    else:
        st.rerun()
        
def end_round():
    """End current round and show results"""
    # Set round completion state instead of immediately incrementing
    st.session_state.round_completed = True
    st.session_state.current_question = 0
    
    # Get the player
    player = st.session_state.players[0]
    
    # Award power-ups to the player if they survived
    if not player['eliminated']:
        player['powerups']['shield'] += 1
        player['powerups']['heal'] += 1
    
    if player['eliminated']:
        player['final_score'] = player['xp'] + (player['hp'] * 2)
        
        st.error("## ELIMINATED")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("FINAL SCORE", player['final_score'])
        with col2:
            st.metric("XP", player['xp'])
        with col3:
            st.metric("HP", player['hp'])
        
        if player['final_score'] > 0:
            add_to_leaderboard(player['name'], player['final_score'], player['avatar'])
        
        if st.button("TRY AGAIN", use_container_width=True):
            reset_game()
        return
    
    st.success(f"## ROUND {st.session_state.current_round} COMPLETE")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("HP", f"{player['hp']}/{player['max_hp']}")
    with col2:
        st.metric("XP", player['xp'])
    with col3:
        st.metric("STREAK", player['streak'])
    
    if st.session_state.current_round >= st.session_state.max_rounds:
        end_game()
    else:
        if st.button("NEXT ROUND"):
            # Now safely increment round and initialize next round
            st.session_state.current_round += 1
            st.session_state.round_completed = False
            
            # Clear any existing round questions to force re-initialization
            round_key = f'round_{st.session_state.current_round}_questions'
            if round_key in st.session_state:
                del st.session_state[round_key]
            
            st.rerun()

def end_game():
    """End the game and show final results"""
    st.session_state.game_state = 'finished'
    
    # Calculate final score for the single player
    player = st.session_state.players[0]
    player['final_score'] = player['xp'] + (player['hp'] * 2)
    
    # Save score to leaderboard
    add_to_leaderboard(player['name'], player['final_score'], player['avatar'])
    
    st.markdown("## FINAL RESULTS")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("SCORE", player['final_score'])
    with col2:
        st.metric("XP", player['xp'])
    with col3:
        st.metric("HP", player['hp'])
    
    st.markdown("---")
    
    if player['final_score'] >= 200:
        st.success("Outstanding!")
    elif player['final_score'] >= 150:
        st.info("Great work!")
    else:
        st.info("Keep practicing!")
    
    if st.button("PLAY AGAIN", use_container_width=True):
        reset_game()

def reset_game():
    """Reset the game to initial state"""
    # Reset all game state safely
    keys_to_reset = ['game_state', 'players', 'current_round', 'current_question', 
                    'game_started', 'leaderboard_data', 'answer_submitted', 'question_start_time',
                    'round_completed', 'last_answer_result', 'last_damage', 'last_heal']
    
    for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
    
    # Clear round topics
    for i in range(1, 4):
        round_key = f'round_{i}_topic'
        if round_key in st.session_state:
            del st.session_state[round_key]
        questions_key = f'round_{i}_questions'
        if questions_key in st.session_state:
            del st.session_state[questions_key]
        used_key = f'round_{i}_used_questions'
        if used_key in st.session_state:
            del st.session_state[used_key]
    
        st.rerun()
    
def validate_session_state():
    """Validate and initialize session state"""
    required_keys = {
        'game_state': 'setup',
        'players': [],
        'current_round': 1,
        'current_question': 0,
        'questions_per_round': 5,
        'max_rounds': 3,
        'game_started': False,
        'leaderboard_data': [],
        'round_completed': False
    }
    
    for key, default_value in required_keys.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def render_footer():
    """Render the team footer"""
    st.markdown("---")
    
    # Team Members Section
    st.markdown("### 🏆 The Knowledge Arena DEVELOPMENT TEAM 🏆")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 20px; margin: 10px 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">
            <h4 style="color: #feca57; margin-bottom: 15px;">👨‍💻 Team Members</h4>
            <p>🎮 Jashan - UID: 25BBE10122</p>
            <p>🎮 Vishal - UID: 25BBE10134</p>
            <p>🎮 Vikanshi - UID: 25BBE10135</p>
            <p>🎮 Somya - UID: 25BBE10130</p>
            <p>🎮 Hrishita - UID: 25BBE10141</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 20px; margin: 10px 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">
            <h4 style="color: #feca57; margin-bottom: 15px;">👨‍💻 Team Members</h4>
            <p>🎮 Surabhi - UID: 25BBE10140</p>
            <p>🎮 Amandeep - UID: 25BBE10196</p>
            <p>🎮 Jasmine - UID: 25BBE10171</p>
            <p>🎮 Aashna - UID: 25BBE10164</p>
            <p>🎮 Lakshmi - UID: 25BBE10137</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mentor Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; padding: 20px; margin: 10px 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">
        <h4 style="color: #feca57; margin-bottom: 15px;">🎓 Mentor</h4>
        <p>👨‍🏫 Mrs. Karuna Kaushik</p>
        <p>📋 Assistant Professor</p>
        <p>📧 karuna.e19106@cumail.in</p>
        <p>🏢 Chandigarh University</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Information
    st.markdown("""
    <div style="background: linear-gradient(135deg, #45b7d1 0%, #96ceb4 100%); border-radius: 15px; padding: 20px; margin: 10px 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">
        <h4 style="color: #feca57; margin-bottom: 15px;">🚀 Project Information</h4>
        <p>📅 Development Period: 2024</p>
        <p>🛠️ Technology Stack: Python + Streamlit</p>
        <p>🎯 Project Type: Interactive Quiz Game</p>
        <p>💡 Special Thanks: Our amazing mentor for guidance and support!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Copyright
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <p style="color: rgba(255,255,255,0.8); margin: 0;">Made with ❤️ by our amazing development team | © 2025 The Knowledge Arena</p>
    </div>
    """, unsafe_allow_html=True)
    
def main():
    """Main game loop"""
    # Validate session state
    validate_session_state()
    
    # Ensure we have at least one player for single-player mode
    if st.session_state.game_state == 'playing' and len(st.session_state.players) == 0:
        st.error("❌ No player found! Redirecting to setup...")
        st.session_state.game_state = 'setup'
        st.rerun()
    
    if st.session_state.game_state == 'setup':
        render_player_setup()
    elif st.session_state.game_state == 'playing':
        render_game_interface()
    elif st.session_state.game_state == 'finished':
        end_game()
    
    render_footer()

if __name__ == "__main__":
    main()
