from __future__ import annotations

from fastmcp import FastMCP

from ktx_mcp.tools.datetime_kst import today_kst_payload

mcp = FastMCP(
    name="ktx-mcp",
    instructions=(
        "Korea long-distance rail (KTX, SRT, ITX) timetables from TAGO public data. "
        "Accept station names in English, Korean, Japanese, or Chinese. "
        "Always call get_today_kst before date-sensitive queries."
    ),
)


@mcp.tool(
    name="get_today_kst",
    description=(
        "Return today's date in Korea Standard Time (Asia/Seoul). "
        "Call this before any train schedule query to avoid date hallucination."
    ),
)
def get_today_kst() -> dict[str, str]:
    return today_kst_payload()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
