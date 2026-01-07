"""
Maze Generator & Solver - Graph algorithms visualization
Generate mazes with various algorithms and solve with pathfinding
"""
import streamlit as st
from typing import List, Tuple, Set, Dict, Optional
from collections import deque
import random
import heapq

# Cell types
WALL = 1
PATH = 0
START = 2
END = 3
VISITED = 4
FRONTIER = 5
SOLUTION = 6

def render_maze_solver(learn_mode: bool = True):
    """Main render function for Maze Generator & Solver"""
    
    st.header("🌀 Maze Generator & Solver")
    st.markdown("""
    **Generate** mazes using different algorithms and **solve** them with pathfinding!
    
    Watch how different algorithms explore the maze to find the optimal path.
    """)
    
    # Initialize state
    if 'maze_grid' not in st.session_state:
        st.session_state.maze_grid = generate_empty_maze(15, 15)
    if 'maze_width' not in st.session_state:
        st.session_state.maze_width = 15
    if 'maze_height' not in st.session_state:
        st.session_state.maze_height = 15
    if 'maze_start' not in st.session_state:
        st.session_state.maze_start = (1, 1)
    if 'maze_end' not in st.session_state:
        st.session_state.maze_end = (13, 13)
    if 'maze_solve_steps' not in st.session_state:
        st.session_state.maze_solve_steps = []
    if 'maze_current_step' not in st.session_state:
        st.session_state.maze_current_step = 0
    if 'maze_edit_mode' not in st.session_state:
        st.session_state.maze_edit_mode = None
    
    # Configuration
    st.subheader("⚙️ Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        width = st.slider("Width", 11, 31, st.session_state.maze_width, step=2)
        height = st.slider("Height", 11, 31, st.session_state.maze_height, step=2)
    
    with col2:
        gen_algorithm = st.selectbox("Generation Algorithm", [
            "Recursive Backtracking",
            "Prim's Algorithm",
            "Kruskal's Algorithm"
        ])
    
    with col3:
        solve_algorithm = st.selectbox("Solving Algorithm", [
            "BFS (Breadth-First Search)",
            "DFS (Depth-First Search)",
            "A* (A-Star)"
        ])
    
    # Generation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Generate Maze", use_container_width=True):
            st.session_state.maze_width = width
            st.session_state.maze_height = height
            
            if gen_algorithm == "Recursive Backtracking":
                maze = generate_maze_recursive_backtracking(width, height)
            elif gen_algorithm == "Prim's Algorithm":
                maze = generate_maze_prims(width, height)
            else:
                maze = generate_maze_kruskals(width, height)
            
            st.session_state.maze_grid = maze
            st.session_state.maze_start = (1, 1)
            st.session_state.maze_end = (height - 2, width - 2)
            st.session_state.maze_solve_steps = []
            st.session_state.maze_current_step = 0
            st.rerun()
    
    with col2:
        if st.button("🔄 Clear Solution", use_container_width=True):
            # Clear visited/solution markers
            grid = st.session_state.maze_grid
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] in [VISITED, FRONTIER, SOLUTION]:
                        grid[i][j] = PATH
            st.session_state.maze_solve_steps = []
            st.session_state.maze_current_step = 0
            st.rerun()
    
    with col3:
        if st.button("🗑️ Empty Maze", use_container_width=True):
            st.session_state.maze_grid = generate_empty_maze(width, height)
            st.session_state.maze_width = width
            st.session_state.maze_height = height
            st.session_state.maze_solve_steps = []
            st.rerun()
    
    st.markdown("---")
    
    # Maze display
    st.subheader("🗺️ Maze")
    
    render_maze(st.session_state.maze_grid, st.session_state.maze_start, st.session_state.maze_end)
    
    # Legend
    st.markdown("""
    ⬛ Wall | ⬜ Path | 🟢 Start | 🔴 End | 🟦 Visited | 🟨 Frontier | 🟩 Solution
    """)
    
    # Edit mode
    st.markdown("---")
    st.subheader("✏️ Edit Mode")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🟢 Set Start", use_container_width=True):
            st.session_state.maze_edit_mode = "start"
            st.info("Click on maze to set start position")
    
    with col2:
        if st.button("🔴 Set End", use_container_width=True):
            st.session_state.maze_edit_mode = "end"
            st.info("Click on maze to set end position")
    
    with col3:
        if st.button("⬛ Draw Walls", use_container_width=True):
            st.session_state.maze_edit_mode = "wall"
            st.info("Click on maze to toggle walls")
    
    with col4:
        if st.button("❌ Cancel Edit", use_container_width=True):
            st.session_state.maze_edit_mode = None
    
    if st.session_state.maze_edit_mode:
        st.warning(f"Edit mode: {st.session_state.maze_edit_mode.upper()}")
    
    st.markdown("---")
    
    # Solving controls
    st.subheader("🔍 Solve Maze")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Solve Maze", use_container_width=True):
            grid = st.session_state.maze_grid
            start = st.session_state.maze_start
            end = st.session_state.maze_end
            
            # Clear previous solution
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] in [VISITED, FRONTIER, SOLUTION]:
                        grid[i][j] = PATH
            
            if "BFS" in solve_algorithm:
                steps = list(solve_maze_bfs(grid, start, end))
            elif "DFS" in solve_algorithm:
                steps = list(solve_maze_dfs(grid, start, end))
            else:
                steps = list(solve_maze_astar(grid, start, end))
            
            st.session_state.maze_solve_steps = steps
            st.session_state.maze_current_step = 0
            st.rerun()
    
    with col2:
        if st.button("⏩ Solve Instantly", use_container_width=True):
            grid = st.session_state.maze_grid
            start = st.session_state.maze_start
            end = st.session_state.maze_end
            
            # Clear and solve
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] in [VISITED, FRONTIER, SOLUTION]:
                        grid[i][j] = PATH
            
            if "BFS" in solve_algorithm:
                steps = list(solve_maze_bfs(grid, start, end))
            elif "DFS" in solve_algorithm:
                steps = list(solve_maze_dfs(grid, start, end))
            else:
                steps = list(solve_maze_astar(grid, start, end))
            
            # Apply final step
            if steps:
                final = steps[-1]
                for pos in final.get('visited', []):
                    if grid[pos[0]][pos[1]] == PATH:
                        grid[pos[0]][pos[1]] = VISITED
                for pos in final.get('path', []):
                    if grid[pos[0]][pos[1]] in [PATH, VISITED]:
                        grid[pos[0]][pos[1]] = SOLUTION
            
            st.session_state.maze_solve_steps = steps
            st.session_state.maze_current_step = len(steps) - 1 if steps else 0
            st.rerun()
    
    # Step controls
    if st.session_state.maze_solve_steps:
        steps = st.session_state.maze_solve_steps
        current = st.session_state.maze_current_step
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⏮️ Prev", disabled=current == 0):
                st.session_state.maze_current_step -= 1
                apply_solve_step(current - 1)
                st.rerun()
        
        with col2:
            st.progress((current + 1) / len(steps))
            st.caption(f"Step {current + 1} of {len(steps)}")
        
        with col3:
            if st.button("⏭️ Next", disabled=current >= len(steps) - 1):
                st.session_state.maze_current_step += 1
                apply_solve_step(current + 1)
                st.rerun()
        
        # Stats
        if current < len(steps):
            step = steps[current]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Cells Visited", len(step.get('visited', [])))
            with col2:
                st.metric("Frontier Size", len(step.get('frontier', [])))
            with col3:
                path_len = len(step.get('path', []))
                st.metric("Path Length", path_len if path_len > 0 else "—")
    
    # Learn mode
    if learn_mode:
        st.markdown("---")
        st.subheader("🎓 Algorithm Details")
        
        tab1, tab2, tab3 = st.tabs(["🏗️ Generation", "🔍 Solving", "📊 Comparison"])
        
        with tab1:
            render_generation_info(gen_algorithm)
        
        with tab2:
            render_solving_info(solve_algorithm)
        
        with tab3:
            render_algorithm_comparison_maze()

