import json
import yfinance as yf

def get_investor_prompt(investor, ticker, stock_info):
    """Generate a prompt for famous investor analysis."""
    
    # Common financial metrics if available
    financial_data = {
        "ticker": ticker,
        "name": stock_info.get("longName", ticker),
        "sector": stock_info.get("sector", "Unknown"),
        "industry": stock_info.get("industry", "Unknown"),
        "current_price": stock_info.get("currentPrice", "N/A"),
        "pe_ratio": stock_info.get("trailingPE", "N/A"),
        "forward_pe": stock_info.get("forwardPE", "N/A"),
        "peg_ratio": stock_info.get("pegRatio", "N/A"),
        "dividend_yield": stock_info.get("dividendYield", "N/A"),
        "market_cap": stock_info.get("marketCap", "N/A"),
        "eps": stock_info.get("trailingEps", "N/A"),
        "book_value": stock_info.get("bookValue", "N/A"),
        "price_to_book": stock_info.get("priceToBook", "N/A"),
        "debt_to_equity": stock_info.get("debtToEquity", "N/A"),
        "return_on_equity": stock_info.get("returnOnEquity", "N/A"),
        "free_cash_flow": stock_info.get("freeCashflow", "N/A"),
        "operating_margins": stock_info.get("operatingMargins", "N/A"),
        "profit_margins": stock_info.get("profitMargins", "N/A"),
        "revenue_growth": stock_info.get("revenueGrowth", "N/A"),
        "earnings_growth": stock_info.get("earningsGrowth", "N/A"),
        "business_summary": stock_info.get("longBusinessSummary", "No business summary available.")
    }
    
    # Base prompt structure
    prompt_base = f"""
As a stock market expert, analyze {ticker} ({financial_data['name']}) in the style of {investor}. 
Use the following information about the company:

Business Summary: {financial_data['business_summary']}

Financial Data:
- Current Price: ${financial_data['current_price']}
- P/E Ratio: {financial_data['pe_ratio']}
- Forward P/E: {financial_data['forward_pe']}
- PEG Ratio: {financial_data['peg_ratio']}
- Dividend Yield: {financial_data['dividend_yield']}
- Market Cap: ${financial_data['market_cap']}
- EPS: ${financial_data['eps']}
- Book Value: ${financial_data['book_value']}
- Price to Book: {financial_data['price_to_book']}
- Debt to Equity: {financial_data['debt_to_equity']}
- Return on Equity: {financial_data['return_on_equity']}
- Free Cash Flow: ${financial_data['free_cash_flow']}
- Operating Margins: {financial_data['operating_margins']}
- Profit Margins: {financial_data['profit_margins']}
- Revenue Growth: {financial_data['revenue_growth']}
- Earnings Growth: {financial_data['earnings_growth']}

Sector: {financial_data['sector']}
Industry: {financial_data['industry']}
"""
    
    # Investor-specific prompts
    if investor == "Warren Buffett":
        prompt = prompt_base + """
Analyze this stock in Warren Buffett's style, focusing on:
1. The company's economic moat and competitive advantages
2. The quality of management and capital allocation
3. The stability and predictability of earnings
4. Whether the stock is trading at a discount to its intrinsic value
5. Long-term growth prospects and sustainability
6. Return on invested capital (ROIC)
7. The margin of safety in the current stock price

Use Buffett's value investing principles and his famous quotes. Consider whether this is a "wonderful company at a fair price" or a "fair company at a wonderful price." Evaluate if this company has the characteristics that would make Buffett consider it for his long-term, concentrated portfolio.

Format your response with clear sections for:
- Initial impression
- Business quality analysis
- Management assessment
- Financial strength
- Valuation
- Risks and concerns
- Conclusion with a buy/hold/sell recommendation
"""

    elif investor == "Peter Lynch":
        prompt = prompt_base + """
Analyze this stock using Peter Lynch's investment style, focusing on:
1. What category the stock falls into: slow grower, stalwart, fast grower, cyclical, turnaround, or asset play
2. The PEG ratio and whether growth is reasonably priced
3. The company's "story" and whether it's easy to understand
4. Potential catalysts for future growth
5. Whether this is a business that an average person could understand
6. Signs that might indicate this is a "ten-bagger" opportunity

Use Lynch's down-to-earth, common-sense approach. Consider his principle of "invest in what you know" and his preference for companies with boring names and boring businesses in dull industries.

Format your response with clear sections for:
- Stock category (according to Lynch's classifications)
- The company's "story"
- Growth analysis and PEG ratio
- Competitive position
- Potential catalysts
- Red flags or concerns
- Conclusion with a buy/hold/sell recommendation
"""

    elif investor == "Charlie Munger":
        prompt = prompt_base + """
Analyze this stock using Charlie Munger's mental models and investment philosophy, focusing on:
1. The "four essential filters": a business you can understand, favorable long-term prospects, trustworthy management, and attractive price
2. The quality of the business and its competitive position using his "moat and castle" framework
3. Incentive structures within the company and potential agency problems
4. Potential psychological biases affecting the market's view of this company
5. The margin of safety in the current valuation

Use Munger's multidisciplinary approach and his emphasis on rational thinking. Consider his focus on avoiding stupidity rather than seeking brilliance, and his preference for paying fair prices for great businesses rather than cheap prices for mediocre ones.

Format your response with clear sections for:
- Initial assessment
- Business quality and competitive moat
- Management quality and incentive structures
- Psychological factors affecting valuation
- Risks and potential pitfalls
- Conclusion with a buy/hold/sell recommendation
"""

    elif investor == "Ray Dalio":
        prompt = prompt_base + """
Analyze this stock using Ray Dalio's principles and macroeconomic approach, focusing on:
1. How this company fits into the current phase of the economic cycle
2. Debt levels and vulnerability to economic shifts
3. Correlation with broader market movements and potential as a portfolio diversifier
4. Sensitivity to inflation, interest rates, and currency movements
5. Global trends affecting the business and its resilience to various economic scenarios

Use Dalio's emphasis on understanding the "economic machine" and finding uncorrelated return streams. Consider his principles of radical transparency and thoughtful disagreement.

Format your response with clear sections for:
- Macroeconomic positioning
- Debt and balance sheet analysis
- Correlation with economic indicators
- Inflation and interest rate sensitivity
- Global exposure and risks
- Portfolio fit (would this help or hurt diversification)
- Conclusion with a buy/hold/sell recommendation
"""

    elif investor == "Cathie Wood":
        prompt = prompt_base + """
Analyze this stock using Cathie Wood's innovation-focused investment approach, focusing on:
1. The company's position in disruptive innovation and transformative technologies
2. Growth potential and addressable market size
3. The S-curve adoption phase of the technology or service
4. How the company might benefit from Wright's Law (cost declines with cumulative production)
5. The company's potential to disrupt traditional industries
6. Network effects and scalability

Use Wood's focus on five innovation platforms: DNA sequencing, robotics, energy storage, artificial intelligence, and blockchain technology. Consider her emphasis on convergence between technologies and her long-term investment horizon.

Format your response with clear sections for:
- Innovation category and disruptive potential
- Addressable market analysis
- Technology adoption phase
- Competitive advantage in innovation
- Growth metrics and valuation
- Risks to the innovation thesis
- Conclusion with a buy/hold/sell recommendation
"""

    else:
        prompt = prompt_base + """
Provide a detailed stock analysis covering:
1. Business fundamentals
2. Financial health
3. Valuation
4. Growth prospects
5. Risks and challenges
6. Conclusion with a buy/hold/sell recommendation
"""

    return prompt

