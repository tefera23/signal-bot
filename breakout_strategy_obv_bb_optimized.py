import ccxt
import pandas as pd
import ta
import time
import requests
import datetime
import os
import csv

LOG_FILE = "breakout_signals.csv"

# Create log file if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['datetime', 'symbol', 'signal', 'price'])

# === CONFIGURATION ===
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'
ASSETS = ['AIDOGE-USDT-SWAP',
'SATS-USDT-SWAP',
'NFT-USDT-SWAP',
'CAT-USDT-SWAP',
'PEPE-USDT-SWAP',
'SHIB-USDT-SWAP',
'BONK-USDT-SWAP',
'LUNC-USDT-SWAP',
'X-USDT-SWAP',
'FLOKI-USDT-SWAP',
'DOGS-USDT-SWAP',
'NEIRO-USDT-SWAP',
'BOME-USDT-SWAP',
'SLP-USDT-SWAP',
'VRA-USDT-SWAP',
'MEME-USDT-SWAP',
'FOXY-USDT-SWAP',
'HMSTR-USDT-SWAP',
'NOT-USDT-SWAP',
'DOG-USDT-SWAP',
'MEW-USDT-SWAP',
'DEGEN-USDT-SWAP',
'DUCK-USDT-SWAP',
'MEMEFI-USDT-SWAP',
'IOST-USDT-SWAP',
'ULTI-USDT-SWAP',
'TURBO-USDT-SWAP',
'SWEAT-USDT-SWAP',
'BUZZ-USDT-SWAP',
'RSR-USDT-SWAP',
'DGB-USDT-SWAP',
'SWELL-USDT-SWAP',
'ZENT-USDT-SWAP',
'PENGU-USDT-SWAP',
'RVN-USDT-SWAP',
'USTC-USDT-SWAP',
'ZIL-USDT-SWAP',
'VELO-USDT-SWAP',
'ONE-USDT-SWAP',
'CSPR-USDT-SWAP',
'PEOPLE-USDT-SWAP',
'GALA-USDT-SWAP',
'T-USDT-SWAP',
'ANIME-USDT-SWAP',
'ORBS-USDT-SWAP',
'LOOKS-USDT-SWAP',
'PIPPIN-USDT-SWAP',
'GPS-USDT-SWAP',
'WAXP-USDT-SWAP',
'RDNT-USDT-SWAP',
'ACH-USDT-SWAP',
'ATH-USDT-SWAP',
'SWARMS-USDT-SWAP',
'JELLYJELLY-USDT-SWAP',
'SOLV-USDT-SWAP',
'JST-USDT-SWAP',
'ALPHA-USDT-SWAP',
'CHZ-USDT-SWAP',
'MOODENG-USDT-SWAP',
'NC-USDT-SWAP',
'VINE-USDT-SWAP',
'ZEREBRO-USDT-SWAP',
'FLM-USDT-SWAP',
'SUNDOG-USDT-SWAP',
'BR-USDT-SWAP',
'ACT-USDT-SWAP',
'AVAAI-USDT-SWAP',
'ZK-USDT-SWAP',
'ARC-USDT-SWAP',
'OL-USDT-SWAP',
'GMT-USDT-SWAP',
'GUN-USDT-SWAP',
'GRIFFAIN-USDT-SWAP',
'BRETT-USDT-SWAP',
'NEIROETH-USDT-SWAP',
'SLERF-USDT-SWAP',
'BIO-USDT-SWAP',
'WOO-USDT-SWAP',
'CFX-USDT-SWAP',
'BIGTIME-USDT-SWAP',
'GOAT-USDT-SWAP',
'ENJ-USDT-SWAP',
'PRCL-USDT-SWAP',
'W-USDT-SWAP',
'CRO-USDT-SWAP',
'SIGN-USDT-SWAP',
'MERL-USDT-SWAP',
'GRT-USDT-SWAP',
'LRC-USDT-SWAP',
'BABY-USDT-SWAP',
'CATI-USDT-SWAP',
'ICX-USDT-SWAP',
'GODS-USDT-SWAP',
'BLUR-USDT-SWAP',
'AEVO-USDT-SWAP',
'CVC-USDT-SWAP',
'BICO-USDT-SWAP',
'STRK-USDT-SWAP',
'PYTH-USDT-SWAP',
'BAT-USDT-SWAP',
'TNSR-USDT-SWAP',
'ONT-USDT-SWAP',
'ALCH-USDT-SWAP',
'DOGE-USDT-SWAP',
'AIXBT-USDT-SWAP',
'COOKIE-USDT-SWAP',
'PNUT-USDT-SWAP',
'HBAR-USDT-SWAP',
'LUNA-USDT-SWAP',
'MAJOR-USDT-SWAP',
'JOE-USDT-SWAP',
'PUFFER-USDT-SWAP',
'CETUS-USDT-SWAP',
'1INCH-USDT-SWAP',
'YGG-USDT-SWAP',
'IOTA-USDT-SWAP',
'PARTI-USDT-SWAP',
'ID-USDT-SWAP',
'MAGIC-USDT-SWAP',
'SHELL-USDT-SWAP',
'ALGO-USDT-SWAP',
'J-USDT-SWAP',
'POL-USDT-SWAP',
'MINA-USDT-SWAP',
'TRX-USDT-SWAP',
'MOVE-USDT-SWAP',
'ZETA-USDT-SWAP',
'GLM-USDT-SWAP',
'XLM-USDT-SWAP',
'ZRX-USDT-SWAP',
'AI16Z-USDT-SWAP',
'SAND-USDT-SWAP',
'STORJ-USDT-SWAP',
'MANA-USDT-SWAP',
'ARB-USDT-SWAP',
'SONIC-USDT-SWAP',
'PERP-USDT-SWAP',
'SCR-USDT-SWAP',
'CELO-USDT-SWAP',
'KNC-USDT-SWAP',
'PROMPT-USDT-SWAP',
'WCT-USDT-SWAP',
'POPCAT-USDT-SWAP',
'FLOW-USDT-SWAP',
'UXLINK-USDT-SWAP',
'JUP-USDT-SWAP',
'BNT-USDT-SWAP',
'OM-USDT-SWAP',
'S-USDT-SWAP',
'APE-USDT-SWAP',
'LSK-USDT-SWAP',
'RON-USDT-SWAP',
'XTZ-USDT-SWAP',
'IMX-USDT-SWAP',
'ARKM-USDT-SWAP',
'ETHFI-USDT-SWAP',
'PI-USDT-SWAP',
'WIF-USDT-SWAP',
'DYDX-USDT-SWAP',
'ACE-USDT-SWAP',
'EOS-USDT-SWAP',
'SUSHI-USDT-SWAP',
'ADA-USDT-SWAP',
'CTC-USDT-SWAP',
'SNX-USDT-SWAP',
'LQTY-USDT-SWAP',
'CRV-USDT-SWAP',
'OP-USDT-SWAP',
'INIT-USDT-SWAP',
'THETA-USDT-SWAP',
'CORE-USDT-SWAP',
'API3-USDT-SWAP',
'STX-USDT-SWAP',
'BAND-USDT-SWAP',
'LDO-USDT-SWAP',
'KAITO-USDT-SWAP',
'ONDO-USDT-SWAP',
'EIGEN-USDT-SWAP',
'BAL-USDT-SWAP',
'USDC-USDT-SWAP',
'WLD-USDT-SWAP',
'AGLD-USDT-SWAP',
'ME-USDT-SWAP',
'BADGER-USDT-SWAP',
'MASK-USDT-SWAP',
'UMA-USDT-SWAP',
'MORPHO-USDT-SWAP',
'FARTCOIN-USDT-SWAP',
'GRASS-USDT-SWAP',
'VIRTUAL-USDT-SWAP',
'JTO-USDT-SWAP',
'ETHW-USDT-SWAP',
'QTUM-USDT-SWAP',
'XRP-USDT-SWAP',
'FXS-USDT-SWAP',
'AXS-USDT-SWAP',
'NEAR-USDT-SWAP',
'TIA-USDT-SWAP',
'FIL-USDT-SWAP',
'ZRO-USDT-SWAP',
'RAY-USDT-SWAP',
'LAYER-USDT-SWAP',
'CVX-USDT-SWAP',
'TON-USDT-SWAP',
'GAS-USDT-SWAP',
'BERA-USDT-SWAP',
'SUI-USDT-SWAP',
'IP-USDT-SWAP',
'DOT-USDT-SWAP',
'ATOM-USDT-SWAP',
'RENDER-USDT-SWAP',
'ICP-USDT-SWAP',
'LPT-USDT-SWAP',
'UNI-USDT-SWAP',
'APT-USDT-SWAP',
'VANA-USDT-SWAP',
'NEO-USDT-SWAP',
'MOVR-USDT-SWAP',
'SSV-USDT-SWAP',
'AR-USDT-SWAP',
'ORDI-USDT-SWAP',
'NMR-USDT-SWAP',
'INJ-USDT-SWAP'
]  # Truncated for brevity
TIMEFRAME = '15m'
LOOP_INTERVAL = 15 * 60  # 1 hour

