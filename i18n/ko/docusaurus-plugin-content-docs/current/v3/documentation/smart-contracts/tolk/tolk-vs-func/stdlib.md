# Tolk vs FunC: 표준 라이브러리

FunC는 *"stdlib.fc"* 파일로 알려진 풍부한 [표준 라이브러리](/v3/documentation/smart-contracts/func/docs/stdlib)를 가지고 있습니다.
이것은 매우 로우레벨이며 TVM 명령어와 매우 유사하게 명명된 많은 `asm` 함수들을 포함하고 있습니다.

Tolk 또한 FunC 기반의 표준 라이브러리를 가지고 있습니다. 세 가지 주요 차이점:

1. 여러 파일로 분할되어 있습니다: `common.tolk`, `tvm-dicts.tolk` 등. `common.tolk`의 함수들은 항상 사용 가능합니다. 다른 파일의 함수들은 import 후 사용 가능합니다:

```tolk
import "@stdlib/tvm-dicts"

beginCell()          // available always
createEmptyDict()    // available due to import
```

2. GitHub에서 다운로드할 필요가 없으며, Tolk 배포판의 일부입니다.
3. 거의 모든 FunC 함수들이 ~~장황한~~ 명확한 이름으로 변경되었습니다. 그래서 계약을 작성하거나 예제를 읽을 때 무슨 일이 일어나는지 더 잘 이해할 수 있습니다.

## 이름이 변경된 함수들의 목록

"Required import" 열이 비어있다면, 해당 함수는 import 없이 사용 가능합니다.

일부 함수들은 구문적으로 표현될 수 있거나 실제로 매우 드물게 사용되었기 때문에 삭제되었음을 참고하세요.

