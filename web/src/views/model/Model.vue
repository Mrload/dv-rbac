<template>
  <el-button 
    type="primary" 
    @click="addModel"
  >
    注册模型
  </el-button>
  <el-table
    :data=modelData
    stripe
    border
  >
    <el-table-column prop="name" label="模型名称" width="200" />
    <el-table-column prop="alias" label="模型别称" width="200" />
    <el-table-column prop="kind" label="类型" width="200" />
    <el-table-column prop="description" label="描述信息" minWidth="400" />
    <el-table-column prop="init_params" label="初始参数" minWidth="400" />

    <el-table-column prop="call_url" label="调用地址" minWidth="400" />
    <el-table-column prop="call_params" label="调用参数" minWidth="400" />
    <el-table-column fixed="right" label="操作" minWidth="300">
      <template #default="scope">
        <el-button 
          link
          type="primary"
          @click="handleEdit"
        >
        编辑
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  
</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue"
  import { request } from "@/api/request"

  const modelData = ref([])


  onMounted(() => {
    request({
      url:"/api/system/models/",
      method:"GET"
    }).then(({data})=>{
      modelData.value = data
    })
  })
  
  const addModel = () => {

  }

  const handleEdit = () => {

  }
</script>

<style lang="css">
  
</style>
