import {configureStore} from "@reduxjs/toolkit";
import game from "./service/game";

export const store = configureStore({
    reducer: {
        game: game
    }
})
