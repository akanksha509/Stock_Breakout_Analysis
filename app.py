# app.py
from flask import Flask, render_template, request, send_file, jsonify
import yfinance as yf
import pandas as pd
from io import BytesIO
import datetime
import json

app = Flask(__name__)

def analyze_stock(ticker, start_date, end_date, volume_threshold, price_threshold, hold_period):
    # Download stock data
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)

    # Calculate 20-day moving average volume
    df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()

    # Calculate daily returns
    df['Daily_Return'] = df['Close'].pct_change()

    # Create volume ratio
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA20']

    # Find breakout days
    breakouts = df[
        (df['Volume_Ratio'] > volume_threshold) &  # Volume > threshold
        (df['Daily_Return'] > price_threshold)     # Price up > threshold
    ].copy()

    # Calculate forward returns
    results = []
    for idx, row in breakouts.iterrows():
        entry_price = df.loc[idx, 'Close']
        entry_date = idx

        # Find the price after hold_period days
        if idx + datetime.timedelta(days=hold_period) < df.index[-1]:
            future_dates = df.index[df.index > idx]
            if len(future_dates) >= hold_period:
                exit_date = future_dates[hold_period-1]
                exit_price = df.loc[exit_date, 'Close']
                hold_return = (exit_price - entry_price) / entry_price

                results.append({
                    'Entry_Date': entry_date.strftime('%Y-%m-%d'),
                    'Entry_Price': round(entry_price, 2),
                    'Volume_Ratio': round(row['Volume_Ratio'], 2),
                    'Daily_Return': f"{row['Daily_Return']:.2%}",
                    'Exit_Date': exit_date.strftime('%Y-%m-%d'),
                    'Exit_Price': round(exit_price, 2),
                    'Hold_Return': f"{hold_return:.2%}"
                })

    # Calculate summary statistics
    summary = {
        'Total_Trades': len(results),
        'Average_Return': f"{pd.Series([float(r['Hold_Return'].rstrip('%')) for r in results]).mean():.2f}%" if results else "0%",
        'Win_Rate': f"{pd.Series([float(r['Hold_Return'].rstrip('%')) > 0 for r in results]).mean():.2%}" if results else "0%",
        'Best_Trade': max([r['Hold_Return'] for r in results], default="0%"),
        'Worst_Trade': min([r['Hold_Return'] for r in results], default="0%")
    }

    return results, summary


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    ticker = data['ticker']
    start_date = data['start_date']
    end_date = data['end_date']
    volume_threshold = float(data['volume_threshold']) / 100
    price_threshold = float(data['price_threshold']) / 100
    hold_period = int(data['hold_period'])

    results, summary = analyze_stock(ticker, start_date, end_date, volume_threshold,
                                     price_threshold, hold_period)

    return jsonify({
        'results': results,
        'summary': summary
    })


@app.route('/download', methods=['POST'])
def download():
    data = request.json
    results = pd.DataFrame(data['results'])
    summary = pd.DataFrame([
        {'Metric': k, 'Value': v}
        for k, v in data['summary'].items()
    ])

    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        results.to_excel(writer, sheet_name='Breakout Analysis', index=False)
        summary.to_excel(writer, sheet_name='Summary', index=False)

    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'{data["ticker"]}_breakout_analysis.xlsx'
    )


if __name__ == '__main__':
    app.run(debug=True)
