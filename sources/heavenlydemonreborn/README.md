# 환생천마 정책 및 고객지원

한국 Google Play 출시를 위한 공식 정책 사이트입니다. 2026-11-06에 별도 저장소(`fellow-survivor-studio/heavenlydemonreborn`, 보관됨)에서 회사 홈페이지 저장소로 옮겼습니다.

공개 주소: **https://fellowsurvivor.com/heavenlydemonreborn/**

현재 문서는 **출시 준비 버전**입니다. 사이트 공개와 게임 출시 요건 충족은 별개입니다. 확정이 필요한 내용은 [출시 체크리스트](LAUNCH_CHECKLIST.md)에 기록했습니다.

| 페이지 | 경로 | 용도 |
| --- | --- | --- |
| 안내 홈 | `/` | 정책·고객지원 탐색 |
| 이용약관 | `/terms/` | 게임 이용계약 |
| 개인정보처리방침 | `/privacy/` | Google Play 개인정보처리방침 URL |
| 계정 및 개인정보 삭제 | `/delete-account/` | Google Play 웹 계정 삭제 URL |
| 구매·청약철회·환불 | `/refund/` | 유료 상품·미성년자·결제 문의 |
| 확률형 아이템 안내 | `/probabilities/` | 실제 확률 공개 전 준비 페이지 |
| 운영정책 | `/operation-policy/` | 이용제한·복구·이의신청 |
| 동의 안내 | `/consent/` | 약관·선택 동의·권한 구분 |
| 고객지원 | `/support/` | 이메일·전화·사업자 정보 |
| 공지·이력 | `/notices/` | 개정·서비스 준비 공지 |

`/privacy/` 등은 위 공개 주소 아래에 붙는 경로입니다. 로그인 없이 접근하는 HTML 페이지이며 별도 방문 분석, 광고 SDK, 외부 폰트, 쿠키 배너, 개인정보 입력 폼을 사용하지 않습니다. 이메일 버튼은 메일 앱의 작성 화면만 열며, 실제 발송은 이용자가 합니다.

## 수정 및 검증

저장소 루트에서 실행합니다. Python 3.10 이상, 추가 패키지 없이 실행합니다.

```sh
python sources/heavenlydemonreborn/build_site.py
python sources/heavenlydemonreborn/validate_site.py
python -m http.server 8765 --bind 127.0.0.1
```

로컬 미리보기 주소는 `http://127.0.0.1:8765/heavenlydemonreborn/`입니다.

- 정책 원문·사업자 정보: `sources/heavenlydemonreborn/content/site.py`
- HTML 공통 구조: `sources/heavenlydemonreborn/build_site.py`
- 디자인: `heavenlydemonreborn/styles.css`, `heavenlydemonreborn/favicon.svg`
- 빌드 결과: `heavenlydemonreborn/` 아래 각 페이지의 `index.html`, `404.html`, `sitemap.xml`, `robots.txt`, `.nojekyll`

원문 수정 후 반드시 재빌드하고 결과 HTML도 함께 커밋합니다. 검증 스크립트는 내부 링크·목차, 메타데이터, 메일 작성 링크, 원문과 빌드 결과의 일치 여부를 확인합니다. 법률 적합성이나 앱의 실제 데이터 처리 동작을 자동 검증하는 도구는 아닙니다.
결과 파일을 추가하거나 지울 때는 저장소의 `scripts/pages-manifest.json` `files` 목록도 함께 고칩니다.

## 게시

회사 홈페이지와 같은 방식으로 게시됩니다. `main`에 푸시하면 Cloudflare가 `https://fellowsurvivor.com/heavenlydemonreborn/`에 배포하고, GitHub Actions **Cloudflare deploy check**가 실제 사이트 파일을 확인합니다. 이전 `github.io` 주소는 GitHub Pages가 대표 주소로 넘겨줍니다.

`sources/`는 Cloudflare에 게시하지 않습니다. 공개 저장소이므로 Firebase 서비스 계정, 결제 검증 키, 실제 이용자 데이터 등을 넣지 않습니다.

## 운영 시 주의할 점

- 게임 출시 전에 최종 시행일·이용등급·통신판매업 신고 사항·상품 조건·실제 확률·SDK 처리 조건을 확정합니다.
- 앱 내 계정 삭제 진입점과 Auth/Firestore의 실제 삭제 처리는 게임에서 구현해야 합니다. 이 정적 사이트는 서버 데이터를 자동 삭제하지 않습니다.
- 약관 동의 기록, 결제 검증, 개인정보 동의·철회도 앱·백엔드의 별도 구현입니다.
- 실제 적용 문서를 개정할 때 적용일과 주요 변경 사항을 공지하고 이전 버전을 별도 URL로 보관합니다. Git 이력만으로 이용자용 과거 약관 열람을 대신하지 않습니다.
- 개인정보처리방침의 웹사이트 호스팅 안내 문구는 2026-11-06 기준 아직 GitHub Pages로 되어 있어, Cloudflare 제공 사실에 맞게 고쳐야 합니다.
