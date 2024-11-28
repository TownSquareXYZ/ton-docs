# 작동 방식

![작동 방식](/img/localizationProgramGuideline/localization-program.png)

**ownSquare Labs 현지화 프로그램**은 몇 가지 주요 요소로 구성됩니다. 이 장에서는 프로그램의 작동 방식을 개괄적으로 설명하여, 그 작동 원리와 효과적인 사용 방법을 이해할 수 있도록 도와줍니다.

이 시스템 내에서는 여러 애플리케이션을 통합하여 하나의 통합된 프로그램으로 원활하게 작동하도록 합니다:

- **GitHub**: 문서를 호스팅하고, 업스트림 리포지토리에서 문서를 동기화하고, 특정 브랜치에 번역을 동기화합니다.
- **Crowdin**: 번역, 교정, 언어 기본 설정 등 번역 프로세스를 관리합니다.
- **AI 시스템**: 번역자들을 지원하기 위해 고급 AI를 활용하여 원활한 워크플로우를 보장합니다.
- **맞춤형 용어집**: 번역자들을 안내하고 AI가 프로젝트의 맥락에 맞는 정확한 번역을 생성하도록 합니다. 사용자들은 필요에 따라 자신들의 용어집을 업로드할 수도 있습니다.

:::info
이 가이드는 전체 과정을 자세히 다루지는 않지만, TownSquare Labs 현지화 프로그램의 독특한 주요 요소들을 강조할 것입니다. 프로그램을 더 자세히 탐색해 보세요.
:::

## 문서 및 번역을 위한 GitHub 동기화

우리 리포지토리는 문서와 번역 관리를 위해 여러 브랜치를 활용합니다. 각 특수 브랜치의 목적과 기능에 대한 자세한 설명은 다음과 같습니다:

### 브랜치 개요

