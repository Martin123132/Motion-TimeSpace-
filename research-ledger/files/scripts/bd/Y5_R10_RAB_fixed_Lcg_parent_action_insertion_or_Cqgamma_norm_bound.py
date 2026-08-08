from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1371"
TITLE = "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PARENT_ACTION_PATH = OUT_DIR / f"{PACK_ID}_FIXED_L0_PARENT_ACTION_INSERTION.csv"
LOCAL_RESIDUAL_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv"
CQGAMMA_NORM_PATH = OUT_DIR / f"{PACK_ID}_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv"
RUNNER_BOUND_PATH = OUT_DIR / f"{PACK_ID}_QLOC_GAMMA_BOUND_RUNNER_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1371_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1371_0_1370_doc",
            "source_path": "1370-Y5-R10-RAB-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
            "required_anchor": "NEXT1370_0_1371",
            "purpose": "1370 handoff to fixed-L0 parent action insertion or C_qgamma norm bound.",
        },
        {
            "source_id": "SRC1371_1_1370_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1370_NEXT_TARGET.csv",
            "required_anchor": "NEXT1370_0_1371",
            "purpose": "machine-readable 1371 target.",
        },
        {
            "source_id": "SRC1371_2_1370_lcg_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
            "required_anchor": "LCC1370_4_metric_silence_result",
            "purpose": "fixed-L0 metric-silence contract.",
        },
        {
            "source_id": "SRC1371_3_1370_cqgamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1370_WARD_SAFE_CQGAMMA_DERIVATION.csv",
            "required_anchor": "CQG1370_4_norm_bound",
            "purpose": "symbolic Ward-safe C_qgamma norm bound.",
        },
        {
            "source_id": "SRC1371_4_1287_volume",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
            "required_anchor": "KMC1287_0_volume_metric_response",
            "purpose": "volume metric response term that fixed M_L alone does not remove.",
        },
        {
            "source_id": "SRC1371_5_1289_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
            "required_anchor": "KVE1289_0_action_convention",
            "purpose": "action convention and chain-rule variation of Gamma_eff.",
        },
        {
            "source_id": "SRC1371_6_1289_delta_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
            "required_anchor": "DTC1289_1_Kmetric_partial",
            "purpose": "Kmetric decomposition into volume, chain, connection, domain, and boundary pieces.",
        },
        {
            "source_id": "SRC1371_7_798_gamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_2_local_locked_expansion",
            "purpose": "local stationary expansion and F_prime zero branch.",
        },
        {
            "source_id": "SRC1371_8_metric_contract",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "required_anchor": "MR514_5_double_zero",
            "purpose": "double-zero metric-response requirement.",
        },
        {
            "source_id": "SRC1371_9_1301_stress_split",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv",
            "required_anchor": "MSS1301_2_memory_potential_volume",
            "purpose": "memory potential/volume stress retained unless background and drift gates close.",
        },
        {
            "source_id": "SRC1371_10_1186_ward_operator",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv",
            "required_anchor": "RQB1186_2_operator_factorization",
            "purpose": "Ward-safe response-operator norm source.",
        },
        {
            "source_id": "SRC1371_11_1181_cassini",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "required_anchor": "SRC1181W_0_Cassini_gamma",
            "purpose": "Cassini gamma comparator.",
        },
        {
            "source_id": "SRC1371_12_1244_policy",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict gamma policy feed.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def parent_action_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "action_id": "PAI1371_0_fixed_L0_action_branch",
                "object": "S_GK^0[g,m;L0,m_*]",
                "formula": "S_GK^0=-int d^4x sqrt(-g) L0^-2 Fhat(m;m_*), with L0 fixed and Fhat(m;m_*)=F(m)-F(m_*).",
                "derived_result": "constant vacuum piece is subtracted/absorbed into the cosmological background; L0 is not varied.",
                "status": "PARENT_ACTION_CLOSURE_BRANCH_WRITTEN",
                "remaining_inputs": "parent adoption; sign convention; whether subtraction is global and not arena-fitted",
                "claim_effect": "inserts the fixed-L0 contract into an explicit action branch without claiming it is the live theory",
            },
            {
                "action_id": "PAI1371_1_volume_stress_gate",
                "object": "Kmetric_volume^{mu nu}",
                "formula": "delta sqrt(-g) Gamma_eff supplies a metric-proportional volume contribution proportional to Gamma_eff g^{mu nu}.",
                "derived_result": "fixed M_L alone does not remove this term; local silence needs Gamma_eff(m_*)=0 or an EH/cosmological-background subtraction.",
                "status": "VOLUME_BLOCKER_EXPOSED_AND_ROUTED",
                "remaining_inputs": "background subtraction convention; Fhat(m_*)=0; source-independent m_*",
                "claim_effect": "prevents a false local-GR pass from closing only chain kernels",
            },
            {
                "action_id": "PAI1371_2_strict_double_zero",
                "object": "Fhat local vacuum conditions",
                "formula": "Fhat(m_*)=0 and Fhat_prime(m_*)=F_prime(m_*)=0.",
                "derived_result": "at m=m_*, the volume term and first m-chain variation vanish; with fixed L0, the L-chain also vanishes.",
                "status": "STRICT_DOUBLE_ZERO_CONTRACT_WRITTEN",
                "remaining_inputs": "parent law selecting m_*; proof F_prime(m_*)=0; no per-system tuning of m_*",
                "claim_effect": "gives a serious route to local algebraic silence, still closure-only",
            },
            {
                "action_id": "PAI1371_3_first_variation_result",
                "object": "delta_g S_GK^0 at local vacuum",
                "formula": "delta_g[ sqrt(-g)L0^-2 Fhat(m)] = volume[0] + L0^-2 Fhat_prime(m_*) delta_g m + fixed-L0 term[0] + cdb terms.",
                "derived_result": "volume, m-chain, and L-chain vanish only under fixed L0, fixed/locked m=m_*, and double-zero conditions.",
                "status": "ALGEBRAIC_CHAIN_SILENCE_DERIVED_UNDER_CLOSURE",
                "remaining_inputs": "M_m fixed-field signature; K_conn/K_domain/K_boundary bounds; memory kinetic/source stress",
                "claim_effect": "narrows local residuals to cdb and memory/source channels",
            },
            {
                "action_id": "PAI1371_4_gradient_source_after_double_zero",
                "object": "nabla Gamma_eff",
                "formula": "nabla_mu Gamma_eff = L0^-2 Fhat_doubleprime(m_*) delta m nabla_mu delta m + O(delta m^2 nabla delta m).",
                "derived_result": "source vector is quadratic in the local displacement if L0 is fixed and m is locked near a stationary point.",
                "status": "QUADRATIC_SOURCE_SUPPRESSION_DERIVED_UNDER_CLOSURE",
                "remaining_inputs": "bound on delta m; bound on nabla delta m; transition/support/no-hair theorem",
                "claim_effect": "turns q_loc source safety into a norm-bound/no-hair problem",
            },
            {
                "action_id": "PAI1371_5_action_insertion_verdict",
                "object": "fixed-L0 double-zero branch",
                "formula": "fixed L0 + Fhat(m_*)=0 + Fhat_prime(m_*)=0 + fixed-field m closes the algebraic volume/m/L chain.",
                "derived_result": "this is the cleanest local branch found so far, but it is not claim-grade until parent adoption and residual bounds close.",
                "status": "CLOSURE_BRANCH_READY_NOT_LIVE_CLAIM",
                "remaining_inputs": "parent action signature; K_cdb; memory stress; q_loc norm or zero theorem",
                "claim_effect": "advance to residual theorem / norm-bound work",
            },
        ]
    )


