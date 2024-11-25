import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from fastapi.responses import FileResponse

app = FastAPI()


class WineDataFilter:
    def __init__(self, data_file: str):
        try:
            self.data = pd.read_csv(data_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{data_file}' was not found. Please ensure it exists.")

    def filter_by_quality(self, quality: List[int]) -> pd.DataFrame:
        """Filter wine data based on a list of qualities."""
        return self.data[self.data['quality'].isin(quality)]

    def plot_feature_distribution(self, filtered_data: pd.DataFrame, feature: str, filename: str):
        if feature not in filtered_data.columns:
            raise ValueError(f"Feature '{feature}' is not a valid column in the dataset.")
        plt.figure(figsize=(8, 6))
        plt.hist(filtered_data[feature], bins=20, color='c', edgecolor='black')
        plt.title(f'Distribution of {feature}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.savefig(filename)
        plt.close()


# Initialize the WineDataFilter instance
wine_data_filter = WineDataFilter('winequality-red.csv')


@app.get("/")
def root():
    """
    Root endpoint with welcome message and available endpoints.
    """
    return {
        "message": "Welcome to the Wine Data API!",
        "endpoints": {
            "/filter_wine/": "Filter wine data and visualize distributions of specified features.",
            "/download_image/": "Download the generated feature distribution images."
        }
    }


@app.get("/filter_wine/")
def filter_wine(
    quality: List[int] = Query(..., description="List of quality levels to filter the wine data."),
    features: Optional[List[str]] = Query(None, description="List of feature names for visualization.")
):
    """
    Filter wine data based on quality and visualize distributions of specified features.
    """
    try:
        # Filter the data
        filtered_data = wine_data_filter.filter_by_quality(quality)
        if filtered_data.empty:
            raise HTTPException(status_code=404, detail="No data found for the specified quality levels.")

        # Generate visualizations for the requested features
        image_files = []
        if features:
            for feature in features:
                filename = f"{feature}_distribution.png"
                try:
                    wine_data_filter.plot_feature_distribution(filtered_data, feature, filename)
                    image_files.append(filename)
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))

        return {
            "filtered_data": filtered_data.to_dict(orient="records"),
            "images": image_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download_image/")
def download_image(filename: str):
    """
    Endpoint to download the saved feature distribution visualization image.
    """
    try:
        return FileResponse(filename, media_type='image/png', filename=filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Image file '{filename}' not found.")
