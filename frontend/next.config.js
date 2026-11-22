/** @type {import('next').NextConfig} */
module.exports = {
  // lets the app import ../shared (model code, sample lessons) and ../models (trained weights),
  // so the HTML demo and this app always use the same files
  experimental: { externalDir: true },
  reactStrictMode: true,
};
