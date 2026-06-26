# tools — 색인 통보 유틸리티

사이트 빌드(`build/`)는 의존성 0을 유지하고, 색인 통보 도구만 별도로 둔다.
도메인·키는 모두 `build/data.py`의 `SITE`를 단일 소스로 읽는다.

## indexnow.py — 빙·네이버 즉시 색인 (의존성 없음)

IndexNow 참여 엔진(Bing·Naver·Seznam·Yandex 등)에 URL 변경을 즉시 통보한다.

```bash
python tools/indexnow.py                  # sitemap.xml의 전체 URL 일괄 통보
python tools/indexnow.py /magazine/새글/   # 특정 경로만
python tools/indexnow.py --dry-run         # 대상만 출력
```

- 키 파일 `/{indexnow_key}.txt`이 **라이브(200)** 인 상태에서 실행할 것. (배포 후)
- 키는 `build/data.py`의 `indexnow_key`. 빌드 시 루트에 키 파일이 자동 생성된다.

## google_index.py — 구글 Indexing API (google-auth 필요)

구글은 IndexNow 미참여이므로 별도 경로로 통보한다.

```bash
pip install google-auth
python tools/google_index.py                 # sitemap 전체 갱신 통보
python tools/google_index.py /magazine/새글/  # 특정 경로
python tools/google_index.py --delete /폐기/  # 삭제 통보
python tools/google_index.py --dry-run        # 대상만 출력
```

**1회 설정**
1. Google Cloud → 프로젝트 생성 → **Indexing API** 사용 설정
2. 서비스 계정 생성 → JSON 키 다운로드 → `tools/google-service-account.json` 저장
   (`.gitignore` 처리되어 커밋되지 않음. 환경변수 `GOOGLE_INDEX_CREDENTIALS`로 경로 변경 가능)
3. Search Console → 설정 → 사용자/권한 → 서비스 계정 이메일(`client_email`)을 **소유자**로 추가
4. 일일 할당량 기본 200건. 대량 통보 시 상향 신청 필요.

> 참고: 더 안정적인 구글 색인 경로는 **Search Console에 sitemap.xml 제출**이다.
> Indexing API는 공식적으로 JobPosting/BroadcastEvent용이라 일반 페이지는 비공식 동작.
