import React, { useState } from 'react';
import axios from 'axios';

const ScenarioUploader = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('http://localhost:8000/upload-scenario', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.message);
      onUpload();
    } catch (error) {
      setMessage(error.response.data.detail || 'Upload failed.');
    }
  };

  return (
    <div>
      <h2>Upload Scenario</h2>
      <input type="file" accept=".yaml, .yml" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
};

export default ScenarioUploader;
