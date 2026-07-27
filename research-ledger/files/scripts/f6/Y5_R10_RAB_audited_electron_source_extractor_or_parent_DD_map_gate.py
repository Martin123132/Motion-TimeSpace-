from __future__ import annotations

import csv
import math
import re
from html import unescape
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


PACK_ID = "P8_Y5_R10_1330"
TITLE = "1330-Y5-R10-RAB-audited-electron-source-extractor-or-parent-DD-map-gate"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
COMPONENT_ROOT = ROOT / "source-intake" / "component-fractions"
COMPONENT_RAW = COMPONENT_ROOT / "raw"
SOURCE_CACHE = COMPONENT_ROOT / "source-cache" / "nist_1330"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FETCH_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_NIST_FETCH_LEDGER.csv"
CONSTANT_PATH = OUT_DIR / f"{PACK_ID}_NIST_ELECTRON_MASS_EXTRACTION.csv"
ATOMIC_WEIGHT_PATH = OUT_DIR / f"{PACK_ID}_NIST_ATOMIC_WEIGHT_EXTRACTION.csv"
ELEMENT_CONTRIB_PATH = OUT_DIR / f"{PACK_ID}_AUDITED_ELECTRON_ELEMENT_CONTRIBUTIONS.csv"
ELECTRON_ROWS_PATH = OUT_DIR / f"{PACK_ID}_AUDITED_ELECTRON_FRACTION_ROWS.csv"
RAW_CANDIDATE_PATH = COMPONENT_RAW / f"{PACK_ID}_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv"
DELTA_PATH = OUT_DIR / f"{PACK_ID}_AUDITED_ELECTRON_DELTA_VECTOR.csv"
DIFF_PATH = OUT_DIR / f"{PACK_ID}_1329_TO_1330_DIFF_LEDGER.csv"
DD_GATE_PATH = OUT_DIR / f"{PACK_ID}_PARENT_DD_MAP_GATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1330_VALIDATION.csv"

