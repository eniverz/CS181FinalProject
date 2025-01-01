import { ThemeProvider } from "@/components/ThemeProvider"
import { matchRoutes, useLocation, useRoutes, useNavigate } from "react-router"
import { routes } from "@/routes"
import { useEffect } from "react"
import { useSelector } from "react-redux"
import { RootState } from "./redux/model"

export default () => {
    const { pathname } = useLocation()
    const navigate = useNavigate()
    const game = useSelector((state: RootState) => state.game)

    useEffect(() => {
        const matched = matchRoutes(routes, pathname)
        if (!matched) {
            return
        }
        matched.map((item) => {
            const path = item.route.path
            if ((path === "/play" || path === "/ai") && !game.gameType) navigate("/")
        })
    }, [pathname])
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <div className="w-screen h-screen bg-[url(/bg.jpg)] bg-no-repeat bg-cover">{useRoutes(routes)}</div>
        </ThemeProvider>
    )
}
