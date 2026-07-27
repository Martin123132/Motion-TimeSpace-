from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_ORDINARY_MATTER_EXCHANGE_GRAPH_CONNECTIVITY_AND_SOURCE_SHADOW_BAN_OR_DELTAW_BLOCK_BOUND_2400"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2400-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2400_2399_doc",
        "path": str(post("2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md")),
        "needles": "NEXT2399_0_selected|delta_w_block|sum_i w_i C_i^nu=0|SLF2399_4_noether_exchange_filter|VAL2399_OVERALL",
        "role": "immediate parent: selected exchange graph/source-shadow target",
    },
    {
        "source_id": "SRC2400_2399_label_attempt",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2399_LABEL_FORGETTING_PROOF_ATTEMPT.csv")),
        "needles": "SLF2399_3_same_action_filter|SLF2399_4_noether_exchange_filter|SLF2399_6_current_verdict",
        "role": "species-label forgetting proof attempt",
    },
    {
        "source_id": "SRC2400_2399_domain_fork",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2399_SOURCE_DOMAIN_FORK_AUDIT.csv")),
        "needles": "SDF2399_3_disconnected_blocks|SDF2399_4_hidden_return|SDF2399_5_fork_verdict",
        "role": "counterdomains left open by 2399",
    },
    {
        "source_id": "SRC2400_1765_doc",
        "path": str(post("1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md")),
        "needles": "delta_w_species -> delta_w_block|THO1765_3_source_shadow_ban|SZ1765_1_no_source_shadow|VAL1765_OVERALL",
        "role": "earlier total-Hilbert/no-prefactor attempt",
    },
    {
        "source_id": "SRC2400_1765_no_source_prefactor",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv")),
        "needles": "NSP1765_1_same_action_filter|NSP1765_2_exchange_filter|NSP1765_4_current_verdict",
        "role": "same-action and exchange-filter source",
    },
    {
        "source_id": "SRC2400_1765_total_owner",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv")),
        "needles": "THO1765_1_total_hilbert_derivative|THO1765_2_interaction_stress|THO1765_3_source_shadow_ban",
        "role": "total Hilbert owner and source-shadow gap",
    },
    {
        "source_id": "SRC2400_954_parent_clause",
        "path": str(post("source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv")),
        "needles": "PAC954_1_no_source_prefactors|PAC954_2_total_Hilbert_derivative|PAC954_5_GR_source_limit_clause",
        "role": "older parent-action source-side clause",
    },
    {
        "source_id": "SRC2400_977_constant_source",
        "path": str(post("source-intake/mts_residuals/P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv")),
        "needles": "CSC977_3_hilbert_source_current|CSC977_4_single_universal_kappa|CSC977_5_bianchi_limit",
        "role": "constant source certificate attempt and Bianchi caveat",
    },
]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCES:
        path = Path(source["path"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_path": source["path"],
                "exists": str(path.exists()).lower(),
                "needles": source["needles"],
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def exchange_graph_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "EG2400_0_vertices",
            "object": "ordinary matter exchange graph vertices",
            "definition": "V_ord={A: ordinary Hilbert-source sector T_A is present in S_matter}",
            "condition": "sector stress must be obtained from the same observed coframe/metric variation",
            "status": "DEFINITION",
            "issue": "component choices are bookkeeping until the parent action fixes the actual matter ontology",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EG2400_1_edges",
            "object": "exchange edges",
            "definition": "edge A--B exists when an allowed parent matter solution has nonzero local exchange current C_AB^nu with nabla_mu T_A^{mu nu}=C_AB^nu and nabla_mu T_B^{mu nu}=-C_AB^nu",
            "condition": "exchange current must be ordinary-sector, not a hidden source-shadow return",
            "status": "DEFINITION",
            "issue": "needs parent-signed matter-sector map before real SM/clock/orbital cases can be stamped",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EG2400_2_components",
            "object": "connected ordinary source blocks",
            "definition": "B_I are connected components of G_ord=(V_ord,E_exchange); T_BI=sum_{A in B_I} T_A",
            "condition": "within a connected component, arbitrary allowed exchange histories are admitted",
            "status": "DERIVED_BOOKKEEPING",
            "issue": "if G_ord is not connected, each component may carry one common residual weight",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EG2400_3_weighted_source",
            "object": "weighted source ansatz",
            "definition": "E^{mu nu}=kappa_0 sum_A (1+epsilon_A) T_A^{mu nu}",
            "condition": "epsilon_A are constant source weights after the same-action filter has removed action-level duplication",
            "status": "TEST_ANSATZ",
            "issue": "nonconstant epsilon_A would create derivative terms and is a separate forbidden slot",
            "valid_for_claim": "false",
        },
    ]


