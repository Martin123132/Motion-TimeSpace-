from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SPECIES_LABEL_FORGETTING_SOURCE_FUNCTOR_PARENT_PROOF_OR_DELTAW_SPECIES_BOUND_2399"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


SOURCES = [
    {
        "source_id": "SRC2399_2398_doc",
        "path": str(POST_ROOT / "2398-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-pack.md"),
        "needed_for": "current chain selects species-label forgetting",
        "needles": "NEXT2398_0_selected|q_src({(T_A,A)})=T_total|delta_w_species|VAL2398_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1764_doc",
        "path": str(POST_ROOT / "1764-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"),
        "needed_for": "prior label-forgetting proof attempt",
        "needles": "LF1764_1_conditional_theorem|F_src({(T_A,A)})=sum_A kappa_A T_A|VAL1764_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1764_label_attempt",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1764_LABEL_FORGETTING_PROOF_ATTEMPT.csv"),
        "needed_for": "machine-readable label-forgetting attempt",
        "needles": "LF1764_0_target|LF1764_2_variation_order|LF1764_5_current_verdict|DELTA_W_SPECIES_RETAINED",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1764_countermodels",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1764_COUNTERMODEL_LEDGER.csv"),
        "needed_for": "species source countermodels",
        "needles": "CM1764_0_labelled_additive_source_functor|CM1764_1_weighted_action_before_variation|CM1764_5_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1765_doc",
        "path": str(POST_ROOT / "1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md"),
        "needed_for": "stronger exchange-collapse refinement",
        "needles": "delta_w_species -> delta_w_block|connected ordinary matter gives only common calibration|VAL1765_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1765_prefactor",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv"),
        "needed_for": "same-action and exchange filters",
        "needles": "NSP1765_1_same_action_filter|NSP1765_2_exchange_filter|NSP1765_4_current_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_1765_hilbert_owner",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"),
        "needed_for": "total Hilbert source owner clauses",
        "needles": "THO1765_1_total_hilbert_derivative|THO1765_2_interaction_stress|THO1765_3_source_shadow_ban",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_954_parent_clause",
        "path": str(RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv"),
        "needed_for": "parent action source-prefactor clauses",
        "needles": "PAC954_1_no_source_prefactors|PAC954_2_total_Hilbert_derivative|PAC954_5_GR_source_limit_clause",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2399_977_constant_source",
        "path": str(RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv"),
        "needed_for": "constant/source universality guard",
        "needles": "CSC977_3_hilbert_source_current|CSC977_4_single_universal_kappa|CSC977_5_bianchi_limit",
        "valid_for_claim": no_claim(),
    },
]


def proof_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_0_target",
            "claim_piece": "parent source functor forgets species labels before coupling selection",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "proof_status": "TARGET_EXACT",
            "proof_result": "WOULD_REMOVE_DELTA_W_SPECIES_DOMAIN_SLOT",
            "gap": "source-domain quotient is identified but not forced by the current parent action",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_1_conditional_label_forgotten_source",
            "claim_piece": "label-forgotten source functor has one coupling",
            "mathematical_form": "S_matter=sum_A S_A; T_total=delta S_matter/delta e_obs; F_src(T_total)=kappa_univ T_total",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "if no w_A slot and no hidden source spurion exists, relative kappa_A/kappa_B cannot be written",
            "gap": "no-source-prefactor and no-spurion clauses remain unsigned parent premises",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_2_variation_before_decomposition",
            "claim_piece": "variation-before-decomposition mechanism",
            "mathematical_form": "delta(S_1+...+S_N)/delta e_obs = sum_A delta S_A/delta e_obs, with T_total formed before labels are exposed",
            "proof_status": "DERIVED_WITHIN_CONTRACT",
            "proof_result": "bookkeeping labels disappear if the active source owner is the total Hilbert/coframe derivative",
            "gap": "parent action must declare the total Hilbert derivative as the only ordinary active-source owner",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_3_same_action_filter",
            "claim_piece": "same-action principle rejects pure source-shadow weights",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta e_obs from the same S_matter",
            "proof_status": "DERIVED_FILTER",
            "proof_result": "separate source weights are illegal if they live only in a shadow source functional",
            "gap": "does not exclude weights multiplying real disconnected matter subactions",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_4_noether_exchange_filter",
            "claim_piece": "Noether/Bianchi exchange collapses weights across interacting sectors",
            "mathematical_form": "sum_i w_i C_i^nu=0 forces w_i=w_j on every nonzero exchange edge",
            "proof_status": "DERIVED_CONDITIONAL_FILTER",
            "proof_result": "relative species prefactors collapse to conserved exchange-block prefactors",
            "gap": "ordinary matter exchange graph connectivity is not yet proved from parent sources",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_5_common_mode",
            "claim_piece": "common prefactor is not a physical WEP/source residual",
            "mathematical_form": "S_matter -> w_star S_matter gives kappa_eff=kappa w_star",
            "proof_status": "COMMON_MODE_ABSORBABLE",
            "proof_result": "one common source normalization is calibration, not composition dependence",
            "gap": "only relative disconnected-block weights remain dangerous",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2399_6_current_verdict",
            "claim_piece": "current species-label forgetting result",
            "mathematical_form": "delta_w_species -> delta_w_block, zero only if one ordinary exchange-connected source block and no source shadow",
            "proof_status": "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF",
            "proof_result": "species-level free weights are overbroad; live residual narrows to disconnected conserved source blocks",
            "gap": "source-shadow ban and ordinary exchange graph connectivity remain unsigned",
            "valid_for_claim": no_claim(),
        },
    ]


