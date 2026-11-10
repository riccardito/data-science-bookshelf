"""Synthetic Swiss QR bills: generate, draw, photograph badly, decode, check.

Nothing here is a real bill. The generator invents creditors, debtors, QR-IBANs and QR
references that pass the same checks a bank applies (the IBAN's mod-97 digits, the reference's
mod-10 recursive digit), and ``qrbill`` builds the payload the Swiss standard prescribes. The
drawing follows the payment part's layout closely enough for detection and OCR to face the same
problems a scanned bill poses: a QR code with the Swiss cross in it, and short printed fields.

``distort`` turns a clean bill into a photo of five qualities, from a flat scan (0) to a small,
blurred, compressed snapshot (4) -- the axis every challenge result is reported along.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

import numpy as np

QUALITY_LEVELS = {0: "flat scan", 1: "good photo", 2: "handheld photo", 3: "far and blurred", 4: "unreadable"}
FIELDS = ("iban", "amount", "reference", "creditor_name", "creditor_city")

_COMPANIES = ["Muster AG", "Alpina Bau GmbH", "Seeblick Treuhand AG", "Bergquelle Getränke AG",
              "Rhein Elektro GmbH", "Jura Uhren AG", "Limmat Druck GmbH", "Säntis Holzbau AG",
              "Aare Reinigung GmbH", "Pilatus Software AG", "Rigi Gartenbau GmbH", "Lötschberg Transport AG"]
_PEOPLE = ["Anna Beispiel", "Luca Meier", "Sara Keller", "Noah Frei", "Mia Schmid", "Jonas Weber",
           "Lea Brunner", "Elias Huber", "Nina Baumann", "David Steiner", "Laura Fischer", "Tim Graf"]
_PLACES = [("8000", "Zürich"), ("3000", "Bern"), ("4051", "Basel"), ("6003", "Luzern"), ("9000", "St. Gallen"),
           ("1003", "Lausanne"), ("1201", "Genève"), ("6900", "Lugano"), ("7000", "Chur"), ("2502", "Biel/Bienne"),
           ("5000", "Aarau"), ("8400", "Winterthur")]


# -- check digits -------------------------------------------------------------------------------

def iban_valid(iban: str) -> bool:
    s = re.sub(r"\s", "", iban).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", s):
        return False
    digits = "".join(str(int(c, 36)) for c in s[4:] + s[:4])
    return int(digits) % 97 == 1


def make_iban(bank_id: str, account: str, country: str = "CH") -> str:
    """An IBAN with correct check digits for a Swiss bank id (5 digits) and account (12)."""
    body = f"{bank_id}{account}"
    digits = "".join(str(int(c, 36)) for c in body + country + "00")
    return f"{country}{98 - int(digits) % 97:02d}{body}"


_MOD10 = [0, 9, 4, 6, 8, 2, 7, 1, 3, 5]


def reference_check_digit(digits: str) -> int:
    carry = 0
    for d in digits:
        carry = _MOD10[(carry + int(d)) % 10]
    return (10 - carry) % 10


def reference_valid(ref: str) -> bool:
    s = re.sub(r"\s", "", ref)
    return bool(re.fullmatch(r"\d{27}", s)) and reference_check_digit(s[:-1]) == int(s[-1])


# -- the bill ---------------------------------------------------------------------------------

@dataclass(frozen=True)
class Bill:
    bill_id: str
    iban: str
    amount: str            # "1199.95"
    reference: str         # 27 digits
    creditor_name: str
    creditor_pcode: str
    creditor_city: str
    debtor_name: str
    debtor_pcode: str
    debtor_city: str

    @property
    def creditor_line(self) -> str:
        return f"{self.creditor_pcode} {self.creditor_city}"

    def fields(self) -> dict[str, str]:
        return {"iban": self.iban, "amount": self.amount, "reference": self.reference,
                "creditor_name": self.creditor_name, "creditor_city": self.creditor_city}

    def qr_payload(self) -> str:
        import qrbill

        bill = qrbill.QRBill(
            account=self.iban, amount=self.amount, reference_number=self.reference,
            creditor={"name": self.creditor_name, "pcode": self.creditor_pcode, "city": self.creditor_city,
                      "country": "CH"},
            debtor={"name": self.debtor_name, "pcode": self.debtor_pcode, "city": self.debtor_city,
                    "country": "CH"},
        )
        return bill.qr_data()

    def to_dict(self) -> dict:
        return asdict(self)


def generate_bills(n: int, seed: int = 0) -> list[Bill]:
    """``n`` invented bills, each with a QR-IBAN (bank id 30000-31999) and a QR reference."""
    rng = np.random.default_rng(seed)
    bills = []
    for k in range(n):
        iban = make_iban(str(rng.integers(30000, 32000)), "".join(map(str, rng.integers(0, 10, 12))))
        body = "".join(map(str, rng.integers(0, 10, 26)))
        reference = body + str(reference_check_digit(body))
        amount = f"{rng.choice([rng.uniform(8, 120), rng.uniform(120, 1500), rng.uniform(1500, 9800)]):.2f}"
        cp, cc = _PLACES[rng.integers(len(_PLACES))]
        dp, dc = _PLACES[rng.integers(len(_PLACES))]
        bills.append(Bill(f"bill-{k:03d}", iban, amount, reference, str(rng.choice(_COMPANIES)), cp, cc,
                          str(rng.choice(_PEOPLE)), dp, dc))
    return bills


def tamper(bill: Bill, rng: np.random.Generator) -> tuple[Bill, str]:
    """A copy whose PRINTED text differs from its QR code in one field -- amount or IBAN."""
    field = str(rng.choice(["amount", "iban"]))
    if field == "amount":
        value = f"{float(bill.amount) * rng.choice([1.1, 1.5, 2.0, 10.0]):.2f}"
    else:
        value = make_iban(str(rng.integers(30000, 32000)), "".join(map(str, rng.integers(0, 10, 12))))
    return Bill(**{**bill.to_dict(), field: value}), field


# -- formatting as printed --------------------------------------------------------------------

def format_iban(iban: str) -> str:
    return " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))


def format_reference(ref: str) -> str:
    return ref[:2] + " " + " ".join(ref[i:i + 5] for i in range(2, len(ref), 5))


def format_amount(amount: str) -> str:
    return f"{float(amount):,.2f}".replace(",", " ")


# -- drawing ----------------------------------------------------------------------------------

def _fonts():
    from matplotlib import font_manager
    from PIL import ImageFont

    regular = font_manager.findfont("DejaVu Sans")
    bold = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))
    return {"text": ImageFont.truetype(regular, 22), "head": ImageFont.truetype(bold, 20),
            "title": ImageFont.truetype(bold, 30)}


def render(bill: Bill, printed: Bill | None = None, dpi: int = 150) -> np.ndarray:
    """The payment part (148 x 105 mm) with the receipt strip beside it, as an RGB array.

    ``printed`` draws different text next to the QR code of ``bill`` -- a tampered bill.
    """
    import qrcode
    from PIL import Image, ImageDraw

    p = printed or bill
    mm = dpi / 25.4
    width, height = int(210 * mm), int(105 * mm)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    f = _fonts()
    draw.line([(int(62 * mm), 0), (int(62 * mm), height)], fill="black", width=1)
    draw.text((int(5 * mm), int(5 * mm)), "Receipt", font=f["title"], fill="black")
    draw.text((int(67 * mm), int(5 * mm)), "Payment part", font=f["title"], fill="black")

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(bill.qr_payload())
    qr.make(fit=True)
    side = int(46 * mm)
    code = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((side, side), Image.NEAREST)
    cross = ImageDraw.Draw(code)
    s, mid = int(7 * mm), side // 2
    arm, half = s // 5, int(s * 0.35)
    cross.rectangle([mid - s // 2, mid - s // 2, mid + s // 2, mid + s // 2], fill="black")
    cross.rectangle([mid - arm // 2, mid - half, mid + arm // 2, mid + half], fill="white")
    cross.rectangle([mid - half, mid - arm // 2, mid + half, mid + arm // 2], fill="white")
    img.paste(code, (int(67 * mm), int(17 * mm)))

    x, y = int(118 * mm), int(5 * mm)
    for title, lines in [("Account / Payable to", [format_iban(p.iban), p.creditor_name, p.creditor_line]),
                         ("Reference", [format_reference(p.reference)]),
                         ("Payable by", [p.debtor_name, f"{p.debtor_pcode} {p.debtor_city}"])]:
        draw.text((x, y), title, font=f["head"], fill="black")
        y += 28
        for line in lines:
            draw.text((x, y), line, font=f["text"], fill="black")
            y += 27
        y += 12
    draw.text((int(67 * mm), int(68 * mm)), "Currency", font=f["head"], fill="black")
    draw.text((int(85 * mm), int(68 * mm)), "Amount", font=f["head"], fill="black")
    draw.text((int(67 * mm), int(74 * mm)), "CHF", font=f["text"], fill="black")
    draw.text((int(85 * mm), int(74 * mm)), format_amount(p.amount), font=f["text"], fill="black")
    # the receipt strip repeats the essentials, small
    ry = int(17 * mm)
    for line in ["Account / Payable to", format_iban(p.iban), p.creditor_name, "", "Amount",
                 "CHF " + format_amount(p.amount)]:
        draw.text((int(5 * mm), ry), line, font=f["head"] if line in ("Amount", "Account / Payable to") else
                  f["text"], fill="black")
        ry += 27
    return np.array(img)


def distort(img: np.ndarray, level: int, seed: int = 0) -> np.ndarray:
    """A photo of ``img`` at quality ``level`` (0-4): rotation, perspective, uneven light, blur,
    noise, a smaller image and JPEG compression, each growing with the level."""
    import cv2

    if level not in QUALITY_LEVELS:
        raise ValueError(f"level must be one of {sorted(QUALITY_LEVELS)}")
    rng = np.random.default_rng(seed)
    h, w = img.shape[:2]
    out = img.copy()
    if level >= 1:
        rot = cv2.getRotationMatrix2D((w / 2, h / 2), rng.uniform(-3, 3) * level, 1)
        out = cv2.warpAffine(out, rot, (w, h), borderValue=(235, 235, 235))
    if level >= 2:
        j = 0.03 * level * min(w, h)
        src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        dst = (src + rng.uniform(-j, j, src.shape)).astype(np.float32)
        out = cv2.warpPerspective(out, cv2.getPerspectiveTransform(src, dst), (w, h), borderValue=(220, 220, 220))
        light = np.linspace(0.75, 1.05, w)[None, :, None]
        out = np.clip(out * light, 0, 255).astype(np.uint8)
    if level >= 1:
        out = cv2.GaussianBlur(out, (0, 0), [0, 1.0, 1.6, 2.4, 3.2][level])
        out = np.clip(out + rng.normal(0, 4 * level, out.shape), 0, 255).astype(np.uint8)
    if level >= 3:
        f = [1, 1, 1, 0.6, 0.45][level]
        out = cv2.resize(out, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    if level >= 2:
        ok, enc = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, [95, 95, 60, 40, 25][level]])
        out = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    return out


# -- reading the QR code ----------------------------------------------------------------------

def sharpen_for_qr(img: np.ndarray) -> np.ndarray:
    """Upscale, unsharp-mask and binarise: the preprocessing that rescues a soft QR code."""
    import cv2

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if img.ndim == 3 else img
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    soft = cv2.GaussianBlur(gray, (0, 0), 2)
    gray = cv2.addWeighted(gray, 1.8, soft, -0.8, 0)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 10)


def decode_qr(img: np.ndarray, preprocess: bool = True) -> str | None:
    """The QR payload, or None. Tries the image as it is, then sharpened."""
    import cv2

    detector = cv2.QRCodeDetectorAruco()
    candidates = [img] + ([sharpen_for_qr(img)] if preprocess else [])
    for candidate in candidates:
        data, _, _ = detector.detectAndDecode(candidate)
        if data:
            return data
    return None


def parse_payload(payload: str) -> dict[str, str] | None:
    """The fields of a Swiss QR payload (SPC / 0200), or None if it is not one."""
    lines = payload.replace("\r\n", "\n").split("\n")
    if len(lines) < 31 or lines[0] != "SPC" or lines[1] != "0200":
        return None
    return {"iban": lines[3], "creditor_name": lines[5], "creditor_city": lines[9],
            "amount": lines[18], "reference": lines[28]}


# -- reading the printed text -----------------------------------------------------------------

_ocr_engine = None


def ocr_lines(img: np.ndarray) -> list[list]:
    """RapidOCR's text lines as ``[text, x, y]`` -- the centre of each line's box as a fraction of the
    image's width and height -- top to bottom, then left to right. The models ship inside the wheel."""
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr_engine = RapidOCR()
    result, _ = _ocr_engine(img)
    h, w = img.shape[:2]
    rows = []
    for box, text, _conf in result or []:
        xs, ys = [p[0] for p in box], [p[1] for p in box]
        rows.append([text, round((min(xs) + max(xs)) / 2 / w, 3), round((min(ys) + max(ys)) / 2 / h, 3)])
    return sorted(rows, key=lambda r: (round(r[2] * 50), r[1]))


