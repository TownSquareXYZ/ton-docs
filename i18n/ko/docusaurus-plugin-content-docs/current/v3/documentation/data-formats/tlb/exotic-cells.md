# 특수 셀

모든 셀은 -1에서 255 사이의 정수로 인코딩된 자체 유형을 갖습니다.
유형 -1인 셀은 `일반` 셀이고, 나머지는 `특수` 또는 `이국적인` 셀이라고 합니다.
특수 셀의 유형은 데이터의 첫 8비트에 저장됩니다. 특수 셀의 데이터 비트가 8비트 미만이면 유효하지 않습니다.
현재 4가지 특수 셀 유형이 있습니다:

```json
{
  Prunned Branch: 1,
  Library Reference: 2,
  Merkle Proof: 3,
  Merkle Update: 4
}
```

### 가지치기된 브랜치

가지치기된 브랜치는 삭제된 셀의 하위 트리를 나타내는 셀입니다.

레벨 `1 <= l <= 3`을 가질 수 있으며 정확히 `8 + 8 + 256 * l + 16 * l` 비트를 포함합니다.

첫 번째 바이트는 항상 `01` - 셀 유형입니다. 두 번째는 가지치기된 브랜치 레벨 마스크입니다. 그 다음에는 삭제된 하위 트리의 해시 `l * 32` 바이트가 오고 그 뒤에 삭제된 하위 트리의 깊이 `l * 2` 바이트가 옵니다.

브랜치가 가지치기된 머클 증명이나 머클 업데이트의 구성 중에 결정되기 때문에 가지치기된 브랜치 셀의 레벨 `l`을 드 브루인 인덱스라고 부를 수 있습니다.

가지치기된 브랜치의 상위 해시는 데이터에 저장되며 다음과 같이 얻을 수 있습니다:

```cpp
Hash_i = CellData[2 + (i * 32) : 2 + ((i + 1) * 32)]
```

### 라이브러리 참조

라이브러리 참조 셀은 스마트 계약에서 라이브러리를 사용하는 데 사용됩니다.

항상 레벨 0을 가지며 `8 + 256` 비트를 포함합니다.

