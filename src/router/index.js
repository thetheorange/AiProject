import Login from "@/components/pages/LoginView.vue"
import ModelConsole from "@/components/pages/ModelConsole.vue"
import AppInfo from "@/components/pages/AppInfo.vue"
import NormalUserManager from "@/components/pages/NormalUserManager.vue"
import AdminUserManager from "@/components/pages/AdminUserManager.vue"
import TokenManager from "@/components/pages/TokenManager.vue"

import VueRouter from "vue-router"

const router = new VueRouter({
    routes: [
        {
            path: "/",
            redirect: "/login"
        },
        {
            path: "/Login",
            name: "Login",
            component: Login
        },
        {
            path: "/ModelConsole",
            component: ModelConsole,
            meta: {authRequire: true}
        },
        {
            path: "/AppInfo",
            component: AppInfo,
            meta: {authRequire: true}
        },
        {
            path: "/NormalUserManager",
            component: NormalUserManager,
            meta: {authRequire: true}
        },
        {
            path: "/AdminUserManager",
            component: AdminUserManager,
            meta: {authRequire: true}
        },
        {
            path: "/TokenManager",
            component: TokenManager,
            meta: {authRequire: true}
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.authRequire){
        if (localStorage.getItem("access_token")) {
            console.log(to.path);
            next();
        }
        else {
            if (from.path !== "/Login") next({name: "Login"});
        }
    }else{
        next()
    }
})

export default router