# Fellow Survivor Studio

펠로우서바이버스튜디오의 회사 소개 및 프로덕트 웹사이트입니다.
HTML과 CSS로 구성하며, 별도의 빌드·패키지 설치·JavaScript 없이 실행됩니다. 본문 웹폰트는 로컬 파일로 제공합니다.

- [공식 웹사이트](https://fellow-survivor-studio.github.io/)
- [GitHub 저장소](https://github.com/fellow-survivor-studio/fellow-survivor-studio.github.io)
- [Reel Nest Google Play](https://play.google.com/store/apps/details?id=studio.fellowsurvivor.reelnest)

## 페이지 구성

| 경로 | 소스 | 내용 |
| --- | --- | --- |
| `/` | `index.html` | 브랜드 메시지, 회사 소개, 개발 분야, 문의 |
| `/products/` | `products/index.html` | 유틸리티(Reel Nest·Paper Markdown)과 게임(환생천마) 목록 |
| `/products/reel-nest/` | `products/reel-nest/index.html` | Reel Nest 기능, 스크린샷, Free·Pro 비교, FAQ, 다운로드 안내 |

홈페이지 메뉴에서 프로덕트 목록으로 이동하고, Reel Nest 소개 영역의 이미지나 자세히 보기 링크에서 상세 소개를 볼 수 있습니다.
Reel Nest 목록에서는 설명 바로 아래에 자세히 보기 링크를 배치하고, 그다음에 Google Play 다운로드를 아이콘이 있는 텍스트 링크로 표시합니다. 이용약관은 상세 소개 페이지에서 안내합니다.
홈페이지에는 개별 제품을 노출하지 않으며, 유틸리티·게임 소개 섹션에서 프로덕트 목록의 해당 카테고리로 이동합니다.

### 별도로 운영하는 정책·지원 페이지

아래 주소는 이 저장소의 제품 소개 페이지와 별도로 운영합니다.
기존 주소를 유지하고, 필요한 곳에서 전체 URL로 연결합니다.

| 페이지 | 주소 |
| --- | --- |
| Reel Nest 개인정보처리방침 | [정책 페이지](https://fellow-survivor-studio.github.io/reel-nest/) |
| Reel Nest 이용약관 | [이용약관](https://fellow-survivor-studio.github.io/reel-nest/terms/) |
| 환생천마 정책 및 고객지원 | [정책·지원 페이지](https://fellow-survivor-studio.github.io/heavenlydemonreborn/) |
| Paper Markdown for Windows | [제품 저장소](https://github.com/fellow-survivor-studio/paper-markdown-for-windows) |

Reel Nest 소개는 `/products/reel-nest/`, 개인정보처리방침은 `/reel-nest/`입니다.
소개 페이지를 수정할 때 정책 페이지 주소를 덮어쓰지 않습니다.

## 로컬 미리보기

Python이 설치된 환경에서 저장소 루트를 작업 폴더로 열고 실행합니다.

```sh
python -m http.server 8765 --bind 127.0.0.1
```

- [회사 소개](http://127.0.0.1:8765/)
- [프로덕트 목록](http://127.0.0.1:8765/products/)
- [Reel Nest 소개](http://127.0.0.1:8765/products/reel-nest/)

서버를 종료하려면 실행한 터미널에서 `Ctrl+C`를 누릅니다.
페이지 이동과 디렉터리 경로를 확인할 수 있도록 HTML 파일을 직접 여는 대신 로컬 서버로 확인합니다.

## 파일 구조

```text
.
├── index.html                       # 회사 소개
├── styles.css                       # 이전 시안 스타일 (현재 페이지에서 사용하지 않음)
├── home.css                         # 공통 기본 스타일·헤더·푸터 및 회사 홈 레이아웃
├── product.css                      # 프로덕트 목록·상세 페이지 스타일
├── reel-nest.css                    # Reel Nest 상세 전용 레이아웃·반응형 스타일
├── favicon.svg                      # 스튜디오 파비콘
├── products/
│   ├── index.html                   # 프로덕트 목록
│   └── reel-nest/
│       └── index.html               # Reel Nest 소개
├── assets/
│   ├── fonts/                       # Pretendard Regular 및 SIL OFL 라이선스
│   ├── google-play-icon.png         # Google Play 다운로드 링크 아이콘
│   ├── studio-everyday.jpg          # 홈 첫 화면 사진
│   ├── studio-utilities.svg         # 링크·사진·문서를 정돈한 유틸리티 그래픽
│   ├── studio-utilities.jpg         # 이전 유틸리티 사진 (현재 사용하지 않음)
│   ├── studio-games.jpg             # 게임 분야 사진
│   ├── reel-nest-icon.png           # 제공받은 원본 아이콘
│   ├── reel-nest-screen-1.png        # Google Play 소개 이미지
│   ├── reel-nest-screen-2.png
│   ├── reel-nest-screen-3.png
│   └── reel-nest-screen-4.png
├── app-ads.txt                      # 앱 광고 판매자 인증
├── googleabe82689611d6157.html       # Google Search Console 소유권 확인
└── .nojekyll                        # Jekyll 처리 없이 정적 파일 제공
```

로컬 `.preview/` 폴더는 시안 캡처와 작업용 스크립트 보관용이며, 웹사이트 실행에 필요하지 않습니다.
배포 파일에 포함하지 않습니다.

## 콘텐츠와 디자인 수정

| 수정할 내용 | 파일 |
| --- | --- |
| 회사 소개 문구, 브랜드 프레이즈, 개발 분야, 문의 안내 | `index.html` |
| 프로덕트 카테고리, 제품 정보, 출시 상태 | `products/index.html` |
| Reel Nest 기능, Free·Pro 비교, FAQ | `products/reel-nest/index.html` |
| 공통 컬러·폰트·헤더·푸터, 회사 홈 레이아웃과 반응형 스타일 | `home.css` |
| 프로덕트 페이지 레이아웃과 반응형 스타일 | `product.css` |
| Reel Nest 상세 레이아웃과 반응형 스타일 | `reel-nest.css` |
| 아이콘 및 스토어 이미지 | `assets/` |

### 브랜드 컬러

Reel Nest 아이콘의 차콜 블랙과 오렌지를 대표 컬러로 사용합니다.
회사 홈은 흰색과 밝은 회색을 바탕으로 하고, 오렌지는 카테고리명과 문의 버튼에 사용합니다.
얇은 고정 헤더, 큰 사진과 브랜드 문구, 중앙 정렬 회사 소개,
사진과 설명이 교차하는 유틸리티·게임 섹션, 문의 영역 순서로 구성합니다.
세 페이지 모두 흰색·밝은 회색 배경과 같은 헤더·푸터를 사용하며, 섹션 번호와 영문 장식 라벨은 사용하지 않습니다.
프로덕트 목록은 카테고리별로 제품 이미지와 설명을 넓게 교차 배치합니다.
Reel Nest 상세는 중앙 정렬 제품 소개, 실제 스토어 이미지와 기능 설명, 추가 기능, Free·Pro 비교표, FAQ, 다운로드·정책 안내 순서로 구성합니다.
스토어 이미지는 데스크톱에서 세 열로, 모바일에서는 좌우로 넘길 수 있는 영역으로 표시합니다. 다운로드는 Google Play 아이콘이 있는 텍스트 링크로 제공합니다.

### 브랜드 메시지와 카테고리

- 메인 프레이즈: **당신의 오늘이 조금 더 편해지고, 조금 더 즐거워지는 것.** 첫 화면에 세 줄로 배치합니다.
- 메인 보조 문구: **거창한 변화보다, 당신의 하루에 닿는 작은 차이를 믿습니다.** 메인 제목 아래에 두 줄로 배치합니다.
- 헤더에는 **Fellow Survivor Studio** 회사명을 표시합니다.
- 회사명은 Fellow Survivor Studio로 사용하며, 단어별 의미 풀이와 감성적인 서사 대신 개발 분야·기능·사용성을 설명합니다.
- 회사 소개: **일상의 편리함과 즐거움을 만듭니다.** “조금 더”는 메인 프레이즈에만 사용합니다.
- **유틸리티** — 일상에 필요한 기능을 편하게. Reel Nest와 Paper Markdown을 분류합니다. 모바일과 데스크톱 도구를 모두 포함합니다.
- **게임** — 쉬는 시간을 즐겁게. 환생천마를 분류합니다.
- 카테고리 주소: `/products/#utilities`, `/products/#games`. 회사 홈과 Reel Nest 상세 페이지의 돌아가기 링크에서도 사용합니다.

| 용도 | CSS 변수 | 색상 |
| --- | --- | --- |
| 기본 배경 | — | `#FFFFFF` |
| 보조 배경 | — | `#F6F7F8` |
| 본문·어두운 영역 | `--ink` | `#1C1D1E` |
| 대표 포인트 | `--accent` | `#FF5F0A` |
| 주요 버튼 배경 (흰색 글자) | `--button-bg` | `#CC4800` |
| 주요 버튼 호버 | `--button-hover` | `#B83F00` |

공통 컬러 변수는 `home.css`의 `:root`에서 관리합니다.
본문 문단과 표 내용은 로컬 Pretendard Regular를 사용하며 제목과 굵은 글씨는 기존 시스템 글꼴을 유지합니다. 폰트 원본은 [Pretendard v1.3.9](https://github.com/orioncactus/pretendard/tree/v1.3.9)이며 라이선스는 `assets/fonts/Pretendard-LICENSE.txt`에 포함합니다.
홈은 `home.css`만 불러오고, 프로덕트 목록·상세는 `home.css` 다음에 `product.css`를 불러옵니다.
Reel Nest 상세는 마지막에 `reel-nest.css`를 추가로 불러옵니다.
`styles.css`는 이전 시안 보관용이며 현재 세 페이지에서는 불러오지 않습니다.
헤더·푸터는 각 HTML 파일에 포함되어 있습니다. 공통 메뉴나 회사 정보를 바꾸면 세 페이지에 함께 반영합니다.

### 홈 이미지 출처

홈 사진은 회사의 실제 사무실이나 제품 사진이 아닌 분야 소개용 이미지입니다. Unsplash License로 제공되는 사진을 로컬 에셋으로 저장했습니다.
유틸리티 영역은 자체 제작 SVG 그래픽을 사용합니다. 링크·사진·문서 카드만 배치하며 텍스트 라벨과 폴더 장식은 사용하지 않습니다. 실제 앱 화면이 아닌 분야 소개용 그래픽입니다.

| 파일 | 사진가 및 원본 |
| --- | --- |
| `assets/studio-everyday.jpg` | [Guillermo Latorre / Unsplash](https://unsplash.com/photos/iPNiy0D5KjE) |
| `assets/studio-utilities.jpg` (현재 미사용) | [ergonofis / Unsplash](https://unsplash.com/photos/tdnYk4qOGhc) |
| `assets/studio-games.jpg` | [RoonZ nl / Unsplash](https://unsplash.com/photos/5ZH9FheQ9t8) |

레이아웃 참고: [토스 공식 사이트](https://toss.im/). 토스의 이미지, 로고, 소스는 사용하지 않습니다.

### 제품 정보 관리

Google Play로 이동하는 링크에는 [Google 제공 컬러 아이콘](https://www.gstatic.com/images/branding/product/2x/play_96dp.png)을 사용합니다. 원본 색상과 비율을 유지하며, 텍스트와 중복해서 읽히지 않도록 장식 이미지로 처리합니다.

프로덕트 목록의 Reel Nest 이미지는 실제 스토어 소개 이미지입니다. Paper Markdown의 문서 그래픽과 환생천마의 검 그래픽은 카테고리 소개용으로 제작한 그래픽이며 실제 제품 화면이 아닙니다.

Reel Nest의 기능, Android 요구사항, 무료·Pro 조건은
[Google Play 등록 정보](https://play.google.com/store/apps/details?id=studio.fellowsurvivor.reelnest&hl=ko)를 기준으로
2026년 10월 17일 확인했습니다. 스크린샷 4장도 같은 등록 페이지의 소개 이미지입니다.

- Android 7.0 이상을 지원합니다.
- 무료 버전은 광고 시청 후 5분 동안 다운로드 기능을 이용하며, Nest 저장 공간은 최대 500MB입니다.
- Pro는 월간·연간 구독으로 다운로드 전 광고 시청 단계를 없애고 앱 내 Nest 저장 용량 제한을 해제합니다. 실제 저장 가능 용량은 기기 여유 공간과 시스템 제한에 따라 달라집니다.
- 구독 가격은 페이지에 고정하지 않고 앱 또는 Google Play에서 확인하도록 안내합니다.
- 클라우드 백업·동기화·데이터 복구 서비스를 제공하지 않는다는 안내를 유지합니다.

앱 기능이나 구독 조건이 변경되면 스토어와 소개 페이지를 함께 갱신합니다.
환생천마는 현재 페이지에서 **출시 준비**로 표시하며, 정책·고객지원 링크는 목록에 노출하지 않습니다. 출시 상태는 프로덕트 목록에 반영합니다.
문의 이메일과 사업자 정보도 세 페이지에서 일치하도록 유지합니다.

## 배포

GitHub Pages 설정은 **Settings → Pages → Deploy from a branch → main → / (root)**를 사용합니다.

대표 도메인은 `https://fellowsurvivor.com/`이며 루트 `CNAME` 파일에 호스트명을 유지합니다.
Cloudflare는 DNS를 관리하고, 실제 정적 호스팅과 자동 배포는 기존 GitHub Pages가 담당합니다.
루트 A/AAAA 레코드는 GitHub Pages 주소를, `www` CNAME은 `fellow-survivor-studio.github.io`를 가리키며 DNS only로 설정합니다.
기존 `github.io` 주소와 `www`·HTTP 주소가 대표 HTTPS 도메인의 동일한 경로로 이동하는지도 배포 후 검사합니다.

1. 로컬에서 세 페이지와 연결 경로를 확인합니다.
2. 배포할 소스와 에셋을 검토해 커밋하고 `main`에 푸시합니다. 로컬 `.preview/` 작업 파일은 제외합니다.
3. GitHub Actions의 **pages build and deployment** 완료 여부를 확인합니다.
4. [공식 웹사이트](https://fellowsurvivor.com/)에서 변경된 페이지와 이미지가 표시되는지 확인합니다.

로컬 미리보기의 변경은 `main`에 푸시하고 Pages 배포가 완료되어야 공개 사이트에 반영됩니다.

2026-10-17 사전 검사 결과와 명시적 파일 추가·배포 후 재검사 절차는
[Pages 배포 사전 점검](docs/pages-preflight.md)에 정리되어 있습니다.
배포 전에 다음 명령으로 인증 파일, 기존 정책 주소, 새 페이지의 리소스 누락을 검사합니다.

```powershell
python -X utf8 scripts/check-pages.py --online --report .preview/pages-preflight-latest.json
```

`scripts/pages-manifest.json`에 배포 파일과 보호 경로가 정의되어 있습니다.
스테이징 후 `--require-index` 옵션으로 새 파일 누락까지 확인합니다. `.preview/`는 Git에서 제외됩니다.

### 배포 전 확인

- 데스크톱과 모바일에서 가로 넘침, 글자 잘림, 이미지 누락이 없는지 확인합니다.
- 회사 소개 → 프로덕트 목록 → Reel Nest 소개 이동과 돌아가기 링크를 확인합니다.
- Google Play 다운로드, 문의 이메일, 정책·지원 링크를 확인합니다.
- Reel Nest FAQ 펼치기와 섹션 이동을 확인합니다.
- 키보드 포커스와 본문 건너뛰기 링크를 확인합니다.

### 루트에서 유지할 파일

다음 파일은 홈페이지 개편과 관계없이 기존 경로에 유지합니다.

- `app-ads.txt`: 광고 구매자가 개발자 웹사이트 루트에서 확인하는 판매자 인증 파일입니다. 제품 하위 경로로 옮기지 않습니다.
- `googleabe82689611d6157.html`: Google Search Console 소유권 확인 파일입니다.
- `.nojekyll`: 정적 파일을 Jekyll 처리 없이 제공합니다.
