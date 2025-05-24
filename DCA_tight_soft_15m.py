import requests
import pandas as pd
import numpy as np
import time

# === TELEGRAM CONFIG ===
BOT_TOKEN = '7762261757:AAHdfupSiXXFMa5E6wpopgsyYEUDbylEB5g'
CHAT_ID = '968054209'

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg})

# === INDICATORS ===
def compute_rsi(series, window=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window).mean()
    avg_loss = pd.Series(loss).rolling(window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_ema(series, span=20):
    return series.ewm(span=span, adjust=False).mean()

def compute_bollinger(series, window=20, num_std=2):
    ma = series.rolling(window).mean()
    std = series.rolling(window).std()
    return ma - num_std * std, ma + num_std * std

def compute_obv(close, volume):
    obv = [0]
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i - 1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=close.index)

# === OKX FETCH FUNCTIONS ===
def get_usdt_swap_symbols():
    url = "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
    response = requests.get(url)
    data = response.json().get("data", [])
    return [item['instId'] for item in data if item['settleCcy'] == 'USDT']

def get_okx_ohlcv(symbol='BTC-USDT-SWAP', interval='24h', limit=100):
    url = f"https://www.okx.com/api/v5/market/candles?instId={symbol}&bar={interval}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        candles = response.json().get("data", [])[::-1]
        
        if not candles or len(candles) < 20:
            print(f"⚠️ No or insufficient data for {symbol}. Skipping.")
            return pd.DataFrame()

        df = pd.DataFrame(candles, columns=[
            'ts_start', 'open', 'high', 'low', 'close', 'volume',
            'quote_volume', 'ignore1', 'ts_end'
        ])
        df['timestamp'] = pd.to_datetime(df['ts_end'].astype('int64'), unit='ms')
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df[['timestamp', 'close', 'volume']]
    
    except Exception as e:
        print(f"❌ Error fetching OHLCV for {symbol}: {e}")
        return pd.DataFrame()

# === STRATEGY CHECK ===
def check_dca_signal(symbol):
    
    df = get_okx_ohlcv(symbol)
    df['rsi'] = compute_rsi(df['close'])
    df['ema20'] = compute_ema(df['close'])
    df['bb_lower'], df['bb_upper'] = compute_bollinger(df['close'])
    df['obv'] = compute_obv(df['close'], df['volume'])
    df['obv_signal'] = (df['obv'].diff() > 0) & (df['obv'].shift(1).diff() < 0)

    last = df.iloc[-1]
    print(f"Checking {symbol} | RSI={last['rsi']:.2f}, Close={last['close']:.2f}, BB_L={last['bb_lower']:.2f}, EMA20={last['ema20']:.2f}, OBV_Signal={last['obv_signal']}")

    # 🔴 Primary (Strict) DCA Buy Signal
    if (
        last['rsi'] < 30 and
        last['close'] < last['bb_lower'] and
        last['close'] < last['ema20'] and
        last['obv_signal']
    ):
        msg = (
            f"🔴 DCA Buy Signal on {symbol}\n"
            f"RSI: {last['rsi']:.2f} | Close: {last['close']:.4f}\n"
            f"BB_L: {last['bb_lower']:.4f} | EMA20: {last['ema20']:.4f}"
        )
        send_telegram(msg)

    # 🟡 Optional: Uptrend Pullback Buy Signal
    elif (
        last['rsi'] < 50 and
        last['close'] < last['ema20'] and
        last['obv_signal']
    ):
        msg = (
            f"🟡 Pullback Opportunity on {symbol}\n"
            f"RSI: {last['rsi']:.2f} | Close: {last['close']:.4f}\n"
            f"EMA20: {last['ema20']:.4f} | OBV Rebound Confirmed ✅"
        )
        send_telegram(msg)



# === MAIN LOOP ===
if __name__ == '__main__':
    while True:
        try:
            symbols = get_usdt_swap_symbols()
            for symbol in symbols:
                try:
                    check_dca_signal(symbol)
                    time.sleep(1.5)  # rate limit handling
                except Exception as e:
                    send_telegram(f"⚠️ Error checking {symbol}: {e}")
        except Exception as big_e:
            send_telegram(f"🚨 Global bot error: {big_e}")
        time.sleep(900)  # wait 15 minutes



