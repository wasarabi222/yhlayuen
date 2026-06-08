# 어라연 홈페이지 스펙

최종 업데이트: 2026-06-08

## 1. 목적

어라연 김현숙의 작가 프로필, 전각 작품, 인사동 체험관, 글로벌 문화체험 활동을 소개하는 정적 홈페이지다.

핵심 방향:

- 전통문화와 한옥 브랜드 계열의 차분한 고급감
- 전각 작품 `창조`, `부활`을 중심으로 한 강한 첫인상
- 체험 예약 사이트보다 작가 프로필과 체험관 신뢰도를 먼저 보여주는 구조
- 글로벌 방문객과 여행사/기관 담당자가 신뢰할 수 있는 정보 구조

## 2. 페이지 구조

### `index.html`

- Hero: `창조`, `부활` 전각 작품 슬라이드
- Yhlayuen Experience: 주요 경로 카드
- About 요약: 작가/연구자 소개와 상세 약력 링크
- Works: 전각 작품 이미지
- Experience: 전각, 캘리그라피, 그룹 워크숍
- Lab & Experience Center: 연구소와 체험관 역할 분리 소개
- Global: 해외 문화체험, SITM, Connections Luxury Seoul 등
- Global proof: Connections Luxury Seoul, SITM, 러시아 한국문화원, CIEE/대학/어학당/여행사 방문객
- Visit: 인사동 체험관 주소, 문의, 지도

### `about.html`

- 김현숙 프로필 사진
- 작가 소개문
- 학력 및 연구
- 개인전
- 단체전 및 소장
- 교육 및 경력
- 현재 활동
- 전시, 강의, 단체 체험 문의 CTA
- KO/EN 언어 전환 콘텐츠

## 3. 에셋

위치: `yhlayuen_site/assets`

핵심 이미지:

- `hero-creation.jpg`: 창조 · Creativity
- `hero-resurrection.jpg`: 부활 · Resurrection
- `kim-hyunsook-profile.jpg`: 김현숙 프로필 사진
- `artist-selfportrait.jpg`: 어라연 자화상 전각 이미지
- `work-seal-gyeoul-spring.jpg`: 기존 홈페이지 작품 후보, 겨울 지나 새봄
- `work-installation-sijo108.jpg`: 기존 홈페이지 작품 후보, 시조108, 웹용 최적화 이미지
- `hero-resurrection.jpg`: 부활
- `experience-calligraphy-goods.jpg`: 작품이 잘리지 않도록 재크롭한 한글 캘리그라피 굿즈 이미지
- `experience-group-stamps.jpg`: 제공 자료의 도장 배열 이미지, 그룹 워크숍 카드 사용
- `global-connections-hands.jpg`: 커넥션스 럭셔리 서울 체험 손 클로즈업
- `global-english-ppt-workshop.jpg`: 제공 자료의 체험 사진 크롭 이미지
- `map-insadong.jpg`: 영문 약도

이미지 최적화:

- `work-seal-gyeoul-spring.jpg`: 약 3.58MB에서 약 1.07MB로 웹용 최적화
- `work-installation-sijo108.jpg`: 약 619KB 웹용 최적화 이미지

작품 캡션 원칙:

- 작품 하단 캡션은 작품명만 짧게 표기
- 작품별 크기, 재료, 전시 연도, 전시장명은 확정 근거가 부족하거나 화면이 복잡해져 공개 캡션에는 미기재

## 4. 스타일

참고 톤:

- `rkj.co.kr` 계열의 고급 전통문화/한옥 브랜드 랜딩

디자인 원칙:

- 큰 히어로 이미지
- 얇은 고정 내비게이션
- 넓은 여백과 낮은 채도
- 과한 전통 문양 대신 전각 작품 자체를 시각 중심으로 사용
- 모바일에서는 카드형 구조로 단순하게 쌓기
- 연구소/체험관 구간은 배너 이미지 없이 텍스트 카드로만 정리해 이질감을 낮춤

주요 색상:

- Background: `#f4eee4`
- Paper: `#fbf8f1`
- Ink: `#211d18`
- Seal Red: `#9f332c`
- Line: `#d8cdbc`

## 5. 기능

- 히어로 자동 슬라이드
- 히어로 Prev/Next 버튼
- 스크롤 시 헤더 배경 처리
- 모바일 햄버거 메뉴
- EN/KO 언어 전환
- `content.js` 기반 번역 원문 관리
- 체험 카드의 시간, 제목, 설명도 `content.js`의 `home.program.*` 키에서 KO/EN 함께 관리
- 한글 캘리그라피 굿즈 영어 표기는 `portable handheld fans`, `decorative mini lamps`처럼 실제 물건의 성격이 드러나도록 번역
- 연구소/체험관 카드 제목도 `content.js`의 `home.identity.*Title` 키에서 KO/EN 함께 관리
- 영어 공개 표기는 `어라연`을 `Yhlayuen`으로 통일
- 내부 앵커 이동
- 이메일 문의 링크
- WebSite, Person, LocalBusiness, TouristAttraction, OfferCatalog 구조화 데이터

## 6. 검색/AI 노출 구조

인사동 체험, 인사동 할거리, 서울 전통문화 체험, 한국 수제도장 체험, 전각 체험, 한글 캘리그라피 워크숍 등으로 검색될 때 문맥이 연결되도록 아래 정보를 반영한다.

- 메인 페이지 `description`, `keywords`, `robots`
- About 페이지 `description`, `keywords`, `robots`
- Open Graph 메타 정보
- Twitter Card 메타 정보
- JSON-LD `WebSite`, `Person`, `LocalBusiness`, `TouristAttraction`, `OfferCatalog`
- 공식 웹사이트, 블로그, SNS, 지도 링크를 `sameAs`로 연결

주의:

- 실제 배포 URL이 정해지면 canonical URL과 JSON-LD 이미지 URL을 절대 URL로 교체한다.

## 7. QA 체크리스트

자동 검증:

- `tools/validate_site.py`
- `tools/validate_i18n.js`
- `tools/ui_qa_playwright.js`
- `node --check yhlayuen_site/script.js`
- `node --check yhlayuen_site/content.js`

검증 항목:

- HTML 페이지 존재 여부
- CSS/JS 연결 여부
- 이미지 경로 누락 여부
- 내부 HTML 링크 누락 여부
- KO/EN 번역 키 누락 여부
- 방문자에게 보이면 안 되는 내부 메모성 문구 포함 여부
- 390/768/1280px 가로 넘침 여부
- JS 문법 오류 여부

수동 확인 필요:

- 실제 브라우저 렌더링
- 모바일 메뉴 클릭
- 히어로 슬라이드 전환
- 이미지 크롭 적합성
- 인물 사진 및 해외 참가자 사진 사용 허가

## 8. GitHub 저장소 상태

- 원격 저장소: `https://github.com/wasarabi222/yhlayuen`
- 소유자/저장소명: `wasarabi222/yhlayuen`
- 확인일: 2026-06-08
- 현재 상태: 저장소는 생성되어 있으나 GitHub API 기준 커밋이 없는 빈 저장소
- README 방향: 프로젝트 설명, 공식 채널, 체험 프로그램, SEO 구조를 함께 정리

## 9. 공개 전 확인 필요

- 전화번호 최종 표기
- 이메일 최종 표기
- 김현숙 프로필 사진 최신본 여부
- 해외 참가자 얼굴 사진 사용 허가
- HWP 해외 예약 문의 매뉴얼의 정확 문구 반영
