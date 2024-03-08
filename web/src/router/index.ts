import { createRouter, createWebHistory } from 'vue-router'
import { getJWT, setJWT } from '@/util'
import useMenuStore from "@/store/menus"



const routes = [
  {
    name:"login",
    path:'/login',
    component:() => import('@/views/Login.vue')
  },
  {
    name:'main',
    path:'',
    component: () => import("@/views/container/Container.vue"),
    children:[
      {
        name:'dashboard',
        path:'/dashboard',
        component: () => import("@/views/dashboard/Dashboard.vue")
      },
      {
        name:'users',
        path:'/system/users',
        component: () => import("@/views/system/Users.vue")
      },
    ],
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes, 
})


// 路由守卫
router.beforeEach(async (to, from, next) => {
  let token = getJWT()
  const menuStore = useMenuStore()


  // 路由至登录页且无token:跳转登录页 
  if(to.name == 'login' && !token){
    console.log("路由至登录页且无token:跳转登录页 ")
    next()
  }
  // 路由至登录页但有token:到主页 
  else if (to.name == 'login' && token) {
    console.log("路由至登录页但有token:到主页 ")
    next({name:""})
  }

  //无token: 跳转登录页
  else if(!token){
    console.log("无token: 跳转登录页")
    next({name:'login'})
  }
 
  // 有token且非前往登录页
  else{
    console.log("正常跳转")

    console.log(menuStore)
    // 验证pinia内容是否存在，否则先拉取各类信息
    if (!menuStore.menuList.value) {
      console.log("动态路由信息为空")
      await menuStore.setMenuList()  //从服务器后端获取动态路由
      // 添加动态路由
      console.log(menuStore.menuList)
      //更新路由
    }

    next()
  }


  

})



export default router


