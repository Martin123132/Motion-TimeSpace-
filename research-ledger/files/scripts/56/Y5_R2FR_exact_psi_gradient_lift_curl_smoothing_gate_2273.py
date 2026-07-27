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

BRANCH_ID = "MTS_R2FR_EXACT_PSI_GRADIENT_LIFT_CURL_SMOOTHING_GATE_2273"
DOC = ROOT / "2273-Y5-R2FR-exact-psi-gradient-lift-curl-smoothing-gate.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2273_00_2272_doc",
        "source_key": "2272_doc",
        "source_path": ROOT / "2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md",
        "needles": ["ACL2272_1_right_inverse", "FIL2272_0_exactness", "NEXT2272_0_primary"],
        "role": "handoff: algebraic covariance lift exists conditionally; exactness gate selected",
    },
    {
        "source_id": "SRC2273_01_2272_validation",
        "source_key": "2272_validation",
        "source_path": OUT / "P8_Y5_BRR545_2272_VALIDATION.csv",
        "needles": ["VAL2272_OVERALL", "PASS"],
        "role": "confirms 2272 passed before 2273 starts",
    },
    {
        "source_id": "SRC2273_02_2272_algebraic_lift",
        "source_key": "2272_algebraic_lift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2272_ALGEBRAIC_COVARIANCE_LIFT.csv",
        "needles": ["ACL2272_1_right_inverse", "ALGEBRAIC_COVARIANCE_LIFT_EXISTS_CONDITIONALLY"],
        "role": "machine-readable covariance right-inverse formula",
    },
    {
        "source_id": "SRC2273_03_2272_q_lift",
        "source_key": "2272_q_lift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2272_Q_TANGENT_LIFT_ATTEMPT.csv",
        "needles": ["QTL2272_0_target", "TARGET_TANGENT_LOCKED_LIFT_CONDITIONAL"],
        "role": "q tangent target and conditional lift candidate",
    },
    {
        "source_id": "SRC2273_04_2272_integrability",
        "source_key": "2272_integrability",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2272_FIELD_INTEGRABILITY_LEDGER.csv",
        "needles": ["FIL2272_0_exactness", "FIL2272_1_smoothing_inverse", "UNSIGNED"],
        "role": "exactness/smoothing gates requiring attempted closure",
    },
    {
        "source_id": "SRC2273_05_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "L_MTS", "∂_μψ"],
        "role": "parent scalar psi action and gradient-covariance definition",
    },
    {
        "source_id": "SRC2273_06_motion_action",
        "source_key": "motion_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["g_{μν}(x)", "∂_μ ψ(x) ∂_ν ψ(x)", "correct Lorentzian signature"],
        "role": "macro smoothing/readout statement for emergent metric",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2273_SOURCE_REGISTER.csv",
    "exact_lift_equations": OUT / "P8_Y5_PARENT_QLOC_2273_EXACT_LIFT_EQUATIONS.csv",
    "curl_obstruction": OUT / "P8_Y5_PARENT_QLOC_2273_CURL_OBSTRUCTION_DERIVATION.csv",
    "pointwise_vs_field": OUT / "P8_Y5_PARENT_QLOC_2273_POINTWISE_VS_FIELD_LEDGER.csv",
    "smoothing_projection": OUT / "P8_Y5_PARENT_QLOC_2273_SMOOTHING_HODGE_PROJECTION_GATE.csv",
    "qR_consequence": OUT / "P8_Y5_PARENT_QLOC_2273_QR_CONSEQUENCE_LEDGER.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2273_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2273_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2273_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2273_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2273_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2273_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_curl": QUEUE / "JR2273_EXACT_PSI_GRADIENT_CURL_GATE_NONCLAIM.csv",
    "queue_projection": QUEUE / "JR2273_SMOOTHING_HODGE_PROJECTION_GATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_exact_psi_gradient_lift_refusal_2273.csv",
    "beta_docs": BETA_DOCS / "RAB_EXACT_PSI_GRADIENT_LIFT_2273_NONCLAIM.csv",
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


def exact_lift_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "equation_id": "ELE2273_0_parent_readout",
            "object": "exact field-level covariance variation",
            "equation": "deltaC_mn=<partial_m zeta_A partial_n psi_A + partial_m psi_A partial_n zeta_A>_smooth",
            "meaning": "A lawful lift of deltaC must be generated by scalar perturbations zeta_A=delta psi_A, not just arbitrary one-form perturbations.",
            "status": "FIELD_LIFT_TARGET",
            "valid_for_claim": False,
        },
        {
            "equation_id": "ELE2273_1_algebraic_candidate",
            "object": "candidate one-form lift",
            "equation": "delta u_A,m=M_m^n u_A,n with M=(1/2) deltaC C^{-1}",
            "meaning": "This is the 2272 right inverse written as a one-form deformation of each active carrier.",
            "status": "CANDIDATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "equation_id": "ELE2273_2_exactness_condition",
            "object": "curl-free condition",
            "equation": "Omega_A,mn=partial_m(delta u_A,n)-partial_n(delta u_A,m)=0",
            "meaning": "Because delta u_A must equal d zeta_A locally, its exterior derivative must vanish.",
            "status": "NECESSARY_FIELD_LIFT_CONDITION",
            "valid_for_claim": False,
        },
        {
            "equation_id": "ELE2273_3_obstruction_expansion",
            "object": "curl obstruction for algebraic candidate",
            "equation": "Omega_A,mn=partial_m(M_n^r u_A,r)-partial_n(M_m^r u_A,r)",
            "meaning": "Since u_A=d psi_A has du_A=0, this expands into derivative-of-M terms plus Hessian-of-psi terms; it is not generically zero.",
            "status": "DERIVED_OBSTRUCTION",
            "valid_for_claim": False,
        },
    ]


