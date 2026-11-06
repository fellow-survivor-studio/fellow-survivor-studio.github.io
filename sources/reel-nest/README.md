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

- `content/privacy_policy_<언어>.txt`, `content/terms_of_use_<언어>.txt`: 현재 원문. 앱에 들어가는 문서
  (`app/src/main/assets/legal/` 같은 이름의 파일)와 글자 하나까지 같아야 합니다.
- `content/archive/<문서>_<언어>_<시행일>.txt`: 이전 버전 원문. 날짜는 그 문서의 시행일이고, 날짜마다 한국어 파일이 꼭 있어야 합니다.
- `build_site.py`: 원문으로 `products/reel-nest/privacy/`, `products/reel-nest/terms/`, `products/reel-nest/sitemap.xml`을 만듭니다(두 폴더는 지우고 새로 씀).
- `validate_site.py`: 원문마다 페이지가 있는지, 대표 주소·언어·링크·목차가 맞는지, 사이트맵, 다시 만들어도 같은지 확인합니다.
- `check_live.py`: 실제 사이트에서 새 주소 전부와 옛 주소 넘김(fellowsurvivor.com, github.io 두 경로)을 확인합니다. 읽기만 합니다.
- 페이지 모양: `products/reel-nest/policy.css`(손으로 관리).

## 문서 개정 (예: 1.3.0 출시일)

저장소 맨 위 폴더에서 실행합니다. Python 3.10 이상, 추가 설치 없음(Windows는 `-X utf8`).

1. 바꿀 문서의 현재 원문 6개를 `content/archive/`로 복사합니다. 이름의 날짜는 **지금 문서의 시행일**입니다.
   예: 현재 처리방침(시행일 2026-11-06) → `content/archive/privacy_policy_ko_2026-11-06.txt` 등 6개.
2. 새 원문(앱에 넣은 파일과 같은 내용)을 `content/`에 덮어씁니다.
3. 생성하고 검사합니다.
   ```sh
   python -X utf8 sources/reel-nest/build_site.py
   python -X utf8 sources/reel-nest/validate_site.py
   ```
4. 새로 생긴 파일을 `scripts/pages-manifest.json`에 등록합니다. 보관 원문은 `maintenance_files`, 새 이전 버전 페이지
   (`products/reel-nest/<privacy|terms>/archive/<시행일>/…/index.html` 6개)는 `files`, 날짜는 `privacy_archives`·`terms_archives`에 넣습니다.
5. 전체 검사 후 작업 줄기에서 커밋하고 변경 요청(PR)을 엽니다. 바뀐 문장을 보여 주고 사용자 승인을 받은 뒤 합칩니다.
   ```sh
   git add -A && python -X utf8 scripts/check-pages.py --require-index
   ```
6. 합친 뒤 GitHub Actions **Cloudflare deploy check** 성공을 확인하고, 실제 사이트를 확인합니다.
   ```sh
   python -X utf8 sources/reel-nest/check_live.py
   ```

앱 출시와 같은 날 게시하고, 약관 변경은 약관 제3조의 공지 기간을 따릅니다.
`products/reel-nest/privacy/`, `terms/` 아래 HTML은 생성 결과이므로 직접 고치지 않습니다.

## 게시

회사 홈페이지와 같습니다. `main`에 합치면 Cloudflare가 배포하고, **Cloudflare deploy check**가 실제 사이트 파일을 하나씩 대조해
다르면 GitHub이 실패 메일을 보냅니다. `sources/`는 게시하지 않습니다.
