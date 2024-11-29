import { Checker } from "@/redux/model/checker"

const drawDot = (ctx: CanvasRenderingContext2D, x: number, y: number, radius: number, fill = "white", stroke = "black") => {
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fillStyle = fill
    ctx.fill()
    ctx.strokeStyle = stroke
    ctx.stroke()
}

export const drawBoard = (canvas: HTMLCanvasElement, width: number, height: number, board: [number, number][]) => {
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
    const startX = centerX - 8 * (1 + 0.5) * margin
    const startY = centerY - 8 * Math.sqrt(0.75) * margin

    // Function to draw a dot

    for (const pos of board) {
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(ctx, x, y, dotRadius)
    }
}

export const getClickedChecker = (canvas: HTMLCanvasElement, width: number, height: number, clickEvent: React.MouseEvent<HTMLCanvasElement>) => {}

export const drawChecker = (canvas: HTMLCanvasElement, width: number, height: number, checkers: Checker[]) => {
    const centerX = width / 2
    const centerY = height / 2
    const dotRadius = Math.min(width, height) * 0.02 // Dot radius as 5% of smaller dimension
    const margin = 2.5 * dotRadius
    const startX = centerX - 8 * (1 + 0.5) * margin
    const startY = centerY - 8 * Math.sqrt(0.75) * margin

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    for (const checker of checkers) {
        const pos = checker.position
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(ctx, x, y, dotRadius, checker.color)
    }
}
