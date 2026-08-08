from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_MULTIMODE_PERMISSION_OR_SCALAR_NO_GO_2276"
DOC = ROOT / "2276-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2276_00_2275_doc",
        "source_key": "2275_doc",
        "source_path": ROOT / "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md",
        "needles": ["MCI2275_0_covariance_ensemble", "PPC2275_0_multicarrier_permission", "NEXT2275_0_primary"],
        "role": "handoff: carrier inventory represented q tangent but parent permission unsigned",
    },
    {
        "source_id": "SRC2276_01_2275_validation",
        "source_key": "2275_validation",
        "source_path": OUT / "P8_Y5_BRR545_2275_VALIDATION.csv",
        "needles": ["VAL2275_OVERALL", "PASS"],
        "role": "confirms 2275 passed before 2276 starts",
    },
    {
        "source_id": "SRC2276_02_2275_inventory",
        "source_key": "2275_inventory",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2275_MINIMAL_CARRIER_INVENTORY.csv",
        "needles": ["MCI2275_0_covariance_ensemble", "C_mn=sum_I s_I W_I k_I,m k_I,n"],
        "role": "machine-readable carrier covariance inventory",
    },
    {
        "source_id": "SRC2276_03_2275_contract",
        "source_key": "2275_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2275_PARENT_PERMISSION_CONTRACT.csv",
        "needles": ["PPC2275_0_multicarrier_permission", "UNSIGNED"],
        "role": "parent permission clauses",
    },
    {
        "source_id": "SRC2276_04_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "nonlinear wave equation", "Superposition → linear regime of ψ"],
        "role": "scalar psi action, wave dynamics, and linear-regime superposition statement",
    },
    {
        "source_id": "SRC2276_05_motion_action",
        "source_key": "motion_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["rapid Planck-scale oscillations average out", "⟨ ∂_μ ψ(x) ∂_ν ψ(x) ⟩_{smooth}", "GR is the long-wavelength effective theory of MTS"],
        "role": "smoothing and long-wavelength effective-theory statements",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2276_SOURCE_REGISTER.csv",
    "permission": OUT / "P8_Y5_PARENT_QLOC_2276_MULTIMODE_PERMISSION_AUDIT.csv",
    "wkb_derivation": OUT / "P8_Y5_PARENT_QLOC_2276_WKB_COVARIANCE_DERIVATION.csv",
    "scalar_no_go": OUT / "P8_Y5_PARENT_QLOC_2276_SCALAR_ONLY_NO_GO_LEDGER.csv",
    "weight_contract": OUT / "P8_Y5_PARENT_QLOC_2276_WEIGHT_DYNAMICS_CONTRACT.csv",
    "qr_route": OUT / "P8_Y5_PARENT_QLOC_2276_QR_ROUTE_CONSEQUENCE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2276_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2276_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2276_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2276_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2276_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2276_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_permission": QUEUE / "JR2276_PARENT_MULTIMODE_PERMISSION_AUDIT_NONCLAIM.csv",
    "queue_weight_contract": QUEUE / "JR2276_WEIGHT_DYNAMICS_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_parent_multimode_permission_refusal_2276.csv",
    "beta_docs": BETA_DOCS / "RAB_PARENT_MULTIMODE_PERMISSION_2276_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path) if path.exists() else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def permission_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "MPA2276_0_single_field_multimode",
            "question": "Can a scalar field contain multiple local carriers?",
            "answer": "YES_AS_ASYMPTOTIC_WKB_STRUCTURE",
            "reason": "A single real scalar field can be a sum of local high-frequency phase modes, psi=sum_I a_I cos(S_I/epsilon+theta_I).",
            "claim_ceiling": "permits a carrier inventory as an ansatz/effective expansion, not as a parent-signed exact theory",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPA2276_1_current_corpus_support",
            "question": "Does the current corpus gesture toward this?",
            "answer": "PARTIAL_SUPPORT",
            "reason": "The action material states wave dynamics, linear-regime superposition, rapid oscillations averaging out, and smoothed gradient covariance.",
            "claim_ceiling": "the smoothing kernel, phase ensemble, and amplitude/weight equations are not formalized",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPA2276_2_strict_scalar_no_go",
            "question": "Does scalar-only mean one coherent mode?",
            "answer": "NO_IF_MULTIMODE_ALLOWED",
            "reason": "Scalar-valued does not imply rank-one covariance after smoothing; rank can be built from several phase modes.",
            "claim_ceiling": "strict single-mode or static scalar readings remain insufficient",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPA2276_3_parent_permission_verdict",
            "question": "Is the parent permission claim closed?",
            "answer": "CONDITIONAL_PERMISSION_NOT_PARENT_SIGNED",
            "reason": "The route is mathematically legitimate as WKB/multimode scalar field theory, but MTS has not yet elevated W_I and S_I into controlled parent variables.",
            "claim_ceiling": "no exact local-GR claim",
            "valid_for_claim": False,
        },
    ]


