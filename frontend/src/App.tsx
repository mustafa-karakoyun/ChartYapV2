import { useState } from 'react';
import axios from 'axios';
import { Dropzone } from './components/Dropzone';
import { ChartGallery } from './components/ChartGallery';
import { UserChoiceDisplay } from './components/UserChoiceDisplay';
import { DataPreview } from './components/DataPreview';
import { SkeletonChart } from './components/SkeletonChart';
import { BarChart3, Loader2, Play, X } from 'lucide-react';

function App() {
  const [data, setData] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [stylePreview, setStylePreview] = useState<string | null>(null);

  // Staging state
  const [dataReady, setDataReady] = useState(false);
  const [styleReady, setStyleReady] = useState(false);
  const [fileToUpload, setFileToUpload] = useState<File | null>(null);
  const [styleToUpload, setStyleToUpload] = useState<File | null>(null);
  const [styleType, setStyleType] = useState<string>("bar");

  // Library Modal State
  const [showLibrary, setShowLibrary] = useState(false);

  // Hardcoded list for library view
  const CHART_CATEGORIES = [
    { name: "Distributions", types: ["Histogram", "Density Area", "Density Curve", "Boxplot", "Strip Plot", "Dot Plot", "CDF"] },
    { name: "Part-to-Whole", types: ["Pie Chart", "Donut Chart", "Radial Bar", "Treemap", "Sunburst"] },
    { name: "Correlation", types: ["Scatter Plot", "Bubble Chart", "Heatmap", "Connected Scatter", "Regression Line"] },
    { name: "Ranking", types: ["Bar Chart", "Sorted Bar", "Horizontal Bar", "Lollipop Chart", "Bump Chart"] },
    { name: "Evolution", types: ["Line Chart", "Area Chart", "Step Line", "Streamgraph", "Multi-Series Line"] },
    { name: "Flow & Maps", types: ["Sankey Diagram", "Chord Diagram", "Choropleth Map", "Symbol Map"] },
    { name: "Statistical", types: ["Error Bars", "Confidence Interval", "Violin Plot", "QQ Plot"] },
  ];

  const handleDataDrop = (files: File[]) => {
    if (files.length === 0) return;
    setFileToUpload(files[0]);
    setDataReady(true);
  };

  const handleStyleDrop = (files: File[]) => {
    if (files.length === 0) return;
    const file = files[0];
    setStylePreview(URL.createObjectURL(file));
    setStyleToUpload(file);
    setStyleReady(true);
  };

  const handleGenerate = async () => {
    if (!fileToUpload) return;
    setLoading(true);
    // Clear previous results to show skeleton
    setData([]);
    setRecommendations([]);

    try {
      // 1. Analyze Data
      const dataFormData = new FormData();
      dataFormData.append('file', fileToUpload);
      const dataRes = await axios.post('http://localhost:8000/analyze-data', dataFormData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setData(dataRes.data.preview);
      setRecommendations(dataRes.data.recommendations);

      // 2. Analyze Image
      if (styleReady && styleToUpload) {
        const imgFormData = new FormData();
        imgFormData.append('file', styleToUpload);
        try {
          const imgRes = await axios.post('http://localhost:8000/analyze-image', imgFormData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          if (imgRes.data.detected_type) {
            setStyleType(imgRes.data.detected_type);
          }
        } catch (err) {
          console.error("Image analysis failed", err);
        }
      }
    } catch (error) {
      alert("Error analyzing data. Ensure backend is running.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto font-['Inter'] relative">
      <header className="mb-12 border-b-4 border-black pb-4 flex justify-between items-end bg-[#F4F4F4]">
        <div>
          <h1 className="text-6xl font-black tracking-tighter uppercase leading-none">
            Chart<span className="text-[var(--swiss-red)]">Yap</span>
          </h1>
        </div>
        <div className="flex items-end gap-6">
          <button
            onClick={() => setShowLibrary(true)}
            className="text-sm font-bold uppercase tracking-widest hover:text-[var(--swiss-red)] underline decoration-2 underline-offset-4 mb-1"
          >
            View Chart Library
          </button>
          <BarChart3 size={48} />
        </div>
      </header>

      {/* LIBRARY MODAL */}
      {showLibrary && (
        <div className="fixed inset-0 z-[100] bg-black/95 text-white p-8 overflow-y-auto animate-in slide-in-from-bottom duration-300">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-12 border-b border-gray-800 pb-8">
              <h2 className="text-4xl font-black uppercase tracking-tighter">Supported Chart Library (45+)</h2>
              <button onClick={() => setShowLibrary(false)} className="p-2 hover:bg-white hover:text-black rounded-full transition-colors">
                <X size={32} />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
              {CHART_CATEGORIES.map((cat) => (
                <div key={cat.name} className="space-y-4">
                  <h3 className="text-xl font-bold text-[var(--swiss-red)] uppercase border-b border-gray-800 pb-2">{cat.name}</h3>
                  <ul className="space-y-2">
                    {cat.types.map(t => (
                      <li key={t} className="text-gray-400 hover:text-white transition-colors cursor-default text-lg flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-gray-600 rounded-full"></div>
                        {t}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div className="mt-16 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
              * Actual availability depends on your dataset columns.
            </div>
          </div>
        </div>
      )}

      <main>
        {/* DUAL UPLOAD GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <div className="space-y-4">
            <h2 className="swiss-title text-2xl uppercase border-l-4 border-[var(--swiss-red)] pl-4">
              01. Upload Data
            </h2>
            <p className="text-sm text-gray-600 mb-2">Supported: CSV, Excel. Drag & Drop.</p>
            <Dropzone
              onDrop={handleDataDrop}
              accept={{ 'text/csv': ['.csv'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] }}
              label={dataReady ? "Data Loaded" : "Drop Data File"}
              icon="data"
            />
          </div>

          <div className="space-y-4">
            <h2 className="swiss-title text-2xl uppercase border-l-4 border-black pl-4">
              02. Style Reference
            </h2>
            <p className="text-sm text-gray-600 mb-2">Optional: Upload an image to match style.</p>
            <Dropzone
              onDrop={handleStyleDrop}
              accept={{ 'image/*': ['.png', '.jpg', '.jpeg'] }}
              label="Style Image"
              icon="image"
              preview={stylePreview}
            />
          </div>
        </div>

        {/* ACTION BAR */}
        <div className="flex justify-center mb-16 flex-col items-center gap-8">
          <button
            onClick={handleGenerate}
            disabled={!dataReady || loading}
            className={`
              text-2xl font-black uppercase py-6 px-12 tracking-widest transition-all duration-300 active:scale-95
              flex items-center gap-4
              ${!dataReady || loading
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-black text-white hover:bg-[var(--swiss-red)] hover:scale-105 shadow-xl'}
            `}
          >
            {loading ? (
              <Loader2 className="animate-spin" size={32} />
            ) : (
              <Play fill="currentColor" size={32} />
            )}
            {loading ? "Analyzing..." : "Generate Visuals"}
          </button>

          {/* DATA PREVIEW */}
          {!loading && data.length > 0 && (
            <DataPreview data={data} />
          )}
        </div>

        {/* LOADING STATE - SKELETONS */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <SkeletonChart key={i} />
            ))}
          </div>
        )}

        {/* RESULTS */}
        {!loading && recommendations.length > 0 && (
          <section className="animate-fade-in duration-700 slide-in-from-bottom-8 fill-mode-forwards">
            {/* USER CHOICE VALIDATION */}
            {styleReady && (
              <UserChoiceDisplay
                userImage={stylePreview}
                recommendations={recommendations}
                data={data}
                detectedType={styleType}
              />
            )}

            <h2 className="swiss-title text-3xl uppercase mb-8 flex items-center gap-2 border-b-2 border-black pb-4">
              <div className="w-6 h-6 bg-[var(--swiss-red)]" />
              12 Concept Recommendations
            </h2>
            <ChartGallery recommendations={recommendations} data={data} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
