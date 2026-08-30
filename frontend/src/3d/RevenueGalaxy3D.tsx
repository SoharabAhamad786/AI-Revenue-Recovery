import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { use3D } from './ThreeDContext';
import { Sparkles, Eye } from 'lucide-react';

interface RevenueGalaxy3DProps {
  stats?: {
    total_outstanding?: number;
    overdue_amount?: number;
    recovered_amount?: number;
    recovery_rate?: number;
  };
}

export const RevenueGalaxy3D: React.FC<RevenueGalaxy3DProps> = ({ stats }) => {
  const { is3DMode } = use3D();
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  useEffect(() => {
    if (!is3DMode || !containerRef.current) return;

    const container = containerRef.current;
    const scene = new THREE.Scene();

    const width = container.clientWidth || 500;
    const height = 320;

    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 15, 45);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Central Core: Total Pipeline
    const coreGeom = new THREE.IcosahedronGeometry(4, 1);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0x6366f1,
      emissive: 0x4f46e5,
      emissiveIntensity: 0.8,
      wireframe: true,
    });
    const coreMesh = new THREE.Mesh(coreGeom, coreMat);
    scene.add(coreMesh);

    // Orbiting Invoice Clusters
    const clusterGroup = new THREE.Group();
    scene.add(clusterGroup);

    // Categories of nodes:
    // Green: Recovered ($168k)
    // Red: High-Risk Overdue
    // Cyan: In Recovery / Reminder Sent
    // Amber: Pending Verification
    const nodeConfigs = [
      { name: 'Recovered Revenue', count: 18, color: 0x10b981, radius: 14, speed: 0.008, yOff: 2 },
      { name: 'Active AI Reminders', count: 12, color: 0x06b6d4, radius: 22, speed: -0.006, yOff: -3 },
      { name: 'High-Risk Escalations', count: 8, color: 0xf43f5e, radius: 28, speed: 0.005, yOff: 4 },
      { name: 'Pending Review', count: 10, color: 0xf59e0b, radius: 18, speed: -0.007, yOff: 0 },
    ];

    const sphereGeom = new THREE.SphereGeometry(0.7, 16, 16);

    nodeConfigs.forEach((cfg) => {
      const mat = new THREE.MeshStandardMaterial({
        color: cfg.color,
        emissive: cfg.color,
        emissiveIntensity: 0.6,
        roughness: 0.3,
      });

      for (let i = 0; i < cfg.count; i++) {
        const angle = (i / cfg.count) * Math.PI * 2 + Math.random() * 0.4;
        const mesh = new THREE.Mesh(sphereGeom, mat);
        const r = cfg.radius + (Math.random() - 0.5) * 3;
        mesh.position.set(
          Math.cos(angle) * r,
          cfg.yOff + (Math.random() - 0.5) * 4,
          Math.sin(angle) * r
        );
        mesh.userData = { config: cfg, angle, r, speed: cfg.speed, yBase: mesh.position.y };
        clusterGroup.add(mesh);
      }
    });

    // Orbit Rings
    [14, 18, 22, 28].forEach((r, idx) => {
      const ringGeom = new THREE.RingGeometry(r - 0.1, r + 0.1, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: idx % 2 === 0 ? 0x6366f1 : 0x06b6d4,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.25,
      });
      const ring = new THREE.Mesh(ringGeom, ringMat);
      ring.rotation.x = Math.PI / 2;
      scene.add(ring);
    });

    // Lights
    const pLight = new THREE.PointLight(0xffffff, 2, 100);
    pLight.position.set(10, 20, 20);
    scene.add(pLight);
    scene.add(new THREE.AmbientLight(0xffffff, 0.7));

    // Mouse Drag Rotation
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let rotX = 0.3;
    let rotY = 0;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;
      rotY += deltaX * 0.005;
      rotX += deltaY * 0.005;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    container.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    let animId: number;
    const animate = () => {
      animId = requestAnimationFrame(animate);

      if (!isDragging) {
        rotY += 0.003;
      }

      coreMesh.rotation.y += 0.01;
      coreMesh.rotation.x += 0.005;

      clusterGroup.rotation.y = rotY;
      clusterGroup.rotation.x = rotX;

      clusterGroup.children.forEach((child) => {
        const u = child.userData;
        if (u && u.angle !== undefined) {
          u.angle += u.speed;
          child.position.x = Math.cos(u.angle) * u.r;
          child.position.z = Math.sin(u.angle) * u.r;
        }
      });

      camera.lookAt(0, 0, 0);
      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animId);
      container.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      coreGeom.dispose();
      coreMat.dispose();
      sphereGeom.dispose();
      renderer.dispose();
    };
  }, [is3DMode]);

  if (!is3DMode) return null;

  return (
    <div className="card-3d-glass rounded-2xl p-5 border border-indigo-100/60 overflow-hidden relative">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-indigo-500 animate-pulse" />
          <h3 className="font-semibold text-gray-900 text-sm">3D Revenue Recovery Galaxy</h3>
        </div>
        <span className="text-xs bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-full font-medium flex items-center gap-1 border border-indigo-100">
          <Eye className="w-3.5 h-3.5" /> Interactive 3D Orbit (Drag to rotate)
        </span>
      </div>

      <div className="relative w-full h-[280px] flex items-center justify-center cursor-grab active:cursor-grabbing" ref={containerRef}>
        {/* Hologram HUD overlay */}
        <div className="absolute top-2 left-2 pointer-events-none space-y-1 text-[11px] font-mono bg-white/75 backdrop-blur-md p-2.5 rounded-lg border border-gray-200/60 shadow-sm z-20">
          <div className="text-indigo-600 font-semibold flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-ping" />
            AI Pipeline Cluster Active
          </div>
          <div className="text-gray-500">Recovery Nodes: <span className="text-gray-900 font-bold">48 Invoices</span></div>
          <div className="flex items-center gap-3 pt-1 text-[10px]">
            <span className="text-emerald-600 flex items-center gap-1">● Recovered</span>
            <span className="text-cyan-600 flex items-center gap-1">● In Recovery</span>
            <span className="text-rose-600 flex items-center gap-1">● High Risk</span>
          </div>
        </div>
      </div>
    </div>
  );
};
