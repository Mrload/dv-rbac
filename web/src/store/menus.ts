import { defineStore } from 'pinia'
import { ref } from 'vue'
import { request } from "@/api/request"


const useMenusStore = defineStore('menus', () => {
  const menuList = ref([])
  
  const getMenuList = ()=>{
    return menuList.value.length
  }

  const setMenuList = () => {
    request({
      url:'/api/system/menus/',
      method:'get',
    }).then(res => {
      menuList.value = res.data
    })
  }

  return { menuList, setMenuList }
})

export default useMenusStore
