# 🦖 Dino Game

A Python-based dinosaur running game inspired by Chrome's offline T-Rex game, developed to practice Python programming skills and explore machine learning concepts.

![Game Screenshot](.github/assets/game.png)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Pygame library

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dino.git
cd dino
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎮 Run Methods

### Play Mode

```bash
python main.py play
```

- Single dinosaur with keyboard controls
- Use Space/Up/Down arrows to control

### Training Mode

```bash
python main.py train
```

- Multiple dinosaurs with random AI behavior
- Collects training data for machine learning

### Auto Mode

```bash
python main.py auto
```

- Multiple dinosaurs with trained AI model
- Uses the last trained model for intelligent gameplay

## 🎯 How to Play

### Controls

- **Space/Up Arrow**: Jump
- **Down Arrow**: Duck (when falling)

### Objective

- Avoid obstacles (trees) by jumping over them
- Survive as long as possible to achieve high scores
- Top 5 scores are displayed in real-time
