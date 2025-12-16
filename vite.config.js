import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import glslify from 'rollup-plugin-glslify';

export default defineConfig({
    plugins: [
        // CRITICAL: Process GLSL shaders before JS
        glslify({
            include: ['**/*.vs', '**/*.fs', '**/*.vert', '**/*.frag', '**/*.glsl'],
            compress: false
        }),
        svelte()
    ],
    server: {
        host: true,
        port: 3344,
        // PROXY: Routes /images requests to our Python server
        proxy: {
            '/images': {
                target: 'http://localhost:8123',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/images/, '')
            }
        },
        watch: {
            // CRITICAL: Ignore image folder to prevent 'ENOSPC' crash
            ignored: ['**/public/**', '**/tiles/**']
        }
    },
    optimizeDeps: {
        include: ['regl', 'glslify', 'apache-arrow']
    }
});
