import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const config = {
    plugins: [react()],
    base: '/',
    server: {
      port: 5173, // Cổng mặc định của Vite
      proxy: {
        // Cấu hình Proxy để chuyển hướng API sang Django (8080)
        '/api': {
          target: 'http://127.0.0.1:8080',
          changeOrigin: true,
          secure: false,
        },
      }
    }
  }

  // Cấu hình riêng cho lệnh 'npm run build' để Django đọc được file tĩnh
  if (command !== 'serve') {
    config.base = '/static/';
  }

  return config
})