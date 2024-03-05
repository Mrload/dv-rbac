<template>
    <el-container class='main-container'>
      <el-header>
        Header
      </el-header>
      <el-container>
        <el-aside >
          <Aside></Aside>
        </el-aside>
        <el-main>
          Main
        </el-main>
      </el-container>
    </el-container>
</template>

<script setup lang='ts' name="main">
import Aside from '@/views/container/Aside.vue'
import useMenuStore from '@/store/menus'

const menuStore = useMenuStore()



</script>

<style>
.main-container {
  height:100vh
}

.el-header {
  height:100px;
  background-color:red;
  padding:10px;
  border:5px solid black;
}

.el-aside {
  width:200px;
  background-color:green;
  border:5px solid white;
}

.el-main {
  background-color:blue;
  border:2px solid red;
}


</style>
