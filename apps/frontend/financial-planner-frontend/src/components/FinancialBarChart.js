// src/components/FinancialBarChart.js

import React, { useMemo } from 'react';
import { Bar } from 'react-chartjs-2';
import { createChartOptions } from '../helpers/chartHelpers';

const FinancialBarChart = ({ results }) => {
  const barChartData = useMemo(() => ({
    labels: results.map((r) => r.year),
    datasets: [
      {
        label: 'Total Income',
        data: results.map((r) => r.total_income),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
      {
        label: 'Total Taxes',
        data: results.map((r) => r.total_taxes),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
      {
        label: 'Total Mandatory Expenses',
        data: results.map((r) => r.total_mandatory_expenses),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
      {
        label: 'Leftover',
        data: results.map((r) => r.leftover),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
      },
      {
        label: 'Naive Discretionary',
        data: results.map((r) => r.naive_discretionary),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      },
      {
        label: 'Living Costs',
        data: results.map((r) => r.living_costs),
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
      },
      {
        label: 'Housing Costs',
        data: results.map((r) => r.housing_costs),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
    ],
  }), [results]);

  const barChartOptions = useMemo(() => createChartOptions('Financial Simulation Results - Income & Expenses'), []);

  return <Bar data={barChartData} options={barChartOptions} />;
};

export default FinancialBarChart;
