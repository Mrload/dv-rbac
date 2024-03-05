import { defineStore } from 'pinia'
import { ref } from 'vue'

const useMenusStore = defineStore('menus', () => {
  const menuList = ref([])

  return { menuList }
})

export default useMenusStore
