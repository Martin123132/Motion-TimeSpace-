from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_DELTA_P_BETA_DISFORMAL_PPN_VECTOR_2500"
CHECKPOINT_ID = "2500"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2500-Y5-R2FR-delta-p-beta-disformal-PPN-vector-or-parent-no-shadow-proof.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2500_SOURCE_REGISTER.csv",
    "delta_p_proof": OUT / "P8_Y5_NO_SHADOW_2500_DELTA_P_ZERO_PROOF_AUDIT.csv",
    "beta_gate": OUT / "P8_Y5_NO_SHADOW_2500_BETA_SECOND_ORDER_GATE.csv",
    "preferred_kernel": OUT / "P8_Y5_NO_SHADOW_2500_DISFORMAL_ENDPOINT_PPN_KERNEL_ROWS.csv",
    "vector_requirements": OUT / "P8_Y5_NO_SHADOW_2500_FULL_PPN_VECTOR_REQUIREMENTS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2500_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2500_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2500_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2500_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2500_VALIDATION.csv",
}

COPY_TARGETS = {
    "delta_p_proof": LOCAL_BOUNDS / "Delta_p_zero_proof_audit_2500_NONCLAIM.csv",
    "beta_gate": LOCAL_BOUNDS / "Beta_second_order_gate_2500_NONCLAIM.csv",
    "preferred_kernel": LOCAL_BOUNDS / "Disformal_endpoint_PPN_kernel_rows_2500_NONCLAIM.csv",
    "vector_requirements": LOCAL_BOUNDS / "Full_PPN_vector_requirements_2500_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2500_QR_BETA_DISFORMAL_PARENT_SIGNATURE_OR_VECTOR_INPUT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2500_00_2489_handoff",
        "source_path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["NEXT2489_0_selected", "PPNK2489_1_CR_delta_p_combo_kernel", "VAL2489_OVERALL"],
        "role": "current handoff selecting delta_p/beta/disformal PPN vector target",
    },
    {
        "source_id": "SRC2500_01_1884_zero_flux",
        "source_path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": ["NBC1884_1_exact_zero_flux_lemma", "DPQR1884_2_delta_p", "VAL1884_OVERALL"],
        "role": "zero-flux lemma and strict delta_p/q_R_hat input contract",
    },
    {
        "source_id": "SRC2500_02_1883_vector",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["PPNV1883_2_beta_second_order", "PPNV1883_3_dR_preferred_frame", "PPNV1883_7_total_no_cancellation"],
        "role": "full PPN residual-vector precedent",
    },
    {
        "source_id": "SRC2500_03_2231_ppn_coefficients",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2231_PPN_COEFFICIENT_DERIVATION.csv",
        "needles": ["PPNC2231_4_delta_beta_definition", "PPNC2231_6_perihelion_degeneracy"],
        "role": "PPN coefficient dictionary for q_R and beta",
    },
    {
        "source_id": "SRC2500_04_2234_ward_beta",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2234_WARD_PPN_GATE.csv",
        "needles": ["WPPN2234_2_beta", "WPPN2234_5_local_claim"],
        "role": "conditional EH/Ward beta route and blocked local claim",
    },
    {
        "source_id": "SRC2500_05_ppn_contract",
        "source_path": OUT / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_1_g00_quadratic_beta", "MEX524_3_gravitomagnetic_preferred_frame", "MEX524_6_no_cancellation_PPN_envelope"],
        "role": "baseline PPN metric expansion contract",
    },
    {
        "source_id": "SRC2500_06_tau_ppn",
        "source_path": ROOT / "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md",
        "needles": ["TPA2322_1_tau_standard_scalar_tensor", "SIG2322_4_ppn_gauge_source", "VAL2322_OVERALL"],
        "role": "tau_PPN common-frame normalization and readout/gauge blocker",
    },
    {
        "source_id": "SRC2500_07_local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["Will_2014_PPN_beta_table", "Will_2014_PPN_alpha2_table", "Will_2014_PPN_alpha3_table"],
        "role": "PPN beta/preferred-frame comparator bounds",
    },
    {
        "source_id": "SRC2500_08_2489_validation",
        "source_path": OUT / "P8_Y5_BRR545_2489_VALIDATION.csv",
        "needles": ["VAL2489_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def delta_p_proof_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_id": "DPP2500_0_exterior_current",
            "statement": "In the exterior, partial_r(W partial_r C_R)=J_R and J_R=0 imply W partial_r C_R=Q_R.",
            "status": "CONDITIONAL_CURRENT_EQUATION_AVAILABLE",
            "missing_premise": "parent action must define the reciprocal generator and ordinary source silence, not just an exterior integration constant",
            "consequence": "identifies the finite charge that controls delta_p",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2500_1_zero_flux_lemma",
            "statement": "If Q_R=0, W>0, J_R=0 in the exterior, and C_R(infinity)=0, then C_R=0.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "missing_premise": "Q_R=0/no-boundary-charge theorem is not parent-signed",
            "consequence": "delta_p=0 at first PPN order because C_R=2 delta_p U/c^2+O(U^2/c^4)",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2500_2_finite_bridge",
            "statement": "If exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(G M_source), then delta_p=-q_R_hat/2.",
            "status": "DERIVED_CONDITIONAL_BRIDGE_NONCLAIM",
            "missing_premise": "live q_R_hat value, measured-GM convention, source body, and matter/readout descent",
            "consequence": "strict finite input row can feed the full PPN vector without closure cheating",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DPP2500_3_parent_zero_verdict",
            "statement": "Current MTS parent derives Q_R=0 and therefore delta_p=0.",
            "status": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_premise": "boundary charge zero, source descent, matter descent, projection silence, and no-shadow readout must close in one action",
            "consequence": "delta_p remains the first local-GR finite/theorem-zero input",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def beta_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "BETA2500_0_definition",
            "statement": "beta_minus_1 is the second-order g00 residual delta_beta_total.",
            "status": "PPN_DICTIONARY_AVAILABLE",
            "required_inputs": "source-normalized second-order field equation; measured-GM convention; readout/gauge transform",
            "failure_mode": "gamma or delta_p closure does not imply beta=1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2500_1_EH_conditional",
            "statement": "EH core plus correctly normalized Hilbert source and no extra modes gives beta=1.",
            "status": "EXACT_CONDITIONAL_GR_LIMIT",
            "required_inputs": "EH/kappa owner; source closure; boundary silence; no extra scalar/vector/tensor modes; readout fixed before comparison",
            "failure_mode": "using GR Schwarzschild beta=1 as an imported axiom would smuggle the target result",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2500_2_source_coupling",
            "statement": "source-prefactor w_R and non-Hilbert current tails must not re-enter beta through U^2 terms.",
            "status": "MISSING_SOURCE_SECOND_ORDER_CLOSURE",
            "required_inputs": "source-current descent/no source-only slot theorem or finite beta source kernel",
            "failure_mode": "WEP-clean source shifts can survive composition tests and move beta/source normalization",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2500_3_readout_gauge",
            "statement": "PPN gauge and measured-GM calibration must not absorb or create beta/gamma residuals.",
            "status": "MISSING_READOUT_GAUGE_TRANSFER",
            "required_inputs": "fixed-before-readout theorem; GM calibration map; observed PPN gauge transform",
            "failure_mode": "a fitted-GM shortcut can hide a source/readout tail rather than derive local GR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BETA2500_4_verdict",
            "statement": "Current MTS derives beta=1 in the active local branch.",
            "status": "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS",
            "required_inputs": "BETA2500_1 through BETA2500_3 must all be parent-signed or source-bounded",
            "failure_mode": "local-GR claim remains blocked even if gamma channel is bounded",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def preferred_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "DPK2500_0_dR_alpha1_alpha2",
            "component": "d_R common disformal/preferred-frame",
            "candidate_map": "alpha1,alpha2 = K_dis * d_R plus possible current/domain normalization terms",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_alpha1_table:R5_alpha1;Will_2014_PPN_alpha2_table:R6_alpha2",
            "required_inputs": "normalized disformal ansatz, current field normalization, preferred-frame gauge, same matter metric convention",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2500_1_flux_alpha3",
            "component": "source exchange/boundary flux/w_R",
            "candidate_map": "alpha3 = K_flux*(w_R + q_boundary + source_exchange)",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_alpha3_table:R7_alpha3",
            "required_inputs": "momentum conservation/source-current descent, boundary flux silence or finite coefficient row",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2500_2_endpoint_xi",
            "component": "epsilon_endpoint_R/domain/boundary",
            "candidate_map": "xi = K_xi_endpoint*epsilon_endpoint_R + K_xi_domain*q_domain",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Will_2014_PPN_xi_table:R8_xi",
            "required_inputs": "endpoint local projection kernel, domain/support vector, boundary no-hair theorem or finite input",
            "valid_for_claim": False,
        },
        {
            "kernel_id": "DPK2500_3_readout_gamma_beta_tail",
            "component": "post-variation readout/measured-GM tail",
            "candidate_map": "delta_gamma_readout,delta_beta_readout = K_readout*C_readout",
            "status": "SOURCE_READY_TEMPLATE_KERNEL_MISSING",
            "bound_rows": "Cassini_Shapiro_gamma_2003:R3_gamma;Will_2014_PPN_beta_table:R4_beta",
            "required_inputs": "fixed-before-readout proof or explicit readout calibration residual with units",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def vector_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "VREQ2500_0_delta_p",
            "required_for_claim": "delta_p=0 theorem or source-normalized q_R_hat/delta_p row satisfying delta_p=-q_R_hat/2",
            "current_status": "MISSING_PARENT_ZERO_OR_LIVE_INPUT",
            "blocks": "gamma kernel; C_R no-shadow combo",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_1_bR",
            "required_for_claim": "b_R=0 theorem or finite coefficient in same C_R normalization",
            "current_status": "MISSING_NO_SHADOW_ZERO_OR_VALUE",
            "blocks": "common Weyl gamma/clock/source row",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_2_beta",
            "required_for_claim": "beta=1 theorem or delta_beta_total row below beta bound",
            "current_status": "MISSING_SECOND_ORDER_CLOSURE",
            "blocks": "local-GR PPN completion",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_3_dR",
            "required_for_claim": "d_R=0 theorem or alpha1/alpha2 response kernel below preferred-frame bounds",
            "current_status": "MISSING_DISFORMAL_KERNEL",
            "blocks": "preferred-frame PPN",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_4_wR_source",
            "required_for_claim": "w_R/source-only slot theorem-zero or source-normalization kernel below PPN/WEP bounds",
            "current_status": "MISSING_SOURCE_PREFACTOR_CLOSURE",
            "blocks": "beta, alpha3, measured-GM transfer",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_5_endpoint_readout",
            "required_for_claim": "endpoint/readout/gauge tails theorem-zero or source-bounded",
            "current_status": "MISSING_ENDPOINT_READOUT_KERNEL",
            "blocks": "xi, gamma/beta extraction, orbital/light-time",
            "valid_for_claim": False,
        },
        {
            "component_id": "VREQ2500_6_total_no_cancellation",
            "required_for_claim": "componentwise absolute envelope below all relevant bounds or parent identity proving cancellation",
            "current_status": "VECTOR_VALUES_MISSING",
            "blocks": "any PPN/local-GR claim",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2500_0_internal",
            "claim": "2500 may guide private derivation/testing",
            "gate_status": "PASS_INTERNAL_NONCLAIM",
            "reason": "exact conditional lemmas and templates are separated from claims",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2500_1_delta_p_zero",
            "claim": "delta_p=0 is derived for active MTS",
            "gate_status": "BLOCKED",
            "reason": "Q_R=0/no-boundary-charge/source-descent theorem remains unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2500_2_beta_one",
            "claim": "beta=1 is derived for active MTS",
            "gate_status": "BLOCKED",
            "reason": "EH/source/readout/no-extra-mode route is exact conditional but not parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2500_3_preferred_frame_zero",
            "claim": "d_R/endpoint/source tails do not affect alpha_i or xi",
            "gate_status": "BLOCKED",
            "reason": "preferred-frame, boundary and readout kernels are source-ready templates only",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2500_4_full_ppn",
            "claim": "full PPN vector is passed",
            "gate_status": "BLOCKED",
            "reason": "component values/theorem-zero rows are missing and gamma-only/cancellation-only routes are rejected",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2500_5_local_GR_Newton",
            "claim": "local GR/Newton is derived",
            "gate_status": "BLOCKED",
            "reason": "delta_p, beta, preferred-frame, source, endpoint and EH/source-normalization gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2500_0_delta_p",
            "decision": "ZERO_FLUX_ROUTE_REMAINS_BEST_DERIVATION_TARGET",
            "reason": "Q_R=0 would cleanly force C_R=0 and delta_p=0 without fitting",
            "effect": "hunt the parent no-boundary-charge/source-descent signature rather than treat gamma bounds as proof",
        },
        {
            "decision_id": "DEC2500_1_beta",
            "decision": "BETA_REQUIRES_SECOND_ORDER_SOURCE_NORMALIZED_GATE",
            "reason": "gamma closure does not imply beta=1; EH/source/readout/no-extra-mode premises must close",
            "effect": "beta gets its own gate, not a footnote under gamma",
        },
        {
            "decision_id": "DEC2500_2_vector",
            "decision": "DISFORMAL_ENDPOINT_ROWS_STAGED_AS_SOURCE_READY_TEMPLATES",
            "reason": "preferred-frame/location bounds exist, but MTS response kernels do not",
            "effect": "d_R, alpha_i, xi and endpoint kernels are the empirical backstop if proof route stalls",
        },
        {
            "decision_id": "DEC2500_3_next",
            "decision": "QR_PARENT_ZERO_SIGNATURE_SELECTED_NEXT",
            "reason": "the biggest leverage theorem is still Q_R=0/no-boundary-charge plus source descent; beta and disformal rows remain parallel gates",
            "effect": "2501 should attack the Q_R parent-zero signature or produce the first live finite q_R_hat/delta_p input row",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2500_0_selected",
            "selection_status": "selected",
            "target_file": "2501-Y5-R2FR-QR-parent-zero-signature-or-live-delta-p-input-row.md",
            "target_script": "scripts/Y5_R2FR_QR_parent_zero_signature_or_live_delta_p_input_row_2501.py",
            "task": "try to parent-sign Q_R=0 using boundary-charge, source-descent, matter/readout descent and projection-silence clauses; if not, create the first live finite q_R_hat/delta_p input-row contract for the PPN vector",
            "acceptance_target": "parent Q_R=0 theorem package or a strict source-normalized finite delta_p/q_R_hat row that refuses closure/comparator/gamma-only/cancellation-only scoring",
            "guardrails": "no GR Schwarzschild AB=1 import; no gamma-only pass; no closure zero; no fitted GM shortcut; no WEP/Ward shortcut; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "delta_p_proof": OUTPUTS["delta_p_proof"],
        "beta_gate": OUTPUTS["beta_gate"],
        "preferred_kernel": OUTPUTS["preferred_kernel"],
        "vector_requirements": OUTPUTS["vector_requirements"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2500_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2500_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2500_01_zero_flux_conditional",
        any(row["proof_id"] == "DPP2500_1_zero_flux_lemma" and row["status"] == "EXACT_CONDITIONAL_LEMMA" for row in data["delta_p"]),
        "delta_p zero route is exact conditional",
    )
    add(
        "VAL2500_02_parent_delta_p_not_claimed",
        any(row["proof_id"] == "DPP2500_3_parent_zero_verdict" and row["status"] == "NOT_DERIVED_CURRENT_CORPUS" for row in data["delta_p"]),
        "Q_R=0/delta_p=0 is not promoted",
    )
    add(
        "VAL2500_03_beta_gate_blocked",
        any(row["gate_id"] == "BETA2500_4_verdict" and row["status"] == "BETA_CLOSURE_NOT_DERIVED_CURRENT_CORPUS" for row in data["beta"]),
        "beta second-order closure is explicit and blocked",
    )
    add(
        "VAL2500_04_preferred_templates",
        len(data["preferred"]) >= 4 and all(row["valid_for_claim"] is False for row in data["preferred"]),
        "disformal, endpoint, alpha_i, xi and readout kernels are source-ready nonclaim templates",
    )
    add(
        "VAL2500_05_vector_requirements",
        len(data["vector"]) >= 7 and any(row["component_id"] == "VREQ2500_6_total_no_cancellation" for row in data["vector"]),
        "full PPN no-cancellation vector requirements are present",
    )
    add(
        "VAL2500_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "no gate allows delta_p, beta, preferred-frame, PPN, local-GR or Newton claim",
    )
    add(
        "VAL2500_07_next_target_written",
        any(row["route_id"] == "NEXT2500_0_selected" for row in data["next"]),
        "2501 Q_R parent-zero or live delta_p input target selected",
    )
    add("VAL2500_08_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2500*", "*P8_Y5_NO_SHADOW_2500*", "*JR2500*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2500_09_no_formalization_artifacts", not formalization_artifacts, "no 2500 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2500_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2500_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2500_OVERALL",
        overall,
        "2500 preserves delta_p zero as exact conditional, blocks beta/local claims, stages disformal endpoint PPN kernels, and selects Q_R parent-zero/live input next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2500 Y5 R2FR Delta_p Beta Disformal PPN Vector Or Parent No-Shadow Proof",
        "",
        "**Status:** private nonclaim checkpoint. The local-GR route gets sharper, not looser: `delta_p=0` follows from a clean zero-flux lemma if `Q_R=0` is parent-signed, but that signature is still missing. Beta also remains a separate second-order gate.",
        "",
        "**Main result:** the best derivation target is now unambiguous. Prove the parent no-boundary-charge/source-descent package `Q_R=0`, and `C_R=0 -> delta_p=0` follows. Separately, prove EH/source/readout/no-extra-mode closure and beta goes to one. If either proof stalls, the theory must use the full PPN vector, including `d_R`, `w_R`, endpoint and readout tails. Gamma-only is refused.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Delta_p Zero Proof Audit",
        markdown_table(data["delta_p"], ["proof_id", "statement", "status", "missing_premise", "consequence", "valid_for_claim"]),
        "",
        "## Beta Second-Order Gate",
        markdown_table(data["beta"], ["gate_id", "statement", "status", "required_inputs", "failure_mode", "valid_for_claim"]),
        "",
        "## Disformal Endpoint PPN Kernel Rows",
        markdown_table(data["preferred"], ["kernel_id", "component", "candidate_map", "status", "bound_rows", "required_inputs", "valid_for_claim"]),
        "",
        "## Full PPN Vector Requirements",
        markdown_table(data["vector"], ["component_id", "required_for_claim", "current_status", "blocks", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "delta_p": delta_p_proof_rows(),
        "beta": beta_gate_rows(),
        "preferred": preferred_kernel_rows(),
        "vector": vector_requirement_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["delta_p_proof"], data["delta_p"])
    write_csv(OUTPUTS["beta_gate"], data["beta"])
    write_csv(OUTPUTS["preferred_kernel"], data["preferred"])
    write_csv(OUTPUTS["vector_requirements"], data["vector"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
