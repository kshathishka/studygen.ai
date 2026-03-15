# StudyGen.AI

StudyGen.AI is an interactive learning app built with Streamlit that combines AI-powered study tools with algorithm learning games.

It helps students and self-learners:
- Turn raw notes into flashcards
- Generate and answer quizzes
- Build a day-by-day 2-week study plan
- Learn core algorithms through visual and puzzle-based mini games

## Features

### AI Study Tools
- Flashcard Generator
  - Creates concise term-definition flashcards from your notes.
- Quiz Generator
  - Generates multiple-choice questions and scores your answers.
- Study Plan Generator
  - Produces a structured 14-day plan from your syllabus/topics.

### Educational Games
- River Crossing Puzzle
- Tower of Hanoi
- N-Queens Solver
- Sorting Visualizer
- Maze Generator and Solver

The Games page includes:
- Learn Mode for concept explanation and guided understanding
- Play Mode for challenge-based learning
- Progress tracking via session achievements

## Tech Stack

- Python
- Streamlit
- OpenAI Python SDK
- python-dotenv
- NumPy

## Project Structure

- home.py
- utils.py
- requirements.txt
- pages/
  - flashcards.py
  - quiz.py
  - studyplan.py
  - games.py
- game_modules/
  - river_crossing.py
  - tower_of_hanoi.py
  - n_queens.py
  - sorting_visualizer.py
  - maze_solver.py

## Prerequisites

- Python 3.9 or newer
- OpenAI API key

## Installation

1. Clone the repository and open it in your terminal.
2. Create and activate a virtual environment.
3. Install dependencies.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Set your OpenAI API key using an environment variable.

Windows PowerShell (current session):

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Optional: create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_api_key_here
```

The app loads `.env` values from `home.py` using `python-dotenv`.

## Run the App

From the project root:

```powershell
streamlit run home.py
```

Open the local URL shown by Streamlit (commonly `http://localhost:8501`).

## How to Use

1. Launch the app.
2. Choose a tool from the sidebar pages.
3. Paste your notes/topic/syllabus for AI tools, or open Games to practice algorithms.
4. Generate content and iterate with better prompts/input for improved results.

## Notes

- AI response formatting can vary, so parsing is best-effort.
- A valid OpenAI API key is required for AI features.
- Data is session-based in Streamlit; no persistent database is configured.

## Future Improvements

- Add a dedicated topic-assistant chat page.
- Add automated tests for parsing and game logic.
- Add export options for generated content (PDF/CSV/Markdown).
- Add deployment guides for Streamlit Community Cloud and Docker.
