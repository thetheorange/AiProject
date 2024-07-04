import TestApi from "@/components/TestApi.vue"
import VueRouter from "vue-router"

const router = new VueRouter({
    routes: [
        {
            path: "/test",
            component: TestApi
        }
    ]
})

export default router