<template>
  <el-row :gutter="20">
    <el-col :span="6"></el-col>
    <el-col :span="6"></el-col>
    <el-col :span="6"></el-col>
    <el-col :span="6"><el-button @click="logOut">注销</el-button></el-col>
  </el-row> 
</template>

<script setup lang="ts">
  import { rmJWT } from "@/util"

  const logOut = ()=>{
    rmJWT()
  }

</script>
