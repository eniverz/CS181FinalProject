import GlassButton from "@/components/GlassButton"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { clearCycle, drawBoard, drawChecker, drawPosiblePos, getClickedChecker } from "@/lib/draw"
import request, { Response } from "@/lib/request"
import { RootDispatch, RootState } from "@/redux/model"
import { Checker, Player } from "@/redux/model/checker"
import { replay, updateCurrentPlayer } from "@/redux/service/game"
import { useRequest } from "ahooks"
import { useEffect, useRef, useCallback, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router"
import { toast } from "sonner"
import { useImmer } from "use-immer"

export default () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null)
    const [checkers, setCheckers] = useImmer<Checker[]>([])
    const [selectedChecker, setSelectedChecker] = useState<Checker | null>(null)
    const [availablePos, setAvailablePos] = useState<[number, number][]>([])
    const [winner, setWinner] = useState<Player | undefined>(undefined)
    const canvasConfig = useSelector((state: RootState) => state.canvas)
    const gameState = useSelector((state: RootState) => state.game)

    const dispatch = useDispatch<RootDispatch>()
    const navigate = useNavigate()

    const init = useRequest(async (player_num: number) => await request.post("/game/init", null, { params: { player_num } }), { manual: true })
    const getCheckers = useRequest(async () => (await request.get(`/checker/all_position/${gameState.players ?? 1}`)) as Response<[number, number, Player][]>, {
        manual: true,
        onSuccess: (data) => {
            for (const [x, y, player] of data.data) {
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
        async (start: [number, number], end: [number, number]) =>
            (await request.post("/checker/move", null, { params: { start_x: start[0], start_y: start[1], end_x: end[0], end_y: end[1] } })).data,
        {
            manual: true,
            onError: (err) => console.error(err),
            onSuccess: (data: { playerID: Player; isWin: boolean }) => {
                dispatch(updateCurrentPlayer(data.playerID))
                setWinner((prev) => (data.isWin ? (((data.playerID - 1) % (gameState.players ?? 1)) as Player) : prev))
                if (!data.isWin) agentMove.run()
            }
        }
    )
    const agentMove = useRequest(
        async (): Promise<{ movement: [[number, number], [number, number]]; isWin: boolean }> => (await request.get("/agent/move")).data,
        {
            manual: true,
            onSuccess: (data: { movement: [[number, number], [number, number]]; isWin: boolean }) => {
                const startPos = data.movement[0]
                const endPos = data.movement[1]
                const pid = gameState.state.currentPlayer
                const canvas = canvasRef.current
                if (!canvas || !pid) return
                const checker: Checker = { position: endPos, player: pid, color: ["red", "blue", "green", "yellow", "purple", "orange"][pid] }
                memeClearCycle(canvas, canvasConfig, startPos)
                memeDrawChecker(canvas, canvasConfig.width, canvasConfig.height, [checker])
                setWinner((prev) => (data.isWin ? (1 as Player) : prev))
            }
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
                    move.runAsync(selectedChecker.position, [posX, posY])
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

    const restart = useCallback(async () => {
        dispatch(replay())
        setCheckers([])
        setWinner(undefined)
        await init.runAsync(gameState.players ?? 1)
        const checkers = await getCheckers.runAsync()
        if (!canvasRef.current) {
            toast.error("Canvas not found")
            navigate("/")
            return
        }
        memeDrawBorad(canvasRef.current, canvasConfig.width, canvasConfig.height, canvasConfig.board, dispatch)
        memeDrawChecker(
            canvasRef.current,
            canvasConfig.width,
            canvasConfig.height,
            checkers.data.map(([x, y, player]) => ({ color: ["red", "blue", "green", "yellow", "purple", "orange"][player], player, position: [x, y] }))
        )
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
        getCheckers.runAsync().then((res) => {
            memeDrawChecker(
                canvas,
                canvas.width,
                canvas.height,
                res.data.map(([x, y, player]) => ({
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
            <Dialog open={winner !== undefined}>
                <DialogContent showClose={false}>
                    <DialogHeader>
                        <DialogTitle>Player {gameState.state.currentPlayer} win!</DialogTitle>
                        <DialogDescription></DialogDescription>
                    </DialogHeader>
                    <div className="flex justify-center">Do you want to play again?</div>
                    <DialogFooter className="sm:flex-row sm:justify-center sm:items-center sm:space-x-8">
                        <GlassButton className="bg-teal-300/20 after:bg-teal-300" onClick={() => restart()}>
                            Re-play
                        </GlassButton>
                        <GlassButton className="bg-pink-100/20 after:bg-pink-500/70" onClick={() => window.location.reload()}>
                            Back to Menu
                        </GlassButton>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <canvas ref={canvasRef} onClick={handleClick} />
        </div>
    )
}
