import React, { useRef, useState } from 'react';
import { use3D } from './ThreeDContext';

interface Card3DProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  intensity?: number;
  className?: string;
  glowColor?: string;
  depth?: boolean;
}

export const Card3D: React.FC<Card3DProps> = ({
  children,
  intensity = 15,
  className = '',
  glowColor = 'rgba(99, 102, 241, 0.25)',
  depth = true,
  ...props
}) => {
  const { is3DMode } = use3D();
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });
  const [glare, setGlare] = useState({ x: 50, y: 50, opacity: 0 });

  if (!is3DMode) {
    return (
      <div className={`bg-white rounded-xl border border-gray-100 p-5 ${className}`} {...props}>
        {children}
      </div>
    );
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -intensity;
    const rotateY = ((x - centerX) / centerX) * intensity;

    setRotation({ x: rotateX, y: rotateY });
    setGlare({
      x: (x / rect.width) * 100,
      y: (y / rect.height) * 100,
      opacity: 0.25,
    });
  };

  const handleMouseLeave = () => {
    setRotation({ x: 0, y: 0 });
    setGlare(prev => ({ ...prev, opacity: 0 }));
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${rotation.x}deg) rotateY(${rotation.y}deg) scale3d(1.01, 1.01, 1.01)`,
        transition: rotation.x === 0 ? 'transform 0.5s ease, box-shadow 0.5s ease' : 'none',
      }}
      className={`relative overflow-hidden card-3d-glass rounded-2xl p-5 ${className}`}
      {...props}
    >
      {/* 3D Dynamic Specular Light Glare */}
      <div
        className="pointer-events-none absolute inset-0 transition-opacity duration-300 z-10"
        style={{
          background: `radial-gradient(circle at ${glare.x}% ${glare.y}%, ${glowColor}, transparent 60%)`,
          opacity: glare.opacity,
        }}
      />
      {/* Depth transformed content */}
      <div style={{ transform: depth ? 'translateZ(20px)' : 'none', transformStyle: 'preserve-3d' }}>
        {children}
      </div>
    </div>
  );
};