def curl_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "COD2273_0_general",
            "claim_tested": "The 2272 algebraic lift is automatically a psi-gradient lift.",
            "derivation": "Take delta u_A=M u_A. Exactness requires d(delta u_A)=d(M u_A)=0. Because du_A=0, the obstruction is dM wedge u_A plus the index-mixing Hessian terms M_n^r partial_m u_A,r - M_m^r partial_n u_A,r.",
            "result": "FAILS_GENERALLY",
            "missing_zero_mechanism": "Need M constant/proportional in the carrier frame, affine local psi jets, compensating exact projection, or a parent theorem annihilating the curl residual after smoothing.",
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COD2273_1_q_profile",
            "claim_tested": "The q tangent profile can vary with radius while remaining automatically exact.",
            "derivation": "For q-direction, M_q depends on deltaC_q C^{-1}; if Phi(r), deltaq(r), or C(r) vary, then partial_r M_q terms enter Omega_A,mn.",
            "result": "RADIAL_PROFILE_INTRODUCES_CURL_RISK",
            "missing_zero_mechanism": "Need sourced curl-zero carrier ansatz or explicit smoothing projection residual bound.",
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COD2273_2_static_scalar_warning",
            "claim_tested": "A single static scalar psi(t,r) can freely tune C_tt(r) and C_rr(r).",
            "derivation": "If psi=-E(r)t+chi(r), exactness of dpsi ties time/radial dependence; if psi=-E t+chi(r) with E constant, C_tt cannot carry an arbitrary radial potential. More carrier structure or averaging is needed.",
            "result": "SINGLE_SCALAR_STATIC_ROUTE_TOO_WEAK",
            "missing_zero_mechanism": "Need ensemble/carrier inventory or time-dependent microstructure with averaged static covariance.",
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COD2273_3_pointwise_exception",
            "claim_tested": "The lift can be represented at one point.",
            "derivation": "At a single point, arbitrary delta u_A one-forms can be realized as first jets of scalars zeta_A. This proves a pointwise jet lift, not a finite-neighborhood action variation.",
            "result": "POINTWISE_JET_OK_FIELD_ACTION_UNPROVED",
            "missing_zero_mechanism": "Need finite-neighborhood integrability and boundary conditions for a Hessian/source calculation.",
            "claim_allowed": False,
        },
    ]


