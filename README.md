# Chinese Checker

## Setup

### Frontend

install [nodejs](nodejs.org), or using cli:

```bash
# ubuntu
sudo apt install npm
# arch
sudo pacman -S npm
# windows
winget install -i OpenJS.NodeJS.LTS
# mac
brew install npm
```

run command below:

```bash
npm install -g pnpm
pnpm i
pnpm dev
```

### Backend

you need install the requirements.txt

```bash
conda create -n checker python=3.10
cd server
pip install -r requirements.txt
fastapi dev main.py
```

## Frontend
use react for frontend UI

- [x] start scene
- [x] play scene
- [x] winner
- [x] single player
- [ ] multiple player
- [ ] with AI

## Backend

use fast API for service

### Connect with frontend

- [x] fastapi entry point
- [x] get board
- [x] move
- [x] is win / is loss
- [x] change player
- [ ] ai agent
- [ ] connect

### Algorithm

- [x] game: init (number of players, type of game(play with AI? AI v.s. AI?), current state, ...anything)
- [x] game: create board(all available position, all checker, which position has checker)
- [ ] game: checker(record checker position, record which player this checker belong to, get checker by position)
- [ ] game: current player(which checker could be selected) => return a list of checker
- [ ] game: which position is available for selected checker => return a list of position
- [ ] agent: reward function or evaluate function( the distance to target? )
- [ ] agent: use minmax search
- [ ] agent: use reinforcement learning
