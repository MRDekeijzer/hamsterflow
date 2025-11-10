from hamsterflow.config import AppSettings, get_settings


def test_default_feed_present() -> None:
    settings = AppSettings()
    assert "https://feeds.feedburner.com/TechCrunch/" in [str(url) for url in settings.rss_feeds]


def test_get_settings_cached() -> None:
    first = get_settings()
    second = get_settings()
    assert first is second
