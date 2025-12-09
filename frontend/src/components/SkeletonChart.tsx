import React from 'react';

export function SkeletonChart() {
    return (
        <div className="w-full p-4 bg-white border-2 border-gray-200 h-[300px] flex flex-col gap-4 animate-pulse">
            {/* Title Skeleton */}
            <div className="h-6 bg-gray-200 w-3/4 rounded-sm"></div>

            {/* Description Skeleton */}
            <div className="h-4 bg-gray-100 w-1/2 rounded-sm mb-4"></div>

            {/* Chart Area Skeleton */}
            <div className="flex-1 bg-gray-50 rounded-sm w-full flex items-end justify-center gap-2 pb-4 px-8">
                <div className="w-8 bg-gray-200 h-[40%]"></div>
                <div className="w-8 bg-gray-200 h-[70%]"></div>
                <div className="w-8 bg-gray-200 h-[50%]"></div>
                <div className="w-8 bg-gray-200 h-[80%]"></div>
                <div className="w-8 bg-gray-200 h-[60%]"></div>
            </div>
        </div>
    );
}
