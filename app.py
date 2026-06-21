import streamlit as st
import random

st.title("The Monty Hall Problem Simulator")
st.write("Complete 50 trials to see the empirical power of switching!")

# 1. Initialize State Variables (The App's Memory)
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.trials_played = 0
    st.session_state.stick_played = 0
    st.session_state.stick_wins = 0
    st.session_state.switch_played = 0
    st.session_state.switch_wins = 0
    
    # Game phase flags
    # "pick_door" -> User needs to select a door
    # "make_decision" -> Monty revealed a goat, user must choose Stick or Switch
    st.session_state.game_phase = "pick_door"
    st.session_state.winning_door = None
    st.session_state.chosen_door = None
    st.session_state.revealed_door = None
    st.session_state.feedback_message = ""

# 2. Reset the layout for a brand new individual trial
def start_new_trial():
    st.session_state.winning_door = random.randint(1, 3)
    st.session_state.game_phase = "pick_door"
    st.session_state.chosen_door = None
    st.session_state.revealed_door = None

if st.session_state.winning_door is None:
    start_new_trial()

# --- THE GAME ZONE ---
if st.session_state.trials_played < 50:
    st.subheader(f"Current Status: Trial {st.session_state.trials_played + 1} of 50")
    
    # Phase A: User picks initial door
    if st.session_state.game_phase == "pick_door":
        st.write("Pick a door to find the car!")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Door 1", key="d1"):
                st.session_state.chosen_door = 1
        with col2:
            if st.button("Door 2", key="d2"):
                st.session_state.chosen_door = 2
        with col3:
            if st.button("Door 3", key="d3"):
                st.session_state.chosen_door = 3
                
        if st.session_state.chosen_door is not None:
            # Monty reveals a remaining door that has a goat
            remaining_doors = [d for d in [1, 2, 3] if d != st.session_state.chosen_door and d != st.session_state.winning_door]
            st.session_state.revealed_door = random.choice(remaining_doors)
            st.session_state.game_phase = "make_decision"
            st.rerun()

    # Phase B: User decides to stick or switch
    elif st.session_state.game_phase == "make_decision":
        # Calculate what the alternate door is
        available_doors = [1, 2, 3]
        available_doors.remove(st.session_state.chosen_door)
        available_doors.remove(st.session_state.revealed_door)
        alternate_door = available_doors[0]
        
        st.warning(f"You initially chose **Door {st.session_state.chosen_door}**.")
        st.info(f"Monty opens **Door {st.session_state.revealed_door}**, revealing a 🐐 GOAT!")
        st.write(f"Do you want to **Stick** with Door {st.session_state.chosen_door} or **Switch** to Door {alternate_door}?")
        
        col_stick, col_switch = st.columns(2)
        
        with col_stick:
            if st.button(f"Stick with Door {st.session_state.chosen_door}"):
                final_door = st.session_state.chosen_door
                st.session_state.stick_played += 1
                
                if final_door == st.session_state.winning_door:
                    st.session_state.stick_wins += 1
                    st.session_state.feedback_message = f"🎉 Success! You Stuck and won! The car was behind Door {st.session_state.winning_door}."
                else:
                    st.session_state.feedback_message = f"❌ Lost! The car was behind Door {st.session_state.winning_door}."
                
                st.session_state.trials_played += 1
                start_new_trial()
                st.rerun()
                
        with col_switch:
            if st.button(f"Switch to Door {alternate_door}"):
                final_door = alternate_door
                st.session_state.switch_played += 1
                
                if final_door == st.session_state.winning_door:
                    st.session_state.switch_wins += 1
                    st.session_state.feedback_message = f"🎉 Success! You Switched and won! The car was behind Door {st.session_state.winning_door}."
                else:
                    st.session_state.feedback_message = f"❌ Lost! The car was behind Door {st.session_state.winning_door}."
                
                st.session_state.trials_played += 1
                start_new_trial()
                st.rerun()

    if st.session_state.feedback_message:
        st.success(st.session_state.feedback_message)

else:
    st.balloons()
    st.header("🏁 50 Trials Completed!")
    st.write("Here is the final breakdown of your data:")

# --- THE SCOREBOARD ZONE ---
st.markdown("---")
st.subheader("📊 Live Statistics Scoreboard")

total_wins = st.session_state.stick_wins + st.session_state.switch_wins
total_played = st.session_state.trials_played

# Calculate rates safely avoiding division by zero
win_pct = (total_wins / total_played * 100) if total_played > 0 else 0.0
stick_pct = (st.session_state.stick_wins / st.session_state.stick_played * 100) if st.session_state.stick_played > 0 else 0.0
switch_pct = (st.session_state.switch_wins / st.session_state.switch_played * 100) if st.session_state.switch_played > 0 else 0.0

# Render tables/metrics clear for adult learners
st.markdown(f"**Overall Game Totals:** {total_wins} Wins out of {total_played} Played (**{win_pct:.1f}% Win Rate**)")

col_metric1, col_metric2 = st.columns(2)
with col_metric1:
    st.metric(label="When Sticking", value=f"{st.session_state.stick_wins} Wins", delta=f"{st.session_state.stick_played} Total Tries")
    st.write(f"Stick Win Percent: **{stick_pct:.1f}%**")
with col_metric2:
    st.metric(label="When Switching", value=f"{st.session_state.switch_wins} Wins", delta=f"{st.session_state.switch_played} Total Tries")
    st.write(f"Switch Win Percent: **{switch_pct:.1f}%**")

if st.button("Reset Everything"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
