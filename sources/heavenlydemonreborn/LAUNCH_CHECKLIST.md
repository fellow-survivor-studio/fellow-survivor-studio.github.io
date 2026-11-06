# 한국 Google Play 출시 체크리스트

확인 기준일: 2026-10-15. 이 파일은 운영·개발자를 위한 준비 문서입니다. 사이트 게시만으로 아래 항목이 구현되거나 인증되는 것은 아닙니다.

## 확정된 범위

- 게임: 환생천마 / 한국 우선 출시 / 목표 등급 15세 이용가
- 계정: Google 로그인 + Firebase Authentication
- 저장: Cloud Firestore 서울 `asia-northeast3`
- 광고: Google AdMob 단독
- 판매: Google Play 인앱결제 + 유료 뽑기
- 사업자: 펠로우서바이버스튜디오, 대표 박인규, 사업자등록번호 773-26-02197
- 연락처: fellow.survivor.studio@gmail.com / 010-2530-1902
- 주소: (16866) 경기 용인시 수지구 용구대로2790번길 7, 302 - S444호
- 통신판매업 신고번호·기관: 발급 대기 중

## 출시 전에 확정할 사항

| 항목 | 필요한 작업 | 반영 위치 |
| --- | --- | --- |
| 서비스·등급 | 실제 서비스 개시일, 최종 등급분류 결과, 연령 제한 방식 확정 | 모든 페이지의 출시 안내, 약관·공지, 앱·스토어 |
| 사업자 표시 | 통신판매업 신고번호 및 신고기관 반영. 해당되는 게임 제작·배급업 등록 등 영업 요건은 관할 기관에 확인 | 공통 하단, 약관·고객지원·구매 안내 |
| 상품 | 가격, 구성, 유효기간, 지급 시점, 유료·무료 재화 사용 순서, 구매 제한·환불 조건 확정 | 구매 화면, 구매·환불 안내 |
| 확률 | 실제 아이템별 확률·조건부 변화·천장·초기화·이월·중복 보상·단계별 계산 공개, 지급 로직과 대조 | 구매 전 게임 화면 및 확률정보 페이지 |
| 개인정보 위탁 | 실제 계약상 Google/Firebase 법인·위탁 업무·재위탁 구조 확인 | 개인정보처리방침 4항 |
| 국외 이전 | 항목·국가·시기·방법·수신자와 연락처·목적·보유기간·거부 방법과 영향 확정 | 개인정보처리방침 5항, 필요한 별도 안내·동의 |
| 보유·삭제 | Auth 로그, 게임 기록, 광고 데이터, 백업의 실제 보유·삭제 주기 확정 | 개인정보처리방침 6항 및 삭제 안내 |
| 동의 | 약관 동의와 개인정보 처리의 법적 근거 구분. 동의가 필요한 수집·제공·국외 이전을 구분하고 선택 항목은 기본 미선택 | 첫 실행·계정 가입·설정 화면 |
| 개인정보 문서 | 최종 시행일과 실제 설정을 반영. 준비 상태 문구를 실제 운영 내용으로 교체 | 모든 관련 페이지 |

Firestore 서울 저장은 Authentication과 AdMob의 국내 전용 처리를 보장하지 않습니다. Firebase 공식 문서상 Authentication은 미국에서 처리됩니다. AdMob의 전체 Google 데이터센터 목록을 해당 앱의 실제 이전 국가로 임의 기재하지 않습니다. 보고서 조회 가능 기간을 원시 개인정보 보유기간으로 대신 쓰지 않습니다.

## 앱 및 백엔드 구현

- [ ] 앱 내에서 접근하기 쉬운 계정 삭제 진입점과 웹 삭제 URL을 제공한다. Google Play는 계정 생성 기능이 있는 앱에 앱 내부와 외부의 삭제 요청 경로를 요구한다.
- [ ] 삭제 시 Firebase Authentication 사용자만 삭제하지 않고 UID와 연결된 Firestore 문서·하위 컬렉션·관련 개인정보를 처리한다. 삭제 확장 기능을 쓰는 경우 경로와 재귀 삭제를 실제 테스트한다.
- [ ] 법정 보존 대상·기간과 일반 게임 데이터를 분리한다. 보존 종료 후 삭제와 백업 복원 시 재생성 방지 절차를 둔다.
- [ ] Firebase Security Rules를 사용자별 접근으로 제한하고 앱의 구매 결과나 클라이언트 UID만 신뢰하지 않는다.
- [ ] Google Play 구매를 안전한 서버에서 검증하고 중복 지급·미지급·환불·취소를 처리한다.
- [ ] 유료 확률형 아이템 구매 전 획득 확률을 가까운 위치에서 쉽게 확인할 수 있게 한다. 실제 확률과 보장 조건이 없는 현재 페이지로 판매를 시작하지 않는다.
- [ ] 필요한 개인정보 동의가 완료되기 전에 해당 SDK 수집·광고 요청이 시작되지 않게 한다. 비개인화 광고도 개인정보 처리가 전혀 없는 광고가 아님을 고려한다.
- [ ] 미성년자의 법정대리인 동의·결제 취소 요청을 처리한다. 15세 이용등급이나 구글 로그인은 법정대리인 동의를 대신하지 않는다.
- [ ] 동의 항목·버전·시각·철회 이력을 필요한 범위에서 기록한다. 마케팅이나 야간 광고 알림을 도입할 때 해당 동의를 구분한다.
- [ ] 앱에서 개인정보처리방침·이용약관·고객지원·확률정보 링크를 실제 단말에서 연다.

