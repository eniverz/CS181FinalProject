import tailwindAnimate from "tailwindcss-animate"
import tailwindScrollbar from "tailwind-scrollbar-hide"

/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
    theme: {
        extend: {}
    },
    plugins: [tailwindAnimate, tailwindScrollbar]
}
