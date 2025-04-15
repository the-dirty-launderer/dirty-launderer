
# firestore.py
# Firestore backend for Dirty Launderer bot
# Uses consistent naming conventions for collections and global config

from google.cloud import firestore

client = firestore.Client()

# Default config used for groups with no overrides
DEFAULT_CONFIG = {
    "domains": {
        "tiktok.com": "proxy",
        "twitter.com": "proxy",
        "youtube.com": "proxy",
        "instagram.com": "clean",
        "facebook.com": "proxy",
        "reddit.com": "proxy",
        "amazon.com": "clean"
    },
    "logging": False
}

# Per-group config stored in collection: dirty_launderer_group_configs
def get_group_config(chat_id):
    doc_ref = client.collection("dirty_launderer_group_configs").document(str(chat_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return DEFAULT_CONFIG

def set_group_domain(chat_id, domain, mode):
    doc_ref = client.collection("dirty_launderer_group_configs").document(str(chat_id))
    doc = doc_ref.get()
    data = doc.to_dict() if doc.exists else DEFAULT_CONFIG.copy()
    data["domains"][domain] = mode
    doc_ref.set(data)

def list_group_domains(chat_id):
    config = get_group_config(chat_id)
    return config.get("domains", {})

def reset_group_config(chat_id):
    doc_ref = client.collection("dirty_launderer_group_configs").document(str(chat_id))
    doc_ref.set(DEFAULT_CONFIG.copy())

def set_group_logging(chat_id, enabled):
    doc_ref = client.collection("dirty_launderer_group_configs").document(str(chat_id))
    doc = doc_ref.get()
    data = doc.to_dict() if doc.exists else DEFAULT_CONFIG.copy()
    data["logging"] = enabled
    doc_ref.set(data)

# Global fallback setting stored in: dirty_launderer_global_config/default
def set_default_mode(mode):
    ref = client.collection("dirty_launderer_global_config").document("default")
    ref.set({"mode": mode})

def get_default_mode():
    ref = client.collection("dirty_launderer_global_config").document("default")
    doc = ref.get()
    if doc.exists:
        return doc.to_dict().get("mode", "proxy")
    return "proxy"
