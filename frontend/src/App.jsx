import { useState } from 'react';
import Form from './components/Form';
import Spinner from './components/Spinner';
import Result from './components/Result';

function App() {
  const [loading, setLoading] = useState(false);
  const [paper, setPaper] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (data) => {
    setLoading(true);
    setError('');
    setPaper('');
    try {
      const response = await fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (result.success) {
        setPaper(result.paper);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Request failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Form onSubmit={handleSubmit} loading={loading} />
        {loading && <Spinner />}
        <Result paper={paper} error={error} />
      </div>
    </div>
  );
}

export default App;
