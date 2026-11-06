# Reel Nest 개인정보처리방침·이용약관

Android 앱 Reel Nest의 개인정보처리방침과 이용약관 웹페이지입니다.
2026-11-06에 별도 저장소(`fellow-survivor-studio/reel-nest`, 주소 `/reel-nest/`)에서 이 저장소로 옮겼습니다.

## 주소

| 문서 | 주소 |
| --- | --- |
| 개인정보처리방침 | https://fellowsurvivor.com/products/reel-nest/privacy/ (다른 언어: `en/`, `ja/`, `zh/`, `es/`, `pt/`) |
| 이용약관 | https://fellowsurvivor.com/products/reel-nest/terms/ (다른 언어 같음) |
| 이전 버전 | `/products/reel-nest/privacy/archive/<시행일>/…`, `/products/reel-nest/terms/archive/<시행일>/…` |
| 제품 소개 | https://fellowsurvivor.com/products/reel-nest/ (손으로 관리, 생성 스크립트가 건드리지 않음) |

한국어가 각 주소의 기본이고, 다른 언어는 그 아래 언어 코드 경로에 있습니다.
현재 문서에는 이전 버전 목록이 붙고, 이전 버전은 검색에서 빠지며(`noindex`) 사이트맵에도 넣지 않습니다.

옛 주소는 영구히 새 주소로 넘어갑니다(`scripts/cloudflare-build.sh`의 `_redirects`). 1.3.0 이전 앱과 이전 문서가 옛 주소를 안내하고,
처리방침이 "변경 전 방침도 같은 웹페이지에서 확인할 수 있다"고 약속하기 때문에 넘김 규칙은 지우지 않습니다.

| 옛 주소 | 새 주소 |
| --- | --- |
| `fellow-survivor-studio.github.io/reel-nest/…` | GitHub Pages가 `fellowsurvivor.com/reel-nest/…`로 넘긴 뒤 아래 규칙을 탐 |
| `/reel-nest/`, `/reel-nest/<언어>/` | `/products/reel-nest/privacy/…` |
| `/reel-nest/archive/<시행일>/…` | `/products/reel-nest/privacy/archive/<시행일>/…` |
| `/reel-nest/terms/…` (이전 버전 포함) | `/products/reel-nest/terms/…` |
| `/reel-nest/home/…` | `/products/reel-nest/` |
| `/reel-nest/sitemap.xml` | `/products/reel-nest/sitemap.xml` |

## 파일

- `content/privacy_policy_<언어>.txt`, `content/terms_of_use_<언어>.txt`: **가장 최근 판** 원문(시행일이 게시일보다 뒤일 수 있음). 앱에 들어가는 문서
  (`app/src/main/assets/legal/` 같은 이름의 파일)와 글자 하나까지 같아야 합니다.
- `content/archive/<문서>_<언어>_<시행일>.txt`: 이전 버전 원문. 날짜는 그 문서의 시행일이고, 날짜마다 한국어 파일이 꼭 있어야 합니다.
- `content/revisions/<문서>_<언어>_<시행일>.txt`: 개정 안내 페이지에 싣는 변경 사유(평문, 빈 줄로 문단 구분).
- `build_site.py`: 원문으로 `products/reel-nest/privacy/`, `products/reel-nest/terms/`, `products/reel-nest/sitemap.xml`을 만듭니다(두 폴더는 지우고 새로 씀).
- `validate_site.py`: 원문마다 페이지가 있는지, 대표 주소·언어·링크·목차, 적용 기간 표시, 사이트맵, 다시 만들어도 같은지 확인합니다.
- `sync_manifest.py`: `scripts/pages-manifest.json`의 Reel Nest 항목(생성 페이지, 원문, 이전 버전 날짜)을 실제 파일에 맞춥니다.
- `check_live.py`: 실제 사이트에서 새 주소 전부와 옛 주소 넘김(fellowsurvivor.com, github.io 두 경로)을 확인합니다. 읽기만 합니다.
- 페이지 모양: `products/reel-nest/policy.css`(손으로 관리).

### 개정 안내 페이지

