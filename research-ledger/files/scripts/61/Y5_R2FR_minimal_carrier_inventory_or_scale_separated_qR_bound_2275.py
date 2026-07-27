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

BRANCH_ID = "MTS_R2FR_MINIMAL_CARRIER_INVENTORY_OR_SCALE_QR_BOUND_2275"
DOC = ROOT / "2275-Y5-R2FR-minimal-carrier-inventory-or-scale-separated-qR-bound.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2275_00_2274_doc",
        "source_key": "2274_doc",
        "source_path": ROOT / "2274-Y5-R2FR-curl-zero-mechanism-or-Hodge-residual-bound.md",
        "needles": ["CZM2274_1_carrier_aligned_scaling", "SSB2274_1_hodge_residual", "NEXT2274_0_primary"],
        "role": "handoff: carrier-aligned exact mechanism and scale bound selected",
    },
    {
        "source_id": "SRC2275_01_2274_validation",
        "source_key": "2274_validation",
        "source_path": OUT / "P8_Y5_BRR545_2274_VALIDATION.csv",
        "needles": ["VAL2274_OVERALL", "PASS"],
        "role": "confirms 2274 passed before 2275 starts",
    },
    {
        "source_id": "SRC2275_02_2274_mechanisms",
        "source_key": "2274_mechanisms",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2274_CURL_ZERO_MECHANISM_TESTS.csv",
        "needles": ["CZM2274_1_carrier_aligned_scaling", "EXACT_MECHANISM_REQUIRES_UNSOURCED_CARRIER_DECOMPOSITION"],
        "role": "machine-readable carrier-aligned curl-zero mechanism",
    },
    {
        "source_id": "SRC2275_03_2274_bound",
        "source_key": "2274_bound",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2274_SCALE_SEPARATED_CURL_BOUND.csv",
        "needles": ["SSB2274_1_hodge_residual", "ell_cg/L_cg"],
        "role": "scale-separated residual bound",
    },
    {
        "source_id": "SRC2275_04_2274_qr_intake",
        "source_key": "2274_qr_intake",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2274_QR_BOUND_INPUT_LEDGER.csv",
        "needles": ["QBI2274_0_ell_cg", "MISSING_PARENT_SMOOTHING_SCALE"],
        "role": "missing q_R bound inputs",
    },
    {
        "source_id": "SRC2275_05_2271_formulas",
        "source_key": "2271_formulas",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv",
        "needles": ["PBF2271_1_q_tangent", "PBF2271_3_q_zero_channel_relation"],
        "role": "q tangent target and q=0 channel relation",
    },
    {
        "source_id": "SRC2275_06_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "L_MTS", "∂_μψ"],
        "role": "current parent action uses a scalar psi field and covariance readout",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2275_SOURCE_REGISTER.csv",
    "carrier_inventory": OUT / "P8_Y5_PARENT_QLOC_2275_MINIMAL_CARRIER_INVENTORY.csv",
    "q_lift": OUT / "P8_Y5_PARENT_QLOC_2275_CARRIER_WEIGHT_Q_LIFT.csv",
    "curl_audit": OUT / "P8_Y5_PARENT_QLOC_2275_CARRIER_CURL_AUDIT.csv",
    "sign_ledger": OUT / "P8_Y5_PARENT_QLOC_2275_LORENTZIAN_SIGN_CONE_LEDGER.csv",
    "scale_bound": OUT / "P8_Y5_PARENT_QLOC_2275_SCALE_SEPARATED_QR_BOUND_STAGING.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2275_PARENT_PERMISSION_CONTRACT.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2275_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2275_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2275_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2275_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2275_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2275_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_inventory": QUEUE / "JR2275_MINIMAL_CARRIER_INVENTORY_NONCLAIM.csv",
    "queue_contract": QUEUE / "JR2275_PARENT_PERMISSION_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_minimal_carrier_inventory_refusal_2275.csv",
    "beta_docs": BETA_DOCS / "RAB_MINIMAL_CARRIER_INVENTORY_2275_NONCLAIM.csv",
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


def carrier_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "carrier_id": "MCI2275_0_covariance_ensemble",
            "object": "phase/carrier covariance inventory",
            "formula": "C_mn=sum_I s_I W_I k_I,m k_I,n with k_I=dS_I",
            "role": "replaces arbitrary one-form deformations with exact phase gradients plus weights/amplitudes",
            "minimum_needed": "at least one t-dominant carrier and one r-dominant carrier for the local radial block",
            "parent_status": "NOT_IN_CURRENT_SCALAR_ACTION_AS_SIGNED_INVENTORY",
            "valid_for_claim": False,
        },
        {
            "carrier_id": "MCI2275_1_time_carrier",
            "object": "t-channel carrier",
            "formula": "C_tt=s_T W_T Omega_T^2",
            "role": "supplies independent variation of the temporal covariance channel",
            "minimum_needed": "W_T>0, Omega_T nonzero, sign convention s_T sourced",
            "parent_status": "UNSOURCED",
            "valid_for_claim": False,
        },
        {
            "carrier_id": "MCI2275_2_radial_carrier",
            "object": "r-channel carrier",
            "formula": "C_rr=s_R W_R K_R^2",
            "role": "supplies independent variation of the radial covariance channel",
            "minimum_needed": "W_R>0, K_R nonzero, sign convention s_R sourced",
            "parent_status": "UNSOURCED",
            "valid_for_claim": False,
        },
        {
            "carrier_id": "MCI2275_3_offdiag_guard",
            "object": "off-diagonal silence",
            "formula": "C_tr=sum_I s_I W_I k_I,t k_I,r=0",
            "role": "keeps the static local radial block diagonal",
            "minimum_needed": "phase pairing, parity averaging, or orthogonal carrier design",
            "parent_status": "UNSOURCED",
            "valid_for_claim": False,
        },
    ]


