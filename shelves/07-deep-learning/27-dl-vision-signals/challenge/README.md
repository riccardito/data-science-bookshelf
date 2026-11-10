# Challenge · qr-bill-reader

**A photo of a Swiss QR bill arrives. How many of its five payment fields are read correctly, as the
photo gets worse -- and is a bill whose print disagrees with its QR code caught?**

Fields read correctly (IBAN, amount, reference, creditor name, creditor city), 30 bills per quality:

| Reader | 0 · flat scan | 1 · good photo | 2 · handheld | 3 · far and blurred | 4 · unreadable |
|---|---|---|---|---|---|
| QR code alone | 100 % | 100 % | 100 % | 0 % | 0 % |
| OCR + patterns and check digits | 93 % | 93 % | 87 % | 60 % | 0 % |
| OCR + Claude | 100 % | 100 % | 100 % | 83 % | 0 % |
| **combined: QR, else Claude, check digits enforced** | **100 %** | **100 %** | **100 %** | **83 %** | 0 % |

Fields filled in **but wrong** -- the error that sends money to the wrong place:

| Reader | 0-2 | 3 · far and blurred | 4 · unreadable |
|---|---|---|---|
| OCR + patterns and check digits | 7-13 % | 24 % | 6 % |
| OCR + Claude | 0 % | 6 % | 5 % |
| combined, check digits enforced | 0 % | 4 % | 5 % |

**Tampered bills** (6 of 30: printed amount or IBAN differs from the QR code), checked wherever the
QR code decodes: 18 of 18 tampered images caught and 0 of 72 honest ones flagged -- by the rules and
by Claude alike.

- **Data:** 30 invented bills -- valid QR-IBANs and QR references, no real account, person or
  company -- drawn in the payment-part layout and photographed at five qualities (`ds_toolbox.qrbills`).
- **Readers:** OpenCV's QR detector after sharpening; RapidOCR (PP-OCRv4 via ONNX); Claude Opus 5.5
  at effort `low` with a JSON schema, told to repair a digit only where a check digit allows it.
- **What it says:** the QR code is enough on a readable photo; the printed text is the only way in on
  a blurred one, where Claude reads names and places the rules cannot. On an unreadable photo Claude
  still filled in a few amounts -- a guess a check digit cannot catch -- so a reader should answer
  "unreadable" there, which [chapter 5](../05-cnns-on-images.ipynb)'s quality check makes possible.

## Run it

```
make install
jupyter nbconvert --to notebook --execute qr-bill-reader.ipynb
```

Offline, no key: the OCR results and the 135 Claude answers are recorded in [`recordings/`](recordings/)
and replayed (about 20 s). `BOOKSHELF_LIVE=ocr` re-runs the OCR; `BOOKSHELF_LIVE=all` also asks Claude
for anything not yet recorded (needs `pip install -e ".[llm]"` and a key -- the recorded run cost
about $1.70). The numbers go to [`results.json`](results.json).
