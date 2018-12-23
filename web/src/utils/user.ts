import Store from '@/store';
import {userMeAccessKeyUrl} from '@/api/urls';

export const getUserInfo = (): object => {
    const userInfo = localStorage.getItem('userInfo')
    return JSON.parse(userInfo === null ? '{}' : userInfo)
}

export const setUserInfo = (userInfo: object): void => {
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
    Store.commit('changeUserInfo')
}

export const getUserAccessKey = (): object => {
    const userAccessKey = localStorage.getItem('userAccessKey')
    return JSON.parse(userAccessKey === null ? '{}' : userAccessKey)
}

export const setUserAccessKey = (userAccessKey: object): void => {
    localStorage.setItem('userAccessKey', JSON.stringify(userAccessKey))
    Store.commit('changeUserAccessKey')
}

export const checkPermission = (item: boolean): boolean => {
    const permission = (Store.state.userInfo as any).role_codename
    return item === true ? permission === 'admin' : true
}

