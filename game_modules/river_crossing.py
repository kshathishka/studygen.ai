"""
River Crossing Puzzle - State-space search visualization
Classic puzzle: Farmer must transport fox, chicken, and grain across river
"""
import streamlit as st
from collections import deque
from typing import Tuple, List, Set, Dict
import time

# State representation: (farmer, fox, chicken, grain) - True = right bank, False = left bank
State = Tuple[bool, bool, bool, bool]

ITEMS = ['Farmer', 'Fox', 'Chicken', 'Grain']
EMOJIS = {'Farmer': '👨‍🌾', 'Fox': '🦊', 'Chicken': '🐔', 'Grain': '🌾', 'Boat': '🚣'}

def is_valid_state(state: State) -> bool:
    """Check if state is valid (no eating happens)"""
    farmer, fox, chicken, grain = state
    
    # Fox eats chicken if farmer is away
    if fox == chicken and farmer != fox:
        return False
    # Chicken eats grain if farmer is away
    if chicken == grain and farmer != chicken:
        return False
    return True

def get_neighbors(state: State) -> List[State]:
    """Get all valid next states from current state"""
    farmer, fox, chicken, grain = state
    neighbors = []
    
    # Farmer crosses alone
    new_state = (not farmer, fox, chicken, grain)
    if is_valid_state(new_state):
        neighbors.append(new_state)
    
    # Farmer takes fox
    if farmer == fox:
        new_state = (not farmer, not fox, chicken, grain)
        if is_valid_state(new_state):
            neighbors.append(new_state)
    
    # Farmer takes chicken
    if farmer == chicken:
        new_state = (not farmer, fox, not chicken, grain)
        if is_valid_state(new_state):
            neighbors.append(new_state)
    
    # Farmer takes grain
    if farmer == grain:
        new_state = (not farmer, fox, chicken, not grain)
        if is_valid_state(new_state):
            neighbors.append(new_state)
    
    return neighbors

def bfs_solve() -> Tuple[List[State], Dict[State, List[State]]]:
    """Solve using BFS, return path and state tree"""
    start = (False, False, False, False)
    goal = (True, True, True, True)
    
    queue = deque([(start, [start])])
    visited = {start}
    state_tree = {start: []}
    
    while queue:
        current, path = queue.popleft()
        
        if current == goal:
            return path, state_tree
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                state_tree[current] = state_tree.get(current, []) + [neighbor]
                queue.append((neighbor, path + [neighbor]))
    
    return [], state_tree

def dfs_solve() -> Tuple[List[State], Dict[State, List[State]]]:
    """Solve using DFS, return path and state tree"""
    start = (False, False, False, False)
    goal = (True, True, True, True)
    
    stack = [(start, [start])]
    visited = {start}
    state_tree = {start: []}
    
    while stack:
        current, path = stack.pop()
        
        if current == goal:
            return path, state_tree
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                state_tree[current] = state_tree.get(current, []) + [neighbor]
                stack.append((neighbor, path + [neighbor]))
    
    return [], state_tree

def state_to_str(state: State) -> str:
    """Convert state to readable string"""
    farmer, fox, chicken, grain = state
    left = []
    right = []
    
    for i, (item, pos) in enumerate(zip(ITEMS, state)):
        emoji = EMOJIS[item]
        if pos:
            right.append(emoji)
        else:
            left.append(emoji)
    
    return f"{''.join(left) or '(empty)'} | 🌊 | {''.join(right) or '(empty)'}"

def get_move_description(prev: State, curr: State) -> str:
    """Describe the move between two states"""
    items_moved = []
    for i, (p, c) in enumerate(zip(prev, curr)):
        if p != c:
            items_moved.append(ITEMS[i])
    
    direction = "→ Right" if curr[0] else "← Left"
    if len(items_moved) == 1:
        return f"{EMOJIS['Farmer']} Farmer crosses alone {direction}"
    else:
        item = items_moved[1]
        return f"{EMOJIS['Farmer']} Farmer takes {EMOJIS[item]} {item} {direction}"

