from __future__ import annotations

import ccxt

from ..config import settings
from ..utils.logger import get_logger

log = get_logger("exchange")


def get_exchange(name: str | None = None, pro: bool = False):
    exch_name = (name or settings.exchange).lower()
    params = {"enableRateLimit": True}
    if settings.api_key:
        params["apiKey"] = settings.api_key
    if settings.api_secret:
        params["secret"] = settings.api_secret

    if pro:
        try:
            import ccxtpro  # type: ignore

            return getattr(ccxtpro, exch_name)(params)
        except Exception as exc:  # pragma: no cover - optional dependency
            log.warning("ccxt.pro not available (%s); falling back to REST.", exc)

    return getattr(ccxt, exch_name)(params)
