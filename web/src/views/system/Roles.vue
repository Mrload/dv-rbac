<template>
  <el-button 
    type="primary" 
    @click="addRole"
  >
    新增角色
  </el-button>
  <el-table
    :data=roleData
    stripe
    border
  >
    <el-table-column prop="name" label="角色名称" width="200" />
    <el-table-column prop="description" label="描述信息" minWidth="400" />
    <el-table-column fixed="right" label="操作" minWidth="300">
      <template #default="scope">
        <el-button 
          link
          type="primary"
          @click="showRouterPermissionDialog(scope.row)"
        >
        后端路由权限
        </el-button>
        <el-button 
          link
          type="primary"
          @click="showMenuPermissionDialog"
        >
        前端菜单权限
        </el-button>
        <el-button 
          link
          type="primary"
          @click="showModelPermissionDialog(scope.row)"
        >
        各类模型权限
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  
  <el-drawer
    :model-value="currentRouterPermission.length!==0"
    title="后端路由权限管理"
    direction="rtl"
    @close = "handleDialogClose"
  >
    <el-table :data="currentRouterPermission" border style="width: 100%">
      <el-table-column prop="name" label="权限名称" width="180" />
      <el-table-column prop="url" label="路由地址" width="180" />
      <el-table-column prop="method" label="请求方式" />
    </el-table>
  </el-drawer>

  <el-drawer
    :model-value="currentModelPermission.length!==0"
    title="模型权限管理"
    direction="rtl"
    @close = "handleDialogClose"
  >
    <el-table :data="currentModelPermission" border style="width: 100%">
      <el-table-column prop="alias" label="模型名称" width="180" />
    </el-table>
  </el-drawer>

</template>

<script setup lang="ts">
  import { ref, onMounted } from "vue"
  import { request } from "@/api/request"

  const roleData = ref([])


  onMounted(() => {
    request({
      url:"/api/system/roles/",
      method:"GET"
    }).then(({data})=>{
      roleData.value = data
    })
  })
  
  const addRole = () => {

  }

  //----------------------后端路由权限窗口--------------------------
  
  const currentRouterPermission = ref([])

  const showRouterPermissionDialog = (roleInfo)=> {
    // 获取该角色所拥有的路由权限
    request({
      url:"/api/system/router-permissions/",
      method:"GET",
      params:{related_role:roleInfo.id}
    }).then(({data}) => {
      currentRouterPermission.value = data
    })
  }
  //----------------------后端路由权限窗口--------------------------
  const showMenuPermissionDialog = ()=> {
    console.log("打开前端权限弹窗")
  }

  //----------------------模型权限窗口--------------------------
  const currentModelPermission = ref([])
  const showModelPermissionDialog = (roleInfo)=> {
    request({
      url:"/api/system/models/",
      method:"GET",
      params:{roles:roleInfo.id}
    }).then(({data}) => {
      currentModelPermission.value = data
    })
  }

  // ----------------------公共的窗口关闭回调----------------------
  const handleDialogClose = () => {
    currentRouterPermission.value = []
    currentModelPermission.value = []
  }

</script>

<style lang="css">
  
</style>
