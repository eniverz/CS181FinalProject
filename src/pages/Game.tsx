import { drawBoard } from "@/libs/draw"
import request from "@/libs/request"
import { useRequest } from "ahooks"
import { useEffect, useRef, useCallback, useState } from "react"

export default () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const [board, setBoard] = useState<[number, number][]>([])

    useRequest(async () => (await request.get("/board/all_position")).data as [number, number][], {
        onSuccess: (data) => setBoard(data),
        onError: (err) => console.error(err)
    })

    // Function to draw the board
    const memeDrawBorad = useCallback(drawBoard, [])

    // Adjust canvas size and redraw on window resize
    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const resizeCanvas = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
            memeDrawBorad(canvas, canvas.width, canvas.height, board, [])
        }
        // Initial resize
        resizeCanvas()
        // Add event listener
        window.addEventListener("resize", resizeCanvas)
        // Cleanup listener on unmount
        return () => window.removeEventListener("resize", resizeCanvas)
    }, [memeDrawBorad, board])

    return (
        <div className="w-full h-screen flex justify-center items-center bg-transparent">
            <canvas ref={canvasRef} />
        </div>
    )
}
