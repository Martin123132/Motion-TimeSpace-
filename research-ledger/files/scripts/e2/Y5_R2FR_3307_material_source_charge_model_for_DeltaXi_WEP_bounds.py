from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3307-Y5-R2FR-material-source-charge-model-for-DeltaXi-WEP-bounds-under-AX1090.md"

SRC_3306_DOC = ROOT / "3306-Y5-R2FR-linearized-public-metric-projector-extraction-or-WEP-data-acquisition-under-AX1090.md"
SRC_3306_WEP = OUT / "P8_Y5_R2FR_3306_WEP_SOURCE_ANCHORS.csv"
SRC_3306_MAPPING = OUT / "P8_Y5_R2FR_3306_WEP_TO_DELTA_XI_MAPPING.csv"
SRC_3306_DECISION = OUT / "P8_Y5_R2FR_3306_DECISION_LEDGER.csv"
SRC_3306_NEXT = OUT / "P8_Y5_R2FR_3306_NEXT_TARGET.csv"
SRC_3306_VALIDATION = OUT / "P8_Y5_BRR545_3306_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3307_SOURCE_REGISTER.csv",
    "charge_basis": OUT / "P8_Y5_R2FR_3307_MATERIAL_CHARGE_BASIS.csv",
    "material_table": OUT / "P8_Y5_R2FR_3307_MATERIAL_PROXY_CHARGES.csv",
    "pair_deltas": OUT / "P8_Y5_R2FR_3307_WEP_PAIR_CHARGE_DELTAS.csv",
    "delta_xi_law": OUT / "P8_Y5_R2FR_3307_DELTA_XI_LINEAR_MODEL.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3307_WEP_BOUND_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3307_MATERIAL_CHARGE_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3307_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3307_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3307_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3307_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

MATERIALS = {
    "Be_proxy": {
        "element": "Be",
        "Z": 4.0,
        "A": 9.0122,
        "experiment_role": "Eot-Wash Be/Ti test body",
        "composition_status": "natural-element proxy, not full alloy/isotopic assay",
    },
    "Ti_proxy": {
        "element": "Ti",
        "Z": 22.0,
        "A": 47.867,
        "experiment_role": "MICROSCOPE Ti/Pt and Eot-Wash Be/Ti test body",
        "composition_status": "natural-element proxy, not MICROSCOPE alloy/isotopic assay",
    },
    "Pt_proxy": {
        "element": "Pt",
        "Z": 78.0,
        "A": 195.084,
        "experiment_role": "MICROSCOPE Ti/Pt test body",
        "composition_status": "natural-element proxy, not MICROSCOPE alloy/isotopic assay",
    },
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 820) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered_needles):
            hits.append(f"L{line_number}:{compact(line, 420)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3306_DOC, "3306 projector/WEP handoff", ["MICROSCOPE", "Eot-Wash", "Delta_Xi"]),
        (SRC_3306_WEP, "3306 WEP anchors", ["WEP3306_0_MICROSCOPE_Ti_Pt", "WEP3306_1_EOTWASH_Be_Ti"]),
        (SRC_3306_MAPPING, "3306 WEP mapping", ["Delta_Xi_0", "Delta_Xi_2"]),
        (SRC_3306_DECISION, "3306 decision", ["DEC3306_1", "WEP anchors"]),
        (SRC_3306_NEXT, "3306 next target", ["material-source-charge-model", "DeltaXi"]),
        (SRC_3306_VALIDATION, "3306 validation", ["VAL3306_11_overall", "true"]),
    ]
    rows: list[dict[str, Any]] = []
    for index, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3307_{index}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def charge_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "QMAT3307_0_baryon",
            "symbol": "q_B",
            "definition": "baryon/mass-normalized universal matter charge",
            "proxy_formula": "1",
            "why_included": "checks whether Xi residual is just universal mass coupling; should cancel in Delta_Xi if pure Hilbert",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QMAT3307_1_proton_fraction",
            "symbol": "q_p",
            "definition": "proton fraction proxy",
            "proxy_formula": "Z/A",
            "why_included": "composition-dependent coupling to proton/electron/EM-like source content",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QMAT3307_2_neutron_fraction",
            "symbol": "q_n",
            "definition": "neutron fraction proxy",
            "proxy_formula": "(A-Z)/A",
            "why_included": "composition-dependent coupling to neutron content",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QMAT3307_3_coulomb_proxy",
            "symbol": "q_C",
            "definition": "semi-empirical Coulomb binding proxy",
            "proxy_formula": "Z(Z-1)/A^(4/3)",
            "why_included": "tests EM/Poynting/binding-energy leakage into finite-mode source charge",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "QMAT3307_4_neutron_excess",
            "symbol": "q_D",
            "definition": "neutron-proton imbalance proxy",
            "proxy_formula": "(A-2Z)/A",
            "why_included": "common WEP charge direction for nuclear composition contrast",
            "valid_for_claim": "false",
        },
    ]


