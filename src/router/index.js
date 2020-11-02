import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home'
import Register from '@/views/Register'
import Test from '@/views/Test'
import Login from '@/views/Login'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}
Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: { title: 'Home' }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { title: 'Register' }
    },
    {
        path: '/test',
        name: 'Test',
        component: Test,
        meta: { title: 'Test' }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { title: 'Login' }
    },
    {
        path: '/pxc',
        name: 'pxc',
        component: () => import('@/views/pxc.vue'),
        meta: { title: 'pxc' }
    },
    {
        path: '/hxtdyf',
        name: 'hxtdyf',
        component: () => import('@/views/hxt.vue'),
        meta: { title: 'IloveYou' }
    },
    {
        path: '/chat',
        name: 'chat',
        component: () => import('@/views/chat/chat.vue'),
        meta: { title: 'Chat' }
    },
    {
        path: '/404',
        name: '404',
        component: () => import('@/views/404.vue'),
        meta: { title: 'Not Found' }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/profile.vue'),
        meta: { title: 'Profile' }
    },

    {
        path: '*',
        redirect: '/404'
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});
export default router