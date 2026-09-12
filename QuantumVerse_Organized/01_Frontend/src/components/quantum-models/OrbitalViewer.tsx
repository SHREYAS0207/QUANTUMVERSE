"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

interface OrbitalPoint {
  x: number;
  y: number;
  z: number;
  density: number;
}

interface OrbitalViewerProps {
  points?: OrbitalPoint[];
  title?: string;
}

export default function OrbitalViewer({
  points = [],
  title = "Hydrogen Orbital",
}: OrbitalViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;

    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color("#020208");

    const width = container.clientWidth;
    const height = container.clientHeight;

    const camera = new THREE.PerspectiveCamera(
      55,
      width / height,
      0.1,
      1000
    );

    camera.position.set(0, 0, 22);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);

    container.appendChild(renderer.domElement);

    const group = new THREE.Group();
    scene.add(group);

    // Nucleus
    const nucleusGeometry = new THREE.SphereGeometry(
      0.18,
      32,
      32
    );

    const nucleusMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
    });

    const nucleus = new THREE.Mesh(
      nucleusGeometry,
      nucleusMaterial
    );

    group.add(nucleus);

    // Probability cloud
    const positions = new Float32Array(points.length * 3);

    points.forEach((point, index) => {
      const offset = index * 3;

      positions[offset] = point.x;
      positions[offset + 1] = point.y;
      positions[offset + 2] = point.z;
    });

    const cloudGeometry = new THREE.BufferGeometry();

    cloudGeometry.setAttribute(
      "position",
      new THREE.BufferAttribute(positions, 3)
    );

    const cloudMaterial = new THREE.PointsMaterial({
      color: 0x00d9ff,
      size: 0.12,
      transparent: true,
      opacity: 0.65,
      sizeAttenuation: true,
      depthWrite: false,
    });

    const cloud = new THREE.Points(
      cloudGeometry,
      cloudMaterial
    );

    group.add(cloud);

    // Coordinate axes
    const axes = new THREE.AxesHelper(5);

if (Array.isArray(axes.material)) {
  axes.material.forEach((material) => {
    material.transparent = true;
    material.opacity = 0.15;
  });
} else {
  axes.material.transparent = true;
  axes.material.opacity = 0.15;
}

    group.add(axes);

    // Rotation
    let isDragging = false;
    let previousX = 0;
    let previousY = 0;

    const handlePointerDown = (event: PointerEvent) => {
      isDragging = true;
      previousX = event.clientX;
      previousY = event.clientY;
    };

    const handlePointerMove = (event: PointerEvent) => {
      if (!isDragging) return;

      const deltaX = event.clientX - previousX;
      const deltaY = event.clientY - previousY;

      group.rotation.y += deltaX * 0.008;
      group.rotation.x += deltaY * 0.008;

      previousX = event.clientX;
      previousY = event.clientY;
    };

    const handlePointerUp = () => {
      isDragging = false;
    };

    const handleWheel = (event: WheelEvent) => {
      event.preventDefault();

      camera.position.z += event.deltaY * 0.01;

      camera.position.z = THREE.MathUtils.clamp(
        camera.position.z,
        5,
        40
      );
    };

    renderer.domElement.addEventListener(
      "pointerdown",
      handlePointerDown
    );

    renderer.domElement.addEventListener(
      "pointermove",
      handlePointerMove
    );

    renderer.domElement.addEventListener(
      "pointerup",
      handlePointerUp
    );

    renderer.domElement.addEventListener(
      "pointerleave",
      handlePointerUp
    );

    renderer.domElement.addEventListener(
      "wheel",
      handleWheel,
      { passive: false }
    );

    // Resize
    const handleResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();

      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener("resize", handleResize);

    // Render loop
    let animationFrame: number;

    const animate = () => {
      renderer.render(scene, camera);
      animationFrame = requestAnimationFrame(animate);
    };

    animate();

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrame);

      window.removeEventListener(
        "resize",
        handleResize
      );

      renderer.domElement.removeEventListener(
        "pointerdown",
        handlePointerDown
      );

      renderer.domElement.removeEventListener(
        "pointermove",
        handlePointerMove
      );

      renderer.domElement.removeEventListener(
        "pointerup",
        handlePointerUp
      );

      renderer.domElement.removeEventListener(
        "pointerleave",
        handlePointerUp
      );

      renderer.domElement.removeEventListener(
        "wheel",
        handleWheel
      );

      cloudGeometry.dispose();
      cloudMaterial.dispose();

      nucleusGeometry.dispose();
      nucleusMaterial.dispose();

      renderer.dispose();

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [points]);

  return (
    <div
      ref={containerRef}
      className="relative h-[600px] w-full overflow-hidden rounded-2xl border border-white/10 bg-black"
    >
      <div className="pointer-events-none absolute left-4 top-4 z-10">
        <p className="text-sm font-medium text-white/90">
          {title}
        </p>

        <p className="text-xs text-white/50">
          Drag to rotate · Scroll to zoom
        </p>
      </div>
    </div>
  );
}