import { RouteObject } from "react-router"
import { lazy } from "react"

const Start = lazy(() => import("@/pages/Start"))
const Game = lazy(() => import("@/pages/Game"))
const AIGame = lazy(() => import("@/pages/AIGame"))

export const routes: RouteObject[] = [
    {
        path: "/",
        element: <Start />
    },
    {
        path: "/about",
        element: <></>
    },
    {
        path: "/play",
        element: <Game />
    },
    {
        path: "/ai",
        element: <AIGame />
    }
]
