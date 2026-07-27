from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3316-Y5-R2FR-parent-quadratic-hessian-readout-extraction-for-ZiUi-under-AX1090.md"

SRC_ACTION_1 = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_ACTION_2 = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

SOURCES = [
    {
        "source_id": "SRC3316_0_3315_doc",
        "path": ROOT / "3315-Y5-R2FR-parent-residue-readout-source-theorem-for-Ai-and-sik-under-AX1090.md",
        "role": "3315 dust-source theorem and A_i split",
    },
    {
        "source_id": "SRC3316_1_3315_factor",
        "path": OUT / "P8_Y5_R2FR_3315_FACTOR_SPLIT_RESULT.csv",
        "role": "Z_i U_i identified as top residue/readout factor",
    },
    {
        "source_id": "SRC3316_2_3315_theorem",
        "path": OUT / "P8_Y5_R2FR_3315_PARENT_SOURCE_THEOREM_ATTEMPT.csv",
        "role": "Hilbert source variation and dust-limit proof",
    },
    {
        "source_id": "SRC3316_3_fundamental_action",
        "path": SRC_ACTION_1,
        "role": "macroscopic MTS-Einstein action and microscopic psi action source",
    },
    {
        "source_id": "SRC3316_4_motion_action",
        "path": SRC_ACTION_2,
        "role": "MTS action-principle variation source",
    },
    {
        "source_id": "SRC3316_5_1036_quadratic",
        "path": ROOT / "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
        "role": "previous finite-X quadratic action contract and beta split",
    },
    {
        "source_id": "SRC3316_6_1042_nohair",
        "path": ROOT / "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
        "role": "positive operator/no-hair identity and unsigned Hessian premise gates",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3316_SOURCE_REGISTER.csv",
    "scan": OUT / "P8_Y5_R2FR_3316_CORPUS_OPERATOR_SCAN.csv",
    "derivation": OUT / "P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv",
    "contract": OUT / "P8_Y5_R2FR_3316_RESIDUE_EXTRACTION_CONTRACT.csv",
    "factor_update": OUT / "P8_Y5_R2FR_3316_A_FACTOR_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3316_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3316_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3316_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3316_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

SCAN_PATTERNS = [
    "quadratic",
    "Hessian",
    "kinetic operator",
    "propagator",
    "residue",
    "canonical",
    "linearized",
    "L_MTS",
    "L_{",
    "Einstein",
    "matter",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1000) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def first_hits(path: Path, patterns: list[str], max_hits: int = 6) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return ""
    hits: list[str] = []
    lowered = [(pattern, pattern.lower()) for pattern in patterns]
    for index, line in enumerate(lines, start=1):
        lower_line = line.lower()
        if any(pattern_lower in lower_line for _, pattern_lower in lowered):
            hits.append(f"L{index}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        hits = first_hits(path, SCAN_PATTERNS)
        text = ""
        if path.exists() and path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
        has_hessian = "Hessian" in text or "quadratic Hessian" in text
        has_explicit_matrix = ("H_AB" in text or "operator matrix" in text or "kinetic matrix" in text) and (
            "delta^2" in text or "second variation" in text or "quadratic" in text
        )
        has_public_readout_map = "g_pub" in text or "public metric" in text or "observed/public metric" in text
        rows.append(
            {
                "scan_id": f"SCAN3316_{len(rows)}",
                "source_id": source["source_id"],
                "path": str(path),
                "has_hessian_language": bool_str(has_hessian),
                "has_claim_grade_operator_matrix": bool_str(has_explicit_matrix),
                "has_public_readout_map_language": bool_str(has_public_readout_map),
                "evidence_hits": hits,
                "scan_verdict": "operator_contract_or_context" if has_hessian or has_public_readout_map else "context_only",
                "valid_for_claim": "false",
            }
        )
    return rows


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "HDR3316_0_linearize_parent",
            "claim": "The needed object is the quadratic Hessian of the parent fields, not separate fitted Z_i and U_i labels.",
            "formula": "S_2 = 1/2 int Phi^A H_AB(k) Phi^B + 1/2 int T^{mu nu} R_{mu nu,A}(k) Phi^A",
            "meaning": "H_AB is the second variation of the parent action; R_{mu nu,A}=delta g_pub_mu_nu/delta Phi^A is the public metric readout map.",
            "status": "FORMULA_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HDR3316_1_integrate_fields",
            "claim": "The observable two-source exchange is controlled by the public metric propagator.",
            "formula": "G_pub_{mu nu alpha beta}(k)=R_{mu nu,A}(k) [H^{-1}(k)]^{AB} R_{alpha beta,B}(k)",
            "meaning": "This is the invariant replacement for chasing Z_i and U_i separately.",
            "status": "FORMULA_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HDR3316_2_spin_project",
            "claim": "Finite scalar/spin2 amplitudes are pole residues of G_pub in the relevant spin projectors.",
            "formula": "G_pub(k)=G_N P^(2)/k^2 + sum_i B_i P_i/(k^2+m_i^2) + analytic/contact terms",
            "meaning": "B_i is the field-redefinition-invariant residue/readout product equivalent to Z_i U_i in the 3315 split law.",
            "status": "FORMULA_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HDR3316_3_residue_ratio",
            "claim": "The normalized local fifth-force amplitude is a residue ratio against the massless Newton pole.",
            "formula": "B_i = Res_{k^2=-m_i^2}[T_s G_pub T_t]_i / Res_{k^2=0}[T_s G_pub T_t]_{massless}",
            "meaning": "This fixes sign and normalization convention before any empirical fit.",
            "status": "FORMULA_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "HDR3316_4_no_field_redefinition_leak",
            "claim": "B_i is invariant under nonsingular field redefinitions Phi -> M Phi.",
            "formula": "H -> M^T H M, R -> R M, so R H^{-1} R^T is unchanged.",
            "meaning": "This prevents a fake proof from moving the coupling between Z_i and U_i by notation.",
            "status": "GUARDRAIL_DERIVED",
            "valid_for_claim": "false",
        },
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CON3316_0_field_basis",
            "needed_object": "Phi^A field vector and background Phi_0",
            "required_content": "declared perturbation fields including metric/coframe, psi/Gamma sector, finite residual fields, gauge constraints",
            "current_status": "MISSING_CLAIM_GRADE_FIELD_VECTOR",
            "why_needed": "H_AB cannot be formed without the variables being varied",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3316_1_hessian",
            "needed_object": "H_AB(k)",
            "required_content": "second variation of S_parent around the local GR/Newton branch, including gauge fixing or constraint reduction",
            "current_status": "MISSING_EXPLICIT_OPERATOR_MATRIX",
            "why_needed": "residues, ghost signs, pole masses, and ranges come from det H_AB(k)",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3316_2_readout",
            "needed_object": "R_{mu nu,A}(k)",
            "required_content": "linear public metric/coframe readout map from parent variables to observed rods/clocks/free-fall metric",
            "current_status": "MISSING_EXPLICIT_PUBLIC_READOUT_MATRIX",
            "why_needed": "even a valid Hessian is not enough unless ordinary matter sees this readout",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3316_3_residue",
            "needed_object": "B_i residue/readout product",
            "required_content": "spin-projected pole residues of R H^{-1} R^T normalized to the massless Newton pole",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "why_needed": "B_i replaces the old separate Z_i U_i ambiguity",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CON3316_4_local_GR_branch",
            "needed_object": "local decoupling/no-pole/screening condition",
            "required_content": "B_i=0, m_i large, source residual zero, or nonlinear screening/no-hair theorem in the local branch",
            "current_status": "NOT_CLOSED",
            "why_needed": "local GR requires finite modes to be absent, suppressed, or bounded",
            "valid_for_claim": "false",
        },
    ]


