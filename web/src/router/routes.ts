const Main = () => import('@/views/main')

const routes = [
    {
        path: '/login',
        meta: {
            auth: false,
            hidden: true,
            title: '登录',
            icon: 'md-home'
        },
        component: () => import('@/views/login')
    },
    {
        path: '/',
        redirect: '/home',
        meta: {
            auth: true,
            hidden: true,
            title: '首页',
            icon: 'md-home'
        },
        component: Main,
        children: [
            {
                path: '/home',
                name: 'home',
                meta: {
                    auth: true,
                    hidden: true,
                    title: '开始',
                    icon: 'md-home'
                },
                component: () => import('@/views/home')
            }
        ]
    },
    {
        path: '/users',
        meta: {
            auth: true,
            hidden: true,
            title: '用户管理',
            icon: 'md-user'
        },
        component: Main,
        children: [
            {
                path: 'me',
                name: 'userMe',
                meta: {
                    auth: true,
                    hidden: true,
                    title: '个人信息',
                    icon: 'md-user'
                },
                component: () => import('@/views/user')
            }
        ]
    },
    {
        path: '/pics',
        meta: {
            auth: true,
            hidden: false,
            title: '图片管理',
            icon: 'md-images'
        },
        component: Main,
        children: [
            {
                path: '',
                name: 'pics',
                meta: {
                    auth: true,
                    hidden: false,
                    title: '图片列表',
                    icon: 'ios-list-box'
                },
                component: () => import('@/views/pic')
            },
        ]
    },
    {
        path: '/videos',
        meta: {
            auth: true,
            hidden: false,
            title: '视频管理',
            icon: 'logo-youtube'
        },
        component: Main,
        children: [
            {
                path: '',
                name: 'videos',
                meta: {
                    auth: true,
                    hidden: false,
                    title: '视频列表',
                    icon: 'md-videocam'
                },
                component: () => import('@/views/video')
            },
            {
                path: 'aaa',
                name: 'videos1',
                meta: {
                    auth: true,
                    hidden: true,
                    title: '视频列表1',
                    icon: 'md-videocam'
                },
                component: () => import('@/views/video')
            }
        ]
    },
    {
        path: '/admin',
        meta: {
            auth: true,
            permission: true,
            hidden: false,
            title: '综合管理',
            icon: 'md-apps'
        },
        component: Main,
        children: [
            {
                path: 'users',
                name: 'users',
                meta: {
                    auth: true,
                    permission: true,
                    hidden: false,
                    title: '用户列表',
                    icon: 'md-person'
                },
                component: () => import('@/views/user_admin')
            },
            {
                path: 'pics',
                name: 'adminPics',
                meta: {
                    auth: true,
                    permission: true,
                    hidden: false,
                    title: '图片列表',
                    icon: 'md-images'
                },
                component: () => import('@/views/pic_admin')
            },
            {
                path: 'videos',
                name: 'adminVideos',
                meta: {
                    auth: true,
                    permission: true,
                    hidden: false,
                    title: '视频列表',
                    icon: 'logo-youtube'
                },
                component: () => import('@/views/video_admin')
            }
        ]
    },
    {
        path: '/settings',
        meta: {
            auth: true,
            hidden: false,
            title: '设置',
            icon: 'ios-cog'
        },
        component: Main,
        children: [
            {
                path: '',
                name: 'settings',
                meta: {
                    auth: true,
                    hidden: false,
                    title: '安全设置',
                    icon: 'ios-build'
                },
                component: () => import('@/views/home')
            }
        ]
    },
    {
        path: '*',
        redirect: '/home',
        meta: {
            auth: true,
            hidden: true,
            title: '其他',
            icon: 'ios-home'
        },
    }
]

export default routes
