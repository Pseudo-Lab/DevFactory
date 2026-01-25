import { defineConfig } from 'vite';

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
    }
});
