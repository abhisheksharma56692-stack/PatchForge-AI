import React, { createContext, useContext, useState } from 'react';
import { soundManager } from '../utils/soundEffects';

const AudioContext = createContext(null);

export const AudioProvider = ({ children }) => {
  const [isPlayingAmbient, setIsPlayingAmbient] = useState(false);

  const toggleAmbient = () => {
    const nextState = !isPlayingAmbient;
    setIsPlayingAmbient(nextState);
    soundManager.toggleAmbient(nextState);
  };

  const playClick = () => {
    soundManager.playBubble();
  };

  const playRemediationSuccess = () => {
    soundManager.playRemediationChime();
  };

  return (
    <AudioContext.Provider
      value={{
        isPlayingAmbient,
        toggleAmbient,
        playClick,
        playRemediationSuccess,
      }}
    >
      {children}
    </AudioContext.Provider>
  );
};

export const useAudio = () => {
  const ctx = useContext(AudioContext);
  if (!ctx) throw new Error('useAudio must be used within AudioProvider');
  return ctx;
};

