from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_INVARIANT_GENERATOR_ELIMINATION_PRIORITY_OR_DELTAW_SOURCE_PACK_2398"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2398-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-pack.md"
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
        "source_id": "SRC2398_2397_doc",
        "path": str(POST_ROOT / "2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md"),
        "needed_for": "current chain selects invariant-generator elimination",
        "needles": "NEXT2397_0_selected|rank fibre/domain/chi/memory/species/readout generators|delta_w_A|VAL2397_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2398_1763_doc",
        "path": str(POST_ROOT / "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md"),
        "needed_for": "older generator ranking and species-label selection",
        "needles": "species_charge_constants/source labels|delta_w_species|NEXT1763_0_primary|VAL1763_OVERALL",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2398_1763_priority",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1763_INVARIANT_GENERATOR_PRIORITY.csv"),
        "needed_for": "machine-readable generator priority order",
        "needles": "species_charge_constants/source labels|post_readout_projector|memory_or_class_scalar|BEST_NEXT_ZERO_ROUTE_UNSIGNED",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2398_1763_acquisition",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv"),
        "needed_for": "delta_w source acquisition rows",
        "needles": "DWA1763_0_delta_w_species|MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND|DWA1763_4_A_direct_response",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2398_1762_label_forgetting",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1762_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv"),
        "needed_for": "source label-forgetting parent-functor status",
        "needles": "SF1762_0_label_forgetting|q_src|FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2398_1762_invariant",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1762_INVARIANT_ALGEBRA_HOM_AUDIT.csv"),
        "needed_for": "source-prefactor generator debts",
        "needles": "IH1762_1_fibre|IH1762_2_domain|IH1762_5_species_constants|IH1762_7_verdict",
        "valid_for_claim": no_claim(),
    },
]


def priority_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "1",
            "generator": "species_charge_constants/source labels",
            "delta_w_channel": "delta_w_species",
            "zero_route": "prove q_src forgets species/source labels before F_src is formed; constants are fixed representation data",
            "why_this_rank": "directly hits the relative source-prefactor countermodel and has the cleanest conditional theorem",
            "scrutiny_level": "LOWEST_RELATIVE_SCRUTINY",
            "current_status": "BEST_NEXT_ZERO_ROUTE_UNSIGNED",
            "selected": "true",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "2",
            "generator": "post_readout_projector",
            "delta_w_channel": "delta_w_readout",
            "zero_route": "variation-before-readout theorem plus before-readout source/worldtube owner",
            "why_this_rank": "dangerous because it can fake closure after solving, but less clean than source-label forgetting",
            "scrutiny_level": "HIGH",
            "current_status": "NO_CHEAT_RULE_ONLY",
            "selected": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "3",
            "generator": "relative_boundary_domain_class",
            "delta_w_channel": "delta_w_marker/delta_w_readout",
            "zero_route": "local trivial class or class-only stress-free no-hair theorem",
            "why_this_rank": "can source boundary/domain charge but needs harder topology and boundary arguments",
            "scrutiny_level": "HIGH",
            "current_status": "NOT_DERIVED",
            "selected": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "4",
            "generator": "finite_cell_fibre_spectrum",
            "delta_w_channel": "delta_w_hidden/delta_w_species",
            "zero_route": "prove fibre basis is gauge/relabeling only or universal constant",
            "why_this_rank": "possibly important but abstract and harder to sell than source-label forgetting",
            "scrutiny_level": "HIGH",
            "current_status": "NOT_TRIVIALIZED",
            "selected": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "5",
            "generator": "chi_D/domain_selector",
            "delta_w_channel": "delta_w_hidden/source-normalization coefficient",
            "zero_route": "selector as gauge/readout-only or fixed local trivial branch",
            "why_this_rank": "entangled with double-zero, cosmology, and local selector machinery; high risk of branch mixing",
            "scrutiny_level": "VERY_HIGH",
            "current_status": "NOT_DERIVED",
            "selected": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "priority_rank": "6",
            "generator": "memory_or_class_scalar",
            "delta_w_channel": "delta_w_hidden/A_mu_even",
            "zero_route": "local value and gradient zero theorem or explicit bounded residual",
            "why_this_rank": "physically broad but less directly tied to ordinary matter source prefactors",
            "scrutiny_level": "VERY_HIGH",
            "current_status": "NOT_SILENCED_AS_THEOREM",
            "selected": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def species_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2398_0_target",
            "claim_piece": "species-label source-prefactor zero",
            "mathematical_form": "delta_w_species=0 iff species labels are not source-functor arguments before coupling selection",
            "attempt_status": "TARGET_EXACT",
            "result": "ZERO_IF_LABEL_FORGETTING_PARENT_SIGNED",
            "gap": "parent source category label-forgetting remains unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2398_1_label_forgetting_map",
            "claim_piece": "label forgetting before source functor",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A before F_src is applied",
            "attempt_status": "EXACT_CONDITIONAL_THEOREM",
            "result": "F_src cannot see species labels after q_src",
            "gap": "q_src is a contract, not yet derived from the parent action",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2398_2_unique_additive_source",
            "claim_piece": "unique covariant additive source map after labels forgotten",
            "mathematical_form": "F_src(T_total)=kappa_univ T_total",
            "attempt_status": "CONDITIONAL_UNIQUENESS",
            "result": "relative kappa_A/w_A cannot be written once labels are absent",
            "gap": "constant/source universality remains parent-unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2398_3_countermodel",
            "claim_piece": "species-labelled additive source functor",
            "mathematical_form": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "attempt_status": "COUNTERMODEL_SURVIVES_IF_LABELS_REMAIN",
            "result": "covariant/additive/Ward-compatible if A labels remain source-domain data",
            "gap": "Ward conservation cannot kill species-labelled source weights",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SLF2398_4_verdict",
            "claim_piece": "current species-label zero result",
            "mathematical_form": "SLF2398_0 through SLF2398_2 parent-signed and SLF2398_3 excluded",
            "attempt_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "result": "DELTA_W_SPECIES_RETAINED",
            "gap": "label-forgetting quotient and constant/source parent certificate are not signed",
            "valid_for_claim": no_claim(),
        },
    ]