- **`dev`** `dev` 브랜치는 동기화 작업을 처리하기 위해 GitHub Actions를 실행합니다. 워크플로우 설정은 [**`.github/workflows`**](https://github.com/TownSquareXYZ/ton-docs/tree/dev/.github/workflows) 디렉토리에서 찾을 수 있습니다:

  - **`sync-fork.yml`**: 이 워크플로우는 업스트림 리포지토리로부터 문서를 동기화합니다. 매일 00:00에 실행됩니다.
  - **`sync-translations.yml`**: 이 워크플로우는 업데이트된 번역을 해당 언어 브랜치로 동기화하여 해당 언어 웹사이트에서 미리 볼 수 있도록 합니다.

- **`main`** 이 브랜치는 `dev` 브랜치에서 실행되는 GitHub Actions를 통해 업스트림 저장소와 동기화됩니다. 또한 원본 저장소에 제안하고자 하는 특정 코드를 업데이트하는 데도 사용됩니다.

- **`l10n_main`** 이 브랜치는 `main` 브랜치의 모든 변경사항과 Crowdin의 번역을 포함합니다. 이 브랜치의 모든 수정사항은 `l10n_main_[일부 데이터]`라는 이름의 새로운 하위 브랜치를 사용하여 주기적으로 업스트림 저장소에 커밋됩니다.

- **`l10n_main`** 이 브랜치는 `main` 브랜치의 모든 변경사항과 Crowdin의 번역을 포함합니다. 이 브랜치의 모든 수정사항은 `l10n_main_[일부 데이터]`라는 이름의 새로운 하위 브랜치를 사용하여 주기적으로 업스트림 저장소에 커밋됩니다.

- **`[lang]_preview`** 이 브랜치들은 한국어의 경우 `ko_preview`, 일본어의 경우 `ja_preview`와 같이 특정 언어 미리보기를 위해 지정되어 있습니다. 이를 통해 다양한 언어로 웹사이트를 미리볼 수 있습니다.

이 브랜치들을 유지하고 GitHub Actions를 사용함으로써, 우리는 문서와 번역 업데이트의 동기화를 효율적으로 관리하여 다국어 콘텐츠가 항상 최신 상태를 유지하도록 합니다.

## Crowdin의 새 프로젝트를 설정하는 방법

1. [**Crowdin 계정**](https://accounts.crowdin.com/login) 에 로그인하세요.

2. 메뉴에서 `새 프로젝트 만들기`를 클릭하세요.
   ![새 프로젝트 만들기](/img/localizationProgramGuideline/howItWorked/create-new-project.png)

3. 프로젝트 이름과 대상 언어를 설정하세요. 언어는 나중에 설정에서 변경할 수 있습니다.
   ![프로젝트 설정 만들기](/img/localizationProgramGuideline/howItWorked/create-project-setting.png)

4. 방금 만든 프로젝트로 이동하여, 통합 탭을 선택하고 `통합 추가` 버튼을 클릭한 다음, `GitHub`를 검색하여 설치하세요.
   ![GitHub 통합 설치](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)

5. Crowdin에서 GitHub 통합을 구성하기 전에, 불필요한 파일 업로드를 방지하기 위해 Crowdin에 업로드할 파일을 지정하세요:

   1. **GitHub 리포지토리 루트**에 **crowdin.yml** 파일을 기본 설정으로 만드세요:

   ```yml
   project_id: <Your project id>
   preserve_hierarchy: 1
   files:
     - source: <Path of your original files>
       translation: <Path of your translated files>
   ```

   2. 올바른 구성 값을 가져옵니다:
      - **project_id**: Crowdin 프로젝트에서 도구 탭으로 이동하여 API를 선택하고, **project_id**를 찾으세요.
        ![API 도구 선택](/img/localizationProgramGuideline/howItWorked/select-api-tool.png)
        ![project\_id](/img/localizationProgramGuideline/howItWorked/projectId.png)
      - **preserve_hierarchy**: Crowdin 서버에서 GitHub 디렉토리 구조를 유지합니다.
      - **source**와 **translation**: Crowdin에 업로드할 파일 경로와 번역된 파일이 출력될 경로를 지정합니다.

        예시는 [**공식 설정 파일**](https://github.com/TownSquareXYZ/ton-docs/blob/localization/crowdin.yml)을 참고하세요.\
        자세한 내용은 [**Crowdin 구성 파일 문서**](https://developer.crowdin.com/configuration-file/)에서 확인할 수 있습니다.

6. Crowdin을 구성하여 GitHub 리포지토리에 연결합니다:
   1. `리포지토리 추가`를 클릭하고 `소스 및 번역 파일 모드`를 선택합니다.
      ![통합 모드 선택](/img/localizationProgramGuideline/howItWorked/select-integration-mode.png)
   2. GitHub 계정을 연결하고 번역할 리포지토리를 검색하세요.
      ![리포지토리 검색](/img/localizationProgramGuideline/howItWorked/search-repo.png)
   3. 왼쪽에서 브랜치를 선택하면 Crowdin이 번역을 게시할 새 브랜치가 생성됩니다.
      ![브랜치 설정](/img/localizationProgramGuideline/howItWorked/setting-branch.png)
   4. GitHub 브랜치로 번역을 업데이트할 빈도를 선택하세요. 다른 설정은 기본 설정을 유지한 후 저장을 클릭하여 통합을 활성화하세요.
      ![빈도 설정 후 저장](/img/localizationProgramGuideline/howItWorked/frequency-save.png)

자세한 내용은 [**GitHub 연동 문서**](https://support.crowdin.com/github-integration/)를 참조하세요.

7. 마지막으로, 필요할 때마다 `지금 동기화` 버튼을 클릭하여 리포지토리와 번역을 동기화할 수 있습니다.

## 용어집

### 용어집이란 무엇인가요?

때로는 AI 번역기가 번역해서는 안 되는 특정 용어를 인식하지 못할 수 있습니다. 예를 들어, 프로그래밍 언어를 나타내는 "Rust"는 번역하지 않아야 합니다. 이러한 실수를 방지하기 위해 번역 지침으로 용어집을 사용합니다.

**용어집**은 프로젝트별 용어를 한 곳에 생성, 저장 및 관리하여 용어가 올바르고 일관되게 번역되도록 합니다.

참고용으로 [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary)를 확인할 수 있습니다.
![ton-i18n-glossary](/img/localizationProgramGuideline/howItWorked/ton-i18n-glossary.png)

### 새 언어에 대한 용어집을 설정하는 방법은 무엇인가요?

대부분의 번역 플랫폼은 용어집을 지원합니다. Crowdin에서는 용어집을 설정한 후, 각 용어가 편집기에서 밑줄이 그어진 단어로 나타납니다. 용어 위에 마우스를 올리면 번역, 품사, 정의(제공된 경우)를 볼 수 있습니다.
![github-glossary](/img/localizationProgramGuideline/howItWorked/github-glossary.png)
![crowdin-glossary](/img/localizationProgramGuideline/howItWorked/crowdin-glossary.png)

DeepL에서는 용어집을 업로드하면 AI 번역 중 자동으로 사용됩니다.

우리는 업데이트를 자동으로 업로드하는 [**용어집 프로그램**](https://github.com/TownSquareXYZ/ton-i18n-glossary)을 만들었습니다.

용어집에 용어를 추가하려면:

1. 영어 용어가 이미 용어집에 있는 경우, 해당 언어의 번역을 입력하고 업로드합니다.
2. 새 용어집을 업로드하려면, 프로젝트를 클론하고 다음을 실행합니다:

   - `npm i`
   - `npm run generate -- <glossary name you want>`

새 용어를 추가하려면 1단계를 반복합니다.

**간단하고 효율적이지 않나요?**

## AI 번역 Copilot을 활용하는 방법은 무엇인가요?

AI 번역 코파일럿은 여러 가지 이점으로 언어 장벽을 허물어줍니다:

- **향상된 일관성**: AI 번역은 최신 정보를 기반으로 하여 가장 정확하고 최신의 번역을 제공합니다.
- **속도와 효율성**: AI 번역은 실시간으로 대량의 콘텐츠를 즉시 처리합니다.
- **강력한 확장성**: AI 시스템은 지속적으로 학습하고 개선되어 번역 품질이 시간이 지남에 따라 향상됩니다. 제공된 용어집을 통해 AI 번역은 다양한 저장소의 특정 요구에 맞춰 조정될 수 있습니다.

Crowdin에서 AI 번역을 사용하려면(저희 프로젝트에서는 DeepL 사용):

1. Crowdin 메뉴에서 기계 번역을 선택하고 DeepL 라인에서 편집을 클릭하세요.
   ![select-deepl](/img/localizationProgramGuideline/howItWorked/select-deepl.png)
2. DeepL 지원을 활성화하고 DeepL 번역기 API 키를 입력하세요.
   > [DeepL 번역기 API 키 받기 방법](https://www.deepl.com/pro-api?cta=header-pro-api)

![config-crowdin-deepl](/img/localizationProgramGuideline/howItWorked/config-crowdin-deepl.png)

3. 우리의 DeepL 설정은 맞춤형 용어집을 사용합니다. 용어집 업로드에 대한 자세한 내용은 [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary)를 확인하세요.

4. 리포지토리에서 사전 번역을 클릭하고 기계 번역을 통해 선택하세요.
   ![pre-translation](/img/localizationProgramGuideline/howItWorked/pre-translation.png)

5. DeepL을 번역 엔진으로 선택하고, 대상 언어를 선택한 다음 번역할 파일을 선택하세요.
   ![pre-translate-config](/img/localizationProgramGuideline/howItWorked/pre-translate-config.png)

끝났습니다! 이제 사전 번역이 완료될 때까지 잠시 휴식을 취하면 됩니다.
