import requests from '@/libs/request'
import {loginUrl, userMeUrl, refreshTokenUrl, logoutUrl, userMeAccessKeyUrl, userAdminUrl, picUrl} from './urls'

export const loginApi = async (data: object): Promise<any> => {
    return await requests.post(loginUrl, data)
}

export const refreshTokenApi = async (data: object): Promise<any> => {
    return await requests.post(refreshTokenUrl, data)
}

export const logoutApi = async (data: object): Promise<any> => {
    return await requests.post(logoutUrl, data)
}

export const getUserMeApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userMeUrl , params, true)
}

export const getUserMeAccessKeyApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userMeAccessKeyUrl, params, true)
}

export const postUserMeAccessKeyApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(userMeAccessKeyUrl, data, true)
}

export const getUserAdminApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userAdminUrl, params, true)
}

export const postUserAdminApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(userAdminUrl, data, true)
}

export const deleteUserAdminApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${userAdminUrl}/${path}`
    return await requests.delete(url, data, true)
}





