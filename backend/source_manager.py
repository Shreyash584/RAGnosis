import os
import json

SOURCES_FILE = "data/sources.json"


def load_sources():
    if not os.path.exists(SOURCES_FILE):
        return []
    with open(SOURCES_FILE, "r") as f:
        return json.load(f)


def save_sources(sources):
    os.makedirs("data", exist_ok=True)
    with open(SOURCES_FILE, "w") as f:
        json.dump(sources, f, indent=2)


def add_source(source_type, value):
    sources = load_sources()
    sources.append({"type": source_type, "value": value})
    save_sources(sources)


def delete_source(value):
    sources = load_sources()
    sources = [s for s in sources if s["value"] != value]
    save_sources(sources)
