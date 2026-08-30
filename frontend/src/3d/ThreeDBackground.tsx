import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { use3D } from './ThreeDContext';

export const ThreeDBackground: React.FC = () => {
  const { is3DMode } = use3D();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!is3DMode || !containerRef.current) return;

    const container = containerRef.current;
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
      60,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.z = 80;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Particle Cloud (Cash flow / AI nodes)
    const particleCount = 180;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color('#6366f1'); // Indigo
    const color2 = new THREE.Color('#06b6d4'); // Cyan
    const color3 = new THREE.Color('#a855f7'); // Purple
    const colorChoices = [color1, color2, color3];

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 160;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 100;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 80;

      const chosenColor = colorChoices[Math.floor(Math.random() * colorChoices.length)];
      colors[i * 3] = chosenColor.r;
      colors[i * 3 + 1] = chosenColor.g;
      colors[i * 3 + 2] = chosenColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 2.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Floating 3D Geometric Polyhedra (Floating Assets / Invoices)
    const meshGroup = new THREE.Group();
    const geom1 = new THREE.IcosahedronGeometry(2.5, 0);
    const geom2 = new THREE.OctahedronGeometry(2, 0);
    const geom3 = new THREE.TetrahedronGeometry(2.2, 0);

    const wireMat1 = new THREE.MeshBasicMaterial({
      color: 0x6366f1,
      wireframe: true,
      transparent: true,
      opacity: 0.35,
    });
    const wireMat2 = new THREE.MeshBasicMaterial({
      color: 0x06b6d4,
      wireframe: true,
      transparent: true,
      opacity: 0.3,
    });

    for (let i = 0; i < 12; i++) {
      const g = i % 3 === 0 ? geom1 : i % 3 === 1 ? geom2 : geom3;
      const m = i % 2 === 0 ? wireMat1 : wireMat2;
      const mesh = new THREE.Mesh(g, m);

      mesh.position.set(
        (Math.random() - 0.5) * 140,
        (Math.random() - 0.5) * 90,
        (Math.random() - 0.5) * 50
      );
      mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
      meshGroup.add(mesh);
    }
    scene.add(meshGroup);

    // Mouse Interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      mouseX = (e.clientX - window.innerWidth / 2) * 0.05;
      mouseY = (e.clientY - window.innerHeight / 2) * 0.05;
    };

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', handleResize);

    // Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      targetX += (mouseX - targetX) * 0.05;
      targetY += (mouseY - targetY) * 0.05;

      particles.rotation.y += 0.001;
      particles.rotation.x += 0.0005;

      meshGroup.children.forEach((child, index) => {
        child.rotation.x += 0.004 + index * 0.001;
        child.rotation.y += 0.005;
      });

      camera.position.x = targetX * 0.4;
      camera.position.y = -targetY * 0.4;
      camera.lookAt(scene.position);

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, [is3DMode]);

  if (!is3DMode) return null;

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-0 opacity-80"
      style={{ overflow: 'hidden' }}
    />
  );
};
