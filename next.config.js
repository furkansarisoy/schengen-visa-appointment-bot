/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/schengen-visa-appointment-bot',
  images: {
    unoptimized: true,
  },
  assetPrefix: '/schengen-visa-appointment-bot/',
  trailingSlash: true,
}

module.exports = nextConfig 