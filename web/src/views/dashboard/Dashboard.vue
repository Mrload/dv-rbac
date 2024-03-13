<template>
  <el-button class="ml-3" type="success" @click="submitUpload">
    上传并检测
  </el-button>
  <el-upload
    class="upload-demo"
    ref="uploadRef"
    drag
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    multiple
    :auto-upload="false"
    list-type="picture-card"
    :limit=50
    accept="image/jpeg,image/gif,image/png"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖放图片 或 <em>点击上传</em>
    </div>

    <template #tip>
      <div class="el-upload__tip">
        单次上传图片上限50张
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
  import { ref } from "vue"

  const uploadRef = ref()

  const submitUpload = () => {
    console.log(uploadRef)
  }

</script>


<style >
.upload-demo {
  height :100px;
}
</style>
