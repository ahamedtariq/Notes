import httpx
from urllib.parse import quote

class ExternalAPIError(Exception):
    pass

# async def generate_summary(topic: str) -> str:
#     encoded_topic = quote(topic.strip())
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"

#     async with httpx.AsyncClient(timeout=10) as client:
#         try:
#             response = await client.get(url)
#             response.raise_for_status()
#             data = response.json()

#             return data.get("extract", "No summary available")

#         except httpx.RequestError:
#             raise ExternalAPIError("Wikipedia service unavailable")
#         except httpx.HTTPStatusError:
#             raise ExternalAPIError("Invalid topic or Wikipedia error")


async def generate_summary(query: str) -> str:
    url = "https://api.duckduckgo.com/"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params={
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        })
        response.raise_for_status()

        data = response.json()
        return data.get("AbstractText", "No summary available")