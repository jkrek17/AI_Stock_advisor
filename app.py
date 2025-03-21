import streamlit as st

# Set page configuration - must come before any other st commands
st.set_page_config(
    page_title="AI Stock Advisor",
    page_icon="📈",
    layout="wide"
)

import yfinance as yf
import pandas as pd
import os
import re
from dotenv import load_dotenv
from anthropic import Anthropic

# In local development, load from .env
# In Streamlit Cloud, it will use secrets
if os.path.exists(".env"):
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
else:
    # When deployed to Streamlit Cloud, use st.secrets
    api_key = st.secrets.get("ANTHROPIC_API_KEY")

# Define the Claude model to use
# Use the model that's confirmed to work
CLAUDE_MODEL = "claude-3-haiku-20240307"

# App title and description
st.title("AI Stock Advisor")
st.markdown("Get AI-powered stock analysis from the perspective of famous investors")

# Add prominent disclaimer
st.warning("""
**DISCLAIMER: This is not financial advice.** 

This tool provides AI-generated analysis for educational and informational purposes only. The analyses, opinions, and recommendations are generated by an AI model and should not be considered as professional financial advice. Before making any investment decisions, consult with a qualified financial advisor who can consider your personal circumstances and financial goals. Past performance is not indicative of future results. Investing involves risk, including the possible loss of principal.
""")

# Custom CSS to improve appearance
st.markdown("""
<style>
    .main-header {color:#1E88E5; font-size:28px;}
    .subheader {color:#0D47A1; font-size:22px; margin-top:15px;}
    .info-box {background-color:rgba(30, 136, 229, 0.1); padding:15px; border-radius:5px; margin-bottom:20px;}
    .data-source {font-size:12px; color:#666; font-style:italic;}
</style>
""", unsafe_allow_html=True)

# Helper function to determine metric status (positive, neutral, negative)
def get_metric_status(metric_name, value):
    """
    Determine if a metric is positive, neutral, or negative based on generally accepted standards.
    Returns: "positive", "neutral", or "negative"
    """
    if value is None or value == 'N/A':
        return "neutral"
    
    try:
        value = float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else value
        
        # Valuation metrics - lower is generally better
        if metric_name in ["P/E Ratio", "Forward P/E", "Price to Book"]:
            if isinstance(value, (int, float)):
                if metric_name == "P/E Ratio" or metric_name == "Forward P/E":
                    if value < 15:
                        return "positive"
                    elif value < 25:
                        return "neutral"
                    else:
                        return "negative"
                elif metric_name == "Price to Book":
                    if value < 1.5:
                        return "positive"
                    elif value < 3:
                        return "neutral"
                    else:
                        return "negative"
        
        # Growth metrics - higher is generally better
        elif metric_name in ["Revenue Growth", "Earnings Growth", "Dividend Yield", "Return on Equity"]:
            if isinstance(value, (int, float)):
                if metric_name == "Dividend Yield":
                    if value > 0.03:  # > 3%
                        return "positive"
                    elif value > 0.01:  # > 1%
                        return "neutral"
                    elif value > 0:
                        return "neutral"
                    else:
                        return "neutral"  # No dividend isn't necessarily bad
                elif metric_name in ["Revenue Growth", "Earnings Growth"]:
                    if value > 0.15:  # > 15%
                        return "positive"
                    elif value > 0.05:  # > 5%
                        return "neutral"
                    elif value > 0:
                        return "neutral"
                    else:
                        return "negative"
                elif metric_name == "Return on Equity":
                    if value > 0.15:  # > 15%
                        return "positive"
                    elif value > 0.10:  # > 10%
                        return "neutral"
                    elif value > 0:
                        return "neutral"
                    else:
                        return "negative"
        
        # Financial health metrics
        elif metric_name == "Debt to Equity":
            if isinstance(value, (int, float)):
                if value < 0.5:
                    return "positive"
                elif value < 1.5:
                    return "neutral"
                else:
                    return "negative"
        
        # Margin metrics
        elif metric_name in ["Operating Margin", "Profit Margin"]:
            if isinstance(value, (int, float)):
                if value > 0.20:  # > 20%
                    return "positive"
                elif value > 0.10:  # > 10%
                    return "neutral"
                elif value > 0:
                    return "neutral"
                else:
                    return "negative"
        
        # PEG Ratio
        elif metric_name == "PEG Ratio":
            if isinstance(value, (int, float)):
                if value < 1:
                    return "positive"
                elif value < 2:
                    return "neutral"
                else:
                    return "negative"
    
    except (ValueError, TypeError):
        return "neutral"
    
    # Default case
    return "neutral"

