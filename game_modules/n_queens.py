"""
N-Queens Solver - Backtracking algorithm visualization
Place N queens on an N×N chessboard so no two attack each other
"""
import streamlit as st
from typing import List, Tuple, Set
import time

def render_n_queens(learn_mode: bool = True):
    """Main render function for N-Queens puzzle"""
    
    st.header("👑 N-Queens Solver")
    st.markdown("""
    **Goal:** Place N queens on an N×N board so no two queens attack each other!
    
    **Rules:**
    - Queens can attack horizontally, vertically, and diagonally
    - No two queens can share a row, column, or diagonal
    """)
    
    # Initialize state
    if 'nq_n' not in st.session_state:
        st.session_state.nq_n = 4
    if 'nq_board' not in st.session_state:
        st.session_state.nq_board = [[False] * 4 for _ in range(4)]
    if 'nq_solutions' not in st.session_state:
        st.session_state.nq_solutions = []
    if 'nq_current_solution' not in st.session_state:
        st.session_state.nq_current_solution = 0
    if 'nq_backtrack_steps' not in st.session_state:
        st.session_state.nq_backtrack_steps = []
    if 'nq_current_step' not in st.session_state:
        st.session_state.nq_current_step = 0
    
    # Configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_n = st.slider("Board Size (N)", 4, 8, st.session_state.nq_n)
        if new_n != st.session_state.nq_n:
            st.session_state.nq_n = new_n
            st.session_state.nq_board = [[False] * new_n for _ in range(new_n)]
            st.session_state.nq_solutions = []
            st.session_state.nq_backtrack_steps = []
            st.rerun()
    
    with col2:
        queens_placed = sum(sum(row) for row in st.session_state.nq_board)
        st.metric("Queens Placed", f"{queens_placed}/{st.session_state.nq_n}")
    
    with col3:
        conflicts = count_conflicts(st.session_state.nq_board)
        st.metric("Conflicts", conflicts, delta=None if conflicts == 0 else "Fix needed", delta_color="inverse")
    
    st.markdown("---")
    
    n = st.session_state.nq_n
    board = st.session_state.nq_board
    
    # Get attacked squares
    attacked = get_attacked_squares(board, n)
    
    # Render board
    st.subheader("♟️ Chessboard")
    
    # Create board display
    cols = st.columns(n + 1)
    
    # Header row with column numbers
    with cols[0]:
        st.write("")
    for j in range(n):
        with cols[j + 1]:
            st.markdown(f"**{j + 1}**")
    
    # Board rows
    for i in range(n):
        cols = st.columns(n + 1)
        with cols[0]:
            st.markdown(f"**{i + 1}**")
        
        for j in range(n):
            with cols[j + 1]:
                is_queen = board[i][j]
                is_attacked = attacked[i][j]
                is_dark = (i + j) % 2 == 1
                
                if is_queen:
                    btn_label = "👑"
                    btn_type = "primary"
                elif is_attacked:
                    btn_label = "⚔️" if is_dark else "⚔️"
                else:
                    btn_label = "⬛" if is_dark else "⬜"
                
                if st.button(btn_label, key=f"cell_{i}_{j}", use_container_width=True):
                    # Toggle queen
                    board[i][j] = not board[i][j]
                    st.rerun()
    
    # Legend
    st.caption("👑 = Queen | ⚔️ = Under attack | Click to place/remove queen")
    
    # Check win
    if queens_placed == n and conflicts == 0:
        st.balloons()
        st.success("🎉 Congratulations! You solved the N-Queens puzzle!")
        if f"NQueens-{n}" not in st.session_state.achievements:
            st.session_state.achievements.append(f"NQueens-{n}")
    
    st.markdown("---")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear Board", use_container_width=True):
            st.session_state.nq_board = [[False] * n for _ in range(n)]
            st.rerun()
    
    with col2:
        if st.button("🎲 Random Valid", use_container_width=True):
            solutions = find_all_solutions(n)
            if solutions:
                import random
                solution = random.choice(solutions)
                new_board = [[False] * n for _ in range(n)]
                for row, col in enumerate(solution):
                    new_board[row][col] = True
                st.session_state.nq_board = new_board
                st.rerun()
    
    with col3:
        if st.button("🔍 Find All Solutions", use_container_width=True):
            solutions = find_all_solutions(n)
            st.session_state.nq_solutions = solutions
            st.session_state.nq_current_solution = 0
            st.success(f"Found {len(solutions)} solutions!")
    
    # Solutions browser
    if st.session_state.nq_solutions:
        st.markdown("---")
        st.subheader(f"📚 Solutions ({len(st.session_state.nq_solutions)} found)")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⏮️ Previous"):
                st.session_state.nq_current_solution = max(0, st.session_state.nq_current_solution - 1)
                apply_solution(st.session_state.nq_solutions[st.session_state.nq_current_solution], n)
                st.rerun()
        
        with col2:
            current = st.session_state.nq_current_solution
            total = len(st.session_state.nq_solutions)
            st.markdown(f"**Solution {current + 1} of {total}**")
        
        with col3:
            if st.button("⏭️ Next"):
                st.session_state.nq_current_solution = min(len(st.session_state.nq_solutions) - 1, 
                                                           st.session_state.nq_current_solution + 1)
                apply_solution(st.session_state.nq_solutions[st.session_state.nq_current_solution], n)
                st.rerun()
    
    # Learn mode
    if learn_mode:
        st.markdown("---")
        st.subheader("🎓 Algorithm Visualization")
        
        tab1, tab2, tab3 = st.tabs(["🔄 Backtracking Demo", "📊 Complexity", "📝 Pseudocode"])
        
        with tab1:
            if st.button("▶️ Visualize Backtracking", use_container_width=True):
                steps = []
                visualize_backtracking(n, [], steps)
                st.session_state.nq_backtrack_steps = steps
                st.session_state.nq_current_step = 0
            
            if st.session_state.nq_backtrack_steps:
                steps = st.session_state.nq_backtrack_steps
                current = st.session_state.nq_current_step
                
                st.markdown(f"**Step {current + 1} of {len(steps)}**")
                st.progress((current + 1) / len(steps))
                
                if current < len(steps):
                    step = steps[current]
                    action = step['action']
                    pos = step.get('position', None)
                    
                    if action == 'try':
                        st.info(f"🔵 Trying queen at row {pos[0] + 1}, column {pos[1] + 1}")
                    elif action == 'place':
                        st.success(f"✅ Placed queen at row {pos[0] + 1}, column {pos[1] + 1}")
                    elif action == 'conflict':
                        st.error(f"❌ Conflict! Cannot place at row {pos[0] + 1}, column {pos[1] + 1}")
                    elif action == 'backtrack':
                        st.warning(f"⬅️ Backtracking - removing queen from row {pos[0] + 1}")
                    elif action == 'solution':
                        st.success("🎉 Solution found!")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⏮️ Prev Step", disabled=current == 0):
                        st.session_state.nq_current_step -= 1
                        st.rerun()
                with col2:
                    if st.button("⏭️ Next Step", disabled=current >= len(steps) - 1):
                        st.session_state.nq_current_step += 1
                        st.rerun()
        
        with tab2:
            st.markdown(f"""
            **For N = {n}:**
            
            | Metric | Value |
            |--------|-------|
            | Board Size | {n} × {n} = {n*n} squares |
            | Naive Search Space | {n}^{n} = {n**n:,} configurations |
            | Valid Solutions | {len(find_all_solutions(n))} |
            | Time Complexity | O(N!) |
            | Space Complexity | O(N) |
            """)
            
            st.info("""
            **Why O(N!) and not O(N^N)?**
            
            With backtracking, we prune invalid branches early:
            - Each row has at most N choices
            - But previous placements reduce valid columns
            - Average branching factor < N
            - Effective complexity closer to O(N!)
            """)
        
        with tab3:
            st.markdown("""
            ```python
            def solve_n_queens(n):
                solutions = []
                
                def backtrack(row, columns, diag1, diag2, current):
                    if row == n:
                        solutions.append(current[:])
                        return
                    
                    for col in range(n):
                        # Check constraints
                        if col in columns:
                            continue  # Column conflict
                        if (row - col) in diag1:
                            continue  # Main diagonal conflict
                        if (row + col) in diag2:
                            continue  # Anti-diagonal conflict
                        
                        # Place queen
                        columns.add(col)
                        diag1.add(row - col)
                        diag2.add(row + col)
                        current.append(col)
                        
                        # Recurse
                        backtrack(row + 1, columns, diag1, diag2, current)
                        
                        # Backtrack (remove queen)
                        columns.remove(col)
                        diag1.remove(row - col)
                        diag2.remove(row + col)
                        current.pop()
                
                backtrack(0, set(), set(), set(), [])
                return solutions
            ```
            
            **Key Insight:** Use sets for O(1) conflict checking!
            - `columns`: tracks occupied columns
            - `diag1`: main diagonals (row - col is constant)
            - `diag2`: anti-diagonals (row + col is constant)
            """)