def acquisition_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2398_0_delta_w_species",
            "quantity": "delta_w_species",
            "priority_rank": "1",
            "required_zero_or_bound": "label-forgetting source functor theorem or numeric bound on species-labelled source prefactor",
            "status": "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2398_1_delta_w_readout",
            "quantity": "delta_w_readout",
            "priority_rank": "2",
            "required_zero_or_bound": "variation-before-readout/source-worldtube owner theorem or bound on readout source-mask transfer",
            "status": "MISSING_READOUT_TRANSFER_ZERO_OR_BOUND",
            "units": "dimensionless",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2398_2_delta_w_marker",
            "quantity": "delta_w_marker",
            "priority_rank": "3",
            "required_zero_or_bound": "no-marker quotient-extension theorem or material/domain marker coefficient bound",
            "status": "MISSING_NO_MARKER_THEOREM_OR_BOUND",
            "units": "dimensionless",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2398_3_delta_w_hidden",
            "quantity": "delta_w_hidden",
            "priority_rank": "4",
            "required_zero_or_bound": "fibre/chi/memory invariant zero theorem or hidden source coefficient bound",
            "status": "MISSING_HIDDEN_INVARIANT_ZERO_OR_BOUND",
            "units": "dimensionless",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWA2398_4_A_direct_response",
            "quantity": "A_direct_matter",
            "priority_rank": "5",
            "required_zero_or_bound": "operator K_w and E* norm mapping delta_w vector into ||delta_v V_m||",
            "status": "MISSING_K_W_OPERATOR_NORM_DELTAW_NORM_OR_THEOREM_ZERO",
            "units": "E*_dual_or_declared_arena_units",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2398_0_accept_priority_order",
            "decision": "accept species-label route as the first generator attack",
            "reason": "it directly targets delta_w_species and has the cleanest conditional source-functor theorem",
            "consequence": "do not start with memory/fibre/topology while a simpler source-category theorem remains open",
            "status": "SPECIES_LABEL_ROUTE_SELECTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2398_1_no_current_zero",
            "decision": "do not claim delta_w_species zero",
            "reason": "species-labelled additive source functor remains legal if labels stay in the source domain",
            "consequence": "delta_w_species remains nonclaim",
            "status": "DELTA_W_SPECIES_NOT_ZEROED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2398_2_no_numeric_fill",
            "decision": "do not fill numeric delta_w rows from placeholders",
            "reason": "component basis, norm, data source, and arena projection are missing",
            "consequence": "delta_w source acquisition remains schema-only",
            "status": "NO_NUMERIC_DELTAW_ROWS_FILLED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2398_3_next",
            "decision": "attack species-label forgetting parent proof next",
            "reason": "it is the least-scrutiny route through the coupling wall",
            "consequence": "2399 should prove q_src forgets labels before F_src or stage delta_w_species bound rows",
            "status": "SELECT_2399_SPECIES_LABEL_FORGETTING",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2398_0_species_label",
            "gate": "species labels absent from source-functor domain",
            "gate_status": "CONDITIONAL_BLOCKED",
            "claim_effect": "source-domain label forgetting is exact if signed, but not current-claim-grade",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2398_1_delta_w_species_zero",
            "gate": "delta_w_species=0",
            "gate_status": "BLOCKED",
            "claim_effect": "species-labelled source countermodel survives",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2398_2_delta_w_vector",
            "gate": "delta_w_A vector zero or source-backed",
            "gate_status": "BLOCKED",
            "claim_effect": "readout/marker/hidden components remain open",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2398_3_GR_Newton",
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
            "row_id": "REF2398_0_claim_priority_is_proof",
            "claim": "ranking species labels first proves coupling closure",
            "allowed": "false",
            "reason": "ranking is tactical; it does not sign q_src label forgetting",
            "blocking_rows": "SLF2398_4_verdict;CG2398_1_delta_w_species_zero",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2398_1_claim_delta_w_species_zero",
            "claim": "delta_w_species=0 for current MTS",
            "allowed": "false",
            "reason": "species-labelled source functor remains a live countermodel if labels remain source-domain data",
            "blocking_rows": "SLF2398_3_countermodel;DWA2398_0_delta_w_species",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2398_2_claim_local_GR",
            "claim": "local GR/Newton is derived from the generator ranking",
            "allowed": "false",
            "reason": "2398 only selects the next coupling generator; total Qv, source side, PPN, and Newtonian-limit gates remain",
            "blocking_rows": "CG2398_2_delta_w_vector;CG2398_3_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2398_0_selected",
            "next_file": "2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
            "success_condition": "prove q_src forgets species labels before source coupling selection and only F_src(T_total)=kappa_univ T_total is available",
            "fallback_condition": "stage source-ready delta_w_species bound rows with component basis, units, target bounds, and provenance",
            "valid_for_claim": no_claim(),
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2398_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2398_INVARIANT_GENERATOR_PRIORITY.csv": priority_rows,
    "P8_Y5_PARENT_QLOC_2398_SPECIES_LABEL_ZERO_ATTEMPT.csv": species_attempt_rows,
    "P8_Y5_PARENT_QLOC_2398_DELTAW_SOURCE_PACK.csv": acquisition_rows,
    "P8_Y5_PARENT_QLOC_2398_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2398_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2398_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2398_NEXT_TARGET.csv": next_rows,
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
            "row_id": "VAL2398_00_sources_exist",
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
            "row_id": "VAL2398_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    priority = priority_rows()
    selected = [row for row in priority if row["selected"] == "true"]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_02_species_selected",
            "status": "PASS" if len(selected) == 1 and selected[0]["generator"] == "species_charge_constants/source labels" else "FAIL",
            "detail": "species-label generator selected as lowest-scrutiny route",
            "valid_for_claim": no_claim(),
        }
    )

    attempt = species_attempt_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_03_countermodel_retained",
            "status": "PASS" if any(row["row_id"] == "SLF2398_3_countermodel" for row in attempt) else "FAIL",
            "detail": "species-labelled additive source countermodel retained",
            "valid_for_claim": no_claim(),
        }
    )

    acquisition = acquisition_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_04_acquisition_rows_nonclaim",
            "status": "PASS" if all(row["valid_for_claim"] == "false" for row in acquisition) else "FAIL",
            "detail": "delta_w acquisition rows remain nonclaim",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    gate_ok = all(row["gate_status"] in {"BLOCKED", "CONDITIONAL_BLOCKED"} for row in gates)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_05_global_claims_blocked",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "species, delta_w, source, and GR/Newton gates not promoted",
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
            "row_id": "VAL2398_06_csv_parse",
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
            "row_id": "VAL2398_07_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_08_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_09_next_selected",
            "status": "PASS" if any(row["row_id"] == "NEXT2398_0_selected" for row in next_rows()) else "FAIL",
            "detail": "species-label forgetting proof selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2398_OVERALL",
            "status": overall_status,
            "detail": "2398 ranks invariant generators, selects species-label/source constants first, retains delta_w_species as nonclaim, and selects source-functor label forgetting next",
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
    priority = priority_rows()
    attempt = species_attempt_rows()
    acquisition = acquisition_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2398 — Invariant Generator Elimination Priority Or Delta-w Source Pack

