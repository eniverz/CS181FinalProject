import GlassButton from "@/components/GlassButton"
import request from "@/libs/request"
import { RootDispatch } from "@/redux/model"
import { setNumPlayers, setType } from "@/redux/service/game"
import { useRequest } from "ahooks"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router"
import { useState } from "react"

export default () => {
    const navigate = useNavigate()
    const dispatch = useDispatch<RootDispatch>()
    const { runAsync } = useRequest(async (player_num: number) => await request.post("/game/init", null, { params: { player_num } }), { manual: true })
    const [open, setOpen] = useState(false)
    const [playerNum, setPlayerNum] = useState<2 | 3 | 6>(2)

    const singlePlayer = async () => {
        dispatch(setType("single"))
        dispatch(setNumPlayers(1))
        await runAsync(1)
        navigate("/play")
    }
    const multiplePlayer = async () => {
        setOpen(true)
    }
    const submitMultiplePlayer = async () => {
        dispatch(setType("multi"))
        dispatch(setNumPlayers(playerNum))
        await runAsync(playerNum)
        navigate("/play")
    }
    const playWithAI = async () => {
        dispatch(setType("AI"))
        dispatch(setNumPlayers(2))
        await runAsync(2)
        navigate("/play")
    }
    const AIWithAI = async () => {
        dispatch(setType("AI vs AI"))
        dispatch(setNumPlayers(2))
        await runAsync(2)
        navigate("/play")
    }

    const handleDialogKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
        if (event.key === "Escape") setOpen(false)
    }
    const handleClickOuter = (event: React.MouseEvent<HTMLDivElement>) => {
        if (event.target === event.currentTarget) setOpen(false)
    }

    return (
        <div className="w-screen h-screen overflow-hidden flex justify-center items-center">
            {open ? (
                <div
                    className="fixed w-screen h-screen top-0 left-0 flex flex-col justify-center items-center z-10 bg-black/10 backdrop-blur-md"
                    onKeyDown={handleDialogKeyDown}
                    tabIndex={0}
                    onMouseDown={handleClickOuter}
                >
                    <div className="h-1/3 w-2/5 bg-zinc-400 rounded-xl shadow-2xl p-5 flex flex-col">
                        <div className="text-center text-4xl font-extrabold">Number of Player</div>
                        <div className="flex items-center w-full border-t border-dashed my-2 border-zinc-700" />
                        <div className="flex-1 flex flex-col">
                            <div className="flex mt-5">
                                <div>Player Number: </div>
                                <select className="flex-1" value={playerNum} onChange={(e) => setPlayerNum(parseInt(e.target.value) as 2 | 3 | 6)}>
                                    <option value={2}>2</option>
                                    <option value={3}>3</option>
                                    <option value={6}>6</option>
                                </select>
                            </div>
                            <div className="flex-1" />
                            <div className="flex-1 flex">
                                <div className="flex-1" />
                                <GlassButton className="text-lg w-1/6 after:bg-red-500" onClick={() => setOpen(false)}>
                                    cancel
                                </GlassButton>
                                <GlassButton className="text-lg w-1/6 after:bg-teal-300" onClick={submitMultiplePlayer}>submit</GlassButton>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <></>
            )}
            <div className="flex flex-col relative items-center h-1/2 w-1/3 bg-zinc-50/10 backdrop-blur-md rounded-xl border">
                <div className="text-center text-5xl bg-clip-text bg-gradient-to-r from-pink-300 to-violet-300 text-transparent font-extrabold mt-4">
                    Chinese Checker
                </div>
                <div className="space-y-5 flex flex-col justify-center items-center w-full h-full">
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={singlePlayer}>
                        Single Player
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={multiplePlayer}>
                        Multiple Player
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={playWithAI}>
                        Play with AI
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={AIWithAI}>
                        AI v.s. AI
                    </GlassButton>
                </div>
            </div>
        </div>
    )
}
