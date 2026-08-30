import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { use3D } from './ThreeDContext';

interface AIOrb3DProps {
  isAnalyzing?: boolean;
  size?: number;
}

export const AIOrb3D: React.FC<AIOrb3DProps> = ({ isAnalyzing = false, size = 180 }) => {
  const { is3DMode } = use3D();
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!is3DMode || !canvasRef.current) return;

    const container = canvasRef.current;
    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(size, size);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Inner Glowing Core
    const coreGeom = new THREE.SphereGeometry(1.1, 32, 32);
    const coreMat = new THREE.MeshStandardMaterial({
      color: isAnalyzing ? 0x06b6d4 : 0x6366f1,
      emissive: isAnalyzing ? 0x0891b2 : 0x4f46e5,
      emissiveIntensity: isAnalyzing ? 1.2 : 0.6,
      roughness: 0.2,
      metalness: 0.8,
      wireframe: true,
    });
    const core = new THREE.Mesh(coreGeom, coreMat);
    scene.add(core);

    // Orbit Ring 1
    const ring1Geom = new THREE.TorusGeometry(1.6, 0.04, 16, 100);
    const ring1Mat = new THREE.MeshBasicMaterial({
      color: 0x06b6d4,
      transparent: true,
      opacity: 0.8,
    });
    const ring1 = new THREE.Mesh(ring1Geom, ring1Mat);
    scene.add(ring1);

    // Orbit Ring 2
    const ring2Geom = new THREE.TorusGeometry(1.9, 0.03, 16, 100);
    const ring2Mat = new THREE.MeshBasicMaterial({
      color: 0xa855f7,
      transparent: true,
      opacity: 0.7,
    });
    const ring2 = new THREE.Mesh(ring2Geom, ring2Mat);
    scene.add(ring2);

    // Lighting
    const pointLight = new THREE.PointLight(0xffffff, 2, 50);
    pointLight.position.set(2, 3, 4);
    scene.add(pointLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      const speedMult = isAnalyzing ? 2.8 : 1.0;

      core.rotation.y = elapsedTime * 0.4 * speedMult;
      core.rotation.x = elapsedTime * 0.2 * speedMult;

      ring1.rotation.x = elapsedTime * 0.8 * speedMult;
      ring1.rotation.y = elapsedTime * 0.5 * speedMult;

      ring2.rotation.y = -elapsedTime * 0.6 * speedMult;
      ring2.rotation.z = elapsedTime * 0.7 * speedMult;

      const scale = 1 + Math.sin(elapsedTime * (isAnalyzing ? 6 : 2)) * 0.06;
      core.scale.set(scale, scale, scale);

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      coreGeom.dispose();
      coreMat.dispose();
      ring1Geom.dispose();
      ring1Mat.dispose();
      ring2Geom.dispose();
      ring2Mat.dispose();
      renderer.dispose();
    };
  }, [is3DMode, isAnalyzing, size]);

  if (!is3DMode) {
    return (
      <div
        className={`rounded-full flex items-center justify-center ${
          isAnalyzing ? 'animate-spin bg-indigo-100 text-indigo-600' : 'bg-indigo-50 text-indigo-500'
        }`}
        style={{ width: size, height: size }}
      >
        <span className="text-2xl font-bold">AI</span>
      </div>
    );
  }

  return (
    <div
      ref={canvasRef}
      className="relative flex items-center justify-center cursor-pointer select-none"
      style={{ width: size, height: size }}
    />
  );
};
