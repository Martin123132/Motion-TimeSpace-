from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3816"
BRANCH = "MTS_R2FR_Y5_PARENT_QBLIND_MATTER_DESCENT_ACTION_TEMPLATE_OR_FINITE_QMATTER_SOURCE_ROW_3816"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3816_parent_qblind_matter_descent_action_template_or_finite_qmatter_source_row.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_2444 = PCW / "2444-Y5-R2FR-source-leg-S-Eq-owner-from-parent-current-or-local-product-closure.md"
P_2445 = PCW / "2445-Y5-R2FR-Jq-source-current-extraction-from-parent-L-or-Htau-source-charge-certificate.md"
P_2446 = PCW / "2446-Y5-R2FR-EH-baseline-plus-MTS-residual-current-pack-for-S-Eq.md"
P_3806 = PCW / "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md"
P_3807 = PCW / "3807-Y5-R2FR-CSA3806-parent-signature-or-effective-readout-closure-audit.md"
P_3808 = PCW / "3808-Y5-R2FR-visible-coefficient-type-system-from-representation-superselection-or-finite-bounds.md"
P_3810 = PCW / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
P_3813 = PCW / "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md"
P_3815 = PCW / "3815-Y5-R2FR-local-source-current-silence-or-active-cSE-certificate.md"