def line_texts(lines) -> list[str]:
    """Just the text, for lines with or without positions."""
    return [ln[0] if isinstance(ln, list | tuple) else ln for ln in lines]


# digits OCR confuses -- SYMMETRIC: if a 6 can be read as an 8, an 8 must be tried as a 6. A one-way
# table leaves the true digit out of the candidates, and a wrong IBAN can then pass the check by
# chance (measured in chapter 6 of book 27: 2.4 % wrong repairs one-way, 0.0 % symmetric).
_PAIRS = [("0", "8"), ("1", "7"), ("5", "6"), ("3", "8"), ("6", "8"), ("0", "6"), ("4", "9"), ("2", "7")]
CONFUSIONS: dict[str, str] = {}
for _a, _b in _PAIRS:
    CONFUSIONS[_a] = "".join(sorted(set(CONFUSIONS.get(_a, "")) | {_b}))
    CONFUSIONS[_b] = "".join(sorted(set(CONFUSIONS.get(_b, "")) | {_a}))


def repair(value: str, valid) -> str:
    """``value`` if it passes ``valid``; else the one-character confusion that does; else ``value``."""
    if valid(value):
        return value
    fixes = []
    for i, c in enumerate(value):
        for alt in CONFUSIONS.get(c, ""):
            cand = value[:i] + alt + value[i + 1:]
            if valid(cand):
                fixes.append(cand)
    return fixes[0] if len(fixes) == 1 else value


