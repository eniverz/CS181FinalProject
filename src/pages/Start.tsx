import GlassButton from "@/components/GlassButton"
import { RootDispatch } from "@/redux/model"
import { setNumPlayers, setType } from "@/redux/service/game"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router"

export default () => {
    const navigate = useNavigate()
    const dispatch = useDispatch<RootDispatch>()

    const singlePlayer = () => {
        navigate("/play")
        dispatch(setType("single"))
        dispatch(setNumPlayers(1))
    }
    const multiplePlayer = () => {
        navigate("/play")
        dispatch(setType("multi"))
        dispatch(setNumPlayers(2))
    }
    const playWithAI = () => {
        navigate("/play")
        dispatch(setType("AI"))
        dispatch(setNumPlayers(2))
    }
    const AIWithAI = () => {
        navigate("/play")
        dispatch(setType("AI vs AI"))
        dispatch(setNumPlayers(2))
    }

    return (
        <div className="w-screen h-screen overflow-hidden flex justify-center items-center">
            <div className="flex flex-col relative items-center h-1/2 w-1/3 bg-zinc-50/10 backdrop-blur-md rounded-xl border">
                <div className="text-center text-5xl bg-clip-text bg-gradient-to-r from-pink-300 to-violet-300 text-transparent font-extrabold mt-4">
                    Chinese Checker
                </div>
                <div className="space-y-5  flex flex-col justify-center items-center w-full h-full">
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
