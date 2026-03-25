/**
 * @file App.tsx
 * @description Main application component for Primal Genesis Console
 * Entry point that renders the command-center dashboard
 */

import React from 'react';
import ConsoleDashboard from './components/ConsoleDashboard';
import './App.css';

/**
 * Main application component
 */
const App: React.FC = () => {
  return (
    <div className="App">
      <ConsoleDashboard />
    </div>
  );
};

export default App;