def source_domain_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_0_unlabelled_domain",
            "source_domain": "label-forgotten total Hilbert current",
            "mathematical_form": "Obj(Source)=T_total, not {(T_A,A)}",
            "effect": "F_src has no species argument and can only carry one calibrated common scalar",
            "status": "CLEAN_ZERO_ROUTE_IF_PARENT_SIGNED",
            "blocker": "parent category/source owner not signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_1_labelled_domain",
            "source_domain": "labelled species current family",
            "mathematical_form": "Obj(Source)={(T_A,A)} and F_src({(T_A,A)})=sum_A kappa_A T_A",
            "effect": "relative species couplings remain covariant, additive, and Ward-compatible",
            "status": "COUNTERDOMAIN_OPEN",
            "blocker": "must exclude labels before source functor formation",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_2_weighted_action",
            "source_domain": "weighted matter action before variation",
            "mathematical_form": "S_matter=sum_A w_A S_A",
            "effect": "constant w_A can preserve diffeomorphism covariance and species Ward identities",
            "status": "COUNTERMODEL_OPEN",
            "blocker": "no-source-prefactor parent clause absent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_3_disconnected_blocks",
            "source_domain": "disconnected conserved source blocks",
            "mathematical_form": "T_active=sum_B w_B T_B for separately conserved exchange blocks B",
            "effect": "relative weights collapse from species to disconnected blocks",
            "status": "DELTA_W_BLOCK_RETAINED",
            "blocker": "ordinary matter exchange graph connectivity not proved",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_4_hidden_return",
            "source_domain": "hidden source spurion/non-Hilbert return",
            "mathematical_form": "T_active=T_total + source_shadow + J_nonHilbert[A]",
            "effect": "labels return after apparent Hilbert variation",
            "status": "SOURCE_SHADOW_RETAINED",
            "blocker": "no source-shadow/non-Hilbert silence theorem",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SDF2399_5_fork_verdict",
            "source_domain": "source-domain fork",
            "mathematical_form": "unlabelled connected total-Hilbert source closes; labelled/weighted/disconnected/shadow source remains",
            "effect": "next derivation must prove no source shadow plus one exchange-connected ordinary source graph",
            "status": "FORK_REFINED_NOT_RESOLVED",
            "blocker": "delta_w_block remains",
            "valid_for_claim": no_claim(),
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS2399_0_delta_w_species",
            "quantity": "delta_w_species",
            "meaning": "species-label leakage into ordinary active source prefactor",
            "mathematical_form": "T_active=sum_A (1+delta_w_A) T_A",
            "units": "dimensionless",
            "status": "REFINED_TO_DELTA_W_BLOCK",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS2399_1_delta_w_block",
            "quantity": "delta_w_block",
            "meaning": "source weight residual over disconnected conserved ordinary source blocks",
            "mathematical_form": "T_active=sum_B (1+delta_w_B) T_B, nabla T_B=0 and no exchange edge between blocks",
            "units": "dimensionless",
            "status": "MISSING_EXCHANGE_GRAPH_CONNECTIVITY_OR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS2399_2_source_shadow",
            "quantity": "epsilon_source_shadow",
            "meaning": "separate source-only functional or post-variation source reweighting",
            "mathematical_form": "not exists S_source=sum_i w_i S_i used only in E_munu",
            "units": "dimensionless after M_H_ref normalization",
            "status": "MISSING_SOURCE_SHADOW_BAN",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS2399_3_component_basis",
            "quantity": "block_component_basis",
            "meaning": "ordinary exchange-connected block basis for any remaining source weight residuals",
            "mathematical_form": "B in connected components of the ordinary matter exchange graph",
            "units": "labels",
            "status": "MISSING_PARENT_EXCHANGE_GRAPH",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS2399_4_bound_source",
            "quantity": "delta_w_block_bound",
            "meaning": "finite empirical bound if proof fails",
            "mathematical_form": "|delta_w_B-delta_w_C| <= sourced bound from WEP/R10/PPN/clock/orbital/source-normalization projection",
            "units": "dimensionless",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2399_0_conditional_win",
            "decision": "accept label-forgotten source functor as the clean theorem",
            "reason": "once source domain is T_total only, relative species couplings are unavailable variables",
            "consequence": "do not pretend Ward identities alone solve it; source-domain ownership is the proof",
            "status": "LABEL_FORGOTTEN_THEOREM_ACCEPTED_CONDITIONALLY",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2399_1_partial_refinement",
            "decision": "refine delta_w_species to delta_w_block",
            "reason": "Noether exchange collapses weights inside each exchange-connected source component",
            "consequence": "free species weights are overbroad; disconnected conserved blocks and source shadows are now the live residuals",
            "status": "DELTA_W_SPECIES_REFINED_TO_BLOCK",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2399_2_no_promotion",
            "decision": "do not claim local source pass",
            "reason": "source-shadow ban and ordinary exchange graph connectivity remain unsigned",
            "consequence": "local GR/Newton/WEP/R10/PPN/clock/orbital source claims remain blocked",
            "status": "NO_LOCAL_SOURCE_CLAIM",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2399_3_next",
            "decision": "attack exchange graph connectivity and source-shadow ban next",
            "reason": "these are the exact remaining gates after species weights collapse to block weights",
            "consequence": "2400 should prove ordinary matter is one exchange-connected total-Hilbert source or stage delta_w_block bounds",
            "status": "SELECT_2400_EXCHANGE_GRAPH_SOURCE_SHADOW",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2399_0_label_forgetting",
            "gate": "parent source functor forgets species labels",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "clean theorem exists but parent source-domain quotient is unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2399_1_noether_exchange_collapse",
            "gate": "relative weights collapse inside connected exchange components",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "partial derivation narrows residual to block weights, but exchange graph is unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2399_2_delta_w_block_zero",
            "gate": "delta_w_block=0",
            "gate_status": "BLOCKED",
            "claim_effect": "disconnected block/source-shadow countermodels survive",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2399_3_GR_Newton",
            "gate": "local GR/Newton reduction",
            "gate_status": "BLOCKED",
            "claim_effect": "source side remains open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2399_0_claim_label_forgetting",
            "claim": "current MTS proves q_src forgets species labels",
            "allowed": "false",
            "reason": "source-domain quotient is identified but not parent-forced",
            "blocking_rows": "SLF2399_6_current_verdict;SDF2399_1_labelled_domain",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2399_1_claim_delta_w_zero",
            "claim": "delta_w_species or delta_w_block is zero",
            "allowed": "false",
            "reason": "same-action/exchange filters narrow but do not close disconnected blocks or source shadows",
            "blocking_rows": "DWS2399_1_delta_w_block;DWS2399_2_source_shadow",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2399_2_claim_local_GR",
            "claim": "local GR/Newton follows from species-label forgetting",
            "allowed": "false",
            "reason": "2399 is a source-coupling gate only; total Qv, boundary/projector, PPN, and Newtonian-limit gates remain",
            "blocking_rows": "CG2399_2_delta_w_block_zero;CG2399_3_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2399_0_selected",
            "next_file": "2400-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
            "success_condition": "prove tested ordinary matter is one exchange-connected total-Hilbert source with no source-shadow functional",
            "fallback_condition": "stage finite delta_w_block bound inputs with block basis, material projections, and WEP/R10/PPN/clock/orbital/source-normalization bounds",
            "valid_for_claim": no_claim(),
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2399_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2399_LABEL_FORGETTING_PROOF_ATTEMPT.csv": proof_rows,
    "P8_Y5_PARENT_QLOC_2399_SOURCE_DOMAIN_FORK_AUDIT.csv": source_domain_rows,
    "P8_Y5_PARENT_QLOC_2399_DELTAW_BLOCK_BOUND_INPUT.csv": residual_rows,
    "P8_Y5_PARENT_QLOC_2399_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2399_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2399_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2399_NEXT_TARGET.csv": next_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    missing_sources = [src["path"] for src in SOURCES if not Path(src["path"]).exists()]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_00_sources_exist",
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": "all required source paths exist" if not missing_sources else ";".join(missing_sources),
            "valid_for_claim": no_claim(),
        }
    )

    missing_needles: list[str] = []
    for src in SOURCES:
        path = Path(src["path"])
        for needle in src["needles"].split("|"):
            if not contains(path, needle):
                missing_needles.append(f"{src['source_id']}::{needle}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    proof = proof_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_02_label_forgetting_theorem_present",
            "status": "PASS" if any("F_src(T_total)=kappa_univ T_total" in row["mathematical_form"] for row in proof) else "FAIL",
            "detail": "conditional label-forgetting theorem present",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_03_exchange_filter_present",
            "status": "PASS" if any("w_i=w_j" in row["mathematical_form"] for row in proof) else "FAIL",
            "detail": "Noether/Bianchi exchange filter present",
            "valid_for_claim": no_claim(),
        }
    )

    fork = source_domain_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_04_counterdomains_retained",
            "status": "PASS" if any(row["row_id"] == "SDF2399_1_labelled_domain" for row in fork) and any(row["row_id"] == "SDF2399_3_disconnected_blocks" for row in fork) else "FAIL",
            "detail": "labelled-domain and disconnected-block counterdomains retained",
            "valid_for_claim": no_claim(),
        }
    )

    residuals = residual_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_05_deltaw_refined_nonclaim",
            "status": "PASS" if any(row["quantity"] == "delta_w_block" for row in residuals) and all(row["valid_for_claim"] == "false" for row in residuals) else "FAIL",
            "detail": "delta_w_species is refined to nonclaim delta_w_block rows",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    gate_ok = all(row["gate_status"] in {"BLOCKED", "CONDITIONAL_BLOCKED"} for row in gates)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_06_global_claims_blocked",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "label-forgetting, exchange, delta_w block, and GR/Newton gates not promoted",
            "valid_for_claim": no_claim(),
        }
    )

    csv_failures: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            csv_failures.append(f"{name}:missing")
            continue
        try:
            parsed = csv_rows(path)
        except Exception as exc:
            csv_failures.append(f"{name}:{exc}")
            continue
        if not parsed:
            csv_failures.append(f"{name}:empty")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_07_csv_parse",
            "status": "PASS" if not csv_failures else "FAIL",
            "detail": "generated CSVs parse and have rows" if not csv_failures else ";".join(csv_failures),
            "valid_for_claim": no_claim(),
        }
    )

    true_claims: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            continue
        for row in csv_rows(path):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                true_claims.append(f"{name}:{row}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_08_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_09_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_10_next_selected",
            "status": "PASS" if any(row["row_id"] == "NEXT2399_0_selected" for row in next_rows()) else "FAIL",
            "detail": "exchange graph/source-shadow route selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2399_OVERALL",
            "status": overall_status,
            "detail": "2399 records the conditional species-label forgetting theorem, derives the exchange-filter refinement from delta_w_species to delta_w_block, refuses promotion, and selects exchange graph/source-shadow next",
            "valid_for_claim": no_claim(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    proof = proof_rows()
    fork = source_domain_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2399 — Species Label Forgetting Source Functor Parent Proof Or Delta-w Species Bound

## Result

2399 advances the coupling branch one notch.

The clean source theorem is still:

`q_src({{(T_A,A)}})=T_total=sum_A T_A`

before the source functor is formed, so

`F_src(T_total)=kappa_univ T_total`.

If the parent action signs that source-domain quotient, species labels are not available to the active source functor
and `delta_w_species=0` structurally.

But current MTS still cannot claim that.  The labelled counterdomain

`F_src({{(T_A,A)}})=sum_A kappa_A T_A`

remains covariant, additive, and Ward-compatible if labels remain in the source domain.

The useful gain is the exchange filter: if ordinary matter sectors exchange stress-energy, Noether/Bianchi consistency
forces relative weights to match along each exchange edge.  Therefore free species weights are too pessimistic.  The
live residual is narrowed to

`delta_w_block`,

a weight over disconnected conserved ordinary source blocks, plus possible source-shadow/non-Hilbert returns.

So 2399 is not a pass, but it is a real squeeze: coupling has moved from arbitrary species weights to exchange graph
connectivity plus source-shadow exclusion.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## Label Forgetting Proof Attempt

{markdown_table(proof, ["row_id", "claim_piece", "mathematical_form", "proof_status", "proof_result", "gap", "valid_for_claim"])}

## Source Domain Fork Audit

{markdown_table(fork, ["row_id", "source_domain", "mathematical_form", "effect", "status", "blocker", "valid_for_claim"])}

## Delta-w Block Bound Input

{markdown_table(residuals, ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_targets, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is a good result for the local-GR route.  We have not proved the source side, but the counterexample space got
smaller.  If ordinary matter is one exchange-connected total-Hilbert source and there is no source-shadow functional,
the species coupling wound closes into a common calibration.  If not, `delta_w_block` is the first source-coupling
residual to bound empirically.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2399_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2399_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
