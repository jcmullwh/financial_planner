// src/components/ResultsDisplay.js

import React from 'react';
import FinancialTable from './FinancialTable';
import FinancialBarChart from './FinancialBarChart';
import FinancialLineChart from './FinancialLineChart';
import DownloadButton from './DownloadButton';
import useSimulationResults from '../hooks/useSimulationResults';

const ResultsDisplay = () => {
  const { results, error, loading } = useSimulationResults();

  if (loading) {
    return (
      <div>
        <h2>Simulation Results</h2>
        <p>Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h2>Simulation Results</h2>
        <p style={{ color: 'red' }}>{error}</p>
      </div>
    );
  }

  if (!results.length) {
    return (
      <div>
        <h2>Simulation Results</h2>
        <p>No results available. Please run the simulation.</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h2>Simulation Results</h2>
      <DownloadButton results={results} />
      <FinancialTable results={results} />
      <FinancialBarChart results={results} />
      <FinancialLineChart results={results} />
    </div>
  );
};

export default ResultsDisplay;
