import { request } from "@/api/request"
import { ElMessage } from 'element-plus'
import { useRouter } from "vue-router"



// 登录接口
export const doLogin=(data)=>{
    return request({
        url:'/api/login/',
        method:'post',
        data:data
    })
}

// 验证登录
export const verifyLogin = ()=>{
    return request({
        url:'/api/login_verify/',
        data:{token:localStorage.getItem('JWT')},
        method:'post'
    })
} 

//获取登录用户信息的接口
export const getUserInfo = ()=>{
    return request({
        url:'/api/login_user_info/',
        method:'get'
    })
}

//获取模型类信息
export const getDetectModels = (model_type,use_for=null)=>{
    return request({
        url:'/api/models-info/',
        method:'get',
        params:{
            "model_type": model_type,
            "use_for":use_for
        }
    })
}

//调用批量检测接口
export const customDetect = (data)=>{
    return request({
        url:'/api/custom-detect/',
        method:'post',
        data:data,
        timeout:600000
    })
}
