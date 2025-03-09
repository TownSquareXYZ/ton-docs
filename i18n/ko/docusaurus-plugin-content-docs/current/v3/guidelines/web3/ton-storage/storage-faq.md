# TON 스토리지 FAQ

## TON Storage 파일 가방에 TON 도메인을 할당하는 방법

1. 파일 가방을 네트워크에 [업로드](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files)하고 Bag ID를 받습니다

2. 컴퓨터에서 Google Chrome 브라우저를 엽니다.

3. Google Chrome용 [TON 확장 프로그램](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd)을 설치합니다.
   [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc)도 사용할 수 있습니다.

4. 확장 프로그램을 열고 "Import wallet"을 클릭한 다음 복구 구문을 사용하여 도메인을 소유한 지갑을 가져옵니다.

5. 이제 https://dns.ton.org 에서 도메인을 열고 "Edit"을 클릭합니다.

6. "Storage" 필드에 Bag ID를 복사하고 "Save"를 클릭합니다.

## TON Storage에서 정적 TON 사이트를 호스팅하는 방법

1. 웹사이트 파일이 있는 폴더에서 Bag을 [생성](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files)하고, 네트워크에 업로드한 다음 Bag ID를 받습니다. 폴더에는 `index.html` 파일이 포함되어 있어야 합니다.

2. 컴퓨터에서 Google Chrome 브라우저를 엽니다.

3. Google Chrome용 [TON 확장 프로그램](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd)을 설치합니다.
   [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc)도 사용할 수 있습니다.

4. 확장 프로그램을 열고 "Import wallet"을 클릭한 다음 복구 구문을 사용하여 도메인을 소유한 지갑을 가져옵니다.

5. 이제 https://dns.ton.org 에서 도메인을 열고 "Edit"을 클릭합니다.

6. "Site" 필드에 Bag ID를 복사하고, "Host in TON Storage" 체크박스를 선택한 다음 "Save"를 클릭합니다.

## TON NFT 콘텐츠를 TON Storage로 마이그레이션하는 방법

컬렉션에 [표준 NFT 스마트 컨트랙트](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-collection-editable.fc)를 사용한 경우, 새로운 URL 접두사와 함께 컬렉션 소유자의 지갑에서 컬렉션 스마트 컨트랙트로 [메시지](https://github.com/ton-blockchain/token-contract/blob/2d411595a4f25fba43997a2e140a203c140c728a/nft/nft-collection-editable.fc#L132)를 보내야 합니다.

예를 들어, URL 접두사가 `https://mysite/my_collection/`였다면, 새로운 접두사는 `tonstorage://my_bag_id/`가 됩니다.

## TON Storage 가방에 TON 도메인을 할당하는 방법 (로우 레벨)

TON 도메인의 sha256("storage") DNS 레코드에 다음 값을 할당해야 합니다:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

## TON Storage에서 정적 TON 사이트를 호스팅하는 방법 (로우 레벨)

웹사이트 파일이 있는 폴더에서 Bag을 [생성](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files)하고, 네트워크에 업로드한 다음 Bag ID를 받습니다. 폴더에는 `index.html` 파일이 포함되어 있어야 합니다.

TON 도메인의 sha256("site") DNS 레코드에 다음 값을 할당해야 합니다:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

