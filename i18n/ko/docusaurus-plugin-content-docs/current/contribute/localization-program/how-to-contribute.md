# 기여 방법

**TON을 가장 성공적인 블록체인으로 만드는** 우리의 목표를 이루기 위해, TON 문서가 전 세계 사람들에게 이해될 수 있도록 하는 것이 중요합니다. 현지화가 핵심이며, 이 노력에 당신이 함께 해주신다면 **정말 기쁠 것**입니다.

## 사전 준비 사항

**TownSquare Labs Localization Program**은 누구에게나 열려 있습니다! 기여를 시작하기 전에 다음 단계를 따라주세요:

1. [**Crowdin**](https://crowdin.com) 계정에 로그인하거나 가입하세요.
2. 기여하고 싶은 언어를 선택하세요.
3. [**Crowdin 사용 방법**](/contribute/localization-program/how-to-contribute) 가이드와 [**번역 스타일 가이드**](/contribute/localization-program/translation-style-guide)를 읽고 팁과 모범 사례를 익히세요.
4. 기계 번역을 사용하여 작업을 보조하지만, 단독으로 의존하지 마세요.
5. 모든 번역 결과는 교정이 완료된 후 1시간 내에 웹사이트에서 미리 볼 수 있습니다.

## 역할

시스템에서 맡을 수 있는 **역할**은 다음과 같습니다:

- **언어 코디네이터** – 할당된 언어 내 프로젝트 기능을 관리합니다.
- **개발자** – 파일 업로드, 번역 가능한 텍스트 편집, 통합 연결 및 API 사용을 담당합니다.
- **교정자** – 문자열을 번역하고 승인합니다.
- **번역가** (내부 또는 커뮤니티) – 문자열을 번역하고 다른 사람이 추가한 번역에 투표합니다.

우리의 현지화 프로젝트는 [Crowdin](https://crowdin.com/project/ton-docs)에서 호스팅됩니다.

:::info
Before you start contributing, **read the guidelines below** to ensure standardization and quality, making the review process much faster.

## 나란히 보기 모드

모든 작업은 Crowdin Editor의 **나란히 보기** 모드에서 수행됩니다. 이를 활성화하려면 작업할 파일을 클릭하세요. 페이지 오른쪽 상단의 **편집기 보기** 버튼을 클릭하고 더 명확한 편집기 보기를 위해 **나란히 보기** 모드를 선택하세요.
![나란히 보기 모드](/img/localizationProgramGuideline/side-by-side.png)
:::

### 언어 코디네이터

- **문자열 번역 및 승인**
- **프로젝트 콘텐츠 사전 번역**
- **프로젝트 멤버 및 가입 요청 관리**
  ![멤버 관리](/img/localizationProgramGuideline/manage-members.png)
- **프로젝트 보고서 생성**
  ![보고서 생성](/img/localizationProgramGuideline/generate-reports.png)
- **작업 생성**
  ![작업 생성](/img/localizationProgramGuideline/create-tasks.png)

### 개발자

- **파일 업로드**
- **번역 가능한 텍스트 편집**
- **통합 연결** (예: GitHub 통합 추가)
  ![GitHub 통합 설치](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)
- **[Crowdin API](https://developer.crowdin.com/api/v2/) 사용**

### 교정자

**교정자**로서, **파란색 진행 막대**가 있는 파일에서 작업하게 됩니다.
![교정 단계1](/img/localizationProgramGuideline/proofread-step1.png)
파일을 클릭하여 편집 인터페이스로 들어가세요.

#### 기여 시작

1. [**나란히 보기 모드**](#side-by-side-mode)에 있는지 확인하세요. **승인되지 않음** 번역으로 필터링하여 교정이 필요한 문자열을 확인하세요.
   ![교정 필터](/img/localizationProgramGuideline/proofread-filter.png)

2. 다음 규칙을 따르세요:
   - **파란색 큐브 아이콘**이 있는 문자열을 선택하세요. 각 번역을 확인하세요:
     - **올바르면**, ☑️ 버튼을 클릭하세요.
     - **잘못되면**, 다음 줄로 이동하세요.

![교정 승인됨](/img/localizationProgramGuideline/proofread-approved.png)

:::info
You can also review approved lines:

1. **승인됨**으로 필터링하세요.

2. 승인된 줄에 문제가 있으면, ☑️ 버튼을 클릭하여 교정이 필요하도록 되돌리세요.
   :::

3. 다음 파일로 이동하려면 상단의 파일 이름을 클릭하고, 팝업 창에서 새 파일을 선택하여 교정을 계속하세요.
   ![다음으로 이동](/img/localizationProgramGuideline/redirect-to-next.png)

#### 작업 미리보기

모든 승인된 콘텐츠는 1시간 내에 미리보기 웹사이트에 배포됩니다. 최신 PR의 **미리보기** 링크는 [**우리의 레포지토리**](https://github.com/TownSquareXYZ/ton-docs/pulls)에서 확인하세요.
![미리보기 링크](/img/localizationProgramGuideline/preview-link.png)

### 번역가

**번역가**로서, 당신의 목표는 번역이 원문과 가깝고 표현이 풍부하여 이해하기 쉽게 만드는 것입니다. **파란색 진행 막대**를 100%로 만드는 것이 당신의 임무입니다.

#### 번역 시작

성공적인 번역 과정을 위해 다음 단계를 따르세요:

1. 번역이 100%에 도달하지 않은 파일을 선택하세요.
   ![번역가 선택](/img/localizationProgramGuideline/translator-select.png)

2. [**나란히 보기 모드**](#side-by-side-mode)에 있는지 확인하세요. **번역되지 않음** 문자열로 필터링하세요.
   ![번역가 필터](/img/localizationProgramGuideline/translator-filter.png)

3. 작업 공간은 네 부분으로 구성됩니다:
   - **왼쪽 상단:** 소스 문자열을 기반으로 번역을 입력하세요.
   - **왼쪽 하단:** 번역된 파일을 미리보기 합니다. 원본 형식을 유지하세요.
   - **오른쪽 하단:** Crowdin의 번역 제안. 클릭하여 사용할 수 있지만, 특히 링크의 정확성을 확인하세요.

4. 상단의 **저장** 버튼을 클릭하여 번역을 저장하세요.
   ![번역가 저장](/img/localizationProgramGuideline/translator-save.png)

5. 다음 파일로 이동하려면 상단의 파일 이름을 클릭하고 팝업 창에서 새 파일을 선택하세요.
   ![다음으로 이동](/img/localizationProgramGuideline/redirect-to-next.png)

## 새 언어 지원 추가 방법

현재, Crowdin에는 원하는 모든 언어가 있습니다. 커뮤니티 매니저인 경우, 다음 단계를 따르세요:

1. [TownSquareXYZ/ton-docs](https://github.com/TownSquareXYZ/ton-docs)에 `[lang]_localization` (예: 한국어의 경우 `ko_localization`)이라는 새 브랜치를 추가하세요.
2. 이 저장소의 Vercel 소유자에게 연락하여 메뉴에 새 언어를 추가하도록 요청하세요.
3. dev 브랜치에 PR 요청을 생성하세요. **dev로 병합하지 마세요**; 이는 미리보기 용도입니다.

이 단계가 완료되면 PR 요청에서 언어의 미리보기를 볼 수 있습니다.
![ko 미리보기](/img/localizationProgramGuideline/ko_preview.png)

언어가 TON 문서에 준비되면, 문제를 생성하고, 우리가 프로덕션 환경에 언어를 설정하도록 요청하세요.
