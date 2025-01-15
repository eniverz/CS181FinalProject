import { RootDispatch } from "@/redux/model"
import { CanvasConfig } from "@/redux/model/canvas"
import { Checker } from "@/redux/model/checker"
import { setCanvasConfig } from "@/redux/service/canvas"

const config = { board: new Set<string>() }

const drawDot = (ctx: CanvasRenderingContext2D, x: number, y: number, radius: number, fill = "white", stroke = "black") => {
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fillStyle = fill
    ctx.fill()
    ctx.strokeStyle = stroke
    ctx.stroke()
}

export const drawBoard = (canvas: HTMLCanvasElement, width: number, height: number, board: [number, number][], dispatch: RootDispatch, board_size: number = 4) => {
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const centerX = width / 2
    const centerY = height / 2
    const radius = Math.min(width, height) * 0.4 // Board radius as 70% of smaller dimension
    const dotRadius = Math.min(width, height) * 0.02 // Dot radius as 5% of smaller dimension

    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    // Draw outer circle
    ctx.strokeStyle = "black"
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2)
    ctx.stroke()
    const margin = 2.5 * dotRadius
    const edge = (board_size - 1) / 2
    const startX = centerX - edge * (1 + 0.5) * margin
    const startY = centerY - edge * Math.sqrt(0.75) * margin

    dispatch(setCanvasConfig({ width, height, dotRadius, margin, centerX, centerY, startX, startY }))

    // Function to draw a dot

    for (const pos of board) {
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(ctx, x, y, dotRadius)
    }
    config.board = new Set(board.map((val) => JSON.stringify(val)))
}

export const getClickedChecker = (
    canvas: HTMLCanvasElement,
    canvasConfig: CanvasConfig,
    clickEvent: React.MouseEvent<HTMLCanvasElement>
): [number, number, number, number] | [undefined, undefined, undefined, undefined] => {
    const { dotRadius, margin, startX, startY } = canvasConfig
    const rect = canvas.getBoundingClientRect()
    const x = clickEvent.clientX - rect.left
    const y = clickEvent.clientY - rect.top
    const posY = Math.floor((y - startY) / (Math.sqrt(0.75) * margin) + 0.5)
    const posX = Math.floor((x - startX) / margin - posY * 0.5 + 0.5)
    if (!config.board.has(JSON.stringify([posX, posY]))) return [undefined, undefined, undefined, undefined]
    const actX = startX + (posX + 0.5 * posY) * margin
    const actY = startY + posY * Math.sqrt(0.75) * margin
    if (Math.sqrt((x - actX) ** 2 + (y - actY) ** 2) > dotRadius) return [undefined, undefined, undefined, undefined]
    return [posX, posY, actX, actY]
}

export const drawChecker = (canvas: HTMLCanvasElement, width: number, height: number, checkers: Checker[], board_size: number = 4) => {
    const centerX = width / 2
    const centerY = height / 2
    const dotRadius = Math.min(width, height) * 0.02 // Dot radius as 5% of smaller dimension
    const margin = 2.5 * dotRadius
    const edge = (board_size - 1) / 2
    const startX = centerX - edge * (1 + 0.5) * margin
    const startY = centerY - edge * Math.sqrt(0.75) * margin

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    for (const checker of checkers) {
        const pos = checker.position
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(ctx, x, y, dotRadius, checker.color)
    }
}

export const drawPosiblePos = (canvas: HTMLCanvasElement, canvasConfig: CanvasConfig, posiblePos: [number, number][]) => {
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    const { dotRadius, margin, startX, startY } = canvasConfig
    for (const pos of posiblePos) {
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(ctx, x, y, dotRadius, "rgba(0, 0, 0, 0.5)")
    }
}

export const clearCycle = (canvas: HTMLCanvasElement, canvasConfig: CanvasConfig, position: [number, number] | [number, number][]) => {
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    const { dotRadius, margin, startX, startY } = canvasConfig
    if (typeof position[0] === "number" && typeof position[1] === "number") {
        const x = startX + (position[0] + 0.5 * position[1]) * margin
        const y = startY + position[1] * Math.sqrt(0.75) * margin
        ctx.clearRect(x - dotRadius, y - dotRadius, 2 * dotRadius, 2 * dotRadius)
        drawDot(ctx, x, y, dotRadius)
    } else {
        for (const pos of position as [number, number][]) {
            const x = startX + (pos[0] + 0.5 * pos[1]) * margin
            const y = startY + pos[1] * Math.sqrt(0.75) * margin
            ctx.clearRect(x - dotRadius, y - dotRadius, 2 * dotRadius, 2 * dotRadius)
            drawDot(ctx, x, y, dotRadius)
        }
    }
}
