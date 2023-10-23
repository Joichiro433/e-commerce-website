import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
// import mkcert from 'vite-plugin-mkcert';

export default defineConfig({
  plugins: [sveltekit()],
  // plugins: [sveltekit(), mkcert()],
  // server: { https: true },
  server: {
    host: true,
    port: 8080,
  },
  preview: {
    host: true,
    port: 8080,
  },
});
