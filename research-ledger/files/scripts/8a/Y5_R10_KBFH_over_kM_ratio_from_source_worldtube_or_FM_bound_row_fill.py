from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "925-Y5-R10-KBFH-over-kM-ratio-from-source-worldtube-or-FM-bound-row-fill.md"
STATUS = "Y5_R10_925_KBFH_over_kM_ratio_defined_symbolically_source_worldtube_and_BM_unit_still_open_FM_rows_filled_nonclaim"
CLAIM_CEILING = "KBFH_over_kM_ratio_symbolic_only_no_WEP_R10_PPN_Newton_or_local_GR_claim"
NEXT_TARGET = "926-Y5-R10-BM-charge-unit-quantization-or-source-worldtube-equality-proof.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "924_doc",
            "path": "924-Y5-R10-Hamiltonian-mass-charge-normalization-contract-or-FM-bound-row-expansion.md",
            "role": "immediate symbolic K_BF_H/k_M ratio and 925 target",
            "needle": "K_BF_H/k_M = (integral_boundaryC B_M)/(integral_C J_H^H)",
        },
        {
            "source_id": "924_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_924_VALIDATION.csv",
            "role": "proves 924 validation passed",
            "needle": "V924_11_validation_rows_ready",
        },
        {
            "source_id": "924_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_924_HAMILTONIAN_NORMALIZATION_CONTRACT.csv",
            "role": "contract rows giving HMC924_3 integrated ratio and blockers",
            "needle": "HMC924_3_integrated_ratio",
        },
        {
            "source_id": "924_FM_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_924_FM_BOUND_ROW_EXPANSION.csv",
            "role": "blocked FM WEP/clock/gamma/beta rows to fill with ratio placeholders",
            "needle": "FM924_0_R1_WEP_source_charge",
        },
        {
            "source_id": "287_boundary_current",
            "path": "287-boundary-current-charge-owner-attempt.md",
            "role": "relative boundary-current conservation without normalized charge unit",
            "needle": "Q_B[D] = integral_D j_3 - integral_boundaryD b_2.",
        },
        {
            "source_id": "252_topological_projector",
            "path": "252-topological-projector-parent-action-skeleton.md",
            "role": "metric-independent topological/relative action route and source-normalization warning",
            "needle": "metric-independent relative projector + exact/topological action",
        },
        {
            "source_id": "457_Hamiltonian_charge",
            "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
            "role": "Hamiltonian boundary-charge route and Poisson/Gauss bridge warning",
            "needle": "Poisson_Gauss_bridge",
        },
        {
            "source_id": "458_Poisson_Gauss",
            "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
            "role": "conditional measured-GM calibration theorem and failure channels",
            "needle": "conditional_Poisson_Gauss_calibration_theorem",
        },
        {
            "source_id": "505_Noether_mass_charge",
            "path": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
            "role": "worldtube source measure equality remains a core glue premise",
            "needle": "worldtube source measure equals the exterior parent mass charge",
        },
        {
            "source_id": "Hamiltonian_charge_contract",
            "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "role": "HC0-HC9 Hamiltonian source-normalization requirements",
            "needle": "HC8_Poisson_Gauss_orbital_calibration",
        },
        {
            "source_id": "Poisson_Gauss_contract",
            "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
            "role": "PG0-PG10 measured-GM bridge requirements",
            "needle": "PG4_Gauss_surface_integral",
        },
        {
            "source_id": "Hilbert_monopole_contract",
            "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
            "role": "Hilbert current to absolute monopole calibration requirements",
            "needle": "HM3_absolute_monopole_calibration",
        },
        {
            "source_id": "q_retained_zero_conditions",
            "path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
            "role": "forbids erasing boundary/source residuals without a zero theorem or executable row",
            "needle": "Q1_gauge_or_topological",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "K_BF_H/k_M is exactly locked to R_BJ = (integral_boundaryC B_M)/(integral_C J_H^H), but R_BJ is still symbolic",
            "what_changed": "the ratio problem is now split into B_M charge unit, J_H^H=Q_tau source equality, Gauss/Poisson calibration, and observable projection coefficients",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def ratio_derivation_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "R925_0_parent_equation",
            "derivation_clause": "Start from S_M = k_M integral B_M wedge dA_M + K_BF_H integral A_M wedge J_H^H.",
            "mathematical_result": "delta_A S_M = 0 implies k_M dB_M = K_BF_H J_H^H up to orientation convention.",
            "status": "algebraic_from_924_not_parent_promoted",
            "missing_for_numeric_value": "fixed B_M and J_H^H charge units",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "R925_1_integrate_chain",
            "derivation_clause": "Integrate the source equation over a compact source/exterior 3-chain C whose boundary links the source worldtube.",
            "mathematical_result": "k_M integral_boundaryC B_M = K_BF_H integral_C J_H^H.",
            "status": "symbolic_chain_identity",
            "missing_for_numeric_value": "orientation, boundary class, B_M period, and J_H^H source class",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "R925_2_ratio_definition",
            "derivation_clause": "Define the source-worldtube ratio R_BJ before any orbital readout.",
            "mathematical_result": "K_BF_H/k_M = R_BJ, where R_BJ := (integral_boundaryC B_M)/(integral_C J_H^H).",
            "status": "exact_symbolic_ratio_lock",
            "missing_for_numeric_value": "numeric/unit-complete R_BJ",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "R925_3_unit_reduction_if_parent_signed",
            "derivation_clause": "If integral_boundaryC B_M = n_B q_B and integral_C J_H^H = Q_tau = M_source, then the ratio is fixed by source charge units.",
            "mathematical_result": "K_BF_H/k_M = n_B q_B / Q_tau.",
            "status": "conditional_unit_reduction_only",
            "missing_for_numeric_value": "parent-signed q_B, integer/linking number n_B, and Q_tau=M_source",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "R925_4_Gauss_Poisson_readout",
            "derivation_clause": "To become measured Newtonian mass, Q_tau must be the same charge sourcing the matter-frame Poisson/Gauss law.",
            "mathematical_result": "integral_S grad Phi dot dS = 4 pi G_ref Q_tau and a_r = -G_ref Q_tau/r^2 only under the PG/HC/HM clauses.",
            "status": "conditional_calibration_not_parent_signed",
            "missing_for_numeric_value": "PG1, PG4, PG5, PG6, HC4, HC8, HM3",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "R925_5_no_absorption_shortcut",
            "derivation_clause": "A global constant can be calibrated only after derivative, source, range, boundary, and species channels are zero or retained.",
            "mathematical_result": "post-fit G/M absorption cannot supply K_BF_H/k_M or a local-GR pass.",
            "status": "overclaim_blocker",
            "missing_for_numeric_value": "zero theorems or executable residual rows for every failed channel",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def bm_charge_unit_rows() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "BM925_0_form_degree",
            "question": "Does B_M define the boundary charge integrated over partial C?",
            "evidence": "924 gives k_M integral_boundaryC B_M = K_BF_H integral_C J_H^H.",
            "status": "yes_symbolically",
            "blocker": "symbolic charge is not a normalized unit",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "BM925_1_relative_current_support",
            "question": "Does prior boundary-current machinery give conservation/invariance?",
            "evidence": "287 gives Q_B[D] = integral_D j_3 - integral_boundaryD b_2 and conditional variation invariance.",
            "status": "conditional_conservation_support",
            "blocker": "287 explicitly does not derive the normalized charge unit",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "BM925_2_topological_period",
            "question": "Does topological/relative action language select q_B or an integer period?",
            "evidence": "252 supports a metric-independent topological route with no bulk projector stress.",
            "status": "topological_safety_only",
            "blocker": "no Ward/index/period theorem fixes the B_M unit or level",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "BM925_3_unit_status",
            "question": "Can K_BF_H/k_M be numeric from B_M alone?",
            "evidence": "B_M boundary integral needs q_B and linking number n_B.",
            "status": "not_derived",
            "blocker": "MISSING_BM_CHARGE_UNIT; MISSING_LINKING_CLASS_NORMALIZATION",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def worldtube_source_rows() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "WT925_0_source_current_identity",
            "question": "Is J_H^H the observed Hilbert source current before readout?",
            "evidence": "HM0 supplies a conditional Hilbert/coframe current input.",
            "status": "conditional_only",
            "blocker": "same observed coframe and selector-blind matter/source action are not parent-signed here",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "WT925_1_Qtau_equality",
            "question": "Is integral_C J_H^H = Q_tau = M_source?",
            "evidence": "924 writes the required equality; 505 names worldtube source measure matching as core glue.",
            "status": "not_parent_derived",
            "blocker": "MISSING_JHH_QTAU_EQUALITY",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "WT925_2_Hamiltonian_charge_match",
            "question": "Does the Hamiltonian surface charge equal the projected Hilbert mass current?",
            "evidence": "HC4 and PG1 state this as required identity.",
            "status": "not_parent_derived",
            "blocker": "MISSING_HC4_PG1_SOURCE_CURRENT_WARD_IDENTITY",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "audit_id": "WT925_3_measured_GM_calibration",
            "question": "Does Q_tau source the matter-frame Poisson/Gauss/orbital monopole?",
            "evidence": "458 gives the conditional bridge and PG4-PG6 requirements.",
            "status": "conditional_not_parent_derived",
            "blocker": "MISSING_GAUSS_POISSON_ORBITAL_CALIBRATION",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def fm_fill_rows() -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_R10_924_FM_BOUND_ROW_EXPANSION.csv")
    rows: list[dict[str, object]] = []
    for index, prior in enumerate(prior_rows):
        prediction_symbol = prior["FM_prediction_symbol"]
        rows.append(
            {
                "fm_fill_id": f"FM925_{index}_{prior['local_bound_row']}",
                "source_924_row": prior["fm_bound_id"],
                "local_bound_row": prior["local_bound_row"],
                "observable": prior["observable"],
                "upper_bound": prior["upper_bound"],
                "bound_units": prior["bound_units"],
                "ratio_symbol": "R_BJ = (integral_boundaryC B_M)/(integral_C J_H^H)",
                "nonclaim_prediction_template": f"{prediction_symbol} = C_{prior['local_bound_row']}_FM * F_M(R_BJ, Q_tau, G_ref, projection_owner)",
                "missing_inputs": "NUMERIC_R_BJ; B_M_CHARGE_UNIT; J_HH_QTAU_EQUALITY; GAUSS_POISSON_CALIBRATION; OBSERVABLE_PROJECTION_COEFFICIENT",
                "score_status": "blocked_symbolic_ratio_only",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK925_0_numeric_R_BJ",
            "missing_input": "numeric/unit-complete R_BJ",
            "why_needed": "turns the exact symbolic ratio into a prediction rather than a placeholder",
            "next_action": "derive B_M charge unit and J_H^H source-worldtube normalization",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK925_1_BM_charge_unit",
            "missing_input": "q_B and linking/period normalization for integral_boundaryC B_M",
            "why_needed": "sets the numerator of K_BF_H/k_M",
            "next_action": "attempt B_M charge-unit quantization or period theorem",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK925_2_JHH_Qtau_equality",
            "missing_input": "integral_C J_H^H = Q_tau = M_source",
            "why_needed": "sets the denominator of K_BF_H/k_M and prevents wrong-charge credit",
            "next_action": "prove source-worldtube equality from parent matter action or retain residual",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK925_3_Gauss_Poisson_calibration",
            "missing_input": "Q_tau controls measured matter-frame Phi and orbital GM",
            "why_needed": "connects the ratio to Newton/PPN/local-bound observables",
            "next_action": "close PG1/PG4/PG5/PG6 or map to residual rows",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK925_4_projection_coefficients",
            "missing_input": "C_eta_FM, C_clock_FM, C_gamma_FM, C_beta_FM",
            "why_needed": "maps epsilon_FM into WEP, clock, gamma, and beta bound rows",
            "next_action": "linearize after normalization or keep rows blocked",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD925_0_ratio",
            "branch": "KBFH_over_kM_ratio",
            "verdict": "symbolic_ratio_lock_only",
            "reason": "K_BF_H/k_M is exactly R_BJ, but R_BJ has no parent-derived numerical/unit value",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD925_1_BM_unit",
            "branch": "B_M_charge_unit",
            "verdict": "open",
            "reason": "relative/topological boundary-current machinery supports conservation but not the charge unit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD925_2_worldtube",
            "branch": "J_HH_source_worldtube",
            "verdict": "open",
            "reason": "worldtube source measure equality remains a core glue premise rather than a signed theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD925_3_next",
            "branch": "next_derivation_target",
            "verdict": "selected",
            "reason": "the cleanest next fight is the B_M charge-unit quantization theorem or direct source-worldtube equality proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE925_0_KBFH_value",
            "claim": "K_BF_H/k_M is numerically fixed",
            "blocker": "R_BJ is symbolic; B_M unit and J_H^H source equality are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE925_1_WEP_R10_PPN",
            "claim": "FM local-bound rows can score",
            "blocker": "no numeric R_BJ and no observable projection coefficients",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE925_2_measured_GM",
            "claim": "Hamiltonian/source charge equals measured Newtonian GM",
            "blocker": "Gauss/Poisson/orbital calibration remains conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE925_3_local_GR",
            "claim": "local Newton/PPN/local-GR branch passes",
            "blocker": "first-order source calibration, second-order PPN, and extra-sector silence remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to derive the B_M charge unit/period or prove integral_C J_H^H = Q_tau = M_source from the parent source worldtube",
            "include": "B_M quantization/period theorem, source-worldtube equality, Gauss/Poisson calibration hooks, FM row numeric-readiness checklist",
            "exclude": "numeric pass claims, post-fit G/M absorption, topological wrong-charge credit, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    sources: list[dict[str, object]],
    ratio: list[dict[str, object]],
    bm_unit: list[dict[str, object]],
    worldtube: list[dict[str, object]],
    fm_fill: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_924_VALIDATION.csv"
    prior_rows = read_csv(prior) if prior.exists() else []
    prior_ok = bool(prior_rows) and all(row.get("result") == "pass" for row in prior_rows)
    ratio_lock_written = any("K_BF_H/k_M = R_BJ" in str(row["mathematical_result"]) for row in ratio)
    numeric_ratio_absent = not any(str(row.get("status", "")).lower() == "numeric_ratio_derived" for row in ratio)
    bm_unit_open = any("MISSING_BM_CHARGE_UNIT" in str(row.get("blocker", "")) for row in bm_unit)
    worldtube_open = any("MISSING_JHH_QTAU_EQUALITY" in str(row.get("blocker", "")) for row in worldtube)
    fm_rows_blocked = len(fm_fill) >= 4 and all(row["valid_for_claim"] == "false" and "blocked" in str(row["score_status"]) for row in fm_fill)
    generated = ratio + bm_unit + worldtube + fm_fill + blockers + decisions + gates
    changed = formalization_changed_count()
    false_fields = ("claim_allowed", "valid_for_claim")
    return [
        {
            "check_id": "V925_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source path or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_1_prior_924_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_924_VALIDATION.csv clean" if prior_ok else "924 validation missing or not clean",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_2_ratio_identity_written",
            "result": "pass" if ratio_lock_written else "fail",
            "detail": "K_BF_H/k_M = R_BJ symbolic identity is written",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_3_numeric_ratio_not_claimed",
            "result": "pass" if numeric_ratio_absent else "fail",
            "detail": "no numeric/unit-complete K_BF_H/k_M is claimed",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_4_BM_unit_open",
            "result": "pass" if bm_unit_open else "fail",
            "detail": "B_M charge unit/period blocker is explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_5_worldtube_equality_open",
            "result": "pass" if worldtube_open else "fail",
            "detail": "J_H^H to Q_tau/M_source equality blocker is explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_6_FM_fill_rows_blocked",
            "result": "pass" if fm_rows_blocked else "fail",
            "detail": "FM bound rows have nonclaim ratio templates and remain blocked",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_7_blockers_explicit",
            "result": "pass" if len(blockers) >= 5 and all_false(blockers, ("valid_for_claim",)) else "fail",
            "detail": "numeric R_BJ, B_M unit, J_HH/Q_tau, Gauss/Poisson, and projection blockers are listed",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_8_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "KBFH value, WEP/R10/PPN, measured-GM, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_9_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_10_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_11_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("926-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V925_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    ratio: list[dict[str, object]],
    bm_unit: list[dict[str, object]],
    worldtube: list[dict[str, object]],
    fm_fill: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 925 - Y5/R10 KBFH/kM Ratio From Source Worldtube Or FM Bound Row Fill

Private ratio checkpoint. This is not a public WEP, clock, PPN, R10, Newton, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the ratio is now cleanly isolated but still not numerically derived.**

From 924:

```text
k_M integral_boundaryC B_M = K_BF_H integral_C J_H^H,
K_BF_H/k_M = (integral_boundaryC B_M)/(integral_C J_H^H).
```

This checkpoint names the exact object:

```text
R_BJ := (integral_boundaryC B_M)/(integral_C J_H^H),
K_BF_H/k_M = R_BJ.
```

That is the useful lock. The missing physics is no longer vague coupling language: it is the `B_M` charge unit, the source-worldtube equality `integral_C J_H^H = Q_tau = M_source`, the Gauss/Poisson measured-GM bridge, and the observable projection coefficients.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Ratio Derivation Attempt

{md_table(ratio, ["step_id", "derivation_clause", "mathematical_result", "status", "missing_for_numeric_value", "valid_for_claim", "generated_utc"])}

## B_M Charge Unit Audit

{md_table(bm_unit, ["audit_id", "question", "evidence", "status", "blocker", "valid_for_claim", "generated_utc"])}

## Worldtube Source Audit

{md_table(worldtube, ["audit_id", "question", "evidence", "status", "blocker", "valid_for_claim", "generated_utc"])}

## FM Bound Row Fill

{md_table(fm_fill, ["fm_fill_id", "source_924_row", "local_bound_row", "observable", "upper_bound", "bound_units", "ratio_symbol", "nonclaim_prediction_template", "missing_inputs", "score_status", "valid_for_claim", "generated_utc"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = build_sources()
    summary = summary_rows()
    ratio = ratio_derivation_rows()
    bm_unit = bm_charge_unit_rows()
    worldtube = worldtube_source_rows()
    fm_fill = fm_fill_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(sources, ratio, bm_unit, worldtube, fm_fill, blockers, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_925_SOURCE_REGISTER.csv", sources, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_RATIO_DERIVATION_ATTEMPT.csv", ratio, ["step_id", "derivation_clause", "mathematical_result", "status", "missing_for_numeric_value", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_BM_CHARGE_UNIT_AUDIT.csv", bm_unit, ["audit_id", "question", "evidence", "status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_WORLD_TUBE_SOURCE_AUDIT.csv", worldtube, ["audit_id", "question", "evidence", "status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_FM_BOUND_ROW_FILL.csv", fm_fill, ["fm_fill_id", "source_924_row", "local_bound_row", "observable", "upper_bound", "bound_units", "ratio_symbol", "nonclaim_prediction_template", "missing_inputs", "score_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_925_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_925_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(sources, summary, ratio, bm_unit, worldtube, fm_fill, blockers, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
