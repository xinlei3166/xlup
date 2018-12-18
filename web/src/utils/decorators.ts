import { refreshToken } from '@/utils/token'
import Vue from 'vue'
import router from '@/router'

export function checkToken() {
    return function inner(target, key, descriptor) {
        const method = descriptor.value
        descriptor.value = async (...args) => {
            const coro = args[0]    // 异步函数
            const coroArgs = args.slice(1)  // 异步函数参数
            let data = await coro(...coroArgs)    // 获取数据
            if (data) {
                switch (data.code) {
                    case 'AccessTokenExpires':
                        const ret = await refreshToken()
                        if (ret) {
                            data = await coro(...coroArgs)
                            return method.apply(target, [data])
                        } else {
                            Vue.prototype.$Message.error({content: '登录信息已过期，请重新登录', duration: 2})
                            router.push('/login')
                        }
                        break
                    case 'TokenFormatError':
                        Vue.prototype.$Message.error({content: '身份状态失效', duration: 2})
                        router.push('/login')
                        break
                    default:
                        return method.apply(target, [data])
                }
            }
        }
        return descriptor;
    }
}

