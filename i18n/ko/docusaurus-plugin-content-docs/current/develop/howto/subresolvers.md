# TON DNS 확인자

## 소개

TON DNS는 강력한 도구입니다. TON 사이트/스토리지 백을 도메인에 할당할 수 있을 뿐만 아니라 하위 도메인 확인을 설정할 수도 있습니다.

## 관련 링크

1. [TON 스마트 컨트랙트 주소 시스템](/학습/개요/주소)
2. [TEP-0081 - TON DNS 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md)
3. [.ton DNS 수집 소스 코드](https://tonscan.org/address/EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz#source)
4. [.t.me DNS 수집 소스 코드](https://tonscan.org/address/EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi#source)
5. [도메인 계약 검색기](https://tonscan.org/address/EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH_Zp#source)
6. [간편 하위도메인 관리자 코드](https://github.com/Gusarich/simple-subdomain/blob/198485bbc9f7f6632165b7ab943902d4e125d81a/contracts/subdomain-manager.fc)

## 도메인 계약 검색기

하위 도메인은 실용적인 용도로 사용됩니다. 예를 들어, 현재 블록체인 탐색기는 이름만으로 도메인 컨트랙트를 찾을 수 있는 방법을 제공하지 않습니다. 이러한 도메인을 찾을 수 있는 컨트랙트를 만드는 방법을 살펴보겠습니다.

:::info
This contract is deployed at [EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH\_Zp](https://tonscan.org/address/EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH_Zp#source) and linked to `resolve-contract.ton`. To test it, you may write `<your-domain.ton>.resolve-contract.ton` in the address bar of your favourite TON explorer and get to the page of TON DNS domain contract. Subdomains and .t.me domains are supported as well.

'resolve-contract.ton.resolve-contract.ton'으로 이동하여 리졸버 코드를 확인하려고 시도해 볼 수 있습니다. 안타깝게도 하위 리졸버(다른 스마트 계약)는 표시되지 않으며 도메인 계약 자체 페이지가 표시됩니다(
::):

### dnsresolve() 코드

일부 반복되는 부분은 생략되었습니다.

```func
(int, cell) dnsresolve(slice subdomain, int category) method_id {
  int subdomain_bits = slice_bits(subdomain);
  throw_unless(70, (subdomain_bits % 8) == 0);
  
  int starts_with_zero_byte = subdomain.preload_int(8) == 0;  ;; assuming that 'subdomain' is not empty
  if (starts_with_zero_byte) {
    subdomain~load_uint(8);
    if (subdomain.slice_bits() == 0) {   ;; current contract has no DNS records by itself
      return (8, null());
    }
  }
  
  ;; we are loading some subdomain
  ;; supported subdomains are "ton\0", "me\0t\0" and "address\0"
  
  slice subdomain_sfx = null();
  builder domain_nft_address = null();
  
  if (subdomain.starts_with("746F6E00"s)) {
    ;; we're resolving
    ;; "ton" \0 <subdomain> \0 [subdomain_sfx]
    subdomain~skip_bits(32);
    
    ;; reading domain name
    subdomain_sfx = subdomain;
    while (subdomain_sfx~load_uint(8)) { }
    
    subdomain~skip_last_bits(8 + slice_bits(subdomain_sfx));
    
    domain_nft_address = get_ton_dns_nft_address_by_index(slice_hash(subdomain));
  } elseif (subdomain.starts_with("6164647265737300"s)) {
    subdomain~skip_bits(64);
    
    domain_nft_address = subdomain~decode_base64_address_to(begin_cell());
    
    subdomain_sfx = subdomain;
    if (~ subdomain_sfx.slice_empty?()) {
      throw_unless(71, subdomain_sfx~load_uint(8) == 0);
    }
  } else {
    return (0, null());
  }
  
  if (slice_empty?(subdomain_sfx)) {
    ;; example of domain being resolved:
    ;; [initial, not accessible in this contract] "ton\0resolve-contract\0ton\0ratelance\0"
    ;; [what is accessible by this contract]      "ton\0ratelance\0"
    ;; subdomain          "ratelance"
    ;; subdomain_sfx      ""
    
    ;; we want the resolve result to point at contract of 'ratelance.ton', not its owner
    ;; so we must answer that resolution is complete + "wallet"H is address of 'ratelance.ton' contract
    
    ;; dns_smc_address#9fd3 smc_addr:MsgAddressInt flags:(## 8) { flags <= 1 } cap_list:flags . 0?SmcCapList = DNSRecord;
    ;; _ (HashmapE 256 ^DNSRecord) = DNS_RecordSet;
    
    cell wallet_record = begin_cell().store_uint(0x9fd3, 16).store_builder(domain_nft_address).store_uint(0, 8).end_cell();
    
    if (category == 0) {
      cell dns_dict = new_dict();
      dns_dict~udict_set_ref(256, "wallet"H, wallet_record);
      return (subdomain_bits, dns_dict);
    } elseif (category == "wallet"H) {
      return (subdomain_bits, wallet_record);
    } else {
      return (subdomain_bits, null());
    }
  } else {
    ;; subdomain          "resolve-contract"
    ;; subdomain_sfx      "ton\0ratelance\0"
    ;; we want to pass \0 further, so that next resolver has opportunity to process only one byte
    
    ;; next resolver is contract of 'resolve-contract<.ton>'
    ;; dns_next_resolver#ba93 resolver:MsgAddressInt = DNSRecord;
    cell resolver_record = begin_cell().store_uint(0xba93, 16).store_builder(domain_nft_address).end_cell();
    return (subdomain_bits - slice_bits(subdomain_sfx) - 8, resolver_record);
  }
}
```

### dnsresolve()에 대한 설명

- 사용자가 `"stabletimer.ton.resolve-contract.ton"`을 요청합니다.
- 애플리케이션은 이를 '\0톤\0resolve-contract\0톤\0안정 타이머\0'로 변환합니다(첫 번째 0바이트는 선택 사항).
- 루트 DNS 확인자는 요청을 TON DNS 수집에 전달하고 나머지 부분은 `"\0resolve-contract\0ton\0stabletimer\0"`입니다.
- TON DNS 수집은 특정 도메인에 요청을 위임하여 `"\0ton\0stabletimer\0"`를 남깁니다.
- .TON DNS 도메인 계약은 편집자가 지정한 하위 확인자로 확인을 전달하며, 하위 도메인은 `"ton\0stabletimer\0"`입니다.

**이 지점에서 dnsresolve()가 호출됩니다.** 작동 방식에 대한 단계별 분석입니다:

1. 하위 도메인과 카테고리를 입력으로 받습니다.
2. 처음에 0바이트가 있으면 건너뜁니다.
3. 하위 도메인이 `"ton\0"`으로 시작하는지 확인합니다. 그렇다면,
   1. 처음 32비트를 건너뜁니다(하위 도메인 = `"resolve-contract\0"`).
   2. 서브도메인_SFX`값이`SUB도메인\`으로 설정되면 함수는 0바이트까지 바이트를 읽습니다.
   3. (하위 도메인 = `"resolve-contract\0"`, 하위 도메인_sfx = `""`)
   4. 하위 도메인 슬라이스 끝에서 0바이트 및 subdomain_sfx가 잘립니다(하위 도메인 = `"resolve-contract"`).
   5. 함수 slice_hash 및 get_ton_dns_nft_address_by_index는 도메인 이름을 계약 주소로 변환하는 데 사용됩니다. 이 함수는 [[하위 해결자#부록 1. 해결 코드-계약.ton|부록 1]]에서 확인할 수 있습니다.
4. 그렇지 않으면 dnsresolve()는 하위 도메인이 `"address\0"`으로 시작하는지 확인합니다. 그렇다면 해당 접두사를 건너뛰고 base64 주소를 읽습니다.
5. 확인을 위해 제공된 하위 도메인이 이러한 접두사 중 어느 것과도 일치하지 않으면 함수는 `(0, null()`(DNS 항목 없이 0바이트 접두사가 확인됨)을 반환하여 실패를 나타냅니다.)
6. 그런 다음 하위 도메인 접미사가 비어 있는지 확인합니다. 접미사가 비어 있으면 요청이 완전히 충족되었음을 나타냅니다. 접미사가 비어 있으면
   1. dnsresolve()는 검색한 TON 도메인 계약 주소를 사용하여 도메인의 "지갑" 하위 섹션에 대한 DNS 레코드를 생성합니다.
   2. 카테고리 0(모든 DNS 항목)이 요청되면 레코드가 사전으로 래핑되어 반환됩니다.
   3. 카테고리 "지갑"H를 요청하면 레코드가 그대로 반환됩니다.
   4. 그렇지 않으면 지정된 카테고리에 대한 DNS 항목이 없으므로 확인은 성공했지만 결과를 찾지 못했음을 나타냅니다.
7. 접미사가 비어 있지 않은 경우:
   1. 이전에 얻은 컨트랙트 주소가 다음 리졸버로 사용됩니다. 이 함수는 이를 가리키는 다음 리졸버 레코드를 빌드합니다.
   2. "\0톤\0스테이블타이머\0"\`는 해당 컨트랙트로 더 전달됩니다: 처리된 비트는 하위 도메인의 비트입니다.

요약하자면, dnsresolve() 역시 마찬가지입니다:

- 하위 도메인을 DNS 레코드로 완전히 확인합니다.
- 해결자 레코드로 부분적으로 해결하여 다른 컨트랙트로 해결을 전달합니다.
- 알 수 없는 하위 도메인에 대해 "도메인을 찾을 수 없음" 결과를 반환합니다.

:::warning
실제로 base64 주소 구문 분석이 작동하지 않습니다. `<some-address>.address.resolve-contract.ton`을 입력하려고 하면 도메인이 잘못 구성되었거나 존재하지 않는다는 오류가 표시됩니다. 그 이유는 도메인 이름이 대소문자를 구분하지 않기 때문에(실제 DNS에서 상속된 기능) 소문자로 변환되어 존재하지 않는 워크체인 주소로 이동하기 때문입니다.
:::

### 리졸버 바인딩

이제 하위 레졸버 컨트랙트가 배포되었으므로 도메인을 가리키도록, 즉 도메인 `dns_next_resolver` 레코드를 변경해야 합니다. 이를 위해 다음 TL-B 구조의 메시지를 도메인 컨트랙트에 전송하면 됩니다.

1. `change_dns_record#4eb1f0f9 query_id:uint64 record_key#19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff record:^[dns_next_resolver#ba93 resolver:MsgAddressInt]`

## 자체 하위 도메인 관리자 만들기

하위 도메인은 여러 프로젝트를 하나의 도메인에 연결하거나 친구의 지갑에 연결하는 등 일반 사용자에게 유용할 수 있습니다.

### 계약 데이터

컨트랙트 데이터에 소유자의 주소와 *도메인*->*레코드 해시*->*레코드 값* 딕셔너리를 저장해야 합니다.

```func
global slice owner;
global cell domains;

() load_data() impure {
  slice ds = get_data().begin_parse();
  owner = ds~load_msg_addr();
  domains = ds~load_dict();
}
() save_data() impure {
  set_data(begin_cell().store_slice(owner).store_dict(domains).end_cell());
}
```

### 처리 기록 업데이트

```func
const int op::update_record = 0x537a3491;
;; op::update_record#537a3491 domain_name:^Cell record_key:uint256
;;     value:(Maybe ^Cell) = InMsgBody;

() recv_internal(cell in_msg, slice in_msg_body) {
  if (in_msg_body.slice_empty?()) { return (); }   ;; simple money transfer

  slice in_msg_full = in_msg.begin_parse();
  if (in_msg_full~load_uint(4) & 1) { return (); } ;; bounced message

  slice sender = in_msg_full~load_msg_addr();
  load_data();
  throw_unless(501, equal_slices(sender, owner));
  
  int op = in_msg_body~load_uint(32);
  if (op == op::update_record) {
    slice domain = in_msg_body~load_ref().begin_parse();
    (cell records, _) = domains.udict_get_ref?(256, string_hash(domain));

    int key = in_msg_body~load_uint(256);
    throw_if(502, key == 0);  ;; cannot update "all records" record

    if (in_msg_body~load_uint(1) == 1) {
      cell value = in_msg_body~load_ref();
      records~udict_set_ref(256, key, value);
    } else {
      records~udict_delete?(256, key);
    }

    domains~udict_set_ref(256, string_hash(domain), records);
    save_data();
  }
}
```

수신 메시지에 일부 요청이 포함되어 있고 반송되지 않았으며 소유자가 보낸 것인지, 요청이 `op::update_record`인지 확인합니다.

그런 다음 메시지에서 도메인 이름을 로드합니다. 도메인은 길이가 다를 수 있지만 접두사가 없는 TVM 사전은 동일한 길이의 키만 포함할 수 있기 때문에 도메인을 그대로 저장할 수 없습니다. 따라서 도메인 이름의 SHA-256인 '문자열 해시(도메인)\`를 계산합니다. 도메인 이름은 정수의 옥텟 수를 갖도록 보장되므로 작동합니다.

그 후 지정된 도메인에 대한 레코드를 업데이트하고 새 데이터를 컨트랙트 저장소에 저장합니다.

### 도메인 확인

```func
(slice, slice) ~parse_sd(slice subdomain) {
  ;; "test\0qwerty\0" -> "test" "qwerty\0"
  slice subdomain_sfx = subdomain;
  while (subdomain_sfx~load_uint(8)) { }  ;; searching zero byte
  subdomain~skip_last_bits(slice_bits(subdomain_sfx));
  return (subdomain, subdomain_sfx);
}

(int, cell) dnsresolve(slice subdomain, int category) method_id {
  int subdomain_bits = slice_bits(subdomain);
  throw_unless(70, subdomain_bits % 8 == 0);
  if (subdomain.preload_uint(8) == 0) { subdomain~skip_bits(8); }
  
  slice subdomain_suffix = subdomain~parse_sd();  ;; "test\0" -> "test" ""
  int subdomain_suffix_bits = slice_bits(subdomain_suffix);

  load_data();
  (cell records, _) = domains.udict_get_ref?(256, string_hash(subdomain));

  if (subdomain_suffix_bits > 0) { ;; more than "<SUBDOMAIN>\0" requested
    category = "dns_next_resolver"H;
  }

  int resolved = subdomain_bits - subdomain_suffix_bits;

  if (category == 0) { ;; all categories are requested
    return (resolved, records);
  }

  (cell value, int found) = records.udict_get_ref?(256, category);
  return (resolved, value);
}
```

dnsresolve` 함수는 요청된 하위 도메인에 정수의 옥텟이 포함되어 있는지 확인하고, 하위 도메인 슬라이스 시작 부분의 선택적 0 바이트를 건너뛴 다음 최상위 도메인과 그 외 모든 도메인으로 분할합니다(`test\0qwerty\0`는 `test`와 `qwerty\0\`로 분할됩니다). 요청된 도메인에 해당하는 레코드 사전이 로드됩니다.

비어 있지 않은 하위 도메인 접미사가 있으면 이 함수는 확인된 바이트 수와 `"dns_next_resolver"H` 키에서 찾을 수 있는 다음 확인자 레코드를 반환합니다. 그렇지 않으면 이 함수는 확인된 바이트 수(즉, 전체 슬라이스 길이)와 요청된 레코드를 반환합니다.

오류를 더 우아하게 처리하여 이 기능을 개선할 수 있는 방법이 있지만 반드시 필요한 것은 아닙니다.

## 부록 1. 결의문-계약서.ton

<details>
<summary>subresolver.fc</summary>

```func showLineNumbers
(builder, ()) ~store_slice(builder to, slice s) asm "STSLICER";
int starts_with(slice a, slice b) asm "SDPFXREV";

const slice ton_dns_minter = "EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz"a;
cell ton_dns_domain_code() asm """
  B{<TON DNS NFT code in HEX format>}
  B>boc
  PUSHREF
""";

const slice tme_minter = "EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi"a;
cell tme_domain_code() asm """
  B{<T.ME NFT code in HEX format>}
  B>boc
  PUSHREF
""";

cell calculate_ton_dns_nft_item_state_init(int item_index) inline {
  cell data = begin_cell().store_uint(item_index, 256).store_slice(ton_dns_minter).end_cell();
  return begin_cell().store_uint(0, 2).store_dict(ton_dns_domain_code()).store_dict(data).store_uint(0, 1).end_cell();
}

cell calculate_tme_nft_item_state_init(int item_index) inline {
  cell config = begin_cell().store_uint(item_index, 256).store_slice(tme_minter).end_cell();
  cell data = begin_cell().store_ref(config).store_maybe_ref(null()).end_cell();
  return begin_cell().store_uint(0, 2).store_dict(tme_domain_code()).store_dict(data).store_uint(0, 1).end_cell();
}

builder calculate_nft_item_address(int wc, cell state_init) inline {
  return begin_cell()
      .store_uint(4, 3)
      .store_int(wc, 8)
      .store_uint(cell_hash(state_init), 256);
}

builder get_ton_dns_nft_address_by_index(int index) inline {
  cell state_init = calculate_ton_dns_nft_item_state_init(index);
  return calculate_nft_item_address(0, state_init);
}

builder get_tme_nft_address_by_index(int index) inline {
  cell state_init = calculate_tme_nft_item_state_init(index);
  return calculate_nft_item_address(0, state_init);
}

(slice, builder) decode_base64_address_to(slice readable, builder target) inline {
  builder addr_with_flags = begin_cell();
  repeat(48) {
    int char = readable~load_uint(8);
    if (char >= "a"u) {
      addr_with_flags~store_uint(char - "a"u + 26, 6);
    } elseif ((char == "_"u) | (char == "/"u)) {
      addr_with_flags~store_uint(63, 6);
    } elseif (char >= "A"u) {
      addr_with_flags~store_uint(char - "A"u, 6);
    } elseif (char >= "0"u) {
      addr_with_flags~store_uint(char - "0"u + 52, 6);
    } else {
      addr_with_flags~store_uint(62, 6);
    }
  }
  
  slice addr_with_flags = addr_with_flags.end_cell().begin_parse();
  addr_with_flags~skip_bits(8);
  addr_with_flags~skip_last_bits(16);
  
  target~store_uint(4, 3);
  target~store_slice(addr_with_flags);
  return (readable, target);
}

slice decode_base64_address(slice readable) method_id {
  (slice _remaining, builder addr) = decode_base64_address_to(readable, begin_cell());
  return addr.end_cell().begin_parse();
}

(int, cell) dnsresolve(slice subdomain, int category) method_id {
  int subdomain_bits = slice_bits(subdomain);

  throw_unless(70, (subdomain_bits % 8) == 0);
  
  int starts_with_zero_byte = subdomain.preload_int(8) == 0;  ;; assuming that 'subdomain' is not empty
  if (starts_with_zero_byte) {
    subdomain~load_uint(8);
    if (subdomain.slice_bits() == 0) {   ;; current contract has no DNS records by itself
      return (8, null());
    }
  }
  
  ;; we are loading some subdomain
  ;; supported subdomains are "ton\0", "me\0t\0" and "address\0"
  
  slice subdomain_sfx = null();
  builder domain_nft_address = null();
  
  if (subdomain.starts_with("746F6E00"s)) {
    ;; we're resolving
    ;; "ton" \0 <subdomain> \0 [subdomain_sfx]
    subdomain~skip_bits(32);
    
    ;; reading domain name
    subdomain_sfx = subdomain;
    while (subdomain_sfx~load_uint(8)) { }
    
    subdomain~skip_last_bits(8 + slice_bits(subdomain_sfx));
    
    domain_nft_address = get_ton_dns_nft_address_by_index(slice_hash(subdomain));
  } elseif (subdomain.starts_with("6D65007400"s)) {
    ;; "t" \0 "me" \0 <subdomain> \0 [subdomain_sfx]
    subdomain~skip_bits(40);
    
    ;; reading domain name
    subdomain_sfx = subdomain;
    while (subdomain_sfx~load_uint(8)) { }
    
    subdomain~skip_last_bits(8 + slice_bits(subdomain_sfx));
    
    domain_nft_address = get_tme_nft_address_by_index(string_hash(subdomain));
  } elseif (subdomain.starts_with("6164647265737300"s)) {
    subdomain~skip_bits(64);
    
    domain_nft_address = subdomain~decode_base64_address_to(begin_cell());
    
    subdomain_sfx = subdomain;
    if (~ subdomain_sfx.slice_empty?()) {
      throw_unless(71, subdomain_sfx~load_uint(8) == 0);
    }
  } else {
    return (0, null());
  }
  
  if (slice_empty?(subdomain_sfx)) {
    ;; example of domain being resolved:
    ;; [initial, not accessible in this contract] "ton\0resolve-contract\0ton\0ratelance\0"
    ;; [what is accessible by this contract]      "ton\0ratelance\0"
    ;; subdomain          "ratelance"
    ;; subdomain_sfx      ""
    
    ;; we want the resolve result to point at contract of 'ratelance.ton', not its owner
    ;; so we must answer that resolution is complete + "wallet"H is address of 'ratelance.ton' contract
    
    ;; dns_smc_address#9fd3 smc_addr:MsgAddressInt flags:(## 8) { flags <= 1 } cap_list:flags . 0?SmcCapList = DNSRecord;
    ;; _ (HashmapE 256 ^DNSRecord) = DNS_RecordSet;
    
    cell wallet_record = begin_cell().store_uint(0x9fd3, 16).store_builder(domain_nft_address).store_uint(0, 8).end_cell();
    
    if (category == 0) {
      cell dns_dict = new_dict();
      dns_dict~udict_set_ref(256, "wallet"H, wallet_record);
      return (subdomain_bits, dns_dict);
    } elseif (category == "wallet"H) {
      return (subdomain_bits, wallet_record);
    } else {
      return (subdomain_bits, null());
    }
  } else {
    ;; example of domain being resolved:
    ;; [initial, not accessible in this contract] "ton\0resolve-contract\0ton\0resolve-contract\0ton\0ratelance\0"
    ;; [what is accessible by this contract]      "ton\0resolve-contract\0ton\0ratelance\0"
    ;; subdomain          "resolve-contract"
    ;; subdomain_sfx      "ton\0ratelance\0"
    ;; and we want to pass \0 further, so that next resolver has opportunity to process only one byte
    
    ;; next resolver is contract of 'resolve-contract<.ton>'
    ;; dns_next_resolver#ba93 resolver:MsgAddressInt = DNSRecord;
    cell resolver_record = begin_cell().store_uint(0xba93, 16).store_builder(domain_nft_address).end_cell();
    return (subdomain_bits - slice_bits(subdomain_sfx) - 8, resolver_record);
  }
}

() recv_internal() {
  return ();
}
```

</details>
