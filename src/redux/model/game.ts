import { Board, Checker, Player } from "./checker"

export type GameState = {
    checkers: Checker[]
    currentPlayer: Player | null
    selected: Checker | null
    board: Board
    step: number
}

export type Game = {
    type?: "single" | "multi" | "AI" | "AI vs AI"
    players?: 1 | 2 | 3 | 6
    state: GameState
}