# === TELEGRAM NOTIFIER ===
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

# === LOGGING FUNCTION ===
def log_signal(timestamp, symbol, signal, price):
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, symbol, signal, price])

# === FETCH DATA ===
def fetch_ohlcv(exchange, symbol, timeframe='1h', limit=100):
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# === APPLY INDICATORS (BB + OBV only) ===
def apply_indicators(df):
    bb = ta.volatility.BollingerBands(df['close'], window=20)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['obv'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
    return df

# === CHECK BREAKOUT (BB + OBV only, Optimized) ===
# === CHECK BREAKOUT (Tightened) ===
def check_breakout(df, symbol):
    close = df['close'].iloc[-1]
    volume = df['volume'].iloc[-1]
    obv_now = df['obv'].iloc[-1]
    obv_prev = df['obv'].iloc[-5]
    bb_upper = df['bb_upper'].iloc[-1]
    bb_lower = df['bb_lower'].iloc[-1]

    # Filter low-volume and micro-price coins
    if volume * close < 50000 or close < 0.01:
        return

    obv_change = (obv_now - obv_prev) / abs(obv_prev + 1e-9)

    msg = None
    signal = None

    if close > bb_upper and obv_change > 0.02:
        signal = 'breakout-long'
        msg = f"📈 BREAKOUT LONG: {symbol} at {close:.4f}"
    elif close < bb_lower and obv_change < -0.02:
        signal = 'breakout-short'
        msg = f"📉 BREAKOUT SHORT: {symbol} at {close:.4f}"
    elif abs(close - bb_upper) / bb_upper < 0.0025 and obv_change > 0.02:
        signal = 'near-long'
        msg = f"👀 NEAR BREAKOUT (Long): {symbol} at {close:.4f}"
    elif abs(close - bb_lower) / bb_lower < 0.0025 and obv_change < -0.02:
        signal = 'near-short'
        msg = f"👀 NEAR BREAKOUT (Short): {symbol} at {close:.4f}"

    if signal:
        send_telegram(msg)
        log_signal(df['timestamp'].iloc[-1], symbol, signal, close)
        print(msg)



# === STRATEGY RUNNER ===
def run_strategy():
    exchange = ccxt.okx({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'swap',
        },
    })

    for symbol in ASSETS:
        try:
            df = fetch_ohlcv(exchange, symbol, timeframe=TIMEFRAME)
            df = apply_indicators(df)
            check_breakout(df, symbol)
        except Exception as e:
            print(f"❌ Error with {symbol}: {e}")

# === LOOP ===
if __name__ == "__main__":
    while True:
        print(f"\n🔄 Running breakout check at {datetime.datetime.now()}")
        run_strategy()
        print(f"✅ Sleeping for {LOOP_INTERVAL//60} minutes...\n")
        time.sleep(LOOP_INTERVAL)
