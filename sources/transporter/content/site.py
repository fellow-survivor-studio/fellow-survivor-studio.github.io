"""Transporter policy site settings and the short pages (home, support) in Korean and English.

The long documents live next to this file as Markdown:
privacy.ko.md, privacy.en.md (개인정보처리방침 / Privacy Policy) and
terms.ko.md, terms.en.md (이용약관 및 운영정책 / Terms of Use and Acceptable Use Policy).
Keep them in sync with the app. When the Korean and English texts differ, the Korean text prevails.
"""

COMPANY = {
    "name": "펠로우서바이버스튜디오",
    "name_en": "Fellow Survivor Studio",
    "representative": "박인규",
    "registration": "773-26-02197",
    "address": "(16866) 경기 용인시 수지구 용구대로2790번길 7, 302 - S444호",
    "address_en": "Unit 302-S444, 7 Yonggudae-ro 2790beon-gil, Suji-gu, Yongin-si, Gyeonggi-do 16866, Republic of Korea",
    "email": "fellow.survivor.studio@gmail.com",
}

# Publication (and effective) date of the current documents. Change it, rebuild, and add a row to VERSIONS.
PUBLISHED = "2026-11-06"
VERSIONS = [("1.0", "2026-11-06")]


def section(title, body):
    return {"title": title, "body": body.strip()}


def page(slug, nav, title, description, sections=(), markdown=None, intro=None):
    return dict(slug=slug, nav=nav, title=title, description=description, sections=list(sections), markdown=markdown, intro=intro)


HOSTING_KO = """
<p>이 웹사이트는 Cloudflare를 통해 제공되며, 이전 주소(fellow-survivor-studio.github.io)는 GitHub Pages가 이 주소로 연결합니다. 웹페이지 자체에 광고·방문 분석 SDK, 입력정보를 전송하는 문의 폼 또는 추적 쿠키를 넣지 않습니다. 사이트 전송을 맡는 Cloudflare와 이전 주소를 연결하는 GitHub는 접속 시 IP 등 서비스 제공·보안 정보를 각자의 정책에 따라 처리할 수 있습니다. 자세한 내용은 <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare 개인정보처리방침</a>과 <a href="https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement">GitHub 개인정보처리방침</a>을 확인해 주세요.</p>
<p>이메일 링크를 누르면 이용자의 메일 앱이 열립니다. 이용자가 직접 메일을 보내기 전에는 요청 내용이 운영자에게 전송되지 않습니다.</p>"""

HOSTING_EN = """
<p>This website is served through Cloudflare, and the former address (fellow-survivor-studio.github.io) is forwarded here by GitHub Pages. The pages contain no ads, visitor analytics, forms that send what you type, or tracking cookies. Cloudflare, which delivers the site, and GitHub, which forwards the former address, may process your IP address and other information needed to provide and secure their services under their own policies. See the <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare Privacy Policy</a> and the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement">GitHub Privacy Statement</a>.</p>
<p>Email links open your own mail app. Nothing is sent to us until you send the email yourself.</p>"""

