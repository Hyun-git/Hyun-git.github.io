---
layout: post
title: PNG 압축, quality를 낮춰도 크기가 안 줄었던 이유
date: 2026-05-18T16:12:00.000+09:00
---

## 배경

Arkain Console에 이미지 첨부 기능을 추가하면서 문제가 생겼다.

사용자가 스냅샷 이미지를 LLM에 함께 전달하는 기능이었는데, LLM API가 5MB를 초과하는 이미지에 에러를 반환했다. 파일 선택 시 허용 최대 크기는 50MB였기 때문에, 업로드 전에 자동으로 압축하는 유틸(compressImage)을 만들기로 했다.

---

## 처음 만든 로직

Canvas API를 써서 2단계로 압축했다.

1. quality를 0.85 → 0.35 순으로 낮춰가며 5MB 이하가 되면 멈춤
2. 그래도 부족하면 해상도를 `sqrt(maxBytes / blob.size)` 비율로 줄인 뒤 quality 0.3으로 재압축

왜 `sqrt`를 쓰냐면, 이미지 파일 크기는 픽셀 수, 즉 면적에 비례하기 때문이다. 면적 = 가로 × 세로이므로, 파일 크기를 절반으로 줄이려면 가로/세로 각각을 `sqrt(0.5)` 배 해야 한다.

로직 자체는 단순했다. 그런데 문제가 생겼다.

---

## 32MB PNG가 5.4MB로 올라갔다

목표는 5MB 이하인데 5.4MB로 S3에 올라갔다.

처음엔 계산 실수를 의심했다. 그런데 알고 보니 원인은 다른 데 있었다.

> `canvas.toBlob(callback, 'image/png', quality)`에서 PNG는 quality 파라미터를 무시한다.

PNG는 **무손실(lossless)** 포맷이라 quality 개념 자체가 없다. JPEG나 WebP는 quality로 손실 압축 강도를 조절할 수 있지만, PNG는 해상도를 줄이지 않는 한 canvas로 다시 그려도 파일 크기가 거의 변하지 않는다.

```js
// JPEG/WebP는 quality가 효과 있지만
canvas.toBlob(resolve, 'image/jpeg', 0.3); // ✅ 압축됨

// PNG는 quality 파라미터 무시
canvas.toBlob(resolve, 'image/png', 0.3);  // ❌ 해상도만 반영됨
```

그러니까 1단계에서 quality를 0.85부터 0.35까지 6번 시도했지만, PNG는 blob 크기가 그대로였다. 2단계에서 해상도를 한 번 줄이긴 했지만, `sqrt(maxBytes / blob.size)` 계산이 정확하지 않아 5.4MB로 살짝 넘겼다.

---

## 해결

WebP로 변환하면 간단하겠지만, 확장자를 유지해야 해서 제외했다.

대신 2단계를 while 루프로 바꿔, 5MB 이하가 될 때까지 해상도를 반복 축소하도록 수정했다.

```js
// 변경 전: 한 번만 시도
if (blob && blob.size > maxBytes) {
    const scale = Math.sqrt(maxBytes / blob.size);
    // ...한 번 줄이고 끝
}

// 변경 후: 5MB 이하가 될 때까지 반복
while (blob && blob.size > maxBytes && width > 1 && height > 1) {
    const scale = Math.sqrt(maxBytes / blob.size) * 0.9; // 10% 여유
    width = Math.max(1, Math.round(width * scale));
    height = Math.max(1, Math.round(height * scale));
    const canvas = drawToCanvas(bitmap, width, height);
    blob = await toBlob(canvas, file.type, 0.3);
}
```

`0.9` 여유 계수를 둔 이유가 있다. PNG 압축 결과는 픽셀 내용에 따라 예측하기 어렵다. 계산대로 줄였는데도 목표를 살짝 넘기는 경우가 있어서, 매 반복마다 약간 더 공격적으로 줄이도록 했다. 32MB PNG 기준으로 보통 1~2회 반복으로 해결된다.

---

## 정리

```
┌──────┬──────────────┬──────────────────────────────┐
│ 포맷 │ quality 효과 │       크기 줄이는 방법       │
├──────┼──────────────┼──────────────────────────────┤
│ JPEG │ ✅ 있음      │ quality 낮추기 + 해상도 축소 │
├──────┼──────────────┼──────────────────────────────┤
│ WebP │ ✅ 있음      │ quality 낮추기 + 해상도 축소 │
├──────┼──────────────┼──────────────────────────────┤
│ PNG  │ ❌ 없음      │ 해상도 축소만 가능           │
└──────┴──────────────┴──────────────────────────────┘
```

브라우저 Canvas API로 PNG를 압축할 때, quality 파라미터는 아무런 의미가 없다.

크기를 줄이려면 해상도를 줄이는 것만이 방법이고, 목표 크기를 보장하려면 반복 루프가 필요하다.
