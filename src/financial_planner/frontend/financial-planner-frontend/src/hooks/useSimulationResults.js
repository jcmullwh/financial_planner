// src/hooks/useSimulationResults.js

import { useEffect, useState } from 'react';
import axios from 'axios';

const useSimulationResults = () => {
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchResults = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/get-results');
      setResults(response.data.results || []);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch results.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  return { results, error, loading };
};

export default useSimulationResults;
