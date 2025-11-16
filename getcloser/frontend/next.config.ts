const nextConfig = {
  async rewrites() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          // 백엔드에 /api 프리픽스가 포함되어 있으므로 그대로 전달
          destination: `${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/:path*`,
        },
      ];
    }
    return [];
  },
  /* config options here */
};

export default nextConfig;
