import streamlit as st

st.set_page_config(page_title="Educational Games - StudyGen.AI", page_icon="🎮", layout="wide")

st.title("🎮 Educational Algorithm Games")
st.markdown("Learn algorithms through interactive puzzles and visualizations!")

# Game selection
game_options = {
    "🚣 River Crossing Puzzle": "river_crossing",
    "🗼 Tower of Hanoi": "tower_of_hanoi",
    "👑 N-Queens Solver": "n_queens",
    "📊 Sorting Visualizer": "sorting",
    "🌀 Maze Generator & Solver": "maze"
}

# Sidebar for game selection and mode
st.sidebar.header("🎯 Game Selection")
selected_game = st.sidebar.radio("Choose a Game:", list(game_options.keys()))

st.sidebar.markdown("---")
mode = st.sidebar.toggle("🎓 Learn Mode", value=True)
if mode:
    st.sidebar.info("Learn Mode: See algorithm explanations and pseudocode")
else:
    st.sidebar.info("Play Mode: Challenge yourself!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Progress")
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

achievements_count = len(st.session_state.achievements)
st.sidebar.metric("Achievements", f"{achievements_count}/15")

# Route to selected game
game_key = game_options[selected_game]

if game_key == "river_crossing":
    from game_modules.river_crossing import render_river_crossing
    render_river_crossing(learn_mode=mode)
elif game_key == "tower_of_hanoi":
    from game_modules.tower_of_hanoi import render_tower_of_hanoi
    render_tower_of_hanoi(learn_mode=mode)
elif game_key == "n_queens":
    from game_modules.n_queens import render_n_queens
    render_n_queens(learn_mode=mode)
elif game_key == "sorting":
    from game_modules.sorting_visualizer import render_sorting_visualizer
    render_sorting_visualizer(learn_mode=mode)
elif game_key == "maze":
    from game_modules.maze_solver import render_maze_solver
    render_maze_solver(learn_mode=mode)
