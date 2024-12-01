import axios, { AxiosError } from "axios"
import { toast } from "sonner"

const request = axios.create({
    baseURL: "http://localhost:8000"
})

export type Response<T = any> = {
    msg: string
    data: T
    code: 200
}

request.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token")
        if (token) {
            config.headers.set("token", token)
        }
        return config
    },
    (err) => {
        console.error(err)
    }
)

request.interceptors.response.use(
    (res) => res.data,
    (err: AxiosError<{ detail: string }, any>) => {
        switch (err.status) {
            case 401: {
                toast.error("please login to access the resource")
                break
            }
            case 403: {
                toast.error("you have no authorization to access the resource")
                break
            }
            case 404: {
                toast.error("the resource is not found!")
                break
            }
            default: {
                toast.error(err.response?.data?.detail ?? `Error: ${err.message}`)
            }
        }
    }
)

export default request
