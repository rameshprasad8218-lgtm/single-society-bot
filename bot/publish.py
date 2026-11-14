import os, time, requests

API = "https://graph.instagram.com/v21.0"


def ready():
    return bool(os.getenv("IG_ACCESS_TOKEN"))


def publish(image_url, caption):
    tok = os.environ["IG_ACCESS_TOKEN"]
    uid = os.getenv("IG_USER_ID") or requests.get(
        f"{API}/me", params={"fields": "user_id", "access_token": tok}, timeout=30
    ).json()["user_id"]
    r = requests.post(f"{API}/{uid}/media", data={"image_url": image_url, "caption": caption, "access_token": tok}, timeout=60)
    r.raise_for_status()
    cid = r.json()["id"]
    for _ in range(12):  # wait until Instagram has fetched the image
        s = requests.get(f"{API}/{cid}", params={"fields": "status_code", "access_token": tok}, timeout=30).json()
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"Instagram could not process image: {s}")
        time.sleep(5)
    r = requests.post(f"{API}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok}, timeout=60)
    r.raise_for_status()
    return r.json()["id"]


def refresh_token():
    """Long-lived tokens last 60 days; call within that window to extend."""
    tok = os.environ["IG_ACCESS_TOKEN"]
    r = requests.get("https://graph.instagram.com/refresh_access_token",
                     params={"grant_type": "ig_refresh_token", "access_token": tok}, timeout=30)
    r.raise_for_status()
    return r.json()
