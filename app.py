import streamlit as st


# Page configuration
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)

# Main title
st.title("📈 Stock Market Analysis with Moving Averages")

# Sidebar
st.sidebar.header("About")
st.sidebar.info(
    """
    This app provides real-time stock market analysis with:
    - Candlestick charts
    - Moving averages (MA10, MA50, MA100)
    - Live price updates
    - Logarithmic scaling option
    """
)

# Main content area
st.header("Stock Data Configuration")


# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit and yfinance")
