# proxy_helper.py
# Loads rotating proxy frontends for services like Nitter, Invidious, Libreddit
# Reads proxies.json and selects a random instance for each service
# Used in each domain handler to dynamically pick live proxy URLs

import json
import random
from pathlib import Path

def get_proxy_instance(service):
    try:
        with open(Path(__file__).parent / "proxies_validated.json", "r") as f:
            proxies = json.load(f)
            candidates = proxies.get(service, [])
            if candidates:
                return random.choice(candidates)
    except Exception:
        pass
    return None