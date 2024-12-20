# 주석

FunC는 `;;`(이중 `;`)로 시작하는 한 줄 주석을 가집니다. 예시:

```func
int x = 1; ;; assign 1 to x
```

또한 `{-`로 시작하고 `-}`로 끝나는 여러 줄 주석도 있습니다. 다른 많은 언어와 달리 FunC의 여러 줄 주석은 중첩될 수 있습니다. 예시:

```func
{- This is a multi-line comment
    {- this is a comment in the comment -}
-}
```

게다가 여러 줄 주석 안에 한 줄 주석이 있을 수 있으며, 한 줄 주석 `;;`는 여러 줄 주석 `{- -}`보다 "우선순위가 높습니다". 다시 말해 다음 예시에서:

```func
{-
  Start of the comment

;; this comment ending is itself commented -> -}

const a = 10;
;; this comment begining is itself commented -> {-

  End of the comment
-}
```

`const a = 10;`은 여러 줄 주석 안에 있으므로 주석 처리됩니다.
