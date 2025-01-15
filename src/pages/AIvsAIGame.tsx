import GlassButton from "@/components/GlassButton"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { clearCycle, drawBoard, drawChecker } from "@/lib/draw"
import request, { Response } from "@/lib/request"
import { RootDispatch, RootState } from "@/redux/model"
import { Checker, Player } from "@/redux/model/checker"
import { setBoardPos } from "@/redux/service/canvas"
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
    const [winner, setWinner] = useState<Player | undefined>(undefined)
    const canvasConfig = useSelector((state: RootState) => state.canvas)
    const gameState = useSelector((state: RootState) => state.game)

    const dispatch = useDispatch<RootDispatch>()
    const navigate = useNavigate()

    const init = useRequest(async (player_num: number) => (await request.post("/game/init", null, { params: { player_num, board_size: 3 } })).data, {
        manual: true,
        onSuccess: (data: [number, number][]) => {
            dispatch(setBoardPos(data))
        }
    })
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
        }
    })
    const agent2Move = useRequest(
        async (): Promise<{ movement: [[number, number], [number, number]]; isWin: boolean }> => (await request.get("/agent2/move")).data,
        {
            manual: true,
            onSuccess: (data: { movement: [[number, number], [number, number]]; isWin: boolean }) => {
                const startPos = data.movement[0]
                const endPos = data.movement[1]
                const canvas = canvasRef.current
                if (!canvas) return
                const checker: Checker = { position: endPos, player: 1, color: ["red", "blue", "green", "yellow", "purple", "orange"][1] }
                memeClearCycle(canvas, canvasConfig, startPos)
                memeDrawChecker(canvas, canvasConfig.width, canvasConfig.height, [checker], canvasConfig.board_size)
                setWinner((prev) => (data.isWin ? (0 as Player) : prev))
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
                const canvas = canvasRef.current
                if (!canvas) return
                const checker: Checker = { position: endPos, player: 0, color: ["red", "blue", "green", "yellow", "purple", "orange"][0] }
                memeClearCycle(canvas, canvasConfig, startPos)
                memeDrawChecker(canvas, canvasConfig.width, canvasConfig.height, [checker], canvasConfig.board_size)
                setWinner((prev) => (data.isWin ? (1 as Player) : prev))
            }
        }
    )

    // Function to draw the board
    const memeDrawBorad = useCallback(drawBoard, [])
    const memeDrawChecker = useCallback(drawChecker, [])
    const memeClearCycle = useCallback(clearCycle, [])

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
        memeDrawBorad(canvasRef.current, canvasConfig.width, canvasConfig.height, canvasConfig.board, dispatch, canvasConfig.board_size)
        memeDrawChecker(
            canvasRef.current,
            canvasConfig.width,
            canvasConfig.height,
            checkers.data.map(([x, y, player]) => ({ color: ["red", "blue", "green", "yellow", "purple", "orange"][player], player, position: [x, y] })),
            canvasConfig.board_size
        )
    }, [])

    // Adjust canvas size and redraw on window resize
    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const resizeCanvas = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
            memeDrawBorad(canvas, canvas.width, canvas.height, canvasConfig.board, dispatch, canvasConfig.board_size)
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
                })),
                canvasConfig.board_size
            )
        })
        const draw = () => memeDrawChecker(canvas, canvas.width, canvas.height, checkers, canvasConfig.board_size)
        window.addEventListener("resize", draw)
        return () => window.removeEventListener("resize", draw)
    }, [])

    return (
        <div className="w-full h-screen flex justify-center items-center bg-transparent">
            <GlassButton
                onClick={() => {
                    if (gameState.state.currentPlayer === 1 || gameState.state.currentPlayer === undefined) {
                        agent2Move.run()
                        dispatch(updateCurrentPlayer(0))
                    } else {
                        agentMove.run()
                        dispatch(updateCurrentPlayer(1))
                    }
                }}
                className="absolute top-20 right-20 bg-emerald-500/20  after:bg-emerald-500"
                disabled={agent2Move.loading || agentMove.loading}
            >
                Next Player: {gameState.state.currentPlayer ?? 0}
            </GlassButton>
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
            <canvas ref={canvasRef} />
        </div>
    )
}
