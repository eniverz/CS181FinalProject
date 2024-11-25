# Chinese Checker

## Frontend
use react for frontend UI

- [x] start scene
- [ ] play scene
- [ ] single player
- [ ] multiple player
- [ ] with AI

## Backend

use fast API for service

### Connect with frontend

- [x] fastapi entry point
- [ ] connect

### Algorithm

- [ ] game: init (number of players, type of game(play with AI? AI v.s. AI?), current state, ...anything)
- [ ] game: create board(all available position, all checker, which position has checker)
- [ ] game: checker(record checker position, record which player this checker belong to, get checker by position)
- [ ] game: current player(which checker could be selected) => return a list of checker
- [ ] game: which position is available for selected checker => return a list of position
- [ ] agent: reward function or evaluate function( the distance to target? )
- [ ] agent: use minmax search
- [ ] agent: use reinforcement learning
