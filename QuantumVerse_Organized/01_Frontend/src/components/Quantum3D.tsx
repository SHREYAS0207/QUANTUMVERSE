"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function Quantum3D() {
  const mountRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const mount = mountRef.current;

    if (!mount) {
      return;
    }

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2("#020817", 0.08);

    const camera = new THREE.PerspectiveCamera(
      48,
      mount.clientWidth / mount.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 18);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    renderer.setClearColor(0x000000, 0);
    mount.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    const blueLight = new THREE.PointLight(0x00d4ff, 1.8, 100);
    blueLight.position.set(9, 8, 14);

    const purpleLight = new THREE.PointLight(0xff5ef2, 1.1, 100);
    purpleLight.position.set(-10, -6, 12);

    scene.add(ambientLight, blueLight, purpleLight);

    const particleCount = 260;
    const basePositions = new Float32Array(particleCount * 3);
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i += 1) {
      const index = i * 3;
      const radius = 4.5 + Math.random() * 3.8;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      const x = radius * Math.sin(phi) * Math.cos(theta);
      const y = radius * Math.cos(phi);
      const z = radius * Math.sin(phi) * Math.sin(theta);

      basePositions[index] = x;
      basePositions[index + 1] = y;
      basePositions[index + 2] = z;

      const hue = 0.5 + Math.random() * 0.3;
      const color = new THREE.Color().setHSL(hue, 0.9, 0.6);

      colors[index] = color.r;
      colors[index + 1] = color.g;
      colors[index + 2] = color.b;
    }

    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      transparent: true,
      opacity: 0.92,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    const linePairCount = 180;
    const linePairs = Array.from({ length: linePairCount }, (_, index) => {
      const first = index % particleCount;
      const second = (first + 24 + Math.floor((index * 7) % (particleCount - 1))) % particleCount;
      return [first, second] as const;
    });

    const linePositions = new Float32Array(linePairs.length * 2 * 3);
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));

    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0xff5ef2,
      transparent: true,
      opacity: 0.35,
    });

    const entanglementLines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(entanglementLines);

    const updateParticlePositions = (time: number) => {
      for (let i = 0; i < particleCount; i += 1) {
        const index = i * 3;
        const wave = time * 0.00085 + i * 0.27;
        const orbit = 4.6 + Math.sin(time * 0.0004 + i * 0.53) * 1.2;

        const x = basePositions[index] + Math.sin(wave) * 0.9;
        const y = basePositions[index + 1] + Math.cos(wave * 1.3) * 0.75;
        const z = basePositions[index + 2] + Math.sin(wave * 0.8 + 1.5) * 0.8;

        const scale = orbit / Math.sqrt(x * x + y * y + z * z || 1);

        positions[index] = x * scale;
        positions[index + 1] = y * scale;
        positions[index + 2] = z * scale;
      }

      particleGeometry.attributes.position.needsUpdate = true;
      particleGeometry.computeBoundingSphere();

      const lineArray = lineGeometry.attributes.position.array as Float32Array;

      for (let i = 0; i < linePairs.length; i += 1) {
        const [startIndex, endIndex] = linePairs[i];
        const startOffset = startIndex * 3;
        const endOffset = endIndex * 3;
        const lineOffset = i * 6;

        lineArray[lineOffset] = positions[startOffset];
        lineArray[lineOffset + 1] = positions[startOffset + 1];
        lineArray[lineOffset + 2] = positions[startOffset + 2];

        lineArray[lineOffset + 3] = positions[endOffset];
        lineArray[lineOffset + 4] = positions[endOffset + 1];
        lineArray[lineOffset + 5] = positions[endOffset + 2];
      }

      lineGeometry.attributes.position.needsUpdate = true;
    };

    const handleResize = () => {
      if (!mount) {
        return;
      }

      camera.aspect = mount.clientWidth / mount.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mount.clientWidth, mount.clientHeight);
    };

    const animate = (time: number) => {
      updateParticlePositions(time);

      particles.rotation.y = time * 0.00012;
      particles.rotation.x = Math.sin(time * 0.00017) * 0.2;
      entanglementLines.rotation.y = time * 0.00008;

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    let animationFrameId = requestAnimationFrame(animate);

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);

      particleGeometry.dispose();
      particleMaterial.dispose();
      lineGeometry.dispose();
      lineMaterial.dispose();
      renderer.dispose();

      if (mount.contains(renderer.domElement)) {
        mount.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div
      ref={mountRef}
      className="quantum-3d-container"
      aria-label="Quantum 3D visualization"
    />
  );
}