def local_residual_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "residual_id": "LRZ1371_0_volume",
                "channel": "volume metric response",
                "closure_condition": "Fhat(m_*)=0 or source-independent cosmological/background subtraction",
                "status": "CLOSED_UNDER_STRICT_DOUBLE_ZERO_CLOSURE",
                "still_missing": "parent signature and global subtraction convention",
                "next_test": "prove m_* is universal/source-independent",
            },
            {
                "residual_id": "LRZ1371_1_m_chain",
                "channel": "m metric chain",
                "closure_condition": "Fhat_prime(m_*)=0 plus fixed-field m variation or finite M_m bound",
                "status": "CLOSED_UNDER_FIXED_FIELD_DOUBLE_ZERO_CLOSURE",
                "still_missing": "parent m fixed-field signature and local lock to m_*",
                "next_test": "prove local no-hair/locking theorem",
            },
            {
                "residual_id": "LRZ1371_2_L_chain",
                "channel": "L_cg metric chain",
                "closure_condition": "L_cg=L0 fixed constant scalar under Hilbert variation",
                "status": "CLOSED_UNDER_FIXED_L0_CLOSURE",
                "still_missing": "parent adoption and notation split from readout lengths",
                "next_test": "insert contract into full spine",
            },
            {
                "residual_id": "LRZ1371_3_gradient_source",
                "channel": "nabla Gamma_eff / q_loc source",
                "closure_condition": "delta m and nabla delta m vanish or are bounded strongly enough",
                "status": "REDUCED_TO_QUADRATIC_NORM_BOUND",
                "still_missing": "delta m amplitude law; boundary/transition support; no-hair theorem",
                "next_test": "derive q_loc norm bound from local relaxation equation",
            },
            {
                "residual_id": "LRZ1371_4_cdb_terms",
                "channel": "K_conn, K_domain, K_boundary",
                "closure_condition": "connection/domain/boundary no-flux or bounded commutator theorem",
                "status": "OPEN_RETAINED_RESIDUAL",
                "still_missing": "K_conn/K_domain/K_boundary bounds",
                "next_test": "derive fixed-L0 cdb residual theorem",
            },
            {
                "residual_id": "LRZ1371_5_memory_stress",
                "channel": "memory kinetic/potential/source/bath stress",
                "closure_condition": "local no-hair, constant m, source silence, and background subtraction",
                "status": "OPEN_RETAINED_RESIDUAL",
                "still_missing": "kinetic/source/bath stress zero or bound",
                "next_test": "separate stress channel from algebraic Gamma_eff chain",
            },
        ]
    )


