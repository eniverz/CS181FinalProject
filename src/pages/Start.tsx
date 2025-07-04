import GlassButton from "@/components/GlassButton"
import request from "@/lib/request"
import { RootDispatch } from "@/redux/model"
import { setNumPlayers, setType } from "@/redux/service/game"
import { useRequest } from "ahooks"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router"
import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { setBoardPos, setBoardSize } from "@/redux/service/canvas"

const enum GameType {
    PLAYER_VS_PLAYER = 1,
    PLAYER_VS_AI = 2,
    AI_VS_AI = 3
}

const Selection = ({ setSelected }: { setSelected: React.Dispatch<React.SetStateAction<1 | 2 | 3 | 4 | 5 | 6>> }) => {
    return (
        <Select defaultValue="1" onValueChange={(val: string) => setSelected(parseInt(val) as 1 | 2 | 3 | 4 | 5 | 6)}>
            <SelectTrigger className="w-4/5">
                <SelectValue placeholder="AI Agent Type" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem value="1">Minmax</SelectItem>
                <SelectItem value="2">Minmax with Function Approximate</SelectItem>
                <SelectItem value="3">DVI</SelectItem>
                <SelectItem value="4">Greedy</SelectItem>
                <SelectItem value="5">Monte Carlo Tree Search</SelectItem>
            </SelectContent>
        </Select>
    )
}

export default () => {
    const navigate = useNavigate()
    const dispatch = useDispatch<RootDispatch>()
    const init = useRequest(
        async (
            player_num: number,
            game_type: GameType = GameType.PLAYER_VS_PLAYER,
            board_size: number = 3,
            agent_type = 1,
            agent2_type = 1
        ): Promise<[number, number][]> =>
            (await request.post("/game/init", null, { params: { player_num, game_type, board_size, agent_type, agent2_type } })).data,
        {
            manual: true,
            onSuccess: (data: [number, number][]) => {
                dispatch(setBoardPos(data))
            }
        }
    )
    const [open, setOpen] = useState(false)
    const [open2, setOpen2] = useState(false)
    const [open3, setOpen3] = useState(false)
    const [playerNum, setPlayerNum] = useState<2 | 3 | 6>(2)
    const [agentType, setAgentType] = useState<1 | 2 | 3 | 4 | 5 | 6>(1)
    const [agent2Type, setAgent2Type] = useState<1 | 2 | 3 | 4 | 5 | 6>(1)

    const singlePlayer = async () => {
        dispatch(setType("single"))
        dispatch(setNumPlayers(1))
        dispatch(setBoardSize(3 * 4 + 1))
        await init.runAsync(1)
        navigate("/play")
    }
    const submitMultiplePlayer = async () => {
        dispatch(setType("multi"))
        dispatch(setNumPlayers(playerNum))
        dispatch(setBoardSize(3 * 4 + 1))
        await init.runAsync(playerNum)
        navigate("/play")
    }
    const playWithAI = async () => {
        dispatch(setType("AI"))
        dispatch(setNumPlayers(2))
        dispatch(setBoardSize(3 * 4 + 1))
        await init.runAsync(2, GameType.PLAYER_VS_AI, 3, agentType)
        navigate("/ai")
    }
    const AIWithAI = async () => {
        dispatch(setType("AI vs AI"))
        dispatch(setNumPlayers(2))
        dispatch(setBoardSize(3 * 4 + 1))
        await init.runAsync(2, GameType.AI_VS_AI, 3, agentType, agent2Type)
        navigate("/ai_vs_ai")
    }

    return (
        <div className="w-screen h-screen overflow-hidden flex justify-center items-center">
            <Dialog open={open3} onOpenChange={setOpen3}>
                <DialogContent className="w-[30vw]">
                    <DialogHeader>
                        <DialogTitle>Agents Type</DialogTitle>
                        <DialogDescription>choose two agent type</DialogDescription>
                    </DialogHeader>
                    <Selection setSelected={setAgent2Type} />
                    <Selection setSelected={setAgentType} />
                    <DialogFooter>
                        <GlassButton className="text-lg w-1/6 after:bg-red-500 bg-red-500/20" onClick={() => setOpen2(false)}>
                            cancel
                        </GlassButton>
                        <GlassButton className="text-lg w-1/6 after:bg-teal-300 bg-teal-300/20" onClick={AIWithAI}>
                            submit
                        </GlassButton>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <Dialog open={open2} onOpenChange={setOpen2}>
                <DialogContent className="w-[30vw]">
                    <DialogHeader>
                        <DialogTitle>Agent Type</DialogTitle>
                        <DialogDescription>choose type of agent</DialogDescription>
                    </DialogHeader>
                    <Selection setSelected={setAgentType} />
                    <DialogFooter>
                        <GlassButton className="text-lg w-1/6 after:bg-red-500 bg-red-500/20" onClick={() => setOpen2(false)}>
                            cancel
                        </GlassButton>
                        <GlassButton className="text-lg w-1/6 after:bg-teal-300 bg-teal-300/20" onClick={playWithAI}>
                            submit
                        </GlassButton>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <Dialog open={open} onOpenChange={setOpen}>
                <DialogContent className="w-[30vw]">
                    <DialogHeader>
                        <DialogTitle>Number of Player</DialogTitle>
                        <DialogDescription>choose how many player you want to play with</DialogDescription>
                    </DialogHeader>
                    <Select defaultValue="2" onValueChange={(val: string) => setPlayerNum(parseInt(val) as 2 | 3 | 6)}>
                        <SelectTrigger className="w-4/5">
                            <SelectValue placeholder="Number of players " />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="2">2</SelectItem>
                            <SelectItem value="3">3</SelectItem>
                            <SelectItem value="6">6</SelectItem>
                        </SelectContent>
                    </Select>
                    <DialogFooter>
                        <GlassButton className="text-lg w-1/6 after:bg-red-500 bg-red-500/20" onClick={() => setOpen(false)}>
                            cancel
                        </GlassButton>
                        <GlassButton className="text-lg w-1/6 after:bg-teal-300 bg-teal-300/20" onClick={submitMultiplePlayer}>
                            submit
                        </GlassButton>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <div className="flex flex-col relative items-center h-1/2 w-1/3 bg-zinc-50/10 backdrop-blur-md rounded-xl border">
                <div className="text-center text-5xl bg-clip-text bg-gradient-to-r from-pink-300 to-violet-300 text-transparent font-extrabold mt-4">
                    Chinese Checker
                </div>
                <div className="space-y-5 flex flex-col justify-center items-center w-full h-full">
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={singlePlayer}>
                        Single Player
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={() => setOpen(true)}>
                        Multiple Player
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={() => setOpen2(true)}>
                        Play with AI
                    </GlassButton>
                    <GlassButton className="text-2xl w-2/3 after:bg-teal-100" onClick={() => setOpen3(true)}>
                        AI v.s. AI
                    </GlassButton>
                </div>
            </div>
        </div>
    )
}
