import { clearCycle, drawBoard, drawChecker, drawPosiblePos, getClickedChecker } from "@/libs/draw"
import request, { Response } from "@/libs/request"
import { RootDispatch, RootState } from "@/redux/model"
import { Checker, Player } from "@/redux/model/checker"
import { useRequest } from "ahooks"
import { useEffect, useRef, useCallback, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { useImmer } from "use-immer"

export default () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const [checkers, setCheckers] = useImmer<Checker[]>([])
    const [selectedChecker, setSelectedChecker] = useState<Checker | null>(null)
    const [availablePos, setAvailablePos] = useState<[number, number][]>([])
    const canvasConfig = useSelector((state: RootState) => state.canvas)
    const gameState = useSelector((state: RootState) => state.game)
    const dispatch = useDispatch<RootDispatch>()

    const getCheckers = useRequest(async () => (await request.get(`/checker/all_position/${gameState.players ?? 1}`)).data as [number, number, Player][], {
        manual: true,
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
    const getAvailablePos = useRequest(
        async (x: number, y: number) => (await request.get(`/checker/available_pos`, { params: { x, y } })) as Response<[number, number][]>,
        {
            manual: true,
            onError: (err) => console.error(err)
        }
    )
    const move = useRequest(
        async (start: [number, number], end: [number, number], player_id: number) =>
            await request.post("/checker/move", null, { params: { start_x: start[0], start_y: start[1], end_x: end[0], end_y: end[1], player_id } }),
        {
            manual: true,
            onError: (err) => console.error(err)
        }
    )

    // Function to draw the board
    const memeDrawBorad = useCallback(drawBoard, [])
    const memeDrawChecker = useCallback(drawChecker, [])
    const memeClearCycle = useCallback(clearCycle, [])

    const handleClick = useCallback(
        async (event: React.MouseEvent<HTMLCanvasElement>) => {
            const canvas = canvasRef.current
            if (!canvas) return
            const ctx = canvas.getContext("2d")
            if (!ctx) return
            const [posX, posY, actX, actY] = getClickedChecker(canvas, canvasConfig, event)
            if (posX === undefined || posY === undefined || actX === undefined || actY === undefined) return
            if (selectedChecker) {
                // already select
                if (availablePos.some(([x, y]) => x === posX && y === posY)) {
                    // move
                    memeClearCycle(canvas, canvasConfig, selectedChecker.position)
                    setCheckers((checkers) => {
                        const index = checkers.findIndex(
                            (checker) => checker.position[0] === selectedChecker.position[0] && checker.position[1] === selectedChecker.position[1]
                        )
                        checkers[index].position = [posX, posY]
                        memeDrawChecker(canvas, canvas.width, canvas.height, [checkers[index]])
                    })
                    move.runAsync(selectedChecker.position, [posX, posY], selectedChecker.player)
                }
                // clear
                memeClearCycle(canvas, canvasConfig, availablePos)
                setAvailablePos([])
                setSelectedChecker(null)
            } else {
                // need select
                const res = await getAvailablePos.runAsync(posX, posY)
                if (!res) return
                setAvailablePos(res.data)
                drawPosiblePos(canvas, canvasConfig, res.data)
                setSelectedChecker(checkers.find((checker) => checker.position[0] === posX && checker.position[1] === posY) || null)
            }
        },
        [availablePos, selectedChecker, checkers]
    )

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
        getCheckers.runAsync().then((res) => {
            memeDrawChecker(
                canvas,
                canvas.width,
                canvas.height,
                res.map(([x, y, player]) => ({
                    color: ["red", "blue", "green", "yellow", "purple", "orange"][player],
                    player,
                    position: [x, y]
                }))
            )
        })
        const draw = () => memeDrawChecker(canvas, canvas.width, canvas.height, checkers)
        window.addEventListener("resize", draw)
        return () => window.removeEventListener("resize", draw)
    }, [])

    return (
        <div className="w-full h-screen flex justify-center items-center bg-transparent">
            <canvas ref={canvasRef} onClick={handleClick} />
        </div>
    )
}