def cqgamma_norm_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "input_id": "CQN1371_0_gauge",
                "quantity": "gauge/readout",
                "required_value": "standard weak-field PPN/isotropic scalar trace readout",
                "symbol": "P_scalar P_metric",
                "status": "DECLARED_SCHEMA_NOT_NUMERIC",
                "source_or_needed": "PPNP1182_0_metric_ansatz;PPNP1182_2_gamma_leakage",
            },
            {
                "input_id": "CQN1371_1_domain",
                "quantity": "exterior domain",
                "required_value": "compact-source exterior domain with asymptotically flat or Cassini-compatible boundary",
                "symbol": "D_ext",
                "status": "MISSING_DOMAIN_SPEC",
                "source_or_needed": "source radius, ray path, boundary conditions",
            },
            {
                "input_id": "CQN1371_2_potential_floor",
                "quantity": "PPN normalization potential",
                "required_value": "U_min or U_ref=GM/r along the comparator readout",
                "symbol": "U_min",
                "status": "MISSING_NUMERIC_SOURCE_CONVENTION",
                "source_or_needed": "GM convention and evaluation radius/path",
            },
            {
                "input_id": "CQN1371_3_green_norm",
                "quantity": "linearized metric Green norm",
                "required_value": "operator norm from conserved compensator stress to scalar spatial metric trace",
                "symbol": "N_G=||P_scalar P_metric G_EH||",
                "status": "MISSING_OPERATOR_NORM",
                "source_or_needed": "gauge/domain Green function",
            },
            {
                "input_id": "CQN1371_4_div_inverse_norm",
                "quantity": "divergence right-inverse norm",
                "required_value": "minimum-norm compensator or parent-owned C_q with boundary conditions",
                "symbol": "N_D=||Div^-1||",
                "status": "MISSING_OPERATOR_NORM",
                "source_or_needed": "Ward-safe compensator construction",
            },
            {
                "input_id": "CQN1371_5_qloc_norm",
                "quantity": "local residual norm",
                "required_value": "||q_loc|| or q_loc_hat Q0 profile generated by fixed-L0 double-zero branch",
                "symbol": "Q_norm",
                "status": "MISSING_QLOC_NORM",
                "source_or_needed": "delta m amplitude law and cdb residual bounds",
            },
            {
                "input_id": "CQN1371_6_bound_formula",
                "quantity": "Cassini gamma residual bound",
                "required_value": "|gamma-1| <= (c^2/(2U_min)) N_G N_D Q_norm",
                "symbol": "B_gamma",
                "status": "SOURCE_READY_SYMBOLIC_BOUND",
                "source_or_needed": "fill CQN1371_1 through CQN1371_5",
            },
            {
                "input_id": "CQN1371_7_pass_threshold",
                "quantity": "nonclaim pass threshold",
                "required_value": "Q_norm <= 2 U_min sigma_gamma/(c^2 N_G N_D) with sigma_gamma=2.3e-5",
                "symbol": "Q_allowed",
                "status": "SYMBOLIC_ACCEPTANCE_RULE_READY",
                "source_or_needed": "Cassini policy plus numeric norm inputs",
            },
        ]
    )


