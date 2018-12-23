import axios from 'axios'
import qs from 'qs'
import Vue from 'vue'
import Store from '@/store'

axios.defaults.timeout = 2000 // 请求超时时间
axios.defaults.baseURL = ''    // 其他地方请求地址可以省略域名
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded' // 全局设置post请求的数据编码格式
// axios.defaults.headers.common['Authorization'] = '123' // 第三方认证涉及到token 如果没有可以干掉

// request 拦截器
axios.interceptors.request.use(
    config => {
        // const token = getCookie('名称');注意使用的时候需要引入cookie方法，推荐js-cookie
        // config.data = qs.stringify(config.data);
        // if(token){
        //   config.params = {'token': token}
        // }
        return config;
    }, error => {
        return Promise.reject(error);
    }
);

// response 拦截器
axios.interceptors.response.use(response => {
    // 在这里你可以判断后台返回数据携带的请求码
    return response.data
}, (error) => {
    if (error && error.response) {
        switch (error.response.status) {
            case 400:
                error.message = '请求错误(400)';
                break
            case 401:
                error.message = '未授权，请重新登录(401)';
                break
            case 403:
                error.message = '拒绝访问(403)';
                break
            case 404:
                error.message = '请求出错(404)';
                break
            case 408:
                error.message = '请求超时(408)';
                break
            case 500:
                error.message = '服务器错误(500)';
                break
            case 501:
                error.message = '服务未实现(501)';
                break
            case 502:
                error.message = '网络错误(502)';
                break
            case 503:
                error.message = '服务不可用(503)';
                break
            case 504:
                error.message = '网络超时(504)';
                break
            case 505:
                error.message = 'HTTP版本不受支持(505)';
                break
            default:
                error.message = `连接出错(${error.response.status})!`
        }
    } else {
        error.message = '连接服务器失败!'
    }
    Vue.prototype.$Message.error({content: error.message, duration: 2})
    return Promise.reject(error)
})

function request(config: object = {}): Promise<any> {
    return new Promise((resolve, reject) => {
        axios.request(config)
            .then(response => {
                resolve(response);
            })
            .catch(error => {
                reject(error)
            })
    })
}

async function get(url: string, params: object = {}, auth: boolean = false, token: string = null, config: object = {}): Promise<any> {
    config['method'] = 'get'
    config['url'] = url
    config['params'] = params
    if (auth) {
        let localToken
        try {
            localToken = Store.state.token['access_token']
        } catch (e) {
            localToken = ''
        }
        if (config['headers']) {
            config['headers']['Authorization'] = `Bearer ${!token ? localToken : token}`
        } else {
            config['headers'] = {Authorization: `Bearer ${!token ? localToken : token}`}
        }
    }
    try {
        return await request(config)
    } catch (e) {
        return
    }
}

async function post(url: string, data: any, auth: boolean = false, token: string = '', config: object = {}): Promise<any> {
    config['method'] = 'post'
    config['url'] = url
    config['data'] = data
    if (auth) {
        let localToken
        try {
            localToken = Store.state.token['access_token']
        } catch (e) {
            localToken = ''
        }
        if (config['headers']) {
            config['headers']['Authorization'] = `Bearer ${!token ? localToken : token}`
        } else {
            config['headers'] = {Authorization: `Bearer ${!token ? localToken : token}`}
        }
    }
    try {
        return await request(config)
    } catch (e) {
        return
    }
}

async function put(url: string, data: any, auth: boolean = false, token: string = '', config: object = {}): Promise<any> {
    config['method'] = 'put'
    config['url'] = url
    config['data'] = data
    if (auth) {
        let localToken
        try {
            localToken = Store.state.token['access_token']
        } catch (e) {
            localToken = ''
        }
        if (config['headers']) {
            config['headers']['Authorization'] = `Bearer ${!token ? localToken : token}`
        } else {
            config['headers'] = {Authorization: `Bearer ${!token ? localToken : token}`}
        }
    }
    try {
        return await request(config)
    } catch (e) {
        return
    }
}

async function patch(url: string, data: any, auth: boolean = false, token: string = '', config: object = {}): Promise<any> {
    config['method'] = 'patch'
    config['url'] = url
    config['data'] = data
    if (auth) {
        let localToken
        try {
            localToken = Store.state.token['access_token']
        } catch (e) {
            localToken = ''
        }
        if (config['headers']) {
            config['headers']['Authorization'] = `Bearer ${!token ? localToken : token}`
        } else {
            config['headers'] = {Authorization: `Bearer ${!token ? localToken : token}`}
        }
    }
    try {
        return await request(config)
    } catch (e) {
        return
    }
}

async function _delete(url: string, data: any, auth: boolean = false, token: string = '', config: object = {}): Promise<any> {
    config['method'] = 'delete'
    config['url'] = url
    config['data'] = data
    if (auth) {
        let localToken
        try {
            localToken = Store.state.token['access_token']
        } catch (e) {
            localToken = ''
        }
        if (config['headers']) {
            config['headers']['Authorization'] = `Bearer ${!token ? localToken : token}`
        } else {
            config['headers'] = {Authorization: `Bearer ${!token ? localToken : token}`}
        }
    }
    try {
        return await request(config)
    } catch (e) {
        return
    }
}

export default {
    request,
    get,
    post,
    put,
    patch,
    delete: _delete,
}
