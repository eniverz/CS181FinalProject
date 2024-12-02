export type Player = 0 | 1 | 2 | 3 | 4 | 5

export type Checker = {
    color: string
    player: Player
    position: [number, number]
}
