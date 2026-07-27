from __future__ import annotations

import csv
import hashlib
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4032_SOURCE_REGISTER.csv",
    "charge_identity": SOURCE_DIR / "P8_Y5_R2FR_4032_SCALAR_CHARGE_IDENTITY.csv",
    "zero_gate": SOURCE_DIR / "P8_Y5_R2FR_4032_QPHI_ZERO_GATE.csv",
    "yukawa_bound": SOURCE_DIR / "P8_Y5_R2FR_4032_YUKAWA_HAIR_BOUND_INPUT.csv",
    "alpha_map": SOURCE_DIR / "P8_Y5_R2FR_4032_ALPHA_LAMBDA_SCALAR_HAIR_MAP.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4032_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4032_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4032_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4032_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4032_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4032_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4032_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def short_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SRC4032_0_4031_doc",
            "path": "4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md",
            "needle": "Q_phi",
            "role": "selects scalar charge as the theorem-zero fork",
        },
        {
            "source_id": "SRC4032_1_4031_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv",
            "needle": "Q_phi",
            "role": "defines scalar charge leakage trigger",
        },
        {
            "source_id": "SRC4032_2_4031_hair",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4031_DELTAPHI_HAIR_BOUND.csv",
            "needle": "HAIR4031_0_yukawa",
            "role": "provides Yukawa hair template",
        },
        {
            "source_id": "SRC4032_3_phi_owner",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4029_PHI_OWNER_EULER_DERIVATION.csv",
            "needle": "Box phi - mu_phi^2",
            "role": "provides scalar owner Euler equation",
        },
        {
            "source_id": "SRC4032_4_field_gate",
            "path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "needle": "zero source charge",
            "role": "states the acceptance pattern for theorem-zero",
        },
        {
            "source_id": "SRC4032_5_energy_identity",
            "path": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "needle": "no source charge",
            "role": "provides prior positive-operator/no-source-charge pattern",
        },
        {
            "source_id": "SRC4032_6_R10_template",
            "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
            "needle": "alpha(lambda)",
            "role": "requires finite-range scalar hair to map into alpha(lambda)",
        },
        {
            "source_id": "SRC4032_7_GM_queue",
            "path": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
            "needle": "CGM4_range_dependence",
            "role": "confirms range dependence blocks Newton/R10 unless zeroed or scored",
        },
    ]


