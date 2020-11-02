import { login, logout, createRoom, joinRoom, leaveRoom } from '@/api/user'
import router from '@/router/index'

export const user = {
  namespaced: true,
  state: {
    userInfo: {
      username: '',
      email: '',
      IsAdmin: false,
      uuid: '',
      room: '',
      isHost: false,
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
    setRoom(state, roomID) {
      state.userInfo.room = roomID
    },
    setHost(state) {
      state.userInfo.isHost = true;
    }
    ,
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
    },
    deleteHost(state) {
      state.userInfo.isHost = false;
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
    removeHost({commit}) {
        commit('deleteHost');
    },
    async newRoom({ commit }, info) {
      const res = await createRoom(info);
      commit('setRoom', res.data);
      commit('setHost');
      return res.code;
    },
    async joinRoomIn({ commit }, info) {
      const res = await joinRoom(info);
      commit('setRoom', res.data);
      return res.code;
    },
    async leaveRoomOut({ commit }, info) {
      const res = await leaveRoom(info);
      commit('setRoom', "");
      return res.code;
    },
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
