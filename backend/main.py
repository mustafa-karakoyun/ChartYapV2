from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from analyzer import analyze_dataframe
from image_analysis import detect_chart_type

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], # Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze-data")
async def analyze_data_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Simple loader for CSV and Excel
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(contents))
    elif file.filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(io.BytesIO(contents))
    else:
        return {"error": "Unsupported file format"}

    # Run analysis
    result = analyze_dataframe(df)
    
    # Return data for frontend visualization (Limit to 5000 rows to prevent payload issues)
    # Convert all columns to compatible types (e.g. usage of NaN)
    df_clean = df.fillna(0) # Simple fill na for visualization safety
    limit = 5000
    if len(df_clean) > limit:
        result["preview"] = df_clean.head(limit).to_dict(orient="records")
    else:
        result["preview"] = df_clean.to_dict(orient="records")
    
    return result

@app.post("/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        detected_type = detect_chart_type(content)
        
        return {
            "filename": file.filename,
            "detected_type": detected_type, 
            "message": f"Successfully analyzed image. Detected style: {detected_type}"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
