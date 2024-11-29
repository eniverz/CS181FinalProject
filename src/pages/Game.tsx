import { drawBoard, drawChecker } from "@/libs/draw"
import request from "@/libs/request"
import { Checker, Player } from "@/redux/model/checker"
import { useRequest } from "ahooks"
import { useEffect, useRef, useCallback, useState } from "react"
import { useImmer } from "use-immer"

export default () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const [board, setBoard] = useState<[number, number][]>([])
    const [checkers, setCheckers] = useState<Checker[]>([])

    useRequest(async () => (await request.get("/board/all_position")).data as [number, number][], {
        onSuccess: (data) => setBoard(data),
        onError: (err) => console.error(err)
    })
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

    // Adjust canvas size and redraw on window resize
    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const resizeCanvas = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
            memeDrawBorad(canvas, canvas.width, canvas.height, board)
        }
        // Initial resize
        resizeCanvas()
        // Add event listener
        window.addEventListener("resize", resizeCanvas)
        // Cleanup listener on unmount
        return () => window.removeEventListener("resize", resizeCanvas)
    }, [memeDrawBorad, board])

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
            <canvas ref={canvasRef} />
        </div>
    )
}