def q_lift_rows() -> list[dict[str, Any]]:
    return [
        {
            "lift_id": "CWQ2275_0_target",
            "target": "q tangent at fixed Phi",
            "formula": "deltaC_tt=-(A/2)deltaq; deltaC_rr=(B/2)deltaq",
            "carrier_weight_lift": "deltaW_T=deltaC_tt/(s_T Omega_T^2); deltaW_R=deltaC_rr/(s_R K_R^2)",
            "curl_status": "phase gradients k_I remain exact if only W_I changes",
            "blocker": "W_I dynamics/amplitude variation are not parent-signed variables",
            "valid_for_claim": False,
        },
        {
            "lift_id": "CWQ2275_1_fractional_form",
            "target": "fractional carrier response",
            "formula": "deltaW_T/W_T=deltaC_tt/C_tt; deltaW_R/W_R=deltaC_rr/C_rr",
            "carrier_weight_lift": "for nonzero background channels, q is a relative transfer between temporal and radial carrier weights",
            "curl_status": "no new one-form curl if implemented as statistical/phase-weight modulation",
            "blocker": "finite positivity cone and parent conservation law for W_I are missing",
            "valid_for_claim": False,
        },
        {
            "lift_id": "CWQ2275_2_q_zero_background",
            "target": "q=0 relation",
            "formula": "(1-C_tt)(1+C_rr)=1",
            "carrier_weight_lift": "requires background weights satisfying C_rr=C_tt/(1-C_tt)",
            "curl_status": "algebraic relation can be represented by weights if signs/cones permit",
            "blocker": "no parent theorem selects this weight relation in local vacuum",
            "valid_for_claim": False,
        },
    ]


def curl_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CCA2275_0_fixed_phase",
            "route": "fixed exact phase gradients",
            "curl_check": "dk_I=d^2S_I=0",
            "result": "CURL_SAFE_FOR_PHASES",
            "residual": "weight/amplitude gradients can still enter the microscopic scalar derivative unless W_I is a true ensemble variable",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CCA2275_1_real_scalar_amplitude",
            "route": "real scalar amplitude modulation",
            "curl_check": "psi_I=a_I cos(S_I/epsilon) gives dpsi_I terms from da_I and dS_I",
            "result": "WKB_ONLY_NOT_EXACT",
            "residual": "amplitude-gradient covariance terms scale like |da|/(|a k|)",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CCA2275_2_phase_pairing",
            "route": "paired phases/parity average",
            "curl_check": "opposite phases or parity-related carriers can cancel C_tr and fast oscillatory cross terms after smoothing",
            "result": "POSSIBLE_AVERAGE_SILENCE",
            "residual": "requires explicit smoothing kernel and phase distribution",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CCA2275_3_single_scalar_no_go",
            "route": "single static scalar",
            "curl_check": "one scalar cannot independently tune C_tt(r), C_rr(r), and C_tr=0 over a finite radial cell without extra structure",
            "result": "SINGLE_SCALAR_ROUTE_INSUFFICIENT",
            "residual": "needs ensemble/multimode interpretation or scalar-only no-go must be accepted",
            "valid_for_claim": False,
        },
    ]


