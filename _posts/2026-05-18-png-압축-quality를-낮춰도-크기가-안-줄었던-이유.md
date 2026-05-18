---
layout: post
title: PNG 압축, quality를 낮춰도 크기가 안 줄었던 이유
date: 2026-05-18T16:12:00.000+09:00
---
## 배경

Arkain Console의 AI 프롬프트 기능에 이미지 첨부를 추가했다. 사용자가 스냅샷 이미지를 LLM에 함께 전달할 수 있는 기능인데, LLM API 쪽에서 5MB 초과 이미지에 대해 에러를 반환하는 제약이 있었다.

파일 선택 시 허용 최대 크기는 50MB로 설정해뒀기 때문에, 클라이언트에서 5MB를 초과하는 이미지를 업로드하면 업로드 전에 자동으로 압축해주는 로직을 작성했다.

---
## 문제

Canvas API를 이용한 압축 유틸(compressImage)을 만들었다. 로직은 단순했다.

1. 1단계: quality를 0.85 → 0.35 순으로 낮춰가며 5MB 이하가 되면 멈춤
2. 2단계: quality 조절로도 부족하면 해상도를 축소한 뒤 quality 0.3으로 재압축

그런데 32MB짜리 PNG 파일을 올렸을 때 S3에 5.4MB로 업로드되는 걸 발견했다. 목표는 5MB 이하인데 초과된 채로 올라간 것이다.

---
## 원인

canvas.toBlob(callback, type, quality)에서 PNG는 quality 파라미터를 무시한다.

PNG는 무손실(lossless) 포맷이기 때문에 quality 개념 자체가 없다. JPEG나 WebP는 quality로 손실 압축 강도를 조절할 수 있지만, PNG는 해상도를 줄이지 않는 한 canvas로 다시 그려도 파일 크기가 거의 변하지 않는다.

결국 1단계에서 quality를 0.85부터 0.35까지 6번 시도해도 PNG는 blob 크기가 그대로였고, 2단계에서 해상도를 sqrt(maxBytes / blob.size)로 한 번 줄인 뒤 quality 0.3으로 재압축해도 PNG는 quality를 무시하므로 해상도 축소 효과만 남았다. scale 계산이 정확하지 않아 5.4MB로 5MB를 살짝 넘긴 결과가 나온 것이다.

// JPEG/WebP는 quality가 효과 있지만
canvas.toBlob(resolve, 'image/jpeg', 0.3); // ✅ 압축됨

// PNG는 quality 파라미터 무시
canvas.toBlob(resolve, 'image/png', 0.3);  // ❌ 해상도만 반영됨

---
## 해결

확장자를 유지해야 했기 때문에 webp 변환은 선택지에서 제외했다. 대신 2단계를 while 루프로 바꿔 5MB 이하가 될 때까지 해상도를 반복 축소하도록 수정했다.

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

* 0.9 여유 계수를 둔 이유는 PNG 압축 결과가 픽셀 내용에 따라 예측하기 어렵기 때문이다. scale만큼 줄였는데도 목표를 살짝 넘기는 경우가 생길 수 있어, 매 반복마다 약간 더 공격적으로 줄이도록 했다. 32MB PNG 기준 보통 1~2회 반복으로 해결된다.

---
## 정리

┌──────┬──────────────┬──────────────────────────────┐
│ 포맷 │ quality 효과 │       크기 줄이는 방법       │
├──────┼──────────────┼──────────────────────────────┤
│ JPEG │ ✅ 있음      │ quality 낮추기 + 해상도 축소 │
├──────┼──────────────┼──────────────────────────────┤
│ WebP │ ✅ 있음      │ quality 낮추기 + 해상도 축소 │
├──────┼──────────────┼──────────────────────────────┤
│ PNG  │ ❌ 없음      │ 해상도 축소만 가능           │
└──────┴──────────────┴──────────────────────────────┘

브라우저 Canvas API로 이미지를 압축할 때 PNG를 다루는 경우, quality 파라미터는 아무런 의미가 없다. 크기를 줄이려면 해상도를 줄이는 것만이 방법이고, 목표 크기를 정확히 보장하려면 반복 루프가 필요하다.