이용약관 제3조 2항(2026-11-14 개정부터)은 변경 사유, 변경된 약관 전문, 변경 전 약관과 변경 전후 비교를 약관 웹페이지에서 볼 수 있다고 약속합니다.
그래서 2026-11-14 이후 시행되는 약관 개정마다 `terms/revision/<시행일>/`(6개 언어)에 개정 안내 페이지를 만듭니다(`REVISION_PAGES_SINCE`).
순서: "○○부터 적용되는 개정 버전입니다" → 변경 사유 → 변경 전후 비교표(직전 판과 문단 단위 자동 비교) → 개정 버전 전문. 이 페이지는 계속 남습니다.

### 적용 기간 표시 (개인정보처리방침·이용약관)

개정본을 시행일보다 먼저 공개할 수 있도록(이용약관은 7일 전 공개, 처리방침은 출시일 전에 게시 가능), 날짜가 지나면
틀려지는 말("현행", "이전 버전", "시행 예정")을 쓰지 않고 판마다 **적용 기간**만 적습니다(`DATED_DOCS`).
그래서 시행일이 와도 사이트를 고칠 일이 없고, 시행일 전에 합쳐도 내용이 맞습니다.
- 문서 페이지(`privacy/`, `terms/`): 가장 최근 판을 본문으로 두고, 제목 아래에 시행일과 적용 기간("2026년 11월 14일부터"),
  맨 위에 최근 두 판의 적용 기간과 링크, 아래에 모든 판의 적용 기간 목록을 둡니다.
- 지난 판(`<문서>/archive/<시행일>/`): "적용 기간: 2026년 10월 25일 ~ 2026년 11월 13일"처럼 적고 '이전 버전' 표시를 하지 않습니다.
  하루만 적용된 판은 날짜 하나만 적습니다(예: 처리방침 2026년 11월 6일 판).
- 적용 기간의 끝은 다음 판 시행일의 전날로 자동 계산합니다.
변경 사유 파일이 없으면 생성이 멈춥니다.

## 문서 개정

저장소 맨 위 폴더에서 실행합니다. Python 3.10 이상, 추가 설치 없음(Windows는 `-X utf8`).
`products/reel-nest/privacy/`, `terms/` 아래 HTML은 생성 결과이므로 직접 고치지 않습니다.

### 개정 원문 넣기 (시행일이 게시일과 같든 뒤든 같은 방법)

1. 바꿀 문서의 지금 원문 6개를 `content/archive/<문서>_<언어>_<지금 원문의 시행일>.txt`로 옮깁니다.
   예: 처리방침(시행일 2026-11-06) → `content/archive/privacy_policy_ko_2026-11-06.txt` 등 6개.
2. 새 원문(앱에 넣은 파일과 같은 내용)을 `content/<문서>_<언어>.txt`로 둡니다.
3. 이용약관(2026-11-14 이후 개정)이면 변경 사유 6개를 `content/revisions/terms_of_use_<언어>_<새 시행일>.txt`로 둡니다.
4. 아래 "생성·검사·게시"를 합니다. 시행일이 게시일보다 뒤인 약관도 이날 한 번만 게시하면 됩니다.

### 생성·검사·게시

1. 생성하고 검사한 뒤, 검사 목록을 맞춥니다.
   ```sh
   python -X utf8 sources/reel-nest/build_site.py
   python -X utf8 sources/reel-nest/validate_site.py
   python -X utf8 sources/reel-nest/sync_manifest.py
   git add -A && python -X utf8 scripts/check-pages.py --require-index
   ```
2. 작업 줄기에서 커밋하고 변경 요청(PR)을 엽니다. 바뀐 문장을 보여 주고 사용자 승인을 받은 뒤 합칩니다.
3. 합친 뒤 GitHub Actions **Cloudflare deploy check** 성공을 확인하고, 실제 사이트를 확인합니다.
   ```sh
   python -X utf8 sources/reel-nest/check_live.py
   ```

앱 출시와 같은 날 게시하고, 약관 변경은 약관 제3조의 공지 기간을 따릅니다.

## 게시

회사 홈페이지와 같습니다. `main`에 합치면 Cloudflare가 배포하고, **Cloudflare deploy check**가 실제 사이트 파일을 하나씩 대조해
다르면 GitHub이 실패 메일을 보냅니다. `sources/`는 게시하지 않습니다.
