# Rimaz - Interactive Detective Game

A FastAPI-based interactive detective game that combines digital clues with smart home effects, including Philips Hue lighting and audio feedback.

## 🎯 Overview

Rimaz is an immersive detective game where players solve clues to progress through a mystery. The game features:
- **Digital Clue System**: Web-based clues with voting mechanisms
- **Smart Home Integration**: Philips Hue lighting effects and audio feedback
- **Multi-Player Support**: Multiple detectives can participate simultaneously
- **Real-time Effects**: Lights and sounds trigger when clues are solved

## 🚀 Features

### Core Game Mechanics
- **Clue Management**: Create, release, and track clue progress
- **Detective System**: Player registration and progress tracking
- **Voting System**: Suspect voting after solving clues
- **Progress Tracking**: Individual detective progress per clue

### Smart Home Effects
- **Lighting Control**: Automatic light sequences for clue completion
- **Audio Feedback**: Sound effects when clues are solved
- **Effect Triggers**: Synchronized light and sound effects

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Philips Hue Bridge (for lighting effects)
- Audio output device (for sound effects)

### Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rimaz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file with your Philips Hue bridge details:
   ```env
   BRIDGE_IP=192.168.1.120
   HUE_USERNAME=your_hue_username
   ```

4. **Database Setup**
   ```bash
   # Run database migrations
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Philips Hue Setup
1. Find your bridge IP address in the Hue app
2. Generate a username using the setup script:
   ```bash
   python scripts/setup_hue_bridge_user.py
   ```
3. Update `common/constants.py` with your bridge details

### Audio Configuration
- Update `sounds/speakers.py` with your preferred audio device
- Place sound effect files in `sounds/assets/`

## 🎮 Game Flow

1. **Detective Registration**: Players register with unique codes
2. **Clue Release**: Game master releases clues to detectives
3. **Clue Solving**: Detectives attempt to solve clues with answers
4. **Progress Tracking**: System tracks individual detective progress
5. **Voting**: After solving, detectives vote on suspects
6. **Effects**: Lights and sounds trigger for completed clues

## 🚀 Development

### Running in Development
```bash
# Start with auto-reload
uvicorn main:app --reload

# Run database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Testing
```bash
# Run tests (if available)
pytest

# Manual testing
curl http://localhost:8000/
```