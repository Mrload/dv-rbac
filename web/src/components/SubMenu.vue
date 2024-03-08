<template>
  
  <!-- 有子DOM递归渲染 -->
  <el-sub-menu :index="menu.url" v-if="menu.childrens">
    <template #title>
      <el-icon>
        <component :is="menu.icon" ></component>
      </el-icon>
      <span>{{ menu.alias }}</span>
    </template>

    <!-- 多级嵌套菜单渲染 -->
    <SubMenu :menu="menuItem" v-for="menuItem in menu.childrens" :key="menuItem.name"></SubMenu>
  </el-sub-menu>


  <!-- 无子DOM -->
  <el-menu-item :index="menu.url" v-else>
    <el-icon>
      <component :is="menu.icon"></component>
    </el-icon>
    <template #title>{{ menu.alias }}</template>
  </el-menu-item>

</template>

<script setup lang="ts">
interface Menu {
  name: string //菜单唯一标识，与路由名保持一致
  chineseName: string //菜单显示名称
  childMenu?: Menu[] | undefined //子菜单
}

defineProps<{
  menu: Menu
}>()
</script>

