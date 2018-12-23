import requests from '@/libs/request'
import qs from 'qs'
import { picUrl, picAdminUrl } from './urls'

export const getPicApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(picUrl, params, true)
}

export const postPicApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(picUrl, data, true)
}

export const deletePicApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${picUrl}/${path}`
    return await requests.delete(url, qs.stringify(data), true)
}

export const getPicAdminApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(picAdminUrl, params, true)
}

export const deletePicAdminDetailsApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${picAdminUrl}/${path}`
    return await requests.delete(url, qs.stringify(data), true)
}
