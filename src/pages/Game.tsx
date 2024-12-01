import { drawBoard, drawChecker, getClickedChecker } from "@/libs/draw"
import request from "@/libs/request"
import { RootDispatch, RootState } from "@/redux/model"
import { Checker, Player } from "@/redux/model/checker"
import { useRequest } from "ahooks"
import { useEffect, useRef, useCallback, useState } from "react"
import { useDispatch, useSelector } from "react-redux"

export default () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const [checkers, setCheckers] = useState<Checker[]>([])
    const canvasConfig = useSelector((state: RootState) => state.canvas)
    const dispatch = useDispatch<RootDispatch>()

    useRequest(async () => (await request.get(`/checker/all_position/${6}`)).data as [number, number, Player][], {
        onSuccess: (data) => {
            for (const [x, y, player] of data) {
                const checker: Checker = {
                    color: ["red", "blue", "green", "yellow", "purple", "orange"][player],
                    player,
                    position: [x, y]
                }
                setCheckers((checkers) => [...checkers, checker])
            }
        },
        onError: (err) => console.error(err)
    })

    // Function to draw the board
    const memeDrawBorad = useCallback(drawBoard, [])
    const memeDrawChecker = useCallback(drawChecker, [])
    const handleClick = useCallback((event: React.MouseEvent<HTMLCanvasElement>) => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext("2d")
        if (!ctx) return
        const [posX, posY, actX, actY] = getClickedChecker(canvas, canvasConfig, event)
        if (posX === undefined || posY === undefined || actX === undefined || actY === undefined) return
        ctx.beginPath()
        ctx.arc(actX, actY, canvasConfig.dotRadius, 0, Math.PI * 2)
        ctx.fillStyle = "black"
        ctx.fill()
    }, [])

    // Adjust canvas size and redraw on window resize
    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const resizeCanvas = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
            memeDrawBorad(canvas, canvas.width, canvas.height, canvasConfig.board, dispatch)
        }
        // Initial resize
        resizeCanvas()
        // Add event listener
        window.addEventListener("resize", resizeCanvas)
        // Cleanup listener on unmount
        return () => window.removeEventListener("resize", resizeCanvas)
    }, [memeDrawBorad])

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const draw = () => memeDrawChecker(canvas, canvas.width, canvas.height, checkers)
        draw()
        window.addEventListener("resize", draw)
        return () => window.removeEventListener("resize", draw)
    })

    return (
        <div className="w-full h-screen flex justify-center items-center bg-transparent">
            <canvas ref={canvasRef} onClick={handleClick} />
        </div>
    )
}
