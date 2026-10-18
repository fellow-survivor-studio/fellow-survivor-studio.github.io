# GitHub Pages 배포 사전 점검 — 2026-10-17

대상: `fellow-survivor-studio/fellow-survivor-studio.github.io`

「회사 소개 페이지 시안 잡기」의 최종 작업을 배포하기 위한 검사입니다. 실제 공개 배포는 진행하지 않았습니다.
기준 원격 커밋은 `6f067dcc9c9034c3312c56625ee8373f3ebcf7bf`입니다.

## 경로 보존 결과

기존 공개 URL **40개**가 HTTP 200으로 응답하고 원래 URL을 유지했습니다. 검사 시점의
응답 본문 SHA-256, 제목, MIME 형식, 최종 URL을 로컬 기준 보고서에 저장했습니다.

| 대상 | 검사 범위 | 결과 |
| --- | --- | --- |
| 회사 홈 | `/`, 기존 `#main`, `#about`, `#projects`, `#contact` | 공개 홈 정상, 새 홈의 기존 앵커 유지 |
| 광고 인증 | `/app-ads.txt` | HTTP 200, `text/plain`, 기존 게시자 코드 유지 |
| 검색 소유권 인증 | `/googleabe82689611d6157.html` | HTTP 200, 기존 내용 유지 |
| Reel Nest 개인정보처리방침 | `/reel-nest/` 및 `en/`, `ja/`, `zh/`, `es/`, `pt/` | 6개 정상 |
| Reel Nest 약관 | `/reel-nest/terms/` 및 동일한 5개 번역 경로 | 6개 정상 |
| 이전 개인정보처리방침 | `/reel-nest/archive/2026-09-11/`, `2026-09-13/` 및 번역 경로 | 12개 정상 |
| 기존 Reel Nest 소개 | `/reel-nest/home/` | 정상, 기존 주소 보존 |
| 환생천마 정책·지원 | `/heavenlydemonreborn/`와 아래 9개 하위 경로 | 10개 정상 |
| 프로젝트 사이트맵 | `/reel-nest/sitemap.xml`, `/heavenlydemonreborn/sitemap.xml` | 2개 정상 |

환생천마 하위 경로: `terms/`, `privacy/`, `delete-account/`, `refund/`, `probabilities/`,
`operation-policy/`, `consent/`, `support/`, `notices/`.

광고 인증 파일의 게시자 코드는 다음과 같습니다.

```text
google.com, pub-4991823555158376, DIRECT, f08c47fec0942fa0
```

`app-ads.txt`, 검색 인증 파일, `.nojekyll`은 원격 기준 내용과 동일합니다.
Windows 작업 파일의 CRLF는 Git의 LF 변환을 반영해 비교합니다.

## 배포 구조

새 페이지는 `/`, `/products/`, `/products/reel-nest/`입니다.
기존 `/reel-nest/`와 `/heavenlydemonreborn/`은 각각 별도 저장소가 제공하는 프로젝트 사이트입니다.
이 저장소 루트에 같은 이름의 폴더를 만들거나 약관을 새 소개 페이지로 덮어쓰지 않습니다.
새 Reel Nest 상세 화면의 개인정보처리방침·이용약관 링크는 기존 공개 URL을 그대로 사용합니다.

배포 대상 정적 파일 **23개**, 내부 링크·리소스 참조 **64개**를 검사했습니다.
새 CSS, 로컬 폰트와 라이선스, 승인된 카드 SVG, 스토어 이미지도 파일 목록에 포함했습니다.
기존 `styles.css`와 사용하지 않는 이전 에셋은 삭제하지 않았습니다.
로컬 HTTP 서버에서도 배포 대상 23개 파일이 모두 200으로 응답했습니다.

Ego Lite에서 세 페이지를 1440px, 390px, 320px 너비로 확인했습니다. 가로 넘침은 없었으며,
회사 홈 → 프로덕트 목록 → Reel Nest 소개, 개인정보처리방침 연결, 홈 문의 앵커 복귀,
FAQ 펼치기 및 이미지·스타일 로딩을 확인했습니다.

`.gitignore`에 `.preview/`와 Python 캐시 제외 규칙을 추가했습니다. 시안, 스크린샷,
검사 보고서는 배포 대상에 넣지 않습니다. 검색 설명의 `유틸리티과` 오타도 수정했습니다.

## 반복 검사

저장소 루트에서 실행합니다. Python 3.10 이상만 있으면 되며 추가 패키지는 필요 없습니다.

```powershell
python -X utf8 scripts/check-pages.py --online --report .preview/pages-preflight-latest.json
```

검사기는 다음 상황에서 실패합니다.

- 인증 파일 삭제·변경, 기존 프로젝트 경로와 폴더 충돌
- 배포 목록에서 빠진 이미지·CSS·폰트, 존재하지 않는 내부 앵커
- Reel Nest 약관·개인정보처리방침·Google Play 다운로드 링크 누락
- 예상하지 않은 Git 추적 파일, 새 도메인·리디렉션·크롤링 설정 파일
- 기존 공개 URL의 오류, 다른 URL로의 리디렉션, 사이트맵에 새로 생긴 미등록 경로

