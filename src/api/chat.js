import service from '@/utils/request'

export const sendMessage = (data) => {
    return service({
        url: "/chat/sendmessage/", 
        method: "post", 
        data: JSON.stringify(data)
    })
}

export const loadChat = (data) => {
    return service({
        url: "/chat/loadchat/", 
        method: "post", 
        data: JSON.stringify(data)
    })
}

export const getRoomMembers = (data) => {
    return service({
        url: '/chat/getroommembers/',
        method: "post",
        data: JSON.stringify(data)
    })
}

export const gameStart = (data) => {
    return service({
        url: '/game/start/',
        method: 'post',
        data: JSON.stringify(data)
    })
}