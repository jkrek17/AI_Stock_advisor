# AI Stock Advisor

This application uses AI to analyze stocks from the perspective of famous investors and provides comprehensive market analysis.

## Features

- **Famous Investor Analysis**: Get stock analysis in the style of Warren Buffett, Peter Lynch, and other legendary investors
- **Intrinsic Value Calculation**: Calculate a stock's intrinsic value using various methodologies
- **Technical Analysis**: Evaluate the technical setup of a stock
- **Market Condition Analysis**: Analyze broader market conditions with indices like SPY, QQQ, IWM, and VIX

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```
4. Run the application: `streamlit run app.py`

> **Note on Claude Models**: The application uses the Claude 3 Haiku model (`claude-3-haiku-20240307`). If you experience issues, you may need to update the model name in the `app.py` file to match a currently available model from Anthropic.

## Usage

1. Enter a stock ticker
2. Select the type of analysis you want
3. View the AI-generated analysis based on your selection 