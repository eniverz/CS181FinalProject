import axios from "axios"

const request = axios.create({
    baseURL: "http://localhost:8000"
})

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
    (res) => {
        return res.data
    },
    (err) => {
        switch (err.response.status) {
            case 401: {
                console.error("please login to access the resource", err)
                break
            }
            case 403: {
                console.error("you have no authorization to access the resource", err)
                break
            }
            case 404: {
                console.error("the resource is not found!", err)
                break
            }
            default: {
                console.error(err)
            }
        }
    }
)

export default request
