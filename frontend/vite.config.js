import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// Resolve a path relative to this config file (frontend/)
const r = (p) => fileURLToPath(new URL(p, import.meta.url))

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
    fs: { allow: ['..'] },
  },
  resolve: {
    // Tests live outside frontend/, so bare-module imports in test files need to
    // be explicitly routed to the packages installed in frontend/node_modules.
    alias: {
      '@vue/test-utils': r('./node_modules/@vue/test-utils'),
      'vue': r('./node_modules/vue'),
      'vitest': r('./node_modules/vitest'),
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['../tests/frontend/**/*.test.js'],
  },
})
