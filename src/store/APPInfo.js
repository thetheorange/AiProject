export default {
    namespaced: true,
    state: {
        textModelToken: 1000,
        APPID: "",
        APIKEY: "",
        API_SECRET: ""
    },
    actions: {
        app_id({ commit }, payload) {
            commit("APPID", payload.app_id);
        },
        api_key({ commit }, payload) {
            commit("APIKEY", payload.api_key);
        },
        api_secret({ commit }, payload) {
            commit("API_SECRET", payload.api_secret);
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