| FunC name                                                                                                             | Tolk name                               | Required import |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------- |
| empty_tuple                                                                                      | createEmptyTuple                        |                 |
| tpush                                                                                                                 | tuplePush                               |                 |
| first                                                                                                                 | tupleFirst                              |                 |
| at                                                                                                                    | tupleAt                                 |                 |
| touch                                                                                                                 | stackMoveToTop                          | tvm-lowlevel    |
| impure_touch                                                                                     | *(deleted)*          |                 |
| single                                                                                                                | *(deleted)*          |                 |
| unsingle                                                                                                              | *(deleted)*          |                 |
| pair                                                                                                                  | *(deleted)*          |                 |
| unpair                                                                                                                | *(deleted)*          |                 |
| triple                                                                                                                | *(deleted)*          |                 |
| untriple                                                                                                              | *(deleted)*          |                 |
| tuple4                                                                                                                | *(deleted)*          |                 |
| untuple4                                                                                                              | *(deleted)*          |                 |
| second                                                                                                                | *(deleted)*          |                 |
| third                                                                                                                 | *(deleted)*          |                 |
| fourth                                                                                                                | *(deleted)*          |                 |
| pair_first                                                                                       | *(deleted)*          |                 |
| pair_second                                                                                      | *(deleted)*          |                 |
| triple_first                                                                                     | *(deleted)*          |                 |
| triple_second                                                                                    | *(deleted)*          |                 |
| triple_third                                                                                     | *(deleted)*          |                 |
| minmax                                                                                                                | minMax                                  |                 |
| my_address                                                                                       | getMyAddress                            |                 |
| get_balance                                                                                      | getMyOriginalBalanceWithExtraCurrencies |                 |
| cur_lt                                                                                           | getLogicalTime                          |                 |
| block_lt                                                                                         | getCurrentBlockLogicalTime              |                 |
| cell_hash                                                                                        | cellHash                                |                 |
| slice_hash                                                                                       | sliceHash                               |                 |
| string_hash                                                                                      | stringHash                              |                 |
| check_signature                                                                                  | isSignatureValid                        |                 |
| check_data_signature                                                        | isSliceSignatureValid                   |                 |
| compute_data_size                                                           | calculateCellSizeStrict                 |                 |
| slice_compute_data_size                                | calculateSliceSizeStrict                |                 |
| compute_data_size?                                                          | calculateCellSize                       |                 |
| slice_compute_data_size?                               | calculateSliceSize                      |                 |
| ~dump                                                                                                 | debugPrint                              |                 |
| ~strdump                                                                                              | debugPrintString                        |                 |
| dump_stack                                                                                       | debugDumpStack                          |                 |
| get_data                                                                                         | getContractData                         |                 |
| set_data                                                                                         | setContractData                         |                 |
| get_c3                                                                                           | getTvmRegisterC3                        | tvm-lowlevel    |
| set_c3                                                                                           | setTvmRegisterC3                        | tvm-lowlevel    |
| bless                                                                                                                 | transformSliceToContinuation            | tvm-lowlevel    |
| accept_message                                                                                   | acceptExternalMessage                   |                 |
| set_gas_limit                                                               | setGasLimit                             |                 |
| buy_gas                                                                                          | *(deleted)*          |                 |
| commit                                                                                                                | commitContractDataAndActions            |                 |
| divmod                                                                                                                | divMod                                  |                 |
| moddiv                                                                                                                | modDiv                                  |                 |
| muldiv                                                                                                                | mulDivFloor                             |                 |
| muldivr                                                                                                               | mulDivRound                             |                 |
| muldivc                                                                                                               | mulDivCeil                              |                 |
| muldivmod                                                                                                             | mulDivMod                               |                 |
| begin_parse                                                                                      | beginParse                              |                 |
| end_parse                                                                                        | assertEndOfSlice                        |                 |
| load_ref                                                                                         | loadRef                                 |                 |
| preload_ref                                                                                      | preloadRef                              |                 |
| load_int                                                                                         | loadInt                                 |                 |
| load_uint                                                                                        | loadUint                                |                 |
| preload_int                                                                                      | preloadInt                              |                 |
| preload_uint                                                                                     | preloadUint                             |                 |
| load_bits                                                                                        | loadBits                                |                 |
| preload_bits                                                                                     | preloadBits                             |                 |
| load_grams                                                                                       | loadCoins                               |                 |
| load_coins                                                                                       | loadCoins                               |                 |
| skip_bits                                                                                        | skipBits                                |                 |
| first_bits                                                                                       | getFirstBits                            |                 |
| skip_last_bits                                                              | removeLastBits                          |                 |
| slice_last                                                                                       | getLastBits                             |                 |
| load_dict                                                                                        | loadDict                                |                 |
| preload_dict                                                                                     | preloadDict                             |                 |
| skip_dict                                                                                        | skipDict                                |                 |
| load_maybe_ref                                                              | loadMaybeRef                            |                 |
| preload_maybe_ref                                                           | preloadMaybeRef                         |                 |
| cell_depth                                                                                       | getCellDepth                            |                 |
| slice_refs                                                                                       | getRemainingRefsCount                   |                 |
| slice_bits                                                                                       | getRemainingBitsCount                   |                 |
| slice_bits_refs                                                             | getRemainingBitsAndRefsCount            |                 |
| slice_empty?                                                                                     | isEndOfSlice                            |                 |
| slice_data_empty?                                                           | isEndOfSliceBits                        |                 |
| slice_refs_empty?                                                           | isEndOfSliceRefs                        |                 |
| slice_depth                                                                                      | getSliceDepth                           |                 |
| equal_slice_bits                                                            | isSliceBitsEqual                        |                 |
| builder_refs                                                                                     | getBuilderRefsCount                     |                 |
| builder_bits                                                                                     | getBuilderBitsCount                     |                 |
| builder_depth                                                                                    | getBuilderDepth                         |                 |
| begin_cell                                                                                       | beginCell                               |                 |
| end_cell                                                                                         | endCell                                 |                 |
| store_ref                                                                                        | storeRef                                |                 |
| store_uint                                                                                       | storeUint                               |                 |
| store_int                                                                                        | storeInt                                |                 |
| store_slice                                                                                      | storeSlice                              |                 |
| store_grams                                                                                      | storeCoins                              |                 |
| store_coins                                                                                      | storeCoins                              |                 |
| store_dict                                                                                       | storeDict                               |                 |
| store_maybe_ref                                                             | storeMaybeRef                           |                 |
| store_builder                                                                                    | storeBuilder                            |                 |
| load_msg_addr                                                               | loadAddress                             |                 |
| parse_addr                                                                                       | parseAddress                            |                 |
| parse_std_addr                                                              | parseStandardAddress                    |                 |
| parse_var_addr                                                              | *(deleted)*          |                 |
| config_param                                                                                     | getBlockchainConfigParam                |                 |
| raw_reserve                                                                                      | reserveToncoinsOnBalance                |                 |
| raw_reserve_extra                                                           | reserveExtraCurrenciesOnBalance         |                 |
| send_raw_message                                                            | sendRawMessage                          |                 |
| set_code                                                                                         | setContractCodePostponed                |                 |
| rand                                                                                                                  | randomRange                             |                 |
| get_seed                                                                                         | randomGetSeed                           |                 |
| set_seed                                                                                         | randomSetSeed                           |                 |
| randomize                                                                                                             | randomizeBy                             |                 |
| randomize_lt                                                                                     | randomizeByLogicalTime                  |                 |
| dump                                                                                                                  | debugPrint                              |                 |
| strdump                                                                                                               | debugPrintString                        |                 |
| dump_stk                                                                                         | debugDumpStack                          |                 |
| empty_list                                                                                       | createEmptyList                         | lisp-lists      |
| cons                                                                                                                  | listPrepend                             | lisp-lists      |
| uncons                                                                                                                | listSplit                               | lisp-lists      |
| list_next                                                                                        | listNext                                | lisp-lists      |
| car                                                                                                                   | listGetHead                             | lisp-lists      |
| cdr                                                                                                                   | listGetTail                             | lisp-lists      |
| new_dict                                                                                         | createEmptyDict                         | tvm-dicts       |
| dict_empty?                                                                                      | dictIsEmpty                             | tvm-dicts       |
| idict_set_ref                                                               | iDictSetRef                             | tvm-dicts       |
| udict_set_ref                                                               | uDictSetRef                             | tvm-dicts       |
| idict_get_ref                                                               | iDictGetRefOrNull                       | tvm-dicts       |
| idict_get_ref?                                                              | iDictGetRef                             | tvm-dicts       |
| udict_get_ref?                                                              | uDictGetRef                             | tvm-dicts       |
| idict_set_get_ref                                      | iDictSetAndGetRefOrNull                 | tvm-dicts       |
| udict_set_get_ref                                      | iDictSetAndGetRefOrNull                 | tvm-dicts       |
| idict_delete?                                                                                    | iDictDelete                             | tvm-dicts       |
| udict_delete?                                                                                    | uDictDelete                             | tvm-dicts       |
| idict_get?                                                                                       | iDictGet                                | tvm-dicts       |
| udict_get?                                                                                       | uDictGet                                | tvm-dicts       |
| idict_delete_get?                                                           | iDictDeleteAndGet                       | tvm-dicts       |
| udict_delete_get?                                                           | uDictDeleteAndGet                       | tvm-dicts       |
| udict_set                                                                                        | uDictSet                                | tvm-dicts       |
| idict_set                                                                                        | iDictSet                                | tvm-dicts       |
| dict_set                                                                                         | sDictSet                                | tvm-dicts       |
| udict_add?                                                                                       | uDictSetIfNotExists                     | tvm-dicts       |
| udict_replace?                                                                                   | uDictSetIfExists                        | tvm-dicts       |
| idict_add?                                                                                       | iDictSetIfNotExists                     | tvm-dicts       |
| idict_replace?                                                                                   | iDictSetIfExists                        | tvm-dicts       |
| udict_set_builder                                                           | uDictSetBuilder                         | tvm-dicts       |
| idict_set_builder                                                           | iDictSetBuilder                         | tvm-dicts       |
| dict_set_builder                                                            | sDictSetBuilder                         | tvm-dicts       |
| udict_add_builder?                                                          | uDictSetBuilderIfNotExists              | tvm-dicts       |
| udict_replace_builder?                                                      | uDictSetBuilderIfExists                 | tvm-dicts       |
| idict_add_builder?                                                          | iDictSetBuilderIfNotExists              | tvm-dicts       |
| idict_replace_builder?                                                      | iDictSetBuilderIfExists                 | tvm-dicts       |
| udict_delete_get_min                                   | uDictDeleteFirstAndGet                  | tvm-dicts       |
| idict_delete_get_min                                   | iDictDeleteFirstAndGet                  | tvm-dicts       |
| dict_delete_get_min                                    | sDictDeleteFirstAndGet                  | tvm-dicts       |
| udict_delete_get_max                                   | uDictDeleteLastAndGet                   | tvm-dicts       |
| idict_delete_get_max                                   | iDictDeleteLastAndGet                   | tvm-dicts       |
| dict_delete_get_max                                    | sDictDeleteLastAndGet                   | tvm-dicts       |
| udict_get_min?                                                              | uDictGetFirst                           | tvm-dicts       |
| udict_get_max?                                                              | uDictGetLast                            | tvm-dicts       |
| udict_get_min_ref?                                     | uDictGetFirstAsRef                      | tvm-dicts       |
| udict_get_max_ref?                                     | uDictGetLastAsRef                       | tvm-dicts       |
| idict_get_min?                                                              | iDictGetFirst                           | tvm-dicts       |
| idict_get_max?                                                              | iDictGetLast                            | tvm-dicts       |
| idict_get_min_ref?                                     | iDictGetFirstAsRef                      | tvm-dicts       |
| idict_get_max_ref?                                     | iDictGetLastAsRef                       | tvm-dicts       |
| udict_get_next?                                                             | uDictGetNext                            | tvm-dicts       |
| udict_get_nexteq?                                                           | uDictGetNextOrEqual                     | tvm-dicts       |
| udict_get_prev?                                                             | uDictGetPrev                            | tvm-dicts       |
| udict_get_preveq?                                                           | uDictGetPrevOrEqual                     | tvm-dicts       |
| idict_get_next?                                                             | iDictGetNext                            | tvm-dicts       |
| idict_get_nexte idict_get_nexteq? | iDictGetNextOrEqual                     | tvm-dicts       |
| idict_get_prev?                                                             | iDictGetPrev                            | tvm-dicts       |
| idict_get_preveq?                                                           | iDictGetPrevOrEqual                     | tvm-dicts       |
| udict::delete_get_min                       | uDictDeleteFirstAndGet                  | tvm-dicts       |
| idict::delete_get_min                       | iDictDeleteFirstAndGet                  | tvm-dicts       |
| dict::delete_get_min                        | sDictDeleteFirstAndGet                  | tvm-dicts       |
| udict::delete_get_max                       | uDictDeleteLastAndGet                   | tvm-dicts       |
| idict::delete_get_max                       | iDictDeleteLastAndGet                   | tvm-dicts       |
| dict::delete_get_max                        | sDictDeleteLastAndGet                   | tvm-dicts       |
| pfxdict_get?                                                                                     | prefixDictGet                           | tvm-dicts       |
| pfxdict_set?                                                                                     | prefixDictSet                           | tvm-dicts       |
| pfxdict_delete?                                                                                  | prefixDictDelete                        | tvm-dicts       |