def get_attacked_squares(board: List[List[bool]], n: int) -> List[List[bool]]:
    """Get all squares under attack"""
    attacked = [[False] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if board[i][j]:
                # Mark row, column, diagonals
                for k in range(n):
                    attacked[i][k] = True  # Row
                    attacked[k][j] = True  # Column
                    
                    # Diagonals
                    if 0 <= i + k < n and 0 <= j + k < n:
                        attacked[i + k][j + k] = True
                    if 0 <= i - k < n and 0 <= j - k < n:
                        attacked[i - k][j - k] = True
                    if 0 <= i + k < n and 0 <= j - k < n:
                        attacked[i + k][j - k] = True
                    if 0 <= i - k < n and 0 <= j + k < n:
                        attacked[i - k][j + k] = True
    
    return attacked

def count_conflicts(board: List[List[bool]]) -> int:
    """Count queen conflicts"""
    n = len(board)
    queens = [(i, j) for i in range(n) for j in range(n) if board[i][j]]
    conflicts = 0
    
    for i, (r1, c1) in enumerate(queens):
        for r2, c2 in queens[i + 1:]:
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1
    
    return conflicts

def find_all_solutions(n: int) -> List[List[int]]:
    """Find all N-Queens solutions using backtracking"""
    solutions = []
    
    def backtrack(row: int, cols: Set[int], d1: Set[int], d2: Set[int], current: List[int]):
        if row == n:
            solutions.append(current[:])
            return
        
        for col in range(n):
            if col in cols or (row - col) in d1 or (row + col) in d2:
                continue
            
            cols.add(col)
            d1.add(row - col)
            d2.add(row + col)
            current.append(col)
            
            backtrack(row + 1, cols, d1, d2, current)
            
            cols.remove(col)
            d1.remove(row - col)
            d2.remove(row + col)
            current.pop()
    
    backtrack(0, set(), set(), set(), [])
    return solutions

def apply_solution(solution: List[int], n: int):
    """Apply a solution to the board"""
    board = [[False] * n for _ in range(n)]
    for row, col in enumerate(solution):
        board[row][col] = True
    st.session_state.nq_board = board

def visualize_backtracking(n: int, current: List[int], steps: List[dict], max_steps: int = 100):
    """Generate backtracking visualization steps"""
    
    def backtrack(row: int, cols: Set[int], d1: Set[int], d2: Set[int]):
        if len(steps) >= max_steps:
            return True
        
        if row == n:
            steps.append({'action': 'solution', 'board': current[:]})
            return True
        
        for col in range(n):
            steps.append({'action': 'try', 'position': (row, col)})
            
            if col in cols or (row - col) in d1 or (row + col) in d2:
                steps.append({'action': 'conflict', 'position': (row, col)})
                continue
            
            cols.add(col)
            d1.add(row - col)
            d2.add(row + col)
            current.append(col)
            steps.append({'action': 'place', 'position': (row, col)})
            
            if backtrack(row + 1, cols, d1, d2):
                return True
            
            steps.append({'action': 'backtrack', 'position': (row, current[-1] if current else 0)})
            cols.remove(col)
            d1.remove(row - col)
            d2.remove(row + col)
            current.pop()
        
        return False
    
    backtrack(0, set(), set(), set())
