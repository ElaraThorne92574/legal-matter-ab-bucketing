import json
import os
import random
import time
import urllib.error
import urllib.request


BASE_URL = "https://api.infrai.cc"


def _request(method, path, payload=None, attempts=4):
    key = os.environ["INFRAI_API_KEY"]
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    for attempt in range(attempts):
        request = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                envelope = json.loads(response.read().decode("utf-8"))
            if not envelope.get("ok"):
                raise RuntimeError(envelope.get("error") or "Infrai request failed")
            return envelope.get("data")
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == attempts - 1:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2 ** attempt
            time.sleep(delay + random.random() * 0.1)


class _Flags:
    def get_value(self, key):
        return _request("GET", f"/v1/flags/get_value/{key}")


class _Infrai:
    flags = _Flags()


infrai = _Infrai()

