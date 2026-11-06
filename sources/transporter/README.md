# Transporter 정책 페이지 원문

`https://fellowsurvivor.com/products/transporter/`에 게시하는 Transporter(문자 자동전달) 정책·지원 페이지의 원문과 생성·검증 스크립트입니다. 이 폴더는 게시하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| `content/privacy.ko.md`, `content/privacy.en.md` | 개인정보처리방침 / Privacy Policy |
| `content/terms.ko.md`, `content/terms.en.md` | 이용약관 및 운영정책 / Terms of Use and Acceptable Use Policy |
| `content/site.py` | 사업자 정보, 게시일과 문서 버전, 홈·고객지원 페이지, 화면 문구 |
| `build_site.py` | 원문으로 `products/transporter/`(한국어)와 `products/transporter/en/`(영어)를 만듦 |
| `validate_site.py` | 링크, 대표 주소, 언어 짝, 남은 초안 표시, 재생성 결과가 같은지 검사 |

## 고치는 법

1. `content/`의 원문을 고칩니다. 두 언어판의 내용이 다르면 한국어판을 따르므로 함께 고칩니다.
2. 개정이면 `content/site.py`의 `PUBLISHED`를 새 시행일로 바꾸고 `VERSIONS`에 줄을 더합니다. 이전 버전 보관은 회사 스킬의 개정 절차를 따릅니다.
3. 저장소 루트에서 생성과 검사를 돌립니다.

```sh
python -X utf8 sources/transporter/build_site.py
python -X utf8 sources/transporter/validate_site.py
git add -A && python -X utf8 scripts/check-pages.py --require-index
```

`products/transporter/`는 생성 결과라서 직접 고치지 않습니다. `styles.css`와 `favicon.svg`만 생성 대상이 아닙니다.

원문 마크다운에서 `{{DATE}}`는 시행일(예: 2026년 11월 6일, November 6, 2026), `{{ISO}}`는 `2026-11-06` 꼴로 바뀝니다.
