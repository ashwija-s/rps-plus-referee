import random
from google.adk import Agent

# Game state for Rock-Paper-Scissors-Plus
# This state persists across turns

game_state = {
    "round": 1,              # current round number (starts at 1)
    "max_rounds": 3,         # total rounds allowed
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}

"""
State transition rules:

- round increments after every turn (valid or invalid)
- invalid input still consumes a round
- bomb can be used only once per player
- game_over becomes True after max_rounds are completed
- agent must stop the game when game_over is True
"""


# IMPORTANT:
# All game logic must update and rely on this state object.
# The agent should never guess or invent state.

# -----------------------------
# Tool Functions (Game Logic)
# -----------------------------

def validate_move(move: str, state: dict) -> dict:
    """
    Validates the user's move.

    Returns:
        {
            "valid": bool,
            "reason": str
        }
    """
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    # Normalize input
    move = move.lower().strip()

    # Invalid move
    if move not in valid_moves:
        return {
            "valid": False,
            "reason": "Invalid move"
        }

    # Bomb reuse check
    if move == "bomb" and state["user_bomb_used"]:
        return {
            "valid": False,
            "reason": "Bomb already used"
        }

    return {
        "valid": True,
        "reason": "Valid move"
    }


def resolve_round(user_move: str, bot_move: str, state: dict) -> dict:
    """
    Resolves a single round and updates state.

    Returns:
        {
            "round_winner": "user" | "bot" | "draw",
            "state": updated_state
        }
    """

    # Handle bomb usage flags
    if user_move == "bomb":
        state["user_bomb_used"] = True
    if bot_move == "bomb":
        state["bot_bomb_used"] = True

    # Bomb logic
    if user_move == "bomb" and bot_move == "bomb":
        winner = "draw"
    elif user_move == "bomb":
        winner = "user"
    elif bot_move == "bomb":
        winner = "bot"
    else:
        # Normal RPS logic
        if user_move == bot_move:
            winner = "draw"
        elif (
            (user_move == "rock" and bot_move == "scissors") or
            (user_move == "paper" and bot_move == "rock") or
            (user_move == "scissors" and bot_move == "paper")
        ):
            winner = "user"
        else:
            winner = "bot"

    # Update scores
    if winner == "user":
        state["user_score"] += 1
    elif winner == "bot":
        state["bot_score"] += 1

    # Advance round
    state["round"] += 1

    # Check game over
    if state["round"] > state["max_rounds"]:
        state["game_over"] = True

    return {
        "round_winner": winner,
        "state": state
    }

# NOTE:
# Invalid input still consumes a round.
# In such cases, resolve_round is NOT called,
# but round should still increment and game_over should be checked.

def get_bot_move(state: dict) -> str:
    """
    Selects a valid move for the bot.
    Bot can use bomb only once.
    """
    moves = ["rock", "paper", "scissors"]

    if not state["bot_bomb_used"]:
        moves.append("bomb")

    return random.choice(moves)


def handle_invalid_input(state: dict) -> dict:
    """
    Handles invalid input by consuming a round.
    """
    state["round"] += 1

    if state["round"] > state["max_rounds"]:
        state["game_over"] = True

    return state

def check_game_over(state: dict) -> bool:
    """
    Checks whether the game should end.
    """
    if state["round"] > state["max_rounds"]:
        state["game_over"] = True
        return True
    return False

def get_final_result(state: dict) -> str:
    """
    Determines the final game result.
    """
    if state["user_score"] > state["bot_score"]:
        return "User wins"
    elif state["bot_score"] > state["user_score"]:
        return "Bot wins"
    else:
        return "Draw"
    
agent = Agent(
    name="RPSPlusReferee",
    tools=[
        validate_move,
        resolve_round,
        handle_invalid_input
    ]
)


if __name__ == "__main__":
    print("Welcome to Rock-Paper-Scissors-Plus!")
    print("Rules:")
    print("- Best of 3 rounds")
    print("- Moves: rock, paper, scissors, bomb (once per player)")
    print("- Bomb beats all moves; bomb vs bomb is a draw")
    print("- Invalid input still consumes the round\n")

    state = game_state

    while not state["game_over"]:
        user_input = input(f"Round {state['round']} - Enter your move: ")

        validation = validate_move(user_input, state)

        if not validation["valid"]:
            print(f"Invalid move ({validation['reason']}). Round wasted.")
            state = handle_invalid_input(state)
            check_game_over(state)
            continue

        bot_move = get_bot_move(state)
        result = resolve_round(user_input, bot_move, state)
        state = result["state"]

        print(f"You played: {user_input}")
        print(f"Bot played: {bot_move}")
        if result["round_winner"] == "draw":
            print("Round result: Draw")
        elif result["round_winner"] == "user":
            print("Round result: You win this round")
        print(f"Current score → You: {state['user_score']} | Bot: {state['bot_score']}")
        

        check_game_over(state)

    print("\nGame Over!")
    print("Final score → You:", state["user_score"], "| Bot:", state["bot_score"])
    print("Result:", get_final_result(state))