def factor_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor_id": "AFU3316_0_scalar",
            "old_law": "A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)]",
            "new_invariant_law": "A_0 = (1/3) B_0 [1 + epsilon_0(Earth)], where B_0 = scalar pole residue of R H^{-1} R^T normalized to the Newton pole",
            "status": "INVARIANT_FORMULA_DERIVED_NUMERIC_VALUE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "AFU3316_1_spin2",
            "old_law": "A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)]",
            "new_invariant_law": "A_2 = (-4/3) B_2 [1 + epsilon_2(Earth)], where B_2 = massive spin-2 pole residue of R H^{-1} R^T normalized to the Newton pole",
            "status": "INVARIANT_FORMULA_DERIVED_NUMERIC_VALUE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "AFU3316_2_zero_condition",
            "old_law": "Z_i U_i small/zero by assumption or closure",
            "new_invariant_law": "A finite mode is locally safe only if B_i=0, m_i r_local >> 1, its source residual vanishes, or a parent nonlinear screening/no-hair theorem applies",
            "status": "LOCAL_GR_GATE_SHARPENED",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(scan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    has_operator = any(row["has_claim_grade_operator_matrix"] == "true" for row in scan)
    return [
        {
            "gate_id": "GATE3316_0_formula",
            "claim": "invariant Hessian/readout residue formula is derived",
            "passed": "true",
            "reason": "R H^{-1} R^T and residue-ratio expression are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3316_1_operator_matrix",
            "claim": "current corpus supplies claim-grade H_AB(k)",
            "passed": bool_str(has_operator),
            "reason": "scan found explicit operator matrix" if has_operator else "scan found action language/contracts but no explicit local quadratic operator matrix",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3316_2_numeric_Bi",
            "claim": "B_0 and B_2 can be numerically/sign-evaluated",
            "passed": "false",
            "reason": "requires H_AB(k), R map, spin projectors, pole locations, and gauge reduction",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3316_3_local_GR",
            "claim": "local GR/Newton limit follows",
            "passed": "false",
            "reason": "needs B_i zero/suppression or screened/no-hair branch plus residual bounds",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3316_0",
            "question": "Did 3316 move the coupling problem forward?",
            "answer": "yes: it replaces separate Z_i and U_i with invariant pole residues B_i of R H^{-1} R^T",
            "reason": "that object is unchanged by field redefinitions and is exactly what local tests see",
            "next_action": "try to build the minimal local quadratic operator from the existing MTS action terms",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3316_1",
            "question": "Can the current corpus already evaluate B_0/B_2?",
            "answer": "not yet",
            "reason": "the action files give EH + curvature-exchange/microscopic psi structure, but not a fully reduced local Hessian/readout matrix with finite pole locations",
            "next_action": "construct a minimal symbolic Hessian ansatz and test the GR limit conditions instead of writing another missing ledger",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3316_2",
            "question": "What would count as a real local-GR leap?",
            "answer": "prove B_i=0/no finite pole in the local branch, prove m_i is too short-range, or prove a positive no-hair/screening identity",
            "reason": "any of those makes the finite sector harmless without pretending G_cal absorbed it",
            "next_action": "3317 should build and stress-test the minimal symbolic Hessian/no-pole branch",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3317-Y5-R2FR-minimal-symbolic-hessian-no-pole-or-finite-residue-branch-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3317_minimal_symbolic_hessian_no_pole_or_finite_residue_branch.py",
            "objective": "construct the least-assumption local quadratic Hessian/readout ansatz compatible with the MTS action language and test whether finite scalar/spin2 poles are absent, constrained, or retained as B_i envelopes",
            "must_include": "field vector, gauge/constraint split, H_AB(k), R map, determinant/pole test, residue sign, local-GR gate, no absorption into G_cal, fallback B_i envelope rows",
            "fallback_if_failed": "retain B_0/B_2 as bounded empirical amplitudes and proceed to residual epsilon/EM-Poynting bounds",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    scan = scan_rows()
    derivation = derivation_rows()
    factors = factor_update_rows()
    gates = gate_rows(scan)
    next_rows = next_target_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3316_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3316_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3316_2_outputs_parse",
            "check": "all 3316 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3316_3_propagator_formula",
            "check": "R H^{-1} R^T formula is present",
            "passed": any("H^{-1}" in row["formula"] and "R" in row["formula"] for row in derivation),
            "detail": "",
        },
        {
            "check_id": "VAL3316_4_residue_ratio",
            "check": "residue ratio formula is present",
            "passed": any("Res_{k^2=-m_i^2}" in row["formula"] for row in derivation),
            "detail": "",
        },
        {
            "check_id": "VAL3316_5_invariant_Bi_update",
            "check": "A0/A2 laws are updated to B0/B2",
            "passed": any("B_0" in row["new_invariant_law"] for row in factors)
            and any("B_2" in row["new_invariant_law"] for row in factors),
            "detail": "",
        },
        {
            "check_id": "VAL3316_6_no_numeric_claim",
            "check": "numeric B_i and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3316_2_numeric_Bi", "GATE3316_3_local_GR"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3316_7_next_symbolic_hessian",
            "check": "next target is minimal symbolic Hessian/no-pole branch",
            "passed": any("minimal-symbolic-hessian-no-pole" in row["target_doc"] for row in next_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3316_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3316_9_overall",
            "check": "3316 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for row in checks:
        row["passed"] = bool_str(bool(row["passed"]))
    return checks


def render_doc() -> str:
    sources = source_register_rows()
    scan = scan_rows()
    derivation = derivation_rows()
    contract = contract_rows()
    factors = factor_update_rows()
    gates = gate_rows(scan)
    decisions = decision_rows()
    next_rows = next_target_rows()
    lines: list[str] = [
        "# 3316 - Parent quadratic Hessian/readout extraction for ZiUi under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3316 sharpens the coupling problem again.",
        "",
        "The separate symbols `Z_i` and `U_i` are not the safest primitive. The claim-grade object is the public metric propagator residue:",
        "",
        "`G_pub = R H^{-1} R^T`",
        "",
        "where `H` is the parent quadratic Hessian and `R` is the public metric/readout map. The finite-mode amplitude is the pole residue of this object, normalized to the massless Newton pole. I label that invariant product `B_i`.",
        "",
        "So the 3315 split becomes:",
        "",
        "`A_0 = (1/3) B_0 [1 + epsilon_0(Earth)]`",
        "",
        "`A_2 = (-4/3) B_2 [1 + epsilon_2(Earth)]`",
        "",
        "This is progress because `B_i` cannot be moved around by a field redefinition. The corpus has action language and prior quadratic contracts, but not yet the explicit local `H_AB(k)` and `R` matrices needed to evaluate `B_0` or `B_2`.",
        "",
        "## Source Register",
        "",
    ]
    for row in sources:
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}"
        )
    lines.extend(["", "## Corpus Operator Scan", ""])
    for row in scan:
        lines.append(
            f"- `{row['scan_id']}` `{row['source_id']}`: operator_matrix={row['has_claim_grade_operator_matrix']}; public_readout={row['has_public_readout_map_language']}; verdict={row['scan_verdict']}; hits={row['evidence_hits']}"
        )
    lines.extend(["", "## Hessian Readout Derivation", ""])
    for row in derivation:
        lines.append(f"- `{row['step_id']}` `{row['status']}`: {row['claim']} Formula: `{row['formula']}` Meaning: {row['meaning']}")
    lines.extend(["", "## Residue Extraction Contract", ""])
    for row in contract:
        lines.append(
            f"- `{row['contract_id']}` `{row['needed_object']}`: {row['current_status']}. Needed: {row['required_content']}. Why: {row['why_needed']}."
        )
    lines.extend(["", "## A Factor Update", ""])
    for row in factors:
        lines.append(f"- `{row['factor_id']}` `{row['status']}`: {row['new_invariant_law']}")
    lines.extend(["", "## Promotion Gates", ""])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}; reason={row['reason']}")
    lines.extend(["", "## Decision", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['answer']} - {row['reason']} Next: {row['next_action']}.")
    lines.extend(["", "## Next Target", ""])
    for row in next_rows:
        lines.append(f"- `{row['target_doc']}`")
        lines.append(f"- `{row['target_script']}`")
        lines.append(f"- Objective: {row['objective']}")
        lines.append(f"- Fallback: {row['fallback_if_failed']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    scan = scan_rows()
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["scan"], scan)
    write_csv(OUTPUTS["derivation"], derivation_rows())
    write_csv(OUTPUTS["contract"], contract_rows())
    write_csv(OUTPUTS["factor_update"], factor_update_rows())
    write_csv(OUTPUTS["gates"], gate_rows(scan))
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
