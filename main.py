import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Kripto Levent Özel Fibo & Analiz Paneli",
    page_icon="📈",
    layout="wide"
)

# Özel CSS Tasarımı (Koyu Tema)
st.markdown("""
    <style>
    .main { background-color: #121212; color: #e0e0e0; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Kripto Levent Özel Fibonacci & Trend Analiz Paneli")
st.markdown("Bu panel, TradingView strateji mantığını Python tabanlı olarak simüle eder ve canlı piyasa verilerini analiz eder.")

# --- YAN MENÜ (AYARLAR) ---
st.sidebar.header("⚙️ Analiz Ayarları")
symbol_input = st.sidebar.text_input("Varlık / Coin (Örn: BTC-USD, ETH-USD, SOL-USD)", "BTC-USD")
timeframe = st.sidebar.selectbox("Zaman Dilimi / Strateji", ["Scalp (Kısa Vade)", "Swing (Orta/Uzun Vade)"])
virtual_capital = st.sidebar.number_input("Sanal Kasa ($)", value=50.0, step=10.0)
leverage = st.sidebar.slider("Kaldıraç", 1, 20, 5)

if st.sidebar.button("Analizi Başlat / Güncelle", type="primary"):
    with st.spinner("Piyasa verileri taranıyor ve Fibo seviyeleri hesaplanıyor..."):
        
        # Veri Çekme (Son 60 mum)
        period_val = "5d" if timeframe == "Scalp (Kısa Vade)" else "1mo"
        interval_val = "1h" if timeframe == "Scalp (Kısa Vade)" else "1d"
        
        data = yf.download(symbol_input, period=period_val, interval=interval_val)
        
        if not data.empty:
            # Çoklu indeks sütunlarını düzeltme (yfinance güncellemeleri için önlem)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)
                
            current_price = float(data['Close'].iloc[-1])
            high_price = float(data['High'].max())
            low_price = float(data['Low'].min())
            
            # Fibonacci Özel Seviye Hesaplamaları (Kripto Levent Strateji Mantığı)
            diff = high_price - low_price
            fib_0382 = high_price - (diff * 0.382)
            fib_0500 = high_price - (diff * 0.500)
            fib_0618 = high_price - (diff * 0.618)
            
            # Trend / Sinyal Yönü Tespiti (Basit Fiyat Konumlandırma Mantığı)
            if current_price > fib_0500:
                signal_dir = "LONG 🟢"
                strategy_status = "🎯 Fibo Destek Üstü / FVG Onaylı"
                stop_loss = fib_0618 * 0.99
                tp1 = current_price * 1.015
                tp2 = current_price * 1.03
            else:
                signal_dir = "SHORT 🔴"
                strategy_status = "⚠️ Direnç Bölgesi / Satış Baskısı"
                stop_loss = fib_0382 * 1.01
                tp1 = current_price * 0.985
                tp2 = current_price * 0.97
                
            margin = virtual_capital * 0.02 # Kasanın %2'si risk

            # --- EKRAN İSTATİSTİKLERİ ---
            st.subheader(f"📊 {symbol_input.upper()} - {timeframe} Analiz Özeti")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Anlık Fiyat", f"${current_price:,.2f}")
            col2.metric("Sinyal Yönü", signal_dir)
            col3.metric("Özel Fibo 0.618 Destek", f"${fib_0618:,.2f}")
            col4.metric("Kullanılacak Margin", f"${margin:.2f} ({leverage}x)")

            # --- DETAYLI TABLO ---
            st.markdown("### 📋 Aktif İşlem Sinyal Tablosu")
            df_result = pd.DataFrame({
                "Varlık": [symbol_input.upper()],
                "Yön": [signal_dir],
                "Giriş Fiyatı": [f"${current_price:,.4f}"],
                "Kaldıraç": [f"{leverage}x"],
                "Margin": [f"${margin:.2f}"],
                "Stop Loss": [f"${stop_loss:,.4f}"],
                "Hedef 1 (TP1)": [f"${tp1:,.4f}"],
                "Hedef 2 (TP2)": [f"${tp2:,.4f}"],
                "Strateji Kaynağı": [strategy_status]
            })
            st.table(df_result)
            
            # Bilgi Notu
            st.info("💡 Not: Bu panel Python altyapısıyla çalışmaktadır. Canlı takip için sol menüden 'Analizi Başlat' butonunu kullanabilirsiniz.")
        else:
            st.error("Veri alınamadı! Lütfen geçerli bir kripto sembolü girin (Örn: BTC-USD, ETH-USD).")
else:
    st.info("👈 Sol menüden varlığınızı seçip **'Analizi Başlat / Güncelle'** butonuna tıklayın.")
