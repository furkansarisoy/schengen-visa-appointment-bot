/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/schengen-visa-appointment',
  images: {
    unoptimized: true,
  },
  assetPrefix: '/schengen-visa-appointment/',
  trailingSlash: true,
}

module.exports = nextConfig 