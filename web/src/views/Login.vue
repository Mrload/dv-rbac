<template>
    <div class="mainBox">
        <div class="loginBox">
            <h1 class="loginTitle">XXX</h1>
            <h5 class="loginTitle1">Biodiversity Intelligent Monitoring System</h5>
            
            <el-form ref="loginRef"  :model="loginForm" size="default" status-icon 
                class="demo-ruleForm">
    
                <el-form-item  prop="username">
                    <el-input v-model="loginForm.username" placeholder="用户名" type="text" autocomplete="off" />
                </el-form-item>

                <el-form-item prop="password">
                    <el-input v-model="loginForm.password" placeholder="密码" type="password" autocomplete="off" />
                </el-form-item>

                <el-form-item>
                    <el-button class="loninBtn" type="primary" @click='handleLogin'>登录</el-button>
                </el-form-item>
                
            </el-form>
        </div>
        
    </div>
    
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { doLogin } from '@/api'
import { getJWT, setJWT } from '@/util'
import { useRouter } from 'vue-router';
//import { ElMessage } from 'element-plus';

const name = '全生物监测系统登录'
const router = useRouter()


// form 值
const loginForm = reactive({
    username: '',
    password: ''
})

const handleLogin = () => {
    doLogin(loginForm).then(res => {
        setJWT(res.data.access)
        router.push('/')
    }).catch(err => {
        ElMessage({ message: '用户名或密码错误', type: 'error' })
    })
}

onMounted(() => {
    document.title = name
})

</script>

<style scoped>
.mainBox {
    position: fixed;
    /*position: absolute;*/
    width: 100%;
    height: 100%;
    /*background: url('../../assets/all-animal.jpg');
    background-size: 100% 100%;*/
    /*background-size: contain;*/
    /*background-attachment:fixed;*/
    /*background-repeat:no-repeat;*/
}



.loginBox {
    border-radius: 15px;
    margin: 230px auto;
    width: 500px;
}

.login-label{
    float:left;
    color:red;
}
.loginTitle {
    margin: 0px auto 0px auto;
    text-align: center;
    font-size: 40px;
    color: aliceblue;
    text-shadow: 2px 2px 5px black;
}

.loginTitle1 {
    margin: 0px auto 0px auto;
    text-align: center;
    font-size: 20px;
    color: aliceblue;
    text-shadow: 2px 2px 5px black;
}


.demo-ruleForm {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 20px auto;
    width: 350px;
    padding: 15px 35px 15px 35px;
    backdrop-filter: blur(5px);
    border-style: double;
    border-color: gray;
    border-width: 1px;
    padding-top: 30px;
}

.label {
    font-size: large;
}

.loninBtn {
    width: 100%;
}
</style>