def pointwise_vs_field_rows() -> list[dict[str, Any]]:
    return [
        {
            "ledger_id": "PVF2273_0_pointwise",
            "level": "pointwise 1-jet",
            "what_is_true": "A covariance tangent can be matched at x0 by choosing scalar perturbations with prescribed first derivatives at x0.",
            "what_is_not_true": "This does not define zeta_A on a neighborhood or supply A_MTS second variation.",
            "use_in_theory": "Useful for local algebra and variable mapping only.",
            "claim_allowed": False,
        },
        {
            "ledger_id": "PVF2273_1_cell",
            "level": "coarse cell / finite neighborhood",
            "what_is_true": "A lift is possible only if the chosen one-form perturbations satisfy curl-free compatibility or are replaced by exact projections.",
            "what_is_not_true": "The current corpus does not prove that the q tangent lies in the range of the exact-gradient smoothing map.",
            "use_in_theory": "This is the level needed for local GR reduction and q_R Hessian/source scoring.",
            "claim_allowed": False,
        },
        {
            "ledger_id": "PVF2273_2_action",
            "level": "parent action Hessian",
            "what_is_true": "A claim-grade q_R requires M_R^2=<delta_q psi,H_psi delta_q psi> and j_R=<delta_q psi,source>.",
            "what_is_not_true": "No exact delta_q psi and no H_psi pullback have been supplied.",
            "use_in_theory": "Defines the missing bridge between MTS micro-action and GR-local q suppression.",
            "claim_allowed": False,
        },
    ]


