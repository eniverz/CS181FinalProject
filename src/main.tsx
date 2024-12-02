import { createRoot } from "react-dom/client"
import "./index.css"
import App from "./App.tsx"
import { Provider } from "react-redux"
import { BrowserRouter } from "react-router-dom"
import { store } from "@/redux/index.ts"
import { Suspense } from "react"
import { Loader2Icon } from "lucide-react"
import { Toaster } from "sonner"

createRoot(document.getElementById("root")!).render(
    <Provider store={store}>
        <BrowserRouter>
            <Suspense fallback={<Loader2Icon className="animate-spin" />}>
                <App />
                <Toaster visibleToasts={5} richColors closeButton position="top-right" />
            </Suspense>
        </BrowserRouter>
    </Provider>
)
