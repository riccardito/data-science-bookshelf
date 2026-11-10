# 27 · Deep Learning on Images & Signals

*Shelf VII · Deep Learning · FHNW modules: dlbs, bver, bverI, gbsv*

## Why it matters

Most of the world's paperwork still arrives as a picture: a scanned form, a photographed receipt, a
bill held up to a phone. Reading it reliably is a chain of small, separate problems -- correct the
geometry, find the code, read the text, check what was read -- and each link can be solved with a
classical method or a learned one. Knowing which, and measuring the difference, is the skill.

The whole book works on one kind of image: the Swiss QR bill, invented so that no real account
appears anywhere, and photographed at five qualities from a flat scan to an unreadable snapshot.

## Chapters

Read in order: each chapter builds on the one before it.

1. [Images as arrays](01-images-as-arrays.ipynb) — shape and channels, colour to grey, resizing without aliasing, what JPEG costs (PSNR)
2. [Classical image processing](02-classical-image-processing.ipynb) — convolution by hand, blur and sharpen, edges, adaptive thresholds, morphology
3. [Geometry and distortion](03-geometry-and-distortion.ipynb) — affine maps, the homography, measuring blur, the five photo qualities
4. [Detection](04-detection.ipynb) — finder patterns from contours, QR decoding per quality, where preprocessing stops helping
5. [CNNs on images](05-cnns-on-images.ipynb) — a small CNN against one hand-made feature, the confusion matrix, when transfer learning pays
6. [OCR and documents](06-ocr-and-documents.ipynb) — detection and recognition, character error rate, check digits that verify and (sometimes) repair

## Challenge · [qr-bill-reader](challenge/)

**How many payment fields are read correctly from a photo of a QR bill, per photo quality?**

| Reader | readable photos (0-2) | far and blurred (3) | wrong, not empty (3) |
|---|---|---|---|
| QR code alone | 100 % | 0 % | 0 % |
| OCR + patterns and check digits | 87-93 % | 60 % | 24 % |
| **combined: QR, else Claude, check digits enforced** | **100 %** | **83 %** | **4 %** |

Tampered bills caught where the QR code decodes: 18 of 18, no false alarm. [The notebook](challenge/qr-bill-reader.ipynb) ·
[the numbers](challenge/results.json).

## Key concepts

- Images as arrays; colour spaces; resampling and aliasing; compression and PSNR
- Convolution and kernels; Gaussian blur; unsharp masking; gradients and edges; Otsu and adaptive thresholds; morphology
- Affine maps and homographies; rectification; a focus measure
- Detection versus decoding; QR finder patterns; the resolution budget per module
- CNNs: learned kernels, pooling, a split by the unit that repeats; transfer learning and when to skip it
- OCR as detection plus recognition; character error rate; check digits (mod 97, mod 10 recursive)
- Structured extraction with a language model; recording its answers; wrong versus empty

## Tools

| Tool | Used for |
|---|---|
| `numpy`, `Pillow` | arrays, drawing, JPEG |
| `opencv-python-headless` | filters, warps, contours, the QR detector |
| `torch` | the CNN |
| `rapidocr-onnxruntime` | OCR, with the models in the wheel |
| `qrbill`, `qrcode` | the Swiss QR payload and its code |
| `anthropic` | the structured extraction, recorded once and replayed |
| `ds_toolbox` | `qrbills` (bills, distortion, decoding, check digits, rules), `llm` (the recorder) |

## Where it was learned

FHNW `dlbs` (deep learning for images and signals), `bver` / `bverI` (image processing), `gbsv`
(signal processing). The book itself was written in November 2026.
