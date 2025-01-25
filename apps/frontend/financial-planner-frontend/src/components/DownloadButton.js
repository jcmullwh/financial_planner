// src/components/DownloadButton.js

import React from 'react';
import { saveAs } from 'file-saver';

const DownloadButton = ({ results }) => {
  const downloadCSV = () => {
    const headers = [
      'Year',
      'Total Income',
      'Total Taxes',
      'Total Mandatory Expenses',
      'Leftover',
      'Naive Discretionary',
      'Living Costs',
      'Housing Costs',
    ];

    const rows = results.map((r) => [
      r.year,
      r.total_income,
      r.total_taxes,
      r.total_mandatory_expenses,
      r.leftover,
      r.naive_discretionary,
      r.living_costs,
      r.housing_costs,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers, ...rows].map((e) => e.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'financial_simulation_results.csv');
  };

  return (
    <button onClick={downloadCSV} style={{ marginBottom: '10px' }}>
      Download CSV Report
    </button>
  );
};

export default DownloadButton;
