from __future__ import annotations

import os
from dataclasses import dataclass

from ktx_mcp.adapters.tago_client import TagoApiError, load_service_key


@dataclass(frozen=True, slots=True)
class Settings:
    transport: str = "stdio"
    host: str = "0.0.0.0"
    port: int = 8080
    default_locale: str = "en"
    tago_service_key: str | None = None
    sync_secret: str | None = None

    @classmethod
    def from_env(cls) -> Settings:
        port_raw = os.environ.get("KTX_MCP_PORT", "8080")
        return cls(
            transport=os.environ.get("KTX_MCP_TRANSPORT", "stdio").strip().lower(),
            host=os.environ.get("KTX_MCP_HOST", "0.0.0.0"),
            port=int(port_raw),
            default_locale=os.environ.get("KTX_MCP_DEFAULT_LOCALE", "en"),
            tago_service_key=_load_tago_service_key(),
            sync_secret=_optional("SYNC_SECRET"),
        )


def _optional(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None


def _load_tago_service_key() -> str | None:
    try:
        return load_service_key()
    except TagoApiError:
        return None