def material_charges(material: dict[str, Any]) -> dict[str, float]:
    z = float(material["Z"])
    a = float(material["A"])
    return {
        "q_B": 1.0,
        "q_p": z / a,
        "q_n": (a - z) / a,
        "q_C": z * (z - 1.0) / (a ** (4.0 / 3.0)),
        "q_D": (a - 2.0 * z) / a,
    }


def material_table_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for material_id, material in MATERIALS.items():
        charges = material_charges(material)
        rows.append(
            {
                "material_id": material_id,
                "element_proxy": material["element"],
                "Z": material["Z"],
                "A": material["A"],
                "q_B": f"{charges['q_B']:.12g}",
                "q_p": f"{charges['q_p']:.12g}",
                "q_n": f"{charges['q_n']:.12g}",
                "q_C": f"{charges['q_C']:.12g}",
                "q_D": f"{charges['q_D']:.12g}",
                "experiment_role": material["experiment_role"],
                "composition_status": material["composition_status"],
                "valid_for_claim": "false",
            }
        )
    return rows


def pair_delta_rows() -> list[dict[str, Any]]:
    material_rows = {row["material_id"]: row for row in material_table_rows()}
    pairs = [
        ("PAIR3307_0_MICROSCOPE_Ti_Pt", "Ti_proxy", "Pt_proxy", "WEP3306_0_MICROSCOPE_Ti_Pt"),
        ("PAIR3307_1_EOTWASH_Be_Ti", "Be_proxy", "Ti_proxy", "WEP3306_1_EOTWASH_Be_Ti"),
    ]
    rows: list[dict[str, Any]] = []
    for pair_id, material_a, material_b, anchor_id in pairs:
        row_a = material_rows[material_a]
        row_b = material_rows[material_b]
        delta = {
            key: float(row_a[key]) - float(row_b[key])
            for key in ["q_B", "q_p", "q_n", "q_C", "q_D"]
        }
        rows.append(
            {
                "pair_id": pair_id,
                "anchor_id": anchor_id,
                "material_A": material_a,
                "material_B": material_b,
                "Delta_q_B": f"{delta['q_B']:.12g}",
                "Delta_q_p": f"{delta['q_p']:.12g}",
                "Delta_q_n": f"{delta['q_n']:.12g}",
                "Delta_q_C": f"{delta['q_C']:.12g}",
                "Delta_q_D": f"{delta['q_D']:.12g}",
                "interpretation": "proxy material charge contrast; not claim-ready without exact alloy/isotope composition",
                "valid_for_claim": "false",
            }
        )
    return rows


def delta_xi_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "DXI3307_0_scalar_linear_charge",
            "quantity": "Delta_Xi_0[A,B]",
            "formula": "Delta_Xi_0[A,B] = s_0B Delta_q_B + s_0p Delta_q_p + s_0n Delta_q_n + s_0C Delta_q_C + s_0D Delta_q_D + higher_terms",
            "meaning": "first-order scalar finite-mode source nonuniversality in a material charge basis",
            "claim_status": "coefficients s_0k not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "law_id": "DXI3307_1_spin2_linear_charge",
            "quantity": "Delta_Xi_2[A,B]",
            "formula": "Delta_Xi_2[A,B] = s_2B Delta_q_B + s_2p Delta_q_p + s_2n Delta_q_n + s_2C Delta_q_C + s_2D Delta_q_D + higher_terms",
            "meaning": "first-order massive spin-2 source nonuniversality in a material charge basis",
            "claim_status": "coefficients s_2k not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "law_id": "DXI3307_2_universal_limit",
            "quantity": "Xi_i[A]=1",
            "formula": "all nonuniversal coefficients s_ik=0, or all material charge contrasts project to zero",
            "meaning": "returns to Hilbert universal source coupling",
            "claim_status": "not proven",
            "valid_for_claim": "false",
        },
    ]


