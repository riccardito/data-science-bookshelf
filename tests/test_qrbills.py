import numpy as np
import pytest

from ds_toolbox import qrbills as qb


def test_check_digits():
    assert qb.iban_valid("CH44 3199 9123 0008 8901 2")        # the standard's example QR-IBAN
    assert not qb.iban_valid("CH44 3199 9123 0008 0901 2")    # one digit misread
    assert not qb.iban_valid("not an iban")
    assert qb.reference_valid("21 00000 00003 13947 14300 09017")
    assert not qb.reference_valid("21 00000 00003 13947 14300 09018")
    iban = qb.make_iban("30000", "123456789012")
    assert qb.iban_valid(iban) and iban.startswith("CH")


def test_generated_bills_are_valid_and_reproducible():
    bills = qb.generate_bills(20, seed=3)
    assert bills == qb.generate_bills(20, seed=3)
    for b in bills:
        assert qb.iban_valid(b.iban) and qb.reference_valid(b.reference)
        assert 30000 <= int(b.iban[4:9]) <= 31999          # a QR-IBAN
        assert set(b.fields()) == set(qb.FIELDS)


def test_tamper_changes_exactly_one_printed_field():
    b = qb.generate_bills(1, seed=1)[0]
    t, field = qb.tamper(b, np.random.default_rng(0))
    changed = [k for k in qb.FIELDS if b.fields()[k] != t.fields()[k]]
    assert changed == [field]


def test_formatting():
    assert qb.format_iban("CH4431999123000889012") == "CH44 3199 9123 0008 8901 2"
    assert qb.format_reference("210000000003139471430009017") == "21 00000 00003 13947 14300 09017"
    assert qb.format_amount("1199.95") == "1 199.95"


def test_render_decode_parse_round_trip():
    b = qb.generate_bills(1, seed=7)[0]
    img = qb.render(b)
    assert img.shape == (620, 1240, 3)
    payload = qb.decode_qr(img)
    assert payload == b.qr_payload()
    assert qb.parse_payload(payload) == b.fields()
    assert qb.parse_payload("SPC\n0100\n") is None


def test_distortion_levels():
    img = qb.render(qb.generate_bills(1, seed=2)[0])
    assert np.array_equal(qb.distort(img, 0), img)
    assert qb.distort(img, 4).shape[1] < img.shape[1]       # the far snapshot is smaller
    assert np.array_equal(qb.distort(img, 2, seed=5), qb.distort(img, 2, seed=5))
    with pytest.raises(ValueError):
        qb.distort(img, 7)
    assert qb.decode_qr(qb.distort(img, 4, seed=1)) is None


def test_repair_fixes_one_confusion_and_only_one():
    good = "CH4431999123000889012"
    assert qb.repair(good, qb.iban_valid) == good
    assert qb.repair("CH4431999123000809012", qb.iban_valid) == good      # 8 read as 0
    assert qb.repair("CH4431999999999999999", qb.iban_valid) == "CH4431999999999999999"


def test_rules_read_a_clean_ocr_transcript():
    b = qb.generate_bills(1, seed=4)[0]
    lines = ["Payment part", "Account/Payableto", qb.format_iban(b.iban), b.creditor_name,
             f"{b.creditor_pcode}{b.creditor_city}", "Reference", qb.format_reference(b.reference),
             "CurrencyAmount", "CHF", qb.format_amount(b.amount)]
    got = qb.extract_by_rules(lines)
    assert all(qb.score_fields(got, b.fields()).values()), got
    assert qb.extract_by_rules([]) == dict.fromkeys(qb.FIELDS)


def test_normalise_and_score():
    assert qb.normalise("amount", "1 199.95") == "1199.95"
    assert qb.normalise("amount", "x") is None and qb.normalise("iban", " ") is None
    assert qb.normalise("creditor_name", "Muster AG") == qb.normalise("creditor_name", "MusterAG")
    assert qb.score_fields({"iban": "ch44 3199"}, {"iban": "CH443199"})["iban"]


def test_ocr_reads_a_clean_bill():
    b = qb.generate_bills(1, seed=9)[0]
    lines = qb.ocr_lines(qb.render(b))
    assert all(0 <= x <= 1 and 0 <= y <= 1 for _, x, y in lines)
    got = qb.extract_by_rules(lines)
    assert qb.normalise("iban", got["iban"]) == b.iban and got["amount"] == b.amount
    assert got["creditor_city"] == b.creditor_city or got["creditor_city"].casefold() in b.creditor_city.casefold()
    assert qb.line_texts(lines)[0] == lines[0][0] and qb.line_texts(["a"]) == ["a"]


def test_confusion_table_is_symmetric():
    for a, alts in qb.CONFUSIONS.items():
        for b in alts:
            assert a in qb.CONFUSIONS[b]
    # a 6 misread as an 8 is now repairable
    good = qb.make_iban("30000", "123456789012")
    i = good.index("6", 4)
    assert qb.repair(good[:i] + "8" + good[i + 1:], qb.iban_valid) in (good, good[:i] + "8" + good[i + 1:])


def test_rules_skip_the_receipts_repeated_lines():
    b = qb.generate_bills(1, seed=4)[0]
    iban = qb.format_iban(b.iban)
    lines = ["Receipt", "Payment part", "Account/Payableto", iban, iban.replace(" ", ""), b.creditor_name,
             b.creditor_name.replace(" ", ""), f"{b.creditor_pcode} {b.creditor_city}", "Reference"]
    got = qb.extract_by_rules(lines)
    assert qb.normalise("creditor_name", got["creditor_name"]) == qb.normalise("creditor_name", b.creditor_name)
    assert got["creditor_city"] == b.creditor_city
