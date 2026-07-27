from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1402-Y5-R10-RAB-local-domain-tau-transfer-theorem-or-arena-isolation-ledger.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1402_SOURCE_REGISTER.csv"
TRANSFER_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv"
ARENA_ISOLATION_PATH = SRC_DIR / "P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv"
DOMAIN_MATRIX_PATH = SRC_DIR / "P8_Y5_R10_1402_DOMAIN_TRANSFER_MATRIX.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1402_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1402_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1402_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1402_VALIDATION.csv"

STATUS = (
    "Y5_R10_1402_shared_tau_domain_transfer_not_derived_"
    "arena_isolation_ledger_written_nonclaim"
)
CLAIM_CEILING = (
    "domain_tau_transfer_or_isolation_ledger_only_no_clock_to_WEP_transfer_no_R10_transfer_"
    "no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1402_0_1401_doc",
        "source_path": "1401-Y5-R10-RAB-finite-EM-local-residual-source-map-and-PPN-pressure-gate.md",
        "required_anchor": "NEXT1401_0_1402",
        "purpose": "handoff selecting local domain/tau transfer theorem or arena isolation ledger",
    },
    {
        "source_id": "SRC1402_1_1401_map",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1401_RESIDUAL_SOURCE_MAP.csv",
        "required_anchor": "RSM1401_9_local_PPN",
        "purpose": "residual source map requiring tau/domain transfer",
    },
    {
        "source_id": "SRC1402_2_1401_targets",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1401_PRESSURE_TARGET_LEDGER.csv",
        "required_anchor": "PT1401_0_clock_product",
        "purpose": "clock/WEP/R10/local pressure targets",
    },
    {
        "source_id": "SRC1402_3_1401_ppn",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1401_PPN_PRESSURE_GATE.csv",
        "required_anchor": "PPN1401_5_verdict",
        "purpose": "local PPN projection gate",
    },
    {
        "source_id": "SRC1402_4_988_joint",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "required_anchor": "JAV988_3_cross_arena_policy",
        "purpose": "cross-arena policy forbidding clock-only screen reuse",
    },
    {
        "source_id": "SRC1402_5_989_beta_source",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
        "required_anchor": "BSO989_3_not_clock_screen",
        "purpose": "clock screen cannot substitute for WEP force-source normalization",
    },
    {
        "source_id": "SRC1402_6_1400_vector",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
        "required_anchor": "REM1400_9_local_PPN",
        "purpose": "finite EM local residual vector",
    },
    {
        "source_id": "SRC1402_7_1398_prior",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv",
        "required_anchor": "LAP1398_3_clock_bound_channel",
        "purpose": "prior vector notes clock/WEP/R10 transfer maps missing",
    },
    {
        "source_id": "SRC1402_8_1392_template",
        "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        "required_anchor": "K_bulk_ST(lambda)",
        "purpose": "R10 has its own kernel/range/material domain",
    },
    {
        "source_id": "SRC1402_9_this_script",
        "source_path": "scripts/Y5_R10_RAB_local_domain_tau_transfer_theorem_or_arena_isolation_ledger.py",
        "required_anchor": "STATUS",
        "purpose": "1402 generator",
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


def transfer_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "DTT1402_0_shared_b_alpha_symbol",
            "candidate_statement": "clock, WEP, R10, and local PPN all depend on the same finite alphaEM branch",
            "mathematical_form": "b_alpha_EM appears in C_clock, C_WEP, beta_EM, C_R10, and R_EM_local",
            "current_evidence": "same symbol identified in 988/1401",
            "status": "PARTIAL_SYMBOLIC_COMMONALITY",
            "blocker": "same symbol is not a parent-normalized domain/tau transfer theorem",
            "if_closed": "would permit one branch variable to be carried consistently across arenas",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_1_tau_clock_owner",
            "candidate_statement": "tau_clock is derived by the same local domain map as WEP/R10/local PPN",
            "mathematical_form": "tau_clock = T_clock[D_parent(local lab)]",
            "current_evidence": "clock product bound exists only for b_alpha_EM*tau_clock",
            "status": "UNSIGNED_PRODUCT_ONLY",
            "blocker": "standalone b_alpha_EM and tau_clock dynamics are missing",
            "if_closed": "clock bound could become a transferable alphaEM pressure bound",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_2_tau_WEP_source_owner",
            "candidate_statement": "tau_WEP and beta_source_alpha descend from the same local source map as tau_clock",
            "mathematical_form": "eta_AB = DeltaQ_AB beta_source_alpha b_alpha_EM tau_WEP with tau_WEP=T_WEP[D_parent]",
            "current_evidence": "989 says clock screen cannot replace force-source normalization",
            "status": "UNSIGNED_SEPARATE_DEBT",
            "blocker": "beta_source_alpha and tau_WEP source map are unowned",
            "if_closed": "WEP target could constrain the same local branch as clocks",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_3_tau_R10_kernel_owner",
            "candidate_statement": "R10 tau/domain map is the same local branch map with finite-range kernel attached",
            "mathematical_form": "C_R10_EM(lambda)=K_bulk_ST(lambda) beta_bulk,S beta_bulk,T + tail, with tau_R10=T_R10[D_parent]",
            "current_evidence": "R10 template exposes K_bulk_ST(lambda), beta legs, and epsilon_tail as separate missing inputs",
            "status": "UNSIGNED_KERNEL_DOMAIN_MISSING",
            "blocker": "R10 kernel/tail/material geometry and full bound curve are not claim-ready",
            "if_closed": "R10 could become a finite-range pressure lane for the same EM residual branch",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_4_tau_PPN_projection_owner",
            "candidate_statement": "local PPN projection coefficients are generated by the same local domain map",
            "mathematical_form": "delta PPN_i = A_i[D_parent] · R_EM_local for i in gamma,beta,alpha1,alpha2,G",
            "current_evidence": "1401 PPN gate has missing A_gamma,A_beta,A_alpha1,A_G projections",
            "status": "UNSIGNED_PROJECTION_MISSING",
            "blocker": "no local projection coefficients or thresholds are derived",
            "if_closed": "finite EM residual could be pressure-tested against local PPN/Newton gates",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_5_no_arena_specific_screen",
            "candidate_statement": "one arena may not introduce a private screen absent a parent domain theorem",
            "mathematical_form": "S_clock = S_WEP = S_R10 = S_PPN only if parent proves a common D_parent; otherwise no cross-transfer",
            "current_evidence": "988 cross-arena policy and 989 not-clock-screen row",
            "status": "POLICY_SIGNED_AS_DISCIPLINE_NOT_THEOREM",
            "blocker": "policy prevents misuse but does not supply a common transfer map",
            "if_closed": "would enforce consistent screening or explicit isolation",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_6_exact_conditional_theorem",
            "candidate_statement": "if DTT1402_0 through DTT1402_5 close, one shared tau/domain map exists",
            "mathematical_form": "tau_a = T_a[D_parent] and all T_a are fixed functions of one parent local domain, with no private screens",
            "current_evidence": "conditions are named but not parent-signed",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "blocker": "tau_clock, tau_WEP, tau_R10, and PPN projection owners are missing",
            "if_closed": "cross-arena pressure comparison becomes legitimate",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "DTT1402_7_current_verdict",
            "candidate_statement": "shared tau/domain transfer status",
            "mathematical_form": "Z_shared_tau_domain=false until parent domain map exists",
            "current_evidence": "1401 pressure map plus 988/989 cross-arena warnings",
            "status": "SHARED_TRANSFER_NOT_DERIVED_ARENA_ISOLATION_REQUIRED",
            "blocker": "same b_alpha branch is not enough to transfer clock relief to WEP/R10/local PPN",
            "if_closed": "replace isolation ledger with common transfer theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_isolation_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ISO1402_0_clock",
            "arena": "clock/fine-structure",
            "observable_form": "C_clock_EM = K_alpha b_alpha_EM tau_clock",
            "owned_inputs": "source-backed product target only",
            "missing_transfer": "tau_clock and standalone b_alpha_EM",
            "isolation_rule": "clock product cannot bound WEP/R10/PPN without a parent tau transfer theorem",
            "claim_status": "ISOLATED_PRODUCT_PRESSURE_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ISO1402_1_WEP",
            "arena": "WEP/Coulomb",
            "observable_form": "C_WEP_EM = DeltaQ beta_source_alpha b_alpha_EM tau_WEP + binding terms",
            "owned_inputs": "pressure targets for beta_source_alpha only",
            "missing_transfer": "beta_source_alpha owner, tau_WEP, binding map, normalized charges",
            "isolation_rule": "WEP target cannot be satisfied by clock screening alone",
            "claim_status": "ISOLATED_TARGET_PRESSURE_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ISO1402_2_R10",
            "arena": "R10",
            "observable_form": "C_R10_EM(lambda)=K_bulk_ST(lambda) beta_bulk,S beta_bulk,T + epsilon_tail",
            "owned_inputs": "anchor-only noncurve bound rows",
            "missing_transfer": "tau_R10/domain map, kernel, tail, beta maps, full claim-ready bound curve",
            "isolation_rule": "R10 cannot be inferred from clock or WEP relief; it needs finite-range kernel data",
            "claim_status": "ISOLATED_SYMBOLIC_PRESSURE_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ISO1402_3_PPN",
            "arena": "local PPN/Newton/GR",
            "observable_form": "delta PPN_i = A_i · R_EM_local",
            "owned_inputs": "explicit R_EM_local vector only",
            "missing_transfer": "A_gamma,A_beta,A_alpha1,A_alpha2,A_G and local thresholds",
            "isolation_rule": "PPN cannot use clock/WEP/R10 screens unless A_i projection theorem supplies them",
            "claim_status": "ISOLATED_LOCAL_PROJECTION_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ISO1402_4_global_policy",
            "arena": "cross-arena finite EM branch",
            "observable_form": "R_EM_local components feed arenas through separate T_clock,T_WEP,T_R10,A_PPN maps",
            "owned_inputs": "symbolic common residual branch",
            "missing_transfer": "one parent D_parent map or explicit arena-by-arena source maps",
            "isolation_rule": "no arena-specific screen may be reused elsewhere without a source row and parent theorem",
            "claim_status": "ARENAS_ISOLATED_UNTIL_TRANSFER_THEOREM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def domain_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "matrix_id": "DTM1402_0_clock_to_WEP",
            "from_arena": "clock",
            "to_arena": "WEP",
            "transfer_needed": "tau_clock -> beta_source_alpha*tau_WEP",
            "current_status": "FORBIDDEN_WITHOUT_PARENT_THEOREM",
            "reason": "989 separates time-drift screening from force-source normalization",
            "allowed_use_now": "none; compare only as pressure diagnostics",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "matrix_id": "DTM1402_1_clock_to_R10",
            "from_arena": "clock",
            "to_arena": "R10",
            "transfer_needed": "tau_clock -> tau_R10 plus material kernel",
            "current_status": "FORBIDDEN_WITHOUT_KERNEL_AND_DOMAIN",
            "reason": "R10 needs K_bulk_ST(lambda), beta maps, tail, and bound curve",
            "allowed_use_now": "none; clock product cannot be an R10 pass",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "matrix_id": "DTM1402_2_clock_to_PPN",
            "from_arena": "clock",
            "to_arena": "local PPN",
            "transfer_needed": "tau_clock -> A_i projection coefficients",
            "current_status": "FORBIDDEN_WITHOUT_LOCAL_PROJECTION",
            "reason": "PPN pressure gate lacks A_gamma,A_beta,A_alpha1,A_G",
            "allowed_use_now": "none; clock product cannot be local-GR evidence",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "matrix_id": "DTM1402_3_WEP_to_R10",
            "from_arena": "WEP",
            "to_arena": "R10",
            "transfer_needed": "beta_source_alpha*tau_WEP -> beta_bulk,S/T and K_bulk_ST(lambda)",
            "current_status": "FORBIDDEN_WITHOUT_MATERIAL_KERNEL",
            "reason": "WEP target lacks R10 kernel/tail/range dependence",
            "allowed_use_now": "none; WEP target is not alpha(lambda)",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "matrix_id": "DTM1402_4_WEP_to_PPN",
            "from_arena": "WEP",
            "to_arena": "local PPN",
            "transfer_needed": "composition residual -> PPN projection coefficients",
            "current_status": "FORBIDDEN_WITHOUT_LOCAL_COMPOSITION_PROJECTION",
            "reason": "WEP pressure is a target-only force-source diagnostic, not a PPN bound",
            "allowed_use_now": "none; local-GR claim stays blocked",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "matrix_id": "DTM1402_5_R10_to_PPN",
            "from_arena": "R10",
            "to_arena": "local PPN",
            "transfer_needed": "finite-range alpha(lambda) -> local effective-G/PPN limit",
            "current_status": "FORBIDDEN_WITHOUT_RANGE_LIMIT_AND_BOUND_CURVE",
            "reason": "R10 live curve is placeholder-invalid and finite-range-to-local limit is missing",
            "allowed_use_now": "none; R10 remains smoke lane only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1402_0_shared_transfer",
            "claim": "one shared local tau/domain transfer map exists",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau_clock, tau_WEP, tau_R10, and PPN projection owners are all missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1402_1_clock_relieves_WEP",
            "claim": "clock screening can relieve WEP pressure",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "clock product and force-source normalization are explicitly separate debts",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1402_2_clock_or_WEP_relieves_R10",
            "claim": "clock/WEP pressure can be transferred to R10",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R10 kernel, material beta maps, tail, and bound curve are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1402_3_arena_to_PPN",
            "claim": "clock/WEP/R10 pressure implies PPN/local-GR safety",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "local PPN projection coefficients are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1402_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "arena isolation protects against false local-GR transfer claims",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1402_0_transfer_status",
            "decision": "do not promote shared tau/domain transfer",
            "reason": "same b_alpha branch is not enough; each arena requires its own tau/source/kernel/projection owner",
            "consequence": "use arena isolation ledger until a parent D_parent theorem exists",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1402_1_safest_empirical_route",
            "decision": "treat clock, WEP, R10, and PPN as isolated pressure lanes",
            "reason": "this prevents post-hoc transfer of a favorable screen between incompatible observables",
            "consequence": "future tests must source each lane separately",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1402_2_next",
            "decision": "attack WEP source normalization first",
            "reason": "WEP has the sharpest numeric pressure target and the missing object is exact: beta_source_alpha*tau_WEP",
            "consequence": "next target 1403",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1402_0_1403",
            "target_doc": "1403-Y5-R10-RAB-WEP-source-normalization-owner-or-finite-beta-source-prior.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_source_normalization_owner_or_finite_beta_source_prior.py",
            "task": "derive beta_source_alpha*tau_WEP from same-owner current/source geometry, or retain it as an explicit finite empirical prior against the WEP pressure targets",
            "success_condition": "either WEP source normalization is theorem-zero/owned, or beta_source_alpha*tau_WEP is a nonclaim prior row with alpha-only and robust pressure targets",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    transfer: list[dict[str, str]],
    isolation: list[dict[str, str]],
    matrix: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    transfer_blocked = any(
        row["audit_id"] == "DTT1402_7_current_verdict"
        and row["status"] == "SHARED_TRANSFER_NOT_DERIVED_ARENA_ISOLATION_REQUIRED"
        for row in transfer
    )
    conditional_present = any(
        row["audit_id"] == "DTT1402_6_exact_conditional_theorem"
        and row["status"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED"
        for row in transfer
    )
    isolation_ok = all(
        row["valid_for_claim"] == "False"
        and row["claim_allowed"] == "False"
        and ("ISOLATED" in row["claim_status"] or row["arena_id"] == "ISO1402_4_global_policy")
        for row in isolation
    )
    matrix_blocks = all(
        row["valid_for_claim"] == "False"
        and row["claim_allowed"] == "False"
        and row["current_status"].startswith("FORBIDDEN")
        for row in matrix
    )
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        TRANSFER_AUDIT_PATH,
        ARENA_ISOLATION_PATH,
        DOMAIN_MATRIX_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = source_ok and transfer_blocked and conditional_present and isolation_ok and matrix_blocks and gates_blocked and scope_ok
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1402_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_1_transfer_audit",
            "status": "PASS" if transfer_blocked and conditional_present else "FAIL",
            "detail": "shared tau/domain theorem is exact conditional only and not promoted",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_2_arena_isolation",
            "status": "PASS" if isolation_ok else "FAIL",
            "detail": "clock, WEP, R10, and PPN lanes are explicitly isolated and nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_3_transfer_matrix",
            "status": "PASS" if matrix_blocks else "FAIL",
            "detail": "all cross-arena transfers are forbidden without parent theorem or source map",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_4_claim_refusal",
            "status": "PASS" if gates_blocked else "FAIL",
            "detail": "clock-to-WEP, clock/WEP-to-R10, arena-to-PPN, and local-GR claims are refused",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_5_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1402_6_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1402 rejects shared tau transfer for now and installs arena isolation ledger",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    transfer: list[dict[str, str]],
    isolation: list[dict[str, str]],
    matrix: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1402 Y5 R10 RAB: Local Domain Tau Transfer Theorem Or Arena Isolation Ledger

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** a shared local `tau/domain` transfer map is not derived. The corpus has a common finite `b_alpha_EM` symbol, but not a parent-signed map that turns `tau_clock`, `tau_WEP`, `tau_R10`, and local PPN projections into the same physical screen.

**Discipline move:** isolate the arenas until a parent domain theorem exists. Clock pressure, WEP pressure, R10 pressure, and PPN pressure are all useful, but none can be used to relieve another without a source-backed transfer row.

## Source Register

{md_table(sources)}

## Shared Tau Transfer Theorem Audit

{md_table(transfer)}

## Arena Isolation Ledger

{md_table(isolation)}

## Domain Transfer Matrix

{md_table(matrix)}

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
    transfer = transfer_audit_rows()
    isolation = arena_isolation_rows()
    matrix = domain_matrix_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, transfer, isolation, matrix, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(TRANSFER_AUDIT_PATH, transfer)
    write_csv(ARENA_ISOLATION_PATH, isolation)
    write_csv(DOMAIN_MATRIX_PATH, matrix)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, transfer, isolation, matrix, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1402 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