첫 번째 바이트는 항상 `02` - 셀 유형입니다. 다음 32바이트는 참조되는 라이브러리 셀의 [표현 해시](/v3/documentation/data-formats/tlb/cell-boc#standard-cell-representation-hash-calculation)입니다.

### 머클 증명

머클 증명 셀은 셀 트리 데이터의 일부가 전체 트리에 속하는지 확인하는 데 사용됩니다. 이 설계를 통해 검증자는 트리의 전체 내용을 저장하지 않고도 루트 해시로 내용을 확인할 수 있습니다.

머클 증명은 정확히 하나의 참조를 가지며 레벨 `0 <= l <= 3`은 `max(Lvl(ref) - 1, 0)`이어야 합니다. 이 셀들은 정확히 `8 + 256 + 16 = 280` 비트를 포함합니다.

첫 번째 바이트는 항상 `03` - 셀 유형입니다. 다음 32바이트는 `Hash_1(ref)`(또는 참조 레벨이 0인 경우 `ReprHash(ref)`)입니다. 다음 2바이트는 참조로 대체된 삭제된 하위 트리의 깊이입니다.

머클 증명 셀의 상위 해시 `Hash_i`는 일반 셀의 상위 해시와 유사하게 계산되지만, `Hash_i(ref)` 대신 `Hash_i+1(ref)`를 사용합니다.

### 머클 업데이트

머클 업데이트 셀은 항상 2개의 참조를 가지며 두 참조 모두에 대한 머클 증명처럼 동작합니다.

머클 업데이트 레벨 `0 <= l <= 3`은 `max(Lvl(ref1) − 1, Lvl(ref2) − 1, 0)`입니다. 정확히 `8 + 256 + 256 + 16 + 16 = 552` 비트를 포함합니다.

첫 번째 바이트는 항상 `04` - 셀 유형입니다. 다음 64바이트는 `Hash_1(ref1)`과 `Hash_2(ref2)` - 이전 해시와 새 해시라고 합니다. 그 다음에는 삭제된 이전 하위 트리와 새 하위 트리의 실제 깊이를 나타내는 4바이트가 옵니다.

## 간단한 증명 검증 예제

셀 `c`가 있다고 가정해봅시다:

```json
24[000078] -> {
	32[0000000F] -> {
		1[80] -> {
			32[0000000E]
		},
		1[00] -> {
			32[0000000C]
		}
	},
	16[000B] -> {
		4[80] -> {
			267[800DEB78CF30DC0C8612C3B3BE0086724D499B25CB2FBBB154C086C8B58417A2F040],
			512[00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000064]
		}
	}
}
```

하지만 우리는 해시 `44efd0fdfffa8f152339a0191de1e1c5901fdcfe13798af443640af99616b977`만 알고 있고, 전체 `c`를 받지 않고도 셀 `a` `267[800DEB78CF30DC0C8612C3B3BE0086724D499B25CB2FBBB154C086C8B58417A2F040]`가 실제로 `c`의 일부임을 증명하고 싶습니다.
따라서 우리는 증명자에게 관심 없는 모든 브랜치를 가지치기된 브랜치 셀로 대체하여 머클 증명을 만들도록 요청합니다.

`a`에 도달할 수 없는 첫 번째 `c` 자손은 `ref1`입니다:

```json
32[0000000F] -> {
	1[80] -> {
		32[0000000E]
	},
	1[00] -> {
		32[0000000C]
	}
}
```

따라서 증명자는 해시(`ec7c1379618703592804d3a33f7e120cebe946fa78a6775f6ee2e28d80ddb7dc`)를 계산하고, 가지치기된 브랜치 `288[0101EC7C1379618703592804D3A33F7E120CEBE946FA78A6775F6EE2E28D80DDB7DC0002]`를 만들어 `ref1`을 대체합니다.

두 번째는 `512[0000000...00000000064]`이므로, 증명자는 이 셀도 대체할 가지치기된 브랜치를 만듭니다:

```json
24[000078] -> {
	288[0101EC7C1379618703592804D3A33F7E120CEBE946FA78A6775F6EE2E28D80DDB7DC0002],
	16[000B] -> {
		4[80] -> {
			267[800DEB78CF30DC0C8612C3B3BE0086724D499B25CB2FBBB154C086C8B58417A2F040],
			288[0101A458B8C0DC516A9B137D99B701BB60FE25F41F5ACFF2A54A2CA4936688880E640000]
		}
	}
}
```

증명자가 검증자(이 예제에서는 우리)에게 보내는 결과 머클 증명은 다음과 같습니다:

```json
280[0344EFD0FDFFFA8F152339A0191DE1E1C5901FDCFE13798AF443640AF99616B9770003] -> {
	24[000078] -> {
		288[0101EC7C1379618703592804D3A33F7E120CEBE946FA78A6775F6EE2E28D80DDB7DC0002],
		16[000B] -> {
			4[80] -> {
				267[800DEB78CF30DC0C8612C3B3BE0086724D499B25CB2FBBB154C086C8B58417A2F040],
				288[0101A458B8C0DC516A9B137D99B701BB60FE25F41F5ACFF2A54A2CA4936688880E640000]
			}
		}
	}
}
```

우리(검증자)가 증명 셀을 받으면 데이터에 `c` 해시가 포함되어 있는지 확인한 다음, 유일한 증명 참조에서 `Hash_1`을 계산합니다: `44efd0fdfffa8f152339a0191de1e1c5901fdcfe13798af443640af99616b977`, 그리고 `c` 해시와 비교합니다.

이제 해시가 일치하는지 확인했으므로, 셀 깊숙이 들어가서 셀 `a`(우리가 관심 있는)가 있는지 확인해야 합니다.

이러한 증명은 계산 부하와 검증자에게 보내거나 저장해야 하는 데이터의 양을 반복적으로 줄입니다.

## 참고

- [고급 증명 검증 예제](/v3/documentation/data-formats/tlb/proofs)