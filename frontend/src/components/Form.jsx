import { useState } from 'react';

const Form = ({ onSubmit, loading }) => {
  const [topic, setTopic] = useState('');
  const [format, setFormat] = useState('ieee');
  const [length, setLength] = useState('short');
  const [outputType, setOutputType] = useState('summary');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim()) {
      setError('Topic is required');
      return;
    }
    if (topic.length > 100) {
      setError('Topic must be 100 characters or less');
      return;
    }
    setError('');
    onSubmit({ topic: topic.trim(), format, length, outputType });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-2xl font-bold mb-4 text-center">Generate Research Paper</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="mb-4">
        <label className="block text-gray-700">Research Topic</label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
          placeholder="e.g. AI in Healthcare"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Paper Format</label>
        <select value={format} onChange={(e) => setFormat(e.target.value)} className="w-full p-2 border border-gray-300 rounded">
          <option value="ieee">IEEE</option>
          <option value="springer">Springer</option>
          <option value="apa">APA</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Paper Length</label>
        <select value={length} onChange={(e) => setLength(e.target.value)} className="w-full p-2 border border-gray-300 rounded">
          <option value="short">Short (1-2 pages)</option>
          <option value="medium">Medium (3-5 pages)</option>
          <option value="long">Long (6+ pages)</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Output Type</label>
        <select value={outputType} onChange={(e) => setOutputType(e.target.value)} className="w-full p-2 border border-gray-300 rounded">
          <option value="summary">Summary</option>
          <option value="abstract">Abstract Only</option>
          <option value="full">Full Draft</option>
        </select>
      </div>
      <button type="submit" disabled={loading} className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400">
        {loading ? 'Generating...' : 'Generate Paper'}
      </button>
    </form>
  );
};

export default Form;
