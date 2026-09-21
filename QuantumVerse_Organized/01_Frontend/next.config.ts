import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: process.env.VERCEL ?
  undefined : "standalone" ,           // Needed for Docker
  poweredByHeader: false,
  images: {
    domains: ["avatars.githubusercontent.com", "lh3.googleusercontent.com"],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1",
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options",         value: "DENY"                          },
          { key: "X-Content-Type-Options",   value: "nosniff"                       },
          { key: "Referrer-Policy",          value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
