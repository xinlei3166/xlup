import requests from '@/libs/request'
import { videoUrl } from './urls'

export const getVideoApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(videoUrl, params, true)
}

export const deleteVideoApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${videoUrl}/${path}`
    return await requests.delete(url, data, true)
}