def get_intrinsic_value_prompt(ticker, stock_info):
    """Generate a prompt for intrinsic value analysis."""
    
    prompt = f"""
As a financial analyst specializing in valuation, calculate and explain the intrinsic value of {ticker} ({stock_info.get('longName', ticker)}).

Use multiple valuation methods including:
1. Discounted Cash Flow (DCF) Analysis
2. Dividend Discount Model (if applicable)
3. Comparable Company Analysis (using industry P/E, P/B, P/S ratios)
4. Graham's Number (Benjamin Graham's formula)
5. Asset-based valuation

Current financial data:
- Current Price: ${stock_info.get('currentPrice', 'N/A')}
- EPS (TTM): ${stock_info.get('trailingEps', 'N/A')}
- Forward EPS: ${stock_info.get('forwardEps', 'N/A')}
- Book Value Per Share: ${stock_info.get('bookValue', 'N/A')}
- Free Cash Flow: ${stock_info.get('freeCashflow', 'N/A')}
- Historical Growth Rate: {stock_info.get('earningsGrowth', 'N/A')}
- Expected 5-Year Growth Rate: {stock_info.get('earningsQuarterlyGrowth', 'N/A')}
- Current P/E Ratio: {stock_info.get('trailingPE', 'N/A')}
- Industry Average P/E: Calculate based on peers
- Dividend Yield: {stock_info.get('dividendYield', 'N/A')}
- Beta: {stock_info.get('beta', 'N/A')}

For the DCF calculation:
- Use a discount rate that accounts for the company's risk profile, beta, and current market conditions
- Project cash flows for 5-10 years with justifiable growth assumptions
- Calculate a terminal value using a reasonable perpetuity growth rate

For each valuation method:
1. Show your calculations step-by-step
2. Explain key assumptions you're making
3. Provide a sensitivity analysis for critical variables
4. Discuss the strengths and limitations of each approach for this specific company

Conclude with:
1. A range of intrinsic values derived from different methods
2. Your assessment of which valuation method is most appropriate for this company and why
3. The margin of safety at current prices
4. A buy/hold/sell recommendation based on the valuation analysis
"""
    
    return prompt

