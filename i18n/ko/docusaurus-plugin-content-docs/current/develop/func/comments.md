# 댓글

FunC에는 `;;`(이중 `;`)로 시작하는 한 줄 주석이 있습니다. 예를 들어

```func
int x = 1; ;; assign 1 to x
```

또한 `{-`로 시작하고 `-}`로 끝나는 여러 줄 주석도 있습니다. 다른 많은 언어와 달리 FunC의 여러 줄 주석은 중첩할 수 있다는 점에 유의하세요. 예를 들어

```func
{- This is a multi-line comment
    {- this is a comment in the comment -}
-}
```

또한 여러 줄짜리 주석 안에 한 줄짜리 주석이 있을 수 있으며, 한 줄짜리 주석 `;;`은 여러 줄짜리 `{- -}`보다 "더 강력"합니다. 즉, 다음 예시에서는

```func
{-
  Start of the comment

;; this comment ending is itself commented -> -}

const a = 10;
;; this comment begining is itself commented -> {-

  End of the comment
-}
```

`const a = 10;`는 여러 줄 주석 안에 있으며 주석 처리됩니다.
