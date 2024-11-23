import { RouteObject } from "react-router"
import { lazy } from "react"

const Start = lazy(() => import("@/pages/Start"))

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
        element: <></>
    }
]
