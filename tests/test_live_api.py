"""
Live smoke tests — call the real Olostep API to verify each plugin workflow.

Skipped automatically if OLOSTEP_API_KEY is not set.

Run with:
    OLOSTEP_API_KEY=your_key pytest tests/test_live_api.py -v
"""
import pytest

Olostep = pytest.importorskip(
    "olostep",
    reason="Install the optional olostep SDK to run live API tests",
).Olostep


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client(api_key):
    return Olostep(api_key=api_key)


# ---------------------------------------------------------------------------
# Scrape
# ---------------------------------------------------------------------------

class TestScrapeSkill:
    def test_basic_scrape_markdown(self, client):
        """scrape skill: scrape a simple page as markdown."""
        result = client.scrapes.create(
            "https://example.com",
            formats=["markdown"],
        )
        # API may normalise URL with a trailing slash
        assert result.url.rstrip("/") == "https://example.com"
        assert result.markdown_content
        assert "Example" in result.markdown_content

    def test_scrape_returns_credits_consumed(self, client):
        """scrape result exposes credits_consumed field."""
        result = client.scrapes.create("https://example.com", formats=["markdown"])
        assert isinstance(result.credits_consumed, (int, float))

    def test_scrape_html_format(self, client):
        """scrape skill: html format returns raw HTML."""
        result = client.scrapes.create("https://example.com", formats=["html"])
        # Field name is html_content on ScrapeResult
        assert result.html_content
        assert "<html" in result.html_content.lower()


# ---------------------------------------------------------------------------
# Map (sitemap)
# ---------------------------------------------------------------------------

class TestMapSkill:
    def test_basic_map(self, client):
        """map skill: return sitemap URLs for a domain."""
        result = client.maps.create(url="https://example.com")
        # Sitemap object exposes initial_urls_count and _initial_urls
        assert result.initial_urls_count >= 0
        # Initial URLs should be a list of strings
        assert isinstance(result._initial_urls, list)


# ---------------------------------------------------------------------------
# Answers
# ---------------------------------------------------------------------------

class TestAnswersSkill:
    def test_basic_answer(self, client):
        """answers skill: returns an answer and sources for a factual question."""
        result = client.answers.create(task="What is the capital of France?")
        assert result.answer
        # answer should contain Paris
        answer_text = str(result.answer).lower()
        assert "paris" in answer_text
        assert isinstance(result.sources, list)

    def test_structured_json_answer(self, client):
        """answers skill: json_format returns structured dict."""
        import json
        result = client.answers.create(
            task="What is the capital of France?",
            json_format={"capital": "", "country": ""},
        )
        # answer is a JSON string when json_format is used; parse it
        parsed = json.loads(result.answer)
        assert isinstance(parsed, dict)
        assert "capital" in parsed


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------

class TestBatchSkill:
    def test_batch_create_and_poll(self, client):
        """batch skill: create a batch and poll its status."""
        urls = ["https://example.com", "https://example.org"]
        batch = client.batches.create(urls=urls)
        assert batch.id
        assert batch.status  # e.g. "in_progress"

        # Poll status via info()
        info = client.batches.info(batch.id)
        assert info.id == batch.id
        assert info.status in ("in_progress", "completed", "failed", "queued")
        assert info.total_urls == len(urls)
