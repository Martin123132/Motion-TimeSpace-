from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2851-Y5-R2FR-minimal-parent-amplitude-owner-ansatz-or-no-go-under-AX1090.md"

SRC_2850_DOC = ROOT / "2850-Y5-R2FR-core-amplitude-parent-source-equation-hunt-or-manual-source-ledger-under-AX1090.md"
SRC_2850_HUNT = RESIDUALS / "P8_Y5_R2FR_2850_PARENT_EQUATION_HUNT_LEDGER.csv"
SRC_2850_MANUAL = RESIDUALS / "P8_Y5_R2FR_2850_MANUAL_SOURCE_LEDGER.csv"
SRC_2850_ROUTES = RESIDUALS / "P8_Y5_R2FR_2850_DERIVATION_ROUTE_RANKING.csv"
SRC_2850_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2850_VALIDATION.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_CANCEL = RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2851_SOURCE_REGISTER.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_2851_COMMON_CURRENT_ANSATZ.csv",
    "proof": RESIDUALS / "P8_Y5_R2FR_2851_ALGEBRAIC_PROOF_ATTEMPT.csv",
    "nogos": RESIDUALS / "P8_Y5_R2FR_2851_NO_GO_TUNING_LEDGER.csv",
    "requirements": RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2851_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2851_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2851_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2851_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2851_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ansatz_copy": LOCAL_BOUNDS / "RAB_COMMON_CURRENT_AMPLITUDE_ANSATZ_2851_NONCLAIM.csv",
    "requirements_copy": SOURCE_WEIGHT / "RAB_PARENT_SIGNATURE_REQUIREMENTS_2851_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2851_source_doublet_symmetry_owner_NEXT.csv",
    "nogo_copy": BETA_DOCS / "RAB_COMMON_CURRENT_NO_GO_2851_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2851_0_2850_doc", SRC_2850_DOC, "NEXT2850_0_2851;VAL2850_OVERALL", "2850 selected the minimal parent amplitude owner ansatz/no-go target"),
        ("SRC2851_1_2850_hunt", SRC_2850_HUNT, "HUNT2850_4_relation;HUNT2850_5_current_owner", "2850 relation/current-owner hunt rows"),
        ("SRC2851_2_2850_manual", SRC_2850_MANUAL, "MAN2850_4_identity;MAN2850_5_boundary", "manual source ledger identity and boundary requirements"),
        ("SRC2851_3_2850_routes", SRC_2850_ROUTES, "ROUTE2850_0_shared_parent_current;ROUTE2850_4_absorb_into_GM", "route ranking from 2850"),
        ("SRC2851_4_2850_validation", SRC_2850_VALIDATION, "VAL2850_OVERALL", "2850 validation"),
        ("SRC2851_5_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "exact amplitude suppression condition"),
        ("SRC2851_6_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "parent source-current and sign still missing"),
        ("SRC2851_7_2844_cancel", SRC_2844_CANCEL, "CANCEL2844_1_parent_source_identity;CANCEL2844_5_verdict", "cancellation theorem remains parent-proof missing"),
        ("SRC2851_8_1078_owner", SRC_1078, "CO1078_3_current_rescaling_counterexample;CO1078_4_verdict", "current-owner no-go pressure"),
        ("SRC2851_9_2631_vector", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full PPN vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def ansatz_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ANS2851_0_general_source_doublet",
            "S_src=-int J_star*(a_C*C_AB+a_R*R_delta)",
            "L_CAB C_AB=a_C J_star; L_R R_delta=a_R J_star",
            "Q_CAB=a_C I_star; q_R_eff=a_R I_star",
            "A_total=(sigma_R*a_R+a_C)*I_star/(4*pi)",
            "algebraic_template",
            "ratio a_C=-sigma_R*a_R is required for exact cancellation",
        ),
        (
            "ANS2851_1_candidate_owner_ratio",
            "a_C=-sigma_R*kappa_star; a_R=kappa_star",
            "L_CAB C_AB=-sigma_R*kappa_star J_star; L_R R_delta=kappa_star J_star",
            "Q_CAB=-sigma_R*kappa_star I_star; q_R_eff=kappa_star I_star",
            "A_total=0",
            "conditional_zero_template",
            "works algebraically if the ratio is symmetry-owned, not chosen after the fact",
        ),
        (
            "ANS2851_2_auxiliary_constraint_form",
            "S_aux=int lambda_amp*(Q_CAB+sigma_R*q_R_eff) or local current equivalent",
            "variation imposes Q_CAB+sigma_R*q_R_eff=0",
            "global charge relation",
            "A_total=0",
            "dangerous_constraint_template",
            "rejected unless lambda_amp follows from an existing parent gauge/constraint algebra",
        ),
    ]
    return [
        nonclaim(
            {
                "ansatz_id": ansatz_id,
                "source_term": source_term,
                "field_equations": equations,
                "charge_result": charge_result,
                "amplitude_result": amplitude_result,
                "status": status,
                "condition": condition,
                "parent_signed": False,
                "theorem_accepted": False,
                "control_only": True,
            }
        )
        for ansatz_id, source_term, equations, charge_result, amplitude_result, status, condition in specs
    ]


def proof_rows() -> list[dict[str, Any]]:
    specs = [
        ("ALG2851_0_define_charge_integral", "Let I_star=int_W J_star with compact support and no exterior boundary leakage.", "Q_CAB=a_C I_star and q_R_eff=a_R I_star after common Green normalization.", "CONDITIONAL_STEP", "requires boundary/source convention from parent action"),
        ("ALG2851_1_compute_total_amplitude", "Insert the charges into A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi).", "A_total=(sigma_R*a_R+a_C) I_star/(4*pi).", "DERIVED_SYMBOLIC", "pure algebra once common-current ansatz is granted"),
        ("ALG2851_2_zero_condition", "Demand local 1/r amplitude suppression for arbitrary I_star.", "sigma_R*a_R+a_C=0, hence a_C=-sigma_R*a_R.", "EXACT_CONDITIONAL", "this is a coupling-ratio condition"),
        ("ALG2851_3_identity", "If parent symmetry fixes a_C=-sigma_R*a_R before fitting, then Q_CAB=-sigma_R*q_R_eff.", "A_total=0 and the first gamma-channel amplitude vanishes.", "CONDITIONAL_THEOREM", "not accepted until the symmetry/current owner is sourced"),
        ("ALG2851_4_no_free_lunch", "If a_C/a_R is not parent-owned, cancellation is a codimension-one tuning.", "independent rescaling a_C->lambda_C a_C or a_R->lambda_R a_R breaks A_total=0.", "NO_GO_FOR_UNOWNED_COUPLINGS", "matches the 1078 current-rescaling counterexample"),
    ]
    return [
        nonclaim(
            {
                "proof_id": proof_id,
                "step": step,
                "result": result,
                "status": status,
                "gap": gap,
                "parent_signed": False,
                "theorem_accepted": False,
                "control_only": True,
            }
        )
        for proof_id, step, result, status, gap in specs
    ]


def nogo_rows() -> list[dict[str, Any]]:
    specs = [
        ("NG2851_0_ratio_tuning", "a_C=-sigma_R*a_R can be imposed by hand", "that is a closure axiom unless a symmetry or Noether owner fixes it", "ROUTE_NOT_ACCEPTED"),
        ("NG2851_1_current_rescaling", "J_star or one projection can be rescaled independently", "A_total=0 is destroyed by legal source-normalization changes unless one owner forbids them", "CURRENT_OWNER_REQUIRED"),
        ("NG2851_2_auxiliary_multiplier", "lambda_amp can enforce the charge relation", "if introduced only to kill local PPN amplitude, it is a plateau axiom in disguise", "AUXILIARY_REJECTED_UNLESS_PARENT_MOTIVATED"),
        ("NG2851_3_boundary_shift", "boundary/corner charges can shift Q_CAB or q_R_eff", "charge identity must include or zero all boundary fluxes", "BOUNDARY_CERTIFICATE_REQUIRED"),
        ("NG2851_4_gamma_only", "A_total=0 addresses only the first gamma amplitude", "beta/preferred/source/endpoint/readout/q_loc channels still need full-vector closure", "NO_LOCAL_GR_CLAIM"),
    ]
    return [
        nonclaim(
            {
                "nogo_id": nogo_id,
                "failure_mode": failure_mode,
                "reason": reason,
                "verdict": verdict,
                "blocks_claim": True,
                "control_only": True,
            }
        )
        for nogo_id, failure_mode, reason, verdict in specs
    ]


def requirement_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2851_0_object_language", "single object-language slot for C_AB and R_delta projections", "forbids adding unrelated source coefficients", "MISSING_PARENT_OBJECT_LANGUAGE"),
        ("REQ2851_1_symmetry_owner", "symmetry/constraint fixes coupling vector (a_C,a_R)=kappa_star*(-sigma_R,1)", "turns ratio into theorem rather than tuning", "MISSING_SOURCE_DOUBLET_SYMMETRY"),
        ("REQ2851_2_current_owner", "one current J_star owns both projections before readout", "kills independent current rescaling", "MISSING_CURRENT_OWNER"),
        ("REQ2851_3_operator_sign", "sigma_R is fixed by parent quadratic operator and Green kernel", "prevents sign convention drift", "MISSING_SIGMA_R_PARENT_SIGN"),
        ("REQ2851_4_boundary_silence", "boundary/corner flux is zero or included in both charges", "keeps Q_CAB=-sigma_R*q_R_eff exact", "MISSING_BOUNDARY_FLUX_CERTIFICATE"),
        ("REQ2851_5_GM_and_vector", "measured-GM charge and full PPN vector close in same branch", "prevents a gamma-only false local-GR pass", "MISSING_GM_AND_FULL_VECTOR_CLOSURE"),
    ]
    return [
        nonclaim(
            {
                "requirement_id": req_id,
                "parent_signature": signature,
                "why_required": why,
                "current_status": status,
                "satisfied": False,
                "control_only": True,
            }
        )
        for req_id, signature, why, status in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    specs = [
        ("CG2851_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2851_1_algebra", "common-current algebra derives cancellation condition", "PASS_CONDITIONAL_ONLY", "A_total=0 follows if a_C=-sigma_R*a_R is parent-owned", True),
        ("CG2851_2_parent_signature", "parent source-doublet signature accepted", "BLOCKED", "symmetry/current-owner/sign/boundary requirements are missing", False),
        ("CG2851_3_auxiliary_route", "auxiliary multiplier route accepted", "BLOCKED", "would be a closure axiom unless existing parent constraint algebra signs it", False),
        ("CG2851_4_local_GR", "local GR/Newton reduction claimed", "BLOCKED", "gamma amplitude algebra is not full-vector local GR", False),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "control_check_passed": control_passed,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason, control_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2851_0_algebra_result", "The shared-current ansatz can algebraically derive the amplitude identity.", "CONDITIONAL_SUCCESS", "for arbitrary source strength, A_total=0 iff a_C=-sigma_R*a_R"),
        ("DEC2851_1_claim_result", "The route is not yet a parent theorem.", "NOT_PARENT_SIGNED", "the coupling ratio/current owner can still be tuned or rescaled"),
        ("DEC2851_2_auxiliary_result", "The auxiliary multiplier route is not accepted as-is.", "CLOSURE_AXIOM_RISK", "it would insert the desired plateau unless sourced from an existing constraint algebra"),
        ("DEC2851_3_best_next", "Next target is the symmetry owner of the source doublet.", "SELECT_2852", "this is the exact missing step between conditional algebra and derivation"),
        ("DEC2851_4_no_claim", "No PPN/local-GR/Newton claim.", "LOCKED", "2851 proves a conditional algebraic spine only"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2851_0_2852",
                "status": "selected_primary",
                "target_doc": "2852-Y5-R2FR-source-doublet-symmetry-owner-or-closure-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_doublet_symmetry_owner_or_closure_demotion_under_AX1090_2852.py",
                "mission": "try to find or construct a parent symmetry/object-language owner that fixes the source-doublet coupling ratio a_C=-sigma_R*a_R; if none exists, demote the shared-current route to closure-only and keep finite amplitude fallback",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2851_0_ansatz", OUTPUTS["ansatz"], BRANCH_OUTPUTS["ansatz_copy"], "common-current ansatz nonclaim copy"),
        ("COPY2851_1_requirements", OUTPUTS["requirements"], BRANCH_OUTPUTS["requirements_copy"], "parent signature requirements nonclaim copy"),
        ("COPY2851_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2852"),
        ("COPY2851_3_nogo", OUTPUTS["nogos"], BRANCH_OUTPUTS["nogo_copy"], "common-current no-go ledger nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {"valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "parent_signed", "theorem_accepted", "satisfied", "gate_passed"}
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value", "A_total_value", "delta_p_value", "q_R_hat_value", "Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_prediction_present") is True or row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2851_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2851_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2851_2_conditional_algebra_present", any(row["proof_id"] == "ALG2851_3_identity" and row["status"] == "CONDITIONAL_THEOREM" for row in rows_by_name["proof"]), "conditional amplitude identity algebra is present"),
        ("VAL2851_3_unowned_ratio_blocked", any(row["nogo_id"] == "NG2851_0_ratio_tuning" for row in rows_by_name["nogos"]) and not any(row["theorem_accepted"] for row in rows_by_name["proof"]), "unowned coupling-ratio route remains blocked"),
        ("VAL2851_4_parent_requirements_missing", not any(row["satisfied"] for row in rows_by_name["requirements"]), "parent signature requirements remain unsatisfied"),
        ("VAL2851_5_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2851_6_next_target_2852", any(row["next_id"] == "NEXT2851_0_2852" and row["selected"] for row in rows_by_name["next"]), "2852 source-doublet symmetry owner target selected"),
        ("VAL2851_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2851_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2851_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2851_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2851_11_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2851_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2851_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2851_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2851_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2851_OVERALL",
            "passed": overall,
            "detail": "2851 derives the conditional common-current amplitude identity, blocks it as unowned/tunable, and selects the source-doublet symmetry owner test for 2852.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2851 - Y5 R2FR Minimal Parent Amplitude Owner Ansatz Or No-Go Under AX1090

Status: `Y5_R2FR_2851_common_current_identity_conditional_ratio_owner_missing_nonclaim`

## Private Verdict

2851 gets a real mathematical foothold, but not a claim.

The minimal common-current template is:

```text
S_src = - int J_star (a_C C_AB + a_R R_delta)
Q_CAB = a_C I_star
q_R_eff = a_R I_star
A_total = (sigma_R a_R + a_C) I_star / (4 pi)
```

Therefore the local 1/r amplitude cancels for arbitrary compact source strength exactly when:

```text
a_C = - sigma_R a_R
```

That is useful because it turns the missing coupling into one precise question: does the parent theory own the source-doublet ratio, or is the ratio a hand-tuned closure axiom?

Current verdict: conditional algebra succeeds; parent derivation does not. Without a symmetry/object-language/current owner fixing `(a_C,a_R)=kappa_star(-sigma_R,1)`, this is still a codimension-one tuning and the 1078 rescaling counterexample survives.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Common Current Ansatz

{markdown_table(rows["ansatz"], ["ansatz_id", "source_term", "charge_result", "amplitude_result", "status", "condition", "theorem_accepted", "valid_for_claim"])}

## Algebraic Proof Attempt

{markdown_table(rows["proof"], ["proof_id", "step", "result", "status", "gap", "theorem_accepted", "valid_for_claim"])}

## No-Go / Tuning Ledger

{markdown_table(rows["nogos"], ["nogo_id", "failure_mode", "reason", "verdict", "blocks_claim", "valid_for_claim"])}

## Parent Signature Requirements

{markdown_table(rows["requirements"], ["requirement_id", "parent_signature", "current_status", "why_required", "satisfied", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["ansatz"] = ansatz_rows()
    rows["proof"] = proof_rows()
    rows["nogos"] = nogo_rows()
    rows["requirements"] = requirement_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "ansatz", "proof", "nogos", "requirements", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2851_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2851_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
