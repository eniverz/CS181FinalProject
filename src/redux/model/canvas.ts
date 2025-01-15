export type Board = [number, number][]

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
    board_size: number
}
