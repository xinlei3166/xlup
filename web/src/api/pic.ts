import requests from '@/libs/request'
import { picUrl } from './urls'

export const getPicApi = async (...args: object[]): Promise<any> => {
    const params = args ? args[0] : {}
    return await requests.get(picUrl, params, true)
}

export const deletePicApi = async (...args: object[]): Promise<any> => {
    const path = args ? args[0] : ''
    const data = args ? args[1] : {}
    const url = `${picUrl}/${path}`
    return await requests.delete(url, data, true)
}