def get_technical_analysis_prompt(ticker, history):
    """Generate a prompt for technical analysis."""
    
    # Calculate some basic technical indicators
    if not history.empty:
        # Convert history to JSON for the prompt
        history_sample = history.tail(50).to_json()
    else:
        history_sample = "{}"
    
    prompt = f"""
As a professional technical analyst, provide a comprehensive technical analysis for {ticker}.

Use the following technical analysis tools and concepts:
1. Trend Analysis
   - Primary trend direction (bullish, bearish, or neutral)
   - Support and resistance levels
   - Trendlines and channels
   - Price patterns (head and shoulders, double tops/bottoms, triangles, etc.)

2. Moving Averages
   - 50-day and 200-day simple moving averages
   - Golden crosses or death crosses
   - Price relative to key moving averages

3. Momentum Indicators
   - Relative Strength Index (RSI)
   - MACD (Moving Average Convergence Divergence)
   - Stochastic oscillator
   - Rate of Change (ROC)

4. Volume Analysis
   - Volume trends and abnormalities
   - On-balance volume (OBV)
   - Volume by price

5. Volatility Measures
   - Bollinger Bands
   - Average True Range (ATR)

6. Chart Patterns
   - Identify any significant chart patterns
   - Measure targets based on pattern projections
   - Failure levels where patterns would be invalidated

For each indicator or analysis method:
1. Explain what it's showing
2. How it should be interpreted for this specific stock
3. What trading signals it might be generating

Conclude with:
1. A summary of the technical position (strong buy, buy, neutral, sell, strong sell)
2. Key price levels to watch (immediate support/resistance, stop-loss levels)
3. Potential price targets based on your technical analysis
4. Timeframe considerations (short-term vs. medium-term outlook)
5. Any notable divergences between price action and indicators

Recent price data sample: {history_sample}
"""
    
    return prompt

