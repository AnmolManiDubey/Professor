import { useState } from "react";

export default function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const res = await fetch(`https://professor-backend.vercel.app/teach?topic=${encodeURIComponent(topic)}`);
      if (!res.ok) {
        throw new Error("Failed to fetch explanation");
      }
      const result = await res.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Professor AI - Teach</h1>

      <form onSubmit={handleSubmit} className="mb-6">
        <input
          type="text"
          placeholder="Enter topic (e.g. Linear Regression)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="border p-2 rounded w-full mb-2"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Get Explanation"}
        </button>
      </form>

      {error && <p className="text-red-600 mb-4">Error: {error}</p>}

      {data && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">{data.topic}</h2>
<div
  className="prose prose-sm max-w-none mb-4"
  dangerouslySetInnerHTML={{ __html: data.explanation }}
></div>

          {data.images && data.images.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {data.images.map((img, idx) => (
                <a key={idx} href={img.link} target="_blank" rel="noopener noreferrer" className="block">
                  <img src={img.thumbnail} alt={img.title} className="rounded shadow" />
                  <p className="text-sm mt-1">{img.title}</p>
                </a>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
