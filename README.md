# GraphCrackers 웹사이트

GraphCrackers의 교육 철학과 ARETE 프로그램을 소개하는 공식 정적 웹사이트다. 별도의 애플리케이션 서버 없이 GitHub Pages가 `main` 브랜치의 루트 파일을 [graphcrackers.github.io](https://graphcrackers.github.io/)에 배포한다.

## 현재 반영된 수정

기존 단일 홈을 GraphCrackers의 교육 방향이 먼저 드러나는 모바일 우선 사이트로 재구성했다. 홈에서 프로그램 소개, 교육 방법, 공개 기록, 상담 안내로 이어지고 각 주제는 독립된 하위 페이지에서 자세히 설명한다.

| 경로 | 반영 내용 |
| --- | --- |
| `/` | 핵심 메시지, 사고 과정, ARETE 요약, 수업 원칙, 편지 발행 상태, 상담 안내를 한 흐름으로 구성 |
| `/arete/` | 프로그램의 대상·형태·구성, 4개 트랙, 수업 방법과 진행 원칙 설명 |
| `/about/` | GraphCrackers가 교육을 설계하고 검토하는 기준 소개 |
| `/letters/` | 「혁신가를 위한 편지」의 목적과 0·1·2편 준비 상태 표시 |
| `/contact/` | 체험 및 상담 절차, 현재 사용할 수 있는 연락 방법 안내 |
| `/privacy/` | 개인정보처리방침이 법률 검토 전임을 명시하는 게시 상태 페이지 |
| 존재하지 않는 경로 | 공통 디자인을 유지하는 맞춤형 `404.html` 제공 |

공통 헤더에는 프로그램, 팀, 편지, 문의 메뉴를 항상 노출하고, 각 페이지의 푸터에서 연락처와 개인정보처리방침 상태를 확인할 수 있게 했다. SVG 파비콘과 검색·공유를 위한 페이지별 제목, 설명 메타데이터도 추가했다.

## 구현 방식

사이트는 빌드 도구나 프레임워크 없이 HTML과 CSS만으로 동작한다. JavaScript가 비활성화된 환경에서도 본문, 메뉴, 내부 링크를 모두 사용할 수 있다.

- 각 공개 경로는 해당 디렉터리의 `index.html`로 구현했다.
- 모든 페이지가 `/assets/style.css`를 공유하며, 페이지 안의 `<style>` 요소와 `style` 속성은 사용하지 않는다.
- CSS 사용자 정의 속성으로 색상, 간격, 타이포그래피, 콘텐츠 폭, 터치 영역을 관리한다.
- 기본 레이아웃은 작은 화면을 기준으로 작성하고 `48rem`, `23.5rem` 미디어 쿼리에서 내비게이션과 그리드를 재배치한다.
- Google Fonts의 `Cormorant Garamond`와 `Noto Serif KR`을 사용하고, 로드되지 않을 때를 위한 시스템 세리프 폴백을 지정했다.
- `.nojekyll`을 두어 GitHub Pages가 파일을 Jekyll로 변환하지 않고 현재 디렉터리 구조 그대로 배포하게 했다.

## 디자인과 접근성

전체 화면은 밝은 종이색 배경, 짙은 본문색, 절제된 금색 강조색을 사용하는 연구 노트형 시각 언어로 통일했다. 장식보다 제목의 위계, 구분선, 충분한 여백으로 정보 구조가 드러나도록 구성했다.

- 본문으로 바로 이동하는 건너뛰기 링크 제공
- `header`, `nav`, `main`, `section`, `footer` 등 의미에 맞는 HTML 요소 사용
- 현재 페이지를 `aria-current`로 표시하고 주요 영역에 접근 가능한 이름 제공
- 키보드 사용자를 위한 `:focus-visible` 윤곽선 적용
- 메뉴와 주요 링크에 최소 `44×44px` 터치 영역 확보
- `prefers-reduced-motion` 환경에서 스크롤 및 전환 효과 축소
- 기본 본문색과 배경색 조합을 WCAG 일반 텍스트 기준인 `4.5:1` 이상으로 유지

## 파일 구조

```text
.
├── index.html                 # 홈
├── arete/index.html          # ARETE 프로그램
├── about/index.html          # 팀과 교육 설계 기준
├── letters/index.html        # 편지 발행 상태
├── contact/index.html        # 체험 및 상담 안내
├── privacy/index.html        # 개인정보처리방침 게시 상태
├── 404.html                  # 찾을 수 없는 경로
├── assets/
│   ├── style.css             # 전 페이지 공통 디자인 시스템
│   └── favicon.svg           # 사이트 파비콘
├── scripts/
│   └── validate_site.py      # 정적 사이트 자동 검증
└── .nojekyll                 # GitHub Pages의 Jekyll 처리 비활성화
```

## 로컬 확인과 검증

저장소 루트에서 정적 서버를 실행한다.

```bash
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 열면 GitHub Pages와 같은 루트 경로 기준으로 확인할 수 있다.

변경 후에는 외부 패키지 없이 실행되는 검증 스크립트를 사용한다.

```bash
python3 scripts/validate_site.py .
```

스크립트는 모든 HTML을 순회하며 다음 항목을 확인한다.

- 끊어진 내부 링크와 존재하지 않는 앵커
- 페이지별 `<title>`과 설명 메타데이터
- 중복 `id`, 대체 텍스트가 없는 이미지
- `/assets/style.css` 사용 여부
- 인라인 스타일과 `<script>` 사용 여부
- 미완성 플레이스홀더와 금지 문자열
- 주요 텍스트 색상과 배경색의 대비비
- `.nojekyll` 존재 여부

## 아직 확정되지 않은 콘텐츠

다음 정보는 확인되지 않은 내용을 임의로 게시하지 않는 원칙에 따라 상태만 표시했거나 연결을 보류했다.

- 8강 커리큘럼의 확정 제목과 한 줄 설명
- 「혁신가를 위한 편지」 0·1·2편의 웹 원고와 발행일
- Google Form과 Instagram의 확정 URL
- 사업자 정보
- 법률 검토를 마친 개인정보처리방침

작업은 별도 브랜치에서 진행하고 Pull Request 검토 후 `main`에 병합한다. `main`에 반영된 변경은 GitHub Pages의 `pages-build-deployment` 워크플로를 통해 공개 사이트에 배포된다.