def connectivity_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CONN2400_0_bianchi_start",
            "claim": "Bianchi/Noether consistency tests weighted source universality",
            "derivation": "0=nabla_mu E^{mu nu}=kappa_0 sum_A (1+epsilon_A) nabla_mu T_A^{mu nu}",
            "condition": "geometric left side has the GR/EH identity and matter equations give sum_A nabla_mu T_A^{mu nu}=0",
            "result": "only weighted exchange imbalance remains",
            "status": "CONDITIONAL_DERIVATION",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CONN2400_1_edge_constraint",
            "claim": "one nonzero exchange edge collapses two weights",
            "derivation": "for an A--B exchange, weighted divergence contains (epsilon_A-epsilon_B) C_AB^nu",
            "condition": "C_AB^nu can vary over allowed local histories and is not identically zero",
            "result": "epsilon_A=epsilon_B on that edge",
            "status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CONN2400_2_connected_component",
            "claim": "connected ordinary exchange component has one common calibration",
            "derivation": "edge equality propagates along every path in G_ord, so epsilon_A=epsilon_B for all A,B in the same B_I",
            "condition": "G_ord component is connected through nonzero ordinary exchange currents",
            "result": "T_active on B_I is kappa_I T_BI rather than species-by-species kappa_A T_A",
            "status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CONN2400_3_global_connectivity",
            "claim": "all ordinary matter has one common source calibration",
            "derivation": "if G_ord has exactly one connected component, all epsilon_A collapse to epsilon_common",
            "condition": "parent signs ordinary matter exchange connectivity and no source-shadow sector returns independent weights",
            "result": "delta_w_block=0 up to one absorbed Newton/G calibration",
            "status": "NOT_CLAIMED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CONN2400_4_current_verdict",
            "claim": "current MTS proves local source universality",
            "derivation": "2399+2400 derive the collapse rule, not the parent-signed connectivity/source-shadow facts",
            "condition": "missing parent matter ontology, hidden source-shadow exclusion, and arena projections",
            "result": "delta_w_species is no longer the right wound; delta_w_block plus delta_w_shadow are the remaining wounds",
            "status": "PARTIAL_REFINEMENT_NOT_PROOF",
            "valid_for_claim": "false",
        },
    ]