## Play Console 제출

- [ ] 개인정보처리방침: `https://fellowsurvivor.com/products/heavenlydemonreborn/privacy/`
- [ ] 계정 삭제 웹 URL: `https://fellowsurvivor.com/products/heavenlydemonreborn/delete-account/`
- [ ] 지원 사이트: `https://fellowsurvivor.com/products/heavenlydemonreborn/support/`
- [ ] 데이터 보안 설문: 로그인·저장·구매·광고 SDK의 실제 전송·수집·공유·삭제 동작과 일치시킨다. 수탁자 처리가 Play 설문의 공유 예외에 해당하는지는 정의를 확인하고, 정책에서 개인정보처리방침과 용어가 다를 수 있음을 고려한다.
- [ ] 광고 포함 여부, 대상 연령, 콘텐츠 등급 설문, 앱 접근 권한·심사용 로그인 방법, 개발자 연락처·사업자 확인을 작성한다.
- [ ] 현재 적용되는 SDK·대상 API·결제 라이브러리·테스트 트랙 및 계정별 출시 접근 요건은 제출 시 Console에서 다시 확인한다. 해당 요건은 수시로 변경될 수 있다.
- [ ] 스토어·게임·광고물의 확률형 아이템 관련 법정 표시를 적용한다. 구체적인 표시 의무와 적용 예외는 현행 법령과 실제 사업 구조로 확인한다.

## 조사 근거

아래 공식 자료를 기준으로 문서를 구성했습니다. 법령의 개정·시행일과 플랫폼 정책 적용일은 실제 제출 시 다시 확인해야 합니다.

| 분야 | 공식 자료 |
| --- | --- |
| 개인정보 수집·계약 근거·위탁·국외 이전·방침 | [개인정보 보호법](https://www.law.go.kr/lsInfoP.do?ancYnChk=0&lsId=011357), 특히 제15조·제22조·제26조·제28조의8·제30조 |
| 사업자 표시·청약철회·환급 | [전자상거래 등에서의 소비자보호에 관한 법률](https://www.law.go.kr/lsInfoP.do?ancYnChk=0&lsId=009318), 특히 제13조·제17조·제18조 및 시행령의 거래기록 보존 조항 |
| 모바일 게임 계약 참고 | [공정거래위원회 모바일게임 표준약관](https://www.ftc.go.kr/www/selectBbsNttView.do?bordCd=201&key=202&nttSn=11196&pageIndex=1&pageUnit=10&searchCnd=all) |
| 확률정보 | [게임산업법 시행령 관련 조문](https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lspttninfSeq=56614), [문체부 확률형 아이템 정보공개 해설서](https://www.mcst.go.kr/site/s_notice/notice/noticeView.jsp?pSeq=17856) |
| Google Play 개인정보 | [사용자 데이터 정책](https://support.google.com/googleplay/android-developer/answer/10144311?hl=ko) |
| Google Play 계정 삭제 | [계정 삭제 요구사항](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en) |
| 결제·확률형 상품 | [Google Play 결제 정책](https://support.google.com/googleplay/android-developer/answer/9858738?hl=en), [안전한 결제 처리](https://developer.android.com/google/play/billing/security) |
| Firebase 처리·위치 | [Firebase 개인정보 보호](https://firebase.google.com/support/privacy/), [Firestore 위치](https://firebase.google.com/docs/firestore/locations) |
| Firebase 삭제 | [Delete User Data 확장 기능](https://firebase.google.com/docs/extensions/official/delete-user-data) |
| AdMob SDK 데이터 | [Google Mobile Ads 데이터 공개 안내](https://developers.google.com/admob/android/privacy/play-data-disclosure?hl=ko) |

통신판매업 신고·등급·확률 수치·실제 SDK 계약 등 아직 제공되지 않은 사실을 문서의 일반적인 문구만으로 확정하지 않습니다.
