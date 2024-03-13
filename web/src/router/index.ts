import { createRouter, createWebHistory } from 'vue-router'
import { getJWT, setJWT } from '@/util'
import { request } from "@/api/request"
import useMenuStore from "@/store/menus"



const routes = [
  {
    name:"login",
    path:'/login',
    component:() => import('@/views/Login.vue')
  },
  {
    name:'main',
    path:'/main',
    redirect:to => {
      return {name:'dashboard'}
    },
    component: () => import("@/views/container/Layout.vue"),
    children:[
      {
        name:'dashboard',
        path:'',
        component: () => import("@/views/dashboard/Dashboard.vue")
      },
      //{
      //  name:'users',
      //  path:'/system/users',
      //  component: () => import("@/views/system/Users.vue")
      //},
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

    // 验证pinia内容是否存在，否则先拉取各类信息
    if (menuStore.getMenuList.length==0) {
      console.log("动态路由信息为空,设置动态路由")
      await request({
        url:'/api/system/menus/',
        method:'get',
      }).then(res => {
        menuStore.setMenuList(res.data)  //从服务器后端获取动态路由存储至pinia
        return res
      }).then((res) => {
        addRoute(res.data) // 遍历前端的路由组件，用于前端加载
        router.push({name:"main"}) // 没搞定加载顺序，所以强制跳到了主页
      })
    }
    next()
  }

})

const addRoute = (data) => {
  data.forEach(element => {
    if (element.childrens && element.childrens.length !== 0) {
      addRoute(element.childrens)
    }else{
      console.log(element)
      router.addRoute("main",{name:element.name,path:element.url,component:()=>import(element.component_path)})
    }
  })
}


export default router