def wkb_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "WKB2276_0_ansatz",
            "object": "multimode scalar ansatz",
            "formula": "psi_epsilon(x)=sum_I a_I(x) cos(S_I(x)/epsilon+theta_I)",
            "derivation": "one scalar field carries several local phases S_I and amplitudes a_I",
            "status": "ASYMPTOTIC_ANSATZ",
            "valid_for_claim": False,
        },
        {
            "step_id": "WKB2276_1_gradient",
            "object": "leading gradient",
            "formula": "partial_m psi_epsilon=sum_I[-a_I k_I,m sin(phi_I)/epsilon + partial_m a_I cos(phi_I)]",
            "derivation": "k_I,m=partial_m S_I and phi_I=S_I/epsilon+theta_I",
            "status": "DERIVED",
            "valid_for_claim": False,
        },
        {
            "step_id": "WKB2276_2_smoothed_covariance",
            "object": "phase-averaged covariance",
            "formula": "<partial_m psi partial_n psi>_smooth=sum_I (a_I^2/(2 epsilon^2)) k_I,m k_I,n + R_mn",
            "derivation": "phase averaging kills I!=J cross terms and averages sin^2 to 1/2; R_mn contains amplitude-gradient and imperfect-averaging residuals",
            "status": "CARRIER_INVENTORY_RECOVERED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "step_id": "WKB2276_3_weight_identification",
            "object": "carrier weights",
            "formula": "W_I=a_I^2/(2 epsilon^2), C_mn=sum_I W_I k_I,m k_I,n + R_mn",
            "derivation": "this matches the 2275 carrier inventory up to signs/cone conventions and residual terms",
            "status": "MATCHES_2275_INVENTORY_WITH_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "step_id": "WKB2276_4_residual_size",
            "object": "amplitude/smoothing leakage",
            "formula": "||R||/||C|| = O(epsilon/L_amp) + O(kernel_cross_phase_leakage)",
            "derivation": "slow amplitude variation and many-phase smoothing suppress non-carrier terms",
            "status": "BOUND_TEMPLATE_NOT_NUMERIC",
            "valid_for_claim": False,
        },
    ]