def get_market_condition_prompt():
    """Generate a prompt for market condition analysis."""
    
    # Fetch current market data for the prompt
    try:
        # Prepare tickers to fetch data
        tickers = ["SPY", "QQQ", "IWM", "^VIX", 
                  "XLK", "XLF", "XLV", "XLE", "XLY", 
                  "XLP", "XLI", "XLB", "XLU", "XLRE", "XLC"]
        
        # Dictionary to store results
        market_data = {}
        sector_data = {}
        
        # Define sector names
        sectors = {
            "XLK": "Technology",
            "XLF": "Financial",
            "XLV": "Healthcare",
            "XLE": "Energy",
            "XLY": "Consumer Discretionary",
            "XLP": "Consumer Staples",
            "XLI": "Industrial",
            "XLB": "Materials",
            "XLU": "Utilities",
            "XLRE": "Real Estate",
            "XLC": "Communication Services"
        }
        
        # Fetch data for each ticker
        for symbol in tickers:
            ticker_data = yf.Ticker(symbol).history(period="1mo")
            if not ticker_data.empty:
                if symbol in ["SPY", "QQQ", "IWM"]:
                    perf = ((ticker_data['Close'].iloc[-1] / ticker_data['Close'].iloc[0]) - 1) * 100
                    market_data[symbol] = f"{perf:.2f}%"
                elif symbol == "^VIX":
                    market_data[symbol] = f"{ticker_data['Close'].iloc[-1]:.2f}"
                elif symbol in sectors:
                    perf = ((ticker_data['Close'].iloc[-1] / ticker_data['Close'].iloc[0]) - 1) * 100
                    sector_data[sectors[symbol]] = f"{perf:.2f}%"
    except Exception as e:
        market_data = {"SPY": "N/A", "QQQ": "N/A", "IWM": "N/A", "^VIX": "N/A"}
        sector_data = {name: "N/A" for name in sectors.values()}
    
    # Format as JSON string
    sector_performance = json.dumps(sector_data, indent=2)
    
    prompt = f"""
As a market strategist, provide a comprehensive analysis of current market conditions and the broader economic environment.

Current Market Indicators:
- S&P 500 (SPY) 1-Month Performance: {market_data.get('SPY', 'N/A')}
- Nasdaq 100 (QQQ) 1-Month Performance: {market_data.get('QQQ', 'N/A')}
- Russell 2000 (IWM) 1-Month Performance: {market_data.get('IWM', 'N/A')}
- VIX (Volatility Index) Current Level: {market_data.get('^VIX', 'N/A')}

Sector Performance (1-Month):
{sector_performance}

Analyze the following aspects of the current market environment:

1. Market Trend Analysis
   - Overall market direction (bull, bear, or transitional market)
   - Market breadth and internals
   - Relative performance of large caps vs. small caps
   - Growth vs. value performance

2. Sector Rotation
   - Leading and lagging sectors
   - Defensive vs. cyclical sector performance
   - Sector rotation implications for the economic cycle
   - Opportunities in specific sectors based on current trends

3. Risk Assessment
   - Volatility levels and trends
   - Credit spreads and fixed income signals
   - Correlation between asset classes
   - Potential market risks on the horizon

4. Economic Indicators
   - Interest rate environment and Federal Reserve positioning
   - Inflation trends and expectations
   - Employment and consumer spending outlook
   - Corporate earnings trends

5. Technical Market Position
   - Key support and resistance levels for major indices
   - Overbought/oversold conditions
   - Significant chart patterns or technical signals
   - Volume trends and money flow

6. Investment Strategy Implications
   - Appropriate asset allocation in the current environment
   - Sectors or themes that merit overweight positions
   - Defensive measures to consider if applicable
   - Time horizon considerations for different strategies

Provide a well-structured analysis with clear explanations of the data's significance. Conclude with an overall market outlook and general positioning advice for investors with different time horizons (short-term traders, medium-term investors, and long-term investors).
"""
    
    return prompt

def get_elliott_wave_analysis_prompt(ticker, history):
    """Generate a prompt for Elliott Wave analysis."""
    
    # Convert history to JSON for the prompt
    if not history.empty:
        history_sample = history.tail(250).to_json()
    else:
        history_sample = "{}"
    
    prompt = f"""
As an expert in Elliott Wave Theory, provide a comprehensive Elliott Wave analysis for {ticker}.

Use the following aspects of Elliott Wave Theory:
1. Wave Identification
   - Identify the current position within the five-wave impulse and three-wave corrective pattern
   - Determine if we are in impulse waves (1, 3, 5) or corrective waves (2, 4, A, B, C)
   - Identify wave degrees (Grand Supercycle, Supercycle, Cycle, Primary, Intermediate, Minor, Minute, Minuette, Subminuette)

2. Fibonacci Relationships
   - Analyze Fibonacci retracements and extensions within the identified waves
   - Look for common Fibonacci relationships (wave 3 often extends to 161.8% of wave 1, wave 4 often retraces to 38.2% of wave 3)
   - Check for Fibonacci time relationships

3. Wave Characteristics
   - Examine the personality of each wave (wave 3 typically strongest, wave 5 often shows divergence)
   - Analyze volume characteristics of each wave
   - Check for wave alternation (if wave 2 is sharp, wave 4 is typically flat, or vice versa)

4. Pattern Recognition
   - Identify key Elliott Wave patterns (triangles, flats, zigzags)
   - Look for ending diagonals, leading diagonals, or triangle patterns
   - Check for wave extensions, particularly in wave 3

5. Wave Counting Guidelines
   - Apply the rules of wave counting (wave 3 never shortest, wave 4 never overlaps wave 1, etc.)
   - Consider alternative wave counts
   - Discuss confidence level in the primary wave count

Based on your Elliott Wave analysis, provide:
1. Current wave position and count
2. Potential price targets for completion of the current wave
3. Expected next wave movement with price targets
4. Critical invalidation levels
5. Trading implications based on the analysis
6. Time expectations for the current and next wave movements

Include a disclaimer about the subjective nature of Elliott Wave analysis and the importance of risk management and alternative scenarios.

Format your response with clear sections for:
- Current Elliott Wave Count
- Wave Characteristics Analysis
- Price Targets
- Invalidation Levels
- Trading Strategy Implications
- Alternative Wave Counts
- Risk Assessment

Recent price data sample: {history_sample}
"""
    
    return prompt 