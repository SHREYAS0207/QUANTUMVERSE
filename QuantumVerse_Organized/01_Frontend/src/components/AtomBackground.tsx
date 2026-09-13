"use client";

import { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  radius: number;
  speed: number;
  phase: number;
}

export function AtomBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext("2d");
    if (!context) return;

    let animationFrame = 0;
    let particles: Particle[] = [];

    const resize = () => {
      const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = window.innerWidth * pixelRatio;
      canvas.height = window.innerHeight * pixelRatio;
      canvas.style.width = `${window.innerWidth}px`;
      canvas.style.height = `${window.innerHeight}px`;
      context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
      particles = Array.from({ length: 34 }, (_, index) => ({
        x: (index * 97) % window.innerWidth,
        y: (index * 53) % window.innerHeight,
        radius: 1 + (index % 3) * 0.45,
        speed: 0.00035 + (index % 5) * 0.00008,
        phase: index * 0.7,
      }));
    };

    const draw = (time: number) => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      context.clearRect(0, 0, width, height);

      const centerX = width * 0.72;
      const centerY = height * 0.36;
      context.save();
      context.translate(centerX, centerY);
      context.rotate(time * 0.00003);
      context.shadowColor = "rgba(0, 212, 255, 0.8)";
      context.shadowBlur = 10;
      context.strokeStyle = "rgba(0, 212, 255, 0.7)";
      context.lineWidth = 2;
      [90, 145, 205].forEach((radius, index) => {
        context.save();
        context.rotate(index * 0.9);
        context.scale(1, 0.38);
        context.beginPath();
        context.arc(0, 0, radius, 0, Math.PI * 2);
        context.stroke();
        context.restore();
      });
      context.shadowBlur = 0;
      context.restore();

      const glow = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, 34);
      glow.addColorStop(0, "rgba(6, 255, 165, 0.45)");
      glow.addColorStop(1, "rgba(6, 255, 165, 0)");
      context.fillStyle = glow;
      context.beginPath();
      context.arc(centerX, centerY, 34, 0, Math.PI * 2);
      context.fill();

      particles.forEach((particle) => {
        const drift = time * particle.speed + particle.phase;
        const x = particle.x + Math.sin(drift) * 18;
        const y = particle.y + Math.cos(drift * 0.8) * 12;
        context.beginPath();
        context.shadowColor = "rgba(6, 255, 165, 0.9)";
        context.shadowBlur = 8;
        context.fillStyle = "rgba(6, 255, 165, 0.95)";
        context.arc(x, y, particle.radius, 0, Math.PI * 2);
        context.fill();
        context.shadowBlur = 0;
      });

      animationFrame = window.requestAnimationFrame(draw);
    };

    resize();
    window.addEventListener("resize", resize);
    animationFrame = window.requestAnimationFrame(draw);

    return () => {
      window.cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <div aria-hidden="true" className="quantum-background pointer-events-none fixed inset-0 z-[2]">
      <div className="quantum-background__atom">
        <span className="quantum-background__nucleus" />
        <span className="quantum-background__orbit quantum-background__orbit--one" />
        <span className="quantum-background__orbit quantum-background__orbit--two" />
        <span className="quantum-background__orbit quantum-background__orbit--three" />
      </div>
      <canvas ref={canvasRef} className="absolute inset-0 h-full w-full opacity-100" />
    </div>
  );
}
