import React, { useState } from 'react';
import axios from 'axios';

const SimulationControls = ({ onRun }) => {
  const [message, setMessage] = useState('');

  const handleRun = async () => {
    try {
      const response = await axios.post('http://localhost:8000/run-simulation');
      setMessage(response.data.message);
      onRun();
    } catch (error) {
      setMessage(error.response.data.detail || 'Simulation failed.');
    }
  };

  return (
    <div>
      <h2>Run Simulation</h2>
      <button onClick={handleRun}>Run Simulation</button>
      <p>{message}</p>
    </div>
  );
};

export default SimulationControls;
