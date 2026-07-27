from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1291"
TITLE = "1291-Y5-R10-RAB-strict-double-zero-parent-clause-or-chain-kernel-residual-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PARENT_CLAUSE_PATH = OUT_DIR / f"{PACK_ID}_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv"
VARIATION_PROOF_PATH = OUT_DIR / f"{PACK_ID}_VARIATION_PROOF_NONCLAIM.csv"
ADOPTION_GATES_PATH = OUT_DIR / f"{PACK_ID}_ADOPTION_GATES.csv"
RESIDUAL_BOUND_PATH = OUT_DIR / f"{PACK_ID}_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv"
DELTAK_STATUS_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_STATUS_UPDATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1291_VALIDATION.csv"


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
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PARENT_CLAUSE_PATH,
        VARIATION_PROOF_PATH,
        ADOPTION_GATES_PATH,
        RESIDUAL_BOUND_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1291_0_1290_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_NEXT_TARGET.csv",
            "needle": "NEXT1290_0_1291",
            "role": "handoff into strict double-zero parent clause or residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_1_1290_kernel_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv",
            "needle": "MKA1290_3_strict_double_zero_branch",
            "role": "strict double-zero is best low-scrutiny route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_2_1290_chain_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_FIXED_POINT_CHAIN_ZERO_ATTEMPT.csv",
            "needle": "FCZ1290_4_chain_zero_verdict",
            "role": "chain zero not yet claimed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_3_1290_residuals",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_KERNEL_RESIDUAL_ROWS_NONCLAIM.csv",
            "needle": "KRR1290_0_m_kernel_residual",
            "role": "m-chain residual to bound if clause fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_4_1290_L_residual",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_KERNEL_RESIDUAL_ROWS_NONCLAIM.csv",
            "needle": "KRR1290_1_Lcg_kernel_residual",
            "role": "Lcg-chain residual to bound if clause fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_5_1290_DeltaK",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_DELTAK_STATUS_UPDATE.csv",
            "needle": "DKU1290_2_DeltaK00_verdict",
            "role": "DeltaK00 narrowed but not computable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_6_514_contract_double_zero",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_5_double_zero",
            "role": "stress first variation must vanish",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_7_801_lemma",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_801_DOUBLE_ZERO_LEMMA.csv",
            "needle": "DZ801_1_norm_evenness",
            "role": "norm/evenness double-zero theorem if parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_8_801_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_801_PARENT_FIXED_POINT_CONTRACT.csv",
            "needle": "FPC801_2_even_scalar_readout",
            "role": "parent fixed-point readout contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_9_R11_parent_clause",
            "local_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv",
            "needle": "C1_composite_squared_selector",
            "role": "composite squared selector parent clause template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_10_R11_variation",
            "local_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv",
            "needle": "V1_composite_delta_zero",
            "role": "variation proof for composite squared selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_11_R11_gates",
            "local_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_GATES.csv",
            "needle": "G0_Yloc_parent_owned",
            "role": "parent ownership gate for local silence multiplet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_12_memory_origin",
            "local_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
            "needle": "O2_quadratic_gate_sufficient",
            "role": "quadratic gate sufficiency clue",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_13_min_parent",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_3_extra_field_silence",
            "role": "minimal parent extra-field silence block",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_14_fixed_point_conditions",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "needle": "FP511_1_double_zero_nonEH_coupling",
            "role": "double-zero fixed-point condition remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1291_15_1279_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1279_DOUBLE_ZERO_SILENCE_AUDIT.csv",
            "needle": "DZS1279_7_verdict",
            "role": "extra-sector silence not yet closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    parent_clause = [
        {
            "clause_id": "SDZ1291_0_local_zero_variable",
            "object": "z_m := m-m_* or parent norm R_m=G_AB Y_m^A Y_m^B",
            "parent_clause": "The compact local branch has a parent-owned zero variable z_m=0, derived from Euler/fixed-point equations rather than imposed as a readout selector.",
            "variation_consequence": "if z_m=0 is parent-owned, scalar activation can be built from z_m^2 or R_m so first variation vanishes",
            "required_sources": "parent action for m/Y_m; positive local operator; no source/boundary flux",
            "current_status": "CLAUSE_WRITTEN_NOT_PARENT_MATCHED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_801_PARENT_FIXED_POINT_CONTRACT.csv;source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "source_anchor": "FPC801_0_local_fixed_surface;FP511_0_stationary_local_vacuum",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SDZ1291_1_strict_F_form",
            "object": "F(m)",
            "parent_clause": "F(m)=(m-m_*)^2 H(m) with H smooth and finite on the local branch; equivalently F(0)=F_prime(0)=0 in the parent zero variable.",
            "variation_consequence": "F(m_*)=0 and F_prime(m_*)=0, so the m and L_cg metric-chain channels vanish to first variation when kernels are finite",
            "required_sources": "source-backed F form; m_* definition; smooth H; no inverse zero factors",
            "current_status": "STRICT_DOUBLE_ZERO_FORM_WRITTEN_NONCLAIM",
            "source_path": "source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv;source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
            "source_anchor": "L2_double_zero_sufficient;O2_quadratic_gate_sufficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SDZ1291_2_Lcg_status",
            "object": "L_cg",
            "parent_clause": "L_cg is either a finite parent scalar/global scale held fixed in local Hilbert variation, or all L_cg metric dependence is multiplied by the same strict double-zero F(m).",
            "variation_consequence": "the term -2 L_cg^-3 F(m_*) M_L^{00} vanishes by F(m_*)=0 even if M_L^{00} is finite",
            "required_sources": "parent definition of L_cg; finite nonzero L_cg; no singular H or inverse local-zero dependence",
            "current_status": "CLAUSE_WRITTEN_NOT_PARENT_MATCHED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "MKA1290_2_Lcg_metric_length_branch;GSE798_1_gradient_expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SDZ1291_3_no_multiplier_or_readout_cheat",
            "object": "selector stress",
            "parent_clause": "The double-zero is a composite/even scalar dependence in the action, not an independent multiplier constraint or post-readout switch.",
            "variation_consequence": "prevents Lambda_Sigma or post-hoc selector stress from reintroducing a first-variation source",
            "required_sources": "composite selector construction; multiplier absence or multiplier zero theorem; variation ledger",
            "current_status": "GUARD_WRITTEN",
            "source_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv;source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_GATES.csv",
            "source_anchor": "C3_no_independent_multiplier;G1_composite_not_independent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SDZ1291_4_boundary_domain_closure",
            "object": "K_conn,K_domain,K_boundary",
            "parent_clause": "Connection/domain/boundary terms are absent, topological/no-flux, or multiplied by the same parent-owned double-zero factor.",
            "variation_consequence": "prevents a killed chain term from being replaced by derivative/projector/worldtube stress",
            "required_sources": "boundary no-flux theorem; metric-free/topological projector or retained residual map",
            "current_status": "OPEN_GUARD_NOT_CLOSED",
            "source_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv;source-intake/mts_residuals/P8_Y5_R10_1290_KERNEL_RESIDUAL_ROWS_NONCLAIM.csv",
            "source_anchor": "V3_topological_boundary_terms;KRR1290_2_connection_domain_boundary_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SDZ1291_5_parent_clause_verdict",
            "object": "strict double-zero parent clause",
            "parent_clause": "SDZ1291_0..4 are sufficient to kill the first m/L_cg chain response locally, but current MTS has not yet matched all premises to a parent action.",
            "variation_consequence": "Kmetric_chain^{00}=0 remains a theorem target, not a local-GR result",
            "required_sources": "actual MTS source paths for m,L_cg,F,H,Y_m, boundary/domain closure",
            "current_status": "SUFFICIENT_CLAUSE_WRITTEN_CURRENT_CLAIM_BLOCKED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1290_FIXED_POINT_CHAIN_ZERO_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1279_DOUBLE_ZERO_SILENCE_AUDIT.csv",
            "source_anchor": "FCZ1290_4_chain_zero_verdict;DZS1279_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    variation_proof = [
        {
            "step_id": "VP1291_0_define_strict_F",
            "input": "Gamma_eff=L_cg^-2 F(m), F(m)=(m-m_*)^2 H(m)",
            "calculation": "F(m_*)=0 and F_prime(m)=2(m-m_*)H(m)+(m-m_*)^2 H_prime(m), so F_prime(m_*)=0",
            "result": "strict double zero at m=m_*",
            "assumptions": "H smooth finite; m_* parent-defined",
            "claim_status": "mathematical_identity_nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VP1291_1_metric_variation",
            "input": "delta Gamma_eff=L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg",
            "calculation": "evaluate at m=m_* gives delta Gamma_eff|_* = L_cg^-2*0*delta m - 2 L_cg^-3*0*delta L_cg = 0",
            "result": "m and L_cg chain-kernel terms vanish even when delta m/delta g and delta L_cg/delta g are finite",
            "assumptions": "finite metric kernels; no singular H/L_cg; algebraic Gamma term only",
            "claim_status": "conditional_variation_proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VP1291_2_gradient_variation",
            "input": "nabla Gamma_eff=L_cg^-2 F_prime(m)nabla m - 2 L_cg^-3 F(m)nabla L_cg",
            "calculation": "at locked m=m_* with F=F_prime=0, the local source-gradient channel vanishes provided the branch is actually locked and kernels are finite",
            "result": "q_loc source-gradient channel can be killed by the same strict double zero",
            "assumptions": "parent lock to m_*; no baseline drift; no transition layer gradient singularity",
            "claim_status": "conditional_source_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VP1291_3_second_order_residual",
            "input": "m=m_*+delta m",
            "calculation": "Gamma_eff=L_cg^-2 delta m^2 H(m_*+delta m), so residual amplitude starts at O(delta m^2) plus L_cg/boundary/domain terms",
            "result": "linear F_1 leakage is removed; remaining branch is quadratic or residual-ledger controlled",
            "assumptions": "delta m small by parent local operator; transition gradients bounded",
            "claim_status": "conditional_quadratic_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VP1291_4_proof_verdict",
            "input": "VP1291_0..3",
            "calculation": "the algebra closes, but the parent action has not yet been shown to contain this F form or to lock m=m_*",
            "result": "strict double-zero parent clause is a serious theorem target, not a completed derivation",
            "assumptions": "parent match still missing",
            "claim_status": "PROOF_CONDITIONAL_CURRENT_CLAIM_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    adoption_gates = [
        {
            "gate_id": "ADG1291_0_actual_F_form",
            "needed_for_adoption": "actual MTS Gamma_eff uses F(m)=(m-m_*)^2 H(m) or equivalent norm-square parent scalar",
            "current_evidence": "798 gives Gamma_eff=L_cg^-2 F(m), but not the strict F form",
            "status": "MISSING_ACTUAL_F_SOURCE",
            "failure_mode": "linear F_prime or nonzero F leaves KRR1290 residuals active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ADG1291_1_parent_lock",
            "needed_for_adoption": "local compact branch Euler equations force m=m_* without source or boundary flux",
            "current_evidence": "fixed-point contracts exist but are not matched to actual MTS fields",
            "status": "MISSING_PARENT_LOCK",
            "failure_mode": "delta m and transition gradients become physical fifth-force/PPN hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ADG1291_2_Lcg_finite_safe",
            "needed_for_adoption": "L_cg is finite/nonzero and has no singular inverse or metric-readout divergence at the local branch",
            "current_evidence": "L_cg appears in Gamma source expansion, but parent definition is not signed",
            "status": "MISSING_LCG_PARENT_DEFINITION",
            "failure_mode": "the L_cg channel becomes source-normalization or PPN hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ADG1291_3_gradient_control",
            "needed_for_adoption": "transition gradients are bounded so quadratic amplitude does not hide a large derivative source",
            "current_evidence": "801 gradient warning and 798 support-law verdict keep this open",
            "status": "MISSING_GRADIENT_POWER_PROOF",
            "failure_mode": "nabla Gamma_eff survives even if the amplitude is double-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ADG1291_4_boundary_domain_stress",
            "needed_for_adoption": "connection/domain/boundary terms vanish, are topological/no-flux, or are bounded",
            "current_evidence": "1290 retains R_cdb and R11 variation proof keeps boundary stress open",
            "status": "MISSING_CDB_ZERO_OR_BOUND",
            "failure_mode": "Delta_K^{00} remains incomplete and local-GR claim fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ADG1291_5_current_MTS_match",
            "needed_for_adoption": "the clause maps to current MTS variables rather than a new closure-only patch",
            "current_evidence": "1279 says extra-sector silence is not closed",
            "status": "MISSING_CURRENT_MTS_MATCH",
            "failure_mode": "route remains a clean closure candidate, not a derivation of the existing framework",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_bound = [
        {
            "bound_id": "KRB1291_0_m_chain_bound",
            "residual_component": "R_m^{00}",
            "bound_form": "|R_m^{00}| <= |C_sign| L_cg^-2 |F_prime(m)| |M_m^{00}|",
            "zero_or_small_route": "strict double zero gives F_prime(m_*)=0; near branch F_prime=O(|m-m_*|)",
            "needed_inputs": "MISSING_m_PROFILE;MISSING_F_PRIME_BOUND;MISSING_M_m_00_BOUND;MISSING_C_SIGN;MISSING_OBSERVABLE_RESPONSE",
            "maps_to_tests": "Newton_source;PPN;clock;orbital;R10_if_range_component",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "KRB1291_1_Lcg_chain_bound",
            "residual_component": "R_L^{00}",
            "bound_form": "|R_L^{00}| <= 2 |C_sign| L_cg^-3 |F(m)| |M_L^{00}|",
            "zero_or_small_route": "strict double zero gives F(m_*)=0; near branch F=O((m-m_*)^2)",
            "needed_inputs": "MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_M_L_00_BOUND;MISSING_LCG_LOWER_BOUND;MISSING_OBSERVABLE_RESPONSE",
            "maps_to_tests": "Newton_source;PPN;clock;orbital;source_normalization",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "KRB1291_2_cdb_bound",
            "residual_component": "R_cdb^{00}",
            "bound_form": "|R_cdb^{00}| <= |K_conn^{00}|+|K_domain^{00}|+|K_boundary^{00}|",
            "zero_or_small_route": "topological/projector metric-silence or no-flux boundary theorem; otherwise explicit residual bounds",
            "needed_inputs": "MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND;MISSING_NO_FLUX_SOURCE;MISSING_RESPONSE_LIMIT",
            "maps_to_tests": "PPN;clock;orbital;boundary_mass_flux",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "KRB1291_3_residual_verdict",
            "residual_component": "chain_kernel_residual_vector",
            "bound_form": "R_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}",
            "zero_or_small_route": "claim allowed only if SDZ gates pass or every KRB row receives sourced numeric/theorem bounds below response limits",
            "needed_inputs": "MISSING_ALL_KRB_NUMERIC_OR_THEOREM_INPUTS",
            "maps_to_tests": "all_local",
            "current_status": "RESIDUAL_VECTOR_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    deltak_status = [
        {
            "status_id": "DKS1291_0_chain_clause",
            "object": "Kmetric_chain^{00}",
            "status": "STRICT_DOUBLE_ZERO_CLAUSE_WRITTEN_NOT_ADOPTED",
            "formula": "if F=(m-m_*)^2H and m=m_* locally, then R_m^{00}=R_L^{00}=0 to first variation",
            "remaining_missing": "MISSING_ACTUAL_F_SOURCE;MISSING_PARENT_LOCK;MISSING_GRADIENT_CONTROL;MISSING_CDB_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKS1291_1_residual_bound_branch",
            "object": "Kmetric_chain_residual",
            "status": "BOUND_LEDGER_STAGED",
            "formula": "R_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}",
            "remaining_missing": "MISSING_PROFILES;MISSING_KERNEL_BOUNDS;MISSING_RESPONSE_LIMITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKS1291_2_DeltaK00",
            "object": "Delta_K^{00}",
            "status": "NOT_COMPUTABLE_YET",
            "formula": "Delta_K^{00}=K_L^{00}-[Kmetric_volume^{00}+R_chain^{00}]",
            "remaining_missing": "MISSING_CURRENT_KHAT_MATCH;MISSING_VOLUME_CONVENTION;MISSING_CHAIN_ZERO_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1291_0_source_provenance",
            "claim": "private checkpoint source provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "all registered local source paths and anchors are validated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1291_1_strict_double_zero",
            "claim": "strict double-zero parent clause adopted",
            "current_status": "BLOCKED_MISSING_ACTUAL_PARENT_MATCH",
            "reason": "the clause is mathematically sufficient but not sourced as the actual MTS Gamma/F branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1291_2_chain_zero",
            "claim": "Kmetric_chain^{00}=0",
            "current_status": "BLOCKED_CONDITIONAL_ONLY",
            "reason": "parent lock, F form, gradient control, and boundary/domain silence are still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1291_3_residual_bound",
            "claim": "chain residual is below local tests",
            "current_status": "BLOCKED_BOUND_FORMS_ONLY",
            "reason": "residual rows have no numeric profiles, kernel bounds, or response limits yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1291_4_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "current_status": "BLOCKED_NONCLAIM",
            "reason": "Delta_K^{00}, response vector, and amplitude/PPN scores remain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1291_0_clause_written",
            "decision": "write the strict double-zero parent clause as the preferred theorem target",
            "because": "F=(m-m_*)^2H kills both m and L_cg metric-chain terms with less reliance on kernel-zero assumptions",
            "next_action": "source-match the actual MTS F/m/L_cg definitions or keep residual bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1291_1_no_adoption_yet",
            "decision": "do not adopt the clause as current MTS",
            "because": "actual parent F form, local lock, gradient control, and boundary/domain closure are missing",
            "next_action": "hunt source text for F form and m/L_cg parent definitions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1291_2_residual_fallback",
            "decision": "stage the residual bound branch immediately",
            "because": "if source-match fails, the route remains testable rather than rhetorical",
            "next_action": "build a source-match audit for F=(m-m_*)^2H and m/L_cg definitions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1291_0_1292",
            "target_file": "1292-Y5-R10-RAB-F-form-and-m-Lcg-parent-source-match-or-residual-runner-input.md",
            "target_script": "scripts/Y5_R10_RAB_F_form_and_m_Lcg_parent_source_match_or_residual_runner_input.py",
            "task": "source-match the corpus for an actual source-backed F=(m-m_*)^2H form and parent definitions of m,L_cg, or turn KRB1291 residual bounds into runner inputs",
            "success_condition": "actual source-match rows for F,m,L_cg are found and gated, or residual runner input rows are produced with missing numeric/theorem inputs explicit",
            "do_not": "do not treat the sufficient double-zero clause as adopted unless it is matched to actual MTS source equations and boundary/domain gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PARENT_CLAUSE_PATH, parent_clause)
    write_csv(VARIATION_PROOF_PATH, variation_proof)
    write_csv(ADOPTION_GATES_PATH, adoption_gates)
    write_csv(RESIDUAL_BOUND_PATH, residual_bound)
    write_csv(DELTAK_STATUS_PATH, deltak_status)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1291_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    strict_clause = next(row for row in parent_clause if row["clause_id"] == "SDZ1291_1_strict_F_form")
    validations.append(
        validation_row(
            "VAL1291_1_strict_clause_written",
            "strict F=(m-m*)^2H parent clause is written as nonclaim",
            "F(m)=(m-m_*)^2 H(m)" in strict_clause["parent_clause"]
            and strict_clause["current_status"] == "STRICT_DOUBLE_ZERO_FORM_WRITTEN_NONCLAIM"
            and is_false(strict_clause["claim_allowed"]),
            "SDZ1291_1_strict_F_form",
        )
    )
    variation_verdict = next(row for row in variation_proof if row["step_id"] == "VP1291_1_metric_variation")
    validations.append(
        validation_row(
            "VAL1291_2_variation_zero_conditional",
            "metric-chain variation zero is shown conditionally",
            "delta Gamma_eff|_*" in variation_verdict["calculation"]
            and variation_verdict["result"].startswith("m and L_cg chain-kernel terms vanish"),
            "VP1291_1_metric_variation",
        )
    )
    adoption_blocked = all("MISSING" in row["status"] for row in adoption_gates)
    validations.append(
        validation_row(
            "VAL1291_3_adoption_gates_blocked",
            "adoption gates keep the sufficient clause from becoming a claim",
            adoption_blocked and all(is_false(row["claim_allowed"]) for row in adoption_gates),
            f"adoption_gate_rows={len(adoption_gates)}",
        )
    )
    residual_verdict = next(row for row in residual_bound if row["bound_id"] == "KRB1291_3_residual_verdict")
    validations.append(
        validation_row(
            "VAL1291_4_residual_bound_ledger_retained",
            "chain residual bound ledger is retained as nonclaim fallback",
            residual_verdict["current_status"] == "RESIDUAL_VECTOR_RETAINED"
            and "MISSING_ALL_KRB" in residual_verdict["needed_inputs"],
            "KRB1291_3_residual_verdict",
        )
    )
    deltak_verdict = next(row for row in deltak_status if row["status_id"] == "DKS1291_2_DeltaK00")
    validations.append(
        validation_row(
            "VAL1291_5_DeltaK_still_blocked",
            "DeltaK00 remains not computable",
            deltak_verdict["status"] == "NOT_COMPUTABLE_YET"
            and "MISSING_CURRENT_KHAT_MATCH" in deltak_verdict["remaining_missing"],
            "DKS1291_2_DeltaK00",
        )
    )
    validations.append(
        validation_row(
            "VAL1291_6_claim_gates_blocked",
            "claim gates block local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        PARENT_CLAUSE_PATH,
        VARIATION_PROOF_PATH,
        ADOPTION_GATES_PATH,
        RESIDUAL_BOUND_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1291_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1291_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1291_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, parent_clause, variation_proof, adoption_gates, residual_bound, deltak_status, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1291_10_next_target_1292",
            "next target routes to source-match or residual runner input",
            next_target[0]["next_id"] == "NEXT1291_0_1292" and "source-match" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1291_11_overall",
            "overall 1291 validation",
            overall_pass,
            "1291 writes the strict double-zero parent clause, proves its conditional chain-kernel silence, blocks adoption until source match, and stages residual bounds",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1291 Y5 R10 RAB strict double-zero parent clause or chain-kernel residual bound

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1291 constructs the exact strict double-zero parent clause: `F(m)=(m-m_*)^2 H(m)`. This is mathematically strong because `F(m_*)=0` and `F_prime(m_*)=0`, so the first `m/L_cg` metric-chain variation of `Gamma_eff=L_cg^-2 F(m)` vanishes on the locked local branch even if `M_m^{{00}}` and `M_L^{{00}}` are finite.

**Main progress:** this is a genuine theorem target, not just a vibe. The parent clause now states exactly what MTS must source-match: the actual `F`, the parent lock `m=m_*`, finite/safe `L_cg`, gradient control, and boundary/domain closure. Until those are sourced, the route is a clean closure candidate plus residual-bound branch, not a local-GR proof.

**Next derivation target:** audit the corpus for an actual `F=(m-m_*)^2H` source and parent definitions of `m,L_cg`; if absent, convert the residual bound forms into runner inputs.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Strict Double-Zero Parent Clause

{markdown_table(parent_clause, ["clause_id", "object", "parent_clause", "variation_consequence", "required_sources", "current_status", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Variation Proof

{markdown_table(variation_proof, ["step_id", "input", "calculation", "result", "assumptions", "claim_status", "valid_for_claim", "claim_allowed"])}

## Adoption Gates

{markdown_table(adoption_gates, ["gate_id", "needed_for_adoption", "current_evidence", "status", "failure_mode", "valid_for_claim", "claim_allowed"])}

## Chain-Kernel Residual Bound Ledger

{markdown_table(residual_bound, ["bound_id", "residual_component", "bound_form", "zero_or_small_route", "needed_inputs", "maps_to_tests", "current_status", "valid_for_claim", "claim_allowed"])}

## DeltaK Status Update

{markdown_table(deltak_status, ["status_id", "object", "status", "formula", "remaining_missing", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