def combined_uncertainty(stat: str, syst: str) -> str:
    try:
        stat_value = float(stat)
        syst_value = float(syst)
    except ValueError:
        return "MISSING_COMBINED_UNCERTAINTY"
    return f"{math.sqrt(stat_value**2 + syst_value**2):.12g}"


def bound_rows() -> list[dict[str, Any]]:
    anchors = {row["anchor_id"]: row for row in read_csv(SRC_3306_WEP)}
    pair_rows = {row["anchor_id"]: row for row in pair_delta_rows()}
    rows: list[dict[str, Any]] = []
    for anchor_id, anchor in anchors.items():
        if anchor_id not in pair_rows:
            continue
        pair = pair_rows[anchor_id]
        rows.append(
            {
                "bound_id": f"BND3307_{anchor_id}",
                "anchor_id": anchor_id,
                "experiment": anchor["experiment"],
                "source_url": anchor["source_url"],
                "test_body_pair": anchor["test_body_pair"],
                "attractor_source": anchor["attractor_source"],
                "eta_central": anchor["eta_central"],
                "eta_sigma_proxy": combined_uncertainty(anchor["eta_stat_uncertainty"], anchor["eta_syst_uncertainty"]),
                "Delta_q_vector": f"({pair['Delta_q_B']},{pair['Delta_q_p']},{pair['Delta_q_n']},{pair['Delta_q_C']},{pair['Delta_q_D']})",
                "bound_template": "|sum_i alpha_i_star Xi_i[E] (s_i dot Delta_q_AB) range_factor(lambda_i,r)| <= eta_bound",
                "missing_before_claim": "s_ik coefficients; alpha_i_star; lambda_i; Xi_i[E]; exact material composition; confidence convention",
                "current_status": "NONCLAIM_BOUND_ROW",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows() -> list[dict[str, Any]]:
    materials = material_table_rows()
    pairs = pair_delta_rows()
    laws = delta_xi_law_rows()
    bounds = bound_rows()
    nonclaim = all(row["valid_for_claim"] == "false" for row in materials + pairs + laws + bounds)
    return [
        {
            "runner_id": "RUN3307_0_material_basis",
            "test": "material proxy charges exist for Be/Ti/Pt",
            "result": "PASS_NONCLAIM" if len(materials) == 3 else "FAIL",
            "detail": ";".join(row["material_id"] for row in materials),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3307_1_pair_deltas",
            "test": "charge contrasts exist for MICROSCOPE and Eot-Wash pairs",
            "result": "PASS_NONCLAIM" if len(pairs) == 2 else "FAIL",
            "detail": ";".join(row["pair_id"] for row in pairs),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3307_2_bound_rows_safe",
            "test": "bound rows exist but remain nonclaim",
            "result": "PASS_NONCLAIM" if len(bounds) == 2 and nonclaim else "FAIL",
            "detail": ";".join(row["bound_id"] for row in bounds),
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RUN3307_3_claim_permission",
            "test": "can score WEP claim",
            "result": "REFUSE_CLAIM_SOURCE_COEFFICIENTS_MISSING",
            "detail": "s_ik, alpha_i_star, lambda_i, Xi_i[E], exact materials, and CL convention are missing",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3307_0_material_charge_claim",
            "claim": "proxy material charges are exact experiment material charges",
            "requirements": "actual alloy/isotopic composition, EM/binding-energy model, and source-body composition",
            "current_evidence": "element proxy rows only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3307_1_DeltaXi_bound_claim",
            "claim": "WEP anchors bound Delta_Xi_0 and Delta_Xi_2",
            "requirements": "source coefficients s_ik and mode/range factors derived or bounded",
            "current_evidence": "linear model only",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3307_2_source_coupling_closed",
            "claim": "finite-mode source coupling is safe for local GR",
            "requirements": "Xi universality proof or numerical WEP bound pass",
            "current_evidence": "neither route closed",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3307_0",
            "question": "Did 3307 turn WEP anchors into a useful coupling model?",
            "answer": "yes, nonclaim",
            "reason": "Delta_Xi is now represented as source-coefficient vectors dotted into material charge contrasts for Ti/Pt and Be/Ti",
            "next_action": "derive or bound the source coefficients s_ik and the finite-mode range factors",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3307_1",
            "question": "Can MTS claim WEP/local source safety from this?",
            "answer": "no",
            "reason": "charge rows are proxy-level and source coefficients/ranges are missing",
            "next_action": "build the s_ik coefficient gate from the parent source projector or use WEP anchors to bound s_ik combinations",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3307_0_3308",
            "target_doc": "3308-Y5-R2FR-source-coefficient-sik-gate-or-WEP-linear-bound-runner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3308_source_coefficient_sik_gate_or_WEP_linear_bound_runner.py",
            "objective": "derive the source-charge coefficients s_ik from the parent projector, or build a linear WEP bound runner that constrains combinations of s_ik using the Ti/Pt and Be/Ti charge contrasts",
            "guardrails": "do not claim exact material composition from proxy rows; do not collapse scalar and spin-2 source coefficients without derivation",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_paths = [Path(row["path"]) for row in source_rows]
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    charge_basis = charge_basis_rows()
    materials = material_table_rows()
    pairs = pair_delta_rows()
    laws = delta_xi_law_rows()
    bounds = bound_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()

    checks = [
        (
            "VAL3307_0_sources_exist",
            "all cited source paths exist",
            all(path.exists() for path in source_paths),
            "",
        ),
        (
            "VAL3307_1_sources_parse",
            "all cited source paths parse",
            all(parse_ok(path) for path in source_paths),
            "",
        ),
        (
            "VAL3307_2_outputs_parse",
            "all 3307 non-validation output CSVs parse",
            all(csv_parse_ok(path) for path in output_paths),
            "",
        ),
        (
            "VAL3307_3_charge_basis_complete",
            "charge basis includes q_B, q_p, q_n, q_C, q_D",
            all(any(row["symbol"] == symbol for row in charge_basis) for symbol in ["q_B", "q_p", "q_n", "q_C", "q_D"]),
            "",
        ),
        (
            "VAL3307_4_materials_present",
            "proxy materials include Be, Ti, and Pt",
            all(any(row["element_proxy"] == element for row in materials) for element in ["Be", "Ti", "Pt"]),
            "",
        ),
        (
            "VAL3307_5_pair_deltas_present",
            "pair deltas cover Ti/Pt and Be/Ti anchors",
            all(any(anchor in row["anchor_id"] for row in pairs) for anchor in ["MICROSCOPE", "EOTWASH"]),
            "",
        ),
        (
            "VAL3307_6_deltaXi_laws_present",
            "DeltaXi laws cover scalar and spin2 source coefficients",
            any("Delta_Xi_0" in row["quantity"] and "s_0" in row["formula"] for row in laws)
            and any("Delta_Xi_2" in row["quantity"] and "s_2" in row["formula"] for row in laws),
            "",
        ),
        (
            "VAL3307_7_bound_rows_nonclaim",
            "bound rows exist and remain nonclaim",
            len(bounds) == 2 and all(row["valid_for_claim"] == "false" for row in bounds),
            "",
        ),
        (
            "VAL3307_8_runner_refuses_claim",
            "runner refuses WEP claim until coefficients/ranges/materials are filled",
            any(row["result"] == "REFUSE_CLAIM_SOURCE_COEFFICIENTS_MISSING" for row in runners),
            "",
        ),
        (
            "VAL3307_9_claim_gates_false",
            "all promotion gates remain false",
            all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in gates),
            "",
        ),
        (
            "VAL3307_10_next_target_sik",
            "next target is s_ik coefficient gate or WEP linear bound runner",
            "source-coefficient-sik" in next_rows[0]["target_doc"],
            "",
        ),
    ]

    formalization_after = snapshot_tree(FW)
    formalization_changed = changed_count(formalization_before, formalization_after)
    checks.append(
        (
            "VAL3307_11_formalization_untouched",
            "formalization-workbench modified-file count remains zero by this script",
            formalization_changed == 0,
            f"formalization_changed_count={formalization_changed}",
        )
    )

    overall = all(passed for _, _, passed, _ in checks)
    checks.append(
        (
            "VAL3307_12_overall",
            "3307 validation overall",
            overall,
            "all required checks passed" if overall else "one or more checks failed",
        )
    )

    return [
        {
            "check_id": check_id,
            "check": check,
            "passed": bool_str(passed),
            "detail": detail,
        }
        for check_id, check, passed, detail in checks
    ]


def render_doc() -> str:
    source_table = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` — exists={row['exists']}; role={row['role']}"
        for row in source_register_rows()
    )
    basis_table = "\n".join(
        f"- `{row['symbol']}`: {row['definition']} using `{row['proxy_formula']}`."
        for row in charge_basis_rows()
    )
    material_table = "\n".join(
        f"- `{row['material_id']}` {row['element_proxy']}: q_p={row['q_p']}, q_n={row['q_n']}, q_C={row['q_C']}, q_D={row['q_D']}."
        for row in material_table_rows()
    )
    pair_table = "\n".join(
        f"- `{row['pair_id']}`: Delta(q_B,q_p,q_n,q_C,q_D)=({row['Delta_q_B']},{row['Delta_q_p']},{row['Delta_q_n']},{row['Delta_q_C']},{row['Delta_q_D']})."
        for row in pair_delta_rows()
    )
    law_table = "\n".join(
        f"- `{row['law_id']}` `{row['quantity']}`: `{row['formula']}`"
        for row in delta_xi_law_rows()
    )
    bound_table = "\n".join(
        f"- `{row['bound_id']}`: `{row['test_body_pair']}` eta={row['eta_central']} sigma_proxy={row['eta_sigma_proxy']}; template `{row['bound_template']}`"
        for row in bound_rows()
    )
    runner_table = "\n".join(
        f"- `{row['runner_id']}`: `{row['result']}` — {row['detail']}"
        for row in runner_rows()
    )
    gate_table = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}"
        for row in promotion_gate_rows()
    )
    decision_table = "\n".join(
        f"- `{row['decision_id']}`: {row['answer']} — {row['reason']}"
        for row in decision_rows()
    )
    next_row = next_target_rows()[0]

    return f"""# 3307 - Material source-charge model for DeltaXi WEP bounds under AX1090

Run UTC: `{RUN_UTC}`

## Verdict

The WEP fallback now has a material-charge model.

For each finite mode,

`Delta_Xi_i[A,B] = s_iB Delta_q_B + s_ip Delta_q_p + s_in Delta_q_n + s_iC Delta_q_C + s_iD Delta_q_D + ...`.

This turns the coupling gap into a concrete object: either derive the source coefficients `s_ik` from the parent projector, or use WEP anchors to bound combinations of them.

The material rows are proxy rows only. They are useful for plumbing and scale checks, not publication claims, because exact alloy/isotope composition, source-body composition, ranges, mode strengths, and confidence conventions remain unresolved.

## Source Register

{source_table}

## Charge Basis

{basis_table}

## Material Proxy Charges

{material_table}

## Pair Charge Contrasts

{pair_table}

## DeltaXi Linear Laws

{law_table}

## Nonclaim WEP Bound Rows

{bound_table}

## Runner

{runner_table}

## Promotion Gates

{gate_table}

## Decision

{decision_table}

## Next Target

- `{next_row['target_doc']}`
- `{next_row['target_script']}`
- Objective: {next_row['objective']}
"""


def main() -> None:
    formalization_before = snapshot_tree(FW)

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["charge_basis"], charge_basis_rows())
    write_csv(OUTPUTS["material_table"], material_table_rows())
    write_csv(OUTPUTS["pair_deltas"], pair_delta_rows())
    write_csv(OUTPUTS["delta_xi_law"], delta_xi_law_rows())
    write_csv(OUTPUTS["bound_rows"], bound_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))

    if PYCACHE.exists():
        for child in PYCACHE.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(PYCACHE.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        PYCACHE.rmdir()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
