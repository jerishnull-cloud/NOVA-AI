from ddgs import DDGS


def web_search(query):

    try:
        print("🌐 NOVA is searching the web...")

        results = DDGS().text(
            query,
            region="in-en",
            safesearch="moderate",
            max_results=5
        )

        if not results:
            return "I couldn't find any results on the web, sir."

        formatted_results = []

        for result in results:

            title = result.get("title", "No title")
            body = result.get("body", "")
            url = result.get("href", "")

            formatted_results.append(
                f"Title: {title}\n"
                f"Information: {body}\n"
                f"URL: {url}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:

        print("Web search error:", error)

        return f"I couldn't complete the web search, sir. Error: {error}"