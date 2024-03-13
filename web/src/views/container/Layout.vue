<template>
    <el-container class='main-container'>
      <el-header>
        <Header></Header>
      </el-header>
      <el-container>
        <el-aside >
          <Aside></Aside>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
</template>

<script setup lang='ts' name="main">
import Aside from '@/views/container/Aside.vue'
import Header from '@/views/container/Header.vue'
import useMenuStore from '@/store/menus'

const menuStore = useMenuStore()



</script>

<style>
.main-container {
  height:100vh
}

.el-header {
  height:100px;
  padding:10px;
}

.el-aside {
  width:200px;
}

.el-main {
  border:2px solid red;
}


</style>
