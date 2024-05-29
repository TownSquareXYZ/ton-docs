# 톤클리 사용

톤클리 - 오픈 네트워크 크로스 플랫폼 스마트 컨트랙트 명령줄 인터페이스._

TON 스마트 컨트랙트를 쉽게 배포하고 상호 작용할 수 있습니다.

Python\*\* 스택 개발자를 위한 좋은 솔루션입니다.

- [깃허브 리포지토리](https://github.com/disintar/toncli)

## 빠른 시작 📌

다음은 톤클리 라이브러리를 사용하여 만든 튜토리얼입니다:

- [빠른 시작 가이드](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md) - 스마트 컨트랙트 예시를 TON에 배포하는 간단한 단계입니다.
- [TON Learn: FunC 여정 개요 1부](https://blog.ton.org/func-journey)
- [TON Learn: FunC 여정 개요. 2부](https://blog.ton.org/func-journey-2)
- [TON Learn: FunC 여정 개요. 3부](https://blog.ton.org/func-journey-3)
- [톤 학습: 제로에서 히어로까지 10가지 레슨](https://github.com/romanovichim/TonFunClessons_Eng) ([Ru 버전](https://github.com/romanovichim/TonFunClessons_ru))

## 설치 💾

### Docker: Linux/MacOS(m1 지원)

- 도커허브 프리빌드 이미지는 [여기](https://hub.docker.com/r/trinketer22/func_docker/)에서 찾을 수 있습니다.
- 지침이 포함된 Docker 파일은 [여기](https://github.com/Trinketer22/func_docker)에서 찾을 수 있습니다.

### Linux/맥OS(인텔)

1. 필요한 특별 사전 빌드를 다운로드하세요(최신 빌드 사용).

- 리눅스용: [여기](https://github.com/SpyCheese/ton/actions/workflows/ubuntu-compile.yml?query=branch%3Atoncli-local++)
- Mac용: [여기](https://github.com/SpyCheese/ton/actions/workflows/macos-10.15-compile.yml?query=branch%3A톤클리-로컬)

:::info 특별 사전 빌드 팁 다운로드
필요한 파일을 다운로드하려면 계정에 로그인해야 합니다.
:::

2. 파이썬3.9](https://www.python.org/downloads/) 이상 설치

3. 터미널에서 `pip install toncli` 또는 `pip3 install toncli`로 실행합니다.

:::tip 가능한 오류
'경고: 톤클리 스크립트가 PATH에 없는 '/Python/3.9/bin'에 설치되어 있습니다'라고 표시되면 PATH 환경설정에 bin의 전체 경로를 추가합니다.
:::

4. 톤클리`를 실행하고 첫 번째 단계부터 `func/fift/lite-client\`에 절대 경로를 전달합니다.

### Windows

1. 여기]에서 필요한 특별 사전 빌드를 다운로드하세요(https://github.com/SpyCheese/ton/actions/workflows/win-2019-compile.yml?query=branch%3A톤클리-로컬)(최신 빌드 사용).

:::info 특별 사전 빌드 팁 다운로드
필요한 파일을 다운로드하려면 계정에 로그인해야 합니다.
:::

2. 파이썬3.9](https://www.python.org/downloads/) 이상 설치

:::info 매우 중요합니다!
설치 중 첫 번째 화면에서 '경로에 파이썬 추가' 확인란을 클릭해야 합니다.
:::

3. 관리자 권한으로 터미널을 열고 'toncli'를 설치하여 `pip install toncli`를 실행합니다.

4. 다운로드한 아카이브의 압축을 풀고 압축을 푼 파일에 [libcrypto-1_1-x64.dll](https://disk.yandex.ru/d/BJk7WPwr_JT0fw)을 추가합니다.

5. Windows 사용자의 경우 콘솔에서 폴더를 엽니다:

**Windows 11**:

- 마우스 오른쪽 버튼, 터미널에서 열기

**Windows 10**:

- 탐색기에서 경로를 복사하고 터미널 `cd FULL PATH`에서 실행합니다.

## 프로젝트 만들기 ✏️

다음은 TON에 스마트 컨트랙트 예시를 배포하는 간단한 단계입니다.
공식 문서는 [여기](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md)에서 확인할 수 있습니다.

### 단계별 가이드

1. 관리자로 터미널을 열고 프로젝트 폴더로 이동합니다.

2. 프로젝트를 생성하려면 `toncli start YOUR-PROJECT-NAME`을 실행합니다.

3. 프로젝트 폴더 `cd YOUR-PROJECT-NAME`으로 이동합니다.

:::info 결과

- 빌드
- func
- 다섯
- test
  :::

4. 테스트넷 또는 메인넷에 배포할 수 있습니다: 'toncli deploy -n testnet'

## 예제

기여자들은 새로운 테스트에서 다룰 샘플 프로젝트를 매우 잘 준비했습니다. 예를 들어, 이제 두 가지 명령어를 사용해 NFT 컬렉션이나 제톤을 배포할 수 있습니다.

```bash
toncli start nft_colletion/jetton_minter/nft_item/jetton_wallet
```

이 모든 프로젝트에는 톤클리와 블록체인 상호작용에 대한 흥미로운 예시가 많이 있으며, 맞춤형 스마트 컨트랙트 개발에 도움이 되는 극한의 테스트도 진행 중입니다.

## 톤클리를 사용하여 스마트 컨트랙트를 테스트하려면 [테스트](/개발/스마트-컨트랙트/테스트/톤클리)로 이동하세요.

## 유용한 문서

개발 시 톤클리 사용에 대한 기타 유용한 글입니다:

1. [모든 cli 명령](https://github.com/disintar/toncli/blob/master/docs/advanced/commands.md)
2. [get-methods 실행](https://github.com/disintar/toncli/blob/master/docs/advanced/get_methods.md)
3. [복수 계약](https://github.com/disintar/toncli/blob/master/docs/advanced/multiple_contracts.md)
4. [파이브와 함께 boc 보내기](https://github.com/disintar/toncli/blob/master/docs/advanced/send_boc_with_fift.md)
5. [프로젝트 구조](https://github.com/disintar/toncli/blob/master/docs/advanced/project_structure.md)
6. [흥미로운 기능](https://github.com/disintar/toncli/blob/master/docs/advanced/intresting_features.md)
7. [내부 5가지 메시지 보내기](https://github.com/disintar/toncli/blob/master/docs/advanced/send_fift_internal.md)
8. [FunC 테스트는 어떻게 진행되나요?(https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
9. [톤클리로 트랜잭션을 디버깅하는 방법](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)
10. [펀씨 테스트용 도커파일 GitHub 리포지토리](https://github.com/Trinketer22/func_docker)
