export type Board = Set<string>

export type CanvasConfig = {
    width: number
    height: number
    dotRadius: number
    margin: number
    centerX: number
    centerY: number
    startX: number
    startY: number
    board: Board
}