def render_banks(state: State):
    """Render the river crossing scene"""
    farmer, fox, chicken, grain = state
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown("### 🏖️ Left Bank")
        left_items = []
        if not farmer: left_items.append(f"{EMOJIS['Farmer']} Farmer")
        if not fox: left_items.append(f"{EMOJIS['Fox']} Fox")
        if not chicken: left_items.append(f"{EMOJIS['Chicken']} Chicken")
        if not grain: left_items.append(f"{EMOJIS['Grain']} Grain")
        
        if left_items:
            for item in left_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("*(empty)*")
    
    with col2:
        st.markdown("### 🌊")
        st.markdown(f"## {EMOJIS['Boat']}")
        boat_side = "Right →" if farmer else "← Left"
        st.caption(f"Boat at {boat_side.split()[0]} bank")
    
    with col3:
        st.markdown("### 🏝️ Right Bank")
        right_items = []
        if farmer: right_items.append(f"{EMOJIS['Farmer']} Farmer")
        if fox: right_items.append(f"{EMOJIS['Fox']} Fox")
        if chicken: right_items.append(f"{EMOJIS['Chicken']} Chicken")
        if grain: right_items.append(f"{EMOJIS['Grain']} Grain")
        
        if right_items:
            for item in right_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("*(empty)*")