def scalar_no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "SNG2276_0_single_mode",
            "case": "one coherent phase mode",
            "rank_capacity": "rank <= 1 before background eta",
            "q_capacity": "cannot independently tune C_tt and C_rr while keeping C_tr silent over a finite radial cell",
            "verdict": "INSUFFICIENT_FOR_LOCAL_Q_BRANCH",
            "valid_for_claim": False,
        },
        {
            "case_id": "SNG2276_1_static_single_scalar",
            "case": "psi=-E t+chi(r)",
            "rank_capacity": "two components but tied by exactness and static assumptions",
            "q_capacity": "cannot freely choose arbitrary radial C_tt(r), C_rr(r), and C_tr=0 without extra structure",
            "verdict": "INSUFFICIENT_EXCEPT_SPECIAL_PROFILES",
            "valid_for_claim": False,
        },
        {
            "case_id": "SNG2276_2_multimode_scalar",
            "case": "sum of high-frequency local phases",
            "rank_capacity": "rank can equal number of independent smoothed carriers",
            "q_capacity": "can represent temporal/radial q tangent algebraically with residuals",
            "verdict": "NOT_A_NO_GO_BUT_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def weight_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "WDC2276_0_eikonal",
            "requirement": "derive eikonal/dispersion equations for S_I from A_MTS[psi]",
            "why_needed": "carrier directions k_I must be lawful parent modes",
            "current_status": "MISSING_WKB_EIKONAL_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "contract_id": "WDC2276_1_transport",
            "requirement": "derive transport/weight equations for W_I=a_I^2/(2 epsilon^2)",
            "why_needed": "q=0 or finite q_R depends on how temporal/radial carrier weights evolve",
            "current_status": "MISSING_WEIGHT_DYNAMICS",
            "valid_for_claim": False,
        },
        {
            "contract_id": "WDC2276_2_smoothing",
            "requirement": "define smoothing kernel and phase ensemble conditions that kill cross terms/off-diagonal leakage",
            "why_needed": "carrier covariance must be a controlled output, not a convenient average",
            "current_status": "MISSING_KERNEL_AND_PHASE_AVERAGING_THEOREM",
            "valid_for_claim": False,
        },
        {
            "contract_id": "WDC2276_3_q_selection",
            "requirement": "derive C_rr=C_tt/(1-C_tt) or a sourced q_R residual bound from the weight transport law",
            "why_needed": "this is the local-GR reduction gate",
            "current_status": "MISSING_Q_ZERO_SELECTION_OR_QR_BOUND",
            "valid_for_claim": False,
        },
    ]


