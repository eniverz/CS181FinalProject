import { createSlice } from "@reduxjs/toolkit"
import { CanvasConfig } from "@/redux/model/canvas"

const initialBoardPos: [number, number][] = [
    [0, 12],
    [1, 11],
    [1, 12],
    [2, 10],
    [2, 11],
    [2, 12],
    [3, 9],
    [3, 10],
    [3, 11],
    [3, 12],
    [4, 4],
    [4, 5],
    [4, 6],
    [4, 7],
    [4, 8],
    [4, 9],
    [4, 10],
    [4, 11],
    [4, 12],
    [4, 13],
    [4, 14],
    [4, 15],
    [4, 16],
    [5, 4],
    [5, 5],
    [5, 6],
    [5, 7],
    [5, 8],
    [5, 9],
    [5, 10],
    [5, 11],
    [5, 12],
    [5, 13],
    [5, 14],
    [5, 15],
    [6, 4],
    [6, 5],
    [6, 6],
    [6, 7],
    [6, 8],
    [6, 9],
    [6, 10],
    [6, 11],
    [6, 12],
    [6, 13],
    [6, 14],
    [7, 4],
    [7, 5],
    [7, 6],
    [7, 7],
    [7, 8],
    [7, 9],
    [7, 10],
    [7, 11],
    [7, 12],
    [7, 13],
    [8, 4],
    [8, 5],
    [8, 6],
    [8, 7],
    [8, 8],
    [8, 9],
    [8, 10],
    [8, 11],
    [8, 12],
    [9, 3],
    [9, 4],
    [9, 5],
    [9, 6],
    [9, 7],
    [9, 8],
    [9, 9],
    [9, 10],
    [9, 11],
    [9, 12],
    [10, 2],
    [10, 3],
    [10, 4],
    [10, 5],
    [10, 6],
    [10, 7],
    [10, 8],
    [10, 9],
    [10, 10],
    [10, 11],
    [10, 12],
    [11, 1],
    [11, 2],
    [11, 3],
    [11, 4],
    [11, 5],
    [11, 6],
    [11, 7],
    [11, 8],
    [11, 9],
    [11, 10],
    [11, 11],
    [11, 12],
    [12, 0],
    [12, 1],
    [12, 2],
    [12, 3],
    [12, 4],
    [12, 5],
    [12, 6],
    [12, 7],
    [12, 8],
    [12, 9],
    [12, 10],
    [12, 11],
    [12, 12],
    [13, 4],
    [13, 5],
    [13, 6],
    [13, 7],
    [14, 4],
    [14, 5],
    [14, 6],
    [15, 4],
    [15, 5],
    [16, 4]
]

const initialState: CanvasConfig = {
    board: initialBoardPos,
    width: window.innerWidth,
    height: window.innerHeight,
    dotRadius: Math.min(window.innerWidth, window.innerHeight) * 0.02,
    margin: 2.5 * Math.min(window.innerWidth, window.innerHeight) * 0.02,
    centerX: window.innerWidth / 2,
    centerY: window.innerHeight / 2,
    startX: window.innerWidth / 2 - 8 * (1 + 0.5) * 2.5 * Math.min(window.innerWidth, window.innerHeight) * 0.02,
    startY: window.innerHeight / 2 - 8 * Math.sqrt(0.75) * 2.5 * Math.min(window.innerWidth, window.innerHeight) * 0.02
}

const canvas = createSlice({
    name: "board",
    initialState,
    reducers: {
        setCanvasConfig(state: CanvasConfig, { payload }: { payload: Partial<CanvasConfig> }) {
            if (payload.width) state.width = payload.width
            if (payload.height) state.height = payload.height

            if (payload.dotRadius) state.dotRadius = payload.dotRadius
            else state.dotRadius = Math.min(state.width, state.height) * 0.02

            if (payload.margin) state.margin = payload.margin
            else state.margin = 2.5 * state.dotRadius

            if (payload.centerX) state.centerX = payload.centerX
            else state.centerX = state.width / 2

            if (payload.centerY) state.centerY = payload.centerY
            else state.centerY = state.height / 2

            if (payload.startX) state.startX = payload.startX
            else state.startX = state.centerX - 8 * (1 + 0.5) * state.margin

            if (payload.startY) state.startY = payload.startY
            else state.startY = state.centerY - 8 * Math.sqrt(0.75) * state.margin
        }
    }
})

export default canvas.reducer
export const { setCanvasConfig } = canvas.actions
