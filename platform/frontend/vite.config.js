import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    server: {
        allowedHosts: [
            'private.pseudolab-devfactory.com'
        ],
        host: '0.0.0.0',
        port: 5173,
        // Add HMR port if needed for Traefik
        hmr: {
            clientPort: 443
        }
    },
    build: {
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html'),
                history: resolve(__dirname, 'history/index.html'),
            },
        },
    },
});