def qr_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "QRR2276_0_exact_route",
            "route": "exact GR-local route",
            "condition": "WKB transport selects the q=0 carrier-weight relation in local vacuum",
            "consequence": "R_AB/q becomes structurally suppressed rather than fitted",
            "status": "not proven",
            "valid_for_claim": False,
        },
        {
            "route_id": "QRR2276_1_residual_route",
            "route": "finite q_R route",
            "condition": "WKB residuals and weight-source mismatch produce finite q_R",
            "consequence": "q_R must be bounded through epsilon_amp, ell_cg/L_cg, Kq, and local-test tolerances",
            "status": "staged only",
            "valid_for_claim": False,
        },
        {
            "route_id": "QRR2276_2_failure_route",
            "route": "scalar-only failure route",
            "condition": "parent action forbids multimode/ensemble interpretation and no residual bound is sourced",
            "consequence": "local-GR branch is closure-only",
            "status": "not reached; multimode remains conditionally allowed",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2276_0_parent_permission_claim",
            "attempted_claim": "The parent action has fully derived the multimode carrier inventory.",
            "runner_result": "BLOCKED",
            "blocked_by": "WKB ansatz is conditionally permitted, but eikonal, transport, smoothing, and q-selection are unsigned",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2276_1_scalar_no_go_claim",
            "attempted_claim": "A scalar psi cannot support the carrier inventory.",
            "runner_result": "BLOCKED",
            "blocked_by": "multimode WKB scalar ansatz can reproduce the carrier covariance at leading smoothed order",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2276_2_local_gr_claim",
            "attempted_claim": "MTS has now derived the local GR limit.",
            "runner_result": "BLOCKED",
            "blocked_by": "carrier permission is only conditional and q=0 selection/finite q_R scoring is still missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2276_0_conditional_multimode_permission",
            "claim": "a scalar field can conditionally realize a multimode carrier inventory after smoothing",
            "gate_pass": True,
            "reason": "WKB phase expansion gives C_mn=sum_I W_I k_I,m k_I,n plus residuals",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2276_1_parent_signed_inventory",
            "claim": "MTS parent action signs the inventory as exact structure",
            "gate_pass": False,
            "reason": "eikonal/transport/kernel/q-selection derivations are missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2276_2_scalar_only_no_go",
            "claim": "scalar psi route is impossible",
            "gate_pass": False,
            "reason": "single-mode scalar fails, but multimode scalar remains conditionally viable",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2276_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "q=0 selection or sourced finite q_R bound remains absent",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2276_0_gain",
            "decision": "SCALAR_MULTIMODE_PERMISSION_CONDITIONALLY_OPEN",
            "reason": "A scalar field can contain many high-frequency local phase carriers, so scalar-valued does not force rank-one covariance.",
            "next_action": "Promote this only if WKB eikonal/transport/smoothing are derived from A_MTS.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2276_1_no_go",
            "decision": "STRICT_SINGLE_MODE_SCALAR_ROUTE_REJECTED",
            "reason": "A single coherent/static scalar cannot support the local q branch generally.",
            "next_action": "Do not use single-mode arguments as local-GR derivations.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2276_2_blocker",
            "decision": "WEIGHT_TRANSPORT_IS_THE_ACTIVE_BLOCKER",
            "reason": "The carrier inventory is useful only if parent dynamics tell W_T and W_R how to evolve/select q=0.",
            "next_action": "derive WKB transport and q-zero/finite-q_R equation.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2276_3_next",
            "decision": "WKB_TRANSPORT_OR_Q_SELECTION_NEXT",
            "reason": "This is the next mathematical place where local GR could become derivable rather than represented.",
            "next_action": "2277-Y5-R2FR-WKB-carrier-transport-or-q-zero-selection-gate.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2276_0_primary",
            "next_target": "2277-Y5-R2FR-WKB-carrier-transport-or-q-zero-selection-gate.md",
            "script": "scripts/Y5_R2FR_WKB_carrier_transport_or_q_zero_selection_gate_2277.py",
            "objective": "derive eikonal/transport equations for the carrier weights from A_MTS and test whether they select q=0 or produce a finite q_R residual source",
            "selection_status": "selected",
            "success_condition": "parent WKB transport yields q=0 in local vacuum, or a source-backed q_R residual equation with all missing scale/readout inputs tracked as nonclaim",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_permission": OUTPUTS["permission"],
        "queue_weight_contract": OUTPUTS["weight_contract"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["decision"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for downstream WKB transport and q-selection audits",
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
                if "gate_pass" in row and row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_text = read_text(OUT / "P8_Y5_BRR545_2275_VALIDATION.csv")
    prior_ok = "VAL2275_OVERALL" in prior_text and "PASS" in prior_text

    permission = permission_rows()
    wkb = wkb_derivation_rows()
    no_go = scalar_no_go_rows()
    contract = weight_contract_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()

    conditional_permission = any(row["answer"] == "YES_AS_ASYMPTOTIC_WKB_STRUCTURE" for row in permission)
    wkb_covariance = any("sum_I (a_I^2/(2 epsilon^2))" in row["formula"] for row in wkb)
    residual_tracked = any(row["step_id"] == "WKB2276_4_residual_size" for row in wkb)
    single_mode_blocked = any(row["case_id"] == "SNG2276_0_single_mode" and row["verdict"].startswith("INSUFFICIENT") for row in no_go)
    multimode_not_nogo = any(row["case_id"] == "SNG2276_2_multimode_scalar" and row["verdict"] == "NOT_A_NO_GO_BUT_NOT_PARENT_SIGNED" for row in no_go)
    contract_missing = all(row["valid_for_claim"] is False and row["current_status"].startswith("MISSING") for row in contract)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusal)
    parent_claim_blocked = any(row["claim_id"] == "CG2276_1_parent_signed_inventory" and row["gate_pass"] is False for row in claims)
    local_claim_blocked = any(row["claim_id"] == "CG2276_3_local_GR" and row["gate_pass"] is False for row in claims)
    conditional_not_promoted = any(row["claim_id"] == "CG2276_0_conditional_multimode_permission" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2276_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2276*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2276_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2276_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2276_2_prior_validation", prior_ok, "2275 validation passes"),
        ("VAL2276_3_conditional_permission", conditional_permission, "scalar multimode WKB permission recorded"),
        ("VAL2276_4_wkb_covariance", wkb_covariance, "WKB smoothed covariance recovers carrier inventory"),
        ("VAL2276_5_residual_tracked", residual_tracked, "WKB amplitude/smoothing residual tracked"),
        ("VAL2276_6_single_mode_blocked", single_mode_blocked, "single-mode scalar insufficiency recorded"),
        ("VAL2276_7_multimode_not_nogo", multimode_not_nogo, "multimode scalar route is not declared impossible"),
        ("VAL2276_8_contract_missing", contract_missing, "eikonal/transport/smoothing/q-selection contract remains missing"),
        ("VAL2276_9_refusal_blocks", refusal_blocks, "refusal runner blocks parent/local-GR claims"),
        ("VAL2276_10_parent_claim_blocked", parent_claim_blocked, "parent-signed inventory claim remains blocked"),
        ("VAL2276_11_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2276_12_conditional_not_promoted", conditional_not_promoted, "conditional permission is not promoted to claim-grade"),
        ("VAL2276_13_next_selected", next_selected, "2277 target selected"),
        ("VAL2276_14_csv_parse", csvs_parse, "all generated 2276 CSVs parse"),
        ("VAL2276_15_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2276_16_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2276_17_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2276_18_formalization_no_2276", formalization_clean, "formalization-workbench has no 2276 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2276_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2276 keeps scalar multimode permission conditionally open via WKB smoothing, rejects strict single-mode scalar as insufficient, blocks local-GR claims, and selects 2277",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    permission = permission_rows()
    wkb = wkb_derivation_rows()
    no_go = scalar_no_go_rows()
    contract = weight_contract_rows()
    qr = qr_route_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2276 - Y5/R2FR Parent Multimode Permission Or Scalar-Only No-Go",
        "",
        "## Verdict",
        "",
        "This checkpoint is a relief, but not a free pass. A scalar-valued `psi` is not automatically limited to one carrier. A high-frequency multimode scalar ansatz `psi=sum_I a_I cos(S_I/epsilon+theta_I)` produces, after smoothing, the same carrier covariance inventory needed in 2275: `C_mn=sum_I W_I k_I,m k_I,n + R_mn`.",
        "",
        "So the strict scalar-only no-go is avoided if MTS allows a WKB/multiphase reading of `psi`. But the parent action has not yet derived the eikonal equations, weight transport, smoothing kernel, or q-zero selection. Local GR therefore remains blocked, but the route is alive and sharper.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Multimode Permission Audit",
        table(["audit_id", "question", "answer", "reason", "claim_ceiling", "valid_for_claim"], permission),
        "",
        "## WKB Covariance Derivation",
        table(["step_id", "object", "formula", "derivation", "status", "valid_for_claim"], wkb),
        "",
        "## Scalar-Only No-Go Ledger",
        table(["case_id", "case", "rank_capacity", "q_capacity", "verdict", "valid_for_claim"], no_go),
        "",
        "## Weight Dynamics Contract",
        table(["contract_id", "requirement", "why_needed", "current_status", "valid_for_claim"], contract),
        "",
        "## q_R Route Consequence",
        table(["route_id", "route", "condition", "consequence", "status", "valid_for_claim"], qr),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is a better place than a scalar-only dead end. The carrier idea can be interpreted as the smoothed covariance of multiple local phases of one scalar field. The price is now exact and useful: derive WKB transport from `A_MTS[psi]`, then show whether the transport selects `q=0` in local vacuum or produces a bounded finite `q_R` residual.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["permission"], permission_rows())
    write_csv(OUTPUTS["wkb_derivation"], wkb_derivation_rows())
    write_csv(OUTPUTS["scalar_no_go"], scalar_no_go_rows())
    write_csv(OUTPUTS["weight_contract"], weight_contract_rows())
    write_csv(OUTPUTS["qr_route"], qr_route_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["permission"], COPY_TARGETS["queue_permission"])
    shutil.copyfile(OUTPUTS["weight_contract"], COPY_TARGETS["queue_weight_contract"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
