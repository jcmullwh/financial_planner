// src/components/FinancialLineChart.js

import React, { useMemo } from 'react';
import { Line } from 'react-chartjs-2';
import { createChartOptions } from '../helpers/chartHelpers';

const FinancialLineChart = ({ results }) => {
  const lineChartData = useMemo(() => ({
    labels: results.map((r) => r.year),
    datasets: [
      {
        label: 'Living Costs',
        data: results.map((r) => r.living_costs),
        borderColor: 'rgba(255, 159, 64, 1)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        fill: true,
      },
      {
        label: 'Housing Costs',
        data: results.map((r) => r.housing_costs),
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
      },
    ],
  }), [results]);

  const lineChartOptions = useMemo(() => createChartOptions('Financial Simulation Results - Living & Housing Costs'), []);

  return <Line data={lineChartData} options={lineChartOptions} />;
};

export default FinancialLineChart;
