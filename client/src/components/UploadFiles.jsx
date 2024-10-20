import React, { useState } from 'react';
import ReportDisplay from './ReportDisplay';

const UploadFiles = () => {
  const [uploadStatus, setUploadStatus] = useState('');
  const [report, setReport] = useState({});
  const [isUploading, setIsUploading] = useState(false); // Add a loading state

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    setIsUploading(true); // Set uploading to true

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }

      const data = await response.json();
      setReport(data);
      console.log(data);
      setUploadStatus('Upload successful!'); // Set success message

    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setIsUploading(false); // Reset uploading state regardless of success or failure
    }
  };

  return (
    <div className='flex flex-col gap-16'>
      <div className="my-10 mx-8 md:mx-0 h-screen md:flex md:flex-row flex flex-col items-center text-gray-900 bg-gray-100 bg-opacity-80 rounded-md">
        <div className="flex flex-col gap-4 md:w-3/5 w-11/12 h-full justify-center pl-16">
          <h2 className="font-semibold text-5xl md:w-11/12 w-full leading-tight opacity-90 pr-4">
            Securely Upload Your Infrastructure Documents with ShieldAI
          </h2>
          <p className="text-xl md:w-4/5 w-full leading-7 opacity-80 pr-4 md:pr-8">
            Seamlessly upload your security documents for AI-driven analysis and real-time risk assessment, ensuring your data stays protected and compliant.
          </p>
        </div>
        <div className="flex justify-center items-center w-full md:w-2/5 pb-16 md:pb-0">
          <div className="w-[400px] md:w-4/5 h-[200px] flex items-center justify-center border-2 border-dotted border-gray-900 rounded-xl">
            <form onSubmit={handleSubmit} className="flex flex-col gap-2 justify-center items-center">
              <input
                type="file"
                id="file-upload"
                name="file"
                className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
                required
              />
              <button 
                type="submit" 
                className={`mt-4 px-4 py-2 ${isUploading ? 'bg-gray-400' : 'bg-purple-600 bg-opacity-50'} text-white rounded-lg`} 
                disabled={isUploading} // Disable button when uploading
              >
                {isUploading ? 'Uploading...' : 'Upload'} {/* Change button text based on upload status */}
              </button>
            </form>
            {uploadStatus && <p className="mt-4 text-center text-red-600">{uploadStatus}</p>}
          </div>
        </div>
      </div>
      {Object.keys(report).length > 0 && ( // Only show report if it exists
        <div className="text-gray-900 bg-gray-100 bg-opacity-80 px-16 py-8 rounded-md h-auto mx-8 md:mx-0">
          <p className="font-medium opacity-80 pb-4">Report loaded successfully 📑</p>
          <ReportDisplay report={report} />
        </div>
      )}
    </div>
  );
};

export default UploadFiles;
