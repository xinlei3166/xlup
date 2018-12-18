import Vue from 'vue'
import Vuex from 'vuex'
import routes from '@/router/routes'
import { getToken } from '@/utils/token'
import { getUserInfo, getUserAccessKey } from '@/utils/user'

Vue.use(Vuex);

export interface State {
    slideMenus: object[]
    token: object
    userInfo: object
    userAccessKey: object
}

const state: State = {
    slideMenus: routes,
    token: getToken(),
    userInfo: getUserInfo(),
    userAccessKey: getUserAccessKey()
}

const getters = {
    //
}

const mutations = {
    changeToken: (state) => {
        state.token = getToken()
    },
    changeUserInfo: (state) => {
        state.userInfo = getUserInfo()
    },
    changeUserAccessKey: (state) => {
        state.userAccessKey = getUserAccessKey()
    },
}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions: {},
});