def source_shadow_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSB2400_0_forbidden_shape",
            "slot": "source-shadow functional",
            "definition": "S_shadow[e_obs,Phi]=sum_I eta_I int d^4x sqrt(-g_obs) U_I(Phi,e_obs,T_BI) whose metric/coframe derivative contributes to the active source but is not ordinary matter stress",
            "needed_ban": "parent action grammar must exclude source-only, representative-dependent, and post-variation source weighting functionals",
            "status": "IDENTIFIED_NOT_EXCLUDED",
            "issue": "same-action filter does not by itself ban a hidden gravitational/source functional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSB2400_1_total_hilbert_owner",
            "slot": "total Hilbert source owner",
            "definition": "T_total := -2/sqrt(-g_obs) delta S_matter/delta g_obs; interactions and binding stresses are inside this same derivative",
            "needed_ban": "no independent active-source owner besides S_matter and the geometric EH/MTS side",
            "status": "PARTIAL_FROM_1765_954_977",
            "issue": "existing clauses state the need but do not yet prove the parent grammar",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSB2400_2_disformal_weyl_return",
            "slot": "representative-dependent return",
            "definition": "matter sees e_obs but hidden Weyl/disformal dependence of e_obs on MTS fields can return apparent source weights after projection",
            "needed_ban": "observed coframe/frame lock plus quotient invariance must eliminate direct species/block-labelled coefficients",
            "status": "OPEN",
            "issue": "ties back to the R2FR frame-source leak and q_loc closure gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSB2400_3_current_verdict",
            "slot": "source-shadow ban",
            "definition": "no non-Hilbert ordinary-source functional may feed q_loc^nu or local field equations",
            "needed_ban": "explicit parent-action exclusion theorem",
            "status": "BLOCKED_AS_PROOF",
            "issue": "without this theorem, local GR remains a conditional branch rather than a derived limit",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB2400_0_delta_w_block",
            "residual": "delta_w_block",
            "definition": "max_{I,J}|epsilon_I-epsilon_J| over disconnected ordinary exchange components B_I",
            "observable_link": "WEP/R10, PPN, clock-comparison, orbital composition tests",
            "needed_input": "parent-signed component map plus arena projection coefficients",
            "status": "BOUND_INPUT_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB2400_1_delta_w_shadow",
            "residual": "delta_w_shadow",
            "definition": "effective source-weight leakage from non-Hilbert source-shadow functionals or representative-dependent returns",
            "observable_link": "same arenas as delta_w_block, plus local q_loc residual vector",
            "needed_input": "source-shadow exclusion theorem or explicit shadow coupling coefficient",
            "status": "ROOT_BLOCKER",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB2400_2_single_component_common_mode",
            "residual": "epsilon_common",
            "definition": "one universal common calibration on a connected ordinary component",
            "observable_link": "absorbed into measured G/Newton normalization, not a WEP-violating local residual",
            "needed_input": "one connected ordinary component and no source shadow",
            "status": "BENIGN_IF_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWB2400_3_bound_rows",
            "residual": "delta_w_block_bound_pack",
            "definition": "future numeric pack should carry tau_R10, tau_PPN, tau_clock, tau_orbital and projection coefficients K_X,Qbar_XH,lambda_X",
            "observable_link": "local tests if proof route fails",
            "needed_input": "real source-backed bounds and parent projection coefficients",
            "status": "NOT_BUILT_NUMERICALLY_HERE",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2400_0_keep_derivation_route",
            "decision": "keep deriving rather than jumping to fits",
            "reason": "exchange connectivity gives an exact equality theorem if parent facts are signed",
            "consequence": "do not spend the next step on numeric delta_w bounds until source-shadow grammar is attacked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2400_1_refine_wound",
            "decision": "replace species wound with block/shadow wound",
            "reason": "Noether/Bianchi exchange edges force equal weights inside connected ordinary components",
            "consequence": "future local tests should bound delta_w_block and delta_w_shadow, not raw species weights",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2400_2_no_local_GR_promotion",
            "decision": "do not promote local GR/Newton reduction",
            "reason": "ordinary exchange graph connectivity and source-shadow exclusion are not parent-signed",
            "consequence": "GR bridge remains promising but conditional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2400_3_next",
            "decision": "attack source-shadow exclusion grammar next",
            "reason": "this is now the highest-leverage remaining coupling loophole",
            "consequence": "select 2401 source-shadow functional exclusion parent-action grammar",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2400_0_exchange_connectivity",
            "gate": "ordinary exchange graph connected",
            "status": "BLOCKED",
            "why": "2400 proves the consequence of connectivity, not the parent-signed graph itself",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2400_1_source_shadow_ban",
            "gate": "source-shadow functional excluded",
            "status": "BLOCKED",
            "why": "no explicit parent-action grammar theorem yet forbids hidden source functional returns",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2400_2_delta_w_block_zero",
            "gate": "delta_w_block=0",
            "status": "BLOCKED",
            "why": "requires one connected ordinary block plus source-shadow ban",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2400_3_GR_Newton",
            "gate": "local GR/Newton reduction",
            "status": "BLOCKED",
            "why": "source universality is refined but not closed",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2400_0_claim_connected_graph",
            "claim": "MTS proves all ordinary matter sectors are exchange-connected",
            "allowed": "false",
            "reason": "requires parent-signed matter ontology and exchange-current graph",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2400_1_claim_no_source_shadow",
            "claim": "MTS excludes all source-shadow functionals",
            "allowed": "false",
            "reason": "source-shadow grammar has been isolated but not proved impossible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2400_2_claim_local_GR",
            "claim": "local GR/Newton limit is derived",
            "allowed": "false",
            "reason": "2400 is a coupling-collapse lemma, not the final local limit proof",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2400_0_selected",
            "next_doc": "2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md",
            "why": "source-shadow is now the cleanest remaining loophole after exchange-connectivity collapses block weights conditionally",
            "expected_output": "either a parent grammar theorem banning source shadows, or a source-shadow bound pack with explicit nonclaim rows",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2400_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2400_EXCHANGE_GRAPH_DEFINITION.csv": exchange_graph_rows,
    "P8_Y5_PARENT_QLOC_2400_CONNECTIVITY_PROOF_ATTEMPT.csv": connectivity_proof_rows,
    "P8_Y5_PARENT_QLOC_2400_SOURCE_SHADOW_BAN_AUDIT.csv": source_shadow_rows,
    "P8_Y5_PARENT_QLOC_2400_DELTAW_BLOCK_BOUND_INPUT.csv": residual_rows,
    "P8_Y5_PARENT_QLOC_2400_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2400_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2400_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2400_NEXT_TARGET.csv": next_target_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sources_exist() -> bool:
    return all(Path(source["path"]).exists() for source in SOURCES)


def needles_found() -> bool:
    for source in SOURCES:
        path = Path(source["path"])
        if not path.exists():
            return False
        text = read_text(path)
        for needle in source["needles"].split("|"):
            if needle and needle not in text:
                return False
    return True


