import React from 'react';
import { use3D } from './ThreeDContext';
import { Box, Layers } from 'lucide-react';

export const ThreeDToggle: React.FC = () => {
  const { is3DMode, toggle3DMode } = use3D();

  return (
    <button
      onClick={toggle3DMode}
      title={is3DMode ? "Switch to Classic 2D View" : "Enable 3D Hologram View"}
      className={`relative flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-300 ${
        is3DMode
          ? 'bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 text-white shadow-lg shadow-indigo-500/25 border border-white/30 scale-105'
          : 'bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-200'
      }`}
    >
      {is3DMode ? (
        <>
          <Box className="w-4 h-4 animate-spin" style={{ animationDuration: '6s' }} />
          <span>3D Hologram View</span>
          <span className="w-2 h-2 rounded-full bg-cyan-300 animate-ping" />
        </>
      ) : (
        <>
          <Layers className="w-4 h-4 text-gray-500" />
          <span>2D Mode</span>
        </>
      )}
    </button>
  );
};
