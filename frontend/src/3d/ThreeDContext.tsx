import React, { createContext, useContext, useState, useEffect } from 'react';

interface ThreeDContextType {
  is3DMode: boolean;
  set3DMode: (enabled: boolean) => void;
  toggle3DMode: () => void;
  isPitchMode: boolean;
  setPitchMode: (enabled: boolean) => void;
  togglePitchMode: () => void;
}

const ThreeDContext = createContext<ThreeDContextType>({
  is3DMode: true,
  set3DMode: () => {},
  toggle3DMode: () => {},
  isPitchMode: false,
  setPitchMode: () => {},
  togglePitchMode: () => {},
});

export const ThreeDProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Default to 3D Mode enabled
  const [is3DMode, setIs3DMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('recoverai_3d_mode');
    return saved !== null ? saved === 'true' : true;
  });

  // Pitch Mode for 5-minute video presentation
  const [isPitchMode, setIsPitchMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('recoverai_pitch_mode');
    return saved !== null ? saved === 'true' : false;
  });

  useEffect(() => {
    localStorage.setItem('recoverai_3d_mode', String(is3DMode));
    if (is3DMode) {
      document.documentElement.classList.add('mode-3d-active');
    } else {
      document.documentElement.classList.remove('mode-3d-active');
    }
  }, [is3DMode]);

  useEffect(() => {
    localStorage.setItem('recoverai_pitch_mode', String(isPitchMode));
    if (isPitchMode) {
      document.documentElement.classList.add('pitch-mode-active');
    } else {
      document.documentElement.classList.remove('pitch-mode-active');
    }
  }, [isPitchMode]);

  const toggle3DMode = () => setIs3DMode(prev => !prev);
  const set3DMode = (enabled: boolean) => setIs3DMode(enabled);

  const togglePitchMode = () => setIsPitchMode(prev => !prev);
  const setPitchMode = (enabled: boolean) => setIsPitchMode(enabled);

  return (
    <ThreeDContext.Provider value={{
      is3DMode, set3DMode, toggle3DMode,
      isPitchMode, setPitchMode, togglePitchMode
    }}>
      {children}
    </ThreeDContext.Provider>
  );
};

export const use3D = () => useContext(ThreeDContext);