## 추가된 함수들의 목록

Tolk 표준 라이브러리는 FunC에는 없었지만 일상적인 작업에 꽤 일반적인 일부 함수들을 가지고 있습니다.

Tolk가 활발하게 개발되고 있고 표준 라이브러리가 변경되고 있으므로, [여기](https://github.com/ton-blockchain/ton/tree/master/crypto/smartcont/tolk-stdlib)의 소스에서 `tolk-stdlib/` 폴더를 참고하는 것이 좋습니다.
함수 외에도 일부 상수가 추가되었습니다: `SEND_MODE_*`, `RESERVE_MODE_*` 등.

FunC가 더 이상 사용되지 않게 되면, Tolk stdlib에 대한 문서는 어쨌든 완전히 다시 작성될 것입니다.

그리고 위의 모든 함수들이 실제로는 TVM 어셈블러에 대한 래퍼라는 것을 기억하세요. 무언가 누락되었다면,
어떤 TVM 명령어든 직접 래핑할 수 있습니다.

## 일부 함수들이 복사본을 반환하지 않고 변경하는 함수가 되었습니다

<table className="cmp-func-tolk-table">
  <thead>
  <tr>
    <th>FunC</th>
    <th>Tolk</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td><code>{'int flags = cs~load_uint(32);'}</code></td>
    <td><code>{'var flags = cs.loadUint(32);'}</code></td>
  </tr>
  <tr>
    <td><code>{'dict~udict_set(...);'}</code></td>
    <td><code>{'dict.uDictSet(...);'}</code></td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
  </tr>
  </tbody>
</table>

실제로 `~` 틸다와 함께 사용되었던 대부분의 FunC 함수들은 이제 객체를 변경합니다. 위의 예시를 참조하세요.

예를 들어, `dict~udict_set(…)`를 사용했다면, 단순히 `dict.uDictSet(…)`를 사용하면 모든 것이 잘 작동합니다.
하지만 복사본을 얻기 위해 `dict.udict_set(…)`를 사용했다면, 다른 방식으로 표현해야 할 것입니다.

[가변성에 대해 읽어보세요](/v3/documentation/smart-contracts/tolk/tolk-vs-func/mutability).

## 내장된 stdlib은 내부적으로 어떻게 작동하나요

위에서 말했듯이, 모든 표준 함수는 즉시 사용할 수 있습니다.
네, 비-공통 함수에 대해서는 `import`가 필요하지만(의도적입니다), 여전히 외부 다운로드는 필요 없습니다.

다음과 같은 방식으로 작동합니다.

Tolk 컴파일러가 시작할 때 가장 먼저 하는 일은 실행 파일 바이너리를 기준으로 미리 정의된 경로에서 stdlib 폴더를 찾는 것입니다.
예를 들어, 설치된 패키지에서 Tolk 컴파일러를 실행하면(예: `/usr/bin/tolk`), `/usr/share/ton/smartcont`에서 stdlib을 찾습니다.
비표준 설치를 한 경우 `TOLK_STDLIB` 환경 변수를 전달할 수 있습니다. 이는 컴파일러의 표준 관행입니다.

WASM 래퍼인 [tolk-js](https://github.com/ton-blockchain/tolk-js)도 stdlib을 포함하고 있습니다.
따라서 tolk-js나 blueprint를 사용할 때도 모든 stdlib 함수를 즉시 사용할 수 있습니다.

IDE 플러그인(JetBrains와 VS Code 모두)도 자동 완성을 제공하기 위해 stdlib을 자동으로 찾습니다.
blueprint를 사용하는 경우 자동으로 tolk-js를 설치하므로 프로젝트 파일 구조에 `node_modules/@ton/tolk-js/` 폴더가 존재합니다.
그 안에는 `common.tolk`, `tvm-dicts.tolk` 등이 있습니다.
