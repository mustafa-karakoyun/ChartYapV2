import React from 'react';
import { Table } from 'lucide-react';

interface DataPreviewProps {
    data: any[];
}

export function DataPreview({ data }: DataPreviewProps) {
    if (!data || data.length === 0) return null;

    // Get headers from the first object
    const headers = Object.keys(data[0]);
    const previewData = data.slice(0, 5);

    return (
        <div className="w-full max-w-2xl mx-auto mt-8 bg-white border-2 border-black p-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] animate-in fade-in slide-in-from-top-4 duration-500">
            <div className="flex items-center gap-2 mb-4 border-b-2 border-gray-100 pb-2">
                <Table className="text-[var(--swiss-red)]" size={20} />
                <h3 className="font-bold uppercase tracking-widest text-sm text-gray-800">Data Preview (First 5 Rows)</h3>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                    <thead className="text-xs text-gray-500 uppercase bg-gray-50">
                        <tr>
                            {headers.map((header) => (
                                <th key={header} scope="col" className="px-4 py-3 font-black text-black">
                                    {header}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {previewData.map((row, index) => (
                            <tr key={index} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                                {headers.map((header) => (
                                    <td key={`${index}-${header}`} className="px-4 py-2 font-medium text-gray-700">
                                        {row[header]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="mt-2 text-xs text-gray-400 text-center font-mono">
                Showing {previewData.length} of {data.length} rows
            </div>
        </div>
    );
}
