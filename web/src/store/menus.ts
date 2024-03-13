import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { request } from "@/api/request"


const useMenusStore = defineStore('menus', () => {
  const menuList = ref([])

  const getMenuList = computed(() => menuList.value)
  
  const getMenuLength = ()=>{
    return menuList.value.length
  }

  const setMenuList = (v) => {
    menuList.value = v
  }

  return { menuList, getMenuList, setMenuList }
})

export default useMenusStore
