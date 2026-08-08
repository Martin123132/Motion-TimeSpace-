from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1396-Y5-R10-RAB-beta-EM-lock-repair-or-finite-alphaEM-source-bound.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1396_SOURCE_REGISTER.csv"
EM_LOCK_REPAIR_PATH = SRC_DIR / "P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv"
BETA_EM_BOUND_PATH = SRC_DIR / "P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv"
INTERFACE_PATH = SRC_DIR / "P8_Y5_R10_1396_BETA_EM_INTERFACE_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1396_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1396_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1396_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1396_VALIDATION.csv"

STATUS = (
    "beta_EM_lock_repair_attempt_failed_current_corpus_"
    "finite_alphaEM_source_bound_template_nonclaim_written"
)
CLAIM_CEILING = (
    "EM_lock_repair_and_finite_beta_EM_template_only_no_beta_EM_zero_no_alphaEM_bound_claim_"
    "no_WEP_no_clock_no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1396_0_1395_doc",
        "source_path": "1395-Y5-R10-RAB-sector-beta-zero-theorem-or-binding-sector-source-pack.md",
        "required_anchor": "NEXT1395_0_1396",
        "purpose": "handoff to beta_EM lock repair or finite alpha_EM source bound",
    },
    {
        "source_id": "SRC1396_1_1395_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_NEXT_TARGET.csv",
        "required_anchor": "NEXT1395_0_1396",
        "purpose": "machine-readable 1396 target",
    },
    {
        "source_id": "SRC1396_2_1395_zero",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_SECTOR_BETA_ZERO_THEOREM_ATTEMPT.csv",
        "required_anchor": "SBZ1395_2_EM_zero",
        "purpose": "beta_EM zero has active EM-lock blockers",
    },
    {
        "source_id": "SRC1396_3_1395_pack",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
        "required_anchor": "SBP1395_2_beta_EM",
        "purpose": "beta_EM source row to refine",
    },
    {
        "source_id": "SRC1396_4_987_doc",
        "source_path": "987-Y5-R10-Coulomb-to-alphaEM-normal-form-or-parent-zero-gate.md",
        "required_anchor": "EMNF987_4_verdict",
        "purpose": "Coulomb-to-alphaEM normal form remains finite but unsigned",
    },
    {
        "source_id": "SRC1396_5_988_doc",
        "source_path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
        "required_anchor": "EMLOCK988_5_theorem_verdict",
        "purpose": "EM-lock theorem remains conditional and not promoted",
    },
    {
        "source_id": "SRC1396_6_989_doc",
        "source_path": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
        "required_anchor": "ELA989_5_total",
        "purpose": "EM-lock signature audit fails current corpus",
    },
    {
        "source_id": "SRC1396_7_989_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
        "required_anchor": "ELA989_1_unique_F2",
        "purpose": "unique Maxwell F2 blocker remains active",
    },
    {
        "source_id": "SRC1396_8_989_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
        "required_anchor": "BSO989_4_failure_action",
        "purpose": "finite alpha/source beta branch remains closure-only",
    },
    {
        "source_id": "SRC1396_9_988_joint_alpha",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "required_anchor": "JAV988_1_clock_product",
        "purpose": "clock alpha product bound is nonclaim and not a WEP pass",
    },
    {
        "source_id": "SRC1396_10_988_WEP",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
        "required_anchor": "WEP988_WAS651_0_alpha_Coulomb",
        "purpose": "finite alpha WEP source-normalization pressure imports",
    },
    {
        "source_id": "SRC1396_11_1394_binding",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BINDING_BETA_COEFFICIENT_ROWS.csv",
        "required_anchor": "BBR1394_2_beta_EM",
        "purpose": "beta_EM feeds binding beta rows",
    },
    {
        "source_id": "SRC1396_12_this_script",
        "source_path": "scripts/Y5_R10_RAB_beta_EM_lock_repair_or_finite_alphaEM_source_bound.py",
        "required_anchor": "STATUS",
        "purpose": "1396 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def em_lock_repair_rows() -> list[dict[str, str]]:
    return [
        {
            "repair_id": "ELR1396_0_charge_generator",
            "clause": "parent charge generator owner",
            "repair_attempt": "require T_Q to be a compact vertical generator in the varied parent action with fixed lattice/norm data",
            "current_result": "UNSIGNED",
            "remaining_blocker": "T_Q is not supplied as a parent-action object with fixed normalization",
            "if_closed": "charge units and A_Q normalization cannot be rescaled independently",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_1_unique_Maxwell_F2",
            "clause": "unique Maxwell kinetic subblock",
            "repair_attempt": "forbid every standalone lambda_A F_Q^2 counterterm by parent curvature-norm uniqueness",
            "current_result": "FAILS_CURRENT_CORPUS",
            "remaining_blocker": "prior audit retains lambda_A F_Q^2 as a legal counterexample",
            "if_closed": "alpha_EM normalization becomes parent-owned instead of branch-owned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_2_current_owner",
            "clause": "charge-current/source normalization owner",
            "repair_attempt": "make matter current, charge labels, and Maxwell source normalization descend from the same T_Q Noether owner",
            "current_result": "UNSIGNED",
            "remaining_blocker": "current rescaling and beta_source_alpha remain unowned",
            "if_closed": "WEP/R10 source-test EM strength stops floating independently",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_3_readout_descent",
            "clause": "dimensionless alpha_EM readout descent",
            "repair_attempt": "fix Hodge star, coframe, and hbar*c readout so Lie_v ln alpha_EM=0",
            "current_result": "UNSIGNED",
            "remaining_blocker": "coframe/Hodge/readout leakage remains possible",
            "if_closed": "clock/spectroscopy alpha drift cannot re-enter through units",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_4_no_alpha_vertex",
            "clause": "matter functor no-alpha/no-mass vertex",
            "repair_attempt": "forbid alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), and binding-response vertices in ordinary matter functor",
            "current_result": "UNSIGNED",
            "remaining_blocker": "composition-dependent Coulomb/mass/binding channels remain physical fallback rows",
            "if_closed": "Damour-Donoghue-style composition charges are theorem-zero locally",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_5_conditional_theorem",
            "clause": "EM-lock beta_EM zero theorem",
            "repair_attempt": "if ELR1396_0 through ELR1396_4 all close, beta_EM=0, b_alpha_EM=0, and EM binding contribution can be zero-certified",
            "current_result": "EXACT_CONDITIONAL_THEOREM_READY",
            "remaining_blocker": "unique F2 fails current corpus and other signatures are unsigned",
            "if_closed": "beta_EM row can be demoted to theorem-zero certificate",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "repair_id": "ELR1396_6_current_verdict",
            "clause": "EM-lock repair status",
            "repair_attempt": "compare 987/988/989 EM-lock audits with 1395 beta_EM source row",
            "current_result": "EM_LOCK_NOT_REPAIRED_FINITE_TEMPLATE_REQUIRED",
            "remaining_blocker": "no parent-signed T_Q/F2/current/readout/no-alpha package",
            "if_closed": "return to beta_EM theorem-zero branch",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def beta_em_bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BEM1396_0_beta_EM",
            "quantity": "beta_EM",
            "role": "EM binding/charge/fine-structure sector beta feeding beta_bind,A",
            "formula_or_target": "beta_EM := partial_phi_c ln M_EM^obs contribution; also related to finite alpha_EM branch only after a parent map",
            "source_bound_or_target": "MISSING",
            "provenance": "requires EM-lock theorem or sourced WEP/clock/R10/alpha_EM bound map",
            "current_status": "MISSING_BETA_EM_ZERO_OR_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_1_b_alpha_EM",
            "quantity": "b_alpha_EM",
            "role": "dimensionless alpha_EM drift/coupling slot",
            "formula_or_target": "b_alpha := d ln alpha_EM / d Xhat or canonical phi_c equivalent after normalization map",
            "source_bound_or_target": "clock product bound exists only for b_alpha*tau_clock, not standalone b_alpha",
            "provenance": "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv::JAV988_1_clock_product",
            "current_status": "PRODUCT_BOUND_NONCLAIM_STANDALONE_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_2_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "role": "WEP/source-force normalization multiplying finite alpha_EM channel",
            "formula_or_target": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "source_bound_or_target": "alpha-only target <= 4.797780522732e-05; robust target <= 2.887280314062e-05",
            "provenance": "P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv::BSO989_1/BSO989_2 and P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "current_status": "NUMERIC_TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_3_clock_WEP_split",
            "quantity": "tau_clock vs tau_WEP/source",
            "role": "prevents clock-screening from being used as a WEP or R10 pass",
            "formula_or_target": "clock constrains b_alpha*tau_clock; WEP constrains beta_source_alpha*b_alpha*tau_WEP",
            "source_bound_or_target": "separate parent map missing",
            "provenance": "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv::JAV988_3_cross_arena_policy",
            "current_status": "CROSS_ARENA_MAP_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_4_R10_material_leg",
            "quantity": "beta_EM contribution to R10 material leg",
            "role": "feeds beta_bind,S/T through f_EM,S/T beta_EM and then beta_bulk,S/T",
            "formula_or_target": "alpha_bulk,ST(lambda) includes K(lambda)(...+f_EM,S beta_EM)(...+f_EM,T beta_EM)+tail",
            "source_bound_or_target": "requires f_EM,S/T, beta_EM, K(lambda), tail, and full R10 bound curve",
            "provenance": "1394 composition map and 1392 bulk alpha template",
            "current_status": "R10_MATERIAL_INPUTS_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_5_local_residual",
            "quantity": "R_EM_local",
            "role": "finite beta_EM residual vector for local GR/Newton/WEP/clock/R10 gates",
            "formula_or_target": "collect alpha_EM drift, Coulomb WEP, clock, binding, and R10 material effects",
            "source_bound_or_target": "complete residual vector missing",
            "provenance": "requires BEM1396_0 through BEM1396_4 to be source-backed",
            "current_status": "LOCAL_RESIDUAL_VECTOR_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "BEM1396_6_template_verdict",
            "quantity": "finite beta_EM source-bound template",
            "role": "nonclaim fallback if EM-lock remains unsigned",
            "formula_or_target": "all EM finite slots must be zero-certified or source-backed before scoring",
            "source_bound_or_target": "BEM1396_0 through BEM1396_5 complete without MISSING markers",
            "provenance": "1396 checkpoint",
            "current_status": "BETA_EM_SOURCE_BOUND_TEMPLATE_READY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "EMG1396_0_alphaEM",
            "arena": "alpha_EM/fine-structure",
            "dependency": "b_alpha_EM and readout descent",
            "blocked_by": "EM-lock readout descent and no-alpha vertex unsigned",
            "current_status": "BLOCKED_ALPHAEM_LOCK_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "EMG1396_1_WEP",
            "arena": "WEP/Coulomb composition",
            "dependency": "beta_source_alpha*b_alpha*tau_WEP and beta_EM binding composition",
            "blocked_by": "source normalization owner missing; unit-source overshoots require suppression target only",
            "current_status": "BLOCKED_WEP_SOURCE_NORMALIZATION_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "EMG1396_2_clock",
            "arena": "clocks",
            "dependency": "b_alpha*tau_clock product",
            "blocked_by": "standalone b_alpha and tau_clock dynamics are not parent-derived",
            "current_status": "BLOCKED_CLOCK_PRODUCT_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "EMG1396_3_R10",
            "arena": "R10 material leg",
            "dependency": "f_EM,S/T beta_EM contribution to beta_bulk,S/T",
            "blocked_by": "beta_EM, composition fractions, K/tail, and full bound curve missing",
            "current_status": "BLOCKED_R10_MATERIAL_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "EMG1396_4_local_GR",
            "arena": "local GR/Newton reduction",
            "dependency": "universal matter source and no finite EM sector residual",
            "blocked_by": "EM-lock not signed and finite beta_EM residual vector missing",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def interface_rows() -> list[dict[str, str]]:
    return [
        {
            "interface_id": "BEI1396_0_to_sector_pack",
            "target": "SBP1395_2_beta_EM",
            "dependency": "EM-lock repair or finite beta_EM template",
            "effect": "beta_EM remains missing/nonclaim until EM-lock signs or finite bound map is real",
            "current_status": "SECTOR_BETA_EM_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BEI1396_1_to_binding",
            "target": "BBR1394 beta_bind,S/T",
            "dependency": "f_EM,S/T beta_EM",
            "effect": "EM binding part of beta_bind cannot be filled",
            "current_status": "BINDING_EM_COMPONENT_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BEI1396_2_to_beta_bulk",
            "target": "BBS1393 beta_bulk,S/T",
            "dependency": "beta_bind,S/T including beta_EM",
            "effect": "bulk beta legs remain blocked",
            "current_status": "BULK_BETA_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BEI1396_3_to_R10_template",
            "target": "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
            "dependency": "beta_bulk,S/T and EM material contribution",
            "effect": "R10 alpha remains symbolic/nonclaim",
            "current_status": "R10_TEMPLATE_PROMOTION_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "interface_id": "BEI1396_4_verdict",
            "target": "beta_EM to all local gates",
            "dependency": "EM-lock or finite beta_EM source-bound pack",
            "effect": "all alphaEM/WEP/clock/R10/local gates remain blocked",
            "current_status": "BETA_EM_INTERFACE_READY_SCORING_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1396_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against 987/988/989 and current beta-sector corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1396_1_EM_lock",
            "gate": "EM-lock closes beta_EM=0",
            "status": "BLOCKED_CURRENT_CORPUS_FAILS_UNIQUE_F2",
            "reason": "unique Maxwell F2 fails current corpus and other EM-lock clauses are unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1396_2_finite_template",
            "gate": "finite beta_EM source-bound template exists",
            "status": "PASS_NONCLAIM_TEMPLATE",
            "reason": "beta_EM, b_alpha, beta_source_alpha, clock/WEP split, R10 material leg, and residual vector are explicit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1396_3_empirical_scores",
            "gate": "alphaEM/WEP/clock/R10 scores may be reported",
            "status": "BLOCKED_VALUES_AND_PARENT_MAPS_MISSING",
            "reason": "finite rows are targets/templates only; no standalone beta_EM or cross-arena map exists",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1396_4_R10_score",
            "gate": "R10 alpha(lambda) score may be reported",
            "status": "BLOCKED_R10_MATERIAL_INPUTS_MISSING",
            "reason": "beta_EM contribution cannot fill beta_bulk or runner alpha rows",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1396_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1396 is an EM-lock repair/source-bound checkpoint, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1396_0_EM_lock_status",
            "decision": "do not claim beta_EM=0",
            "because": "unique Maxwell F2 remains an active counterexample and EM-lock package is unsigned",
            "next_action": "either attack unique F2 directly or use finite beta_EM template",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1396_1_template_status",
            "decision": "finite beta_EM route is now explicit but nonclaim",
            "because": "clock product and WEP suppression targets exist only as pressure/targets, not standalone beta_EM bounds",
            "next_action": "build a unique-Maxwell-F2 repair attempt before trying more numeric scoring",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1396_2_next",
            "decision": "attack unique Maxwell F2 first",
            "because": "it is the explicit failed clause in EM-lock and would unlock the cleanest zero route if repaired",
            "next_action": "1397 should try unique F2 parent subblock proof or retain a finite lambda_A F_Q^2 source row",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1396_0_1397",
            "next_doc": "1397-Y5-R10-RAB-unique-Maxwell-F2-proof-or-lambdaA-source-row.md",
            "next_script": "scripts/Y5_R10_RAB_unique_Maxwell_F2_proof_or_lambdaA_source_row.py",
            "task": "try to prove unique Maxwell F2 parent subblock/no independent lambda_A F_Q^2; if it fails, create a finite lambda_A source row tied to beta_EM/alphaEM gates",
            "success_condition": "unique F2 is either parent-signed as a theorem clause or lambda_A is explicit as a nonclaim source coefficient with alphaEM/WEP/clock/R10/local refusal gates",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;clock pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    repair: list[dict[str, str]],
    bounds: list[dict[str, str]],
    arenas: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    theorem_ready = any(
        row["repair_id"] == "ELR1396_5_conditional_theorem"
        and row["current_result"] == "EXACT_CONDITIONAL_THEOREM_READY"
        and row["claim_allowed"] == "False"
        for row in repair
    )
    repair_failed = any(
        row["repair_id"] == "ELR1396_6_current_verdict"
        and row["current_result"] == "EM_LOCK_NOT_REPAIRED_FINITE_TEMPLATE_REQUIRED"
        and row["claim_allowed"] == "False"
        for row in repair
    )
    unique_f2_failed = any(
        row["repair_id"] == "ELR1396_1_unique_Maxwell_F2"
        and row["current_result"] == "FAILS_CURRENT_CORPUS"
        for row in repair
    )
    template_ready = any(
        row["bound_id"] == "BEM1396_6_template_verdict"
        and row["current_status"] == "BETA_EM_SOURCE_BOUND_TEMPLATE_READY_NONCLAIM"
        and row["claim_allowed"] == "False"
        for row in bounds
    )
    all_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in bounds)
    arenas_blocked = all(row["current_status"].startswith("BLOCKED") for row in arenas)
    interface_blocked = any(
        row["interface_id"] == "BEI1396_4_verdict"
        and row["current_status"] == "BETA_EM_INTERFACE_READY_SCORING_BLOCKED"
        and row["claim_allowed"] == "False"
        for row in interface
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1396_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_1395 = csv_rows(SRC_DIR / "P8_Y5_R10_1395_CLAIM_GATE.csv")
    prior_local_blocked = any(
        row["gate_id"] == "GATE1395_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1395
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        EM_LOCK_REPAIR_PATH,
        BETA_EM_BOUND_PATH,
        ARENA_GATE_PATH,
        INTERFACE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_beta_EM_lock_repair_or_finite_alphaEM_source_bound.py"),
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and theorem_ready
        and repair_failed
        and unique_f2_failed
        and template_ready
        and all_nonclaim
        and arenas_blocked
        and interface_blocked
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1396_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1396_1_EM_lock_repair",
            "check": "EM-lock theorem is exact conditional but not repaired",
            "status": "PASS" if theorem_ready and repair_failed and unique_f2_failed else "FAIL",
            "details": "ELR1396_5 records conditional theorem; ELR1396_1 and ELR1396_6 keep it blocked.",
        },
        {
            "validation_id": "VAL1396_2_finite_template",
            "check": "finite beta_EM source-bound template is explicit and nonclaim",
            "status": "PASS" if template_ready and all_nonclaim else "FAIL",
            "details": f"template_rows={len(bounds)}; all_nonclaim={all_nonclaim}",
        },
        {
            "validation_id": "VAL1396_3_arena_interface",
            "check": "alphaEM/WEP/clock/R10/local gates remain blocked",
            "status": "PASS" if arenas_blocked and interface_blocked else "FAIL",
            "details": "EMG1396 rows block arenas and BEI1396_4 blocks beta_EM promotion.",
        },
        {
            "validation_id": "VAL1396_4_claim_refusal",
            "check": "empirical and local claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1396_5 and prior GATE1395_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1396_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1396_6_overall",
            "check": "overall 1396 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1396 keeps EM-lock unsigned, writes a finite beta_EM template, and blocks alphaEM/WEP/clock/R10/local scoring.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    repair: list[dict[str, str]],
    bounds: list[dict[str, str]],
    arenas: list[dict[str, str]],
    interface: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1396 - Y5 R10 RAB Beta-EM Lock Repair Or Finite AlphaEM Source Bound

**Generated:** {generated}

**Current verdict:** EM-lock is still the clean route to `beta_EM=0`, but it is not repaired. The exact theorem is available only if charge generator, unique Maxwell `F^2`, current owner, readout descent, and no-alpha vertex all close; the current corpus still fails the unique-`F^2` clause and leaves the rest unsigned.

**Discipline move:** keep a finite `beta_EM` source-bound template instead of claiming EM-lock. The template separates `beta_EM`, `b_alpha_EM`, `beta_source_alpha`, clock/WEP split, R10 material leg, and local residual vector so clock, WEP, R10, and local-GR gates cannot be confused.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## EM-Lock Repair Attempt

{md_table(repair)}

## Finite `beta_EM` Source-Bound Template

{md_table(bounds)}

## AlphaEM / WEP / Clock / R10 Gate

{md_table(arenas)}

## `beta_EM` Interface Update

{md_table(interface)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    repair = em_lock_repair_rows()
    bounds = beta_em_bound_rows()
    arenas = arena_gate_rows()
    interface = interface_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, repair, bounds, arenas, interface, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(EM_LOCK_REPAIR_PATH, repair)
    write_csv(BETA_EM_BOUND_PATH, bounds)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(INTERFACE_PATH, interface)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, repair, bounds, arenas, interface, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1396 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
