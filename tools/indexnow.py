#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IndexNow 즉시 색인 통보 — 빙·네이버 등 참여 검색엔진에 URL 변경을 통보한다.

사용법:
    python tools/indexnow.py                 # sitemap.xml의 모든 URL 일괄 통보
    python tools/indexnow.py /magazine/새글/  # 특정 경로(들)만 통보 (절대경로 URL도 허용)
    python tools/indexnow.py --dry-run        # 전송 없이 대상 URL만 출력

키는 build/data.py의 SITE["indexnow_key"]를 단일 소스로 사용하며,
루트의 {key}.txt 파일이 소유 증명으로 함께 배포되어 있어야 한다.
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
from data import SITE  # noqa: E402

DOMAIN = SITE["domain"].rstrip("/")          # https://massagego1.vercel.app
HOST = DOMAIN.replace("https://", "").replace("http://", "")
KEY = SITE["indexnow_key"]
KEY_LOCATION = f"{DOMAIN}/{KEY}.txt"

# IndexNow 참여 엔드포인트. api.indexnow.org 하나만 보내도 참여사 전체로 전파되지만,
# 네이버는 즉시성을 위해 자체 엔드포인트로도 직접 통보한다.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://searchadvisor.naver.com/indexnow",
]

# IndexNow는 1회 요청당 최대 10,000 URL 허용. 여유 있게 분할.
BATCH = 1000


def sitemap_urls():
    """루트 sitemap.xml에서 모든 <loc> URL을 추출한다."""
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def normalize(arg):
    """경로 또는 절대 URL을 도메인 기준 절대 URL로 정규화한다."""
    if arg.startswith("http://") or arg.startswith("https://"):
        return arg
    if not arg.startswith("/"):
        arg = "/" + arg
    return DOMAIN + arg


def submit(urls, dry_run=False):
    urls = list(dict.fromkeys(urls))  # 순서 유지 + 중복 제거
    if not urls:
        print("통보할 URL이 없습니다.")
        return 0
    print(f"대상 {len(urls)}개 URL · host={HOST} · key={KEY[:8]}…")
    for u in urls:
        print(f"  • {u}")
    if dry_run:
        print("\n[--dry-run] 전송하지 않고 종료합니다.")
        return 0

    failures = 0
    for start in range(0, len(urls), BATCH):
        chunk = urls[start:start + BATCH]
        payload = json.dumps({
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": chunk,
        }).encode("utf-8")
        for ep in ENDPOINTS:
            req = urllib.request.Request(
                ep, data=payload,
                headers={"Content-Type": "application/json; charset=utf-8"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    print(f"  ✓ {ep} → HTTP {resp.status} ({len(chunk)}개)")
            except urllib.error.HTTPError as e:
                # 200/202 외에도 일부 엔드포인트는 빈 본문으로 4xx를 줄 수 있어 본문을 함께 출력
                body = e.read().decode("utf-8", "ignore")[:200]
                print(f"  ✗ {ep} → HTTP {e.code} {body}")
                failures += 1
            except urllib.error.URLError as e:
                print(f"  ✗ {ep} → 연결 실패: {e.reason}")
                failures += 1
    return failures


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    urls = [normalize(a) for a in args] if args else sitemap_urls()
    rc = submit(urls, dry_run=dry)
    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
