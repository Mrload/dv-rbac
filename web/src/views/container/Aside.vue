<template>

  <el-menu :router="true">
    <SubMenu :menu="menu" v-for="menu in menuList" :key="menu.name"></SubMenu>
  </el-menu>

</template>


<script setup name='aside'>
  import { onMounted,ref } from "vue"
  import useMenusStore from "@/store/menus"
  import SubMenu from "@/components/SubMenu.vue"

  const menuList = ref([])

  onMounted(() => {
    const menuStore = useMenusStore()
    menuList.value = menuStore.menuList
    console.log("加载侧边",menuList.value)
  })
</script>
