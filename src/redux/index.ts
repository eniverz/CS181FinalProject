import {configureStore} from "@reduxjs/toolkit";
import game from "./service/game";
import canvas from "./service/canvas";

export const store = configureStore({
    reducer: {
        game: game,
        canvas: canvas
    }
})