전체 파일 및 보호 경로 정의는 `scripts/pages-manifest.json`에서 관리합니다.
파일/경로를 의도적으로 추가할 때는 이 목록도 검토해서 갱신합니다.
현재 로컬 검사 보고서: `.preview/pages-preflight-20261017/baseline.json`.
최종 재검사 보고서: `.preview/pages-preflight-20261017/final.json`.
검사 오류가 있으면 커밋·푸시 전에 원인을 해결합니다.

검사기 자체도 임시 복사본에서 검증했습니다. 정상 후보 통과, 게시자 코드 변경, 인증 파일 삭제,
기존 앵커 삭제, 잘못된 에셋 경로, 약관 링크 누락, 프로젝트 경로 충돌, 새 CSS의 스테이징 누락,
시안 파일의 잘못된 Git 추가, 원상 복원 후 통과 등 10개 확인을 마쳤습니다. 원본 시안에는
오류 상황을 만들지 않았습니다.

## 다음 배포 작업 순서

1. 배포 직전에 `git fetch origin main`으로 원격 변경을 확인합니다. 다른 변경이 있으면 반영 범위를 다시 검토합니다.
2. 위 `--online` 검사로 그 시점의 기준 보고서를 새로 저장합니다.
3. 아래 명시된 파일만 스테이징하고, `--require-index` 검사까지 통과시킵니다. 현재 사전 준비에서는 스테이징·커밋·푸시를 실행하지 않았습니다.

```powershell
$pagesManifest = Get-Content -Raw -Encoding UTF8 scripts/pages-manifest.json | ConvertFrom-Json
$pagesFiles = @($pagesManifest.files) + @($pagesManifest.maintenance_files)
git add -- $pagesFiles
git diff --cached --check
python -X utf8 scripts/check-pages.py --online --require-index
```

`--require-index`는 새 파일을 빠뜨리거나 스테이징 후 수정한 상태를 실패로 처리합니다.
디렉터리 전체를 일괄 추가하지 않고, 명시된 파일 목록만 사용합니다.

4. 실제 배포를 진행할 때 검토한 변경을 커밋하고 `main`에 푸시합니다. 현재 Pages 설정인
   **Deploy from a branch → main → /(root)**를 유지하고 `pages build and deployment` 성공을 확인합니다.
5. 배포 완료 후 아래 명령으로 새 페이지·정적 파일의 공개 내용과 기존 39개 보존 대상 URL의 본문이 유지되는지 비교합니다.

```powershell
python -X utf8 scripts/check-pages.py --after-deploy --compare .preview/pages-preflight-latest.json --report .preview/pages-postdeploy.json
```

`--after-deploy`는 새 파일이 아직 공개되지 않은 사전 준비 단계에서는 통과하지 않는 것이 정상입니다.
원본 HTML이 바뀌는 `/`는 기존 본문 보존 비교에서 제외하고 새 파일과 비교합니다.
별도 정책 저장소에서 정당한 변경이 있었어도 본문 해시가 달라지면 실패하므로 변경 원인을 확인해야 합니다.

로컬 검사는 GitHub Pages의 실제 배포 결과나 Google의 재크롤링을 대신하지 않습니다.
공개 반영 후 위 검사와 스토어·AdMob 상태 확인을 마쳐야 배포 후 검증이 완료됩니다.

## 도메인 연결 설정 — 2026-10-18

기존 공개 저장소와 GitHub Pages 자동 배포를 유지하고 `fellowsurvivor.com`을 대표 도메인으로 사용합니다.
Cloudflare DNS의 루트 A 4개, AAAA 4개는 GitHub Pages 주소를 가리키며,
`www` CNAME은 `fellow-survivor-studio.github.io`를 가리킵니다. 프록시는 DNS only입니다.
`CNAME` 파일, 세 페이지의 canonical/OG URL, Reel Nest 정책 링크를 대표 도메인에 맞춥니다.

`/reel-nest/`와 `/heavenlydemonreborn/`은 기존 별도 저장소에서 계속 제공합니다.
기존 GitHub 주소의 리디렉션은 같은 경로의 대표 HTTPS 주소로 도착해야 합니다.
도메인 이전은 의도한 리디렉션이므로, 검사기는 호스트만 바뀌고 경로·정책 본문이 보존됐는지 확인합니다.
다른 경로나 다른 사이트로의 이동은 계속 오류로 처리합니다.

도메인 연결 직전 기준 보고서는 `.preview/domain-setup-20261018/baseline.json`입니다.
연결 후에는 다음 명령으로 새 도메인, 기존 GitHub 주소, www 및 HTTP 변형을 검사합니다.

```powershell
python -X utf8 scripts/check-pages.py --after-deploy --compare .preview/domain-setup-20261018/baseline.json --report .preview/domain-setup-20261018/postdeploy.json
```
