# Tujo - Terminal User Journal

Tujo is a minimalist terminal-based journal and task management application built with Python. It combines the simplicity of plain text journaling with the power of terminal-based interfaces.

## Features

- **Task Management**: Create, complete, and track daily tasks
- **7-Day View**: Access and manage tasks from the past week
- **Pomodoro Timer**: Built-in 30-minute focus timer
- **Weather Integration**: Current weather display
- **Task Analytics**: Track your task completion statistics
- **Quotes**: Random Lord of the Rings quotes for motivation
- **Undo Support**: Safely undo task changes

## Requirements

- Python 3.8+
- Textual library
- Flask (for microservices)
- Node.js (for weather service)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tujo.git
   cd tujo
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies for weather service:
   ```bash
   cd src/microservices/weather
   npm install
   ```

## Running the Application

1. Start the microservices:
   ```bash
    # Start the quotes service (port 2001)
   python src/microservices/quotes/quotes.py

   # Start the analytics service (port 2002)
   python src/microservices/data/analytics.py

   # Start the timer service (port 2003)
   python src/microservices/timer/timer.py
   
   # Start the weather service (port 3724)
   cd src/microservices/weather
   node weather.js
   ```

2. Run the main application:
   ```bash
   python run.py
   ```

## Navigation

- `h`: Home screen
- `p`: Pomodoro timer
- `d`: Data analytics
- `a`: About section
- `t`: Create new task
- `x`: Complete task
- `u`: Undo last action
- `↑/k`: Move up
- `↓/j`: Move down
- `Enter`: Toggle task selection
- `^c`: Quit application
- `^p`: Command palette

## Project Structure

The application follows a modular architecture with:
- Core journal functionality in `src/journal`
- Microservices in `src/microservices`
- Screen layouts in `screens` directory
- Components for reusable UI elements
- Utility functions in `utils`
