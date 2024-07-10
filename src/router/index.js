import SimpleTest from "@/components/pages/SimpleTest.vue"
import ModelConsole from "@/components/pages/ModelConsole.vue"
import BlackList from "@/components/pages/BlackList.vue"
import UserManager from "@/components/pages/UserManager.vue"

import VueRouter from "vue-router"

const router = new VueRouter({
    routes: [
        {
            path: "/simpleTest",
            component: SimpleTest
        },
        {
            path: "/ModelConsole",
            component: ModelConsole,
        },
        {
            path: "/BlackList",
            component: BlackList,
        },
        {
            path: "/UserManager",
            component: UserManager,
        }
    ]
})

export default router