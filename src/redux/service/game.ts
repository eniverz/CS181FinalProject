import { createSlice } from "@reduxjs/toolkit"
import { Game } from "../model/game"

const initialState: Game = {
    state: {
        checkers: [],
        currentPlayer: null,
        step: 0
    }
}

const game = createSlice({
    name: "game",
    initialState,
    reducers: {
        setType(state, { payload }: { payload: Game["gameType"] }) {
            state.gameType = payload
        },
        setNumPlayers(state, { payload }: { payload: Game["players"] }) {
            state.players = payload
        },
        updateCurrentPlayer(state, { payload }: { payload: typeof initialState.state.currentPlayer }) {
            state.state.currentPlayer = payload
        }
    }
})

export default game.reducer
export const { setType, setNumPlayers, updateCurrentPlayer } = game.actions
