import React, { useState } from 'react';
import { VegaEmbed } from 'react-vega';
import { Maximize2, X, Info, Lightbulb } from 'lucide-react';

interface ChartRecommendation {
    id: string;
    title: string;
    description: string;
    type: string;
    encoding: any;
    transform?: any[];
    mark?: any;
}

interface ChartGalleryProps {
    recommendations: ChartRecommendation[];
    data: any[];
}

export const ChartGallery: React.FC<ChartGalleryProps> = ({ recommendations, data }) => {
    const [expandedChart, setExpandedChart] = useState<ChartRecommendation | null>(null);

    if (!recommendations.length) return null;

    const renderChart = (rec: ChartRecommendation, isExpanded: boolean = false) => {
        const spec = {
            $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
            // Remove title from internal spec in expanded mode to handle it externally
            title: isExpanded ? undefined : { text: rec.title, fontSize: 16, font: 'Inter', anchor: 'start' },
            description: rec.description,
            data: { values: data },
            mark: rec.type,
            encoding: rec.encoding,
            transform: rec.transform,
            width: "container",
            height: isExpanded ? 400 : 200,
            autosize: { type: "fit", contains: "padding" },
            config: {
                background: "white",
                view: { stroke: "transparent" },
                axis: {
                    domain: false,
                    grid: true,
                    gridColor: "#eee",
                    tickColor: "transparent",
                    labelFont: "Inter",
                    titleFont: "Inter",
                    titleFontWeight: "bold"
                },
                title: { font: "Inter", fontWeight: 900 }
            }
        };

        return (
            <VegaEmbed
                spec={spec as any}
                options={{ actions: isExpanded, renderer: 'svg' }}
                className="w-full h-full"
            />
        );
    };

    // Helper to extract field names for Sidebar
    const getFieldInfo = (rec: ChartRecommendation) => {
        const xField = rec.encoding?.x?.field || rec.encoding?.category?.field || "N/A";
        const yField = rec.encoding?.y?.field || rec.encoding?.theta?.field || "N/A";
        return { x: xField, y: yField };
    };

    return (
        <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12 pb-24">
                {recommendations.map((rec) => (
                    <div key={rec.id} className="swiss-card bg-white flex flex-col relative group transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 border border-transparent hover:border-gray-200">
                        <div className="mb-4 border-b border-gray-100 pb-2 pr-10">
                            <h3 className="swiss-title text-xl uppercase truncate text-gray-900 group-hover:text-[var(--swiss-red)] transition-colors">{rec.title}</h3>
                            <p className="text-xs text-gray-500 mt-1 truncate">{rec.description}</p>
                        </div>

                        {/* Maximize Button - Enhanced Interaction */}
                        <button
                            onClick={() => setExpandedChart(rec)}
                            className="absolute top-4 right-4 p-2 bg-gray-50 hover:bg-black hover:text-white transition-all rounded-full opacity-0 group-hover:opacity-100 shadow-sm hover:scale-110"
                            title="Expand & Download"
                        >
                            <Maximize2 size={16} />
                        </button>

                        <div className="flex-grow w-full h-[250px] overflow-hidden pointer-events-none opacity-90 group-hover:opacity-100 transition-opacity">
                            {renderChart(rec, false)}
                        </div>
                    </div>
                ))}
            </div>

            {/* FULL SCREEN MODAL WITH SIDEBAR */}
            {expandedChart && (
                <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-300">
                    <div className="bg-white w-full max-w-7xl h-[85vh] flex shadow-2xl rounded-sm overflow-hidden flex-col md:flex-row">

                        {/* CHART AREA (Left/Top) */}
                        <div className="flex-grow bg-gray-50 p-8 flex flex-col relative order-2 md:order-1 overflow-hidden">
                            <div className="absolute top-4 right-4 z-10 md:hidden">
                                <button onClick={() => setExpandedChart(null)} className="p-2 bg-black text-white rounded-full">
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="w-full h-full flex items-center justify-center bg-white border-2 border-gray-100 p-4 shadow-sm">
                                {renderChart(expandedChart, true)}
                            </div>

                            <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-400 uppercase tracking-widest">
                                <Info size={14} />
                                <span>Export options available via '...' menu</span>
                            </div>
                        </div>

                        {/* SIDEBAR (Right/Bottom) */}
                        <div className="w-full md:w-[350px] bg-white border-l border-gray-100 p-8 flex flex-col order-1 md:order-2 overflow-y-auto">
                            <div className="flex justify-between items-start mb-8">
                                <h2 className="text-3xl font-black uppercase tracking-tighter leading-none text-black">
                                    {expandedChart.title}
                                </h2>
                                <button
                                    onClick={() => setExpandedChart(null)}
                                    className="hidden md:block p-2 hover:bg-gray-100 rounded-full transition-colors"
                                >
                                    <X size={24} />
                                </button>
                            </div>

                            <div className="space-y-8">
                                <div>
                                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 border-b border-gray-100 pb-1">Description</h4>
                                    <p className="text-gray-700 leading-relaxed font-medium">
                                        {expandedChart.description}
                                    </p>
                                </div>

                                <div>
                                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 border-b border-gray-100 pb-1">Data Mapping</h4>
                                    <div className="grid grid-cols-1 gap-2 text-sm">
                                        <div className="flex justify-between items-center bg-gray-50 p-2 rounded">
                                            <span className="text-gray-500">X-Axis / Category</span>
                                            <span className="font-bold font-mono">{getFieldInfo(expandedChart).x}</span>
                                        </div>
                                        <div className="flex justify-between items-center bg-gray-50 p-2 rounded">
                                            <span className="text-gray-500">Y-Axis / Value</span>
                                            <span className="font-bold font-mono">{getFieldInfo(expandedChart).y}</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="bg-[var(--swiss-red)]/5 p-4 rounded-lg border border-[var(--swiss-red)]/10">
                                    <div className="flex items-center gap-2 mb-2 text-[var(--swiss-red)]">
                                        <Lightbulb size={18} />
                                        <h4 className="font-bold text-sm uppercase">Insight & Tips</h4>
                                    </div>
                                    <p className="text-xs text-gray-600 leading-relaxed">
                                        This chart is optimized for verifying distribution or identifying outliers.
                                        Ensure your data is clean for the best representation.
                                        <br /><br />
                                        Use the menu on the chart to "View Source" or "Save as SVG" for high-res embedding.
                                    </p>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            )}
        </>
    );
};
