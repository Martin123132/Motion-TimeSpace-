from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3669"
BRANCH_ID = "MTS_R2FR_Y5_KH_HESSIAN_STF_PARENT_OWNER_OR_LINEAR_GAMMA_BOUND_ROW_3669"
DOC = ROOT / "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3668", RESIDUALS / "P8_Y5_R2FR_3668_NEXT_TARGET.csv", "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md", "3668 selected this target"),
        ("doc_3668", ROOT / "3668-Y5-R2FR-kH-kG-weak-field-projection-zero-or-transfer-kernel-bound.md", "k_H` piece is linear", "3668 kH/kG hierarchy"),
        ("derivation_3668", RESIDUALS / "P8_Y5_R2FR_3668_KH_KG_PROJECTION_DERIVATION_ROWS.csv", "LINEAR_KH_AND_QUADRATIC_KG_SPLIT_DERIVED", "projection normal form"),
        ("kernels_3668", RESIDUALS / "P8_Y5_R2FR_3668_KERNEL_COEFFICIENT_ROWS.csv", "KCR3668_2_kH", "kH blocker row"),
        ("bounds_3668", RESIDUALS / "P8_Y5_R2FR_3668_REDUCED_BOUND_INTERFACE_ROWS.csv", "RB3668_lambda_over_r_1", "reduced muH/muG bound rows"),
        ("doc_3657", ROOT / "3657-Y5-R2FR-S_TF_MTS-zero-proof-or-gamma-coefficient-bound.md", "radial gradients can source STF slip", "STF counterexample"),
        ("profile_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "GPC3658_2_Yukawa_like_profile", "Hessian-STF kernel"),
        ("common_mode_3060", RESIDUALS / "P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv", "CONDITIONAL_NOT_SIGNED", "common-mode gamma cancellation attempt"),
        ("weak_response_2477", ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "weak-field metric-response factorisation"),
        ("cmetric_2477", RESIDUALS / "P8_Y5_WEAK_FIELD_RESPONSE_2477_CMETRIC_FACTORISATION.csv", "CM2477_2_Cobs", "observable projection factor"),
        ("frame_leak_1027", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "disformal", "disformal/frame leakage counterexamples"),
        ("metric_inputs_3384", RESIDUALS / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv", "MRI3384_1_Cmetric", "PPN metric response input blockers"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def kh_zero_audit_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "audit_id": "KHZ3669_0_operator_form",
            "clause": "linear Hessian-STF channel definition",
            "statement": "The linear channel is the coefficient multiplying P_TF[partial_i partial_j X] in the weak-field trace-free spatial equation.",
            "formula": "S_TF^X|linear = k_H P_TF[partial_i partial_j X]",
            "status": "DEFINITION_LOCKED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "audit_id": "KHZ3669_1_common_mode_sufficient",
            "clause": "common-mode trace response",
            "statement": "If the extra X response enters only as a common trace/source normalization in the same observed frame, then it changes Phi and Psi together and has no Hessian-STF slip.",
            "formula": "delta E_ij^X = delta_ij F_X + common EH source rescaling => P_TF(delta E_ij^X)=0 => k_H=0",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "audit_id": "KHZ3669_2_nonminimal_counterterm",
            "clause": "nonminimal Hessian counterexample",
            "statement": "A scalar nonminimal/metric response can produce terms of the form nabla_i nabla_j F_X - delta_ij nabla^2 F_X/3, which is exactly a Hessian-STF source.",
            "formula": "P_TF[nabla_i nabla_j F_X] != 0 for a nonconstant radial F_X",
            "status": "COUNTERMODEL_LIVE",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "audit_id": "KHZ3669_3_disformal_counterterm",
            "clause": "disformal/frame counterexample",
            "statement": "A shadow/disformal matter or readout frame can create direction-dependent spatial response even when ordinary matter looks isotropic.",
            "formula": "g_m=A(X)^2 g_obs + B(X) U_i U_j or derivative-frame terms => P_TF(delta g_ij) may survive",
            "status": "COUNTERMODEL_LIVE",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "audit_id": "KHZ3669_4_boundary_readout",
            "clause": "boundary/readout STF silence",
            "statement": "Even k_H=0 does not close gamma unless boundary/readout/source STF floors are zero or bounded.",
            "formula": "delta_gamma = C_H mu_H + C_G mu_G + C_other_gamma",
            "status": "FLOOR_TERMS_RETAINED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "audit_id": "KHZ3669_5_verdict",
            "clause": "k_H zero status",
            "statement": "Current MTS does not parent-sign common-mode EH dominance, no nonminimal Hessian response, no disformal/readout frame, and STF boundary silence together.",
            "formula": "k_H=0 not accepted; build linear mu_H bound row",
            "status": "ZERO_NOT_CLOSED_LINEAR_BOUND_REQUIRED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def kh_parent_owner_requirements(ts: str) -> list[dict[str, object]]:
    specs = [
        ("KHO3669_0_same_frame", "same observed local frame", "Phi/Psi, source, readout, and boundary are expressed in one observed coframe", "UNSIGNED", "frame mixing can mimic gamma slip"),
        ("KHO3669_1_EH_common_mode", "EH common-mode response", "X-induced source normalization rescales temporal and spatial weak-field equations together", "CONDITIONAL_NOT_SIGNED", "k_S-k_T can be nonzero"),
        ("KHO3669_2_no_nonminimal_Hessian", "no nonminimal Hessian-STF operator", "parent action excludes F(X)R or equivalent Hessian-STF metric-response terms unless bounded", "UNSIGNED_COUNTERMODEL_LIVE", "P_TF[nabla_i nabla_j F_X] sources k_H"),
        ("KHO3669_3_no_disformal", "no disformal/readout frame", "parent action excludes B(X)U_muU_nu or derivative frame terms in rods/clocks/light propagation", "UNSIGNED_COUNTERMODEL_LIVE", "directional response can survive common Weyl silence"),
        ("KHO3669_4_boundary_readout_silence", "boundary/readout/source STF floors zero", "C_other_gamma is zero or separately bounded", "MISSING_COMPONENT_BOUNDS", "k_H bound cannot be claimed as total gamma score"),
        ("KHO3669_5_transfer_kernel", "K_gamma_H transfer kernel", "local Hessian-STF coefficient is mapped to the Cassini/Shapiro observable", "MISSING_TRANSFER_KERNEL", "mu_H bound remains scale-proxy/nonclaim"),
    ]
    return [
        {
            **base(ts),
            "requirement_id": req_id,
            "requirement": requirement,
            "definition": definition,
            "current_status": status,
            "blocks_if_missing": blocks,
            "claim_allowed": False,
        }
        for req_id, requirement, definition, status, blocks in specs
    ]


def linear_muH_bound_rows(ts: str) -> list[dict[str, object]]:
    rows = []
    for source in load_csv(RESIDUALS / "P8_Y5_R2FR_3668_REDUCED_BOUND_INTERFACE_ROWS.csv"):
        c_h = float(source["C_H_proxy"])
        cassini = 2.3e-05
        # Source rows already contain the same value, but use the explicit Cassini constant here
        # so the row is robust to text-formula parsing.
        mu_h_max = math.inf if c_h <= 0.0 else cassini / c_h
        rows.append(
            {
                **base(ts),
                "row_id": source["row_id"].replace("RB3668", "LMH3669"),
                "lambda_over_r_proxy": source["lambda_over_r_proxy"],
                "C_H_proxy": source["C_H_proxy"],
                "linear_bound_formula": f"mu_H <= {mu_h_max:.12e} if mu_G=0 and C_other_gamma=0",
                "mu_H_max_if_muG_Cother_zero": f"{mu_h_max:.12e}",
                "mu_H_definition": "mu_H=|K_gamma_H(lambda,b,path) k_H f_EM/Z_X|",
                "required_for_claim": "K_gamma_H transfer kernel; k_H parent coefficient or bound; Z_X normalization; f_EM zero/value; C_other_gamma bound; non-EM source floors",
                "current_status": "LINEAR_MUH_BOUND_ROW_SCALE_PROXY_NONCLAIM",
                "why_nonclaim": "inherits 3668 solar-limb scale proxy and assumes mu_G=C_other=0 for isolation; transfer kernel and parent coefficient are missing",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def countermodel_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "countermodel_id": "CE3669_0_FR_like",
            "name": "nonminimal scalar-curvature response",
            "formula": "DeltaS ~ int sqrt(-g) F(X) R",
            "effect": "variation contains nabla_i nabla_j F - g_ij box F; its trace-free spatial part is k_H-like",
            "must_exclude_or_bound": "no F(X)R/nonminimal Hessian response in selected parent branch",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "countermodel_id": "CE3669_1_disformal",
            "name": "disformal readout/matter frame",
            "formula": "g_m=A(X)^2 g_obs + B(X) U_mu U_nu",
            "effect": "directional spatial response can contribute to gamma/readout STF even under spherical matter source",
            "must_exclude_or_bound": "no-shadow/no-disformal theorem or b_dis bound row",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "countermodel_id": "CE3669_2_boundary_readout",
            "name": "boundary/readout STF floor",
            "formula": "C_other_gamma=|C_boundary|+|C_readout|+|C_source|+|C_nonEH_other|",
            "effect": "can saturate Cassini gamma even if k_H is zero",
            "must_exclude_or_bound": "component floor zero theorem or finite bound rows",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3669_0_kH_zero", "k_H=0 theorem", "FAILED_UNSIGNED_COUNTERMODELS_LIVE", "nonminimal Hessian, disformal/readout, common-mode, and boundary clauses not signed together"),
        ("CG3669_1_common_mode", "common-mode sufficient route", "PASSED_CONDITIONAL_DERIVATION", "if X response is trace/common-mode in same frame, k_H vanishes"),
        ("CG3669_2_countermodels", "countermodel audit", "PASSED_GUARDRAIL", "F(X)R, disformal frame, and C_other floors retained"),
        ("CG3669_3_linear_bound", "linear mu_H bound rows", "PASSED_NONCLAIM_INTERFACE", "mu_H rows generated from 3668 reduced bound grid"),
        ("CG3669_4_gamma_claim", "Cassini gamma/local-GR claim", "ACTIVE_GUARD", "no transfer kernel or parent k_H coefficient; no gamma pass"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "KH_ZERO_UNSIGNED_LINEAR_MUH_BOUND_ROWS_STAGED_NONCLAIM",
            "summary": "3669 derives the sufficient k_H=0 condition: X must enter the weak-field metric response only as same-frame trace/common-mode response. It refuses the zero because nonminimal Hessian, disformal/readout, and boundary-floor countermodels remain live, then stages isolated linear mu_H bound rows.",
            "claim_ceiling": "no k_H zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The next best target is K_gamma_H: without a transfer/readout kernel, the linear mu_H bound remains only a solar-limb scale-proxy interface.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3669_0",
            "target_doc": "3670-Y5-R2FR-KgammaH-transfer-kernel-or-conservative-linear-bound.md",
            "target_script": "scripts/Y5_R2FR_3670_KgammaH_transfer_kernel_or_conservative_linear_bound.py",
            "objective": "derive the Hessian-STF transfer/readout kernel K_gamma_H for the Cassini/Shapiro observable, or define a conservative nonclaim bound convention for the linear mu_H branch",
            "success_gate": "mu_H has a transfer-kernel row that is either parent/readout-derived or explicitly conservative and nonclaim, with k_H/f_EM/Z_X blockers preserved",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    requirements: list[dict[str, object]],
    bounds: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(bounds, key=lambda row: float(row["mu_H_max_if_muG_Cother_zero"]))
    lines = [
        "# 3669 - kH Hessian-STF parent owner or linear gamma bound row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "`k_H` is the linear Hessian-STF leakage coefficient:",
        "",
        "`S_TF^X|linear = k_H P_TF[partial_i partial_j X]`.",
        "",
        "A clean zero route exists only if the parent weak-field response is trace/common-mode in the same observed frame, with no nonminimal Hessian, disformal/readout, or boundary/source STF floor. Current files do not sign that package, so `k_H=0` is not claimed.",
        "",
        "The fallback progress is an isolated linear bound interface:",
        "",
        "`mu_H = |K_gamma_H(lambda,b,path) k_H f_EM/Z_X|`.",
        "",
        f"Strongest sampled scale-proxy row: `{strongest['row_id']}` with `{strongest['linear_bound_formula']}`.",
        "",
        "## kH zero audit",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Parent-owner requirements"])
    for row in requirements:
        lines.append(f"- `{row['requirement']}`: {row['current_status']} - blocks: {row['blocks_if_missing']}")
    lines.extend(["", "## Linear muH bound rows"])
    for row in bounds:
        lines.append(f"- `{row['row_id']}`: `{row['linear_bound_formula']}` - {row['current_status']}")
    lines.extend(["", "## Countermodels retained"])
    for row in countermodels:
        lines.append(f"- `{row['countermodel_id']}`: `{row['formula']}` - {row['effect']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    requirements: list[dict[str, object]],
    bounds: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + audit + requirements + bounds + countermodels + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3669*", "3669-Y5-R2FR-*", "P8_Y5*3669*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    add("VAL3669_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3669_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3669_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3669 outputs written")
    add("VAL3669_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3669_4_kh_zero_refused", not any(str(row["accepted_as_zero"]).lower() == "true" for row in audit), "kH zero not accepted")
    add("VAL3669_5_common_mode_condition", any(row["audit_id"] == "KHZ3669_1_common_mode_sufficient" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in audit), "common-mode sufficient zero condition derived")
    add("VAL3669_6_countermodels", {"CE3669_0_FR_like", "CE3669_1_disformal", "CE3669_2_boundary_readout"}.issubset({str(row["countermodel_id"]) for row in countermodels}), "required countermodels retained")
    add("VAL3669_7_requirements", {"K_gamma_H transfer kernel", "no nonminimal Hessian-STF operator", "no disformal/readout frame"}.issubset({str(row["requirement"]) for row in requirements}), "parent owner and transfer requirements listed")
    add("VAL3669_8_linear_bounds", len(bounds) >= 5 and all("mu_H <=" in row["linear_bound_formula"] for row in bounds), "linear muH bound rows generated")
    add("VAL3669_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3669_10_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in bounds), "linear bound rows are not score-ready")
    add("VAL3669_11_doc_written", "k_H" in doc_text and "mu_H" in doc_text and "not claimed" in doc_text, "doc records kH refusal and muH bound")
    add("VAL3669_12_no_formalization_leak", not leaks, "no 3669 checkpoint files in formalization-workbench")
    add("VAL3669_13_next_target", next_target[0]["target_doc"].startswith("3670-") and "KgammaH" in next_target[0]["target_doc"], "3670 KgammaH target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = kh_zero_audit_rows(ts)
    requirements = kh_parent_owner_requirements(ts)
    bounds = linear_muH_bound_rows(ts)
    countermodels = countermodel_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3669_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3669_KH_ZERO_AUDIT_ROWS.csv",
        "requirements": RESIDUALS / "P8_Y5_R2FR_3669_KH_PARENT_OWNER_REQUIREMENTS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3669_LINEAR_MUH_BOUND_ROWS.csv",
        "countermodels": RESIDUALS / "P8_Y5_R2FR_3669_KH_COUNTERMODEL_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3669_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3669_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3669_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3669_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["countermodels"], countermodels)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, requirements, bounds, countermodels, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, requirements, bounds, countermodels, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3669 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3669 checkpoint with {len(validation)} validation checks; kH zero refused and muH bound staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
