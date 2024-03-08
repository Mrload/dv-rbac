import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import path from 'path'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],

  resolve:{
    alias:{'@':path.resolve(__dirname,'./src')}
  },

  server:{
    proxy:{
      "/api":{
        target:"http://120.221.208.98:6012",
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    },
  },

})
