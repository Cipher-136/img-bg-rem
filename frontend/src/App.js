import React, { useState } from 'react'; 
import axios from 'axios';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [resultImage, setResultImage] = useState(null);

  const handleImageChange = (event) => {
    setSelectedImage(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      alert("Please select an image to upload");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await axios.post('http://127.0.0.1:5000/remove-bg', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',  // Specify responseType as blob to handle binary data
      });

      // Convert the received binary data (blob) into a URL
      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl); // Set the processed image URL

    } catch (error) {
      console.error("Error uploading image: ", error);
      alert("Error uploading image");
    }
  };

  return (
    <div className="App">
      <h1>Background Remover</h1>
      <input type="file" onChange={handleImageChange} />
      <button onClick={handleUpload}>Upload and Remove Background</button>

      <div className="image-container">
        {selectedImage && (
          <div className="image">
            <h3>Original Image</h3>
            <img src={URL.createObjectURL(selectedImage)} alt="Original" />
          </div>
        )}
        {resultImage && (
          <div className="image">
            <h3>Processed Image</h3>
            <img src={resultImage} alt="Processed" />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
