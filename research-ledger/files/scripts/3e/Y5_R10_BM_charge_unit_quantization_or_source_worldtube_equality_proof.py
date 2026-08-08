from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "926-Y5-R10-BM-charge-unit-quantization-or-source-worldtube-equality-proof.md"
STATUS = "Y5_R10_926_compact_BF_lattice_theorem_conditional_BM_unit_and_JHH_source_equality_not_parent_signed"
CLAIM_CEILING = "compact_BF_lattice_contract_only_no_numeric_KBFH_ratio_no_WEP_R10_PPN_Newton_or_local_GR_claim"
NEXT_TARGET = "927-Y5-R10-compact-BF-lattice-parent-action-contract-or-JHH-source-proof.md"
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
            "source_id": "925_doc",
            "path": "925-Y5-R10-KBFH-over-kM-ratio-from-source-worldtube-or-FM-bound-row-fill.md",
            "role": "immediate R_BJ ratio lock and 926 target",
            "needle": "R_BJ := (integral_boundaryC B_M)/(integral_C J_H^H)",
        },
        {
            "source_id": "925_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_925_VALIDATION.csv",
            "role": "proves 925 validation passed",
            "needle": "V925_12_validation_rows_ready",
        },
        {
            "source_id": "287_boundary_current",
            "path": "287-boundary-current-charge-owner-attempt.md",
            "role": "relative boundary-current machinery and charge-unit failure",
            "needle": "charge unit `Q_*` derived",
        },
        {
            "source_id": "252_topological_projector",
            "path": "252-topological-projector-parent-action-skeleton.md",
            "role": "topological/relative action safety route",
            "needle": "metric-independent relative projector + exact/topological action",
        },
        {
            "source_id": "536_worldtube_glue",
            "path": "536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md",
            "role": "Hilbert-worldtube theorem target and topological boundary match gap",
            "needle": "HWT536_4_topological_boundary_match",
        },
        {
            "source_id": "537_parent_contract",
            "path": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
            "role": "parent-action contract requiring Hilbert/topological charge equality",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
        },
        {
            "source_id": "541_source_measure_contract",
            "path": "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
            "role": "Hamiltonian PiM source-measure contract",
            "needle": "HSM541_2_observed_worldtube_source",
        },
        {
            "source_id": "542_source_measure_attempt",
            "path": "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
            "role": "conditional source-measure theorem and first residual template",
            "needle": "SMT542_2_observed_worldtube_source",
        },
        {
            "source_id": "925_BM_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_925_BM_CHARGE_UNIT_AUDIT.csv",
            "role": "B_M unit blocker from prior ratio audit",
            "needle": "MISSING_BM_CHARGE_UNIT",
        },
        {
            "source_id": "925_worldtube_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_925_WORLD_TUBE_SOURCE_AUDIT.csv",
            "role": "J_H^H to Q_tau blocker from prior ratio audit",
            "needle": "MISSING_JHH_QTAU_EQUALITY",
        },
        {
            "source_id": "worldtube_certificate",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "role": "explicit missing certificates for Hilbert/topological worldtube glue",
            "needle": "HWG535_2_topological_representative_matches_worldtube_boundary",
        },
        {
            "source_id": "parent_worldtube_clauses",
            "path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "role": "parent worldtube source-measure glue clauses",
            "needle": "W504_4_worldtube_source_measure_glue",
        },
        {
            "source_id": "Hamiltonian_source_measure_contract",
            "path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "role": "source-measure gates for observed worldtube and Gauss readout",
            "needle": "HSM541_5_Gauss_orbital_readout",
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
            "current_result": "a compact BF lattice would fix the ratio to an integer/rational lattice ratio, but current MTS has not parent-signed the compact lattice or the source-worldtube equality",
            "what_changed": "B_M charge-unit language is now a precise compactness/period/source-lattice contract instead of vague coupling normalization",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def bf_lattice_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "BF926_0_compact_fields",
            "claim": "A_M and B_M are compact gauge fields with integral periods in normalized variables a_M=A_M/(2*pi), b_M=B_M/(2*pi).",
            "mathematical_form": "integral_gamma da_M in Z; integral_Sigma b_M in Z on allowed cycles/surfaces",
            "derived_effect": "makes boundary B_M charge a lattice object rather than an arbitrary real normalization",
            "current_MTS_status": "not_parent_signed",
            "missing_certificate": "MISSING_COMPACT_BF_GAUGE_GROUP_AND_PERIODS",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "BF926_1_quantized_BF_level",
            "claim": "Large gauge invariance of the exponentiated BF action quantizes the BF level.",
            "mathematical_form": "S_BF = 2*pi*k_M int b_M wedge da_M with k_M in Z",
            "derived_effect": "prevents k_M from being a post-fit continuous coupling",
            "current_MTS_status": "conditional_BF_lattice_theorem",
            "missing_certificate": "MISSING_PARENT_ACTION_LARGE_GAUGE_INVARIANCE_PROOF",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "BF926_2_quantized_source_current",
            "claim": "The Hilbert source current appearing in A_M wedge J_H^H is on the same integral source lattice.",
            "mathematical_form": "int_C j_H^H = N_H in Z, with j_H^H the normalized source 3-current",
            "derived_effect": "sets the denominator of R_BJ by source charge, not by orbital fitting",
            "current_MTS_status": "not_parent_signed",
            "missing_certificate": "MISSING_JHH_INTEGRAL_SOURCE_LATTICE",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "BF926_3_boundary_flux_integer",
            "claim": "The B_M flux through the linked boundary is an integer lattice charge.",
            "mathematical_form": "int_boundaryC b_M = N_B in Z",
            "derived_effect": "sets the numerator of R_BJ by the boundary class linked to the source",
            "current_MTS_status": "not_parent_signed",
            "missing_certificate": "MISSING_BM_BOUNDARY_PERIOD_AND_LINKING_CLASS",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "BF926_4_ratio_lattice",
            "claim": "If BF926_0 through BF926_3 and the source equation hold, the ratio is fixed by lattice integers.",
            "mathematical_form": "K_BF_H/k_M = R_BJ = N_B/N_H up to orientation/sign and normalization convention",
            "derived_effect": "turns the coupling into a topological/source-lattice ratio",
            "current_MTS_status": "conditional_theorem_only",
            "missing_certificate": "MISSING_SINGLE_SOURCE_MINIMALITY_OR_INTEGER_PAIR_NB_NH",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "BF926_5_minimal_source_special_case",
            "claim": "For a single minimal source in the same boundary class, the conditional lattice ratio would reduce to plus/minus one.",
            "mathematical_form": "if N_B=N_H=1, then K_BF_H/k_M = +/-1",
            "derived_effect": "gives a clean candidate target for a future parent proof",
            "current_MTS_status": "not_claimed_for_current_MTS",
            "missing_certificate": "MISSING_MINIMAL_SOURCE_NORMALIZATION_AND_SAME_CLASS_PROOF",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def source_worldtube_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "SWT926_0_observed_source_support",
            "target_identity": "W_source is fixed by the support of the observed Hilbert source current before readout.",
            "mathematical_form": "W_source = supp(J_H[e_obs])",
            "attempt_result": "definition is coherent and already appears in the 536/537/541 contracts",
            "current_gap": "same observed matter frame and support selector are not derived from the current parent action",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "SWT926_1_Hilbert_to_Hamiltonian_charge",
            "target_identity": "integral_C J_H^H equals the Hamiltonian/covariant-phase-space source charge Q_tau.",
            "mathematical_form": "integral_C J_H^H = Q_tau[W] = H_tau[S] - H_ref",
            "attempt_result": "conditional if integrable charge, fixed reference, and source-measure glue pass",
            "current_gap": "HSM541_1 and HSM541_2 remain not derived",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "SWT926_2_topological_boundary_match",
            "target_identity": "B_M boundary class links the same Hilbert worldtube and not a separate topological label.",
            "mathematical_form": "int_boundary(W_source) omega_M_top = 1 and no independent source label",
            "attempt_result": "needed certificate is explicit in HWG535_2/HWT536_4/PAC537_5",
            "current_gap": "certificate_missing; topology could still conserve the wrong object",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "SWT926_3_Gauss_readout_after_glue",
            "target_identity": "Q_tau controls measured matter-frame Poisson/Gauss/orbital GM only after the charge glue.",
            "mathematical_form": "surface_integral grad Phi dot dS = 4*pi*G_ref*Q_tau and a_r=-G_ref*Q_tau/r^2",
            "attempt_result": "conditional from source-measure plus Gauss/orbital readout contracts",
            "current_gap": "HSM541_5 and PG4/PG5 remain not derived",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def ratio_evaluator_rows() -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "RATIO926_0_symbolic_current",
            "ratio_formula": "K_BF_H/k_M = R_BJ = (integral_boundaryC B_M)/(integral_C J_H^H)",
            "needed_inputs": "B_M period; J_H^H source lattice; source-worldtube equality; Gauss/orbital readout",
            "numeric_value": "MISSING_NUMERIC_R_BJ",
            "status": "current_claim_blocked",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "candidate_id": "RATIO926_1_compact_lattice_conditional",
            "ratio_formula": "R_BJ = N_B/N_H up to sign",
            "needed_inputs": "compact BF gauge group; integer periods; same source boundary class",
            "numeric_value": "CONDITIONAL_INTEGER_RATIO_ONLY",
            "status": "conditional_not_current_MTS_claim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "candidate_id": "RATIO926_2_minimal_link_conditional",
            "ratio_formula": "R_BJ = +/-1 when N_B=N_H=1",
            "needed_inputs": "minimal source normalization; single-link certificate; no extra/source/frame/boundary charge",
            "numeric_value": "REFERENCE_TARGET_NOT_EVIDENCE",
            "status": "not_accepted_for_claim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def fm_readiness_rows() -> list[dict[str, object]]:
    return [
        {
            "check_id": "FMREADY926_0_ratio_value",
            "requirement": "numeric/unit-complete K_BF_H/k_M",
            "current_status": "missing_numeric_R_BJ",
            "blocks_rows": "WEP;clock;gamma;beta;R10",
            "next_action": "prove compact BF lattice and source integer pair or retain residual",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "FMREADY926_1_source_glue",
            "requirement": "integral_C J_H^H = Q_tau = M_source",
            "current_status": "not_parent_derived",
            "blocks_rows": "source_charge;WEP;Gauss;Newton",
            "next_action": "prove observed worldtube source equality from parent matter action",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "FMREADY926_2_same_class",
            "requirement": "B_M boundary lattice links the same Hilbert source worldtube",
            "current_status": "certificate_missing",
            "blocks_rows": "wrong_topological_charge_credit",
            "next_action": "write compact BF lattice parent-action contract with same-class certificate",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "FMREADY926_3_projection_coefficients",
            "requirement": "observable projection coefficients for WEP/clock/PPN/R10",
            "current_status": "not_linearized_after_normalization",
            "blocks_rows": "FM bound scoring",
            "next_action": "linearize only after ratio/source glue exists",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK926_0_compact_BF_parent_action",
            "missing_input": "parent-signed compact BF gauge group and large-gauge invariance",
            "why_needed": "turns B_M periods and k_M into a lattice theorem",
            "next_action": "write/check compact BF lattice parent-action contract",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK926_1_BM_boundary_period",
            "missing_input": "integral_boundaryC b_M = N_B with fixed orientation/linking class",
            "why_needed": "sets numerator of K_BF_H/k_M",
            "next_action": "derive boundary period and same-class link certificate",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK926_2_JHH_integral_lattice",
            "missing_input": "integral_C j_H^H = N_H and integral_C J_H^H = Q_tau = M_source",
            "why_needed": "sets denominator and prevents wrong-source coupling",
            "next_action": "prove observed Hilbert source current is the same source lattice current",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK926_3_Gauss_orbital_readout",
            "missing_input": "Q_tau is measured matter-frame GM after source glue",
            "why_needed": "connects ratio to Newton/PPN/local tests",
            "next_action": "close Gauss/Poisson/orbital readout or keep residual rows blocked",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD926_0_derivation_result",
            "branch": "B_M_charge_unit",
            "verdict": "conditional_compact_BF_lattice_theorem_only",
            "reason": "compact BF quantization would fix R_BJ as N_B/N_H, but current MTS has not parent-signed the lattice or integer source pair",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD926_1_source_worldtube",
            "branch": "J_HH_Qtau_Msource",
            "verdict": "not_derived_current_MTS",
            "reason": "observed worldtube/source-measure equality remains a contract, not a theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD926_2_next",
            "branch": "next_derivation_target",
            "verdict": "selected",
            "reason": "the next useful move is a compact BF lattice parent-action contract with same-worldtube source proof clauses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE926_0_numeric_KBFH_ratio",
            "claim": "K_BF_H/k_M has a claim-ready numerical value",
            "blocker": "only conditional N_B/N_H lattice theorem; no parent-signed N_B,N_H",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE926_1_source_worldtube_equality",
            "claim": "integral_C J_H^H = Q_tau = M_source",
            "blocker": "same observed Hilbert worldtube and Hamiltonian source charge not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE926_2_FM_local_bounds",
            "claim": "WEP/R10/clock/PPN bound rows can score",
            "blocker": "ratio/source glue and projection coefficients are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE926_3_Newton_local_GR",
            "claim": "source-normalized Newton or local GR follows",
            "blocker": "Gauss/orbital readout, extra-sector silence, and PPN followthrough remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "write the exact compact BF lattice parent-action contract and test whether it supplies B_M periods, source integer charge, and same-worldtube equality",
            "include": "compact gauge group, large gauge invariance, integer periods, source-current lattice, same Hilbert worldtube boundary class, R_BJ=N_B/N_H gate",
            "exclude": "numeric pass claims, minimal-link ratio promotion without proof, post-fit G/M absorption, GitHub action, formalization-workbench edits",
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
    bf_lattice: list[dict[str, object]],
    source_worldtube: list[dict[str, object]],
    ratio_eval: list[dict[str, object]],
    fm_ready: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_925_VALIDATION.csv"
    prior_rows = read_csv(prior) if prior.exists() else []
    prior_ok = bool(prior_rows) and all(row.get("result") == "pass" for row in prior_rows)
    conditional_lattice = any("N_B/N_H" in str(row.get("mathematical_form", "")) for row in bf_lattice)
    no_numeric_claim = all(str(row.get("valid_for_claim", "")).lower() == "false" for row in ratio_eval)
    source_gap = any("not derived" in str(row.get("current_gap", "")).lower() for row in source_worldtube)
    readiness_blocked = all(row.get("valid_for_claim") == "false" for row in fm_ready) and len(fm_ready) >= 4
    generated = bf_lattice + source_worldtube + ratio_eval + fm_ready + blockers + decisions + gates
    changed = formalization_changed_count()
    false_fields = ("claim_allowed", "valid_for_claim")
    return [
        {
            "check_id": "V926_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source path or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_1_prior_925_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_925_VALIDATION.csv clean" if prior_ok else "925 validation missing or not clean",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_2_compact_BF_lattice_theorem_written",
            "result": "pass" if conditional_lattice else "fail",
            "detail": "conditional R_BJ=N_B/N_H lattice theorem is written",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_3_no_numeric_ratio_claim",
            "result": "pass" if no_numeric_claim else "fail",
            "detail": "no numeric K_BF_H/k_M value is accepted for claim",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_4_source_worldtube_gap_visible",
            "result": "pass" if source_gap else "fail",
            "detail": "J_H^H to Q_tau/M_source equality remains an explicit gap",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_5_FM_readiness_blocked",
            "result": "pass" if readiness_blocked else "fail",
            "detail": "FM numeric-readiness checklist remains nonclaim and blocked",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_6_blockers_explicit",
            "result": "pass" if len(blockers) >= 4 and all_false(blockers, ("valid_for_claim",)) else "fail",
            "detail": "compact BF, B_M period, J_HH lattice, and Gauss/orbital blockers are listed",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_7_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "numeric ratio, source equality, local-bound, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_8_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_9_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_10_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("927-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V926_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    bf_lattice: list[dict[str, object]],
    source_worldtube: list[dict[str, object]],
    ratio_eval: list[dict[str, object]],
    fm_ready: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 926 - Y5/R10 B_M Charge-Unit Quantization Or Source-Worldtube Equality Proof

Private charge-unit checkpoint. This is not a public WEP, clock, PPN, R10, Newton, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the best derivation route is a compact BF lattice theorem, but current MTS has not earned the lattice yet.**

The clean conditional result is:

```text
If A_M and B_M are compact BF gauge fields,
and int_boundaryC b_M = N_B,
and int_C j_H^H = N_H,
and both integers refer to the same Hilbert source worldtube,
then K_BF_H/k_M = R_BJ = N_B/N_H up to orientation/sign.
```

That is progress: the missing coupling has stopped being a mystery knob. It is now a very concrete parent-action demand: compact gauge periods plus a same-worldtube source lattice. But because the current corpus has not proved those periods or the equality `integral_C J_H^H = Q_tau = M_source`, no numeric ratio or local-GR claim is promoted.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Compact BF Lattice Theorem Attempt

{md_table(bf_lattice, ["clause_id", "claim", "mathematical_form", "derived_effect", "current_MTS_status", "missing_certificate", "valid_for_claim", "generated_utc"])}

## Source-Worldtube Equality Attempt

{md_table(source_worldtube, ["step_id", "target_identity", "mathematical_form", "attempt_result", "current_gap", "valid_for_claim", "generated_utc"])}

## Ratio Branch Evaluator

{md_table(ratio_eval, ["candidate_id", "ratio_formula", "needed_inputs", "numeric_value", "status", "valid_for_claim", "generated_utc"])}

## FM Numeric-Readiness Checklist

{md_table(fm_ready, ["check_id", "requirement", "current_status", "blocks_rows", "next_action", "valid_for_claim", "generated_utc"])}

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
    bf_lattice = bf_lattice_theorem_rows()
    source_worldtube = source_worldtube_attempt_rows()
    ratio_eval = ratio_evaluator_rows()
    fm_ready = fm_readiness_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(sources, bf_lattice, source_worldtube, ratio_eval, fm_ready, blockers, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_926_SOURCE_REGISTER.csv", sources, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_BF_LATTICE_THEOREM_ATTEMPT.csv", bf_lattice, ["clause_id", "claim", "mathematical_form", "derived_effect", "current_MTS_status", "missing_certificate", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv", source_worldtube, ["step_id", "target_identity", "mathematical_form", "attempt_result", "current_gap", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_RATIO_BRANCH_EVALUATOR.csv", ratio_eval, ["candidate_id", "ratio_formula", "needed_inputs", "numeric_value", "status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_FM_NUMERIC_READINESS_CHECKLIST.csv", fm_ready, ["check_id", "requirement", "current_status", "blocks_rows", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_926_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_926_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(sources, summary, bf_lattice, source_worldtube, ratio_eval, fm_ready, blockers, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