def sign_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "sign_id": "LSC2275_0_positive_weights",
            "issue": "weight positivity",
            "condition": "W_I>=0 and W_I+deltaW_I>=0 for finite variations",
            "impact": "small tangent variations are allowed only inside the covariance cone",
            "status": "CONE_GUARD_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "sign_id": "LSC2275_1_lorentzian_signature",
            "issue": "signature source",
            "condition": "eta_mn+C_mn must keep Lorentzian signature",
            "impact": "carrier weights cannot be chosen freely if they flip A or B signs",
            "status": "SIGNATURE_GUARD_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "sign_id": "LSC2275_2_deltaC_tt_negative",
            "issue": "negative temporal q tangent",
            "condition": "deltaC_tt=-(A/2)deltaq may require decreasing W_T for positive s_T Omega_T^2",
            "impact": "fine for infinitesimal tangents if W_T>0, not automatically fine for finite residuals",
            "status": "FINITE_CONE_MARGIN_MISSING",
            "valid_for_claim": False,
        },
    ]


def scale_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SQR2275_0_wkb_amplitude",
            "quantity": "amplitude-gradient residual",
            "bound": "epsilon_amp=max_I |partial a_I|/(|a_I k_I|)",
            "interpretation": "if carrier amplitudes vary slowly relative to phase gradients, the weight-lift behaves approximately curl-safe after smoothing",
            "inputs_needed": "carrier wavelengths/frequencies, amplitude profiles, smoothing kernel",
            "status": "INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SQR2275_1_combined_residual",
            "quantity": "combined exactness/smoothing residual",
            "bound": "epsilon_total <= K2 ell_cg/L_cg + K_amp epsilon_amp",
            "interpretation": "combines 2274 Hodge residual with WKB amplitude leakage",
            "inputs_needed": "K2, ell_cg, L_cg, K_amp, epsilon_amp",
            "status": "INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SQR2275_2_qR_bound",
            "quantity": "finite q_R residual",
            "bound": "|q_R| <= Kq epsilon_total |deltaq_alg|",
            "interpretation": "the local branch becomes testable once Kq and arena tolerances are sourced",
            "inputs_needed": "Kq, local PPN/clock/orbital/R10 tolerances, no-cancellation guard",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PPC2275_0_multicarrier_permission",
            "requirement": "parent psi sector must allow a carrier/phase ensemble or multimode decomposition, not only an undifferentiated single scalar",
            "current_evidence": "core action states scalar psi and smoothed covariance, but does not formalize carrier weights W_I",
            "needed_for_claim": "yes",
            "status": "UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PPC2275_1_weight_dynamics",
            "requirement": "W_I must have parent dynamics or emerge from averaged psi amplitudes with controlled residuals",
            "current_evidence": "no sourced W_I equation or amplitude-phase averaging theorem",
            "needed_for_claim": "yes",
            "status": "UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PPC2275_2_q_zero_selection",
            "requirement": "local vacuum must select C_rr=C_tt/(1-C_tt) or suppress deviations by finite q_R bound",
            "current_evidence": "q=0 relation known, selection theorem missing",
            "needed_for_claim": "yes",
            "status": "UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PPC2275_3_smoothing_kernel",
            "requirement": "kernel/phase average must kill off-diagonal and oscillatory residual channels",
            "current_evidence": "smoothing asserted, not mathematically specified",
            "needed_for_claim": "yes",
            "status": "UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2275_0_carrier_claim",
            "attempted_claim": "The carrier inventory derives the q tangent from the current parent action.",
            "runner_result": "BLOCKED",
            "blocked_by": "multicarrier permission, weight dynamics, and smoothing kernel are unsigned",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2275_1_exact_gr_claim",
            "attempted_claim": "The local branch now derives GR exactly.",
            "runner_result": "BLOCKED",
            "blocked_by": "q=0 weight relation is represented but not selected by a parent theorem",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2275_2_bound_claim",
            "attempted_claim": "The scale-separated q_R residual is within local bounds.",
            "runner_result": "BLOCKED",
            "blocked_by": "epsilon_amp, ell_cg/L_cg, Kq, and arena tolerance remain missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2275_0_algebraic_inventory",
            "claim": "a two-channel carrier inventory can represent the q tangent algebraically",
            "gate_pass": True,
            "reason": "deltaW_T and deltaW_R can match deltaC_tt and deltaC_rr if carrier denominators and cone margins exist",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2275_1_parent_permission",
            "claim": "the current parent action supplies that carrier inventory",
            "gate_pass": False,
            "reason": "carrier weights, signs, phase averaging, and multimode decomposition are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2275_2_exact_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "q=0 relation represented but not dynamically selected",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2275_3_finite_qR_bound",
            "claim": "finite q_R residual can be scored",
            "gate_pass": False,
            "reason": "scale/readout/tolerance inputs are still missing",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2275_0_gain",
            "decision": "MINIMAL_CARRIER_SPLIT_REPRESENTS_Q_TANGENT",
            "reason": "The q tangent can be written as temporal/radial carrier weight transfer without introducing curl in fixed exact phases.",
            "next_action": "Treat as a promising parent-contract target, not a claim.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2275_1_blocker",
            "decision": "CURRENT_PARENT_ACTION_DOES_NOT_SIGN_THE_INVENTORY",
            "reason": "The corpus has scalar psi and smoothed covariance, but not a formal W_I carrier phase ensemble with dynamics.",
            "next_action": "Audit whether psi may be interpreted as a multimode/phase ensemble or prove scalar-only insufficiency.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2275_2_backstop",
            "decision": "SCALE_QR_BOUND_STAGED",
            "reason": "If the carrier inventory becomes WKB-only, the leakage enters epsilon_total and can be bounded later.",
            "next_action": "Source epsilon_amp, ell_cg/L_cg, Kq, and local arena tolerances.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2275_3_next",
            "decision": "PARENT_MULTIMODE_PERMISSION_OR_SCALAR_NO_GO_NEXT",
            "reason": "The next decisive fork is whether MTS permits the carrier ensemble as derived structure.",
            "next_action": "2276-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2275_0_primary",
            "next_target": "2276-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md",
            "script": "scripts/Y5_R2FR_parent_multimode_permission_or_scalar_only_no_go_2276.py",
            "objective": "decide whether the parent psi action permits the carrier/phase ensemble needed for the curl-free q lift, or prove the scalar-only route insufficient and keep q_R residual-bound only",
            "selection_status": "selected",
            "success_condition": "parent-signed multimode/ensemble permission with weight dynamics, or explicit scalar-only no-go plus residual-bound route",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_inventory": OUTPUTS["carrier_inventory"],
        "queue_contract": OUTPUTS["parent_contract"],
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
            "reason": "branch copy for downstream parent-permission and scalar-only audits",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2274_VALIDATION.csv")
    prior_ok = "VAL2274_OVERALL" in prior_text and "PASS" in prior_text

    inventory = carrier_inventory_rows()
    q_lift = q_lift_rows()
    curl = curl_audit_rows()
    signs = sign_ledger_rows()
    scale = scale_bound_rows()
    contract = parent_contract_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()

    inventory_has_two_channels = any(row["carrier_id"] == "MCI2275_1_time_carrier" for row in inventory) and any(
        row["carrier_id"] == "MCI2275_2_radial_carrier" for row in inventory
    )
    q_lift_formula = any("deltaW_T=deltaC_tt" in row["carrier_weight_lift"] for row in q_lift)
    curl_guard = any(row["result"] == "SINGLE_SCALAR_ROUTE_INSUFFICIENT" for row in curl)
    sign_guard = all(row["valid_for_claim"] is False for row in signs)
    scale_template = any("epsilon_total" in row["bound"] for row in scale)
    parent_unsigned = all(row["status"] == "UNSIGNED" and row["valid_for_claim"] is False for row in contract)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    parent_claim_blocked = any(row["claim_id"] == "CG2275_1_parent_permission" and row["gate_pass"] is False for row in claims)
    local_claim_blocked = any(row["claim_id"] == "CG2275_2_exact_local_GR" and row["gate_pass"] is False for row in claims)
    algebraic_not_promoted = any(row["claim_id"] == "CG2275_0_algebraic_inventory" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2275_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2275*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2275_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2275_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2275_2_prior_validation", prior_ok, "2274 validation passes"),
        ("VAL2275_3_two_channel_inventory", inventory_has_two_channels, "minimal t/r carrier inventory written"),
        ("VAL2275_4_q_lift_formula", q_lift_formula, "q tangent carrier-weight lift formula written"),
        ("VAL2275_5_curl_guard", curl_guard, "single-scalar insufficiency guard recorded"),
        ("VAL2275_6_sign_guard", sign_guard, "Lorentzian/sign cone guard rows remain nonclaim"),
        ("VAL2275_7_scale_template", scale_template, "scale-separated q_R bound staging written"),
        ("VAL2275_8_parent_unsigned", parent_unsigned, "parent permission contract remains unsigned"),
        ("VAL2275_9_refusal_blocks", refusal_blocks, "refusal runner blocks carrier/local-GR claims"),
        ("VAL2275_10_parent_claim_blocked", parent_claim_blocked, "parent permission claim remains blocked"),
        ("VAL2275_11_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2275_12_algebraic_not_promoted", algebraic_not_promoted, "algebraic inventory is not promoted to claim-grade"),
        ("VAL2275_13_next_selected", next_selected, "2276 target selected"),
        ("VAL2275_14_csv_parse", csvs_parse, "all generated 2275 CSVs parse"),
        ("VAL2275_15_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2275_16_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2275_17_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2275_18_formalization_no_2275", formalization_clean, "formalization-workbench has no 2275 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2275_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2275 writes a minimal t/r carrier inventory that represents the q tangent algebraically, blocks parent/local-GR claims, stages WKB/scale q_R bounds, and selects 2276",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    inventory = carrier_inventory_rows()
    q_lift = q_lift_rows()
    curl = curl_audit_rows()
    signs = sign_ledger_rows()
    scale = scale_bound_rows()
    contract = parent_contract_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2275 - Y5/R2FR Minimal Carrier Inventory Or Scale-Separated q_R Bound",
        "",
        "## Verdict",
        "",
        "This is the most constructive coupling step so far. A minimal temporal/radial carrier inventory can represent the q tangent as a transfer of carrier weights: `deltaW_T=deltaC_tt/(s_T Omega_T^2)` and `deltaW_R=deltaC_rr/(s_R K_R^2)`. If the phases are fixed exact gradients `k_I=dS_I`, the curl problem moves out of the one-form sector.",
        "",
        "But this is not yet a parent derivation. The current corpus gives a scalar `psi` action plus smoothed covariance; it does not yet sign a carrier/phase ensemble with weights `W_I`, weight dynamics, Lorentzian cone margins, or a smoothing theorem. So the carrier split is promising structure, not a claim.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Minimal Carrier Inventory",
        table(["carrier_id", "object", "formula", "role", "minimum_needed", "parent_status", "valid_for_claim"], inventory),
        "",
        "## Carrier-Weight q Lift",
        table(["lift_id", "target", "formula", "carrier_weight_lift", "curl_status", "blocker", "valid_for_claim"], q_lift),
        "",
        "## Carrier Curl Audit",
        table(["audit_id", "route", "curl_check", "result", "residual", "valid_for_claim"], curl),
        "",
        "## Lorentzian Sign / Cone Ledger",
        table(["sign_id", "issue", "condition", "impact", "status", "valid_for_claim"], signs),
        "",
        "## Scale-Separated q_R Bound Staging",
        table(["bound_id", "quantity", "bound", "interpretation", "inputs_needed", "status", "valid_for_claim"], scale),
        "",
        "## Parent Permission Contract",
        table(["contract_id", "requirement", "current_evidence", "needed_for_claim", "status", "valid_for_claim"], contract),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
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
        "The honest state is better than before. We now have a plausible structural answer to the coupling/curl gap: q can be an exchange between temporal and radial carrier weights instead of a curled deformation of one-forms. The next fork is brutal and useful: either the parent psi action really permits this multimode carrier picture, or a strict scalar-only reading cannot derive the local branch and we must fall back to bounded q_R residuals.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["carrier_inventory"], carrier_inventory_rows())
    write_csv(OUTPUTS["q_lift"], q_lift_rows())
    write_csv(OUTPUTS["curl_audit"], curl_audit_rows())
    write_csv(OUTPUTS["sign_ledger"], sign_ledger_rows())
    write_csv(OUTPUTS["scale_bound"], scale_bound_rows())
    write_csv(OUTPUTS["parent_contract"], parent_contract_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["carrier_inventory"], COPY_TARGETS["queue_inventory"])
    shutil.copyfile(OUTPUTS["parent_contract"], COPY_TARGETS["queue_contract"])
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
