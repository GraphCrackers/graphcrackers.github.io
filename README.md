# GraphCrackers 웹사이트

GraphCrackers와 ARETE 프로그램을 소개하는 정적 웹사이트다. GitHub Pages가 `main` 브랜치의 루트를 그대로 배포한다.

## 구현 원칙

- 빌드 도구와 프레임워크를 사용하지 않는 정적 HTML/CSS
- JavaScript 없이 모든 콘텐츠와 링크 사용 가능
- 모든 페이지가 `/assets/style.css` 하나를 공유
- HTML 인라인 스타일 금지
- 모바일 우선, 전역 헤더의 네 메뉴는 항상 노출
- 확인되지 않은 프로그램 원고, 사업자 정보, 신청 폼 주소, 법률 문안은 임의로 게시하지 않음

## 파일 구조

```text
.
├── index.html
├── arete/index.html
├── about/index.html
├── letters/index.html
├── contact/index.html
├── privacy/index.html
├── assets/style.css
├── scripts/validate_site.py
├── 404.html
└── .nojekyll
```

## 로컬 확인

```bash
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 연다.

## 자동 검증

```bash
python3 scripts/validate_site.py .
```

검증 항목은 내부 링크와 앵커, `<title>`과 설명 메타, 단일 CSS 사용, 인라인 스타일·스크립트 금지, 금지 이메일·플레이스홀더, 기본 텍스트 대비비다.

## 공개 전 필요한 입력

- 8강 커리큘럼의 확정 제목과 한 줄 설명
- 「혁신가를 위한 편지」 0·1·2편의 웹 원고와 발행일
- Google Form과 Instagram의 확정 URL
- 사업자 정보
- 법률 검토를 마친 개인정보처리방침

작업은 `work/*` 브랜치에서 진행하고 Pull Request로 `main`에 병합한다.
