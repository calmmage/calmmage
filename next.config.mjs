// /** @type {import('next').NextConfig} */
// const nextConfig = {};

// export default nextConfig;
import withNextra from 'nextra'

const nextraConfig = withNextra({
      theme: 'nextra-theme-docs',
      themeConfig: './theme.config.tsx',
      NextConfig: {
            output: "standalone",
      },
})
export default nextraConfig;