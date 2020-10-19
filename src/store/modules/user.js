import { login, logout } from '@/api/user'
import router from '@/router/index'

export const user = {
  namespaced: true,
  state: {
    userInfo: {
      // uuid: '',
      username: '',
      email: '',
      IsAdmin: false,
      uuid: '',
    },
    token: '',
    expiresAt: ''
  },
  mutations: {
    setUserInfo(state, userInfo) {
      // 这里的 `state` 对象是模块的局部状态
      state.userInfo = userInfo
    },
    setToken(state, token) {
      // 这里的 `state` 对象是模块的局部状态
      state.token = token
    },
    setExpiresAt(state, expiresAt) {
      // 这里的 `state` 对象是模块的局部状态
      state.expiresAt = expiresAt
    },
    LoginOut(state) {
      state.userInfo = {}
      state.token = ''
      state.expiresAt = ''
      router.push({ name: 'Home', replace: true })
      sessionStorage.clear()
      window.location.reload()
    },
    ResetUserInfo(state, userInfo = {}) {
      state.userInfo = {
        ...state.userInfo,
        ...userInfo
      }
    }
  },
  /*
   res.data {
     userInfo: class, 
     token: string,
      expiresAt: string,
      code: int,
   }
   */
  actions: {
    async LoginIn({ commit }, loginInfo) {
      const res = await login(loginInfo)
      // console.log(res);
      commit('setUserInfo', res.userInfo)
      commit('setToken', res.token)
      commit('setExpiresAt', res.expiresAt)
      if (res.code === 0) {
        const redirect = router.history.current.query.redirect
        if (redirect) {
          router.push({ path: redirect })
        } else {
          router.push({ name: 'Home' })
        }
        return res.code
      } else {
        return res.code
      }
    },
    async LoginOut({ commit }, logoutInfo) {
      const res = await logout(logoutInfo);
      console.log(res)
      commit('LoginOut');
      if (res.code === 0) {
        router.push({ name: 'Home' })
      }
      return res.code
    }
  },
  getters: {
    userInfo(state) {
      return state.userInfo
    },
    token(state) {
      return state.token
    },
    expiresAt(state) {
      return state.expiresAt
    }
  }
}