# Helper function to enhance visual hierarchy of AI responses
def format_ai_response(text):
    """
    Enhance the formatting of AI responses to improve visual hierarchy.
    - Identifies and styles section headers
    - Applies highlighting to key insights
    - Formats lists better
    """
    # Find common section headers in investor analyses (like "Initial impression", "Business quality analysis", etc.)
    enhanced_text = text
    
    # Convert section headers to styled headers with a color accent
    # This pattern matches common section headers from the prompts
    section_headers = [
        "Initial impression", "Business quality analysis", "Management assessment", 
        "Financial strength", "Valuation", "Risks and concerns", "Conclusion",
        "Stock category", "The company's story", "Growth analysis and PEG ratio",
        "Competitive position", "Potential catalysts", "Red flags or concerns",
        "Macroeconomic positioning", "Debt and balance sheet analysis",
        "Correlation with economic indicators", "Portfolio fit",
        "Innovation category", "Addressable market analysis", "Growth metrics"
    ]
    
    # Create a regex pattern that matches these headers (with or without colon)
    headers_pattern = "|".join(section_headers)
    section_pattern = rf'(^|\n)[ \t]*(?:\*\*)?(({headers_pattern})(:)?)(?:\*\*)?[ \t]*(\n|$)'
    
    # Replace with styled headers
    enhanced_text = re.sub(
        section_pattern, 
        r'\1<div style="color:#1E88E5; font-size:22px; font-weight:bold; border-bottom:2px solid #1E88E5; margin-top:25px; margin-bottom:15px; padding-bottom:5px;">\2</div>', 
        enhanced_text,
        flags=re.IGNORECASE
    )
    
    # Second pattern for other capitalized headers with colons
    general_section_pattern = r'(^|\n)[ \t]*([A-Z][A-Za-z\s]+:)[ \t]*(\n|$)'
    enhanced_text = re.sub(
        general_section_pattern, 
        r'\1<div style="color:#1E88E5; font-size:20px; font-weight:bold; margin-top:20px; margin-bottom:10px;">\2</div>', 
        enhanced_text
    )
    
    # Add emphasis to subsections (often marked with bold)
    subsection_pattern = r'\*\*(.*?)\*\*:'
    enhanced_text = re.sub(
        subsection_pattern, 
        r'<span style="color:#0D47A1; font-weight:bold; font-size:18px;">\1:</span>', 
        enhanced_text
    )
    
    # Highlight important metrics/numbers
    metrics_pattern = r'([0-9]+(\.[0-9]+)?\s*%)|(\$[0-9]+(,[0-9]+)*(\.[0-9]+)?[KMBT]?)'
    enhanced_text = re.sub(
        metrics_pattern, 
        r'<span style="color:#FF5722; font-weight:bold;">\g<0></span>', 
        enhanced_text
    )
    
    # Highlight buy/hold/sell recommendations with color-coded badges
    def recommendation_replacement(match):
        rec = match.group(1).lower()
        if rec == 'buy':
            return '<span style="background-color:#4CAF50; color:white; padding:3px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">BUY</span>'
        elif rec == 'sell':
            return '<span style="background-color:#F44336; color:white; padding:3px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">SELL</span>'
        elif rec == 'hold':
            return '<span style="background-color:#FF9800; color:white; padding:3px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">HOLD</span>'
        return match.group(0)
    
    recommendation_pattern = r'\b(buy|hold|sell)\b'
    enhanced_text = re.sub(recommendation_pattern, recommendation_replacement, enhanced_text, flags=re.IGNORECASE)
    
    # Enhance bullet points to make them more visible
    enhanced_text = enhanced_text.replace('- ', '• ')
    
    # Add paragraph spacing for better readability
    enhanced_text = re.sub(r'(\n\n|\r\n\r\n)', r'<div style="margin-bottom:15px;"></div>', enhanced_text)
    
    # Final wrap with better spacing and font, but WITHOUT a background color
    enhanced_text = f'''
    <div style="line-height:1.6; font-size:16px; font-family: 'Segoe UI', Arial, sans-serif; padding:15px; border-radius:5px;">
        {enhanced_text}
    </div>
    '''
    
    return enhanced_text

