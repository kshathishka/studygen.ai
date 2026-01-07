"""
Tower of Hanoi - Recursion & Stack visualization
Classic puzzle with configurable disk count
"""
import streamlit as st
from typing import List, Tuple
import time

def render_tower_of_hanoi(learn_mode: bool = True):
    """Main render function for Tower of Hanoi"""
    
    st.header("🗼 Tower of Hanoi")
    st.markdown("""
    **Goal:** Move all disks from Peg A to Peg C!
    
    **Rules:**
    - Only one disk can be moved at a time
    - Only the top disk of a peg can be moved
    - A larger disk cannot be placed on a smaller disk
    """)
    
    # Configuration
    if 'hanoi_disks' not in st.session_state:
        st.session_state.hanoi_disks = 3
    if 'hanoi_pegs' not in st.session_state:
        st.session_state.hanoi_pegs = {
            'A': list(range(st.session_state.hanoi_disks, 0, -1)),
            'B': [],
            'C': []
        }
    if 'hanoi_moves' not in st.session_state:
        st.session_state.hanoi_moves = 0
    if 'hanoi_history' not in st.session_state:
        st.session_state.hanoi_history = []
    if 'hanoi_selected' not in st.session_state:
        st.session_state.hanoi_selected = None
    if 'hanoi_solution_steps' not in st.session_state:
        st.session_state.hanoi_solution_steps = []
    if 'hanoi_current_step' not in st.session_state:
        st.session_state.hanoi_current_step = 0
    if 'hanoi_call_stack' not in st.session_state:
        st.session_state.hanoi_call_stack = []
    
    # Disk configuration
    col1, col2 = st.columns([1, 2])
    with col1:
        new_disks = st.slider("Number of Disks", 3, 8, st.session_state.hanoi_disks)
        if new_disks != st.session_state.hanoi_disks:
            st.session_state.hanoi_disks = new_disks
            st.session_state.hanoi_pegs = {
                'A': list(range(new_disks, 0, -1)),
                'B': [],
                'C': []
            }
            st.session_state.hanoi_moves = 0
            st.session_state.hanoi_history = []
            st.session_state.hanoi_selected = None
            st.session_state.hanoi_solution_steps = []
            st.rerun()
    
    with col2:
        optimal = 2 ** st.session_state.hanoi_disks - 1
        st.metric("Optimal Moves", optimal, help=f"Formula: 2^n - 1 = 2^{st.session_state.hanoi_disks} - 1")
    
    st.markdown("---")
    
    # Render pegs
    pegs = st.session_state.hanoi_pegs
    disk_colors = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '⚫']
    
    def render_peg(peg_name: str, disks: List[int], max_disks: int):
        """Render a single peg with its disks"""
        st.markdown(f"### Peg {peg_name}")
        
        # Visual representation
        max_width = max_disks * 2 + 1
        
        display = []
        for i in range(max_disks, 0, -1):
            if i <= len(disks):
                disk = disks[i-1]
                width = disk * 2 - 1
                padding = (max_width - width) // 2
                bar = disk_colors[disk-1] * width
                display.append(f"{'　' * padding}{bar}{'　' * padding}")
            else:
                padding = max_width // 2
                display.append(f"{'　' * padding}│{'　' * padding}")
        
        display.append("═" * max_width)
        
        for line in display:
            st.markdown(f"`{line}`")
        
        return disks[-1] if disks else None
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_a = render_peg('A', pegs['A'], st.session_state.hanoi_disks)
        selected = st.session_state.hanoi_selected
        
        if selected == 'A':
            st.success("Selected ✓")
        elif st.button("Select A", use_container_width=True, disabled=not pegs['A']):
            if selected and selected != 'A':
                # Try to move
                if can_move(pegs, selected, 'A'):
                    make_move(selected, 'A')
                    st.rerun()
                else:
                    st.error("Invalid move!")
            else:
                st.session_state.hanoi_selected = 'A'
                st.rerun()
    
    with col2:
        top_b = render_peg('B', pegs['B'], st.session_state.hanoi_disks)
        
        if selected == 'B':
            st.success("Selected ✓")
        elif st.button("Select B", use_container_width=True, disabled=not pegs['B'] and not selected):
            if selected and selected != 'B':
                if can_move(pegs, selected, 'B'):
                    make_move(selected, 'B')
                    st.rerun()
                else:
                    st.error("Invalid move!")
            else:
                st.session_state.hanoi_selected = 'B'
                st.rerun()
    
    with col3:
        top_c = render_peg('C', pegs['C'], st.session_state.hanoi_disks)
        
        if selected == 'C':
            st.success("Selected ✓")
        elif st.button("Select C", use_container_width=True, disabled=not pegs['C'] and not selected):
            if selected and selected != 'C':
                if can_move(pegs, selected, 'C'):
                    make_move(selected, 'C')
                    st.rerun()
                else:
                    st.error("Invalid move!")
            else:
                st.session_state.hanoi_selected = 'C'
                st.rerun()
    
    # Move buttons when something is selected
    if st.session_state.hanoi_selected:
        st.info(f"Disk selected from Peg {st.session_state.hanoi_selected}. Click another peg to move, or:")
        if st.button("❌ Cancel Selection"):
            st.session_state.hanoi_selected = None
            st.rerun()
    
    # Check win
    if len(pegs['C']) == st.session_state.hanoi_disks:
        st.balloons()
        st.success(f"🎉 Congratulations! Solved in {st.session_state.hanoi_moves} moves!")
        if st.session_state.hanoi_moves == optimal:
            st.info("🏆 Perfect! Optimal solution!")
            if f"Hanoi-{st.session_state.hanoi_disks}-Optimal" not in st.session_state.achievements:
                st.session_state.achievements.append(f"Hanoi-{st.session_state.hanoi_disks}-Optimal")
    
    st.markdown("---")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("↩️ Undo", disabled=not st.session_state.hanoi_history):
            if st.session_state.hanoi_history:
                prev_state = st.session_state.hanoi_history.pop()
                st.session_state.hanoi_pegs = prev_state
                st.session_state.hanoi_moves = max(0, st.session_state.hanoi_moves - 1)
                st.rerun()
    
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.hanoi_pegs = {
                'A': list(range(st.session_state.hanoi_disks, 0, -1)),
                'B': [],
                'C': []
            }
            st.session_state.hanoi_moves = 0
            st.session_state.hanoi_history = []
            st.session_state.hanoi_selected = None
            st.session_state.hanoi_solution_steps = []
            st.session_state.hanoi_current_step = 0
            st.rerun()
    
    with col3:
        moves = st.session_state.hanoi_moves
        st.metric("Your Moves", moves, delta=f"{moves - optimal:+d} vs optimal" if moves > 0 else None)
    
    # Learn mode
    if learn_mode:
        st.markdown("---")
        st.subheader("🎓 Algorithm Visualization")
        
        tab1, tab2, tab3 = st.tabs(["🤖 Auto-Solve", "📚 Call Stack", "📝 Pseudocode"])
        
        with tab1:
            if st.button("▶️ Generate Solution", use_container_width=True):
                steps = []
                call_stack = []
                solve_hanoi(st.session_state.hanoi_disks, 'A', 'C', 'B', steps, call_stack)
                st.session_state.hanoi_solution_steps = steps
                st.session_state.hanoi_call_stack = call_stack
                st.session_state.hanoi_current_step = 0
            
            if st.session_state.hanoi_solution_steps:
                steps = st.session_state.hanoi_solution_steps
                current = st.session_state.hanoi_current_step
                
                st.markdown(f"**Step {current + 1} of {len(steps)}**")
                st.progress((current + 1) / len(steps))
                
                if current < len(steps):
                    src, dst = steps[current]
                    st.info(f"Move disk from **Peg {src}** to **Peg {dst}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⏮️ Prev", disabled=current == 0):
                        st.session_state.hanoi_current_step -= 1
                        st.rerun()
                with col2:
                    if st.button("▶️ Apply", disabled=current >= len(steps)):
                        src, dst = steps[current]
                        if can_move(st.session_state.hanoi_pegs, src, dst):
                            make_move(src, dst)
                            st.session_state.hanoi_current_step += 1
                            st.rerun()
                with col3:
                    if st.button("⏭️ Next", disabled=current >= len(steps) - 1):
                        st.session_state.hanoi_current_step += 1
                        st.rerun()
        
        with tab2:
            st.markdown("""
            **Recursive Call Stack Visualization**
            
            The recursive algorithm breaks down the problem:
            1. Move n-1 disks from source to auxiliary
            2. Move largest disk from source to destination  
            3. Move n-1 disks from auxiliary to destination
            """)
            
            if st.session_state.hanoi_call_stack:
                call_stack = st.session_state.hanoi_call_stack
                current = min(st.session_state.hanoi_current_step, len(call_stack) - 1)
                
                st.markdown("**Current Call Stack:**")
                for i, call in enumerate(call_stack[:current + 1]):
                    indent = "  " * call['depth']
                    st.code(f"{indent}hanoi({call['n']}, {call['src']}, {call['dst']}, {call['aux']})")
        
        with tab3:
            st.markdown("""
            ```python
            def hanoi(n, source, destination, auxiliary):
                if n == 1:
                    # Base case: move single disk
                    move(source, destination)
                    return
                
                # Step 1: Move n-1 disks to auxiliary
                hanoi(n-1, source, auxiliary, destination)
                
                # Step 2: Move largest disk to destination
                move(source, destination)
                
                # Step 3: Move n-1 disks from auxiliary to destination
                hanoi(n-1, auxiliary, destination, source)
            ```
            
            **Time Complexity:** O(2ⁿ) - exponential
            
            **Recurrence Relation:** T(n) = 2T(n-1) + 1
            
            **Solution:** T(n) = 2ⁿ - 1 moves
            """)
            
            st.info("""
            **Why 2ⁿ - 1 moves?**
            - Each call generates 2 recursive calls + 1 move
            - The recurrence T(n) = 2T(n-1) + 1 solves to 2ⁿ - 1
            - This is provably optimal - no algorithm can do better!
            """)

def can_move(pegs: dict, src: str, dst: str) -> bool:
    """Check if move is valid"""
    if not pegs[src]:
        return False
    if not pegs[dst]:
        return True
    return pegs[src][-1] < pegs[dst][-1]

def make_move(src: str, dst: str):
    """Execute a move"""
    pegs = st.session_state.hanoi_pegs
    # Save state for undo
    import copy
    st.session_state.hanoi_history.append(copy.deepcopy(pegs))
    
    disk = pegs[src].pop()
    pegs[dst].append(disk)
    st.session_state.hanoi_moves += 1
    st.session_state.hanoi_selected = None

def solve_hanoi(n: int, src: str, dst: str, aux: str, steps: list, call_stack: list, depth: int = 0):
    """Generate solution steps with call stack tracking"""
    call_stack.append({'n': n, 'src': src, 'dst': dst, 'aux': aux, 'depth': depth})
    
    if n == 1:
        steps.append((src, dst))
        return
    
    solve_hanoi(n - 1, src, aux, dst, steps, call_stack, depth + 1)
    steps.append((src, dst))
    solve_hanoi(n - 1, aux, dst, src, steps, call_stack, depth + 1)
