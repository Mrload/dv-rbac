<template>

  <el-menu>
    <SubMenu :menu="menu" v-for="menu in menuList" :key="menu.name"></SubMenu>
  </el-menu>

</template>


<script setup name='aside'>
  import SubMenu from "@/components/SubMenu.vue"

  const menuList = [
    {
      name: 'home',
      chineseName: '首页'
    },
    {
      name: 'literature',
      chineseName: '文学',
      icon:"Edit",
      childMenu: [
        {
          name: 'cartoon',
          chineseName: '动漫',
        },
        {
          name: 'essay',
          chineseName: '散文随笔',
          childMenu: [
            {
              name: 'youth_literature',
              chineseName: '青春文学',
            }
          ]
        },
        {
          name: 'suspenseful_reasoning',
          chineseName: '悬疑推理',
          childMenu: [
            {
              name: 'history',
              chineseName: '历史',
            },
            {
              name: 'noval',
              chineseName: '小说',
              childMenu: [
                {
                  name: 'fiction',
                  chineseName: '科幻',
                },
                {
                  name: 'martial_arts',
                  chineseName: '武侠',
                }
              ]
            }
          ]
        }
      ]
    },
    {
      name: 'psychology',
      chineseName: '心理学',
    }
  ]

</script>