# Helper function to format large numbers
def format_large_number(num):
    """Format large numbers with K, M, B suffixes."""
    if num is None or num == 'N/A':
        return 'N/A'
    
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"${num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"${num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"${num/1_000:.2f}K"
        else:
            return f"${num:.2f}"
    except:
        return str(num)

# Helper function to format percentages
def format_percentage(num):
    """Format a decimal as a percentage."""
    if num is None or num == 'N/A':
        return 'N/A'
    
    try:
        num = float(num)
        return f"{num*100:.2f}%"
    except:
        return str(num)

# Initialize Anthropic client
try:
    anthropic = Anthropic(api_key=api_key)
    if not api_key:
        st.error("API key is missing. Please check your configuration.")
except Exception as e:
    st.error(f"Failed to initialize Anthropic client. Check your API key. Error: {str(e)}")
    anthropic = None

# Create sidebar for user inputs
with st.sidebar:
    st.header("Enter Stock Information")
    ticker = st.text_input("Stock Ticker Symbol (e.g. AAPL)", "AAPL")
    
    analysis_type = st.selectbox(
        "Analysis Type",
        [
            "Famous Investor Analysis",
            "Intrinsic Value Calculation",
            "Technical Analysis",
            "Elliott Wave Analysis",
            "Market Condition Analysis"
        ]
    )
    
    if analysis_type == "Famous Investor Analysis":
        investor = st.selectbox(
            "Select Investor Style",
            [
                "Warren Buffett",
                "Peter Lynch",
                "Charlie Munger",
                "Ray Dalio",
                "Cathie Wood"
            ]
        )
    
    # Remove sidebar footer from here since we'll move it to the bottom

# Function to get stock data
@st.cache_data(ttl=3600)
def get_stock_data(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        info = stock.info
        
        # Don't return the stock object as it's not serializable
        return history, info
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None

# Helper function to create a colored metric display
def colored_metric(label, value, status=None):
    """Create a color-coded metric display based on status"""
    if status is None:
        status = get_metric_status(label, value)
    
    # In Streamlit, "normal" means green for positive delta
    # and "inverse" means red for negative delta
    # This appears to be reversed in some themes, so let's fix it
    if status == "positive":
        # For positive metrics, show an up arrow in green
        delta_color = "normal"  # "normal" should be green
        delta = "Favorable"
    elif status == "negative":
        # For negative metrics, show a down arrow in red
        delta_color = "inverse"  # "inverse" should be red
        delta = "Concerning"
    else:
        # For neutral metrics, show a circle in gray
        delta_color = "off"  # Gray/neutral color
        delta = "Neutral"
    
    return st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

# Main content based on selection
if st.sidebar.button("Analyze"):
    if not ticker:
        st.warning("Please enter a valid ticker symbol")
    else:
        # Remove the data attribution from here since we'll move it to bottom of sidebar
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                # Get stock data
                history, info = get_stock_data(ticker)
                
                if history is not None and not history.empty:
                    # Display basic stock info
                    st.subheader(f"{info.get('longName', ticker)} ({ticker})")
                    
                    # Add company information in a nice box
                    with st.expander("Company Information", expanded=True):
                        cols = st.columns([2, 1])
                        with cols[0]:
                            # Company description
                            st.markdown(f"<div class='info-box'>{info.get('longBusinessSummary', 'No description available.')}</div>", unsafe_allow_html=True)
                            # Company metadata
                            meta_col1, meta_col2, meta_col3 = st.columns(3)
                            meta_col1.metric("Sector", info.get('sector', 'N/A'))
                            meta_col2.metric("Industry", info.get('industry', 'N/A'))
                            meta_col3.metric("Country", info.get('country', 'N/A'))
                        
                        with cols[1]:
                            # Try to display company logo
                            try:
                                logo_url = info.get('logo_url')
                                if logo_url:
                                    st.image(logo_url, width=100)
                            except:
                                pass
                            
                            # Display company website and other links
                            website = info.get('website', '')
                            if website:
                                st.markdown(f"[Visit Website]({website})")
                    
                    # Display a summary card with the most important information in two rows
                    col1, col2 = st.columns(2)
                    with col1:
                        colored_metric("Current Price", format_large_number(info.get('currentPrice')), "neutral")
                    with col2:
                        colored_metric("Market Cap", format_large_number(info.get('marketCap')), "neutral")
                    
                    # Display 52-week range in its own row for better visibility
                    st.metric("52 Week Range", f"{format_large_number(info.get('fiftyTwoWeekLow'))} - {format_large_number(info.get('fiftyTwoWeekHigh'))}")
                    
                    # Display additional key metrics in an expandable section
                    with st.expander("View Key Financial Metrics"):
                        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                        
                        with metrics_col1:
                            pe_ratio = round(info.get('trailingPE', 'N/A'), 2) if info.get('trailingPE') not in ['N/A', None] else 'N/A'
                            colored_metric("P/E Ratio", pe_ratio)
                            
                            forward_pe = round(info.get('forwardPE', 'N/A'), 2) if info.get('forwardPE') not in ['N/A', None] else 'N/A'
                            colored_metric("Forward P/E", forward_pe)
                            
                            peg_ratio = round(info.get('pegRatio', 'N/A'), 2) if info.get('pegRatio') not in ['N/A', None] else 'N/A'
                            colored_metric("PEG Ratio", peg_ratio)
                        
                        with metrics_col2:
                            eps = f"${info.get('trailingEps', 'N/A')}" if info.get('trailingEps') not in ['N/A', None] else 'N/A'
                            colored_metric("EPS", eps)
                            
                            dividend_yield = info.get('dividendYield', 'N/A')
                            colored_metric("Dividend Yield", format_percentage(dividend_yield))
                            
                            book_value = f"${info.get('bookValue', 'N/A')}" if info.get('bookValue') not in ['N/A', None] else 'N/A'
                            colored_metric("Book Value", book_value, "neutral")
                        
                        with metrics_col3:
                            price_to_book = round(info.get('priceToBook', 'N/A'), 2) if info.get('priceToBook') not in ['N/A', None] else 'N/A'
                            colored_metric("Price to Book", price_to_book)
                            
                            roe = info.get('returnOnEquity', 'N/A')
                            colored_metric("Return on Equity", format_percentage(roe))
                            
                            debt_to_equity = round(info.get('debtToEquity', 'N/A'), 2) if info.get('debtToEquity') not in ['N/A', None] else 'N/A'
                            colored_metric("Debt to Equity", debt_to_equity)
                        
                        with metrics_col4:
                            fcf = info.get('freeCashflow', 'N/A')
                            colored_metric("Free Cash Flow", format_large_number(fcf), "neutral")
                            
                            op_margins = info.get('operatingMargins', 'N/A')
                            colored_metric("Operating Margin", format_percentage(op_margins))
                            
                            profit_margins = info.get('profitMargins', 'N/A')
                            colored_metric("Profit Margin", format_percentage(profit_margins))
                    
                    # Enhanced price chart
                    st.subheader("Price History (1 Year)")
                    
                    # Calculate 50-day and 200-day moving averages
                    if not history.empty and len(history) > 200:
                        history['MA50'] = history['Close'].rolling(window=50).mean()
                        history['MA200'] = history['Close'].rolling(window=200).mean()
                        
                        # Create a DataFrame for plotting
                        chart_data = pd.DataFrame({
                            'Price': history['Close'],
                            '50-Day MA': history['MA50'],
                            '200-Day MA': history['MA200']
                        })
                        
                        # Plot with both moving averages
                        st.line_chart(chart_data)
                        
                        # Display moving average status
                        ma_col1, ma_col2 = st.columns(2)
                        
                        # Check if price is above 50-day MA
                        price_above_ma50 = history['Close'].iloc[-1] > history['MA50'].iloc[-1]
                        ma50_status = "positive" if price_above_ma50 else "negative"
                        ma_col1.metric("Price vs 50-Day MA", 
                                 f"{'+' if price_above_ma50 else '-'}{abs(history['Close'].iloc[-1] - history['MA50'].iloc[-1]):.2f}",
                                 f"{'Above' if price_above_ma50 else 'Below'}", 
                                 delta_color="normal" if price_above_ma50 else "inverse")
                        
                        # Check if price is above 200-day MA
                        price_above_ma200 = history['Close'].iloc[-1] > history['MA200'].iloc[-1]
                        ma200_status = "positive" if price_above_ma200 else "negative"
                        ma_col2.metric("Price vs 200-Day MA", 
                                  f"{'+' if price_above_ma200 else '-'}{abs(history['Close'].iloc[-1] - history['MA200'].iloc[-1]):.2f}",
                                  f"{'Above' if price_above_ma200 else 'Below'}", 
                                  delta_color="normal" if price_above_ma200 else "inverse")
                        
                        # Golden/Death Cross detection
                        if history['MA50'].iloc[-1] > history['MA200'].iloc[-1] and history['MA50'].iloc[-20] <= history['MA200'].iloc[-20]:
                            st.success("📈 **Golden Cross Alert**: 50-day MA recently crossed above 200-day MA - typically bullish")
                        elif history['MA50'].iloc[-1] < history['MA200'].iloc[-1] and history['MA50'].iloc[-20] >= history['MA200'].iloc[-20]:
                            st.error("📉 **Death Cross Alert**: 50-day MA recently crossed below 200-day MA - typically bearish")
                    else:
                        # If not enough data for moving averages, just show the price chart
                        st.line_chart(history['Close'])
                    
                    # Handle different analysis types
                    if analysis_type == "Famous Investor Analysis":
                        from prompts import get_investor_prompt
                        prompt = get_investor_prompt(investor, ticker, info)
                        
                        message = anthropic.messages.create(
                            model=CLAUDE_MODEL,
                            max_tokens=4000,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        st.subheader(f"{investor}'s Analysis")
                        st.markdown(format_ai_response(message.content[0].text), unsafe_allow_html=True)
                        
                    elif analysis_type == "Intrinsic Value Calculation":
                        from prompts import get_intrinsic_value_prompt
                        prompt = get_intrinsic_value_prompt(ticker, info)
                        
                        message = anthropic.messages.create(
                            model=CLAUDE_MODEL,
                            max_tokens=4000,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        st.subheader("Intrinsic Value Analysis")
                        st.markdown(format_ai_response(message.content[0].text), unsafe_allow_html=True)
                        
                    elif analysis_type == "Technical Analysis":
                        from prompts import get_technical_analysis_prompt
                        prompt = get_technical_analysis_prompt(ticker, history)
                        
                        message = anthropic.messages.create(
                            model=CLAUDE_MODEL,
                            max_tokens=4000,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        st.subheader("Technical Analysis")
                        st.markdown(format_ai_response(message.content[0].text), unsafe_allow_html=True)
                        
                    elif analysis_type == "Elliott Wave Analysis":
                        from prompts import get_elliott_wave_analysis_prompt
                        prompt = get_elliott_wave_analysis_prompt(ticker, history)
                        
                        message = anthropic.messages.create(
                            model=CLAUDE_MODEL,
                            max_tokens=4000,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        st.subheader("Elliott Wave Analysis")
                        st.markdown(format_ai_response(message.content[0].text), unsafe_allow_html=True)
                        
                    elif analysis_type == "Market Condition Analysis":
                        from prompts import get_market_condition_prompt
                        prompt = get_market_condition_prompt()
                        
                        message = anthropic.messages.create(
                            model=CLAUDE_MODEL,
                            max_tokens=4000,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        st.subheader("Market Condition Analysis")
                        st.markdown(format_ai_response(message.content[0].text), unsafe_allow_html=True)
                else:
                    st.error(f"Could not fetch data for {ticker}. Please check the ticker symbol.")
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# Main content ends here

# Add attribution and app info at the bottom of the sidebar, outside all other sidebar elements
st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)  # Add some space
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem; padding: 10px;">
    <p style="font-size: 1rem; margin-bottom: 10px;">AI Stock Advisor v1.0</p>
    <p>Analysis powered by Claude 3 Haiku</p>
    <p>Data provided by Yahoo Finance</p>
    <p style="font-style: italic; margin-top: 10px;">Not financial advice. For educational purposes only.</p>
</div>
""", unsafe_allow_html=True) 