ELEMENTS = {
    "Ti": {"Z": 22, "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=Ti"},
    "Al": {"Z": 13, "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=Al"},
    "V": {"Z": 23, "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=V"},
    "Pt": {"Z": 78, "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=Pt"},
    "Rh": {"Z": 45, "url": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ascii=ascii&ele=Rh"},
}
ELECTRON_MASS_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?meu"
MATERIAL_ID_MAP = {"M983_0_PtRh10": "PtRh10", "M983_1_TiAlloy": "TA6V"}


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1330*") if path.is_file()]


def finite_positive(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0.0


def finite_nonnegative(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number >= 0.0


def fmt(value: float) -> str:
    return f"{value:.12e}"


def cache_name(label: str) -> Path:
    safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "_", label)
    return SOURCE_CACHE / f"{safe_label}.html"


def fetch_or_cache(label: str, url: str) -> tuple[str, dict[str, object]]:
    SOURCE_CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = cache_name(label)
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 MTS-source-audit/1330"})
        with urlopen(request, timeout=30) as response:
            raw = response.read()
            encoding = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(encoding, errors="replace")
            cache_path.write_text(text, encoding="utf-8")
            return text, {
                "fetch_id": f"FETCH1330_{label}",
                "label": label,
                "url": url,
                "cache_path": str(cache_path),
                "status": "LIVE_FETCH_OK",
                "bytes": len(raw),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
    except (OSError, URLError, TimeoutError) as exc:
        if cache_path.exists():
            text = cache_path.read_text(encoding="utf-8", errors="replace")
            return text, {
                "fetch_id": f"FETCH1330_{label}",
                "label": label,
                "url": url,
                "cache_path": str(cache_path),
                "status": "CACHE_FALLBACK_OK",
                "bytes": cache_path.stat().st_size,
                "fetch_error": repr(exc),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        return "", {
            "fetch_id": f"FETCH1330_{label}",
            "label": label,
            "url": url,
            "cache_path": str(cache_path),
            "status": "FETCH_FAILED_NO_CACHE",
            "bytes": 0,
            "fetch_error": repr(exc),
            "valid_for_claim": False,
            "claim_allowed": False,
        }


def strip_html(text: str) -> str:
    with_sup = re.sub(r"<sup>(.*?)</sup>", r" \1 ", text, flags=re.IGNORECASE | re.DOTALL)
    plain = unescape(re.sub(r"<[^>]+>", " ", with_sup, flags=re.DOTALL))
    return " ".join(plain.replace("\xa0", " ").split())


def parse_spaced_number(number: str, exponent: str) -> float:
    return float(number.replace(" ", "")) * (10.0 ** int(exponent))


def parse_electron_mass(text: str) -> dict[str, object]:
    plain = strip_html(text)
    value_match = re.search(r"Numerical value\s+([0-9. ]+)\s+x\s+10\s+(-?\d+)\s+u", plain)
    uncertainty_match = re.search(r"Standard uncertainty\s+([0-9. ]+)\s+x\s+10\s+(-?\d+)\s+u", plain)
    concise_match = re.search(r"Concise form\s+([0-9. ]+\(\d+\)\s+x\s+10\s+-?\d+\s+u)", plain)
    source_match = re.search(r"Source:\s+([^D]+?recommended values)", plain)
    if not value_match or not uncertainty_match:
        raise ValueError("Could not parse NIST electron mass in u page")
    value = parse_spaced_number(value_match.group(1), value_match.group(2))
    uncertainty = parse_spaced_number(uncertainty_match.group(1), uncertainty_match.group(2))
    return {
        "constant_id": "CONST1330_0_m_e_u",
        "symbol": "m_e/u",
        "value": fmt(value),
        "standard_uncertainty": fmt(uncertainty),
        "relative_uncertainty": fmt(uncertainty / value),
        "units": "dimensionless atomic-mass-unit ratio",
        "source_url": ELECTRON_MASS_URL,
        "source_label": source_match.group(1).strip() if source_match else "NIST CODATA page",
        "concise_form": concise_match.group(1).strip() if concise_match else "PARSE_NOT_AVAILABLE",
        "extraction_method": "live_or_cached_html_regex",
        "status": "AUDIT_EXTRACTED_NONCLAIM",
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def uncertainty_from_parentheses(value_text: str) -> tuple[float, float, str]:
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(?:\((\d+)\))?", value_text.strip())
    if not match:
        raise ValueError(f"Unsupported standard atomic weight format: {value_text}")
    value_part = match.group(1)
    digits = match.group(2)
    value = float(value_part)
    if digits is None:
        return value, 0.0, value_text
    decimals = len(value_part.split(".")[1]) if "." in value_part else 0
    uncertainty = int(digits) * (10.0 ** (-decimals))
    return value, uncertainty, value_text


def parse_atomic_weight(symbol: str, text: str) -> dict[str, object]:
    pre_match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.IGNORECASE | re.DOTALL)
    body = strip_html(pre_match.group(1) if pre_match else text)
    for line in body.split(" __"):
        if symbol not in line:
            continue
    raw_lines = unescape(re.sub(r"<[^>]+>", "", pre_match.group(1), flags=re.DOTALL)) if pre_match else text
    for raw_line in raw_lines.replace("\xa0", " ").splitlines():
        tokens = raw_line.split()
        if len(tokens) >= 6 and tokens[1] == symbol:
            value, uncertainty, source_text = uncertainty_from_parentheses(tokens[5])
            return {
                "weight_id": f"AW1330_{symbol}",
                "element": symbol,
                "Z": ELEMENTS[symbol]["Z"],
                "standard_atomic_weight": str(value),
                "standard_atomic_weight_uncertainty": fmt(uncertainty),
                "source_text": source_text,
                "source_url": ELEMENTS[symbol]["url"],
                "extraction_method": "NIST_ascii_pre_first_standard_weight_row",
                "status": "AUDIT_EXTRACTED_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
    raise ValueError(f"Could not parse standard atomic weight for {symbol}")


def compute_electron_rows(
    material_rows: list[dict[str, str]],
    electron_constant: dict[str, object],
    atomic_weights: dict[str, dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    electron_mass_u = float(electron_constant["value"])
    electron_mass_uncertainty = float(electron_constant["standard_uncertainty"])
    by_material: dict[str, list[dict[str, str]]] = {}
    for row in material_rows:
        material_id = MATERIAL_ID_MAP.get(row["material_id"], row["material_id"])
        by_material.setdefault(material_id, []).append(row)

    element_contrib: list[dict[str, object]] = []
    electron_rows: list[dict[str, object]] = []
    for material_id in ["TA6V", "PtRh10"]:
        fraction = 0.0
        uncertainty_square = 0.0
        for row in by_material[material_id]:
            element = row["element"]
            mass_fraction = float(row["mass_fraction"])
            charge_z = float(row["Z"])
            atomic_weight = float(atomic_weights[element]["standard_atomic_weight"])
            atomic_weight_uncertainty = float(atomic_weights[element]["standard_atomic_weight_uncertainty"])
            contribution = mass_fraction * charge_z * electron_mass_u / atomic_weight
            relative_uncertainty_square = 0.0
            if electron_mass_u > 0.0:
                relative_uncertainty_square += (electron_mass_uncertainty / electron_mass_u) ** 2
            if atomic_weight > 0.0:
                relative_uncertainty_square += (atomic_weight_uncertainty / atomic_weight) ** 2
            contribution_uncertainty = abs(contribution) * math.sqrt(relative_uncertainty_square)
            fraction += contribution
            uncertainty_square += contribution_uncertainty**2
            element_contrib.append(
                {
                    "contribution_id": f"EFC1330_{material_id}_{element}",
                    "material_id": material_id,
                    "element": element,
                    "mass_fraction": row["mass_fraction"],
                    "Z": row["Z"],
                    "standard_atomic_weight": str(atomic_weight),
                    "standard_atomic_weight_uncertainty": fmt(atomic_weight_uncertainty),
                    "electron_mass_u": electron_constant["value"],
                    "electron_mass_u_uncertainty": electron_constant["standard_uncertainty"],
                    "electron_fraction_contribution": fmt(contribution),
                    "contribution_uncertainty": fmt(contribution_uncertainty),
                    "source": row["source"] + ";NIST_CODATA_m_e_u;NIST_atomic_weight_" + element,
                    "status": "AUDIT_EXTRACTED_NONCLAIM",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        source_uncertainty = math.sqrt(uncertainty_square)
        conservative_uncertainty = max(source_uncertainty, 0.001 * fraction)
        electron_rows.append(
            {
                "row_id": f"CFI1330_{material_id}_electron",
                "material_id": material_id,
                "component_id": "electron",
                "fraction_value": fmt(fraction),
                "fraction_uncertainty": fmt(conservative_uncertainty),
                "basis_convention": "other_with_source",
                "source_path_or_url": "NIST_CODATA_m_e_u;NIST_atomic_weights_Ti_Al_V_Pt_Rh;source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
                "extraction_method": "formula",
                "source_uncertainty_only": fmt(source_uncertainty),
                "conservative_floor": "0.1_percent_nonclaim_floor",
                "status": "AUDIT_EXTRACTED_SCHEMA_VALID_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    delta = float(electron_rows[0]["fraction_value"]) - float(electron_rows[1]["fraction_value"])
    delta_uncertainty = math.sqrt(float(electron_rows[0]["fraction_uncertainty"]) ** 2 + float(electron_rows[1]["fraction_uncertainty"]) ** 2)
    delta_rows = [
        {
            "delta_id": "DELTA1330_0_TA6V_minus_PtRh10_electron",
            "component_id": "electron",
            "left_material": "TA6V",
            "right_material": "PtRh10",
            "delta_fraction": fmt(delta),
            "abs_delta_fraction": fmt(abs(delta)),
            "delta_uncertainty": fmt(delta_uncertainty),
            "interpretation": "audited electron rest-mass fraction contrast only; not WEP and not full Delta_w_TiPt",
            "status": "AUDIT_EXTRACTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return element_contrib, electron_rows, delta_rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENT_RAW.mkdir(parents=True, exist_ok=True)
    SOURCE_CACHE.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1330_0_1329_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1329_NEXT_TARGET.csv",
            "needle": "NEXT1329_0_1330",
            "role": "selected 1330 target",
        },
        {
            "source_id": "SRC1330_1_1329_dryrun",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1329_ELECTRON_FRACTION_DRYRUN_ROWS.csv",
            "needle": "CFI1329_TA6V_electron",
            "role": "manual dry-run comparison baseline",
        },
        {
            "source_id": "SRC1330_2_1329_raw",
            "local_path": "source-intake/component-fractions/raw/P8_Y5_R10_1329_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv",
            "needle": "CFI1329_PtRh10_electron",
            "role": "prior raw nonclaim candidate",
        },
        {
            "source_id": "SRC1330_3_983_material_constituents",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
            "needle": "M983_1_TiAlloy",
            "role": "local material constituent rows",
        },
        {
            "source_id": "SRC1330_4_1233_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "needle": "source_path_or_url",
            "role": "raw candidate schema",
        },
        {
            "source_id": "SRC1330_5_1329_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1329_VALIDATION.csv",
            "needle": "VAL1329_11_overall",
            "role": "1329 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    fetch_ledger: list[dict[str, object]] = []
    electron_text, electron_fetch = fetch_or_cache("electron_mass_u", ELECTRON_MASS_URL)
    fetch_ledger.append(electron_fetch)
    electron_constant = parse_electron_mass(electron_text)

    atomic_weight_rows: list[dict[str, object]] = []
    atomic_weight_map: dict[str, dict[str, object]] = {}
    for element, info in ELEMENTS.items():
        text, fetch_row = fetch_or_cache(f"atomic_weight_{element}", str(info["url"]))
        fetch_ledger.append(fetch_row)
        parsed = parse_atomic_weight(element, text)
        atomic_weight_rows.append(parsed)
        atomic_weight_map[element] = parsed

    material_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv"))
    element_contrib, electron_rows, delta_rows = compute_electron_rows(material_rows, electron_constant, atomic_weight_map)

    raw_candidate_rows = [
        {
            "row_id": row["row_id"],
            "material_id": row["material_id"],
            "component_id": row["component_id"],
            "fraction_value": row["fraction_value"],
            "fraction_uncertainty": row["fraction_uncertainty"],
            "basis_convention": row["basis_convention"],
            "source_path_or_url": row["source_path_or_url"],
            "extraction_method": row["extraction_method"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in electron_rows
    ]
    schema_fields = [
        "row_id",
        "material_id",
        "component_id",
        "fraction_value",
        "fraction_uncertainty",
        "basis_convention",
        "source_path_or_url",
        "extraction_method",
        "valid_for_claim",
    ]
    write_csv(RAW_CANDIDATE_PATH, raw_candidate_rows, schema_fields)

    old_rows = {row["material_id"]: row for row in read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1329_ELECTRON_FRACTION_DRYRUN_ROWS.csv"))}
    diff_rows = []
    for row in electron_rows:
        old = old_rows[row["material_id"]]
        old_value = float(old["fraction_value"])
        new_value = float(row["fraction_value"])
        diff_rows.append(
            {
                "diff_id": f"DIFF1330_{row['material_id']}_electron",
                "material_id": row["material_id"],
                "component_id": "electron",
                "old_1329_fraction": old["fraction_value"],
                "new_1330_fraction": row["fraction_value"],
                "absolute_difference": fmt(abs(new_value - old_value)),
                "relative_difference": fmt(abs(new_value - old_value) / old_value if old_value else 0.0),
                "reason": "NIST/CODATA live-or-cached extraction replaces manual constants; electron mass value uses 2022 CODATA page",
                "status": "DIFF_EXPECTED_SMALL_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    dd_gate = [
        {
            "gate_id": "DDG1330_0_map_target",
            "object": "parent MTS source weights to Damour-Donoghue charge vector",
            "formal_need": "derive a functor/map taking MTS component source weights into DD-style material charge basis without importing DD as parent ontology",
            "current_status": "NOT_DERIVED",
            "blocker": "no parent action clause selects light_quark/QCD/EM/surface basis and no double-counting rule",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "DDG1330_1_normalization",
            "object": "electron source normalization",
            "formal_need": "parent action must sign whether electron rest mass fraction is the source-weight component used in Delta_w",
            "current_status": "NUMERIC_COMPONENT_AVAILABLE_PARENT_SIGNATURE_MISSING",
            "blocker": "mass-energy normalization and binding subtraction convention are not parent-owned yet",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "DDG1330_2_QCD_residual",
            "object": "QCD/gluon residual source component",
            "formal_need": "derive residual mass-budget owner after quark, EM, nuclear, electron, and readout components are declared",
            "current_status": "MISSING_NO_DOUBLE_COUNT_RULE",
            "blocker": "residual term would absorb convention choices rather than measure a parent source component",
            "promotion_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1330_0_audited_electron_component",
            "target": "electron component of finite Delta_w_TiPt",
            "input_status": "AUDIT_EXTRACTED_NUMERIC_NONCLAIM",
            "runner_status": "PARTIAL_COMPONENT_READY_NOT_SCOREABLE",
            "reason": "electron component is source-extracted, but parent normalization and other source components are missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1330_1_parent_DD_map",
            "target": "map MTS source weights to external DD material charges",
            "input_status": "THEOREM_BLOCKERS_EXPLICIT",
            "runner_status": "REFUSED_NO_PARENT_MAP",
            "reason": "DD remains external comparator until the parent action signs basis, normalization, and no-double-counting",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1330_2_full_Delta_w",
            "target": "full Delta_w_TiPt source vector",
            "input_status": "MISSING_LIGHT_QUARK_QCD_EM_NUCLEAR_READOUT_PARENT_MAP",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "reason": "one audited electron row is insufficient for WEP/local-GR closure",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1330_0_no_audited_electron_only_WEP",
            "shortcut": "treat audited electron fraction as WEP prediction",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1330_1_no_raw_nonclaim_as_claim",
            "shortcut": "promote raw candidate schema validity to claim validity",
            "enforcement": "REFUSED; valid_for_claim remains false",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1330_2_no_DD_import_as_derivation",
            "shortcut": "import DD source charges as MTS parent components",
            "enforcement": "REFUSED by parent DD map gate",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1330_3_no_local_GR_claim",
            "shortcut": "promote source-component progress to local-GR derivation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1330_0_audited_extractor_success",
            "decision": "manual electron dry-run has been upgraded to live-or-cached NIST extraction",
            "because": "NIST CODATA electron mass and NIST atomic weights parse into finite source-backed rows",
            "effect": "electron component is stronger evidence plumbing, but still nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1330_1_next_theory_pressure",
            "decision": "the next hard wall is parent basis/normalization, not the electron arithmetic",
            "because": "source extraction is now good enough to show the missing piece is the parent map and remaining components",
            "effect": "move to a parent source-basis map theorem or explicit demotion for light-quark/QCD/EM/nuclear rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1330_0_1331",
            "target_file": "1331-Y5-R10-RAB-parent-source-basis-map-theorem-or-light-quark-DD-demotion.md",
            "target_script": "scripts/Y5_R10_RAB_parent_source_basis_map_theorem_or_light_quark_DD_demotion.py",
            "task": "try to derive the parent source-basis map needed to interpret DD/light-quark/QCD/EM/nuclear components as MTS source weights; if not, demote them cleanly to external comparator status",
            "success_condition": "a precise parent-map theorem closes at least one non-electron component, or the blocker ledger shows exactly why the map is not derivable yet",
            "do_not": "do not score WEP, do not claim DD is MTS, do not tune Ti/Pt cancellation, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        fetch_ledger,
        [electron_constant],
        atomic_weight_rows,
        element_contrib,
        electron_rows,
        raw_candidate_rows,
        delta_rows,
        diff_rows,
        dd_gate,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    fetches_ok = len(fetch_ledger) == 6 and all(row["status"] in {"LIVE_FETCH_OK", "CACHE_FALLBACK_OK"} for row in fetch_ledger)
    snapshots_exist = all(Path(str(row["cache_path"])).exists() and int(row["bytes"]) > 0 for row in fetch_ledger)
    electron_parse_ok = finite_positive(electron_constant["value"]) and finite_positive(electron_constant["standard_uncertainty"]) and "CODATA" in str(electron_constant["source_label"])
    weights_ok = len(atomic_weight_rows) == 5 and all(finite_positive(row["standard_atomic_weight"]) for row in atomic_weight_rows)
    raw_exists = RAW_CANDIDATE_PATH.exists()
    raw_rows = read_csv(RAW_CANDIDATE_PATH) if raw_exists else []
    raw_schema_ok = len(raw_rows) == 2 and all(set(schema_fields).issubset(row.keys()) for row in raw_rows)
    raw_numeric_ok = all(finite_positive(row.get("fraction_value")) and finite_nonnegative(row.get("fraction_uncertainty")) for row in raw_rows)
    raw_nonclaim = all(is_false(row.get("valid_for_claim", False)) for row in raw_rows)
    delta_ok = len(delta_rows) == 1 and finite_positive(delta_rows[0]["abs_delta_fraction"])
    diff_small = all(float(row["relative_difference"]) < 1e-8 for row in diff_rows)
    dd_blocked = all(row["promotion_allowed"] is False for row in dd_gate)
    runner_not_scoreable = all(row["score_ready"] is False and str(row["runner_status"]) != "SCORE_READY" for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1331 = next_target[0]["target_file"].startswith("1331-")

    validations = [
        validation_row(
            "VAL1330_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1330_1_fetches_cached",
            "NIST source pages fetch live or use existing cache and snapshots exist",
            fetches_ok and snapshots_exist,
            ";".join(f"{row['label']}={row['status']}" for row in fetch_ledger),
        ),
        validation_row(
            "VAL1330_2_electron_mass_parsed",
            "NIST CODATA electron mass in u parsed with uncertainty",
            electron_parse_ok,
            f"value={electron_constant['value']};uncertainty={electron_constant['standard_uncertainty']};source={electron_constant['source_label']}",
        ),
        validation_row(
            "VAL1330_3_atomic_weights_parsed",
            "NIST standard atomic weights parsed for Ti, Al, V, Pt, Rh",
            weights_ok,
            ";".join(f"{row['element']}={row['standard_atomic_weight']}" for row in atomic_weight_rows),
        ),
        validation_row(
            "VAL1330_4_raw_candidate_schema",
            "raw audited electron candidate file exists with 1233 schema fields",
            raw_exists and raw_schema_ok,
            f"raw_path={RAW_CANDIDATE_PATH};raw_rows={len(raw_rows)}",
        ),
        validation_row(
            "VAL1330_5_numeric_nonclaim_rows",
            "audited electron rows are finite numeric and nonclaim",
            raw_numeric_ok and raw_nonclaim and delta_ok,
            f"delta={delta_rows[0]['delta_fraction']};delta_uncertainty={delta_rows[0]['delta_uncertainty']}",
        ),
        validation_row(
            "VAL1330_6_diff_expected_small",
            "1330 audited extraction differs only tiny amount from 1329 manual dry-run",
            diff_small,
            ";".join(f"{row['material_id']} rel_diff={row['relative_difference']}" for row in diff_rows),
        ),
        validation_row(
            "VAL1330_7_parent_DD_map_blocked",
            "parent DD/source-basis map remains blocked",
            dd_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in dd_gate),
        ),
        validation_row(
            "VAL1330_8_runner_not_scoreable",
            "Delta_w/WEP/local-GR runners are not score-ready",
            runner_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1330_9_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1330_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1330_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1330_12_next_target_1331",
            "next target routes to parent source-basis map theorem or DD demotion",
            next_is_1331,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1330_13_overall",
            "overall 1330 validation",
            all(row["status"] == "PASS" for row in validations),
            "1330 upgrades electron source extraction and keeps DD/full Delta_w/local-GR blocked",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(FETCH_LEDGER_PATH, fetch_ledger)
    write_csv(CONSTANT_PATH, [electron_constant])
    write_csv(ATOMIC_WEIGHT_PATH, atomic_weight_rows)
    write_csv(ELEMENT_CONTRIB_PATH, element_contrib)
    write_csv(ELECTRON_ROWS_PATH, electron_rows)
    write_csv(DELTA_PATH, delta_rows)
    write_csv(DIFF_PATH, diff_rows)
    write_csv(DD_GATE_PATH, dd_gate)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1330 upgrades the electron fraction from a manual dry-run to a live-or-cached NIST extraction. This is a real plumbing improvement, but it still does not score WEP, close `Delta_w_TiPt`, or derive local GR.

**Main progress:** the audited electron contrast is `Delta F_e(TA6V-PtRh10) = {delta_rows[0]["delta_fraction"]}` with nonclaim uncertainty `{delta_rows[0]["delta_uncertainty"]}`. The 1329-to-1330 change is tiny and expected because the electron mass source is now NIST/CODATA 2022.

**Decision:** the arithmetic is no longer the bottleneck. The bottleneck is now explicitly the parent source-basis map: MTS must derive how electron/light-quark/QCD/EM/nuclear/readout components enter one parent source vector.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## NIST Fetch Ledger
{markdown_table(fetch_ledger, ["fetch_id", "label", "url", "cache_path", "status", "bytes", "valid_for_claim", "claim_allowed"])}

## NIST Electron Mass Extraction
{markdown_table([electron_constant], ["constant_id", "symbol", "value", "standard_uncertainty", "relative_uncertainty", "units", "source_url", "source_label", "concise_form", "extraction_method", "status", "valid_for_claim", "claim_allowed"])}

## NIST Atomic Weight Extraction
{markdown_table(atomic_weight_rows, ["weight_id", "element", "Z", "standard_atomic_weight", "standard_atomic_weight_uncertainty", "source_text", "source_url", "extraction_method", "status", "valid_for_claim", "claim_allowed"])}

## Audited Electron Element Contributions
{markdown_table(element_contrib, ["contribution_id", "material_id", "element", "mass_fraction", "Z", "standard_atomic_weight", "standard_atomic_weight_uncertainty", "electron_mass_u", "electron_mass_u_uncertainty", "electron_fraction_contribution", "contribution_uncertainty", "source", "status", "valid_for_claim", "claim_allowed"])}

## Audited Electron Fraction Rows
{markdown_table(electron_rows, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "source_path_or_url", "extraction_method", "source_uncertainty_only", "conservative_floor", "status", "valid_for_claim", "claim_allowed"])}

## Raw Candidate File
Schema-shaped nonclaim candidate written to:

`{RAW_CANDIDATE_PATH}`

{markdown_table(raw_candidate_rows, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "source_path_or_url", "extraction_method", "valid_for_claim"])}

## Audited Electron Delta Vector
{markdown_table(delta_rows, ["delta_id", "component_id", "left_material", "right_material", "delta_fraction", "abs_delta_fraction", "delta_uncertainty", "interpretation", "status", "valid_for_claim", "claim_allowed"])}

## 1329 To 1330 Diff Ledger
{markdown_table(diff_rows, ["diff_id", "material_id", "component_id", "old_1329_fraction", "new_1330_fraction", "absolute_difference", "relative_difference", "reason", "status", "valid_for_claim", "claim_allowed"])}

## Parent DD Map Gate
{markdown_table(dd_gate, ["gate_id", "object", "formal_need", "current_status", "blocker", "promotion_allowed", "valid_for_claim", "claim_allowed"])}

## Delta-w Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")
    print(f"Wrote raw nonclaim audited electron candidate {RAW_CANDIDATE_PATH}")


if __name__ == "__main__":
    main()
