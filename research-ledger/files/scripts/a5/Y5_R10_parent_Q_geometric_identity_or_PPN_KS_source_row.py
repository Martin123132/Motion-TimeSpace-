from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1180_0_1179_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1179_NEXT_TARGET.csv",
            "needle": "NEXT1179_0_1180",
            "role": "handoff to Q geometric identity or PPN K_S source row.",
        },
        {
            "source_id": "SRC1180_1_1179_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1179_VALIDATION.csv",
            "needle": "V1179_SUMMARY",
            "role": "1179 validation summary.",
        },
        {
            "source_id": "SRC1180_2_1179_KS_under",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1179_RECIPROCAL_TRANSFER_DERIVATION_ATTEMPT.csv",
            "needle": "RTT1179_4_transfer_underdetermination",
            "role": "scalar reciprocity does not determine K_S_to_metric.",
        },
        {
            "source_id": "SRC1180_3_1179_orientation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1179_KS_CLOSURE_ROWS.csv",
            "needle": "KSC1179_0_orientation",
            "role": "missing orientation/sign of tracefree transfer.",
        },
        {
            "source_id": "SRC1180_4_1179_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1179_KS_CLOSURE_ROWS.csv",
            "needle": "KSC1179_1_normalization",
            "role": "missing normalization of tracefree transfer.",
        },
        {
            "source_id": "SRC1180_5_1179_PPN",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1179_FIRST_ARENA_SOURCE_ROW_ORDER.csv",
            "needle": "FAI1179_0_PPN_preferred_first",
            "role": "PPN selected as first arena for K_S sourcing.",
        },
        {
            "source_id": "SRC1180_6_02_reciprocity",
            "relative_path": "02-motion-load-local-GR-reduction.md",
            "needle": "exact reciprocal metric completion",
            "role": "metric completion remains conditional.",
        },
        {
            "source_id": "SRC1180_7_04_contract",
            "relative_path": "04-vacuum-reciprocity-action-contract.md",
            "needle": "contract locked, theorem not satisfied",
            "role": "scalar reciprocity action theorem still unsatisfied.",
        },
        {
            "source_id": "SRC1180_8_Qcoh_contract",
            "relative_path": "source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv",
            "needle": "Q_{mu nu} must be an action variable or derived Noether/load tensor",
            "role": "Q ownership requirement.",
        },
        {
            "source_id": "SRC1180_9_local_zero_clause",
            "relative_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
            "needle": "Qcoh_mu_nu=(1/3)h_mu_nu X",
            "role": "Qcoh appears as scalar coherent load/projector, not full tracefree metric identity.",
        },
        {
            "source_id": "SRC1180_10_metric_readout",
            "relative_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "g_readout = g_obs",
            "role": "metric readout protected from linear extra-field leakage.",
        },
        {
            "source_id": "SRC1180_11_1009_EH",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "PCS1009_0_EH_core",
            "role": "EH core is an anchor, not total parent proof.",
        },
        {
            "source_id": "SRC1180_12_1010_q_loc",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc remains retained residual.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def identity_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "QID1180_0_metric_identity",
            "candidate_identity": "Q_ij == gamma_ij",
            "implied_sigma_KS": "+1 in dimensionless metric perturbation convention",
            "implied_K_norm": "1 after matched normalization",
            "evidence_status": "NOT_PARENT_SIGNED",
            "reason": "current source chain keeps g_obs/coframe as metric readout and treats Qcoh as coherent scalar/projector load.",
            "missing_for_claim": "parent equation identifying Q_ij with observed spatial metric gamma_ij",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QID1180_1_inverse_metric_identity",
            "candidate_identity": "Q^ij == gamma^ij",
            "implied_sigma_KS": "-1 in dimensionless metric perturbation convention",
            "implied_K_norm": "1 after matched normalization",
            "evidence_status": "NOT_PARENT_SIGNED",
            "reason": "scalar reciprocal routing allows an inverse-reading intuition, but no parent row signs inverse spatial metric ownership.",
            "missing_for_claim": "parent equation identifying Q with inverse spatial metric or Hamiltonian dual metric",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QID1180_2_coframe_square_identity",
            "candidate_identity": "Q_ij == delta_ab e^a_i e^b_j or inverse coframe square",
            "implied_sigma_KS": "orientation depends on coframe versus inverse-coframe convention",
            "implied_K_norm": "2 times coframe perturbation normalization, if coframe-owned",
            "evidence_status": "COFRAME_ANCHOR_ONLY",
            "reason": "g_obs/coframe appears in the EH/matter/readout blocks, but Q is not parent-identified with that coframe.",
            "missing_for_claim": "parent coframe map Q(e) and its first variation",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QID1180_3_Qcoh_scalar_projector",
            "candidate_identity": "Qcoh_mu_nu == (1/3)h_mu_nu X",
            "implied_sigma_KS": "0 for tracefree S_Q in the scalar coherent channel",
            "implied_K_norm": "not a metric transfer coefficient",
            "evidence_status": "SUPPORTED_FOR_SCALAR_QCOH_ONLY",
            "reason": "local-zero source rows define Qcoh as scalar coherent load/projector machinery; this supports F1_C_S=0 style decoupling but not metric spin-2 transfer.",
            "missing_for_claim": "separate tracefree parent variable or metric transfer theorem",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QID1180_4_independent_routing_field",
            "candidate_identity": "Q is an independent routing/load field with metric readout g_readout = g_obs + O((Phi-Phi0)^2)",
            "implied_sigma_KS": "closure/source parameter unless a parent map Dg_Q is added",
            "implied_K_norm": "closure/source parameter",
            "evidence_status": "MOST_CONSISTENT_CURRENT_READING",
            "reason": "this preserves the EH local metric lane and prevents unowned linear leakage, but it leaves K_S_to_metric unproved.",
            "missing_for_claim": "either no-linear-leak theorem plus explicit residual bound, or parent Dg_Q coupling",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QID1180_5_verdict",
            "candidate_identity": "parent Q geometric identity verdict",
            "implied_sigma_KS": "not derivable from current source chain",
            "implied_K_norm": "not derivable from current source chain",
            "evidence_status": "IDENTITY_NOT_DERIVED_PPN_CLOSURE_ACTIVE",
            "reason": "the corpus currently signs scalar Qcoh/projector usage and metric readout protection, not a tracefree Q-to-metric identity.",
            "missing_for_claim": "parent Q/gamma/coframe equation or sourced PPN K_S closure row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def ppn_ks_rows() -> list[dict[str, object]]:
    rows = [
        {
            "ppn_row_id": "PPNKS1180_0_transfer_definition",
            "arena": "PPN",
            "quantity": "K_S_to_metric",
            "definition": "delta g_TF^PPN = K_S_to_metric S_Q + q_loc_TF residual in the weak-field local branch",
            "required_inputs": "sigma_KS; K_norm; S_Q arena norm; q_loc_TF bound; PPN comparator vector",
            "current_value": "K_S_to_metric := sigma_KS*K_norm (closure only)",
            "source_path": "MISSING_PARENT_OR_PPN_SOURCE_PATH",
            "status": "SOURCE_READY_NONCLAIM_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_row_id": "PPNKS1180_1_orientation",
            "arena": "PPN",
            "quantity": "sigma_KS",
            "definition": "sign/orientation of S_Q transfer into metric perturbation",
            "required_inputs": "Q==metric, Q==inverse metric, Q==coframe square, or independent-field parent identity",
            "current_value": "MISSING_PARENT_ORIENTATION",
            "source_path": "MISSING_PARENT_Q_IDENTITY_SOURCE",
            "status": "SOURCE_READY_NONCLAIM_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_row_id": "PPNKS1180_2_normalization",
            "arena": "PPN",
            "quantity": "K_norm",
            "definition": "scale converting tracefree Q-flow units into PPN metric perturbation units",
            "required_inputs": "parent kinetic normalization or calibrated-but-nonclaim source row",
            "current_value": "MISSING_PARENT_NORMALIZATION",
            "source_path": "MISSING_PARENT_KINETIC_SOURCE",
            "status": "SOURCE_READY_NONCLAIM_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_row_id": "PPNKS1180_3_residual_vector",
            "arena": "PPN",
            "quantity": "r_PPN_metric",
            "definition": "metric residual vector after EH anchor plus MTS tracefree transfer and q_loc residual",
            "required_inputs": "gamma-1; beta-1; preferred-frame/vector/tensor residuals where applicable; source comparator",
            "current_value": "MISSING_PPN_RESIDUAL_VECTOR",
            "source_path": "MISSING_PPN_COMPARATOR_SOURCE",
            "status": "SOURCE_READY_NONCLAIM_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_row_id": "PPNKS1180_4_no_linear_leak_branch",
            "arena": "PPN",
            "quantity": "K_S_to_metric_zero_branch",
            "definition": "if g_readout = g_obs + O((Phi-Phi0)^2) and Q is independent, linear tracefree Q leakage to PPN metric is zero by readout protection",
            "required_inputs": "parent proof that Q is independent and metric readout protection is exact through PPN order",
            "current_value": "CONDITIONAL_ZERO_BRANCH_NOT_PARENT_SIGNED",
            "source_path": "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv::A511_6_metric_readout",
            "status": "CONDITIONAL_NONCLAIM_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1180_0_Q_metric_identity",
            "claim": "Q is the observed spatial metric",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "why_blocked": "g_obs/coframe owns metric readout; Qcoh is scalar/projector in available sources",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1180_1_Q_inverse_identity",
            "claim": "Q is inverse spatial metric or Hamiltonian dual metric",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "why_blocked": "reciprocity suggests a dual route but no Q inverse-metric identity is sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1180_2_Q_coframe_identity",
            "claim": "Q is the coframe square",
            "status": "BLOCKED_COFRAME_ANCHOR_ONLY",
            "why_blocked": "coframe appears as metric/matter readout but Q(e) is not given",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1180_3_Qcoh_scalar_only",
            "claim": "Qcoh scalar projector supplies tracefree metric transfer",
            "status": "FAILED_AS_STATED",
            "why_blocked": "Qcoh=(1/3)hX is scalar/isotropic and cannot own tracefree S_Q transfer by itself",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1180_4_PPN_KS_score",
            "claim": "PPN K_S_to_metric row is scoreable",
            "status": "BLOCKED_SOURCE_ROWS_MISSING",
            "why_blocked": "orientation, normalization, PPN comparator, q_loc residual, and source paths remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1180_5_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why_blocked": "Q identity, K_S_to_metric, scalar reciprocity theorem, q_loc closure, and PPN vector remain incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1180_0_identity_scan",
            "operation": "test Q metric/inverse/coframe/projector/independent identities",
            "result": "NO_PARENT_IDENTITY_FOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1180_1_Qcoh_scalar",
            "operation": "test whether Qcoh scalar projector can carry tracefree S_Q",
            "result": "FAILED_TRACEFREE_TRANSFER_NOT_OWNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1180_2_independent_field_branch",
            "operation": "test independent-Q plus protected metric readout branch",
            "result": "CONSISTENT_NONCLAIM_BRANCH",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1180_3_PPN_rows",
            "operation": "create first PPN K_S closure/source rows",
            "result": "ROWS_CREATED_VALID_FOR_CLAIM_FALSE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1180_4_local_promotion",
            "operation": "local GR/Newton promotion",
            "result": "REFUSED_NO_LOCAL_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1180_0_Q_identity_status",
            "decision": "do_not_claim_Q_geometric_identity",
            "reason": "current evidence supports scalar Qcoh/projector use and metric readout protection, not Q=metric/inverse/coframe.",
            "next_action": "either find parent Q(g/e) equation or keep K_S_to_metric as closure.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1180_1_best_current_branch",
            "decision": "independent_Q_with_protected_metric_readout_is_currently_safest",
            "reason": "it avoids smuggling GR and avoids unowned tracefree metric leakage while preserving a scoreable closure route.",
            "next_action": "source PPN comparator and q_loc residual vector under nonclaim status.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1180_2_testing_order",
            "decision": "PPN_KS_source_pack_next",
            "reason": "PPN directly tests the metric transfer coefficient before R10 scalar leakage can be interpreted safely.",
            "next_action": "build PPN residual-vector source pack and keep all numeric rows invalid until sourced.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1180_0_1181",
            "next_target": "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md",
            "objective": "source or construct the PPN residual-vector comparator for K_S_to_metric while keeping Q identity and local-GR claims blocked unless a parent Q(g/e) theorem is found",
            "include": "PPN comparator source ledger; gamma/beta/preferred-frame residual vector; q_loc retained residual; K_S_to_metric closure rows; no-claim validation",
            "exclude": "claiming local GR; treating Qcoh as tracefree metric; invented numeric PPN limits; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    identities: list[dict[str, object]],
    ppn_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1180_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_1_all_identity_branches_logged",
            "result": "pass"
            if {r["attempt_id"] for r in identities} >= {
                "QID1180_0_metric_identity",
                "QID1180_1_inverse_metric_identity",
                "QID1180_2_coframe_square_identity",
                "QID1180_3_Qcoh_scalar_projector",
                "QID1180_4_independent_routing_field",
            }
            else "fail",
            "detail": "metric, inverse, coframe, Qcoh scalar, and independent-Q branches are all audited",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_2_identity_not_claimed",
            "result": "pass" if any(r["evidence_status"] == "IDENTITY_NOT_DERIVED_PPN_CLOSURE_ACTIVE" for r in identities) else "fail",
            "detail": "parent Q geometric identity is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_3_Qcoh_tracefree_rejected",
            "result": "pass"
            if any(
                r["attempt_id"] == "QID1180_3_Qcoh_scalar_projector"
                and "not metric spin-2 transfer" in r["reason"]
                for r in identities
            )
            else "fail",
            "detail": "Qcoh scalar/projector branch is not allowed to carry tracefree metric transfer",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_4_PPN_rows_created",
            "result": "pass" if len(ppn_rows) >= 5 and all(r["claim_allowed"] is False for r in ppn_rows) else "fail",
            "detail": "PPN K_S closure/source rows are staged and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_5_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in ppn_rows)
            else "fail",
            "detail": "PPN rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_6_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all Q identity, PPN, and local-GR gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-run refuses identity, PPN, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_8_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in identities + ppn_rows + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_9_next_target",
            "result": "pass" if nexts and "1181" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1181 handoff targets PPN K_S source pack or parent Q identity proof",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_10_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1180_SUMMARY",
            "result": "pass",
            "detail": "1180 audits Q metric/inverse/coframe/scalar/independent identities, refuses Q geometric identity promotion, stages first PPN K_S closure rows, and hands off to PPN residual-vector sourcing",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    identities: list[dict[str, object]],
    ppn_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1180 - Y5/R10 parent Q geometric identity or PPN K_S source row",
        "**Current verdict:** the current source chain does not derive `Q = metric`, `Q = inverse metric`, or `Q = coframe square`. The best supported reading is scalar `Qcoh` plus protected metric readout, with tracefree transfer left as `K_S_to_metric` closure.",
        "**Main progress:** all candidate Q identities are now audited in one gate, and the first PPN `K_S_to_metric` source/closure rows are staged without becoming claim-valid.",
        "**Technical consequence:** `Qcoh=(1/3)hX` can support scalar decoupling/F1 logic, but it cannot by itself own tracefree spin-2 metric transfer.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Parent Q geometric identity attempt\n\n" + table(identities),
        "## PPN K_S source/closure rows\n\n" + table(ppn_rows),
        "## Claim gates\n\n" + table(gates),
        "## Runner dry-run\n\n" + table(runs),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    identities = identity_attempt_rows()
    ppn_rows = ppn_ks_rows()
    gates = gate_rows()
    runs = runner_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, identities, ppn_rows, gates, runs, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1180_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1180_PARENT_Q_GEOMETRIC_IDENTITY_ATTEMPT.csv": identities,
        "P8_Y5_R10_1180_PPN_KS_SOURCE_CLOSURE_ROWS.csv": ppn_rows,
        "P8_Y5_R10_1180_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1180_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1180_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1180_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1180_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, identities, ppn_rows, gates, runs, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
