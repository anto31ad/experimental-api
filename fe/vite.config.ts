import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'

export default defineConfig( ( { mode } ) => {

const env = loadEnv(mode, process.cwd(), '');

return {
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
  server: {
    host: env.VITE_HOST,
    port: parseInt(env.VITE_PORT),
  }
}
})