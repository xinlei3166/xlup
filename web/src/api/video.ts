import requests from '@/libs/request'
import qs from 'qs'
import { videoUrl, videoAdminUrl } from './urls'

export const getVideoApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(videoUrl, params, true)
}

export const postVideoApi = async (...args: object[]): Promise<any> => {
    const data = args ? args[0] : {}
    return await requests.post(videoUrl, data, true)
}

export const deleteVideoApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${videoUrl}/${path}`
    return await requests.delete(url, qs.stringify(data), true)
}

export const getVideoAdminApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(videoAdminUrl, params, true)
}

export const deleteVideoAdminDetailsoApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${videoAdminUrl}/${path}`
    return await requests.delete(url, qs.stringify(data), true)
}
