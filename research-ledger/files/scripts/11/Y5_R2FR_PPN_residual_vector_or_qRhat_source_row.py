from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1691"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1691-Y5-R2FR-PPN-residual-vector-or-qRhat-source-row.md"

SOURCE_FILES = {
    "1690_doc": ROOT / "1690-Y5-R2FR-beta-bulk-source-test-convention-or-r10-curve-first-digitization.md",
    "1690_validation": OUT / "P8_Y5_BRR545_1690_VALIDATION.csv",
    "1690_next": OUT / "P8_Y5_PARENT_QLOC_1690_NEXT_ROUTE_SELECTION.csv",
    "1580_doc": ROOT / "1580-Y5-RAB-PPN-residual-vector-or-qRhat-source-row.md",
    "1580_bridge": OUT / "P8_Y5_PARENT_QLOC_1580_PPN_BRIDGE_DERIVATION.csv",
    "1580_qrhat": OUT / "P8_Y5_PARENT_QLOC_1580_QRHAT_SOURCE_ROW_NONCLAIM.csv",
    "1581_profile": OUT / "P8_Y5_PARENT_QLOC_1581_QRHAT_PROFILE_DERIVATION.csv",
    "1581_cassini": OUT / "P8_Y5_PARENT_QLOC_1581_CASSINI_QR_BOUND_ROW_NONCLAIM.csv",
    "1582_nocharge": OUT / "P8_Y5_PARENT_QLOC_1582_NO_CHARGE_SIGNATURE_AUDIT.csv",
    "1582_denominator": OUT / "P8_Y5_PARENT_QLOC_1582_SOURCE_DENOMINATOR_CONTRACT.csv",
    "1582_tail": OUT / "P8_Y5_PARENT_QLOC_1582_PPN_TAIL_ENVELOPE.csv",
    "1583_completion": OUT / "P8_Y5_PARENT_QLOC_1583_GR_COMPLETION_GATE.csv",
    "1584_beta": OUT / "P8_Y5_PARENT_QLOC_1584_BETA_GATE.csv",
    "1584_conservation": OUT / "P8_Y5_PARENT_QLOC_1584_CONSERVATION_GATE.csv",
    "1584_common_matter": OUT / "P8_Y5_PARENT_QLOC_1584_COMMON_MATTER_GATE.csv",
    "1584_newton": OUT / "P8_Y5_PARENT_QLOC_1584_NEWTON_SOURCE_GATE.csv",
    "1585_owner": OUT / "P8_Y5_PARENT_QLOC_1585_EH_SOURCE_OWNER_CONTRACT.csv",
    "1585_beta_residual": OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv",
    "1586_doc": ROOT / "1586-Y5-parent-minimality-no-extra-sector-signature-or-R11-beta-vector-fill.md",
    "1586_validation": OUT / "P8_Y5_BRR545_1586_VALIDATION.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1690_doc": ["derive the PPN residual vector", "gamma_minus_1=C_QR*q_R_hat+source_tail+boundary_tail"],
    "1690_validation": ["VAL1690_OVERALL", "PASS"],
    "1690_next": ["NEXT1690_0_primary", "PPN-residual-vector"],
    "1580_doc": ["R_AB=2(gamma-1)U_N", "q_R_hat:=R_AB^(1)/(2U_N)"],
    "1580_bridge": ["PPNB1580_2_linear_bridge", "DERIVED_CONDITIONAL_BRIDGE"],
    "1580_qrhat": ["QRHAT1580_0_definition", "FORMAL_DEFINITION_DERIVED_VALUE_MISSING"],
    "1581_profile": ["PROF1581_3_ppn_ratio", "DERIVED_CONDITIONAL_BOUND_TARGET"],
    "1581_cassini": ["CB1581_0_qRhat", "4.6e-05"],
    "1582_nocharge": ["NCS1582_4_verdict", "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED"],
    "1582_denominator": ["SD1582_0_QR", "MISSING_QR_VALUE_OR_ZERO_THEOREM"],
    "1582_tail": ["TAIL1582_5_higher_order", "MISSING_SECOND_ORDER_CONTROL"],
    "1583_completion": ["GRC1583_1_beta", "MISSING_DERIVATION"],
    "1584_beta": ["BETA1584_4_verdict", "FAIL_CURRENT_CLAIM_BETA_NOT_DERIVED"],
    "1584_conservation": ["CONS1584_1_projected_identity", "OBSTRUCTION_DERIVED_NOT_ZERO"],
    "1584_common_matter": ["MAT1584_4_verdict", "FAIL_CURRENT_CLAIM_COMMON_MATTER_NOT_DERIVED"],
    "1584_newton": ["NEW1584_4_verdict", "FAIL_CURRENT_CLAIM_NEWTON_SOURCE_NOT_DERIVED"],
    "1585_owner": ["OWN1585_5_verdict", "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED"],
    "1585_beta_residual": ["BRL1585_7_total_no_cancellation", "NOT_RUN_COMPONENTS_MISSING"],
    "1586_doc": ["parent minimality/no-extra-sector would be powerful", "1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md"],
    "1586_validation": ["VAL1586_OVERALL", "PASS"],
    "local_bounds": ["Cassini_Shapiro_gamma_2003", "Will_2014_PPN_beta_table"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1691_SOURCE_REGISTER.csv"
PPN_VECTOR = OUT / "P8_Y5_PARENT_QLOC_1691_PPN_RESIDUAL_VECTOR.csv"
QRHAT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1691_QRHAT_SOURCE_AND_CASSINI_CONTRACT.csv"
GR_GATE = OUT / "P8_Y5_PARENT_QLOC_1691_GR_COMPLETION_GATE_CURRENT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1691_LOCAL_GR_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1691_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1691_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1691_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PPN_VECTOR,
    QRHAT_CONTRACT,
    GR_GATE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    PPN_VECTOR,
    QRHAT_CONTRACT,
    GR_GATE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    PPN_VECTOR: [
        QUARANTINE / "PPN_RESIDUAL_VECTOR.csv",
        BRANCH_RESIDUALS / "R2FR_PPN_residual_vector_1691.csv",
        QUEUE / "JR1691_PPN_RESIDUAL_VECTOR.csv",
    ],
    QRHAT_CONTRACT: [
        QUARANTINE / "QRHAT_SOURCE_AND_CASSINI_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_qRhat_source_and_Cassini_contract_1691.csv",
        QUEUE / "JR1691_QRHAT_SOURCE_AND_CASSINI_CONTRACT.csv",
    ],
    GR_GATE: [
        QUARANTINE / "GR_COMPLETION_GATE_CURRENT.csv",
        BRANCH_RESIDUALS / "R2FR_GR_completion_gate_current_1691.csv",
        QUEUE / "JR1691_GR_COMPLETION_GATE_CURRENT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1691.csv",
        QUEUE / "JR1691_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1691": "current PPN/qRhat/local-GR completion bridge",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def ppn_vector_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PPNV1691_0_observer_identity",
            "R_AB",
            "R_AB=ln(A*B)=ln(T^2*S)",
            "observer reciprocal strain",
            "FORMAL_INPUT",
            "same PPN-compatible observer gauge and source frame",
        ),
        (
            "PPNV1691_1_linear_gamma_bridge",
            "gamma_minus_1",
            "R_AB=2*(gamma-1)*U_N+O(U_N^2)",
            "leading PPN gamma bridge",
            "DERIVED_CONDITIONAL_BRIDGE",
            "gauge/source denominator and observer-map matching must be fixed",
        ),
        (
            "PPNV1691_2_qRhat_definition",
            "q_R_hat",
            "q_R_hat:=R_AB^(1)/(2*U_N)",
            "dimensionless local reciprocal hair",
            "FORMAL_DEFINITION_VALUE_MISSING",
            "R_AB profile or no-charge theorem still missing",
        ),
        (
            "PPNV1691_3_full_gamma_vector",
            "gamma_minus_1",
            "gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+delta_readout+O(U_N)",
            "claim-safe residual vector",
            "FORMAL_NONCLAIM_VECTOR_READY",
            "all tails must be theorem-zero or source-bounded absolutely",
        ),
        (
            "PPNV1691_4_current_hair_projection",
            "q_R_hat",
            "if W=kappa_W*r^2 then q_R_hat=-Q_R/(2*kappa_W*G*M)+O(GM/r)",
            "finite current-hair Cassini target",
            "DERIVED_CONDITIONAL_BOUND_TARGET",
            "Q_R, kappa_W, source mass, sign and domain are unsourced",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "vector_id": vector_id,
            "symbol": symbol,
            "equation": equation,
            "role": role,
            "status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for vector_id, symbol, equation, role, status, gap in rows
    ]


def qrhat_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "QRHC1691_0_qRhat",
            "q_R_hat",
            "q_R_hat:=R_AB^(1)/(2*U_N)",
            "dimensionless",
            "MISSING_VALUE_OR_THEOREM_ZERO",
            "Cassini gamma bound target",
            "abs(q_R_hat+tails)<=2.3e-05",
        ),
        (
            "QRHC1691_1_QR_over_GM",
            "Q_R/(G*M)",
            "-Q_R/(2*kappa_W*G*M) maps to q_R_hat",
            "dimensionless",
            "MISSING_QR_KAPPAW_GM",
            "conditional finite-hair target",
            "if kappa_W=1 and tails=0 then abs(Q_R/(G*M))<=4.6e-05",
        ),
        (
            "QRHC1691_2_nocharge",
            "Q_R=0",
            "Pi_R=0 -> Q_R=0 -> R_AB=0 -> gamma_minus_1=0 at leading order",
            "theorem-zero",
            "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "clean GR route for gamma channel",
            "needs source-boundary and tail silence signatures",
        ),
        (
            "QRHC1691_3_tail_envelope",
            "PPN_tail_abs",
            "abs(Q_R)/(2*abs(kappa_W)*G*M)+abs(delta_gauge)+abs(delta_source)+abs(delta_boundary)+abs(delta_readout)+abs(O(U_N))",
            "dimensionless",
            "MISSING_COMPONENT_VALUES",
            "no-cancellation Cassini readiness contract",
            "all terms must be zero-proved or bounded before scoring",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "symbol": symbol,
            "definition_or_formula": formula,
            "units": units,
            "current_status": status,
            "observable_link": link,
            "bound_contract": bound,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, symbol, formula, units, status, link, bound in rows
    ]


def gr_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "GRG1691_0_gamma",
            "PPN gamma channel",
            "q_R_hat=0 or bounded q_R_hat plus absolute tails",
            "FORMAL_BRIDGE_READY_NOT_SCOREABLE",
            "Q_R/source denominator/tails missing",
        ),
        (
            "GRG1691_1_beta",
            "PPN beta channel",
            "beta_minus_1=0 or Delta_beta_total_abs<=7.8e-05",
            "MISSING_DERIVATION_AND_VALUES",
            "gamma branch does not imply beta",
        ),
        (
            "GRG1691_2_conservation",
            "source-compatible Bianchi/Ward closure",
            "projected Hilbert channel obstruction terms vanish or are bounded",
            "OBSTRUCTION_DERIVED_NOT_ZERO",
            "total Ward conservation alone is insufficient",
        ),
        (
            "GRG1691_3_common_matter",
            "universal observed coframe and matter coupling",
            "one e_obs, tau lock, matter descent, no-marker rule",
            "COMMON_MATTER_UNSIGNED",
            "coframe/tau/matter/no-marker clauses remain open",
        ),
        (
            "GRG1691_4_newton_source",
            "source-normalized Newton denominator",
            "mu_obs=G_eff*M_eff in the same Hilbert/source frame",
            "SOURCE_DENOMINATOR_MISSING",
            "cannot use orbital GM to prove the source normalization it assumes",
        ),
        (
            "GRG1691_5_EH_owner",
            "single parent action owner",
            "EH-like operator plus universal matter plus measured GM plus no U2 leakage",
            "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "next derivation target rather than current evidence",
        ),
        (
            "GRG1691_6_R11_beta_leakage",
            "non-EH/R11 beta vector",
            "minimality/no-extra-sector theorem or source-backed coefficient vector",
            "R11_VECTOR_MISSING",
            "higher-curvature/scalar/source/readout countermodels remain live",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, required, status, gap in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1691_0_gamma_only", "claim local GR from gamma/q_Rhat alone", "REFUSE_PLACEHOLDER", "beta, conservation, common matter and source-normalized Newton remain open"),
        ("RUN1691_1_cassini_score", "score Cassini bound", "NOT_RUN_COMPONENTS_MISSING", "q_Rhat/Q_R, kappa_W, GM and tails are missing"),
        ("RUN1691_2_nocharge_import", "set Q_R=0 by source neutrality label", "REFUSE_UNSIGNED_ZERO", "Pi_R=0/source-boundary theorem is sufficient but unsigned"),
        ("RUN1691_3_beta_score", "score PPN beta bound", "NOT_RUN_PREDICTION_MISSING", "external beta bound exists but MTS beta vector is missing"),
        ("RUN1691_4_EH_reference", "use conditional EH family as current MTS proof", "REFUSE_REFERENCE_PROMOTION", "single parent owner and no-extra-sector signatures are not derived"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1691_0_primary",
            "1692-Y5-R2FR-EH-source-owner-or-R11-beta-vector-current-branch.md",
            "scripts/Y5_R2FR_EH_source_owner_or_R11_beta_vector_current_branch.py",
            "attempt the source-normalized EH parent owner route in the current branch; if still unsigned, carry forward the R11 beta vector fill requirements without claiming local GR",
            "this attacks beta/conservation/Newton completion instead of overusing the gamma channel",
            "selected",
        ),
        (
            "NEXT1691_1_secondary",
            "1692b-Y5-R2FR-QR-nocharge-tail-source-denominator-fill.md",
            "scripts/Y5_R2FR_QR_nocharge_tail_source_denominator_fill.py",
            "fill or theorem-zero Q_R, kappa_W, GM, gauge/source/boundary/readout tails for a future Cassini score",
            "needed if finite q_R_hat branch stays live",
            "held_finite_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1691_0_ppn_vector", "PPN residual vector exists", "PASS_FORMAL_NONCLAIM", "gamma/q_Rhat bridge and tail envelope are formal only"),
        ("CG1691_1_cassini", "Cassini gamma score", "BLOCKED_NO_CLAIM", "no q_Rhat/Q_R value or complete tail envelope"),
        ("CG1691_2_nocharge", "Q_R=0 theorem", "BLOCKED_NO_CLAIM", "Pi_R=0/source-boundary neutrality is unsigned"),
        ("CG1691_3_beta", "PPN beta pass", "BLOCKED_NO_CLAIM", "beta residual vector/EH owner not derived"),
        ("CG1691_4_local_gr", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "gamma, beta, conservation, common matter and source denominator must close together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    vector_rows: list[dict[str, object]],
    qrhat_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    bridge_present = any(row["vector_id"] == "PPNV1691_1_linear_gamma_bridge" and "2*(gamma-1)*U_N" in row["equation"] for row in vector_rows)
    qrhat_present = any(row["contract_id"] == "QRHC1691_0_qRhat" for row in qrhat_rows)
    cassini_nonclaim = any(row["contract_id"] == "QRHC1691_1_QR_over_GM" and "4.6e-05" in row["bound_contract"] for row in qrhat_rows) and all(not bool_cell(row["valid_for_claim"]) for row in qrhat_rows)
    gr_gate_complete = {"PPN gamma channel", "PPN beta channel", "source-compatible Bianchi/Ward closure", "universal observed coframe and matter coupling", "source-normalized Newton denominator", "single parent action owner", "non-EH/R11 beta vector"}.issubset({str(row["gate"]) for row in gr_rows})
    gamma_shortcut_refused = any(row["runner_id"] == "RUN1691_0_gamma_only" and row["status"] == "REFUSE_PLACEHOLDER" for row in runner_rows_)
    cassini_blocked = any(row["claim"] == "Cassini gamma score" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    next_selected = any(row["route_id"] == "NEXT1691_0_primary" and row["selection_status"] == "selected" and "EH-source-owner" in row["next_target"] for row in next_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1691*"))) == 0 if FORMALIZATION.exists() else True

    checks = [
        ("VAL1691_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1691_1_bridge_present", bridge_present, "linear PPN gamma bridge is present"),
        ("VAL1691_2_qrhat_present", qrhat_present, "q_R_hat source contract is present"),
        ("VAL1691_3_cassini_nonclaim", cassini_nonclaim, "Cassini bound target exists but remains nonclaim"),
        ("VAL1691_4_gr_gate_complete", gr_gate_complete, "GR completion gates include gamma beta conservation matter Newton owner and R11 leakage"),
        ("VAL1691_5_gamma_shortcut_refused", gamma_shortcut_refused, "gamma-only local GR shortcut is refused"),
        ("VAL1691_6_cassini_blocked", cassini_blocked, "Cassini score remains blocked"),
        ("VAL1691_7_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1691_8_next_selected", next_selected, "next target selects EH source owner or R11 beta vector current branch"),
        ("VAL1691_9_no_claim_flags", no_claim_flags, "all generated claim/scoring flags remain false"),
        ("VAL1691_10_csv_parse", csv_parse, "all generated 1691 CSVs parse"),
        ("VAL1691_11_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1691_12_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1691_13_formalization_untouched", formalization_untouched, "no 1691 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1691_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1691 current-branch PPN residual vector validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    vector_rows: list[dict[str, object]],
    qrhat_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1691 - PPN Residual Vector Or qRhat Source Row

## Verdict

The current branch now has a clean PPN-facing residual vector. In a PPN-compatible observer gauge, `R_AB=ln(A*B)` gives `R_AB=2*(gamma-1)*U_N+O(U_N^2)`, so the local reciprocal hair variable is `q_R_hat:=R_AB^(1)/(2*U_N)`.

If the finite current-hair branch survives, `W=kappa_W*r^2` gives `q_R_hat=-Q_R/(2*kappa_W*G*M)+O(GM/r)`. That makes Cassini a meaningful pressure test, but not a pass: `Q_R`, `kappa_W`, same-frame `G*M`, gauge/source/boundary/readout tails and second-order control are all still missing.

Most importantly, gamma is not GR. The local-GR route still needs beta, projected conservation, common matter coupling, source-normalized Newton and no non-EH/R11 beta leakage under one parent action. The next attack is therefore the EH/source-owner or R11 beta-vector current-branch gate.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1691"])}

## PPN Residual Vector

{markdown_table(vector_rows, ["vector_id", "symbol", "equation", "status", "blocking_gap"])}

## qRhat Source And Cassini Contract

{markdown_table(qrhat_rows, ["contract_id", "symbol", "definition_or_formula", "current_status", "bound_contract"])}

## GR Completion Gate

{markdown_table(gr_rows, ["gate_id", "gate", "required_statement", "current_status", "blocking_gap"])}

## Local GR Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a real narrowing toward GR: MTS now has a named local PPN residual vector rather than a vague local branch. The grim bit is that the residual vector exposes more gates, not fewer. The hopeful bit is that the right gates are now mathematically sharp: kill or bound `Q_R`, close the tails, then close beta/conservation/source-normalization/R11 leakage under one parent action.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    vector_rows = ppn_vector_rows()
    qrhat_rows = qrhat_contract_rows()
    gr_rows = gr_gate_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1691", "valid_for_claim", "claim_allowed"])
    write_csv(PPN_VECTOR, vector_rows, ["branch_id", "vector_id", "symbol", "equation", "role", "status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(QRHAT_CONTRACT, qrhat_rows, ["branch_id", "contract_id", "symbol", "definition_or_formula", "units", "current_status", "observable_link", "bound_contract", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GR_GATE, gr_rows, ["branch_id", "gate_id", "gate", "required_statement", "current_status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, vector_rows, qrhat_rows, gr_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, vector_rows, qrhat_rows, gr_rows, runner_rows_, next_rows, claim_rows, validation_rows)

    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1691 validation PASS")


if __name__ == "__main__":
    main()