CSV_3815_NEXT = OUT / "P8_Y5_R2FR_3815_NEXT_TARGET.csv"
CSV_3815_ZERO = OUT / "P8_Y5_R2FR_3815_ZERO_SOURCE_SILENCE_THEOREM_AUDIT.csv"
CSV_2444_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv"
CSV_2445_JQ = OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv"
CSV_2445_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_2445_SOURCE_CURRENT_CERTIFICATE_SCHEMA.csv"
CSV_2446_PACK = OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv"
CSV_3806_ACTION = OUT / "P8_Y5_R2FR_3806_COEFFICIENT_SUBQUOTIENT_ACTION_CLAUSE.csv"
CSV_3806_VARIATION = OUT / "P8_Y5_R2FR_3806_VARIATIONAL_ZERO_THEOREM.csv"
CSV_3807_SIGNATURE = OUT / "P8_Y5_R2FR_3807_CSA3806_PARENT_SIGNATURE_THEOREM.csv"
CSV_3807_CLOSURE = OUT / "P8_Y5_R2FR_3807_EFFECTIVE_READOUT_CLOSURE_CONTRACT.csv"
CSV_3808_OBSREP = OUT / "P8_Y5_R2FR_3808_OBSREP_TYPE_SYSTEM_THEOREM.csv"
CSV_3808_CLASS = OUT / "P8_Y5_R2FR_3808_VISIBLE_COEFFICIENT_CLASSIFICATION.csv"
CSV_3810_THEOREM = OUT / "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_THEOREM.csv"
CSV_3813_CONTRACT = OUT / "P8_Y5_R2FR_3813_MATTER_GLUE_ZERO_THEOREM_CONTRACT.csv"
CSV_3813_GLUE = OUT / "P8_Y5_R2FR_3813_RMATTER_GLUE_DECOMPOSITION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3816_SOURCE_REGISTER.csv",
    "template": OUT / "P8_Y5_R2FR_3816_QBLIND_MATTER_ACTION_TEMPLATE.csv",
    "theorem": OUT / "P8_Y5_R2FR_3816_CHAIN_RULE_ZERO_THEOREM.csv",
    "residuals": OUT / "P8_Y5_R2FR_3816_QMATTER_SOURCE_RESIDUAL_DECOMPOSITION.csv",
    "signature": OUT / "P8_Y5_R2FR_3816_STRICT_CORPUS_SIGNATURE_AUDIT.csv",
    "implications": OUT / "P8_Y5_R2FR_3816_LOCAL_GR_IMPLICATION_MATRIX.csv",
    "gates": OUT / "P8_Y5_R2FR_3816_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3816_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3816_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3816_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3816_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3816_0_3815_doc", P_3815, "The useful theorem is short", "3815 local source-current silence theorem handoff"),
    ("SRC3816_1_3815_next", CSV_3815_NEXT, "3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md", "3815 machine handoff"),
    ("SRC3816_2_3815_zero", CSV_3815_ZERO, "ZST3815_1_qblind_matter_descent", "3815 qblind matter descent clause"),
    ("SRC3816_3_2444_contract", CSV_2444_CONTRACT, "SLC2444_0_definition", "source-leg current definition"),
    ("SRC3816_4_2445_doc", P_2445, "JQX2445_3_qblind_zero_route", "qblind zero route source"),
    ("SRC3816_5_2445_jq", CSV_2445_JQ, "JQX2445_3_qblind_zero_route", "machine J_q qblind zero route"),
    ("SRC3816_6_2445_schema", CSV_2445_SCHEMA, "SCS2445_3_zero_theorem", "source current zero theorem schema"),
    ("SRC3816_7_2446_pack", CSV_2446_PACK, "RCS2446_3_matter_source_glue", "matter/source glue residual-current family"),
    ("SRC3816_8_3806_doc", P_3806, "CSA3806", "coefficient subquotient action clause"),
    ("SRC3816_9_3806_action", CSV_3806_ACTION, "CSA3806_1_action_clause", "machine coefficient-subquotient action clause"),
    ("SRC3816_10_3806_variation", CSV_3806_VARIATION, "VZT3806_1_variation_split", "variation split theorem for visible sector"),
    ("SRC3816_11_3807_doc", P_3807, "Strong typed action-domain succeeds conditionally", "typed action-domain theorem source"),
    ("SRC3816_12_3807_signature", CSV_3807_SIGNATURE, "PST3807_1_sufficient_type_split", "sufficient type split theorem"),
    ("SRC3816_13_3807_closure", CSV_3807_CLOSURE, "ERC3807_4_verdict", "effective/readout closure requirement"),
    ("SRC3816_14_3808_doc", P_3808, "visible coefficient slots are `ObsRep` objects", "ObsRep type system source"),
    ("SRC3816_15_3808_obsrep", CSV_3808_OBSREP, "ORT3808_2_chain_rule", "ObsRep chain-rule zero"),
    ("SRC3816_16_3808_class", CSV_3808_CLASS, "VCC3808_3_masses", "matter spectrum/source weight classification"),
    ("SRC3816_17_3810_theorem", CSV_3810_THEOREM, "ZRT3810_1_same_current_extension", "same-current source/readout extension"),
    ("SRC3816_18_3813_contract", CSV_3813_CONTRACT, "ZC3813_0_single_action_density_line", "matter-glue single action-density clause"),
    ("SRC3816_19_3813_glue", CSV_3813_GLUE, "RMG3813_3_nonHilbert_current", "finite matter-glue residual pieces"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def template_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "template_id": "OMAT3816_0_field_split",
            "clause": "observed-matter representation object",
            "formal_form": "ObsMatter_U=(g_obs,e_obs,A_obs,psi_A,theta_rep,matter_rep,boundary_class,source_domain_class)",
            "meaning": "ordinary matter is allowed to see observed metric/coframe/EM fields and fixed representation labels, not an independent hidden q-source coordinate",
            "if_signed": "sets the domain for q-blind matter descent",
            "strict_status": "TEMPLATE_WRITTEN_NOT_STRICT_CORPUS_SIGNED",
        },
        {
            **base,
            "template_id": "OMAT3816_1_action_density",
            "clause": "single ordinary matter action-density line",
            "formal_form": "S_ord=sum_A int_M sqrt(-g_obs) L_A(psi_A,D_obs psi_A; g_obs,e_obs,A_obs,theta_rep,matter_rep)",
            "meaning": "ordinary matter has one variational source owner before source/readout selectors",
            "if_signed": "keeps Hilbert stress nonzero while forbidding independent q-source terms",
            "strict_status": "CONDITIONAL_PARENT_EXTENSION_READY",
        },
        {
            **base,
            "template_id": "OMAT3816_2_no_direct_q_slot",
            "clause": "no direct q-source slot",
            "formal_form": "partial L_A/partial q_src=0 at fixed ObsMatter_U",
            "meaning": "there is no w_A(q_src), m_A(q_src), kappa_A(q_src), clock marker, source weight or boundary weight outside ObsMatter",
            "if_signed": "direct ordinary-matter q-current vanishes",
            "strict_status": "REQUIRES_PARENT_OPERATOR_DOMAIN_EXCLUSION",
        },
        {
            **base,
            "template_id": "OMAT3816_3_visible_coeff_subquotient",
            "clause": "visible coefficients factor through ObsRep",
            "formal_form": "c_J(Phi)=cbar_J(ObsRep_U(Phi)); D ObsRep_U[v_q]=0",
            "meaning": "imports the 3806-3808 type theorem into ordinary matter source weights, masses, clocks and boundary/source-domain coefficients",
            "if_signed": "D_vq c_J=0 for all ordinary visible coefficient slots",
            "strict_status": "EXACT_CONDITIONAL_REUSED_NOT_SIGNED",
        },
        {
            **base,
            "template_id": "OMAT3816_4_variation_order",
            "clause": "variation before readout/projector selection",
            "formal_form": "delta_q S_ord is evaluated before Pi_M, P_loc, W_source, material readout or fitted-source maps",
            "meaning": "prevents data processing from becoming an artificial source coefficient",
            "if_signed": "qblind descent feeds the 3815 zero-source branch rather than a readout residual",
            "strict_status": "READOUT_CLOSURE_UNSIGNED",
        },
        {
            **base,
            "template_id": "OMAT3816_5_hilbert_stress_preserved",
            "clause": "metric variation remains active",
            "formal_form": "T_H^{mu nu}=(2/sqrt(-g_obs)) delta S_ord/delta g_obs_mu_nu may be nonzero even when J_q^ord=0",
            "meaning": "qblind matter descent does not delete matter; it only removes the hidden q-source leg",
            "if_signed": "ordinary matter can still source GR/Newton through Hilbert stress",
            "strict_status": "EXACT_SCOPE_SPLIT",
        },
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "theorem_id": "QMT3816_0_variation_decomposition",
            "claim_piece": "ordinary matter q-variation split",
            "statement": "For an admissible hidden q-source variation v_q, delta_vq S_ord decomposes into Hilbert/coframe/EM observed-field pieces, visible coefficient pieces, direct q-source pieces, measure/source-weight pieces and readout/boundary pieces.",
            "formula": "delta_vq S_ord = 1/2 int sqrt(-g) T_H^{mu nu} D_vq g_mu_nu + int Sigma_e D_vq e + int J_EM D_vq A + sum_J int O_J D_vq c_J + int E_direct_q + E_measure + E_readout",
            "proof_status": "EXACT_VARIATIONAL_IDENTITY",
            "consequence": "every possible ordinary q-source route is now either theorem-zero by factorisation or a named residual component",
            "missing_for_strict_claim": "none for the identity; values/signatures are still needed for zero or bounds",
        },
        {
            **base,
            "theorem_id": "QMT3816_1_chain_rule_zero",
            "claim_piece": "qblind ordinary matter source-current zero",
            "statement": "If S_ord factors through ObsMatter_U and D_vq ObsMatter_U=0 with no direct q-source slot, then J_q^ordinary[v_q]=delta_vq S_ord=0.",
            "formula": "D_vq Sbar_ord[ObsMatter_U]=D Sbar_ord[D_vq ObsMatter_U]=0",
            "proof_status": "EXACT_CONDITIONAL_CHAIN_RULE_THEOREM",
            "consequence": "ordinary matter contributes no hidden q-source current in the local source-silence branch",
            "missing_for_strict_claim": "parent-signed ObsMatter_U object, no direct q slot, fixed representation labels and readout/effective closure",
        },
        {
            **base,
            "theorem_id": "QMT3816_2_hilbert_stress_not_zeroed",
            "claim_piece": "GR source survives",
            "statement": "The qblind theorem sets the derivative along v_q to zero; it does not set delta S_ord/delta g_obs to zero.",
            "formula": "J_q^ordinary=0 does not imply T_H^{mu nu}=0",
            "proof_status": "EXACT_SCOPE_GUARD",
            "consequence": "the route can suppress extra q forces while preserving the standard stress source needed for GR/Newton",
            "missing_for_strict_claim": "EH/metric equation and Bianchi bridge are downstream",
        },
        {
            **base,
            "theorem_id": "QMT3816_3_visible_coeff_import",
            "claim_piece": "masses/source weights/clock markers q-silence",
            "statement": "The 3806-3808 coefficient-subquotient theorem applies to ordinary matter coefficients if they are typed as ObsRep objects rather than functions of hidden q/X_Q data.",
            "formula": "c_J=cbar_J(ObsRep_U), D_vq ObsRep_U=0 => D_vq c_J=0",
            "proof_status": "EXACT_CONDITIONAL_IMPORT",
            "consequence": "mass spectrum, source weights, kappa, clocks and boundary coefficients do not produce ordinary q-current leakage if the type split is parent-signed",
            "missing_for_strict_claim": "matter spectrum owner, source weight owner, effective/readout naturality",
        },
        {
            **base,
            "theorem_id": "QMT3816_4_finite_residual_fallback",
            "claim_piece": "C_qmatter residual row",
            "statement": "If any qblind clause fails, the ordinary q-source current is bounded by the sum of the named component norms C_qmatter_i rather than hidden inside S_E^q.",
            "formula": "||J_q^ordinary||_arena/N_E <= C_qmatter_total := sum_i C_qmatter_i",
            "proof_status": "EXACT_TRIANGLE_BOUND_TEMPLATE",
            "consequence": "failure of the theorem becomes a finite source-current input route, not a vague missing coupling",
            "missing_for_strict_claim": "component values or zero theorems with units and source paths",
        },
        {
            **base,
            "theorem_id": "QMT3816_5_strict_verdict",
            "claim_piece": "strict corpus status",
            "statement": "3816 derives the exact action template and chain-rule theorem but does not prove the current corpus already satisfies the template.",
            "formula": "theorem-ready != claim-ready",
            "proof_status": "PASS_NONCLAIM_CONTRACT_DERIVED_NOT_SIGNED",
            "consequence": "local-GR source silence is closer, but still nonclaim until parent action and readout/projector signatures are signed",
            "missing_for_strict_claim": "parent signature plus projection/readout chain-map from 3815",
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    rows = [
        ("CQM3816_0_direct_q_slot", "C_direct_q", "explicit ordinary matter q-source operator", "||partial L_ord/partial q_src||_arena/N_E", "source_current_over_normalizer", "MISSING_PARENT_OPERATOR_DOMAIN_EXCLUSION", "no direct q-source slot theorem or numeric source coefficient"),
        ("CQM3816_1_metric_leak", "C_gobs", "observed metric variation along hidden q", "||T_H^{mu nu} D_q g_obs_mu_nu||_arena/N_E", "source_current_over_normalizer", "MISSING_DQ_GOBS_ZERO_OR_METRIC_KERNEL", "D_q g_obs=0 for q-source verticals or metric-response bound"),
        ("CQM3816_2_coframe_connection_leak", "C_eobs", "observed coframe/spin-connection variation", "||Sigma_e D_q e_obs + Sigma_omega D_q omega_obs||_arena/N_E", "source_current_over_normalizer", "MISSING_DQ_EOBS_ZERO_OR_FRAME_BOUND", "coframe/frame q-basic theorem or finite common-frame bound"),
        ("CQM3816_3_EM_path_leak", "C_Aobs", "ordinary charged matter EM field path", "||J_EM^mu D_q A_obs_mu||_arena/N_E", "source_current_over_normalizer", "MISSING_SAME_CURRENT_EM_ROUTE_OR_AOBS_ZERO", "same-current EM exchange theorem or D_q A_obs bound"),
        ("CQM3816_4_visible_coefficients", "C_coeff", "masses, source weights, kappa, clocks and material coefficients", "sum_J ||O_J D_q c_J||_arena/N_E", "source_current_over_normalizer", "MISSING_OBSREP_COEFFICIENT_SIGNATURE", "ObsRep type split for every c_J or finite coefficient slopes"),
        ("CQM3816_5_representation_labels", "C_rep", "matter representation and spectrum labels", "||D_q theta_rep|| weighted by matter operators", "source_current_over_normalizer", "MISSING_MATTER_SPECTRUM_OWNER", "fixed/superselected representation labels or finite spectrum response"),
        ("CQM3816_6_measure_source_weight", "C_measure", "measure, source weights and action-scale slots", "||D_q ln dmu_obs|| + ||D_q w_A|| + ||D_q hbar_A||", "source_current_over_normalizer", "MISSING_SINGLE_DENSITY_LINE_AND_SPECIES_BLIND_MEASURE", "3813 single density/species-blind measure theorem signed or finite row"),
        ("CQM3816_7_readout_boundary", "C_readout_boundary", "readout, source-domain and boundary re-entry", "||D_q R_readout|| + ||D_q W_source|| + ||D_q B_ref|| contributions", "source_current_over_normalizer", "MISSING_READOUT_BOUNDARY_CLOSURE", "pure postprocessing/fixed domain theorem or component bound"),
        ("CQM3816_8_total", "C_qmatter_total", "total ordinary q-matter source residual", "C_direct_q+C_gobs+C_eobs+C_Aobs+C_coeff+C_rep+C_measure+C_readout_boundary", "source_current_over_normalizer", "COMPONENTS_MISSING_OR_CONDITIONAL", "all components theorem-zero or source-backed numeric rows"),
    ]
    return [
        {
            **base,
            "residual_id": residual_id,
            "symbol": symbol,
            "source_route": source_route,
            "bound_formula": bound_formula,
            "units": units,
            "current_status": status,
            "exit_requirement": exit_requirement,
        }
        for residual_id, symbol, source_route, bound_formula, units, status, exit_requirement in rows
    ]


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "audit_id": "SIG3816_0_action_template",
            "signature_piece": "ObsMatter action template",
            "current_evidence": "3816 writes OMAT3816 as a parent action contract using 2445 and 3806-3808 machinery",
            "status": "CONTRACT_DERIVED_HERE",
            "missing_for_claim": "not found as an earlier strict-current parent signature",
        },
        {
            **base,
            "audit_id": "SIG3816_1_qblind_zero_route",
            "signature_piece": "J_q^ordinary=0 chain rule",
            "current_evidence": "2445 already had exact qblind zero route; 3816 upgrades it to a full variation decomposition",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "qblind clauses not parent-signed",
        },
        {
            **base,
            "audit_id": "SIG3816_2_coefficients",
            "signature_piece": "matter coefficients and source weights",
            "current_evidence": "3806-3808 give coefficient-subquotient/ObsRep theorem and classify masses/source weights",
            "status": "CONDITIONAL_IMPORT_READY",
            "missing_for_claim": "matter spectrum and source-weight owners unsigned",
        },
        {
            **base,
            "audit_id": "SIG3816_3_same_current",
            "signature_piece": "same-current Hilbert/EM/source owner",
            "current_evidence": "3810 same-current extension forbids source alpha coefficients as separate readout couplings if one descended action owns them",
            "status": "DOWNSTREAM_GATE_NOT_SIGNED",
            "missing_for_claim": "same total source action, boundary/domain silence and arena projection maps",
        },
        {
            **base,
            "audit_id": "SIG3816_4_matter_glue",
            "signature_piece": "single action density and Hilbert-current owner",
            "current_evidence": "3813 constructs the matter-glue zero contract but keeps it unsigned",
            "status": "THEOREM_CONSTRUCTED_NOT_PARENT_SIGNED",
            "missing_for_claim": "single density line, connected naturality, species-blind measure/current, source-label forgetting",
        },
        {
            **base,
            "audit_id": "SIG3816_5_verdict",
            "signature_piece": "strict qblind matter descent claim",
            "current_evidence": "exact theorem and residual row exist",
            "status": "NOT_STRICT_CURRENT_CLAIM",
            "missing_for_claim": "adopt/sign OMAT3816 plus readout/projector chain-map",
        },
    ]