def csvs_parse() -> bool:
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            return False
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def no_claim_flags() -> bool:
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            return False
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for value in row.values():
                    if isinstance(value, str) and value.strip().lower() == "valid_for_claim=true":
                        return False
                if row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def formalization_untouched_by_script() -> bool:
    return not str(DOC_PATH).startswith(str(FORMALIZATION_ROOT)) and not str(RESIDUALS).startswith(str(FORMALIZATION_ROOT))


def validation_rows() -> list[dict[str, str]]:
    generated_text = "\n".join(
        [
            *[str(row) for row in exchange_graph_rows()],
            *[str(row) for row in connectivity_proof_rows()],
            *[str(row) for row in source_shadow_rows()],
            *[str(row) for row in residual_rows()],
            *[str(row) for row in decision_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2400_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2400_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2400_02_exchange_graph_defined",
            "status": "PASS" if "G_ord=(V_ord,E_exchange)" in generated_text and "C_AB^nu" in generated_text else "FAIL",
            "detail": "ordinary exchange graph and edge current are defined",
        },
        {
            "row_id": "VAL2400_03_edge_collapse_theorem",
            "status": "PASS" if "epsilon_A=epsilon_B on that edge" in generated_text else "FAIL",
            "detail": "edge exchange collapse theorem recorded",
        },
        {
            "row_id": "VAL2400_04_block_refinement",
            "status": "PASS" if "delta_w_block plus delta_w_shadow" in generated_text else "FAIL",
            "detail": "raw species wound refined to block/shadow wounds",
        },
        {
            "row_id": "VAL2400_05_source_shadow_retained",
            "status": "PASS" if "IDENTIFIED_NOT_EXCLUDED" in generated_text and "BLOCKED_AS_PROOF" in generated_text else "FAIL",
            "detail": "source-shadow route is isolated but not claimed closed",
        },
        {
            "row_id": "VAL2400_06_global_claims_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_gate_rows()) else "FAIL",
            "detail": "exchange connectivity, shadow ban, delta_w zero, and GR/Newton gates remain blocked",
        },
        {
            "row_id": "VAL2400_07_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2400_08_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2400_09_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2400_10_next_selected",
            "status": "PASS" if "2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md" in generated_text else "FAIL",
            "detail": "source-shadow grammar route selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2400_OVERALL",
            "status": overall,
            "detail": "2400 derives the exchange-edge weight-collapse lemma, refines the coupling wound to delta_w_block/delta_w_shadow, refuses local-GR promotion, and selects source-shadow grammar next",
        }
    )
    return [{"branch_id": BRANCH_ID, **row} for row in checks]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    body = f"""# 2400 — Ordinary Matter Exchange Graph Connectivity And Source-Shadow Ban Or Delta-w Block Bound

## Result

This checkpoint gives the cleanest coupling result so far:

If ordinary matter sectors are vertices in an exchange graph `G_ord`, and an edge `A--B` means the parent matter equations allow a nonzero exchange current `C_AB^nu`, then the weighted source ansatz

`E^{{mu nu}}=kappa_0 sum_A (1+epsilon_A) T_A^{{mu nu}}`

is Bianchi/Noether consistent on that edge only if

`(epsilon_A-epsilon_B) C_AB^nu=0`.

For a genuine nonzero edge this forces `epsilon_A=epsilon_B`.  Along a connected component, equality propagates.  So species-level source weights collapse into one common calibration per connected ordinary exchange block.

That is a real tightening: the old wound `delta_w_species` becomes

`delta_w_block + delta_w_shadow`.

The remaining loopholes are now sharp:

1. prove the ordinary matter exchange graph has one connected component under the parent action;
2. prove no source-shadow functional can return hidden non-Hilbert source weights.

Neither is promoted here.  Local GR/Newton remains blocked.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## Exchange Graph Definition

{markdown_table(exchange_graph_rows(), ["row_id", "object", "definition", "condition", "status", "issue", "valid_for_claim"])}

## Connectivity Proof Attempt

{markdown_table(connectivity_proof_rows(), ["row_id", "claim", "derivation", "condition", "result", "status", "valid_for_claim"])}

## Source-Shadow Ban Audit

{markdown_table(source_shadow_rows(), ["row_id", "slot", "definition", "needed_ban", "status", "issue", "valid_for_claim"])}

## Delta-w Block Bound Input

{markdown_table(residual_rows(), ["row_id", "residual", "definition", "observable_link", "needed_input", "status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows(), ["row_id", "decision", "reason", "consequence", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["row_id", "gate", "status", "why", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(next_target_rows(), ["row_id", "next_doc", "why", "expected_output", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

The coupling problem is not solved, but it is now much less foggy.  We no longer have to fear arbitrary
species-by-species source weights if the ordinary source graph is connected.  The real enemy is narrower:
either disconnected conserved source blocks, or a hidden source-shadow functional.  That makes the next proof
target precise enough to attack rather than just circle.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2400_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2400_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
