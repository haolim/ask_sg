from enum import Enum

class UserIntent(str, Enum):
    KNOWLEDGE_BASE = "historical_hdb_transactions"
    WEB_SEARCH = "current_news_and_live_data"


