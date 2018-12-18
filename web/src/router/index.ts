import Vue from 'vue';
import Router from 'vue-router';
import routes from './routes'
import Store from '@/store'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
})

router.beforeEach((to, from, next) => {
    // @ts-ignore
    to.matched.some(record => {
        const errors = ['', null, 'null', undefined, 'undefined']
        let access_token
        try {
            access_token = (Store.state.token as any).access_token
        } catch (e) {
            access_token = ''
        }
        if (record.meta.auth) {
            if (errors.includes(access_token)) {
                next('/login')
            } else {
                next()
            }
        } else {
            if (record.path === '/login') {
                if (!errors.includes(access_token)) {
                    next('/')
                }
            }
            next()
        }
    })
})

export default router
