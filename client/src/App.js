import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState('');
  const [imageURL, setImageURL] = useState('');

  const onFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const onUpload = async () => {
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result);
      setImageURL(`http://localhost:5000/${response.data.image_url}`);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div className="App">
        <h1>Parkinson's Disease Prediction</h1>
      <div className='container'>
        <input type="file" accept=".jpg, .jpeg, .png" onChange={onFileChange} />
        <button onClick={onUpload}>Upload</button>
        {imageURL && <img src={imageURL} alt="Uploaded" />}
        {result && <div className="result">{result}</div>}
      </div>
    </div>
  );
}

export default App;
