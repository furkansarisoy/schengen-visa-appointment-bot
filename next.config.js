/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  ...(process.env.NODE_ENV === 'production' ? {
    basePath: '/schengen-visa-appointment'
  } : {}),
  images: {
    unoptimized: true
  }
};

module.exports = nextConfig; 