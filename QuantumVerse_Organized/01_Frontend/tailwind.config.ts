import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        quantum: {
          blue: "#00D4FF",
          purple: "#7B2FBE",
          cyan: "#06FFA5",
          dark: "#050A1A",
          navy: "#0A1628",
          panel: "#0D1F3C",
          glow: "rgba(0, 212, 255, 0.15)",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "float": "float 3s ease-in-out infinite",
        "spin-slow": "spin 8s linear infinite",
      },
      keyframes: {
        "accordion-down": {"from": {"height": "0"}, "to": {"height": "var(--radix-accordion-content-height)"}},
        "accordion-up": {"from": {"height": "var(--radix-accordion-content-height)"}, "to": {"height": "0"}},
        "pulse-glow": {"0%, 100%": {"opacity": "1", "boxShadow": "0 0 20px rgba(0,212,255,0.3)"}, "50%": {"opacity": "0.8", "boxShadow": "0 0 40px rgba(0,212,255,0.6)"}},
        "float": {"0%, 100%": {"transform": "translateY(0)"}, "50%": {"transform": "translateY(-10px)"}},
      },
      backgroundImage: {
        "quantum-gradient": "linear-gradient(135deg, #050A1A 0%, #0A1628 50%, #0D1F3C 100%)",
        "glow-gradient": "radial-gradient(ellipse at center, rgba(0,212,255,0.1) 0%, transparent 70%)",
      },
      fontFamily: {
        sans: ["Times New Roman", "Times", "serif"],
        serif: ["Times New Roman", "Times", "serif"],
        mono: ["Times New Roman", "Times", "serif"],
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [animate],
};

export default config;
