/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/schengen-visa-appointment',
  images: {
    unoptimized: true,
  },
  assetPrefix: '/schengen-visa-appointment/',
  trailingSlash: true,
  webpack: (config) => {
    config.module.rules.push({
      test: /\.css$/,
      use: ['style-loader', 'css-loader'],
    });
    return config;
  },
}

module.exports = nextConfig 