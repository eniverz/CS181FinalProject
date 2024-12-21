import classNames from "classnames"

export default ({
    className = "",
    disabled = false,
    children = <></>,
    onClick = () => {}
}: {
    className?: string
    lightColor?: string
    disabled?: boolean
    children?: React.ReactNode
    onClick?: () => void
}) => {
    const buttonClass = classNames({
        // Base styles
        ["px-2 py-1 flex justify-center items-center select-none rounded-2xl backdrop-blur-3xl"]: true,

        // Glass effect
        ["bg-cyan-600/20 backdrop-blur-xl"]: true,
        ["shadow-[inset_0_0_1px_1px_rgba(255,255,255,0.1)]"]: true,

        // Gradient overlay
        ["before:absolute before:inset-0 before:rounded-2xl"]: true,
        ["before:bg-gradient-to-b before:from-white/10 before:to-transparent"]: true,
        ["before:pointer-events-none"]: true,

        // Glow effect
        ["after:absolute after:inset-0 after:-z-10"]: true,
        ["after:bg-cyan-500/30 after:blur-2xl after:rounded-full"]: true,
        ["after:transition-all after:duration-300"]: true,

        // Hover states
        ["hover:scale-105 hover:after:blur-3xl active:scale-100 cursor-pointer"]: !disabled,
        // Disabled state
        ["opacity-50 hover:cursor-not-allowed grayscale"]: disabled,

        [className]: true
    })
    return (
        <div className={buttonClass} onClick={() => !disabled && onClick()} role="button">
            {children}
        </div>
    )
}