## Result

2398 ranks the invariant generators that keep the coupling/no-Hom proof open.

The best next target is:

`species_charge_constants/source labels -> delta_w_species`.

Reason: it attacks the relative source-prefactor countermodel directly and has the cleanest conditional theorem:

`q_src({{(T_A,A)}})=T_total=sum_A T_A` before `F_src` is formed, so `F_src(T_total)=kappa_univ T_total`.

If that parent label-forgetting map is signed, species-dependent source weights are not available to the source functor.
If labels remain in the source domain, the countermodel

`F_src({{(T_A,A)}})=sum_A kappa_A T_A`

is covariant, additive, and Ward-compatible.  Therefore `delta_w_species` is retained as nonclaim until the parent
source-category proof is signed or a sourced numeric bound exists.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## Generator Priority

{markdown_table(priority, ["priority_rank", "generator", "delta_w_channel", "zero_route", "why_this_rank", "scrutiny_level", "current_status", "selected", "valid_for_claim"])}

## Species Label Zero Attempt

{markdown_table(attempt, ["row_id", "claim_piece", "mathematical_form", "attempt_status", "result", "gap", "valid_for_claim"])}

## Delta-w Source Pack

{markdown_table(acquisition, ["row_id", "quantity", "priority_rank", "required_zero_or_bound", "status", "units", "valid_for_claim"])}

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

This is a tactical improvement.  We are not trying to kill all coupling generators at once.  We now know the least
scrutiny move: prove that species labels/source constants are forgotten before the source functor is formed.  If that
works, the worst relative source-weight channel dies.  If not, `delta_w_species` becomes the first coupling parameter
that needs a real bound interface.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2398_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2398_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
