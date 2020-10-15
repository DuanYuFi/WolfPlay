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
        meta: { title: 'Home'}
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { title: 'Register'}
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
        path: '/404',
        name: '404',
        component: () => import('@/views/404.vue'),
        meta: { title: 'Not Found' }
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