def render_river_crossing(learn_mode: bool = True):
    """Main render function for River Crossing puzzle"""
    
    st.header("🚣 River Crossing Puzzle")
    st.markdown("""
    **Goal:** Get the farmer, fox, chicken, and grain to the right bank safely!
    
    **Rules:**
    - 🦊 Fox will eat 🐔 Chicken if left alone
    - 🐔 Chicken will eat 🌾 Grain if left alone
    - Only the farmer can row the boat
    - Boat can carry farmer + one item
    """)
    
    # Initialize state
    if 'rc_state' not in st.session_state:
        st.session_state.rc_state = (False, False, False, False)
    if 'rc_moves' not in st.session_state:
        st.session_state.rc_moves = 0
    if 'rc_history' not in st.session_state:
        st.session_state.rc_history = [(False, False, False, False)]
    if 'rc_auto_solving' not in st.session_state:
        st.session_state.rc_auto_solving = False
    if 'rc_solution_step' not in st.session_state:
        st.session_state.rc_solution_step = 0
    if 'rc_solution' not in st.session_state:
        st.session_state.rc_solution = []
    
    state = st.session_state.rc_state
    farmer, fox, chicken, grain = state
    
    st.markdown("---")
    
    # Current scene
    render_banks(state)
    
    st.markdown("---")
    
    # Check win condition
    if state == (True, True, True, True):
        st.balloons()
        st.success(f"🎉 Congratulations! You solved it in {st.session_state.rc_moves} moves!")
        optimal = 7
        if st.session_state.rc_moves == optimal:
            st.info("🏆 Perfect! You achieved the optimal solution!")
            if "River Crossing - Optimal" not in st.session_state.achievements:
                st.session_state.achievements.append("River Crossing - Optimal")
        
        if st.button("🔄 Play Again"):
            st.session_state.rc_state = (False, False, False, False)
            st.session_state.rc_moves = 0
            st.session_state.rc_history = [(False, False, False, False)]
            st.session_state.rc_auto_solving = False
            st.rerun()
        return
    
    # Move buttons
    st.subheader("🎮 Make a Move")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"{EMOJIS['Farmer']} Cross Alone", use_container_width=True):
            new_state = (not farmer, fox, chicken, grain)
            if is_valid_state(new_state):
                st.session_state.rc_state = new_state
                st.session_state.rc_moves += 1
                st.session_state.rc_history.append(new_state)
                st.rerun()
            else:
                st.error("❌ Invalid move! Something will get eaten!")
    
    with col2:
        can_take_fox = farmer == fox
        if st.button(f"{EMOJIS['Fox']} Take Fox", use_container_width=True, disabled=not can_take_fox):
            new_state = (not farmer, not fox, chicken, grain)
            if is_valid_state(new_state):
                st.session_state.rc_state = new_state
                st.session_state.rc_moves += 1
                st.session_state.rc_history.append(new_state)
                st.rerun()
            else:
                st.error("❌ Invalid move! Something will get eaten!")
    
    with col3:
        can_take_chicken = farmer == chicken
        if st.button(f"{EMOJIS['Chicken']} Take Chicken", use_container_width=True, disabled=not can_take_chicken):
            new_state = (not farmer, fox, not chicken, grain)
            if is_valid_state(new_state):
                st.session_state.rc_state = new_state
                st.session_state.rc_moves += 1
                st.session_state.rc_history.append(new_state)
                st.rerun()
            else:
                st.error("❌ Invalid move! Something will get eaten!")
    
    with col4:
        can_take_grain = farmer == grain
        if st.button(f"{EMOJIS['Grain']} Take Grain", use_container_width=True, disabled=not can_take_grain):
            new_state = (not farmer, fox, chicken, not grain)
            if is_valid_state(new_state):
                st.session_state.rc_state = new_state
                st.session_state.rc_moves += 1
                st.session_state.rc_history.append(new_state)
                st.rerun()
            else:
                st.error("❌ Invalid move! Something will get eaten!")
    
    # Control buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("↩️ Undo", use_container_width=True, disabled=len(st.session_state.rc_history) <= 1):
            st.session_state.rc_history.pop()
            st.session_state.rc_state = st.session_state.rc_history[-1]
            st.session_state.rc_moves = max(0, st.session_state.rc_moves - 1)
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.rc_state = (False, False, False, False)
            st.session_state.rc_moves = 0
            st.session_state.rc_history = [(False, False, False, False)]
            st.session_state.rc_auto_solving = False
            st.rerun()
    
    with col3:
        st.metric("Moves", st.session_state.rc_moves, delta=f"Optimal: 7")
    
    # Learn Mode features
    if learn_mode:
        st.markdown("---")
        st.subheader("🎓 Algorithm Visualization")
        
        tab1, tab2, tab3 = st.tabs(["🤖 Auto-Solve", "🌳 State Tree", "📝 Pseudocode"])
        
        with tab1:
            algo = st.radio("Algorithm:", ["BFS (Breadth-First Search)", "DFS (Depth-First Search)"], horizontal=True)
            
            if st.button("▶️ Solve Step-by-Step", use_container_width=True):
                if "BFS" in algo:
                    solution, tree = bfs_solve()
                else:
                    solution, tree = dfs_solve()
                
                st.session_state.rc_solution = solution
                st.session_state.rc_solution_step = 0
                st.session_state.rc_auto_solving = True
            
            if st.session_state.rc_auto_solving and st.session_state.rc_solution:
                solution = st.session_state.rc_solution
                step = st.session_state.rc_solution_step
                
                st.markdown(f"**Step {step + 1} of {len(solution)}**")
                
                progress = (step + 1) / len(solution)
                st.progress(progress)
                
                if step > 0:
                    st.info(get_move_description(solution[step-1], solution[step]))
                
                st.markdown(f"State: `{state_to_str(solution[step])}`")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⏮️ Previous", disabled=step == 0):
                        st.session_state.rc_solution_step -= 1
                        st.session_state.rc_state = solution[st.session_state.rc_solution_step]
                        st.rerun()
                with col2:
                    if st.button("⏭️ Next", disabled=step >= len(solution) - 1):
                        st.session_state.rc_solution_step += 1
                        st.session_state.rc_state = solution[st.session_state.rc_solution_step]
                        st.session_state.rc_moves = st.session_state.rc_solution_step
                        st.rerun()
        
        with tab2:
            st.markdown("""
            **State Space Tree:**
            
            Each node represents a state: `(Farmer, Fox, Chicken, Grain)`
            - `0` = Left bank
            - `1` = Right bank
            """)
            
            solution, tree = bfs_solve()
            
            st.markdown("**Solution Path:**")
            for i, s in enumerate(solution):
                prefix = "→ " if i > 0 else "  "
                highlight = "**" if s == state else ""
                st.markdown(f"{prefix}{highlight}`{s}` - {state_to_str(s)}{highlight}")
        
        with tab3:
            st.markdown("""
            ```python
            def bfs_solve():
                start = (False, False, False, False)  # All on left
                goal = (True, True, True, True)       # All on right
                
                queue = [(start, [start])]  # (state, path)
                visited = {start}
                
                while queue:
                    current, path = queue.pop(0)  # FIFO
                    
                    if current == goal:
                        return path  # Found solution!
                    
                    for neighbor in get_valid_moves(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))
                
                return None  # No solution
            ```
            
            **Time Complexity:** O(V + E) where V = states, E = transitions
            
            **Space Complexity:** O(V) for visited set and queue
            """)
            
            st.info("""
            **Why BFS finds the optimal solution:**
            BFS explores all states at depth d before moving to depth d+1.
            This guarantees the first solution found has the minimum number of moves.
            """)
