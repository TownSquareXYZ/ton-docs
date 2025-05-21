# مفسرهای TON DNS

## معرفی

TON DNS یک ابزار قدرتمند است. این اجازه می‌دهد تا سایت‌ها/فضاهای ذخیره‌سازی TON به دامنه‌ها اختصاص یابند و همچنین تنظیم مفسر زیر دامنه‌ها ممکن شود.

## لینک‌های مرتبط

1. [مستندات آدرس‌های قرارداد هوشمند](/v3/documentation/smart-contracts/addresses)
2. [TEP-0081 - استاندارد TON DNS](https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md)
3. [سورس کد کلکسیون دامنه .ton](https://tonscan.org/address/EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz#source)
4. [سورس کد کلکسیون دامنه .t.me](https://tonscan.org/address/EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi#source)
5. [جستجوگر قراردادهای دامنه](https://tonscan.org/address/EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH_Zp#source)
6. [کد مدیریت ساده زیر دامنه](https://github.com/Gusarich/simple-subdomain/blob/198485bbc9f7f6632165b7ab943902d4e125d81a/contracts/subdomain-manager.fc)

## جستجوگر قراردادهای دامنه

زیر دامنه‌ها کاربرد عملی دارند. برای مثال، کاوشگرهای بلاک‌چین در حال حاضر راهی برای پیدا کردن قرارداد دامنه با نام آن ارائه نمی‌دهند. بیایید بررسی کنیم که چگونه می‌توان قراردادی ایجاد کرد که فرصتی برای یافتن چنین دامنه‌هایی بدهد.

:::info
This contract is deployed at [EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH\_Zp](https://tonscan.org/address/EQDkAbAZNb4uk-6pzTPDO2s0tXZweN-2R08T2Wy6Z3qzH_Zp#source) and linked to `resolve-contract.ton`. To test it, you may write `<your-domain.ton>.resolve-contract.ton` in the address bar of your favourite TON explorer and get to the page of TON DNS domain contract. Subdomains and .t.me domains are supported as well.

شما می‌توانید برای مشاهده کد مفسر با رفتن به `resolve-contract.ton.resolve-contract.ton` تلاش کنید. متاسفانه، این به شما مفسر فرعی را نشان نمی‌دهد (آن یک قرارداد هوشمند متفاوت است)، بلکه صفحه قرارداد دامنه را می‌بینید.
:::

### کد dnsresolve()

برخی از قسمت‌های تکراری حذف شده‌اند.

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
  ;; supported subdomains are "ton\\0", "me\\0t\\0" and "address\\0"
  
  slice subdomain_sfx = null();
  builder domain_nft_address = null();
  
  if (subdomain.starts_with("746F6E00"s)) {
    ;; we're resolving
    ;; "ton" \\0 <subdomain> \\0 [subdomain_sfx]
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
    ;; [initial, not accessible in this contract] "ton\\0resolve-contract\\0ton\\0ratelance\\0"
    ;; [what is accessible by this contract]      "ton\\0ratelance\\0"
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
    ;; subdomain_sfx      "ton\\0ratelance\\0"
    ;; we want to pass \\0 further, so that next resolver has opportunity to process only one byte
    
    ;; next resolver is contract of 'resolve-contract<.ton>'
    ;; dns_next_resolver#ba93 resolver:MsgAddressInt = DNSRecord;
    cell resolver_record = begin_cell().store_uint(0xba93, 16).store_builder(domain_nft_address).end_cell();
    return (subdomain_bits - slice_bits(subdomain_sfx) - 8, resolver_record);
  }
}
```

### توضیح dnsresolve()

- کاربر `"stabletimer.ton.resolve-contract.ton"` درخواست می‌کند.
- برنامه آن را به `"\0ton\0resolve-contract\0ton\0stabletimer\0"` (اولین بایت صفر اختیاری است) تبدیل می‌کند.
- مفسر DNS ریشه درخواست را به کلکسیون TON DNS هدایت می‌کند، قسمت باقی‌مانده `"\0resolve-contract\0ton\0stabletimer\0"` است.
- کلکسیون TON DNS درخواست را به دامنه خاصی ارجاع می‌دهد، `"\0ton\0stabletimer\0"` باقی می‌ماند.
- قرارداد دامنه DNS .TON فرایند تفسیر را به مفسر فرعی مشخص شده توسط ویرایشگر منتقل می‌کند، زیردامنه `"ton\0stabletimer\0"` می‌باشد.

**این نقطه‌ای است که dnsresolve() فراخوانی می‌شود.** توضیح گام به گام نحوه عملکرد آن:

1. زیر دامنه و دسته را به عنوان ورودی می‌گیرد.
2. اگر در ابتدا بایت صفر وجود داشته باشد، نادیده گرفته می‌شود.
3. بررسی می‌کند که آیا زیر دامنه با `"ton\0"` شروع می‌شود. اگر چنین است،
  1. اولین ۳۲ بیت را نادیده می‌گیرد (زیر دامنه = `"resolve-contract\0"`)
  2. مقدار `subdomain_sfx` به `subdomain` تنظیم می‌شود و تابع بایت‌ها را تا بایت صفر می‌خواند
  3. (subdomain = `"resolve-contract\0"`, subdomain_sfx = `""`)
  4. بایت صفر و subdomain_sfx از انتهای قطعه زیر دامنه برش داده می‌شوند (subdomain = `"resolve-contract"`)
  5. توابع slice_hash و get_ton_dns_nft_address_by_index برای تبدیل نام دامنه به آدرس قرارداد استفاده می‌شوند. می‌توانید آن‌ها را در [[Subresolvers#Appendix 1. Code of resolve-contract.ton | Appendix ۱]] ببینید.
4. در غیر این صورت، dnsresolve() بررسی می‌کند که آیا زیر دامنه با `"address\0"` شروع می‌شود. اگر چنین است، آن پیشوند را نادیده می‌گیرد و آدرس base64 را می‌خواند.
5. اگر زیر دامنه ارائه شده برای حل با هیچ یک از این پیشوندها مطابقت نداشته باشد، تابع با بازگشت `(۰, null())` (پیشوند بایت صفر حل شده بدون هیچ مدخل DNS) شکست را نشان می‌دهد.
6. سپس بررسی می‌کند که آیا پسوند زیر دامنه خالی است یا نه. پسوند خالی به این معنی است که درخواست به طور کامل برآورده شده است. اگر پسوند خالی باشد:
  1. dnsresolve() یک رکورد DNS برای بخش "کیف پول" دامنه ایجاد می‌کند، با استفاده از آدرس قرارداد دامنه TON که بازیابی کرده است.
  2. اگر دسته ۰ (تمام مدخل‌های DNS) درخواست شود، رکورد در یک دیکشنری پیچیده شده و برگردانده می‌شود.
  3. اگر دسته "کیف پول"H درخواست شود، رکورد به همان صورت برگردانده می‌شود.
  4. در غیر این صورت، برای دسته مشخص شده هیچ مدخل DNS وجود ندارد، بنابراین تابع نشان می‌دهد که تفسیر با موفقیت انجام شده اما هیچ نتیجه‌ای پیدا نشده است.
7. اگر پسوند خالی نباشد:
  1. آدرسی که قبلاً دریافت شده است به عنوان مفسر بعدی استفاده می‌شود. تابع رکورد مفسر بعدی را که به آن اشاره می‌کند ایجاد می‌کند.
  2. `"\0ton\0stabletimer\0"` مجدد به آن قرارداد ارسال می‌شود: بیت‌های پردازش شده، بیت‌های زیر دامنه هستند.

به طور خلاصه، dnsresolve() یا:

- زیر دامنه را به طور کامل به یک رکورد DNS تفسیر می‌کند
- تا حدی آن را به یک رکورد مفسر تبدیل می‌کند تا تفسیر را به یک قرارداد دیگر منتقل کند
- برای زیر دامنه‌هایی که ناشناخته‌اند، نتیجه «دامنه پیدا نشد» را بازمی‌گرداند

:::warning
در واقع تجزیه base64 آدرس‌ها کار نمی‌کند: اگر سعی کنید `<some-address>.address.resolve-contract.ton` را وارد کنید، یک خطا خواهید گرفت که نشان می‌دهد دامنه نادرست پیکربندی شده است یا وجود ندارد. بدلیل اینکه نام‌های دامنه به حروف کوچک و بزرگ حساس نیستند (ویژگی‌ای که از DNS واقعی به ارث رسیده) و بنابراین به حروف کوچک تبدیل می‌شوند، شما را به آدرس زنجیره کاری غیر موجود هدایت می‌کند.
:::

### اتصال مفسر

حالا که قرارداد مفسر فرعی پیاده‌سازی شده است، باید دامنه را به آن متصل کنیم، یعنی رکورد `dns_next_resolver` دامنه را تغییر دهیم. می‌توانیم این کار را با ارسال یک پیام با ساختار TL-B زیر به قرارداد دامنه انجام دهیم.

1. `change_dns_record#4eb1f0f9 query_id:uint64 record_key#19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff record:^[dns_next_resolver#ba93 resolver:MsgAddressInt]`

## ایجاد مدیر زیر دامنه‌های خود

زیر دامنه‌ها می‌توانند برای کاربران عادی مفید باشند - به عنوان مثال، پیوند دادن چندین پروژه به یک دامنه، یا پیوند به کیف پول‌های دوستان.

### داده‌های قرارداد

ما نیاز داریم که آدرس مالک و دیکشنری *دامنه*->*هش رکورد*->*مقدار رکورد* را در داده‌های قرارداد ذخیره کنیم.

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

### پردازش به‌روزرسانی رکوردها

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

ما بررسی می‌کنیم که پیام ورودی شامل درخواست باشد، برگردانده نشده باشد، از طرف مالک آمده باشد و درخواست `op::update_record` باشد.

سپس نام دامنه را از پیام بارگذاری می‌کنیم. نمی‌توانیم دامنه‌ها را به همان صورت در دیکشنری ذخیره کنیم: آنها ممکن است طول‌های متفاوتی داشته باشند، اما دیکشنری‌های بدون پیشوند TVM تنها می‌توانند حاوی کلیدهایی با طول یکسان باشند. بنابراین، `string_hash(domain)` را محاسبه می‌کنیم - هش SHA-256 از نام دامنه؛ نام دامنه تضمین شده است که دارای تعداد صحیح اُکتت باشد بنابراین کار می‌کند.

بعد از آن، رکورد برای دامنه مشخص شده را به‌روزرسانی می‌کنیم و داده‌های جدید را به ذخیره‌ساز قرارداد می‌سپاریم.

### تفسیر دامنه‌ها

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

تابع `dnsresolve` بررسی می‌کند که آیا زیر دامنه درخواست شده شامل تعداد صحیحی از اُکتت‌ها است، صفر بایت اختیاری در ابتدای برش زیر دامنه را عبور می‌کند، سپس آن را به دامنه سطح بالاتر و چیزهای دیگر تقسیم می‌کند (`test\0qwerty\0` به `test` و `qwerty\0` تقسیم می‌شود). دیکشنری رکوردهای مربوط به دامنه درخواست شده بارگذاری می‌شود.

اگر پسوند زیر دامنه غیر خالی وجود داشته باشد، تابع تعداد بایت‌های تفسیر شده و رکورد بعدی مفسر که در کلید `"dns_next_resolver"H` یافت شده را برمی‌گرداند. در غیر این صورت، تابع تعداد بایت‌های تفسیر شده (یعنی طول کامل برش) و رکورد درخواست شده را برمی‌گرداند.

روشی برای بهبود این تابع با مدیریت خطاها به شکلی زیباتر وجود دارد، اما این کار به‌طور دقیقی لازم نیست.

## ضمیمه ۱. کد resolve-contract.ton

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
  ;; supported subdomains are "ton\\0", "me\\0t\\0" and "address\\0"
  
  slice subdomain_sfx = null();
  builder domain_nft_address = null();
  
  if (subdomain.starts_with("746F6E00"s)) {
    ;; we're resolving
    ;; "ton" \\0 <subdomain> \\0 [subdomain_sfx]
    subdomain~skip_bits(32);
    
    ;; reading domain name
    subdomain_sfx = subdomain;
    while (subdomain_sfx~load_uint(8)) { }
    
    subdomain~skip_last_bits(8 + slice_bits(subdomain_sfx));
    
    domain_nft_address = get_ton_dns_nft_address_by_index(slice_hash(subdomain));
  } elseif (subdomain.starts_with("6D65007400"s)) {
    ;; "t" \\0 "me" \\0 <subdomain> \\0 [subdomain_sfx]
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
    ;; [initial, not accessible in this contract] "ton\\0resolve-contract\\0ton\\0ratelance\\0"
    ;; [what is accessible by this contract]      "ton\\0ratelance\\0"
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
    ;; [initial, not accessible in this contract] "ton\\0resolve-contract\\0ton\\0resolve-contract\\0ton\\0ratelance\\0"
    ;; [what is accessible by this contract]      "ton\\0resolve-contract\\0ton\\0ratelance\\0"
    ;; subdomain          "resolve-contract"
    ;; subdomain_sfx      "ton\\0ratelance\\0"
    ;; and we want to pass \\0 further, so that next resolver has opportunity to process only one byte
    
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