def implication_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "implication_id": "IMP3816_0_local_GR",
            "if_condition": "OMAT3816 signed and projector/readout chain-map signed",
            "then_result": "ordinary matter has J_q^ordinary=0 while T_H remains available for metric equations",
            "current_status": "PROMISING_CONDITIONAL_NOT_CLAIMED",
            "remaining_gate": "derive EH/Bianchi/Hilbert stress bridge in 3817",
        },
        {
            **base,
            "implication_id": "IMP3816_1_Newton",
            "if_condition": "Hilbert stress survives plus EH weak-field limit and source normalization are owned",
            "then_result": "Newtonian source mass can come from T_H without q-fifth-force source leakage",
            "current_status": "DOWNSTREAM_NOT_DERIVED",
            "remaining_gate": "Hamiltonian/source normalization and Bianchi bridge",
        },
        {
            **base,
            "implication_id": "IMP3816_2_EM",
            "if_condition": "A_obs path is same-current EM exchange rather than a q-source coefficient",
            "then_result": "charged matter can keep Maxwell coupling without opening an independent q-source slot",
            "current_status": "CONDITIONAL_SAME_CURRENT_GATE",
            "remaining_gate": "same-current EM/Hilbert action owner and B_Q normalization",
        },
        {
            **base,
            "implication_id": "IMP3816_3_product_rows",
            "if_condition": "OMAT3816 not signed",
            "then_result": "ordinary matter leakage enters as C_qmatter_total and product-only rows remain nonclaim",
            "current_status": "STRICT_DEFAULT",
            "remaining_gate": "fill or zero every C_qmatter component",
        },
        {
            **base,
            "implication_id": "IMP3816_4_no_overclaim",
            "if_condition": "J_q^ordinary=0 is adopted",
            "then_result": "this only silences ordinary q-current; it does not by itself close boundary, projector, non-EH, PPN or coefficient residuals",
            "current_status": "SCOPE_GUARD",
            "remaining_gate": "3815 residual-current pack still applies",
        },
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    return [
        {
            **base,
            "gate_id": "GATE3816_0_sources",
            "claim": "all cited source paths exist and needles are found",
            "gate_status": "PASS_NONCLAIM" if all_sources else "FAIL",
            "reason": "source-backed action runner is reproducible" if all_sources else "source path or needle missing",
            "gate_pass": bool_text(all_sources),
        },
        {
            **base,
            "gate_id": "GATE3816_1_chain_rule_theorem",
            "claim": "qblind ordinary matter chain-rule theorem is written",
            "gate_status": "PASS_NONCLAIM",
            "reason": "exact conditional theorem and variation decomposition are present",
            "gate_pass": "true",
        },
        {
            **base,
            "gate_id": "GATE3816_2_strict_parent_signature",
            "claim": "current corpus parent-signs OMAT3816",
            "gate_status": "BLOCKED",
            "reason": "OMAT3816 is a derived parent-action contract, not yet a strict-current signature",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3816_3_Cqmatter_finite_ready",
            "claim": "finite C_qmatter residual decomposition exists",
            "gate_status": "PASS_NONCLAIM",
            "reason": "component rows exist with units and exit requirements but no numeric values",
            "gate_pass": "true",
        },
        {
            **base,
            "gate_id": "GATE3816_4_local_GR_claim",
            "claim": "local GR/Newton source reduction is claimed",
            "gate_status": "BLOCKED",
            "reason": "Hilbert stress/Bianchi bridge and projector/readout chain-map remain downstream",
            "gate_pass": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "decision_id": "DEC3816_0_use_OMAT_template",
            "decision": "use OMAT3816 as the explicit parent-action contract for qblind ordinary matter",
            "because": "it proves J_q^ordinary=0 by chain rule without killing Hilbert stress",
            "next_action": "test its compatibility with EH/Bianchi/Hilbert stress in 3817",
        },
        {
            **base,
            "decision_id": "DEC3816_1_no_matter_deletion",
            "decision": "separate hidden q-current from metric Hilbert stress",
            "because": "local GR needs matter to source g_obs even when hidden q-source current vanishes",
            "next_action": "derive the stress-conservation/Bianchi bridge",
        },
        {
            **base,
            "decision_id": "DEC3816_2_keep_residual_fallback",
            "decision": "install C_qmatter_total if OMAT3816 is unsigned",
            "because": "failed qblind clauses must become finite source-current rows, not vague holes",
            "next_action": "fill or zero components only after the GR stress bridge is checked",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md",
            "target_script": "scripts/Y5_R2FR_3817_qblind_matter_descent_preserves_Hilbert_stress_and_Bianchi_current.py",
            "objective": "Prove or bound the next GR bridge: qblind ordinary matter descent sets the hidden q-current to zero while preserving Hilbert stress, Ward/Bianchi conservation, and the weak-field source needed for GR/Newton; if the bridge fails, emit finite R_Hilbert_owner and C_Bianchi rows.",
            "success_gate": "A clean theorem shows J_q^ordinary=0 is compatible with nonzero conserved T_H sourcing the metric, or every obstruction is converted into finite Hilbert-owner/Bianchi residual rows with units.",
            "avoid": "do not claim local GR; do not delete matter stress; do not use positive mass as c_SE; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_QBLIND_MATTER_ACTION_THEOREM_AND_CQMATTER_RESIDUAL_ROWS_BUILT",
            "summary": "3816 writes the parent qblind ordinary-matter action template OMAT3816, proves the exact conditional chain-rule theorem J_q^ordinary=0 at fixed observed matter representation, preserves nonzero Hilbert stress as the GR/Newton source, and emits a finite C_qmatter residual decomposition when the template is unsigned. The next target is proving that this qblind descent preserves Hilbert stress conservation/Bianchi sourcing rather than deleting matter.",
            "valid_for_claim": "false",
        }
    ]


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    status = grouped["status"][0]
    validation = grouped.get("validation", [])
    validation_pass = all(row.get("result") == "PASS" for row in validation) if validation else False
    text = f"""# 3816 - Parent Q-Blind Matter Descent Action Template Or Finite Q-Matter Source Row

## Status

- Status: `{status["status"]}`
- Claim level: private, nonclaim theorem contract.
- Validation pass: `{bool_text(validation_pass)}`
- Key result: `J_q^ordinary=0` is derivable by chain rule if ordinary matter descends through observed matter representation data, while `T_H` remains nonzero for GR/Newton.

## The Action Template

3816 defines the ordinary-matter parent action contract:

```text
ObsMatter_U = (g_obs, e_obs, A_obs, psi_A, theta_rep,
               matter_rep, boundary_class, source_domain_class)

S_ord = sum_A int sqrt(-g_obs)
        L_A(psi_A, D_obs psi_A;
            g_obs, e_obs, A_obs, theta_rep, matter_rep)
```

The rule is: ordinary matter may see the observed metric/coframe/EM fields and fixed representation data, but it may not contain an independent hidden `q_src` source slot such as `w_A(q_src)`, `m_A(q_src)`, `kappa_A(q_src)`, clock markers, source weights, or boundary weights.

## Exact Chain-Rule Theorem

For an admissible hidden q-source variation `v_q`:

```text
delta_vq S_ord =
  1/2 int sqrt(-g) T_H^{{mu nu}} D_vq g_mu_nu
  + int Sigma_e D_vq e
  + int J_EM D_vq A
  + sum_J int O_J D_vq c_J
  + E_direct_q + E_measure + E_readout
```

If `S_ord = Sbar_ord[ObsMatter_U]`, `D_vq ObsMatter_U=0`, and no direct q-source slot exists, then:

```text
J_q^ordinary[v_q] = delta_vq S_ord
                  = D Sbar_ord[D_vq ObsMatter_U]
                  = 0
```

That is real progress because it does **not** set `T_H^{{mu nu}}=0`. The source can still gravitate through the metric/Hilbert variation; it just does not excite the hidden q-current.

## Finite Fallback

If the action template is not parent-signed, ordinary q-matter leakage is no longer vague:

```text
C_qmatter_total =
  C_direct_q + C_gobs + C_eobs + C_Aobs
  + C_coeff + C_rep + C_measure + C_readout_boundary
```

and

```text
||J_q^ordinary||_arena / N_E <= C_qmatter_total
```

All component rows are emitted as nonclaim inputs with units and exit requirements.

## Current Verdict

- The theorem is exact and useful.
- The strict corpus does not yet parent-sign `OMAT3816`.
- No local-GR/Newton/WEP/R10/PPN/clock/orbital claim is made.
- The next target is to prove that qblind matter descent preserves the Hilbert stress/Bianchi current needed for GR/Newton, rather than accidentally deleting the source.

## Next Target

`3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md`

## Machine Outputs

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_SOURCE_REGISTER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_QBLIND_MATTER_ACTION_TEMPLATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_CHAIN_RULE_ZERO_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_QMATTER_SOURCE_RESIDUAL_DECOMPOSITION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_STRICT_CORPUS_SIGNATURE_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_LOCAL_GR_IMPLICATION_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_CLAIM_GATES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_DECISION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_NEXT_TARGET.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3816_STATUS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3816_VALIDATION.csv`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3815",
        "# Local GR Coupling Spine - Current State After 3816",
    )
    new_para = (
        "`3816` writes the parent qblind ordinary-matter action template `OMAT3816` and proves the exact chain-rule theorem: if ordinary matter descends through observed matter representation data and the hidden q-source variation leaves that data fixed, then `J_q^ordinary=0`. The key guardrail is that this does not delete matter: `T_H^{mu nu}=2/sqrt(-g_obs) delta S_ord/delta g_obs` can remain nonzero and source GR/Newton. If the template is unsigned, the failure is now a finite `C_qmatter_total` residual decomposition rather than a vague coupling hole.\n"
    )
    if "`3816` writes the parent qblind ordinary-matter action template" not in text:
        anchor = (
            "`3815` converts the source-amplitude fork into a local source-current runner. The clean route is now exact but conditional: if ordinary matter is q-blind before readout, the q-current `J_q^E` vanishes, and fixed linear projection gives `P_arena[G_qJ_q^E]=0`. The active-positive route is refused unless a real `0<c_SE<=abs(S_E^q)` certificate supplies nonzero current, no nodal cancellation and owned `N_E`; positive mass alone is explicitly not enough. Therefore the strict current branch remains product-only, and the next derivation jump is parent q-blind matter descent or a finite q-matter source row.\n"
        )
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + new_para)
        else:
            text += "\n" + new_para

    history_entry = (
        "- `3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md`: writes the `OMAT3816` parent action template, proves `J_q^ordinary=0` by chain rule under qblind observed-matter descent, preserves Hilbert stress as the GR/Newton source, and emits `C_qmatter_total` residual rows when unsigned."
    )
    if history_entry not in text:
        marker = "## Next Target"
        if marker in text:
            text = text.replace(marker, history_entry + "\n\n" + marker, 1)
        else:
            text += "\n" + history_entry + "\n"

    old_target = (
        "`3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md`\n\n"
        "Target: do the smallest real derivation jump exposed by 3815. Write the parent action clause under which ordinary matter depends on `q` only through observed metric/coframe/representation data, prove `J_q^ordinary=0` by chain rule, or emit a finite `C_qmatter` source-current residual row with arena units.\n\n"
        "This is the best next move because local-GR source silence now reduces to one signable parent-action question rather than another broad residual sweep."
    )
    new_target = (
        "`3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md`\n\n"
        "Target: prove or bound the next GR bridge. Show that qblind ordinary matter descent sets the hidden q-current to zero while preserving nonzero Hilbert stress, Ward/Bianchi conservation, and the weak-field source needed for GR/Newton; if it fails, emit finite `R_Hilbert_owner` and `C_Bianchi` rows.\n\n"
        "This is the best next move because 3816 only wins if q-source silence does not accidentally delete the ordinary stress source of GR."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3816_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3816_QBLIND_MATTER_ACTION_TEMPLATE.csv",
        "P8_Y5_R2FR_3816_CHAIN_RULE_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_3816_QMATTER_SOURCE_RESIDUAL_DECOMPOSITION.csv",
        "P8_Y5_R2FR_3816_STRICT_CORPUS_SIGNATURE_AUDIT.csv",
        "P8_Y5_R2FR_3816_LOCAL_GR_IMPLICATION_MATRIX.csv",
        "P8_Y5_R2FR_3816_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3816_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3816_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3816_STATUS.csv",
        "P8_Y5_BRR545_3816_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3816*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3816 markdown document written"),
        ("template_written", any(row["template_id"] == "OMAT3816_1_action_density" for row in grouped["template"]), "ordinary matter action template emitted"),
        ("chain_rule_theorem", any(row["theorem_id"] == "QMT3816_1_chain_rule_zero" and row["proof_status"] == "EXACT_CONDITIONAL_CHAIN_RULE_THEOREM" for row in grouped["theorem"]), "chain-rule qblind zero theorem written"),
        ("hilbert_stress_preserved", any(row["theorem_id"] == "QMT3816_2_hilbert_stress_not_zeroed" for row in grouped["theorem"]), "Hilbert stress preservation guard present"),
        ("Cqmatter_total_row", any(row["residual_id"] == "CQM3816_8_total" for row in grouped["residuals"]), "finite C_qmatter total row emitted"),
        ("strict_claim_blocked", any(row["gate_id"] == "GATE3816_2_strict_parent_signature" and row["gate_pass"] == "false" for row in grouped["gates"]), "strict parent signature remains blocked"),
        ("local_GR_blocked", any(row["gate_id"] == "GATE3816_4_local_GR_claim" and row["gate_pass"] == "false" for row in grouped["gates"]), "local GR claim remains blocked"),
        ("claim_gates_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("next_target_selected", grouped["next_target"][0]["target_doc"].startswith("3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress"), "3817 Hilbert stress/Bianchi target selected"),
        ("spine_updated", "Current State After 3816" in spine_text and "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md" in spine_text, "live spine updated to 3816 and 3817 target"),
        ("formalization_clean", not fwb_hits, "no 3816 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "template": template_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "residuals": residual_rows(timestamp),
        "signature": signature_rows(timestamp),
        "implications": implication_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