def runner_bound_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "runner_id": "QBR1371_0_symbolic_bound",
                "runner_update": "replace missing C_qgamma with source-ready norm-bound schema",
                "formula": "|gamma-1| <= C_norm Q_norm, C_norm=(c^2/(2U_min)) N_G N_D",
                "status": "SYMBOLIC_BOUND_READY_NUMERIC_INPUTS_MISSING",
                "blocks_claim_because": "U_min, N_G, N_D, and Q_norm are not numeric/source-backed",
            },
            {
                "runner_id": "QBR1371_1_fixed_L0_source_link",
                "runner_update": "link Q_norm source to fixed-L0 double-zero residual ledger",
                "formula": "Q_norm receives quadratic source plus cdb/memory residual contributions",
                "status": "SOURCE_LINK_WRITTEN_NOT_FILLED",
                "blocks_claim_because": "delta m amplitude law and cdb/memory bounds remain open",
            },
            {
                "runner_id": "QBR1371_2_claim_policy",
                "runner_update": "retain strict nonclaim Cassini policy",
                "formula": "accept only if all bound inputs are numeric/source-backed and B_gamma <= sigma_gamma",
                "status": "POLICY_READY_INPUTS_MISSING",
                "blocks_claim_because": "symbolic rows are not empirical evidence",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1371_0_parent_action_branch",
                "gate": "fixed-L0 double-zero parent action branch is written",
                "status": "PASS_CLOSURE_BRANCH",
                "reason": "S_GK^0 with Fhat=F-F(m_*) exposes and closes volume/m/L algebraic pieces under strict clauses.",
            },
            {
                "gate_id": "GATE1371_1_live_parent_signature",
                "gate": "branch is adopted as live parent MTS action",
                "status": "BLOCKED_NOT_LIVE_PARENT_SIGNED",
                "reason": "1371 writes a candidate closure branch; it does not rewrite the main corpus spine.",
            },
            {
                "gate_id": "GATE1371_2_volume_stress",
                "gate": "volume stress is not silently missed",
                "status": "PASS_EXPOSED_AND_CONDITIONALLY_CLOSED",
                "reason": "strict Fhat(m_*)=0/background subtraction is required before local-GR use.",
            },
            {
                "gate_id": "GATE1371_3_cdb_memory_residuals",
                "gate": "connection/domain/boundary and memory stress residuals are closed",
                "status": "BLOCKED_RETAINED_RESIDUALS",
                "reason": "K_cdb and memory/source stress remain open after algebraic chain closure.",
            },
            {
                "gate_id": "GATE1371_4_Cqgamma_norm_bound",
                "gate": "C_qgamma norm bound is source-ready",
                "status": "PASS_SYMBOLIC_INPUT_TABLE",
                "reason": "gauge/domain/U_min/N_G/N_D/Q_norm inputs are named with acceptance formula.",
            },
            {
                "gate_id": "GATE1371_5_numeric_PPN_score",
                "gate": "PPN/Cassini runner can score a number",
                "status": "BLOCKED_NUMERIC_INPUTS_MISSING",
                "reason": "no numeric operator norms or q_loc norm exist yet.",
            },
            {
                "gate_id": "GATE1371_6_local_GR_claim",
                "gate": "local GR/q_loc=0 can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "parent signature, residual bounds, and q_loc norm theorem remain missing.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1371_0_best_local_branch",
                "decision": "use fixed-L0 plus vacuum-subtracted double-zero as the best local closure branch",
                "why": "it closes the volume term that fixed M_L alone would miss",
                "next_action": "try to prove parent adoption and local lock to m_* without per-system tuning",
            },
            {
                "decision_id": "DEC1371_1_do_not_hide_volume",
                "decision": "never claim local algebraic silence from M_m/M_L alone",
                "why": "sqrt(-g) Gamma_eff gives a metric-proportional volume stress unless Fhat(m_*)=0 or background subtraction is explicit",
                "next_action": "carry volume gate in every future local-GR runner",
            },
            {
                "decision_id": "DEC1371_2_testing_lane",
                "decision": "advance C_qgamma from symbolic coefficient to symbolic norm-bound runner",
                "why": "this gives a clear shopping list for numeric PPN readiness",
                "next_action": "derive or source U_min, N_G, N_D, and Q_norm",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1371_0_1372",
                "next_doc": "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
                "next_script": "scripts/Y5_R10_RAB_fixed_L0_double_zero_local_residual_theorem_or_Qnorm_bound.py",
                "task": "attempt to prove the fixed-L0 double-zero local residual theorem by closing K_cdb and memory/source stress; if not, derive a Q_norm bound for q_loc from delta m amplitude, boundary, and transition support",
                "success_condition": "either local algebraic+cdb+memory residuals vanish under source-backed clauses, or Q_norm receives a symbolic/numeric bound usable by the C_qgamma norm runner",
                "do_not_claim": "local GR;PPN pass;q_loc=0;R10 pass;GitHub-ready result",
            }
        ]
    )


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            rows = read_csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    parent_action: list[dict[str, object]],
    local_residuals: list[dict[str, object]],
    norm_inputs: list[dict[str, object]],
    runner_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + parent_action + local_residuals + norm_inputs + runner_bounds + gates
    )
    action_branch = any(row["action_id"] == "PAI1371_0_fixed_L0_action_branch" and row["status"] == "PARENT_ACTION_CLOSURE_BRANCH_WRITTEN" for row in parent_action)
    volume_exposed = any(row["action_id"] == "PAI1371_1_volume_stress_gate" and row["status"] == "VOLUME_BLOCKER_EXPOSED_AND_ROUTED" for row in parent_action)
    double_zero = any(row["action_id"] == "PAI1371_2_strict_double_zero" and row["status"] == "STRICT_DOUBLE_ZERO_CONTRACT_WRITTEN" for row in parent_action)
    cdb_retained = any(row["residual_id"] == "LRZ1371_4_cdb_terms" and row["status"] == "OPEN_RETAINED_RESIDUAL" for row in local_residuals)
    norm_ready = any(row["input_id"] == "CQN1371_7_pass_threshold" and row["status"] == "SYMBOLIC_ACCEPTANCE_RULE_READY" for row in norm_inputs)
    runner_blocked = any(row["runner_id"] == "QBR1371_0_symbolic_bound" and row["status"] == "SYMBOLIC_BOUND_READY_NUMERIC_INPUTS_MISSING" for row in runner_bounds)
    local_claim_blocked = any(row["gate_id"] == "GATE1371_6_local_GR_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1371_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1371_1_action_branch",
            "check": "fixed-L0 parent action branch and strict double-zero contract are written",
            "status": "PASS" if action_branch and volume_exposed and double_zero else "FAIL",
            "details": "branch exposes volume stress and requires Fhat(m_*)=Fhat_prime(m_*)=0",
        },
        {
            "validation_id": "VAL1371_2_residuals_retained",
            "check": "cdb/memory residuals remain retained instead of hidden",
            "status": "PASS" if cdb_retained else "FAIL",
            "details": "LRZ1371_4 keeps K_conn/K_domain/K_boundary open",
        },
        {
            "validation_id": "VAL1371_3_norm_bound_schema",
            "check": "C_qgamma norm-bound inputs and acceptance threshold are source-ready",
            "status": "PASS" if norm_ready and runner_blocked else "FAIL",
            "details": "CQN1371_7 defines symbolic Q_allowed; numeric inputs remain missing",
        },
        {
            "validation_id": "VAL1371_4_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1371 is a closure/norm-bound checkpoint, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1371_5_local_claim_blocked",
            "check": "local GR claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1371_6_local_GR_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1371_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1371_7_overall",
            "check": "overall 1371 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1371 writes the fixed-L0 double-zero action branch, exposes volume stress, retains cdb/memory blockers, and builds a C_qgamma norm-bound table.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    parent_action: list[dict[str, object]],
    local_residuals: list[dict[str, object]],
    norm_inputs: list[dict[str, object]],
    runner_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1371 finds and fixes an important would-be loophole. Fixed `L_cg=L0` closes the `M_L` chain, but it does not by itself remove the metric-proportional volume stress from `sqrt(-g) Gamma_eff`. The clean branch is therefore fixed `L0` plus a vacuum-subtracted double-zero action: `Fhat(m;m_*)=F(m)-F(m_*)`, with `Fhat(m_*)=0` and `Fhat_prime(m_*)=0`.

**Main progress:** the local branch is now much sharper. Under fixed `L0`, fixed/locked `m=m_*`, and strict double-zero, the algebraic volume, `m` chain, and `L_cg` chain can vanish together. What remains is no longer a vague cloud: it is `K_conn/K_domain/K_boundary`, memory kinetic/source/bath stress, and the norm of the quadratic `q_loc` source.

**Testing progress:** the `C_qgamma` lane now has a source-ready norm-bound table: `|gamma-1| <= (c^2/(2U_min)) N_G N_D Q_norm`, with the Cassini acceptance rule `Q_norm <= 2 U_min sigma_gamma/(c^2 N_G N_D)`. It is still nonclaim because `U_min`, `N_G`, `N_D`, and `Q_norm` are not filled.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Fixed-`L0` Parent Action Insertion

{table(["action_id", "object", "status", "formula", "derived_result", "remaining_inputs", "claim_effect", "valid_for_claim", "claim_allowed"], parent_action)}

## Local Residual Zero/Bound Ledger

{table(["residual_id", "channel", "status", "closure_condition", "still_missing", "next_test", "valid_for_claim", "claim_allowed"], local_residuals)}

## `C_qgamma` Norm-Bound Input Table

{table(["input_id", "quantity", "required_value", "symbol", "status", "source_or_needed", "valid_for_claim", "claim_allowed"], norm_inputs)}

## `q_loc -> gamma` Bound Runner Update

{table(["runner_id", "runner_update", "formula", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_bounds)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    parent_action = parent_action_rows()
    local_residuals = local_residual_rows()
    norm_inputs = cqgamma_norm_rows()
    runner_bounds = runner_bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PARENT_ACTION_PATH, parent_action)
    write_csv(LOCAL_RESIDUAL_PATH, local_residuals)
    write_csv(CQGAMMA_NORM_PATH, norm_inputs)
    write_csv(RUNNER_BOUND_PATH, runner_bounds)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        PARENT_ACTION_PATH,
        LOCAL_RESIDUAL_PATH,
        CQGAMMA_NORM_PATH,
        RUNNER_BOUND_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, parent_action, local_residuals, norm_inputs, runner_bounds, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, parent_action, local_residuals, norm_inputs, runner_bounds, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
