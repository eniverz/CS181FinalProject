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
    const handleClick = useCallback((event: React.MouseEvent<HTMLCanvasElement>) => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext("2d")
        if (!ctx) return
        const rect = canvas.getBoundingClientRect()
        const x = event.clientX - rect.left
        const y = event.clientY - rect.top
        const width = canvas.width
        const height = canvas.height
        const margin = 2.5 * 0.02 * Math.min(width, height)
        const startX = width / 2 - 8 * (1 + 0.5) * margin
        const startY = height / 2 - 8 * Math.sqrt(0.75) * margin
        const posY = Math.floor((y - startY) / (Math.sqrt(0.75) * margin) + 0.5)
        const posX = Math.floor((x - startX) / margin - posY * 0.5 + 0.5)
        console.log(posX, posY)
        ctx.beginPath()
        ctx.arc(startX + (posX + 0.5 * posY) * margin, startY + posY * Math.sqrt(0.75) * margin, 0.02 * Math.min(width, height), 0, Math.PI * 2)
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
            <canvas ref={canvasRef} onClick={handleClick} />
        </div>
    )
}
