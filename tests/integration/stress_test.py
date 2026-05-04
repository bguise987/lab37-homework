#!/usr/bin/env python3
"""
Stress test: measures maximum requests per second the backend can handle.

Usage:
    python tests/integration/stress_test.py [BASE_URL]

The backend must be running before executing this script:
    cd backend && uvicorn main:app --reload --port 8000

Uses seeded credentials (alice / password1) and hammers GET /api/recipes
at increasing concurrency levels, reporting peak requests per second.
"""

import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"

CREDENTIALS = {"username": "alice", "password": "password1"}
TEST_DURATION_SECS = 5
CONCURRENCY_LEVELS = [1, 2, 5, 10, 20, 50]


def login(base_url: str) -> str:
    data = json.dumps(CREDENTIALS).encode()
    req = urllib.request.Request(
        f"{base_url}/api/auth/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read())
    return body["token"]


@dataclass
class Result:
    concurrency: int
    successes: int
    errors: int
    duration: float
    rps: float = field(init=False) # Requests per second

    def __post_init__(self):
        self.rps = self.successes / self.duration if self.duration > 0 else 0.0


def _worker(base_url: str, token: str, stop_at: float) -> tuple[int, int]:
    """Hammer GET /api/recipes until stop_at, return (successes, errors)."""
    url = f"{base_url}/api/recipes"
    headers = {"Authorization": f"Bearer {token}"}
    ok = err = 0
    while time.monotonic() < stop_at:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5):
                ok += 1
        except Exception:
            err += 1
    return ok, err


def benchmark(base_url: str, token: str, concurrency: int) -> Result:
    stop_at = time.monotonic() + TEST_DURATION_SECS
    total_ok = total_err = 0
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(_worker, base_url, token, stop_at) for _ in range(concurrency)]
        for f in as_completed(futures):
            ok, err = f.result()
            total_ok += ok
            total_err += err
    elapsed = time.monotonic() - start
    return Result(concurrency, total_ok, total_err, elapsed)


def main():
    print(f"Stress test  →  {BASE_URL}")
    print(f"Duration per level: {TEST_DURATION_SECS}s  |  Concurrency levels: {CONCURRENCY_LEVELS}\n")

    print("Logging in... ", end="", flush=True)
    try:
        token = login(BASE_URL)
    except Exception as e:
        print(f"FAILED\n\nCould not log in: {e}")
        print(f"Is the backend running at {BASE_URL}?")
        sys.exit(1)
    print("OK\n")

    results: list[Result] = []
    print(f"{'Concurrency':>12}  {'Requests':>10}  {'Errors':>8}  {'RPS':>10}")
    print("-" * 48)

    for concurrency in CONCURRENCY_LEVELS:
        r = benchmark(BASE_URL, token, concurrency)
        results.append(r)
        print(f"{r.concurrency:>12}  {r.successes:>10}  {r.errors:>8}  {r.rps:>10.1f}")

    best = max(results, key=lambda r: r.rps)
    print("\n" + "=" * 48)
    print(f"Peak throughput: {best.rps:.1f} req/s  (concurrency={best.concurrency})")
    if best.errors > 0:
        error_pct = 100 * best.errors / (best.successes + best.errors)
        print(f"  Warning: {best.errors} errors at peak ({error_pct:.1f}% error rate)")


if __name__ == "__main__":
    main()
