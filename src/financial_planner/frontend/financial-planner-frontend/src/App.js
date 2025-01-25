import React, { useState } from 'react';
import ScenarioUploader from './components/ScenarioUploader';
import SimulationControls from './components/SimulationControls';
import ResultsDisplay from './components/ResultsDisplay';

const App = () => {
  const [refresh, setRefresh] = useState(false);

  const handleUpload = () => {
    setRefresh(!refresh);
  };

  const handleRun = () => {
    setRefresh(!refresh);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Financial Planner</h1>
      <ScenarioUploader onUpload={handleUpload} />
      <SimulationControls onRun={handleRun} />
      <ResultsDisplay key={refresh} />
    </div>
  );
};

export default App;
