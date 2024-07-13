export default {
    namespaced: true,
    state: {
        textModelToken: 1000,
        APPID: "",
        APIKEY: "",
        API_SECRET: ""
    },
    actions: {
        app_id({ commit }) {
            console.log(1111)
            commit("APPID", "60361ac3");
        },
        api_key({ commit }) {
            commit("APIKEY", "7f8ff2dba8d566abb46791589ba9fed7");
        },
        api_secret({ commit }) {
            commit("API_SECRET", "NTM1ZGY3MjM0ODQxMDBhY2NjMDIyM2E5");
        }
    },
    mutations: {
        APPID(state, value) {
            state.APPID = value;
        },
        APIKEY(state, value) {
            state.APIKEY = value;
        },
        API_SECRET(state, value) {
            state.API_SECRET = value;
        },
    }
}