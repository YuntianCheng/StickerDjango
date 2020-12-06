import axios from './request'


export function getStick(data){
    return axios.request({
        url:'/api/get_sticks/',
        headers:{
            'Content-Type':'multipart/form-data'
        },
        method:'post',
        data:data,
        responseType: 'blob',
    })
}
