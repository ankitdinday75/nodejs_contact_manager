from __future__ import annotations

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    exchange: str = Field("coindcx", env="EXCHANGE")
    api_key: str = Field("", env="API_KEY")
    api_secret: str = Field("", env="API_SECRET")
    quote_balance: float = Field(1000.0, env="QUOTE_BALANCE")
    risk_per_trade: float = Field(0.01, env="RISK_PER_TRADE")
    max_daily_loss: float = Field(0.03, env="MAX_DAILY_LOSS")
    leverage: int = Field(1, env="LEVERAGE")
    tp_pct: float = Field(0.02, env="TAKE_PROFIT_PCT")
    sl_pct: float = Field(0.01, env="STOP_LOSS_PCT")
    timezone: str = Field("Asia/Kolkata", env="TIMEZONE")
    model_path: str = Field("models/xgb_SOLUSDT_1h.pkl", env="MODEL_PATH")
    feature_window: int = Field(200, env="FEATURE_WINDOW")
    pred_threshold: float = Field(0.55, env="PRED_THRESHOLD")
    exit_threshold: float = Field(0.45, env="EXIT_THRESHOLD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
