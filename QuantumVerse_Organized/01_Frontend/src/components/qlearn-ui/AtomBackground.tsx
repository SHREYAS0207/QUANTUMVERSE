"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function AtomBackground() {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      60,
      width / height,
      0.1,
      1000
    );

    camera.position.set(0, 18, 70);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
    });

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    container.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xff5500, 3.2, 140);
    scene.add(pointLight);

    const redLight = new THREE.PointLight(0xef4444, 2.2, 110);
    redLight.position.set(22, 12, 22);
    scene.add(redLight);

    const yellowLight = new THREE.PointLight(0xf59e0b, 2.2, 110);
    yellowLight.position.set(-22, -12, -22);
    scene.add(yellowLight);

    const nucleusGroup = new THREE.Group();
    scene.add(nucleusGroup);

    const nucleonCount = 20;
    const nucleonRadius = 1.3;
    const nucleonGeom = new THREE.SphereGeometry(
      nucleonRadius,
      20,
      20
    );

    const protonMat = new THREE.MeshPhongMaterial({
      color: 0xff3b00,
      emissive: 0xff2200,
      emissiveIntensity: 0.85,
      shininess: 90,
    });

    const neutronMat = new THREE.MeshPhongMaterial({
      color: 0xf59e0b,
      emissive: 0xb45309,
      emissiveIntensity: 0.65,
      shininess: 70,
    });

    for (let i = 0; i < nucleonCount; i++) {
      const isProton = i % 2 === 0;

      const mesh = new THREE.Mesh(
        nucleonGeom,
        isProton ? protonMat : neutronMat
      );

      const phi = Math.acos(-1 + (2 * i) / nucleonCount);
      const theta = Math.sqrt(nucleonCount * Math.PI) * phi;
      const r = 2.5 + (Math.random() * 0.7 - 0.35);

      mesh.position.set(
        r * Math.cos(theta) * Math.sin(phi),
        r * Math.sin(theta) * Math.sin(phi),
        r * Math.cos(phi)
      );

      nucleusGroup.add(mesh);
    }

    const haloGeom = new THREE.SphereGeometry(4.8, 28, 28);

    const haloMat = new THREE.MeshBasicMaterial({
      color: 0xff5500,
      transparent: true,
      opacity: 0.22,
      wireframe: true,
    });

    const haloMesh = new THREE.Mesh(haloGeom, haloMat);
    nucleusGroup.add(haloMesh);

    const orbitsGroup = new THREE.Group();
    scene.add(orbitsGroup);

    const orbitConfigs = [
      { r: 18, tilt: [0.35, 0.2, 0.8] as [number, number, number], speed: 1.8, color: 0xffffff, size: 0.8 },
      { r: 26, tilt: [-0.85, 0.5, -0.4] as [number, number, number], speed: 1.4, color: 0xfbbf24, size: 0.85 },
      { r: 33, tilt: [0.95, -0.7, 0.3] as [number, number, number], speed: 1.1, color: 0xff5500, size: 0.9 },
      { r: 40, tilt: [-0.2, 1.1, -0.9] as [number, number, number], speed: 0.85, color: 0xef4444, size: 0.95 },
      { r: 46, tilt: [0.6, 0.8, 1.4] as [number, number, number], speed: 0.65, color: 0xffffff, size: 0.8 },
    ];

    const orbitData = orbitConfigs.map((cfg) => {
      const curve = new THREE.EllipseCurve(
        0,
        0,
        cfg.r,
        cfg.r,
        0,
        Math.PI * 2,
        false,
        0
      );

      const pathGeom = new THREE.BufferGeometry().setFromPoints(
        curve
          .getPoints(100)
          .map((p) => new THREE.Vector3(p.x, 0, p.y))
      );

      const ring = new THREE.LineLoop(
        pathGeom,
        new THREE.LineBasicMaterial({
          color: cfg.color,
          transparent: true,
          opacity: 0.32,
        })
      );

      ring.rotation.set(cfg.tilt[0], cfg.tilt[1], cfg.tilt[2]);
      orbitsGroup.add(ring);

      const electronMesh = new THREE.Mesh(
        new THREE.SphereGeometry(cfg.size, 14, 14),
        new THREE.MeshPhongMaterial({
          color: cfg.color,
          emissive: cfg.color,
          emissiveIntensity: 1,
          shininess: 100,
        })
      );

      const auraMesh = new THREE.Mesh(
        new THREE.SphereGeometry(cfg.size * 1.8, 10, 10),
        new THREE.MeshBasicMaterial({
          color: cfg.color,
          transparent: true,
          opacity: 0.35,
        })
      );

      electronMesh.add(auraMesh);
      orbitsGroup.add(electronMesh);

      return {
        cfg,
        mesh: electronMesh,
        angle: Math.random() * Math.PI * 2,
      };
    });

    const particleCount = 200;
    const particleGeom = new THREE.BufferGeometry();

    const particlePos = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const colorChoices = [
      new THREE.Color(0xff5500),
      new THREE.Color(0xef4444),
      new THREE.Color(0xf59e0b),
      new THREE.Color(0xffffff),
    ];

    for (let i = 0; i < particleCount; i++) {
      const rad = 14 + Math.random() * 52;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      particlePos[i * 3] =
        rad * Math.sin(phi) * Math.cos(theta);

      particlePos[i * 3 + 1] =
        rad * Math.sin(phi) * Math.sin(theta);

      particlePos[i * 3 + 2] =
        rad * Math.cos(phi);

      const color =
        colorChoices[
          Math.floor(Math.random() * colorChoices.length)
        ];

      particleColors[i * 3] = color.r;
      particleColors[i * 3 + 1] = color.g;
      particleColors[i * 3 + 2] = color.b;
    }

    particleGeom.setAttribute(
      "position",
      new THREE.BufferAttribute(particlePos, 3)
    );

    particleGeom.setAttribute(
      "color",
      new THREE.BufferAttribute(particleColors, 3)
    );

    const particles = new THREE.Points(
      particleGeom,
      new THREE.PointsMaterial({
        size: 0.85,
        vertexColors: true,
        transparent: true,
        opacity: 0.55,
      })
    );

    scene.add(particles);

    const clock = new THREE.Clock();
    let animationFrame = 0;

    const animate = () => {
      animationFrame = requestAnimationFrame(animate);

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      nucleusGroup.rotation.y += 0.75 * delta;
      nucleusGroup.rotation.x += 0.35 * delta;

      haloMesh.rotation.z += 0.5 * delta;

      const pulse = 1 + 0.08 * Math.sin(time * 3);
      haloMesh.scale.set(pulse, pulse, pulse);

      orbitsGroup.rotation.y = time * 0.12;
      orbitsGroup.rotation.x = Math.sin(time * 0.08) * 0.14;

      particles.rotation.y = -time * 0.035;

      orbitData.forEach((item) => {
        item.angle += item.cfg.speed * delta;

        const vector = new THREE.Vector3(
          item.cfg.r * Math.cos(item.angle),
          0,
          item.cfg.r * Math.sin(item.angle)
        );

        vector.applyEuler(
          new THREE.Euler(item.cfg.tilt[0], item.cfg.tilt[1], item.cfg.tilt[2], "XYZ")
        );

        item.mesh.position.copy(vector);
      });

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      const w = container.clientWidth || window.innerWidth;
      const h = container.clientHeight || window.innerHeight;

      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", handleResize);

      particleGeom.dispose();
      nucleonGeom.dispose();
      protonMat.dispose();
      neutronMat.dispose();
      haloGeom.dispose();
      haloMat.dispose();

      renderer.dispose();

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div
      ref={mountRef}
      className="fixed inset-0 z-0 h-full w-full pointer-events-none opacity-40"
    />
  );
}
