export default {
    namespaced: true,
    state: {
        adminName: "",
        historyTokens: 0,
        historyRequestTimes: 0,
    },
    actions: {

    },
    mutations: {
        ADMIN_NAME(state, value) {
            state.adminName = value;
        }
    }
}