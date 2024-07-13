import SimpleTest from "@/components/pages/SimpleTest.vue"
import ModelConsole from "@/components/pages/ModelConsole.vue"
import AppInfo from "@/components/pages/AppInfo.vue"
import NormalUserManager from "@/components/pages/NormalUserManager.vue"
import AdminUserManager from "@/components/pages/AdminUserManager.vue"
import TokenManager from "@/components/pages/TokenManager.vue"

import VueRouter from "vue-router"

const router = new VueRouter({
    routes: [
        {
            path: "/SimpleTest",
            component: SimpleTest
        },
        {
            path: "/ModelConsole",
            component: ModelConsole,
        },
        {
            path: "/AppInfo",
            component: AppInfo,
        },
        {
            path: "/NormalUserManager",
            component: NormalUserManager,
        },
        {
            path: "/AdminUserManager",
            component: AdminUserManager,
        },
        {
            path: "/TokenManager",
            component: TokenManager
        }
    ]
})

export default router