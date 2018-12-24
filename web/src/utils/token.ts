import Store from '@/store'
import { refreshTokenApi } from '@/api/user'

export const getToken = (): object => {
    const token = localStorage.getItem('token')
    return JSON.parse(token === null ? '{}' : token)
}

export const setToken = (token: object): void => {
    localStorage.setItem('token', JSON.stringify(token))
    Store.commit('changeToken')
}

export const refreshToken = async (): Promise<any> => {
    const data = {refresh_token: (Store.state.token as any).refresh_token}
    const ret = await refreshTokenApi(data)
    if (ret && ret.code === 'Success') {
        const token = getToken()
        token['access_token'] = ret.data.access_token
        setToken(token)
        return true
    }
}


