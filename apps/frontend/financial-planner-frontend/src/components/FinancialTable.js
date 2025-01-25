// src/components/FinancialTable.js

import React from 'react';

const FinancialTable = ({ results }) => {
  return (
    <table
      border="1"
      style={{ marginBottom: '20px', borderCollapse: 'collapse', width: '100%' }}
    >
      <thead style={{ backgroundColor: '#f2f2f2' }}>
        <tr>
          <th>Year</th>
          <th>Total Income</th>
          <th>Total Taxes</th>
          <th>Total Mandatory Expenses</th>
          <th>Leftover</th>
          <th>Naive Discretionary</th>
          <th>Living Costs</th>
          <th>Housing Costs</th>
        </tr>
      </thead>
      <tbody>
        {results.map((result, index) => (
          <tr key={index}>
            <td>{result.year}</td>
            <td>${result.total_income.toLocaleString()}</td>
            <td>${result.total_taxes.toLocaleString()}</td>
            <td>${result.total_mandatory_expenses.toLocaleString()}</td>
            <td>${result.leftover.toLocaleString()}</td>
            <td>${result.naive_discretionary.toLocaleString()}</td>
            <td>${result.living_costs.toLocaleString()}</td>
            <td>${result.housing_costs.toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default FinancialTable;