def generate_empty_maze(width: int, height: int) -> List[List[int]]:
    """Generate empty maze with walls on border"""
    maze = [[PATH for _ in range(width)] for _ in range(height)]
    
    # Add border walls
    for i in range(height):
        maze[i][0] = WALL
        maze[i][width - 1] = WALL
    for j in range(width):
        maze[0][j] = WALL
        maze[height - 1][j] = WALL
    
    return maze

def generate_maze_recursive_backtracking(width: int, height: int) -> List[List[int]]:
    """Generate maze using recursive backtracking (DFS)"""
    # Start with all walls
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    
    def carve(x: int, y: int):
        maze[y][x] = PATH
        
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == WALL:
                maze[y + dy // 2][x + dx // 2] = PATH
                carve(nx, ny)
    
    # Start from (1, 1)
    carve(1, 1)
    
    return maze

def generate_maze_prims(width: int, height: int) -> List[List[int]]:
    """Generate maze using Prim's algorithm"""
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    
    # Start cell
    start_x, start_y = 1, 1
    maze[start_y][start_x] = PATH
    
    # Frontier walls
    frontier = []
    
    def add_frontier(x: int, y: int):
        for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1:
                if maze[ny][nx] == WALL and (nx, ny) not in frontier:
                    frontier.append((nx, ny))
    
    add_frontier(start_x, start_y)
    
    while frontier:
        # Pick random frontier cell
        x, y = random.choice(frontier)
        frontier.remove((x, y))
        
        # Find adjacent carved cells
        neighbors = []
        for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1:
                if maze[ny][nx] == PATH:
                    neighbors.append((nx, ny, dx, dy))
        
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[y][x] = PATH
            maze[y - dy // 2][x - dx // 2] = PATH
            add_frontier(x, y)
    
    return maze

def generate_maze_kruskals(width: int, height: int) -> List[List[int]]:
    """Generate maze using Kruskal's algorithm"""
    maze = [[WALL for _ in range(width)] for _ in range(height)]
    
    # Create cells
    cells = {}
    cell_id = 0
    for y in range(1, height - 1, 2):
        for x in range(1, width - 1, 2):
            maze[y][x] = PATH
            cells[(x, y)] = cell_id
            cell_id += 1
    
    # Create list of walls between cells
    walls = []
    for y in range(1, height - 1, 2):
        for x in range(1, width - 1, 2):
            if x + 2 < width - 1:
                walls.append(((x, y), (x + 2, y), (x + 1, y)))
            if y + 2 < height - 1:
                walls.append(((x, y), (x, y + 2), (x, y + 1)))
    
    random.shuffle(walls)
    
    # Union-Find
    def find(cell):
        if cells[cell] != cell:
            cells[cell] = find(cells[cells[cell]]) if cells[cell] in cells else cells[cell]
        return cells[cell]
    
    def union(c1, c2):
        r1, r2 = find(c1), find(c2)
        if r1 != r2:
            for c in cells:
                if cells[c] == r2:
                    cells[c] = r1
            return True
        return False
    
    for cell1, cell2, wall in walls:
        if find(cell1) != find(cell2):
            union(cell1, cell2)
            maze[wall[1]][wall[0]] = PATH
    
    return maze

def render_maze(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    """Render maze as colored grid"""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    
    cell_colors = {
        WALL: "⬛",
        PATH: "⬜",
        VISITED: "🟦",
        FRONTIER: "🟨",
        SOLUTION: "🟩"
    }
    
    maze_html = ""
    for i in range(height):
        row = ""
        for j in range(width):
            if (i, j) == start:
                row += "🟢"
            elif (i, j) == end:
                row += "🔴"
            else:
                row += cell_colors.get(grid[i][j], "⬜")
        maze_html += row + "\n"
    
    st.text(maze_html)

def solve_maze_bfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    """Solve maze using BFS"""
    height, width = len(grid), len(grid[0])
    
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        # Yield current state
        yield {
            'visited': list(visited),
            'frontier': list(queue),
            'current': current,
            'path': []
        }
        
        if current == end:
            # Reconstruct path
            path = []
            node = end
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            yield {
                'visited': list(visited),
                'frontier': [],
                'current': end,
                'path': path
            }
            return
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny][nx] != WALL and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    parent[(ny, nx)] = current
                    queue.append((ny, nx))
    
    yield {'visited': list(visited), 'frontier': [], 'path': [], 'error': 'No path found'}

def solve_maze_dfs(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    """Solve maze using DFS"""
    height, width = len(grid), len(grid[0])
    
    stack = [start]
    visited = {start}
    parent = {start: None}
    
    while stack:
        current = stack.pop()
        
        yield {
            'visited': list(visited),
            'frontier': list(stack),
            'current': current,
            'path': []
        }
        
        if current == end:
            path = []
            node = end
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            yield {
                'visited': list(visited),
                'frontier': [],
                'path': path
            }
            return
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny][nx] != WALL and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    parent[(ny, nx)] = current
                    stack.append((ny, nx))
    
    yield {'visited': list(visited), 'frontier': [], 'path': [], 'error': 'No path found'}

def solve_maze_astar(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    """Solve maze using A* with Manhattan distance heuristic"""
    height, width = len(grid), len(grid[0])
    
    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_set = [(heuristic(start, end), 0, start)]
    visited = set()
    g_score = {start: 0}
    parent = {start: None}
    
    while open_set:
        _, _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        frontier_nodes = [node for _, _, node in open_set]
        yield {
            'visited': list(visited),
            'frontier': frontier_nodes,
            'current': current,
            'path': []
        }
        
        if current == end:
            path = []
            node = end
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            yield {
                'visited': list(visited),
                'frontier': [],
                'path': path
            }
            return
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            ny, nx = current[0] + dy, current[1] + dx
            
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny][nx] != WALL:
                    tentative_g = g_score[current] + 1
                    
                    if (ny, nx) not in g_score or tentative_g < g_score[(ny, nx)]:
                        g_score[(ny, nx)] = tentative_g
                        f_score = tentative_g + heuristic((ny, nx), end)
                        heapq.heappush(open_set, (f_score, tentative_g, (ny, nx)))
                        parent[(ny, nx)] = current
    
    yield {'visited': list(visited), 'frontier': [], 'path': [], 'error': 'No path found'}

def apply_solve_step(step_index: int):
    """Apply a solving step to the maze"""
    steps = st.session_state.maze_solve_steps
    grid = st.session_state.maze_grid
    
    # Clear previous markers
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in [VISITED, FRONTIER, SOLUTION]:
                grid[i][j] = PATH
    
    if step_index < len(steps):
        step = steps[step_index]
        
        for pos in step.get('visited', []):
            if grid[pos[0]][pos[1]] == PATH:
                grid[pos[0]][pos[1]] = VISITED
        
        for pos in step.get('frontier', []):
            if grid[pos[0]][pos[1]] in [PATH, VISITED]:
                grid[pos[0]][pos[1]] = FRONTIER
        
        for pos in step.get('path', []):
            if grid[pos[0]][pos[1]] in [PATH, VISITED]:
                grid[pos[0]][pos[1]] = SOLUTION

def render_generation_info(algorithm: str):
    """Render info about maze generation algorithm"""
    info = {
        "Recursive Backtracking": """
**Recursive Backtracking (DFS)**

1. Start with a grid full of walls
2. Pick a random starting cell, mark it as path
3. Randomly choose an unvisited neighbor
4. Remove wall between current and neighbor
5. Recursively repeat from neighbor
6. Backtrack when stuck

```python
def generate(x, y):
    maze[y][x] = PATH
    for dx, dy in shuffle(directions):
        nx, ny = x + dx*2, y + dy*2
        if valid(nx, ny) and is_wall(nx, ny):
            maze[y+dy][x+dx] = PATH  # Remove wall
            generate(nx, ny)
```

**Properties:**
- Creates long, winding passages
- Low branching factor
- Bias towards long corridors
        """,
        "Prim's Algorithm": """
**Prim's Algorithm (Random)**

1. Start with grid of walls, pick random cell
2. Add neighboring walls to frontier
3. Pick random frontier wall
4. If connects to unvisited cell, carve passage
5. Add new cell's walls to frontier
6. Repeat until frontier empty

**Properties:**
- Creates more branching passages
- Feels more "organic"
- Many short dead ends
        """,
        "Kruskal's Algorithm": """
**Kruskal's Algorithm (Union-Find)**

1. Create cells as separate sets
2. List all walls between adjacent cells
3. Randomly pick a wall
4. If wall separates different sets, remove it and union sets
5. Repeat until all cells in same set

**Properties:**
- More uniform distribution
- Multiple paths feeling
- Uses Union-Find data structure
        """
    }
    st.markdown(info.get(algorithm, "Info not available"))

def render_solving_info(algorithm: str):
    """Render info about maze solving algorithm"""
    info = {
        "BFS (Breadth-First Search)": """
**Breadth-First Search**

Explores all neighbors before going deeper. Uses a **queue** (FIFO).

```python
def bfs(start, end):
    queue = [start]
    visited = {start}
    
    while queue:
        current = queue.pop(0)  # FIFO
        if current == end:
            return reconstruct_path()
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Properties:**
- ✅ Guarantees shortest path
- ❌ Explores many unnecessary cells
- Time: O(V + E)
- Space: O(V)
        """,
        "DFS (Depth-First Search)": """
**Depth-First Search**

Explores as far as possible before backtracking. Uses a **stack** (LIFO).

```python
def dfs(start, end):
    stack = [start]
    visited = {start}
    
    while stack:
        current = stack.pop()  # LIFO
        if current == end:
            return reconstruct_path()
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
```

**Properties:**
- ❌ Does NOT guarantee shortest path
- ✅ Uses less memory
- Time: O(V + E)
- Space: O(V) worst, O(depth) typical
        """,
        "A* (A-Star)": """
**A* Search**

Uses heuristic to guide search towards goal. Priority queue ordered by f(n) = g(n) + h(n).

```python
def astar(start, end):
    open_set = [(heuristic(start, end), start)]
    g_score = {start: 0}
    
    while open_set:
        _, current = heappop(open_set)
        if current == end:
            return reconstruct_path()
        
        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, inf):
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, end)
                heappush(open_set, (f, neighbor))
```

**Heuristic:** Manhattan distance = |x1-x2| + |y1-y2|

**Properties:**
- ✅ Guarantees shortest path (with admissible heuristic)
- ✅ More efficient than BFS
- Optimal when h(n) ≤ actual distance
        """
    }
    st.markdown(info.get(algorithm, "Info not available"))

def render_algorithm_comparison_maze():
    """Render comparison of maze algorithms"""
    st.markdown("""
    ### Generation Algorithms
    
    | Algorithm | Bias | Passages | Memory |
    |-----------|------|----------|--------|
    | Recursive Backtracking | Long corridors | Few branches | O(cells) stack |
    | Prim's | Short dead ends | Many branches | O(frontier) |
    | Kruskal's | Uniform | Balanced | O(cells) for union-find |
    
    ### Solving Algorithms
    
    | Algorithm | Shortest Path? | Time | Space | Best For |
    |-----------|---------------|------|-------|----------|
    | BFS | ✅ Yes | O(V+E) | O(V) | Unweighted graphs |
    | DFS | ❌ No | O(V+E) | O(depth) | Memory constrained |
    | A* | ✅ Yes | O(E) | O(V) | Informed search |
    
    **When to use which solver:**
    - **BFS:** When you need the shortest path and have enough memory
    - **DFS:** When any path is acceptable and memory is limited
    - **A*:** When you have a good heuristic and want efficiency
    """)
