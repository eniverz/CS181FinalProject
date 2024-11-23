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
        ["px-2 py-1 flex justify-center items-center select-none rounded-2xl backdrop-blur-3xl duration-200"]: true,
        ["bg-[radial-gradient(66.92%_66.92%_at_50.23%_50.77%,#d3d3d300_0,#d3d3d300_40.67%,hsla(0,0%,83%,.143)_75.17%,hsla(0,0%,83%,.315)_100%)]"]: !disabled,
        ["after:content-normal after:absolute after:left-1/2 after:top-1/2 after:blur-[30px] after:w-full after:h-2/3"]: !disabled,
        ["after:-translate-x-1/2 after:-translate-y-1/2 after:h-1/2 after:rounded-full after:transition-all after:duration-200 after:z-[-1]"]: !disabled,
        ["hover:cursor-pointer hover:scale-110"]: !disabled,
        ["hover:cursor-not-allowed grayscale opacity-60"]: disabled,
        [className]: true
    })
    const handleClick = () => {
        if (!disabled) onClick()
    }
    return (
        <div className={buttonClass} onClick={handleClick}>
            {children}
        </div>
    )
}
