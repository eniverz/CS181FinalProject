import { createSlice } from "@reduxjs/toolkit"
import { Game } from "../model/game"

const initialState: Game = {
    state: {
        checkers: [],
        currentPlayer: null,
        selected: null,
        step: 0,
        board: []
    }
}

const game = createSlice({
    name: "game",
    initialState,
    reducers: {
        setType(state, { payload }: {payload: Game["type"]}) {
            state.type = payload
        },
        setNumPlayers(state, { payload }: {payload: Game["players"]}) {
            state.players = payload
        }
    }
})

export default game.reducer
export const { setType, setNumPlayers } = game.actions