def build_source_register(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        full = ROOT / spec["path"]
        text = read_text(full)
        rows.append(
            {
                **spec,
                "absolute_path": str(full),
                "exists": full.exists(),
                "needle_found": spec["needle"] in text,
                "sha256_16": short_hash(full),
                "timestamp_utc": ts,
            }
        )
    return rows


def build_charge_identity(ts: str) -> list[dict[str, object]]:
    return [
        {
            "identity_id": "QID4032_0_definition",
            "object": "scalar charge",
            "formula": "Q_phi[S]=int_S n.grad u dS, u:=phi-phi_*",
            "meaning": "Q_phi is the monopole data that sources exterior scalar hair",
            "status": "CHARGE_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "identity_id": "QID4032_1_integrated_owner_equation",
            "object": "source worldtube identity",
            "formula": "for (Delta-mu_phi^2)u=(2/3)F, Q_phi = mu_phi^2 int_W u dV + (2/3)int_W F dV",
            "meaning": "scalar charge is not arbitrary; it is controlled by fixed-branch displacement and total F-charge",
            "status": "WORLD_TUBE_CHARGE_IDENTITY_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "identity_id": "QID4032_2_zero_corollary",
            "object": "zero charge corollary",
            "formula": "Q_phi=0 if int_W F dV=0 and int_W u dV=0, or if the parent boundary condition directly fixes n.grad u=0",
            "meaning": "the theorem-zero route needs source neutrality or no-scalar-flux, not vibes",
            "status": "ZERO_COROLLARY_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "identity_id": "QID4032_3_failure",
            "object": "source scalar charge",
            "formula": "if F contains unneutralized matter/source trace or boundary class charge, Q_phi generally survives",
            "meaning": "surviving Q_phi is a fifth-force/range hair, not a closure term",
            "status": "FAILURE_MODE_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_zero_gate(ts: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "QG4032_0_phi_owner",
            "clause": "phi owner equation is parent-adopted with F split into source-neutral F_rest",
            "required_evidence": "live parent action row and F-dependence guard",
            "current_result": "template exists, not live-adopted",
            "zeroes_Q_phi": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "QG4032_1_source_neutrality",
            "clause": "int_W F dV=0 for compact local source worldtube after EH/Newton routing",
            "required_evidence": "Ward/source-neutrality proof or topological/divergence F with no flux",
            "current_result": "not yet proven",
            "zeroes_Q_phi": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "QG4032_2_fixed_branch",
            "clause": "int_W u dV=0 or u=0 inside the compact fixed branch",
            "required_evidence": "positive energy/mass-gap interior theorem with fixed source boundary",
            "current_result": "exterior theorem exists; interior/source worldtube clause still open",
            "zeroes_Q_phi": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "QG4032_3_no_flux_boundary",
            "clause": "n.grad u=0 on the source boundary or scalar flux cancels by orientation/topological class",
            "required_evidence": "boundary condition from parent variational problem, not imposed after the fact",
            "current_result": "not yet signed",
            "zeroes_Q_phi": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "QG4032_4_if_all_signed",
            "clause": "QG4032_0 through QG4032_3 all hold",
            "required_evidence": "all source paths and parent clauses",
            "current_result": "conditional success path only",
            "zeroes_Q_phi": True,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_yukawa_bound(ts: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "YUK4032_0_solution",
            "quantity": "u(r)",
            "formula": "u(r)=Q_phi exp[-r/lambda_phi]/(4*pi*r)+multipoles+outer_boundary, lambda_phi=1/mu_phi",
            "units_needed": "Q_phi units, lambda_phi length, source radius convention",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "YUK4032_1_force",
            "quantity": "finite-range force",
            "formula": "a_phi/a_N ~ C_phiM*(Q_phi/M_H)*exp[-r/lambda_phi]*(1+r/lambda_phi)",
            "units_needed": "map Q_phi to measured Hilbert mass M_H and test-body scalar response",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "YUK4032_2_tracefree_metric",
            "quantity": "A_delta_phiG/L_phiG",
            "formula": "A_delta_phiG/L_phiG <= |Q_phi| exp[-R_collar/lambda_phi] A_GTF/(4*pi R_collar L_GTF)",
            "units_needed": "A_GTF, L_GTF and collar radius in the same observed frame",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "YUK4032_3_zero_limit",
            "quantity": "Q_phi=0",
            "formula": "Q_phi=0 => alpha_phi(lambda_phi)=0 and A_delta_phiG/L_phiG=0",
            "units_needed": "theorem certificate, not numeric data",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_alpha_map(ts: str) -> list[dict[str, object]]:
    return [
        {
            "alpha_id": "ALPHA4032_0_definition",
            "observable": "alpha_phi(lambda)",
            "formula": "alpha_phi(lambda_phi)=C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)",
            "meaning": "finite-range scalar hair maps to the R10 alpha(lambda) branch",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "alpha_id": "ALPHA4032_1_universal_test_response",
            "observable": "universal scalar response",
            "formula": "if q_test/m_test is universal, WEP composition term may vanish but alpha(lambda) still constrains the common fifth force",
            "meaning": "universal coupling is not automatically safe; it still changes inverse-square gravity",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "alpha_id": "ALPHA4032_2_composition_response",
            "observable": "eta_source_AB",
            "formula": "if q_A/m_A differs by material, eta_AB ~ |q_A/m_A-q_B/m_B|*|Q_phi/M_H|",
            "meaning": "composition-dependent scalar charge goes to WEP/source-charge rows",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "alpha_id": "ALPHA4032_3_required_file",
            "observable": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "formula": "needed columns: lambda_value, lambda_units, alpha_predicted, alpha_source, Q_phi_source, valid_for_claim",
            "meaning": "if Q_phi is not zero, the next empirical path is an alpha(lambda) curve, not prose",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4032_0_zero",
            "input_condition": "source-neutral F, fixed interior u, no scalar flux boundary",
            "expected_verdict": "QPHI_ZERO_IF_SOURCE_NEUTRALITY_SIGNED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4032_1_hair",
            "input_condition": "unneutralized F or scalar boundary flux survives",
            "expected_verdict": "YUKAWA_ALPHA_BRANCH_DEFINED_NOT_NUMERIC",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4032_2_current",
            "input_condition": "current source hierarchy after 4032",
            "expected_verdict": "QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4032_0_zero",
            "verdict": "QPHI_ZERO_IF_SOURCE_NEUTRALITY_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4032",
            "next_action": "then scalar-hair obstruction is removed from exterior PPN/R10",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4032_1_hair",
            "verdict": "YUKAWA_ALPHA_BRANCH_DEFINED_NOT_NUMERIC",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4032",
            "next_action": "source Q_phi, lambda_phi, q_test/m_test and alpha(lambda) bound rows",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4032_2_current",
            "verdict": "QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4032",
            "next_action": "4033 should prove source-neutral F or write the alpha(lambda) curve row",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4032_0_identity",
            "decision": "Q_phi is now derived from the integrated phi-owner equation, not treated as a free missing symbol",
            "status": "SCALAR_CHARGE_OBJECT_OWNED_SYMBOLICALLY",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4032_1_zero",
            "decision": "Q_phi=0 requires source-neutral F plus fixed interior/no scalar flux; these are exact clauses, not closure assumptions",
            "status": "ZERO_GATE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4032_2_bound",
            "decision": "if Q_phi survives, it maps to Yukawa alpha(lambda), source WEP, and trace-free beta rows",
            "status": "BOUND_BRANCH_READY_SYMBOLIC",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4032_3_next",
            "decision": "move to 4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4032_0_Qphi_zero",
            "claim": "Q_phi=0 in the live theory",
            "allowed": False,
            "reason": "source-neutrality/interior/no-flux clauses are not parent-signed yet",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4032_1_R10_pass",
            "claim": "finite-range alpha(lambda) passes",
            "allowed": False,
            "reason": "alpha curve is symbolic and has no numeric Q_phi/lambda/source rows",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4032_2_WEP_pass",
            "claim": "source-charge WEP passes",
            "allowed": False,
            "reason": "test-body scalar response q_A/m_A is not derived universal or bounded",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4032_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "Q_phi, boundary/source-current and adoption gates remain open",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4032_0",
            "next_doc": "4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md",
            "next_script": "scripts/Y5_R2FR_4033_source_neutral_F_proof_or_alpha_lambda_curve_row.py",
            "why": "source-neutral F is the first exact clause needed to make Q_phi=0; otherwise alpha(lambda) must become executable",
            "fallback": "build R10_alpha_lambda_curve_MTS_source_normalization.csv with valid_for_claim=false until Q_phi/lambda are sourced",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4032_0",
            "checkpoint": "4032",
            "headline": "scalar charge identity derived; Q_phi zero gate and Yukawa alpha(lambda) fallback written",
            "verdict": "QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4032 - Scalar Charge Zero Or Yukawa Hair Bound Input

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4032 turns the remaining scalar-hair clause into a concrete charge identity. With

`u := phi - phi_*`

and

`(Delta - mu_phi^2)u = (2/3)F`,

the exterior scalar charge is

`Q_phi[S]=int_S n.grad u dS`.

Integrating over the compact source worldtube gives

`Q_phi = mu_phi^2 int_W u dV + (2/3)int_W F dV`.

So `Q_phi=0` is not magic. It follows if the source branch has neutral `F` charge and fixed-branch/no-flux `u`.

## If The Zero Fails

For `lambda_phi=1/mu_phi`,

`u(r)=Q_phi exp[-r/lambda_phi]/(4*pi*r)+multipoles+outer_boundary`.

That maps to a finite-range row:

`alpha_phi(lambda_phi)=C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)`.

Universal test response may remove composition dependence, but it does not remove the common fifth force. So surviving `Q_phi` must go to R10 `alpha(lambda)`, source-WEP, and `C_beta_TF` scoring.

## Current Verdict

- Current evaluator result: `QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4032`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md`
- `scripts/Y5_R2FR_4033_source_neutral_F_proof_or_alpha_lambda_curve_row.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    charge: list[dict[str, object]],
    zero_gate: list[dict[str, object]],
    yukawa: list[dict[str, object]],
    alpha: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    charge_ids = {str(row["identity_id"]) for row in charge}
    gate_ids = {str(row["gate_id"]) for row in zero_gate}
    yukawa_ids = {str(row["bound_id"]) for row in yukawa}
    alpha_ids = {str(row["alpha_id"]) for row in alpha}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4032_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4032_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4032_02_Q_definition", "QID4032_0_definition" in charge_ids, "Q_phi definition row present", ts)
    add_validation(rows, "VAL4032_03_integrated_identity", "QID4032_1_integrated_owner_equation" in charge_ids, "integrated charge identity row present", ts)
    add_validation(rows, "VAL4032_04_zero_corollary", "QID4032_2_zero_corollary" in charge_ids, "zero corollary row present", ts)
    add_validation(rows, "VAL4032_05_failure_mode", "QID4032_3_failure" in charge_ids, "failure mode row present", ts)
    add_validation(rows, "VAL4032_06_zero_gate_source", "QG4032_1_source_neutrality" in gate_ids, "source-neutrality gate present", ts)
    add_validation(rows, "VAL4032_07_zero_gate_all", "QG4032_4_if_all_signed" in gate_ids, "all-signed gate present", ts)
    add_validation(rows, "VAL4032_08_yukawa_solution", "YUK4032_0_solution" in yukawa_ids, "Yukawa solution row present", ts)
    add_validation(rows, "VAL4032_09_yukawa_force", "YUK4032_1_force" in yukawa_ids, "finite-range force row present", ts)
    add_validation(rows, "VAL4032_10_alpha_def", "ALPHA4032_0_definition" in alpha_ids, "alpha(lambda) definition row present", ts)
    add_validation(rows, "VAL4032_11_alpha_curve", "ALPHA4032_3_required_file" in alpha_ids, "alpha curve required-file row present", ts)
    add_validation(rows, "VAL4032_12_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in yukawa + alpha), "Yukawa/alpha rows not score-ready", ts)
    add_validation(rows, "VAL4032_13_current_verdict", "QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4032_14_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4032_15_next_decision", any("4033" in str(row["decision"]) for row in decisions), "4033 next decision present", ts)
    add_validation(rows, "VAL4032_16_next_target", bool(next_target and "4033" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4032_17_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4032_18_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4032_19_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4032_20_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in charge + zero_gate + yukawa + alpha + decisions), "all rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    charge = build_charge_identity(ts)
    zero_gate = build_zero_gate(ts)
    yukawa = build_yukawa_bound(ts)
    alpha = build_alpha_map(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["charge_identity"], charge)
    write_csv(OUTPUTS["zero_gate"], zero_gate)
    write_csv(OUTPUTS["yukawa_bound"], yukawa)
    write_csv(OUTPUTS["alpha_map"], alpha)
    write_csv(OUTPUTS["evaluator_cases"], cases)
    write_csv(OUTPUTS["evaluator_results"], results)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(
        ts,
        sources,
        charge,
        zero_gate,
        yukawa,
        alpha,
        results,
        decisions,
        claims,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4032 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
