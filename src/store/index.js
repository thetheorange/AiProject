import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex);

import APPInfo from "./APPInfo";
import AdminInfo from "./AdminInfo";

export default new Vuex.Store({
    modules: {
        APPInfo,
        AdminInfo
    }
})