LANGS = {
    "ko": {
        "html_lang": "ko", "og_locale": "ko_KR", "path": "", "other": "en", "switch": "English", "switch_lang": "en",
        "site_name": "Transporter", "brand_sub": "정책 및 고객지원", "home_label": "Transporter 정책 및 고객지원 홈",
        "skip": "본문으로 건너뛰기", "menu": "문서 메뉴", "toc": "이 페이지에서", "toc_label": "문서 목차", "help": "도움이 필요하신가요? →",
        "open_toc": "문서 목차 열기", "top": "맨 위로 ↑", "eyebrow": "TRANSPORTER · 문자 자동전달",
        "published": "게시일", "version": "문서 버전",
        "notice_title": "출시 준비 안내",
        "notice": "Transporter는 Google Play 출시를 준비하고 있습니다. 개인정보처리방침의 광고(Google AdMob), 구독(Google Play 결제), 오류 기록(Firebase Crashlytics), 사용 통계(Firebase) 항목과 이용약관의 무료 한도·광고·구독 조건은 그 기능을 넣은 앱 버전부터 적용됩니다. 이 사이트의 문의 안내는 지금 이용할 수 있습니다.",
        "support_subject": "[Transporter] 문의",
        "not_found_title": "페이지를 찾을 수 없습니다.", "not_found_body": "주소가 바뀌었거나 없는 페이지입니다.", "not_found_home": "정책 및 고객지원 홈으로",
        "pages": [
            page("", "안내 홈", "정책 및 고객지원", "Transporter(문자 자동전달)의 개인정보처리방침, 이용약관과 고객지원 안내입니다.", [
                section("필요한 안내를 찾아보세요", """
<div class="cards">
<a class="card" href="{{HOME}}privacy/"><strong>개인정보처리방침</strong><span>폰 안에만 저장하는 문자와, 광고·오류·통계로 Google에 가는 정보</span></a>
<a class="card" href="{{HOME}}terms/"><strong>이용약관 및 운영정책</strong><span>허용되는 사용, 금지 행위, 책임의 한계</span></a>
<a class="card" href="{{HOME}}support/"><strong>고객지원</strong><span>문의 방법과 문의할 때 적어 주실 것</span></a>
</div>"""),
                section("Transporter는", """
<p>Transporter(한국어 이름 「문자 자동전달」)는 폰에 온 문자를 이용자가 정한 조건에 따라 이용자가 정한 번호로 보내 주는 Android 앱입니다. 받은 문자와 전달 기록은 폰 안에만 저장하며, 운영자는 문자를 받는 서버를 두지 않습니다.</p>
<p>회원 가입이 없어 계정을 만들거나 지울 필요가 없습니다. 폰 안의 기록은 앱에서 바로 지울 수 있고, 앱을 지우면 모두 지워집니다.</p>"""),
                section("이 웹사이트", HOSTING_KO),
                section("운영 사업자", "{{BUSINESS}}"),
            ]),
            page("privacy", "개인정보처리방침", "개인정보처리방침", "Transporter가 다루는 개인정보, 보유 기간, Google로 전송되는 정보와 이용자의 권리를 안내합니다.",
                 markdown="privacy.ko.md", intro="한눈에 보기"),
            page("terms", "이용약관", "이용약관 및 운영정책", "Transporter를 쓸 때 지켜야 할 규칙과 위반 시 조치, 서비스 변경과 책임의 한계를 정합니다.",
                 markdown="terms.ko.md", intro="이 정책에 대해"),
            page("support", "고객지원", "고객지원", "앱 이용 문의, 원치 않는 문자 신고, 개인정보 요청을 이메일로 받습니다.", [
                section("문의하기", """
<p><a class="button" href="{{SUPPORT_MAIL}}">문의 이메일 작성</a></p>
<p>이메일: <a href="mailto:{{EMAIL}}">{{EMAIL}}</a></p>
<p>문의는 7일 안에, 개인정보 열람·삭제 등 요청은 10일 안에 답합니다. 더 걸리면 이유와 예상 날짜를 알립니다. 실시간 상담은 하지 않습니다.</p>"""),
                section("문의할 때 적어 주실 것", """
<ul><li>일어난 날짜와 시각, 무엇이 안 되는지</li><li>앱 버전(설정 &gt; 정보), 폰 기종과 Android 버전</li><li>문제가 난 필터의 조건(받는 번호는 가려도 됩니다)</li></ul>
<p>인증번호, 비밀번호, 다른 사람의 전화번호와 문자 내용은 보내지 마세요. 화면을 첨부할 때는 이런 정보를 가려 주세요.</p>"""),
                section("구독 해지와 환불", """
<p>구독은 Google Play 앱의 「결제 및 정기 결제」에서 언제든 해지할 수 있습니다. 앱을 지워도 구독은 해지되지 않습니다. 환불은 위 이메일이나 Google Play에서 요청할 수 있으며, 기준은 <a href="{{HOME}}terms/">이용약관 및 운영정책</a> 5절에 있습니다. 결제 정보는 Google이 처리하므로 카드 번호는 보내지 마세요.</p>"""),
                section("원치 않는 문자를 받고 있다면", """
<p>이 앱으로 원치 않는 문자를 받고 있다면 보낸 번호를 차단하고, 불법스팸대응센터(118, <a href="https://spam.kisa.or.kr">spam.kisa.or.kr</a>)나 경찰(112)에 신고할 수 있습니다. 운영자에게도 위 이메일로 알려 주세요. 처리 기준은 <a href="{{HOME}}terms/">이용약관 및 운영정책</a>에 있습니다.</p>"""),
                section("사업자 정보", "{{BUSINESS}}"),
            ]),
        ],
    },
    "en": {
        "html_lang": "en", "og_locale": "en_US", "path": "en/", "other": "ko", "switch": "한국어", "switch_lang": "ko",
        "site_name": "Transporter", "brand_sub": "Policies and support", "home_label": "Transporter policies and support home",
        "skip": "Skip to content", "menu": "Documents", "toc": "On this page", "toc_label": "Contents", "help": "Need help? →",
        "open_toc": "Show contents", "top": "Back to top ↑", "eyebrow": "TRANSPORTER · SMS FORWARDING",
        "published": "Published", "version": "Version",
        "notice_title": "Before launch",
        "notice": "Transporter is preparing for release on Google Play. The advertising (Google AdMob), subscription (Google Play billing), crash reporting (Firebase Crashlytics) and usage statistics (Firebase) parts of the Privacy Policy, and the free limit, ads and subscription terms of the Terms of Use, apply from the app version that adds those features. The contact details on this site can be used now.",
        "support_subject": "[Transporter] Support request",
        "not_found_title": "Page not found.", "not_found_body": "The address has changed or the page does not exist.", "not_found_home": "Go to policies and support",
        "pages": [
            page("", "Home", "Policies and support", "The Privacy Policy, Terms of Use and support information for Transporter.", [
                section("Find what you need", """
<div class="cards">
<a class="card" href="{{HOME}}en/privacy/"><strong>Privacy Policy</strong><span>Messages that stay on your phone, and what goes to Google for ads, crash reports and statistics</span></a>
<a class="card" href="{{HOME}}en/terms/"><strong>Terms of Use and Acceptable Use Policy</strong><span>Permitted use, prohibited conduct, limitation of liability</span></a>
<a class="card" href="{{HOME}}en/support/"><strong>Support</strong><span>How to contact us and what to include</span></a>
</div>"""),
                section("About Transporter", """
<p>Transporter is an Android app that forwards text messages received on your phone to numbers you choose, based on conditions you set. Received messages and forwarding history are stored only on your phone, and we run no server that receives your messages.</p>
<p>There is no sign-up, so there is no account to create or delete. You can clear the history on your phone in the app, and uninstalling the app deletes everything.</p>"""),
                section("This website", HOSTING_EN),
                section("Operator", "{{BUSINESS}}"),
            ]),
            page("privacy", "Privacy Policy", "Privacy Policy", "What personal information Transporter handles, how long it is kept, what is sent to Google, and your rights.",
                 markdown="privacy.en.md", intro="At a glance"),
            page("terms", "Terms of Use", "Terms of Use and Acceptable Use Policy", "The rules for using Transporter, what we do about violations, changes to the service and limitation of liability.",
                 markdown="terms.en.md", intro="About this policy"),
            page("support", "Support", "Support", "Questions about the app, reports of unwanted messages and privacy requests by email.", [
                section("Contact us", """
<p><a class="button" href="{{SUPPORT_MAIL}}">Write an email</a></p>
<p>Email: <a href="mailto:{{EMAIL}}">{{EMAIL}}</a></p>
<p>We reply to questions within 7 days and to privacy requests (access, deletion and so on) within 10 days. If it will take longer, we will tell you why and when to expect an answer. There is no live chat.</p>"""),
                section("What to include", """
<ul><li>The date and time it happened and what is not working</li><li>The app version (Settings &gt; About), your phone model and Android version</li><li>The conditions of the filter involved (you may hide the destination numbers)</li></ul>
<p>Do not send verification codes, passwords, or other people's phone numbers or messages. If you attach screenshots, please hide this information.</p>"""),
                section("Cancelling a subscription and refunds", """
<p>You can cancel a subscription at any time in the Google Play app under Payments &amp; subscriptions. Uninstalling the app does not cancel it. You can ask for a refund at the email address above or through Google Play; the rules are in section 5 of the <a href="{{HOME}}en/terms/">Terms of Use and Acceptable Use Policy</a>. Google handles payment details, so please do not send card numbers.</p>"""),
                section("If you are receiving unwanted messages", """
<p>If you are receiving unwanted messages through this app, block the sending number and report it to your local spam or police authority (in Korea: the Illegal Spam Response Center, 118, <a href="https://spam.kisa.or.kr">spam.kisa.or.kr</a>, or the police, 112). Please also tell us at the email address above. How we handle reports is described in the <a href="{{HOME}}en/terms/">Terms of Use and Acceptable Use Policy</a>.</p>"""),
                section("Operator", "{{BUSINESS}}"),
            ]),
        ],
    },
}

SITE = {"published": PUBLISHED, "versions": VERSIONS, "company": COMPANY, "langs": LANGS}
