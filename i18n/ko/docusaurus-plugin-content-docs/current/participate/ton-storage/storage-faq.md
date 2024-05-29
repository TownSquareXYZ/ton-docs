# TON 스토리지 FAQ

## TON 스토리지 파일 백에 TON 도메인을 할당하는 방법

1. [업로드](/참여/톤-스토리지/스토리지-데몬#파일 가방 만들기)를 통해 파일 가방을 네트워크에 업로드하고 가방 ID를 받습니다.

2. 컴퓨터에서 Google Chrome 브라우저를 엽니다.

3. 구글 크롬용 [TON 확장 프로그램](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd)을 설치합니다.
   마이톤월렛](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc)을 사용할 수도 있습니다.

4. 확장 프로그램을 열고 "지갑 가져오기"를 클릭한 다음 복구 문구를 사용하여 도메인을 소유한 지갑을 가져옵니다.

5. 이제 https://dns.ton.org 에서 도메인을 열고 "편집"을 클릭합니다.

6. 가방 ID를 '저장소' 필드에 복사하고 '저장'을 클릭합니다.

## TON 스토리지에서 정적 TON 사이트를 호스팅하는 방법

1. 웹사이트 파일이 있는 폴더에서 백을 [생성](/참여/톤-스토리지/스토리지-데몬#파일-백 생성)하고 네트워크에 업로드한 후 백 ID를 받습니다. 폴더에는 `index.html` 파일이 포함되어 있어야 합니다.

2. 컴퓨터에서 Google Chrome 브라우저를 엽니다.

3. 구글 크롬용 [TON 확장 프로그램](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd)을 설치합니다.
   마이톤월렛](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc)을 사용할 수도 있습니다.

4. 확장 프로그램을 열고 "지갑 가져오기"를 클릭한 다음 복구 문구를 사용하여 도메인을 소유한 지갑을 가져옵니다.

5. 이제 https://dns.ton.org 에서 도메인을 열고 "편집"을 클릭합니다.

6. 백 ID를 '사이트' 필드에 복사하고 '호스트가 톤 스토리지에 있음' 확인란을 선택한 후 '저장'을 클릭합니다.

## TON NFT 콘텐츠를 TON 스토리지로 마이그레이션하는 방법

컬렉션에 [표준 NFT 스마트 컨트랙트](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-collection-editable.fc)를 사용했다면, 컬렉션 소유자의 지갑에서 컬렉션 스마트 컨트랙트에 새 URL 접두사를 붙여 [메시지](https://github.com/ton-blockchain/token-contract/blob/2d411595a4f25fba43997a2e140a203c140c728a/nft/nft-collection-editable.fc#L132)를 보내야 합니다.

예를 들어, 이전에 URL 접두사가 `https://mysite/my_collection/`이었던 경우 새 접두사는 `tonstorage://my_bag_id/`가 됩니다.

## TON 스토리지 백에 TON 도메인을 할당하는 방법(로우 레벨)

TON 도메인의 sha256("저장소") DNS 레코드에 다음 값을 할당해야 합니다:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

## TON 스토리지에서 정적 TON 사이트를 호스팅하는 방법(로우레벨)

웹사이트 파일이 있는 폴더에서 백을 [생성](/참여/톤-스토리지/스토리지-데몬#파일-백 생성)하고 네트워크에 업로드한 후 백 ID를 받습니다. 폴더에는 `index.html` 파일이 포함되어 있어야 합니다.

TON 도메인의 sha256("사이트") DNS 레코드에 다음 값을 할당해야 합니다:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```
