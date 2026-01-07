# Rock–Paper–Scissors–Plus Referee Bot

A minimal conversational game referee built using Google ADK, with explicit state management and tool-based game logic.

## State Model

The game maintains an explicit in-memory state object that persists across turns.  
All game behavior is derived from this state.

```python
{
  "round": 1,
  "max_rounds": 3,
  "user_score": 0,
  "bot_score": 0,
  "user_bomb_used": false,
  "bot_bomb_used": false,
  "game_over": false
}

```markdown
## Tool Design

Game logic is separated from conversational flow using explicit tools registered with the ADK agent.

### Tools

- **validate_move(move, state)**
  - Validates user input
  - Enforces allowed moves and one-time bomb usage

- **resolve_round(user_move, bot_move, state)**
  - Determines round outcome
  - Updates scores, bomb flags, and round count

- **handle_invalid_input(state)**
  - Consumes a round on invalid input
  - Ensures invalid moves still affect game progress

This separation ensures that rules and state mutations do not live in prompts and are deterministic.

## Agent Responsibilities

The ADK agent is used as a tool registry and orchestration layer.

The agent:
- Registers and exposes game logic tools
- Enforces clean separation between intent handling and logic

The agent does NOT:
- Contain game rules
- Mutate state directly
- Store game progress in prompts

The conversational loop is implemented as a CLI-style interaction, which is explicitly allowed by the assignment.

## Tradeoffs and Constraints

- A CLI interface was chosen for simplicity and clarity.
- Bot move selection is randomized to keep the focus on state and logic design.
- Due to ADK schema constraints, the agent does not embed a system prompt and instead focuses on tool registration.

Given more time, the system could be extended with richer intent handling or multiple agents, but this was intentionally avoided to keep the solution minimal and correct.
