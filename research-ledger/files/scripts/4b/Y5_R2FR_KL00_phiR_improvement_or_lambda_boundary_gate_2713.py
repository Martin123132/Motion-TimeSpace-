from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2713"
BRANCH_ID = "Y5_R2FR_KL00_PHIR_IMPROVEMENT_OR_LAMBDA_BOUNDARY_GATE_2713"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2713-Y5-R2FR-KL00-phiR-improvement-or-lambda-boundary-gate-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2713_SOURCE_REGISTER.csv",
    "improvement_rollforward": RESIDUALS / "P8_Y5_R2FR_2713_KL00_PHIR_IMPROVEMENT_ROLLFORWARD.csv",
    "lambda_phi_gate": RESIDUALS / "P8_Y5_R2FR_2713_LAMBDA_PHI_BOUNDARY_GATE.csv",
    "deltak_kbar_status": RESIDUALS / "P8_Y5_R2FR_2713_DELTAK_KBAR_STATUS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2713_CLAIM_GATES.csv",
    "current_blocker_stack": RESIDUALS / "P8_Y5_R2FR_2713_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2713_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2713_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2713_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2713_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds_gate": LOCAL_BOUNDS / "KL00_phiR_improvement_gate_2713_NONCLAIM.csv",
    "deltak_gate": SOURCE_WEIGHT / "DeltaK_Khat_adoption_gate_2713_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2713_LAMBDA_PHI_OR_KHAT_ADOPTION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2713_2712_CURRENT_R2FR_TARGET",
        "relative_path": "2712-Y5-R2FR-A511-local-EH-fixed-point-rollforward-under-AX1090-closure.md",
        "required_needles": ["COMP2712_1_KL00", "QDK2712_2_DeltaK", "NEXT2712_0_selected", "VAL2712_OVERALL"],
        "purpose": "imports the current R2FR handoff: KL00 amplitude/response or Kmetric derivative under AX1090 closure",
    },
    {
        "source_id": "SRC2713_2711_AX1090_CLOSURE",
        "relative_path": "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
        "required_needles": ["AX1090_0_LC", "NEXT2711_0_selected", "VAL2711_OVERALL"],
        "purpose": "keeps the local transition branch explicitly closure-only at the parent-object level",
    },
    {
        "source_id": "SRC2713_1525_KHAT_ORIGIN_GATE",
        "relative_path": "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
        "required_needles": ["KOR1525_0_formal_candidate", "KER1525_7_verdict", "DEC1525_0_best_route", "NEXT1525_0_1526"],
        "purpose": "imports the trace-free Hessian/improvement-action route and full Kmetric fallback",
    },
    {
        "source_id": "SRC2713_1526_PHIR_IDENTITY",
        "relative_path": "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md",
        "required_needles": ["VAR1526_5_verdict", "SYM1526_3_current_MTS_match", "OUT1526_1_current_status", "VAL1526_16_overall"],
        "purpose": "imports the conditional derivation that phi R can generate the KL tensor shape",
    },
    {
        "source_id": "SRC2713_1527_PHI_OWNER",
        "relative_path": "1527-Y5-phi-owner-and-current-Khat-symbol-match-source-hunt.md",
        "required_needles": ["AUX1527_0_local_action_candidate", "KAD1527_4_verdict", "MLT1527_4_verdict", "VAL1527_16_overall"],
        "purpose": "imports the local auxiliary phi-owner contract and staged Khat adoption row",
    },
    {
        "source_id": "SRC2713_1529_LAMBDA_GATE",
        "relative_path": "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
        "required_needles": ["BND1529_2_zero_mode_reference", "RUN1529_2_Khat_route", "NEXT1529_0_1530", "VAL1529_15_overall"],
        "purpose": "imports the unresolved lambda_phi boundary/no-flux and stress-bound gate",
    },
    {
        "source_id": "SRC2713_1299_SPATIAL_TRACE",
        "relative_path": "1299-Y5-R10-RAB-spatial-trace-kernel-bound-or-trace-theorem.md",
        "required_needles": ["KBA1299_0_total_Kbar_abs_bound", "STK1299_0_m_spatial_trace", "NEXT1299_0_1300", "VAL1299_9_overall"],
        "purpose": "imports the warning that Newton Kbar_00 cannot be scored from 00-only data",
    },
    {
        "source_id": "SRC2713_2692_GR_CONTRACT",
        "relative_path": "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "required_needles": ["LHS2692_9_verdict", "ORP2692_10_total_abs_envelope", "VAL2692_OVERALL"],
        "purpose": "imports the exact conditional GR/Newton contract and the residual-pack discipline",
    },
    {
        "source_id": "SRC2713_2699_QLOC_RESIDUAL",
        "relative_path": "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
        "required_needles": ["WID2699_0_definition", "QLOC2699_7_total", "VAL2699_OVERALL"],
        "purpose": "imports q_loc as the official retained residual until the parent stress route closes",
    },
    {
        "source_id": "SRC2713_1510_R10_FREEZE",
        "relative_path": "1510-Y5-R10-RAB-reviewed-figure-digitization-protocol-or-return-to-GR-derivation.md",
        "required_needles": ["R10 scoring branch stays frozen", "ROUTE1510_1_return_to_gr", "VAL1510_12_overall"],
        "purpose": "confirms local empirical scoring remains frozen while GR/Newton derivability is attacked",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def improvement_rollforward_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "IR2713_0_KL00_inherited_component",
            "object": "K_L^{00}",
            "statement": "formal trace-free longitudinal component exists: K_L^{00}=2 nabla^0 nabla^0 phi - (1/2) g^{00} Box phi",
            "source_anchor": "2712 COMP2712_1_KL00; 1525 KOR1525_0_formal_candidate",
            "progress": "COMPONENT_EXISTS_NONCLAIM",
            "blocking_gap": "parent phi owner, coefficient/sign, boundary convention, amplitude/domain and current Khat adoption",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "IR2713_1_phiR_improvement_identity",
            "object": "S_I=c_I int sqrt(-g) phi R",
            "statement": "trace-free metric response of the scalar-curvature improvement term gives the K_L tensor shape up to coefficient/sign and boundary clauses",
            "source_anchor": "1526 VAR1526_5_verdict; 1526 SYM1526_2_tracefree_candidate_match",
            "progress": "REAL_CONDITIONAL_DERIVATION_GAIN",
            "blocking_gap": "not live MTS Khat until phi owner, sigma_resp*c_I=1, boundary term, and current-symbol adoption close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "IR2713_2_local_phi_owner_candidate",
            "object": "S_phiK",
            "statement": "S_phiK=int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma]+B_phiK localizes Box phi=S_Gamma without naked inverse-Box",
            "source_anchor": "1527 AUX1527_0_local_action_candidate; 1527 AUX1527_1_lambda_variation",
            "progress": "LOCAL_AUXILIARY_CONTRACT_STAGED",
            "blocking_gap": "lambda_phi stress, no-flux/zero-mode certificate, and parent adoption remain missing",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "IR2713_3_lambda_phi_obstruction",
            "object": "lambda_phi",
            "statement": "the auxiliary route creates multiplier stress unless lambda_phi=0 by theorem or the stress is bounded below local limits",
            "source_anchor": "1527 MLT1527_4_verdict; 1529 RUN1529_2_Khat_route",
            "progress": "OBSTRUCTION_LOCALIZED",
            "blocking_gap": "missing parent domain, boundary/no-flux, zero-mode, source-boundary matching, and stress-bound constants",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "IR2713_4_Kmetric_kernel_fallback",
            "object": "Kmetric[Gamma_eff]",
            "statement": "if the improvement-action adoption fails, full Kmetric still requires volume, M_m, M_L, connection, domain, boundary, sign and units kernels",
            "source_anchor": "1525 KER1525_7_verdict; 1526 KF1526_5_bound_route",
            "progress": "FALLBACK_RETAINED",
            "blocking_gap": "M_m, M_L, K_conn, K_domain, K_boundary, C_sign and current Khat comparison",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def lambda_phi_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "LPG2713_0_domain_certificate",
            "required_clause": "parent-owned compact local collar/domain for lambda_phi",
            "current_status": "MISSING_PARENT_DOMAIN_CERTIFICATE",
            "if_passes": "energy/no-flux proof can be made a parent theorem rather than a chosen boundary condition",
            "if_fails": "lambda_phi stress remains an explicit local residual",
            "source_anchor": "1529 BND1529_0_domain_certificate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "LPG2713_1_boundary_condition",
            "required_clause": "Dirichlet or Neumann/no-flux condition sourced by parent branch",
            "current_status": "MISSING_BOUNDARY_CONDITION_CERTIFICATE",
            "if_passes": "lambda_phi harmonic branch can be forced toward silence",
            "if_fails": "boundary flux/reference hair enters DeltaK/q_loc",
            "source_anchor": "1529 BND1529_1_boundary_condition",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "LPG2713_2_zero_mode_reference",
            "required_clause": "zero-mode/reference condition for lambda_phi",
            "current_status": "MISSING_ZERO_MODE_CERTIFICATE",
            "if_passes": "constant lambda_phi mode cannot source metric response",
            "if_fails": "Neumann/no-flux alone is insufficient",
            "source_anchor": "1529 BND1529_2_zero_mode_reference",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "LPG2713_3_stress_bound_inputs",
            "required_clause": "C_P, C_E, C_T, R_norm, boundary_source_norm, observable projection",
            "current_status": "MISSING_BOUND_INPUTS",
            "if_passes": "lambda_phi route can be demoted to a finite residual bound instead of a theorem-zero claim",
            "if_fails": "Khat adoption remains staged and unscoreable",
            "source_anchor": "1529 BIN1529_0_C_P through BIN1529_7_observable_projection",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "LPG2713_4_verdict",
            "required_clause": "lambda_phi theorem-zero or finite stress bound",
            "current_status": "BLOCKED_NOT_ZERO_NOT_BOUNDED",
            "if_passes": "current Khat adoption can be revisited under AX1090 closure",
            "if_fails": "local GR/Newton/PPN remains blocked by DeltaK/q_loc residuals",
            "source_anchor": "1527 GATE1527_2; 1529 GATE1529_3_lambda_decision",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def deltak_kbar_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "DKS2713_0_best_zero_route",
            "object": "Delta_K^{mu nu}",
            "formula_or_contract": "Delta_K=0 only if current Khat is the same parent metric response as Kmetric[Gamma_eff], including phi owner, coefficient/sign, boundary and lambda_phi silence",
            "current_status": "BEST_ROUTE_IDENTIFIED_NOT_CLOSED",
            "why": "phi R improvement gives the K_L shape, but adoption and lambda_phi gates are unsigned",
            "next_repair": "derive lambda_phi zero/no-flux certificate or retain source-backed multiplier-stress bound",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "DKS2713_1_Khat_adoption",
            "object": "current MTS K_hat",
            "formula_or_contract": "K_hat^{mu nu}:=TF[sigma_resp c_I metric response of int sqrt(-g) phi R] with sigma_resp*c_I=1",
            "current_status": "ADOPTION_ROW_STAGED_NOT_LIVE",
            "why": "1527 staged the row but did not promote it into the live parent branch",
            "next_repair": "source/adopt the row only after lambda_phi and boundary obligations are resolved",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "DKS2713_2_Kbar_trace_budget",
            "object": "Kbar_L,loc,00",
            "formula_or_contract": "|Kbar_L,loc,00| <= 0.5*(|R_m^{00}|+|R_L^{00}|+|R_cdb^{00}|+|R_m^Sigma|+|R_L^Sigma|+|R_cdb^Sigma|)+|Delta_projector_boundary|",
            "current_status": "TRACE_AWARE_BOUND_FORM_ONLY",
            "why": "1299 rejects 00-only Newton scoring and requires spatial trace kernels or a trace/isotropy theorem",
            "next_repair": "do not compute Newton/PPN scores until spatial trace or Khat identity route closes",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "DKS2713_3_q_loc",
            "object": "q_loc^nu",
            "formula_or_contract": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})=-P_loc nabla_mu T_GK^{mu nu}",
            "current_status": "OFFICIAL_RETAINED_RESIDUAL",
            "why": "parent Hilbert-stress/Euler/boundary/projector/double-zero chain is not signed",
            "next_repair": "close DeltaK/Khat adoption first, then return to q_loc theorem-zero or finite profile",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "DKS2713_4_local_GR",
            "object": "local GR/Newton/PPN",
            "formula_or_contract": "AX1090_0_LC + A511 gates + DeltaK/q_loc/source residuals all pass",
            "current_status": "BLOCKED_BUT_NARROWER",
            "why": "KL00 side is now narrowed to phiR/lambda_phi/Khat adoption rather than vague tensor missingness",
            "next_repair": "run 2714 lambda_phi zero/bound gate under AX1090 closure",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2713_0_KL00_origin", "K_L shape has a conditional phi R origin", "PASS_NONCLAIM", "trace-free improvement identity is real but not live Khat"),
        ("CG2713_1_phi_owner", "local phi owner is parent-adopted", "BLOCKED", "S_phiK is a staged contract only under AX1090 closure"),
        ("CG2713_2_lambda_phi", "lambda_phi stress is theorem-zero or bounded", "BLOCKED", "boundary/no-flux/zero-mode or bound inputs missing"),
        ("CG2713_3_Khat_adoption", "current Khat equals the improvement response", "BLOCKED", "adoption row staged but not promoted"),
        ("CG2713_4_DeltaK", "DeltaK is zero or computable", "BLOCKED", "Khat adoption plus Kmetric fallback kernels unresolved"),
        ("CG2713_5_Kbar_Newton_score", "Newton/PPN Kbar budget is scoreable", "BLOCKED", "spatial trace and observable response inputs missing"),
        ("CG2713_6_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "AX1090 is closure-only and q_loc/source residuals remain active"),
        ("CG2713_7_public_or_github", "public/GitHub action", "BLOCKED", "private checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": "true" if status == "PASS_NONCLAIM" else "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in gates
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK2713_0_parent_object", "AX1090_0 is explicit closure, not derivation", "local transition branch remains closure-only", "derive parent object from MTS primitives or keep closure label"),
        ("BLK2713_1_lambda_phi", "lambda_phi theorem-zero/bound missing", "Khat adoption cannot become live", "derive boundary/no-flux/zero-mode certificate or source stress-bound constants"),
        ("BLK2713_2_current_Khat", "current MTS Khat not adopted as phiR improvement response", "DeltaK cannot be zeroed", "adopt/source Khat row after lambda_phi gate"),
        ("BLK2713_3_Kmetric_fallback", "full Kmetric kernels unresolved", "fallback compute route remains blocked", "fill M_m, M_L, K_conn, K_domain, K_boundary, sign and units"),
        ("BLK2713_4_spatial_trace", "Kbar Newton budget needs spatial trace", "00-only scoring is refused", "derive trace/isotropy theorem or fill spatial trace kernels"),
        ("BLK2713_5_q_loc_profile", "q_loc residual not zero/bounded", "PPN/R10/clock/orbital projections remain nonclaim", "return after Khat/DeltaK gate moves"),
    ]
    return [
        {
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": effect,
            "next_action": next_action,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for blocker_id, blocker, effect, next_action in blockers
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2713_0_not_repeat_KL00",
            "decision": "Do not repeat the older KL00 amplitude row as if it is still the frontier.",
            "rationale": "1525 through 1529 already advanced the problem to phiR improvement identity, phi owner, lambda_phi stress, and Khat adoption.",
            "next_action": "splice that sharper obstruction into the R2FR/AX1090 closure line",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2713_1_best_route",
            "decision": "Prefer the phiR improvement-action route over brute-force Kmetric kernels for the next leap.",
            "rationale": "if parent-signed, it can explain the K_L shape and potentially remove a major DeltaK obstruction in one move.",
            "next_action": "attack lambda_phi boundary/no-flux/zero-mode or bound it honestly",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2713_2_guard",
            "decision": "Keep Kmetric and Kbar trace fallback rows active.",
            "rationale": "if Khat adoption fails, the theory must still compute or bound the full residual; no cancellation-only pass is allowed.",
            "next_action": "retain full kernel and spatial-trace ledgers as fallback",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2713_3_no_claim",
            "decision": "No local GR/Newton/PPN/R10 claim is promoted.",
            "rationale": "AX1090 is closure-only and lambda_phi/Khat/DeltaK/q_loc/source residuals remain unsigned.",
            "next_action": "run 2714 lambda_phi zero/bound gate under AX1090 closure",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2713_0_selected",
            "status": "selected_primary",
            "target_doc": "2714-Y5-R2FR-lambda-phi-zero-bound-or-Khat-adoption-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_lambda_phi_zero_bound_or_Khat_adoption_under_AX1090_closure_2714.py",
            "purpose": "derive a parent boundary/no-flux/zero-mode certificate that makes lambda_phi silent, or source the first multiplier-stress bound inputs before any Khat adoption/local-GR promotion",
            "acceptance_condition": "lambda_phi=0 is parent-certified, or a finite nonclaim stress-bound row with units/source paths/projection is written; Khat adoption remains blocked unless lambda gate passes",
            "forbidden_shortcuts": "choose boundary conditions by hand; ignore lambda_phi stress; silently redefine Khat; compute DeltaK from volume-only terms; score local GR/PPN/R10; GitHub action; edit formalization-workbench",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2713_0_progress",
            "topic": "KL00/Khat route",
            "status": "SHARPENED_TO_PHIR_LAMBDA_GATE",
            "meaning": "the K_L tensor shape now has a serious conditional parent-action explanation; the missing piece is no longer vague KL00 algebra",
            "next_action": "prove or bound lambda_phi and then revisit Khat adoption",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2713_1_gr_reduction",
            "topic": "local GR/Newton",
            "status": "NOT_CLAIMED_BUT_MORE_LOCALIZED",
            "meaning": "GR reduction remains blocked, but the tensor-side obstruction is now a named local auxiliary/boundary problem",
            "next_action": "run 2714 lambda_phi zero/bound gate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2713_2_testing",
            "topic": "empirical local tests",
            "status": "DEFERRED",
            "meaning": "R10/PPN/clock/orbital tests should not be scored from placeholders or 00-only data",
            "next_action": "return to tests after residuals have theorem-zero or source-backed finite bounds",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2713_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "private checkpoint only",
            "next_action": "keep working in post-checkpoint-work",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2713_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2713_KL00_PHIR_IMPROVEMENT_ROLLFORWARD.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds_gate"]),
            "purpose": "quarantine nonclaim local-bounds-facing KL00/phiR gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2713_1_source_weight",
            "source_table": "P8_Y5_R2FR_2713_DELTAK_KBAR_STATUS.csv",
            "copy_path": str(BRANCH_OUTPUTS["deltak_gate"]),
            "purpose": "quarantine nonclaim DeltaK/Khat adoption gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2713_2_rab_queue",
            "source_table": "P8_Y5_R2FR_2713_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "queue 2714 lambda_phi/Khat adoption work",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    count = 0
    threshold = START_UTC.timestamp() - 1.0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                count += 1
        except OSError:
            continue
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], generated_paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, details: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": as_bool(passed),
                "details": details,
                "timestamp_utc": stamp(),
            }
        )

    source_rows = rows_by_name["source_register"]
    add(
        "VAL2713_0_sources_exist",
        all(row["exists"] == "true" and row["missing_needles"] == "" for row in source_rows),
        f"sources_checked={len(source_rows)}",
    )
    add(
        "VAL2713_1_improvement_gain_recorded",
        any(row["row_id"] == "IR2713_1_phiR_improvement_identity" and row["progress"] == "REAL_CONDITIONAL_DERIVATION_GAIN" for row in rows_by_name["improvement_rollforward"]),
        "phiR trace-free improvement identity is carried forward as conditional nonclaim progress",
    )
    add(
        "VAL2713_2_lambda_gate_blocked",
        any(row["gate_id"] == "LPG2713_4_verdict" and row["current_status"] == "BLOCKED_NOT_ZERO_NOT_BOUNDED" for row in rows_by_name["lambda_phi_gate"]),
        "lambda_phi remains neither theorem-zero nor bounded",
    )
    add(
        "VAL2713_3_DeltaK_not_promoted",
        any(row["status_id"] == "DKS2713_1_Khat_adoption" and row["current_status"] == "ADOPTION_ROW_STAGED_NOT_LIVE" for row in rows_by_name["deltak_kbar_status"]),
        "Khat adoption remains staged, so DeltaK cannot be zeroed",
    )
    add(
        "VAL2713_4_Kbar_trace_guard",
        any(row["status_id"] == "DKS2713_2_Kbar_trace_budget" and "00-only" in row["why"] for row in rows_by_name["deltak_kbar_status"]),
        "Newton/PPN scoring from 00-only KL00 data is refused",
    )
    add(
        "VAL2713_5_claims_blocked",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]),
        "all claim gates remain nonclaim",
    )
    add(
        "VAL2713_6_next_target_selected",
        any(row["next_id"] == "NEXT2713_0_selected" and "2714" in row["target_doc"] for row in rows_by_name["next_target"]),
        "2714 lambda_phi zero/bound target selected",
    )
    add(
        "VAL2713_7_branch_copies_declared",
        len(rows_by_name["branch_copies"]) == len(BRANCH_OUTPUTS),
        f"branch_copy_rows={len(rows_by_name['branch_copies'])}",
    )

    parse_details = []
    parse_ok = True
    for name, path in generated_paths.items():
        if path.suffix.lower() != ".csv":
            continue
        if path == OUTPUTS["validation"]:
            continue
        ok, row_count, detail = parse_csv(path)
        parse_ok = parse_ok and ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    add("VAL2713_8_csv_parse", parse_ok, "; ".join(parse_details))

    add(
        "VAL2713_9_no_formalization_outputs",
        not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()),
        "no output path points into formalization-workbench",
    )
    recent_formalization = formalization_recent_change_count()
    add(
        "VAL2713_10_no_formalization_recent_changes",
        recent_formalization == 0,
        f"formalization_recent_changed_count={recent_formalization}",
    )
    add(
        "VAL2713_11_no_github_outputs",
        not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()),
        "no GitHub/public-output path was written",
    )
    add(
        "VAL2713_12_nonclaim_policy",
        all(
            row.get("valid_for_claim") == "false" and row.get("claim_allowed", "false") == "false"
            for table in rows_by_name.values()
            for row in table
            if "valid_for_claim" in row
        ),
        "generated tables keep valid_for_claim=false and claim_allowed=false",
    )

    overall = all(row["passed"] == "true" for row in rows)
    add(
        "VAL2713_OVERALL",
        overall,
        "2713 splices the phiR/KL00 improvement route into the R2FR AX1090 closure line, localizes the obstruction to lambda_phi/Khat adoption, keeps DeltaK/q_loc/local-GR nonclaim, and selects 2714",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    sections = [
        f"# 2713 Y5 R2FR KL00 phiR improvement or lambda boundary gate under AX1090 closure",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2713 is a useful forward splice, not a claim. The old `K_L^{00}` problem has sharpened: the trace-free Hessian component is conditionally explained by a `phi R` improvement-action response, and a local auxiliary `S_phiK` route can avoid naked inverse-Box nonlocality. But that route introduces `lambda_phi` multiplier stress, and the current corpus does not parent-sign the boundary/no-flux/zero-mode certificate or finite stress-bound inputs.",
        "",
        "So the live wall is not “what is `K_L`?” anymore. It is: can `lambda_phi` be proved silent or bounded, and can current MTS `K_hat` be explicitly adopted as the same parent metric response? Until that closes, `Delta_K`, `Kbar`, `q_loc`, local GR, Newton, PPN, R10, clocks and orbital claims stay blocked.",
        "",
        "## Source Register",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## KL00 phiR Improvement Rollforward",
        markdown_table(rows_by_name["improvement_rollforward"]),
        "",
        "## Lambda Phi Boundary Gate",
        markdown_table(rows_by_name["lambda_phi_gate"]),
        "",
        "## DeltaK and Kbar Status",
        markdown_table(rows_by_name["deltak_kbar_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_by_name["claim_gates"]),
        "",
        "## Current Blocker Stack",
        markdown_table(rows_by_name["current_blocker_stack"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        markdown_table(rows_by_name["project_status"]),
        "",
        "## Branch Copies",
        markdown_table(rows_by_name["branch_copies"]),
        "",
        "## Validation",
        markdown_table(rows_by_name["validation"]),
        "",
        "## Plain-English Read",
        "",
        "- This is progress: `K_L` now has a plausible field-action origin instead of being just a formal tensor patch.",
        "- This is not a pass: the auxiliary cure brings a new `lambda_phi` stress gate, and we cannot wish it away.",
        "- The next best shot is clean: prove `lambda_phi=0` from parent boundary/no-flux/zero-mode data, or write a finite stress-bound row with units and observable projection.",
        "- If that closes, Khat adoption and DeltaK can be revisited; if it fails, the branch stays an explicit residual route rather than a local-GR derivation.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "improvement_rollforward": improvement_rollforward_rows(),
        "lambda_phi_gate": lambda_phi_gate_rows(),
        "deltak_kbar_status": deltak_kbar_status_rows(),
        "claim_gates": claim_gate_rows(),
        "current_blocker_stack": blocker_stack_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
        "branch_copies": branch_copy_rows(),
    }

    generated_paths = dict(OUTPUTS)
    generated_paths.update(BRANCH_OUTPUTS)
    generated_paths["doc"] = DOC_PATH

    write_csv(OUTPUTS["source_register"], rows_by_name["source_register"])
    write_csv(OUTPUTS["improvement_rollforward"], rows_by_name["improvement_rollforward"])
    write_csv(OUTPUTS["lambda_phi_gate"], rows_by_name["lambda_phi_gate"])
    write_csv(OUTPUTS["deltak_kbar_status"], rows_by_name["deltak_kbar_status"])
    write_csv(OUTPUTS["claim_gates"], rows_by_name["claim_gates"])
    write_csv(OUTPUTS["current_blocker_stack"], rows_by_name["current_blocker_stack"])
    write_csv(OUTPUTS["decision_ledger"], rows_by_name["decision_ledger"])
    write_csv(OUTPUTS["next_target"], rows_by_name["next_target"])
    write_csv(OUTPUTS["project_status"], rows_by_name["project_status"])
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    write_csv(BRANCH_OUTPUTS["local_bounds_gate"], rows_by_name["improvement_rollforward"])
    write_csv(BRANCH_OUTPUTS["deltak_gate"], rows_by_name["deltak_kbar_status"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    rows_by_name["validation"] = validation_rows(rows_by_name, generated_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    overall = next(row for row in rows_by_name["validation"] if row["validation_id"] == "VAL2713_OVERALL")
    print(f"2713 complete: {overall['passed']} - {overall['details']}")
    print(DOC_PATH)


if __name__ == "__main__":
    main()
