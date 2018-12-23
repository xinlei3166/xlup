import requests from '@/libs/request'
import qs from 'qs'
import {loginUrl, userMeUrl, refreshTokenUrl, logoutUrl, userMeHeadimgUrl, userMePasswordUrl, userMeAccessKeyUrl, userMeUploadPolicyUrl, userAdminUrl, picUrl} from './urls'

export const loginApi = async (data: object): Promise<any> => {
    return await requests.post(loginUrl, qs.stringify(data))
}

export const refreshTokenApi = async (data: object): Promise<any> => {
    return await requests.post(refreshTokenUrl, qs.stringify(data))
}

export const logoutApi = async (data: object): Promise<any> => {
    return await requests.post(logoutUrl, qs.stringify(data))
}

export const getUserMeApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userMeUrl , params, true)
}

export const patchUserMeApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.patch(userMeUrl, qs.stringify(data), true)
}

export const putUserMePasswordApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.put(userMePasswordUrl, qs.stringify(data), true)
}

export const postUserMeHeadimgApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(userMeHeadimgUrl, data, true)
}

export const getUserMeAccessKeyApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userMeAccessKeyUrl, params, true)
}

export const postUserMeAccessKeyApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(userMeAccessKeyUrl, qs.stringify(data), true)
}

export const getUploadPolicy = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userMeUploadPolicyUrl, params, true)
}

export const getUserAdminApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(userAdminUrl, params, true)
}

export const postUserAdminApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(userAdminUrl, qs.stringify(data), true)
}

export const patchUserDetailsAdminApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${userAdminUrl}/${path}`
    return await requests.patch(url, qs.stringify(data), true)
}

export const deleteUserDetailsAdminApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${userAdminUrl}/${path}`
    return await requests.delete(url, qs.stringify(data), true)
}






