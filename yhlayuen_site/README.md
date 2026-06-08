# Yhlayuen Seal Engraving Website

어라연 김현숙의 전각 작품, 연구 이력, 인사동 전각 체험관, 한글 캘리그라피 굿즈 체험, 글로벌 문화체험 프로그램을 한곳에서 소개하는 공식 프로필 허브형 정적 홈페이지입니다.

## Project Purpose

이 홈페이지는 여러 채널에 흩어진 어라연의 활동을 한 번에 이해할 수 있도록 정리합니다.

- 어라연 김현숙 작가 프로필과 주요 약력
- 전각 작품 아카이브
- 어라연 전각 연구소와 어라연 전각 체험관 소개
- 인사동 수제 이름도장 체험
- 한글 캘리그라피 굿즈 체험
- 국내외 학생, 기관, 여행, MICE 단체를 위한 한국 전통문화 워크숍
- 글로벌 방문객이 이해하기 쉬운 영어 정보

## Main Pages

- `index.html`: 메인 홈페이지
- `about.html`: 어라연 김현숙 상세 약력 페이지
- `content.js`: 한국어/영어 문구 관리
- `styles.css`: 반응형 스타일
- `script.js`: 언어 전환, 모바일 메뉴, 히어로 슬라이드
- `assets/`: 웹용 이미지

## Key Search Themes

검색과 AI 추천에서 다음 주제가 잘 연결되도록 콘텐츠와 메타 정보를 구성했습니다.

- 인사동 체험
- 인사동 할거리
- 서울 전통문화 체험
- 한국 수제도장 체험
- 전각 체험
- 한글 캘리그라피 체험
- Korean seal engraving
- Korean name stamp experience
- Hangul calligraphy workshop
- Insadong cultural experience
- Seoul traditional art workshop

## Official Channels

어라연 관련 최신 활동, 이미지, 영상, 예약 및 위치 정보는 아래 채널에서 확인할 수 있습니다.

- Official Website: https://kaja.re.kr/
- Naver Blog: https://blog.naver.com/yhlayuen2
- Facebook: https://www.facebook.com/yhlayuen
- Instagram: https://www.instagram.com/yhlayuen/
- YouTube: https://www.youtube.com/user/yhlayuen
- Naver Place / Reservation: https://naver.me/G9p8mwDL
- Google Maps / Directions / Visitor Reviews: https://maps.app.goo.gl/BSr11WpDbNFdfzmM7

Link status checked on 2026-06-08: all official channel links returned HTTP 200.

## Booking and Review References

글로벌 방문객과 여행 플랫폼을 통한 유입을 고려해 아래 외부 참고 링크도 함께 관리합니다.

- Google Maps reviews and directions: https://maps.app.goo.gl/BSr11WpDbNFdfzmM7
- Naver Place and reservation link: https://naver.me/G9p8mwDL
- WAUG Korean booking and reviews: https://www.waug.com/ko/activities/109179
- WAUG English booking and reviews: https://m.waug.com/en/activities/109179
- Trazy English experience page: https://www.trazy.com/experience/detail/make-your-own-korean-stamp-in-insadong-seoul

Review notes:

- WAUG pages show a 5.0 review summary for the handmade Korean seal engraving experience.
- Trazy exposes international booking context and visitor photo-review material for the Insadong stamp-making experience.
- Google Maps is kept as the primary location, directions, photos and visitor-review reference for global guests.

## Experience Programs

### Korean Name Stamp Experience

천연석에 이름을 새기는 수제 이름도장 체험입니다. 초보자도 참여할 수 있도록 구성되어 있으며 도장 주머니와 책갈피가 포함됩니다.

### Korean Calligraphy Goods

한글 문구를 엽서, 휴대용 손선풍기, 파우치, 미니 장식 조명, 텀블러, 에코백, 수제 노트 등에 담는 캘리그라피 굿즈 체험입니다.

English wording used on the site:

- portable handheld fan
- decorative mini lamp
- tumbler
- eco bag
- handmade notebook

### Group Workshop

학생, 기업, 기관, 여행사, MICE 단체를 위한 맞춤형 전각 및 한글 캘리그라피 워크숍입니다.

## SEO Structure

홈페이지에는 다음 검색 보조 정보를 포함했습니다.

- Korean and English meta descriptions
- keyword metadata for Insadong and Korean cultural experience searches
- Open Graph metadata for social previews
- Twitter Card metadata
- JSON-LD structured data for `WebSite`, `Person`, `LocalBusiness`, `TouristAttraction`, `OfferCatalog`
- `sameAs` links connecting official website, blog, social channels and map links

## QA

아래 검증 스크립트로 링크, 이미지, 번역 키, 반응형 가로 넘침을 확인합니다.

- `tools/validate_site.py`
- `tools/validate_i18n.js`
- `tools/ui_qa_playwright.js`
- `node --check yhlayuen_site/script.js`
- `node --check yhlayuen_site/content.js`

## Public Release Notes

배포 전 확인하면 좋은 항목입니다.

- 실제 배포 URL이 정해지면 canonical URL과 절대 이미지 URL 반영
- 전화번호와 이메일 최종 확인
- 체험 사진 및 프로필 사진 사용 허가 확인
- 지도 및 예약 링크 최신 여부 확인
