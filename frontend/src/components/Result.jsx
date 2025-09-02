const Result = ({ paper, error }) => {
  if (error) {
    return (
      <div className="bg-red-100 p-4 rounded-lg mt-4">
        <h3 className="text-red-800 font-bold">Error</h3>
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (!paper) return null;

  return (
    <div className="bg-green-100 p-4 rounded-lg mt-4">
      <h3 className="text-green-800 font-bold">Generated Paper</h3>
      <pre className="text-green-700 whitespace-pre-wrap">{paper}</pre>
    </div>
  );
};

export default Result;
