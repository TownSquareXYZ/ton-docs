# 데이터 저장소로서의 셀

TON의 모든 것은 셀에 저장됩니다. 셀은 다음을 포함하는 데이터 구조입니다:

- 최대 **1023 비트**의 데이터 (바이트가 아닙니다!)
- 다른 셀에 대한 최대 **4개의 참조**

비트와 참조는 섞이지 않습니다(별도로 저장됨). 순환 참조는 금지됩니다: 어떤 셀에 대해서도, 그 하위 셀들은 이 원래 셀을 참조로 가질 수 없습니다.

따라서, 모든 셀은 방향성 비순환 그래프(DAG)를 구성합니다. 다음은 이를 설명하는 좋은 그림입니다:

![방향성 비순환 그래프](/img/docs/dag.png)

## 셀 타입

현재 5가지 유형의 셀이 있습니다: *일반* 셀과 4가지 *특수* 셀.
특수 타입은 다음과 같습니다:

- 프룬드(Pruned) 브랜치 셀
- 라이브러리 참조 셀
- 머클 증명 셀
- 머클 업데이트 셀

:::tip
특수 셀에 대한 자세한 내용은 다음을 참조하세요: [**TVM 백서, 섹션 3**](https://ton.org/tvm.pdf).
:::

## 셀의 특성

셀은 컴팩트한 저장을 위해 최적화된 불투명한 객체입니다.

특히, 데이터를 중복 제거합니다: 서로 다른 브랜치에서 참조되는 동일한 하위 셀이 여러 개 있는 경우, 그 내용은 한 번만 저장됩니다. 하지만, 불투명성은 셀이 직접 수정되거나 읽을 수 없다는 것을 의미합니다. 따라서, 셀에는 2가지 추가적인 특성이 있습니다:

- 비트열, 정수, 다른 셀 및 다른 셀에 대한 참조를 빠르게 추가하는 연산을 정의할 수 있는 부분적으로 구성된 셀을 위한 *Builder*
- 부분적으로 파싱된 셀의 나머지 부분이나 파싱 명령을 통해 그러한 셀에서 추출된 값(하위 셀)을 나타내는 '해부된' 셀을 위한 *Slice*

TVM에서는 또 다른 특별한 셀 특성이 사용됩니다:

- TON 가상 머신을 위한 연산 코드(명령어)를 포함하는 셀을 위한 *Continuation*, [TVM 개요](/v3/documentation/tvm/tvm-overview)를 참조하세요.

## 데이터의 셀로의 직렬화

TON의 모든 객체(메시지, 메시지 큐, 블록, 전체 블록체인 상태, 컨트랙트 코드 및 데이터)는 셀로 직렬화됩니다.

직렬화 과정은 TL-B 스키마에 의해 설명됩니다: 이 객체를 _Builder_로 직렬화하거나 _Slice_에서 주어진 타입의 객체를 파싱하는 방법에 대한 공식적인 설명입니다.
셀을 위한 TL-B는 바이트 스트림을 위한 TL이나 ProtoBuf와 같습니다.

셀 (역)직렬화에 대해 더 자세히 알고 싶다면, [셀 & 셀의 가방](/v3/documentation/data-formats/tlb/cell-boc) 문서를 읽어보세요.

## 참고

- [TL-B 언어](/v3/documentation/data-formats/tlb/tl-b-language)