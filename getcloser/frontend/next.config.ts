const nextConfig = {
  async rewrites() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: `${process.env.NEXT_PUBLIC_API_BASE || ''}/:path*`,
        },
      ];
    }
    return [];
  },
  /* config options here */
};

export default nextConfig;
