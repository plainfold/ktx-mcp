from __future__ import annotations

import os
from dataclasses import dataclass

from ktx_mcp.adapters.tago_client import TagoApiError, load_service_key
from ktx_mcp.env_util import env_value, read_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    transport: str = "stdio"
    host: str = "0.0.0.0"
    port: int = 8080
    default_locale: str = "en"
    database_url: str | None = None
    tago_service_key: str | None = None
    sync_secret: str | None = None

    @classmethod
    def from_env(cls) -> Settings:
        dotenv = read_dotenv()
        port_raw = os.environ.get("KTX_MCP_PORT", dotenv.get("KTX_MCP_PORT", "8080"))
        return cls(
            transport=os.environ.get("KTX_MCP_TRANSPORT", dotenv.get("KTX_MCP_TRANSPORT", "stdio"))
            .strip()
            .lower(),
            host=os.environ.get("KTX_MCP_HOST", dotenv.get("KTX_MCP_HOST", "0.0.0.0")),
            port=int(port_raw),
            default_locale=os.environ.get(
                "KTX_MCP_DEFAULT_LOCALE", dotenv.get("KTX_MCP_DEFAULT_LOCALE", "en")
            ),
            database_url=env_value("DATABASE_URL", dotenv=dotenv),
            tago_service_key=_load_tago_service_key(),
            sync_secret=env_value("SYNC_SECRET", dotenv=dotenv),
        )


def _load_tago_service_key() -> str | None:
    try:
        return load_service_key()
    except TagoApiError:
        return None