def smoothing_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "SHP2273_0_hodge_projection",
            "object": "exact projection of algebraic one-form",
            "proposal": "Given alpha_A=delta u_A^alg, define zeta_A by minimizing ||d zeta_A-alpha_A||^2 on the coarse cell; residual rho_A=alpha_A-d zeta_A contains the coexact/curl part.",
            "required_inputs": "cell geometry, smoothing kernel, boundary conditions, inner product measure, carrier inventory",
            "pass_condition": "The smoothed covariance contribution of rho_A is zero or bounded below local-test tolerance.",
            "status": "PROJECTION_GATE_DEFINED_NOT_SOURCED",
            "valid_for_claim": False,
        },
        {
            "projection_id": "SHP2273_1_residual_bound",
            "object": "curl residual bound",
            "proposal": "epsilon_curl=||rho||/||alpha|| and deltaC_res=<rho_A u_A + u_A rho_A>_smooth",
            "required_inputs": "norm, carrier amplitudes, smoothing scale, local arena tolerances",
            "pass_condition": "epsilon_curl and induced q_R residual are sourced and below PPN/clock/orbital bounds.",
            "status": "BOUND_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "projection_id": "SHP2273_2_kernel_annihilation",
            "object": "smoothing annihilates curl sector",
            "proposal": "A parent theorem could show <rho_A u_A + u_A rho_A>_smooth=0 for the q channel.",
            "required_inputs": "explicit kernel symmetry, carrier phase averaging, boundary cancellation theorem",
            "pass_condition": "parent-signed zero theorem, not an assumption.",
            "status": "ZERO_THEOREM_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def qR_consequence_rows() -> list[dict[str, Any]]:
    return [
        {
            "consequence_id": "QRC2273_0_exact_route",
            "route": "exact local GR",
            "condition": "Omega_A,mn=0 for the q lift and smoothing/projection terms do not source q.",
            "consequence": "Then q=0 protection can be pursued as a real parent theorem.",
            "current_status": "not established",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "QRC2273_1_residual_route",
            "route": "finite q_R",
            "condition": "Curl residual survives but can be projected into j_R and M_R^2.",
            "consequence": "Then local tests require q_R=j_R/M_R^2 plus induced PPN residual vector.",
            "current_status": "template only",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "QRC2273_2_fail_route",
            "route": "local branch demotion",
            "condition": "No exact lift and no bounded residual profile can be sourced.",
            "consequence": "Then the q-suppressed local-GR route must be demoted to closure-only, not a derived limit.",
            "current_status": "not reached; 2274 should test mechanisms",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2273_0_exact_lift_claim",
            "attempted_claim": "The algebraic covariance lift is a lawful psi-gradient lift.",
            "runner_result": "BLOCKED",
            "blocked_by": "nonzero generic curl obstruction Omega_A,mn; smoothing/projection theorem missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2273_1_local_gr_claim",
            "attempted_claim": "The local branch now derives GR.",
            "runner_result": "BLOCKED",
            "blocked_by": "pointwise lift is not a finite-neighborhood action variation; q=0 still unprotected",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2273_2_smoothing_zero_claim",
            "attempted_claim": "Smoothing kills the curl residual.",
            "runner_result": "BLOCKED",
            "blocked_by": "kernel, phase averaging, boundary conditions, and residual norm are missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2273_0_pointwise_lift",
            "claim": "pointwise covariance tangent has a scalar first-jet lift",
            "gate_pass": True,
            "reason": "at one point, prescribed first derivatives of zeta_A can match algebraic one-form data",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2273_1_exact_field_lift",
            "claim": "finite-neighborhood exact psi-gradient lift exists",
            "gate_pass": False,
            "reason": "curl obstruction is generically nonzero and no exactness theorem is sourced",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2273_2_smoothing_projection",
            "claim": "smoothing/projection residual is zero or bounded",
            "gate_pass": False,
            "reason": "kernel, boundary, carrier inventory, and norm are missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2273_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "q=0 protection or finite q_R bound still absent",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2273_0_gain",
            "decision": "POINTWISE_JET_LIFT_SEPARATED_FROM_FIELD_LIFT",
            "reason": "The algebraic lift is not useless: it works as first-jet data, but that is weaker than a field/action lift.",
            "next_action": "Use the pointwise lift only for mapping; do not use it as local-GR proof.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2273_1_obstruction",
            "decision": "CURL_OBSTRUCTION_IS_THE_ACTIVE_BLOCKER",
            "reason": "Omega_A,mn=d(deltau_A) is the concrete quantity blocking the promotion from covariance algebra to parent psi fields.",
            "next_action": "Try to derive a curl-zero mechanism or bound the Hodge residual.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2273_2_no_claim",
            "decision": "LOCAL_GR_STILL_NONCLAIM",
            "reason": "No smoothing kernel, exact projection, residual bound, or q_R Hessian/source exists.",
            "next_action": "Keep all local arenas blocked.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2273_3_next",
            "decision": "CURL_ZERO_MECHANISM_OR_HODGE_BOUND_NEXT",
            "reason": "This is the narrowest remaining route to make the coupling mathematically lawful.",
            "next_action": "2274-Y5-R2FR-curl-zero-mechanism-or-Hodge-residual-bound.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2273_0_primary",
            "next_target": "2274-Y5-R2FR-curl-zero-mechanism-or-Hodge-residual-bound.md",
            "script": "scripts/Y5_R2FR_curl_zero_mechanism_or_Hodge_residual_bound_2274.py",
            "objective": "attempt a parent mechanism that makes the q-lift curl-free, or define a source-backed Hodge residual bound feeding finite q_R",
            "selection_status": "selected",
            "success_condition": "either Omega_A,mn=0 is derived under explicit parent conditions, or residual rho_A is converted into bounded q_R inputs without claiming local GR",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_curl": OUTPUTS["curl_obstruction"],
        "queue_projection": OUTPUTS["smoothing_projection"],
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
            "reason": "branch copy for downstream exact-lift and finite-residual audits",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2272_VALIDATION.csv")
    prior_ok = "VAL2272_OVERALL" in prior_text and "PASS" in prior_text

    equations = exact_lift_equation_rows()
    curl_rows = curl_obstruction_rows()
    pointwise_rows = pointwise_vs_field_rows()
    projection_rows = smoothing_projection_rows()
    qr_rows = qR_consequence_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()

    exact_formula_ok = any("Omega_A,mn" in row["equation"] and "partial_m(delta u_A,n)" in row["equation"] for row in equations)
    curl_obstruction_ok = any(row["result"] == "FAILS_GENERALLY" for row in curl_rows)
    pointwise_separated = any(row["level"] == "pointwise 1-jet" for row in pointwise_rows) and any(
        row["level"] == "parent action Hessian" for row in pointwise_rows
    )
    projection_nonclaim = all(row["valid_for_claim"] is False for row in projection_rows)
    qr_nonclaim = all(row["valid_for_claim"] is False for row in qr_rows)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusal)
    local_claim_blocked = any(row["claim_id"] == "CG2273_3_local_GR" and row["gate_pass"] is False for row in claims)
    pointwise_not_promoted = any(row["claim_id"] == "CG2273_0_pointwise_lift" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2273_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2273*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2273_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2273_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2273_2_prior_validation", prior_ok, "2272 validation passes"),
        ("VAL2273_3_exact_formula", exact_formula_ok, "curl-free exactness equation written"),
        ("VAL2273_4_curl_obstruction", curl_obstruction_ok, "generic curl obstruction derived"),
        ("VAL2273_5_pointwise_separated", pointwise_separated, "pointwise lift separated from field/action lift"),
        ("VAL2273_6_projection_nonclaim", projection_nonclaim, "smoothing/Hodge projection rows remain nonclaim"),
        ("VAL2273_7_qr_nonclaim", qr_nonclaim, "q_R consequence rows remain nonclaim"),
        ("VAL2273_8_refusal_blocks", refusal_blocks, "refusal runner blocks exact-lift/local-GR claims"),
        ("VAL2273_9_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2273_10_pointwise_not_promoted", pointwise_not_promoted, "pointwise jet gain is not promoted to claim-grade field lift"),
        ("VAL2273_11_next_selected", next_selected, "2274 target selected"),
        ("VAL2273_12_csv_parse", csvs_parse, "all generated 2273 CSVs parse"),
        ("VAL2273_13_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2273_14_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2273_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2273_16_formalization_no_2273", formalization_clean, "formalization-workbench has no 2273 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2273_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2273 derives the curl obstruction for promoting the algebraic q lift to psi fields, separates pointwise from field/action lifts, blocks local-GR claims, and selects 2274",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    equations = exact_lift_equation_rows()
    curl_rows = curl_obstruction_rows()
    pointwise_rows = pointwise_vs_field_rows()
    projection_rows = smoothing_projection_rows()
    qr_rows = qR_consequence_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2273 - Y5/R2FR Exact psi Gradient Lift Curl/Smoothing Gate",
        "",
        "## Verdict",
        "",
        "This checkpoint finds the next real obstruction. The 2272 algebraic lift is valid as covariance linear algebra, and it can be read as pointwise first-jet data. But a parent `psi` field does not vary by arbitrary one-forms; it varies by exact one-forms `d zeta_A`.",
        "",
        "For the 2272 candidate `delta u_A=M u_A`, the exactness test is `Omega_A,mn=partial_m(delta u_A,n)-partial_n(delta u_A,m)=0`. Generically this is not zero because `M`, the carrier gradients, and the q-profile can vary across the coarse cell. So the local-GR route is not dead, but it now needs a curl-zero mechanism or a sourced Hodge/projection residual bound.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Exact Lift Equations",
        table(["equation_id", "object", "equation", "meaning", "status", "valid_for_claim"], equations),
        "",
        "## Curl Obstruction Derivation",
        table(["obstruction_id", "claim_tested", "derivation", "result", "missing_zero_mechanism", "claim_allowed"], curl_rows),
        "",
        "## Pointwise vs Field Lift Ledger",
        table(["ledger_id", "level", "what_is_true", "what_is_not_true", "use_in_theory", "claim_allowed"], pointwise_rows),
        "",
        "## Smoothing / Hodge Projection Gate",
        table(["projection_id", "object", "proposal", "required_inputs", "pass_condition", "status", "valid_for_claim"], projection_rows),
        "",
        "## q_R Consequence Ledger",
        table(["consequence_id", "route", "condition", "consequence", "current_status", "valid_for_claim"], qr_rows),
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
        "This is a useful unpleasant result. The coupling problem has become concrete: the missing object is not a vibe called coupling, it is the exact-gradient/smoothing residual that decides whether q suppression is a theorem or a finite residual to be bounded. The next best attack is therefore 2274: try to construct a curl-zero mechanism; if that fails, turn the curl residual into a source-backed q_R bound input.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["exact_lift_equations"], exact_lift_equation_rows())
    write_csv(OUTPUTS["curl_obstruction"], curl_obstruction_rows())
    write_csv(OUTPUTS["pointwise_vs_field"], pointwise_vs_field_rows())
    write_csv(OUTPUTS["smoothing_projection"], smoothing_projection_rows())
    write_csv(OUTPUTS["qR_consequence"], qR_consequence_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["curl_obstruction"], COPY_TARGETS["queue_curl"])
    shutil.copyfile(OUTPUTS["smoothing_projection"], COPY_TARGETS["queue_projection"])
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
