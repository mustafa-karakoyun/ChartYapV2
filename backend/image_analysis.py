import cv2
import numpy as np

def detect_chart_type(image_bytes):
    """
    Analyzes image bytes using OpenCV to determine the chart type.
    Returns a Vega-Lite mark type: 'arc', 'bar', 'line', 'point', etc.
    """
    try:
        # 1. Decode Image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return "bar" # Fallback

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        # 2. Check for BAR CHART (Rectangles) - Priority over Circle frames
        # Thresholding
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rect_count = 0
        total_contours = 0
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < (width * height * 0.002): # Ignore small dots/noise
                continue
            
            total_contours += 1
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            
            # If it has 4 vertices (+- error), it's a rectangle
            # Bars are usually vertical/horizontal rectangles
            if len(approx) == 4:
                x,y,w,h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                # Bars are usually not perfect squares (1.0), but can be
                rect_count += 1
                
        # Heuristic: If we found distinct rectangles, it's likely a Bar chart
        # Even if it has a circular frame, the presence of bars is distinctive.
        if total_contours > 0 and (rect_count >= 3 or (rect_count/total_contours > 0.4)):
            return "bar"

        # 3. Check for PIE/DONUT (Circles)
        # HoughCircles can prove to be too aggressive if there is just a frame.
        # We only check this if bars weren't found.
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=width/4,
                                   param1=50, param2=30, minRadius=int(min(height, width)*0.1), maxRadius=int(min(height, width)*0.9))
        
        if circles is not None:
            # If we decided it's not a bar, but has a big circle, it's a Pie.
            return "arc"

        # 4. Check for LINE CHART
        # ... (rest of logic)

        # 4. Check for LINE CHART
        # Canny Edges -> Hough Lines
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=width/10, maxLineGap=20)
        
        if lines is not None and len(lines) > 0:
            # If valid lines exist that aren't just frame borders...
            # This is a weak heuristic but better than nothing
            return "line"

        # Default Fallback
        return "bar"

    except Exception as e:
        print(f"Error in image analysis: {e}")
        return "bar" # Safe default
