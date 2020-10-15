import service from '@/utils/request'

// @Summary 用户登录
// @Produce  application/json
// @Param data body {username:"string",password:"string"}
// @Router /user/login [post]
export const login = (data) => {
  return service({
    url: '/user/login/',
    method: 'post',
    data: JSON.stringify(data)
  })
}

// @Summary 用户注册
// @Produce  application/json
// @Param data body {email:"string",username:"string",password:"string"}
// @Router /user/register [post]
export const register = (data) => {
  return service({
    url: '/user/register/',
    method: 'post',
    data: JSON.stringify(data)
  })
}

export const check = (data) => {
  return service({
    url: '/user/register/check',
    method: 'post',
    data: data
  })
}