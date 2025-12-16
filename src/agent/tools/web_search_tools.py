from typing import Type
from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field
from agent.utils.llm_utils import zai_llm


class SearchArgs(BaseModel):
    query: str = Field(..., description="Query for searching")


class WebSearch(BaseTool):
    name: str = "web_search"
    description: str = "Tool functions for searching the Internet for content searches"
    args_schema: Type[BaseModel] = SearchArgs

    def _run(self, query: str) -> str:
        try:
            response = zai_llm.web_search.web_search(
                search_engine="search_std",
                search_query=query,
                search_recency_filter="noLimit",
            )
            if len(response.search_result) > 0:
                return "\n\n".join([item.content for item in response.search_result])
            else:
                return "No results found"
        except Exception as e:
            print(f"search failed: {e}")
            return "search failed"

    async def _run(self, query: str):
        return self._run(query)
