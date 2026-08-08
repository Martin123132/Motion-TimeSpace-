from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3830"
BRANCH = "MTS_R2FR_Y5_NO_SLIP_TRACELESS_IJ_SOURCE_CONDITION_OR_GAMMA_BOUND_SOURCE_3830"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3829 = PCW / "3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md"
CSV_3829_OWNER = OUT / "P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv"
CSV_3829_LOCK = OUT / "P8_Y5_R2FR_3829_SCALAR_LOCK_CONDITIONAL_THEOREM.csv"
CSV_3829_BOUNDS = OUT / "P8_Y5_R2FR_3829_GAMMA_BETA_COEFFICIENT_BOUND_ROWS.csv"
CSV_3829_BUDGET = OUT / "P8_Y5_R2FR_3829_SCALAR_RESIDUAL_BUDGET.csv"
CSV_3829_VALIDATION = OUT / "P8_Y5_BRR545_3829_VALIDATION.csv"
CSV_3825_BOUNDARY = OUT / "P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv"
CSV_3821_STRESS = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3830_SOURCE_REGISTER.csv",
    "operator": OUT / "P8_Y5_R2FR_3830_NO_SLIP_OPERATOR_THEOREM.csv",
    "source_decomposition": OUT / "P8_Y5_R2FR_3830_SLIP_SOURCE_DECOMPOSITION.csv",
    "gamma_bound": OUT / "P8_Y5_R2FR_3830_GAMMA_BOUND_SOURCE_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3830_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3830_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3830_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3830_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3830_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3830_0_3829_doc", P_3829, "Scalar Readout Lock Ct/Cs/Bt Owner Or Bound Fill"),
    ("SRC3830_1_3829_owner", CSV_3829_OWNER, "COEFF3829_3_S_slip"),
    ("SRC3830_2_3829_lock", CSV_3829_LOCK, "LOCK3829_1_gamma_no_slip"),
    ("SRC3830_3_3829_bounds", CSV_3829_BOUNDS, "BND3829_1_gamma"),
    ("SRC3830_4_3829_budget", CSV_3829_BUDGET, "RB3829_0_slip_anisotropic_stress"),
    ("SRC3830_5_3829_validation", CSV_3829_VALIDATION, "VAL3829_4_gamma_blocked_by_slip"),
    ("SRC3830_6_3825_boundary", CSV_3825_BOUNDARY, "BRT3825_2_B_zero_flux_zero"),
    ("SRC3830_7_3821_stress", CSV_3821_STRESS, "R3821_5_total"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_no_slip_traceless_ij_theorem_or_gamma_bound",
                "claim_use": "conditional_theorem_and_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def operator_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "operator_id": "NS3830_0_slip_definition",
            "object": "scalar slip",
            "statement": "Let S = Psi - Phi_s, where Psi=C_t Phi is the temporal scalar and Phi_s=C_s Phi is the spatial curvature scalar.",
            "equation": "S = (C_t - C_s) Phi + eps_slip",
            "zero_route": "S=0 implies C_s=C_t up to eps_slip/Phi",
            "current_status": "DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "NS3830_1_traceless_ij_operator",
            "object": "traceless spatial operator",
            "statement": "The scalar no-slip condition is controlled by the traceless spatial equation.",
            "equation": "D_TF[S] = (partial_i partial_j - delta_ij nabla^2/3)(Psi-Phi_s)",
            "zero_route": "D_TF[S]=0 plus boundary/harmonic silence gives S=0 by elliptic uniqueness on the exterior annulus.",
            "current_status": "CONDITIONAL_OPERATOR_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "NS3830_2_effective_source_equation",
            "object": "effective no-slip source",
            "statement": "Current MTS can only claim no slip if every effective traceless source term is zero or bounded.",
            "equation": "D_TF[S] = Sigma_TF_matter + Sigma_TF_parent_extra + Sigma_TF_boundary + Sigma_TF_readout",
            "zero_route": "all Sigma_TF terms vanish or the inverse-operator bound is below the gamma threshold",
            "current_status": "BLOCKED_SOURCE_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "NS3830_3_gamma_link",
            "object": "gamma residual",
            "statement": "Gamma is bounded by the normalized slip amplitude plus the explicit spatial residual from 3828/3829.",
            "equation": "abs(gamma-1) <= abs(S_slip/C_t) + abs(eps_spatial/Phi)",
            "zero_route": "S_slip=0 and eps_spatial/Phi -> 0",
            "current_status": "FIRST_NO_SLIP_BOUND_CONTRACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": "SLIP3830_0_matter_anisotropic",
            "symbol": "Sigma_TF_matter",
            "definition": "traceless anisotropic matter/source stress in the local exterior scalar equation",
            "zero_condition": "Pi_eff^TF=0 for the relevant compact exterior source and apparatus",
            "current_evidence": "3821 controls trace/virial stress but does not by itself prove traceless anisotropic silence",
            "bound_row": "B_gamma_matter_TF",
            "status": "MISSING_ANISOTROPIC_STRESS_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SLIP3830_1_parent_extra_scalar",
            "symbol": "Sigma_TF_parent_extra",
            "definition": "extra scalar/disformal/vector-tensor contribution that makes spatial and temporal scalar readouts differ",
            "zero_condition": "single metric readout with no representative scalar morphism or extra visible slip coefficient",
            "current_evidence": "not parent-signed in current corpus",
            "bound_row": "B_gamma_parent_extra",
            "status": "MISSING_SINGLE_METRIC_READOUT_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SLIP3830_2_boundary_harmonic",
            "symbol": "Sigma_TF_boundary",
            "definition": "homogeneous/harmonic scalar slip carried by boundary/reference data",
            "zero_condition": "3825 boundary/reference zero route closes for scalar slip mode",
            "current_evidence": "3825 gives conditional boundary-zero route but not a claim-valid scalar slip boundary row",
            "bound_row": "B_gamma_boundary",
            "status": "BOUNDARY_ROUTE_CONDITIONAL_NOT_CLOSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SLIP3830_3_readout_rep",
            "symbol": "Sigma_TF_readout",
            "definition": "representative/readout mismatch that maps the same parent scalar into different g00/gij coefficients",
            "zero_condition": "readout naturality locks scalar coefficients before arena projection",
            "current_evidence": "readout naturality not yet signed",
            "bound_row": "B_gamma_readout",
            "status": "MISSING_READOUT_NATURALITY_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SLIP3830_4_total",
            "symbol": "Sigma_TF_total",
            "definition": "total no-slip source driving S_slip",
            "zero_condition": "all four source terms above vanish on the same compact exterior domain",
            "current_evidence": "not claim-ready",
            "bound_row": "B_gamma_total",
            "status": "INTEGRATED_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gamma_bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "GB3830_0_inverse_operator",
            "observable": "S_slip",
            "bound_formula": "abs(S_slip/C_t) <= abs(G_TF^{-1} Sigma_TF_total)/(abs(C_t Phi)) + abs(H_boundary/Phi)",
            "required_source": "Sigma_TF_total, exterior Green/operator norm, boundary/harmonic amplitude",
            "status": "FORMULA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "GB3830_1_gamma_total",
            "observable": "gamma-1",
            "bound_formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "required_source": "four gamma source rows plus eps_spatial/Phi from 3828",
            "status": "FIRST_GAMMA_SOURCE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "GB3830_2_no_slip_zero",
            "observable": "gamma-1 zero route",
            "bound_formula": "if Sigma_TF_total=0, H_boundary=0, and eps_spatial/Phi=0 then gamma-1=0",
            "required_source": "anisotropic stress silence, parent extra silence, boundary zero, readout naturality",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3830_0_operator_route",
            "gate": "no-slip operator route formulated",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "claim_allowed": False,
            "reason": "D_TF[S] equation and elliptic uniqueness route are explicit",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3830_1_gamma_zero",
            "gate": "gamma zero/no-slip claim",
            "status": "BLOCKED_SOURCE_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "reason": "Sigma_TF_matter, parent extra, boundary, and readout source terms are not all zero-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3830_2_gamma_bound",
            "gate": "gamma finite bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "bound formula exists but no numeric/source-backed rows yet",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3830_3_local_GR",
            "gate": "local GR scalar readout claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "gamma no-slip source terms and beta second-order vertex remain open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3830_4_next_target",
            "gate": "next target attacks anisotropic stress/source silence",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "Sigma_TF_matter is the first source term in the no-slip chain",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3830_0_no_slip_route_real",
            "decision": "the gamma lock now has a real field-equation route",
            "basis": "D_TF[S]=Sigma_TF_total plus boundary uniqueness is the standard no-slip structure",
            "consequence": "future work should fill or prove the source terms rather than rename C_s=C_t as an axiom",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3830_1_trace_not_enough",
            "decision": "stress-virial trace cancellation is not enough to prove no slip",
            "basis": "gamma needs traceless anisotropic stress silence, not only integrated trace/pressure cancellation",
            "consequence": "3831 must target Sigma_TF_matter or keep gamma as a bound row",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3830_2_EM_not_shortcut",
            "decision": "EM/Poynting stress should enter as part of Sigma_TF_total if used",
            "basis": "wave/Poynting stresses can source anisotropic/traceless terms unless parent coupling cancels them",
            "consequence": "EM insight is preserved, but it cannot bypass the local no-slip gate",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3830_0",
            "next_checkpoint": "3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md",
            "script": "scripts/Y5_R2FR_3831_effective_anisotropic_stress_silence_or_SigmaTF_bound_fill.py",
            "objective": "try to prove Sigma_TF_matter=0 or source-bound it for compact exterior local tests, distinguishing stress trace/virial cancellation from traceless anisotropic stress silence",
            "reason": "3830 shows no-slip/gamma recovery fails or survives on the effective traceless stress source first",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_NO_SLIP_OPERATOR_BOUND",
            "claim": "no gamma/local-GR/Newton claim",
            "summary": "3830 derives the no-slip operator route, decomposes Sigma_TF_total source terms, and emits first gamma source-bound rows.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    operator: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    gamma_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3830 — No-Slip Traceless-ij Source Condition Or Gamma Bound Source

Private checkpoint. This tries the `S_slip=0` derivation route exposed by 3829. It does not claim `gamma=1`.

Generated: `{timestamp}`

## Result

3830 turns the gamma lock into a field-equation condition:

`D_TF[S] = (partial_i partial_j - delta_ij nabla^2/3)(Psi-Phi_s)`

`D_TF[S] = Sigma_TF_matter + Sigma_TF_parent_extra + Sigma_TF_boundary + Sigma_TF_readout`.

If the right-hand side vanishes and the boundary/harmonic mode is silent, elliptic uniqueness on the exterior annulus gives `S=0`, hence `C_s=C_t` and `gamma -> 1`.

Current result: no-slip is formulated, not closed. The useful gamma bound is:

`abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## No-Slip Operator Theorem

{markdown_table(operator, ["operator_id", "object", "equation", "zero_route", "current_status"])}

## Slip Source Decomposition

{markdown_table(decomposition, ["source_id", "symbol", "definition", "zero_condition", "status"])}

## Gamma Bound Rows

{markdown_table(gamma_bounds, ["bound_id", "observable", "bound_formula", "required_source", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is the right kind of narrowing: `gamma` is not merely “missing”; it is now exactly a no-slip source problem. The next proof must show whether the effective traceless stress source vanishes or is bounded. Stress-virial trace cancellation helps the active-mass route, but it is not enough by itself for `gamma`; we need traceless anisotropic silence.

Next target: `3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3829", "Current State After 3830", 1)
    paragraph = (
        "`3830` formulates the actual no-slip/gamma route: with `S=Psi-Phi_s`, "
        "`D_TF[S]=(partial_i partial_j-delta_ij nabla^2/3)(Psi-Phi_s)=Sigma_TF_matter+Sigma_TF_parent_extra+Sigma_TF_boundary+Sigma_TF_readout`. "
        "If those sources and the harmonic boundary mode vanish, elliptic uniqueness gives `S=0`, hence `C_s=C_t` and `gamma -> 1`. "
        "The current corpus does not yet sign the effective traceless-stress silence, so 3830 emits the first gamma source-bound row instead of claiming no slip.\n\n"
    )
    anchor = "`3829` reduces"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md`

Target: try to prove `S_slip=0` from the traceless spatial field equation, no anisotropic stress, fixed boundary, and single metric readout; otherwise emit source-backed `gamma` bound rows.

This is the best next move because 3829 reduces the `gamma` lock `C_s=C_t` to the no-slip residual `S_slip`, which is the cleanest linear derivation route toward local GR."""
    new_gate = """`3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md`

Target: try to prove `Sigma_TF_matter=0` or source-bound it for compact exterior local tests, distinguishing stress trace/virial cancellation from traceless anisotropic stress silence.

This is the best next move because 3830 shows no-slip/gamma recovery fails or survives on the effective traceless stress source first."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3830_NO_SLIP_OPERATOR_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3830_SLIP_SOURCE_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3830_GAMMA_BOUND_SOURCE_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3830_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3830_NO_SLIP_OPERATOR_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3830 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3830 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    operator: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    gamma_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in operator + decomposition + gamma_bounds + gates)
    add(
        "VAL3830_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3830_1_operator",
        "D_TF no-slip operator and source equation are present",
        all(token in all_text for token in ["D_TF", "Sigma_TF_total", "Psi-Phi_s"]),
        "operator tokens present",
    )
    add(
        "VAL3830_2_source_decomposition",
        "matter, parent-extra, boundary, and readout slip sources are decomposed",
        all(token in all_text for token in ["Sigma_TF_matter", "Sigma_TF_parent_extra", "Sigma_TF_boundary", "Sigma_TF_readout"]),
        f"{len(decomposition)} decomposition rows",
    )
    add(
        "VAL3830_3_gamma_bound",
        "gamma source-bound row exists",
        any(row["bound_id"] == "GB3830_1_gamma_total" for row in gamma_bounds),
        f"{len(gamma_bounds)} gamma bound rows",
    )
    add(
        "VAL3830_4_nonclaim",
        "all no-slip rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in operator + decomposition + gamma_bounds + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3830_5_gamma_blocked",
        "gamma zero claim remains blocked",
        any(row["gate_id"] == "GATE3830_1_gamma_zero" and row["status"] == "BLOCKED_SOURCE_SIGNATURE_REQUIRED" for row in gates),
        "gamma no-slip source signature required",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3830_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3830_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "Sigma_TF_matter" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3830*", "P8_Y5_BRR545_3830*", "*Y5_R2FR_3830*", "3830-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3830_8_formalization_clean",
        "formalization-workbench has no 3830 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3830 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3830_9_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    operator = operator_rows(timestamp)
    decomposition = source_decomposition_rows(timestamp)
    gamma_bounds = gamma_bound_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["operator"], operator)
    write_csv(OUTPUTS["source_decomposition"], decomposition)
    write_csv(OUTPUTS["gamma_bound"], gamma_bounds)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, operator, decomposition, gamma_bounds, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, operator, decomposition, gamma_bounds, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_NO_SLIP_OPERATOR_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
