import streamlit as st
import matplotlib.pyplot as plt
from monte_carlo import hand_value, estimate_ev

def sum_to_cards_mapper(total):
   num = int(total)
   mapper = {
      2: [1,1],
      3: [1,2],
      4: [1,3],
      5: [2,3],
      6: [3,3],
      7: [3,4],
      8: [3,5],
      9: [4,5],
      10: [5,5],
      11: [5,6],
      12: [6,6],  
      13: [6,7],
      14: [7,7],
      15: [7,8],
      16: [8,8],
      17: [8,9],
      18: [9,9],
      19: [9,10],
      20: [10,10],
      21: [10,11],
   }
   return mapper[num]

def visualize_ev_streamlit(player_cards, dealer_upcard, num_simulations=100000):
    # Run simulations
    hit_result = estimate_ev(player_cards, dealer_upcard, num_simulations, infinite=True, decision="HIT")
    stand_result = estimate_ev(player_cards, dealer_upcard, num_simulations, infinite=True, decision="STAND")
    
    # Extract EVs
    hit_ev = hit_result["ev"]
    stand_ev = stand_result["ev"]
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    decisions = ["HIT", "STAND"]
    evs = [hit_ev, stand_ev]
    colors = ["#2ecc71" if ev > 0 else "#e74c3c" for ev in evs]
    
    bars = ax.bar(decisions, evs, color=colors, alpha=0.7, edgecolor="black", linewidth=2)
    
    for bar, ev in zip(bars, evs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{ev:.4f}',
                ha='center', va='bottom' if height > 0 else 'top', fontsize=12, fontweight='bold')
    
    player_total, _ = hand_value(player_cards)
    ax.set_ylabel("Expected Value (EV)", fontsize=12, fontweight='bold')
    ax.set_title(f"Player {player_total} vs Dealer {dealer_upcard} ({num_simulations:,} simulations)", 
                 fontsize=14, fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_ylim(min(evs) - 0.1, max(evs) + 0.15)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    player_total, _ = hand_value(player_cards)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("HIT EV", f"{hit_ev:.4f}", f"Win: {hit_result['win_rate']:.2%}")
    with col2:
        st.metric("STAND EV", f"{stand_ev:.4f}", f"Win: {stand_result['win_rate']:.2%}")
    
    recommendation = "HIT" if hit_ev > stand_ev else "STAND" if stand_ev > hit_ev else "SAME"
    st.success(f"Recommendation: **{recommendation}**")
    
    # Pie charts for outcome distribution
    st.subheader("Outcome Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**HIT Outcomes**")
        hit_labels = ['Win', 'Loss', 'Push']
        hit_sizes = [hit_result['win_rate'], hit_result['loss_rate'], hit_result['push_rate']]
        hit_colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        
        fig_hit, ax_hit = plt.subplots(figsize=(8, 6))
        ax_hit.pie(hit_sizes, labels=hit_labels, colors=hit_colors, autopct='%1.1f%%', startangle=90)
        ax_hit.set_title('HIT Distribution', fontweight='bold', fontsize=12)
        st.pyplot(fig_hit)
    
    with col2:
        st.write("**STAND Outcomes**")
        stand_labels = ['Win', 'Loss', 'Push']
        stand_sizes = [stand_result['win_rate'], stand_result['loss_rate'], stand_result['push_rate']]
        stand_colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        
        fig_stand, ax_stand = plt.subplots(figsize=(8, 6))
        ax_stand.pie(stand_sizes, labels=stand_labels, colors=stand_colors, autopct='%1.1f%%', startangle=90)
        ax_stand.set_title('STAND Distribution', fontweight='bold', fontsize=12)
        st.pyplot(fig_stand)

st.sidebar.title("Monte Carlo Blackjack EV Visualization")
player = st.sidebar.text_input("Player", 15)
dealer_upcard = st.sidebar.number_input("Dealer's Upcard", min_value=1, max_value=11, value=10, step=1)
trials = st.sidebar.number_input("Number of Trials", min_value=1000, max_value=1000000, value=100000, step=1000)

if st.sidebar.button("Visualize EV"):
   player_cards = sum_to_cards_mapper(player)
   visualize_ev_streamlit(player_cards, dealer_upcard, trials)