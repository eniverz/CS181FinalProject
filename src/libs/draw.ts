export const drawBoard = (canvas: HTMLCanvasElement, width: number, height: number, board: [number, number][], checkers: [number, number][]) => {
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
    const drawDot = (x: number, y: number) => {
        ctx.beginPath()
        ctx.arc(x, y, dotRadius, 0, Math.PI * 2)
        ctx.fillStyle = "white"
        ctx.fill()
        ctx.strokeStyle = "black"
        ctx.stroke()
    }

    for (const pos of board) {
        const x = startX + (pos[0] + 0.5 * pos[1]) * margin
        const y = startY + pos[1] * Math.sqrt(0.75) * margin
        drawDot(x, y)
    }
}
