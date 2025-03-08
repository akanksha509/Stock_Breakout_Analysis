# Stock Breakout Analysis Application

A web application that analyzes stock breakouts based on volume and price thresholds. The application allows users to analyze historical stock data, identify breakout patterns, and generate detailed reports.

Project Link [https://stock-breakout-analysis.onrender.com](https://stock-breakout-analysis.onrender.com)

## Features

- Input custom parameters for stock analysis:
  - Ticker symbol
  - Date range selection
  - Volume breakout threshold
  - Daily price change threshold
  - Holding period
- Interactive results display
- Downloadable Excel reports
- Summary statistics
- Detailed breakout analysis table

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository (or create a new directory):

```bash
git clone https://github.com/Aryaman19/Stock-Breakout-Analysis.git
cd Stock-Breakout-Analysis
```

2. Create a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
stock_analysis/
├── venv/
├── app.py
└── templates/
    └── index.html
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:

```bash
python app.py
```

3. Open your web browser and navigate to:

```
http://localhost:5000
```

## Using the Application

1. Enter Analysis Parameters:

   - Input the stock ticker symbol (e.g., AAPL, MSFT)
   - Select start and end dates for analysis
   - Set volume threshold (e.g., 200 for 200% of average)
   - Set price change threshold (e.g., 2 for 2% increase)
   - Set holding period in days

2. Generate Analysis:

   - Click "Generate Report" button
   - Wait for analysis to complete (loading spinner will appear)

3. View Results:

   - Summary statistics will be displayed
   - Detailed breakout analysis shown in table format

4. Download Report:
   - Click "Download Excel Report" button
   - Excel file will contain:
     - Breakout Analysis sheet
     - Summary Statistics sheet

## Technical Details

- Backend: Flask (Python)
- Frontend: HTML, JavaScript, Tailwind CSS
- Data Source: Yahoo Finance (yfinance)
- Report Generation: pandas, xlsxwriter

## File Descriptions

- `app.py`: Main Flask application containing backend logic
- `templates/index.html`: Frontend template with user interface and JavaScript
- `requirements.txt`: List of Python dependencies

## Analysis Methodology

The application identifies stock breakouts based on two main criteria:

1. Volume exceeding a specified percentage of the 20-day moving average
2. Price increase exceeding a specified percentage on the breakout day

For each identified breakout, the application:

- Records entry price and date
- Calculates exit price after specified holding period
- Computes return on investment
- Generates summary statistics
