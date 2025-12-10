# Should I Hit on 15?

Ever been sitting at a blackjack table wondering if you should hit that 15 against a dealer's 9? 

This project uses **Monte Carlo simulation** to answer that question (and every other "should I hit?" scenario).

## How it works

1. **Pick your hand** - e.g., player has 15 (10 + 5)
2. **Pick the dealer's upcard** - e.g., dealer showing 9
3. **Run Monte Carlo** - simulate thousands of random outcomes

## How to run

1. pip install -r requirements.txt
2. streamlit run monte-carlo-blackjack.py

