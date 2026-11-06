# Transporter 출시 체크리스트(정책 페이지)

| 쓰는 곳 | 값 |
| --- | --- |
| Play Console → 앱 콘텐츠 → 개인정보처리방침 | `https://fellowsurvivor.com/products/transporter/privacy/` |
| Play Console → 데이터 보안 → 계정 삭제 URL | 해당 없음(앱에 계정이 없음) |
| Play Console → 스토어 등록정보 → 웹사이트 | `https://fellowsurvivor.com` (AdMob `app-ads.txt` 확인 위치라 바꾸지 않음) |
| 지원 이메일·지원 사이트 | `fellow.survivor.studio@gmail.com`, `https://fellowsurvivor.com/products/transporter/support/` |
| 앱 안 링크(설정 > 정보) | 개인정보처리방침 `…/transporter/privacy/`, 이용약관 `…/transporter/terms/` (영어 화면은 `…/transporter/en/privacy/`, `…/transporter/en/terms/`) |

## 앱과 맞춰야 할 것

- 처리방침은 AdMob 광고, Firebase Crashlytics, 사용 통계(Google Analytics for Firebase)를 전제로 씁니다. 페이지의 「출시 준비 안내」가 이 항목이 그 기능을 넣은 앱 버전부터 적용된다고 알립니다. 기능을 넣고 실제 동작이 확정되면 안내를 지우고 문서를 다시 확인합니다.
- 앱 설정에 「사용 통계 보내기」, 「광고 동의 바꾸기」, 「내 정보 공유 안 함」 칸이 있어야 문서와 맞습니다.
- 통계 도구의 광고 ID 수집은 끕니다(처리방침은 통계 식별자를 무작위 설치 식별자로만 적음). 통계 보관 기간은 2개월입니다.
- 유료 기능(Google Play 결제)을 넣으면 처리방침에 구매 정보를, 이용약관에 환불 기준을 더합니다.