_IBAN = re.compile(r"CH\d{2}[0-9A-Z]{17}")
_AMOUNT = re.compile(r"(?<![\d.])(\d{1,3}(?:[ ']\d{3})*|\d+)\.(\d{2})(?!\d)")


def extract_by_rules(lines: list[str]) -> dict[str, str | None]:
    """The five fields read from OCR lines with patterns and check digits -- no model.

    With positions (``ocr_lines``), the receipt strip on the left (the first 62 of 210 mm) is
    ignored: it repeats the IBAN and the name and interleaves with the payment part's lines.
    """
    if lines and isinstance(lines[0], list | tuple):
        lines = [ln[0] for ln in lines if ln[1] > 0.27]
    compact = [re.sub(r"\s", "", ln) for ln in lines]
    out: dict[str, str | None] = dict.fromkeys(FIELDS)
    iban_at = None
    for i, c in enumerate(compact):
        m = _IBAN.search(c.upper().replace("O", "0"))
        if m:
            out["iban"] = repair(m.group(0), iban_valid)
            iban_at = i
            break
    for c in compact:
        digits = re.sub(r"\D", "", c)
        if len(digits) == 27:          # a QR reference is the only 27-digit run on the bill
            out["reference"] = repair(digits, reference_valid)
            break
    amounts = [f"{int(m.group(1).replace(' ', '').replace(chr(39), ''))}.{m.group(2)}"
               for ln in lines for m in _AMOUNT.finditer(ln)]
    if amounts:
        out["amount"] = max(set(amounts), key=amounts.count)
    if iban_at is not None:
        # the receipt strip repeats the IBAN and the name beside the payment part, so OCR often
        # returns each twice in a row: skip IBAN-like lines, then skip repeats of the name
        after = [ln.strip() for ln in lines[iban_at + 1:]]
        after = [ln for ln in after if not _IBAN.search(re.sub(r"\s", "", ln).upper().replace("O", "0"))]
        if after:
            name = after[0]
            out["creditor_name"] = name
            rest = [ln for ln in after[1:] if normalise("creditor_name", ln) != normalise("creditor_name", name)]
            if rest:
                out["creditor_city"] = re.sub(r"^\s*[\dOo]{4}\s*", "", rest[0]).strip() or None
    return out


def normalise(field: str, value: str | None) -> str | None:
    """The form two readings are compared in: no spaces, case-blind; amounts as numbers."""
    if value is None or str(value).strip() == "":
        return None
    v = str(value)
    if field == "amount":
        try:
            return f"{float(v.replace(' ', '').replace(chr(39), '')):.2f}"
        except ValueError:
            return None
    v = re.sub(r"\s", "", v)
    return v.upper() if field in ("iban", "reference") else v.casefold()


def score_fields(predicted: dict, truth: dict) -> dict[str, bool]:
    return {f: normalise(f, predicted.get(f)) == normalise(f, truth.get(f)) for f in FIELDS}
