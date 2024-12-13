# Tujo - Terminal User Journal (WIP)

Tujo is a minimalist terminal-based journal and task management application built with Python. It combines the simplicity of plain text journaling with the power of terminal-based interfaces.

## Demo

[Demo](https://github.com/user-attachments/assets/c197c4f1-8c0e-453f-87cf-8a971d145f92)

## Features

- **Task Management**: Create, complete, and track daily tasks
- **7-Day View**: Access and manage tasks from the past week
- **Pomodoro Timer**: Built-in 30-minute focus timer
- **Weather Integration**: Current weather display (code provided by another student)
- **Task Analytics**: Track your task completion statistics
- **Quotes**: Random Lord of the Rings quotes for motivation
- **Undo Support**: Safely undo task changes

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
