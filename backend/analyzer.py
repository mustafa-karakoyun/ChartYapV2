import pandas as pd
from typing import List, Dict, Any
import itertools
import random

def analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes the dataframe and generates 12 chart recommendations 
    from a pool of ~45 capabilities.
    """
    analysis = {
        "columns": {},
        "shape": df.shape,
        "recommendations": []
    }
    
    numeric_cols = []
    categorical_cols = []
    datetime_cols = []
    
    for col in df.columns:
        dtype = df[col].dtype
        unique_count = df[col].nunique()
        
        col_type = "unknown"
        if pd.api.types.is_numeric_dtype(dtype):
            col_type = "numeric"
            numeric_cols.append(col)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            col_type = "datetime"
            datetime_cols.append(col)
        else:
            col_type = "categorical"
            categorical_cols.append(col)
            
        analysis["columns"][col] = {
            "type": col_type,
            "unique_values": unique_count
        }

    # --- 45 CHART CAPABILITY REGISTRY ---
    # We define chart "templates" that check for data requirements
    
    # Helper to create spec
    def create_rec(id, title, desc, type_mark, encoding, transform=None):
        return {
            "id": id,
            "title": title,
            "description": desc,
            "type": type_mark,
            "encoding": encoding,
            "transform": transform
        }

    possible_charts = []

    # --- 1. SINGLE NUMERIC (DISTRIBUTIONS) ---
    for col in numeric_cols[:]:
        # 1. Histogram
        possible_charts.append(create_rec(f"hist_{col}", f"Histogram: {col}", "Frequency distribution.", "bar", 
            {"x": {"field": col, "bin": True}, "y": {"aggregate": "count"}}))
        # 2. Density Area
        possible_charts.append(create_rec(f"dens_area_{col}", f"Density Area: {col}", "Smoothed distribution.", "area", 
            {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "density", "type": "quantitative"}}, transform=[{"density": col}]))
        # 3. Density Line
        possible_charts.append(create_rec(f"dens_line_{col}", f"Density Curve: {col}", "Outline of distribution.", "line", 
            {"x": {"field": "value", "type": "quantitative"}, "y": {"field": "density", "type": "quantitative"}}, transform=[{"density": col}]))
        # 4. Boxplot
        possible_charts.append(create_rec(f"box_{col}", f"Boxplot: {col}", "Median and quartiles.", "boxplot", 
            {"y": {"field": col, "type": "quantitative"}}))
        # 5. Review (Violin-ish with tick)
        possible_charts.append(create_rec(f"strip_{col}", f"Strip Plot: {col}", "Individual data points.", "tick", 
            {"x": {"field": col, "type": "quantitative"}}))
        # 6. ECDF (Cumulative) - approximation via window
        possible_charts.append(create_rec(f"cdf_{col}", f"CDF: {col}", "Cumulative density.", "line",
            {"x": {"field": col, "type": "quantitative"}, "y": {"aggregate": "count", "type": "quantitative", "stack": "normalize"}}, 
            transform=[{"window": [{"op": "count", "as": "count"}], "sort": [{"field": col}]}])) # simplified
        # 7. Dot Plot
        possible_charts.append(create_rec(f"dot_{col}", f"Dot Plot: {col}", "Binned dot frequency.", "circle",
            {"x": {"field": col, "bin": True}, "y": {"aggregate": "count"}}))

    # --- 2. SINGLE CATEGORICAL ---
    for col in categorical_cols[:]:
        # Check if unique (Ratio > 0.9 means mostly unique, like IDs)
        is_unique_id = False
        if len(df) > 0 and (df[col].nunique() / len(df)) > 0.9:
            is_unique_id = True
        
        # If we have a numeric column, prioritize Sum/Mean over Count for Bar Charts
        if numeric_cols:
            val_col = numeric_cols[0]
            # 8. Unsorted Bar (Sum)
            possible_charts.append(create_rec(f"bar_sum_{col}_{val_col}", f"Bar Chart: {col}", f"Sum of {val_col}", "bar",
                {"x": {"field": col, "type": "nominal"}, "y": {"field": val_col, "type": "quantitative", "aggregate": "sum"}}))
            # 9. Sorted Bar (Sum) - only if not unique because unique means no meaningful sort difference usually, but sort by value is distinct
            possible_charts.append(create_rec(f"bar_sort_sum_{col}_{val_col}", f"Sorted Bar: {col}", f"Ordered by {val_col}", "bar",
                {"x": {"field": col, "type": "nominal", "sort": "-y"}, "y": {"field": val_col, "type": "quantitative", "aggregate": "sum"}}))
            
            # 11. Pie Chart (Sum)
            possible_charts.append(create_rec(f"pie_{col}", f"Pie: {col}", f"Share of {val_col}", "arc",
                {"theta": {"aggregate": "sum", "field": val_col}, "color": {"field": col, "type": "nominal"}}))
            # 12. Donut Chart (Sum)
            possible_charts.append(create_rec(f"donut_{col}", f"Donut: {col}", "Ring chart.", "arc",
                {"theta": {"aggregate": "sum", "field": val_col}, "color": {"field": col, "type": "nominal"}, "innerRadius": 50}))

        # Only add Count-based charts if it's NOT a unique ID column (otherwise every bar is size 1)
        if not is_unique_id:
            # 10. Unsorted Bar (Count)
            possible_charts.append(create_rec(f"bar_cat_{col}", f"Bar Count: {col}", "Category frequency.", "bar",
                {"x": {"field": col, "type": "nominal"}, "y": {"aggregate": "count"}}))
            # 11. Horizontal Bar (Count)
            possible_charts.append(create_rec(f"hbar_cat_{col}", f"Horiz Bar: {col}", "Category frequency.", "bar",
                {"y": {"field": col, "type": "nominal"}, "x": {"aggregate": "count"}}))
        
        # 13. Lollipop (Bar with width 1 - simplified)
        if numeric_cols:
             val_col = numeric_cols[0]
             possible_charts.append(create_rec(f"lollipop_{col}", f"Lollipop: {col}", f"Value of {val_col}", "bar",
                {"x": {"field": col, "type": "nominal"}, "y": {"field": val_col, "aggregate": "sum"}, "width": 2}))

    # --- 3. TWO NUMERIC ---
    pairs_num = list(itertools.combinations(numeric_cols, 2))
    for x, y in pairs_num:
        # 14. Scatter
        possible_charts.append(create_rec(f"scatter_{x}_{y}", f"Scatter: {x} vs {y}", "Correlation.", "point",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}}))
        # 15. Bubble (using size for one variable, but here mapping x/y, mock size)
        possible_charts.append(create_rec(f"bubble_{x}_{y}", f"Bubble: {x} vs {y}", "Weighted points.", "circle",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "size": {"field": y, "type": "quantitative"}}))
        # 16. Heatmap (Binned)
        possible_charts.append(create_rec(f"heat_{x}_{y}", f"Heatmap: {x} vs {y}", "2D Histogram.", "rect",
            {"x": {"field": x, "bin": True}, "y": {"field": y, "bin": True}, "color": {"aggregate": "count"}}))
        # 17. Connected Scatter
        possible_charts.append(create_rec(f"conn_scat_{x}_{y}", f"Connected: {x} vs {y}", "Path of values.", "line",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "order": {"field": x}}))
        # 18. Line Regression (Basic Line)
        possible_charts.append(create_rec(f"line_reg_{x}_{y}", f"Line: {x} vs {y}", "Trend line.", "line",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}}))
        # 19. Area Step
        possible_charts.append(create_rec(f"area_step_{x}_{y}", f"Step Area: {x} vs {y}", "Stepped magnitude.", "area",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "interpolate": "step"}))

    # --- 4. NUMERIC + CATEGORICAL ---
    pairs_mix = list(itertools.product(numeric_cols, categorical_cols))
    for num, cat in pairs_mix:
        # 20. Bar (Mean)
        possible_charts.append(create_rec(f"bar_avg_{num}_{cat}", f"Avg {num} by {cat}", "Mean comparison.", "bar",
            {"x": {"field": cat, "type": "nominal"}, "y": {"field": num, "type": "quantitative", "aggregate": "mean"}}))
        # 21. Bar (Max)
        possible_charts.append(create_rec(f"bar_max_{num}_{cat}", f"Max {num} by {cat}", "Peak values.", "bar",
            {"x": {"field": cat, "type": "nominal"}, "y": {"field": num, "type": "quantitative", "aggregate": "max"}}))
        # 22. Boxplot Grouped
        possible_charts.append(create_rec(f"box_grp_{num}_{cat}", f"Box: {num} by {cat}", "Grouped distributions.", "boxplot",
            {"x": {"field": cat, "type": "nominal"}, "y": {"field": num, "type": "quantitative"}}))
        # 23. Violin (Density + Facet - using simple density line faceted)
        possible_charts.append(create_rec(f"violin_sim_{num}_{cat}", f"Density: {num} by {cat}", "Faceted density.", "area",
             {"x": {"field": "value"}, "y": {"field": "density"}, "row": {"field": cat}}, transform=[{"density": num, "groupby": [cat]}]))
        # 24. Tick Plot Grouped
        possible_charts.append(create_rec(f"tick_grp_{num}_{cat}", f"Ticks: {num} by {cat}", "Raw value strip.", "tick",
            {"y": {"field": cat, "type": "nominal"}, "x": {"field": num, "type": "quantitative"}}))
        # 25. Point Plot (Stat)
        possible_charts.append(create_rec(f"point_stat_{num}_{cat}", f"Mean Point: {num} by {cat}", "Focus on mean.", "circle",
            {"x": {"field": cat, "type": "nominal"}, "y": {"field": num, "type": "quantitative", "aggregate": "mean"}, "size": {"value": 100}}))
        # 26. Radial Bar (Simulated with Bar + Polar coord is hard in pure VL JSON without config, using Bar)
        # 27. Error Bar (Simulated with Rule)
        possible_charts.append(create_rec(f"rule_range_{num}_{cat}", f"Range: {num} by {cat}", "Min-max range.", "rule",
             {"x": {"field": cat, "type": "nominal"}, "y": {"field": num, "aggregate": "min"}, "y2": {"field": num, "aggregate": "max"}}))

    # --- 5. TIME SERIES ---
    if datetime_cols and numeric_cols:
        time = datetime_cols[0]
        for num in numeric_cols[:2]:
            # 28. Line Time
            possible_charts.append(create_rec(f"line_t_{num}", f"Timeline: {num}", "Trend over time.", "line",
                {"x": {"field": time, "type": "temporal"}, "y": {"field": num, "type": "quantitative"}}))
            # 29. Area Time
            possible_charts.append(create_rec(f"area_t_{num}", f"Area: {num}", "Volume over time.", "area",
                {"x": {"field": time, "type": "temporal"}, "y": {"field": num, "type": "quantitative"}}))
            # 30. Step Line
            possible_charts.append(create_rec(f"step_t_{num}", f"Step: {num}", "Discrete changes.", {"type": "line", "interpolate": "step-after"},
                {"x": {"field": time, "type": "temporal"}, "y": {"field": num, "type": "quantitative"}}))
            # 31. Point Time
            possible_charts.append(create_rec(f"point_t_{num}", f"Events: {num}", "Discrete measurements.", "point",
                {"x": {"field": time, "type": "temporal"}, "y": {"field": num, "type": "quantitative"}}))
            # 32. Bar Time
            possible_charts.append(create_rec(f"bar_t_{num}", f"Daily/Unit: {num}", "Values per time unit.", "bar",
                {"x": {"field": time, "type": "temporal"}, "y": {"field": num, "type": "quantitative"}}))

    # --- 6. MULTIVARIATE (3+ VARS) ---
    if len(numeric_cols) >= 3:
        x, y, z = numeric_cols[0], numeric_cols[1], numeric_cols[2]
        # 33. Bubble Colored
        possible_charts.append(create_rec(f"bub_col_{x}_{y}_{z}", f"Bubble 3Var", f"{x}/{y} sized by {z}", "circle",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "size": {"field": z, "type": "quantitative"}}))
        # 34. Scatter Colored
        possible_charts.append(create_rec(f"scat_col_{x}_{y}_{z}", f"Scatter Color", f"{x}/{y} colored by {z}", "point",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "color": {"field": z, "type": "quantitative"}}))

    if len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
        x, y = numeric_cols[0], numeric_cols[1]
        c = categorical_cols[0]
        # 35. Scatter Colored Categories
        possible_charts.append(create_rec(f"scat_cat_{x}_{y}_{c}", f"Grouped Scatter", f"{x}/{y} by {c}", "point",
            {"x": {"field": x, "type": "quantitative"}, "y": {"field": y, "type": "quantitative"}, "color": {"field": c, "type": "nominal"}}))
        # 36. Stacked Bar (if y is Agg)
        possible_charts.append(create_rec(f"bar_stack_{x}_{c}", f"Stacked Bar", f"Sum of {x} by {c}", "bar",
            {"x": {"field": c, "type": "nominal"}, "y": {"field": x, "aggregate": "sum"}, "color": {"field": c, "type": "nominal"}})) # Simplistic stack
        # 37. Normalized Bar
        possible_charts.append(create_rec(f"bar_norm_{x}_{c}", f"Norm Bar", f"Example Norm", "bar",
             {"x": {"field": c, "type": "nominal"}, "y": {"field": x, "aggregate": "sum", "stack": "normalize"}, "color": {"field": c}}))
        # 38. Faceted Scatter
        possible_charts.append(create_rec(f"facet_scat_{x}_{y}_{c}", f"Faceted: {c}", f"Scatter split by {c}", "point",
             {"x": {"field": x}, "y": {"field": y}, "row": {"field": c}}))
        # 39. Line Multi-Series (if index is implicitly 2nd numeric acting as time/seq?? No, need time)

    if datetime_cols and categorical_cols and numeric_cols:
        t, n, c = datetime_cols[0], numeric_cols[0], categorical_cols[0]
        # 40. Multi-Line
        possible_charts.append(create_rec(f"mline_{t}_{c}", f"Multi-Line", f"Trends by {c}", "line",
            {"x": {"field": t, "type": "temporal"}, "y": {"field": n}, "color": {"field": c}}))
        # 41. Streamgraph (Stacked Area Center)
        possible_charts.append(create_rec(f"stream_{t}_{c}", f"Streamgraph", f"Flow of {c}", "area",
            {"x": {"field": t, "type": "temporal"}, "y": {"field": n, "aggregate": "sum", "stack": "center"}, "color": {"field": c}}))
        # 42. Stacked Area
        possible_charts.append(create_rec(f"st_area_{t}_{c}", f"Stacked Area", f"Cumulative {c}", "area",
            {"x": {"field": t, "type": "temporal"}, "y": {"field": n, "aggregate": "sum", "stack": "zero"}, "color": {"field": c}}))

    # --- 7. FALLBACK / VARIATIONS TO REACH 45 ---
    # 43. Square Mark
    if numeric_cols:
        possible_charts.append(create_rec(f"sq_{numeric_cols[0]}", "Square Plot", "Simple square mark.", "square", 
            {"x": {"field": numeric_cols[0], "bin": True}, "y": {"aggregate": "count"}}))
    # 44. Rule Plot 1D
    if numeric_cols:
        possible_charts.append(create_rec(f"rule_{numeric_cols[0]}", "Rug Plot", "1D distribution.", "rule", 
            {"x": {"field": numeric_cols[0]}}))
    # 45. Text Mark (Word Cloudish)
    if categorical_cols:
        possible_charts.append(create_rec(f"text_{categorical_cols[0]}", "Text Cloud", "Labels.", "text", 
            {"text": {"field": categorical_cols[0]}, "color": {"field": categorical_cols[0]}}))
    
    # --- INTELLIGENT SELECTION & DEDUPLICATION ---
    unique_recs = []
    seen_signatures = set()
    
    for p in possible_charts:
        # Create a signature based on Mark + Encoding Keys + Fields
        # Simplified signature: Type + XField + YField + Sort + Aggregation
        enc = p["encoding"]
        x_field = enc.get("x", {}).get("field", "") if isinstance(enc.get("x"), dict) else ""
        y_field = enc.get("y", {}).get("field", "") if isinstance(enc.get("y"), dict) else ""
        agg_x = enc.get("x", {}).get("aggregate", "") if isinstance(enc.get("x"), dict) else ""
        agg_y = enc.get("y", {}).get("aggregate", "") if isinstance(enc.get("y"), dict) else ""
        
        # We also check for 'theta' (Pie/Donut)
        theta_field = enc.get("theta", {}).get("field", "") if isinstance(enc.get("theta"), dict) else ""
        
        sig = f"{p['type']}_{x_field}_{y_field}_{theta_field}_{agg_x}_{agg_y}"
        
        if sig not in seen_signatures:
             seen_signatures.add(sig)
             unique_recs.append(p)

    final_recs = unique_recs[:12]
    
    analysis["recommendations"] = final_recs
    return analysis
