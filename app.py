import streamlit as st
import random
import pandas as pd

st.title("The Monty Hall Problem Simulator")
st.write("Test your intuition! Can you successfully beat the game?")

# 1. Initialize State Variables (The App's Memory)
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.trials_played = 0
    st.session_state.total_wins = 0
    st.session_state.total_losses = 0
    st.session_state.stick_played = 0
    st.session_state.stick_wins = 0
    st.session_state.switch_played = 0
    st.session_state.switch_wins = 0
    
    # Game phase flags
    st.session_state.game_phase = "pick_door"
    st.session_state.winning_door = None
    st.session_state.chosen_door = None
    st.session_state.revealed_door = None
    st.session_state.last_outcome = None
    st.session_state.feedback_message = ""

# Set total trials
max_trials = st.number_input("Set number of trials to complete:", min_value=1, max_value=1000, value=50, step=1)

# 2. Reset layout for a brand new trial
def start_new_trial():
    st.session_state.winning_door = random.randint(1, 3)
    st.session_state.game_phase = "pick_door"
    st.session_state.chosen_door = None
    st.session_state.revealed_door = None

if st.session_state.winning_door is None:
    start_new_trial()

# --- THE GAME ZONE ---
if st.session_state.trials_played < max_trials:
    st.subheader(f"Current Status: Trial {st.session_state.trials_played + 1} of {max_trials}")
    
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
            remaining_doors = [d for d in [1, 2, 3] if d != st.session_state.chosen_door and d != st.session_state.winning_door]
            st.session_state.revealed_door = random.choice(remaining_doors)
            st.session_state.game_phase = "make_decision"
            st.rerun()

    # Phase B: User decides to stick or switch
    elif st.session_state.game_phase == "make_decision":
        available_doors = [1, 2, 3]
        available_doors.remove(st.session_state.chosen_door)
        available_doors.remove(st.session_state.revealed_door)
        alternate_door = available_doors[0]
        
        st.warning(f"You initially chose **Door {st.session_state.chosen_door}**.")
        st.info(f"Monty opens **Door {st.session_state.revealed_door}**, revealing a GOAT!")
        st.write(f"Do you want to **Stick** with Door {st.session_state.chosen_door} or **Switch** to Door {alternate_door}?")
        
        col_stick, col_switch = st.columns(2)
        
        with col_stick:
            if st.button(f"Stick with Door {st.session_state.chosen_door}"):
                final_door = st.session_state.chosen_door
                st.session_state.stick_played += 1
                
                if final_door == st.session_state.winning_door:
                    st.session_state.stick_wins += 1
                    st.session_state.total_wins += 1
                    st.session_state.last_outcome = "win"
                    st.session_state.feedback_message = "🎉 Success! You won a Car!"
                else:
                    st.session_state.total_losses += 1
                    st.session_state.last_outcome = "loss"
                    st.session_state.feedback_message = "❌ Lost! You got a Goat."
                
                st.session_state.trials_played += 1
                start_new_trial()
                st.rerun()
                
        with col_switch:
            if st.button(f"Switch to Door {alternate_door}"):
                final_door = alternate_door
                st.session_state.switch_played += 1
                
                if final_door == st.session_state.winning_door:
                    st.session_state.switch_wins += 1
                    st.session_state.total_wins += 1
                    st.session_state.last_outcome = "win"
                    st.session_state.feedback_message = "🎉 Success! You won a Car!"
                else:
                    st.session_state.total_losses += 1
                    st.session_state.last_outcome = "loss"
                    st.session_state.feedback_message = "❌ Lost! You got a Goat."
                
                st.session_state.trials_played += 1
                start_new_trial()
                st.rerun()

    if st.session_state.feedback_message:
        if st.session_state.last_outcome == "win":
            st.success(st.session_state.feedback_message)
        else:
            st.error(st.session_state.feedback_message)

    # --- MID-GAME PUBLIC SCOREBOARD (TEXT ONLY) ---
    st.markdown("---")
    st.subheader("📊 Your Live Progress")
    
    win_pct = (st.session_state.total_wins / st.session_state.trials_played * 100) if st.session_state.trials_played > 0 else 0.0
    st.write(f"Games Played: **{st.session_state.trials_played}** | Total Wins: **{st.session_state.total_wins}** | Total Losses: **{st.session_state.total_losses}** | Win Percentage: **{win_pct:.1f}%**")

else:
    # --- END GAME: REVEAL THE GRAND FINALE SUMMARY ---
    st.balloons()
    st.header(f"🏁 {max_trials} Trials Completed!")
    st.subheader("The Truth Revealed: Stick vs. Switch")
    st.write("Let's look at the final breakdown of your choices and outcomes.")
    
    total_played = st.session_state.trials_played
    stick_losses = st.session_state.stick_played - st.session_state.stick_wins
    switch_losses = st.session_state.switch_played - st.session_state.switch_wins
    
    final_win_pct = (st.session_state.total_wins / total_played * 100) if total_played > 0 else 0.0
    stick_pct = (st.session_state.stick_wins / st.session_state.stick_played * 100) if st.session_state.stick_played > 0 else 0.0
    switch_pct = (st.session_state.switch_wins / st.session_state.switch_played * 100) if st.session_state.switch_played > 0 else 0.0
    
    # Create the exact data matrix requested
    summary_matrix = {
        "Games Played": [st.session_state.stick_played, st.session_state.switch_played, total_played],
        "Games Won": [st.session_state.stick_wins, st.session_state.switch_wins, st.session_state.total_wins],
        "Games Lost": [stick_losses, switch_losses, st.session_state.total_losses],
        "% Win": [f"{stick_pct:.1f}%", f"{switch_pct:.1f}%", f"{final_win_pct:.1f}%"]
    }
    
    # Convert to DataFrame with custom rows
    df_summary = pd.DataFrame(summary_matrix, index=["Stay", "Switch", "Total"])
    
    # Display table beautifully
    st.markdown("---")
    st.dataframe(df_summary, use_container_width=True)
    st.markdown("---")
    
    if st.button("Reset Game and Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
