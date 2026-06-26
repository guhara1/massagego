#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""구글 Indexing API 통보 — URL 발행/갱신·삭제를 구글에 직접 알린다.

구글은 IndexNow에 미참여하므로, 빙·네이버용 tools/indexnow.py와 별개로 운용한다.

사전 준비 (1회):
  1) Google Cloud 콘솔에서 프로젝트 생성 → "Indexing API" 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드 → tools/google-service-account.json 으로 저장
     (이 파일은 .gitignore 처리되어 커밋되지 않는다)
  3) Google Search Console > 설정 > 사용자 및 권한에서
     서비스 계정 이메일(client_email)을 "소유자"로 추가
  4) 의존성 설치:  pip install google-auth

사용법:
  python tools/google_index.py                  # sitemap.xml의 모든 URL 갱신 통보
  python tools/google_index.py /magazine/새글/   # 특정 경로(들)만 통보
  python tools/google_index.py --delete /폐기/   # 삭제 통보(URL_DELETED)
  python tools/google_index.py --dry-run         # 전송 없이 대상만 출력

주의: 기본 일일 할당량은 200건. 대량 통보 시 할당량 상향 신청이 필요하다.
"""
import os
import sys
import re
import json
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
from data import SITE  # noqa: E402

DOMAIN = SITE["domain"].rstrip("/")
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
CRED_PATH = (os.environ.get("GOOGLE_INDEX_CREDENTIALS")
             or os.path.join(ROOT, "tools", "google-service-account.json"))


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def normalize(arg):
    if arg.startswith("http://") or arg.startswith("https://"):
        return arg
    if not arg.startswith("/"):
        arg = "/" + arg
    return DOMAIN + arg


def access_token():
    """서비스 계정 JSON으로 OAuth2 액세스 토큰을 발급한다."""
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except ImportError:
        sys.exit("의존성 누락: pip install google-auth  (먼저 설치하세요)")
    if not os.path.exists(CRED_PATH):
        sys.exit(f"서비스 계정 키가 없습니다: {CRED_PATH}\n"
                 f"  → GOOGLE_INDEX_CREDENTIALS 환경변수로 경로를 지정하거나 위 경로에 저장하세요.")
    creds = service_account.Credentials.from_service_account_file(CRED_PATH, scopes=SCOPES)
    creds.refresh(Request())
    return creds.token


def publish(token, url, action):
    payload = json.dumps({"url": url, "type": action}).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=payload, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:300]
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def main():
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    action = "URL_DELETED" if "--delete" in argv else "URL_UPDATED"
    paths = [a for a in argv if not a.startswith("--")]
    urls = list(dict.fromkeys([normalize(a) for a in paths] if paths else sitemap_urls()))

    if not urls:
        print("통보할 URL이 없습니다.")
        return
    print(f"대상 {len(urls)}개 URL · type={action}")
    for u in urls:
        print(f"  • {u}")
    if dry:
        print("\n[--dry-run] 전송하지 않고 종료합니다.")
        return

    token = access_token()
    ok = fail = 0
    for u in urls:
        status, body = publish(token, u, action)
        if status == 200:
            ok += 1
            print(f"  ✓ {u}")
        else:
            fail += 1
            print(f"  ✗ {u} → HTTP {status} {body}")
    print(f"\n완료: 성공 {ok} · 실패 {fail}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
