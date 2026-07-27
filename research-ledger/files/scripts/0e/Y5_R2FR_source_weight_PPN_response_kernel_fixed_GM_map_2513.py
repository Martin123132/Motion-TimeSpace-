from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_SOURCE_WEIGHT_PPN_RESPONSE_KERNEL_FIXED_GM_2513"
CHECKPOINT_ID = "2513"
DOC = ROOT / "2513-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_SOURCE_REGISTER.csv",
    "fixed_gm_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_FIXED_GM_TRANSFER_GATE.csv",
    "ppn_kernel_matrix": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_PPN_SOURCE_WEIGHT_KERNEL_MATRIX.csv",
    "ppn_bound_interface": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_PPN_BOUND_INTERFACE.csv",
    "no_absorb_guard": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_NO_GM_ABSORB_GUARD.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2513_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2513_VALIDATION.csv",
}

BRANCH_COPIES = {
    "ppn_kernel": ROOT
    / "source-intake"
    / "local_bounds"
    / "PPN_source_weight_response_kernel_2513_NONCLAIM.csv",
    "gm_guard": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Measured_GM_no_absorb_guard_2513_NONCLAIM.csv",
    "bound_interface": ROOT
    / "source-intake"
    / "local_bounds"
    / "PPN_source_weight_bound_interface_2513_NONCLAIM.csv",
    "next_beta": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Beta_source_kernel_next_2513_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2513_0_2512_next",
        "path": "2512-Y5-R2FR-tau-WEP-lower-bound-or-parent-nondegeneracy-proof.md",
        "needles": ["NEXT2512_0_selected", "PPN source-weight response kernel"],
        "role": "authoritative theory-route pivot from tau gate to PPN/fixed-GM kernel",
    },
    {
        "source_id": "SRC2513_1_2489_ppn_vector",
        "path": "source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv",
        "needles": ["PPNV2489_4_wR", "PPNV2489_7_total_abs"],
        "role": "PPN residual vector slots including source prefactor and no-cancellation total",
    },
    {
        "source_id": "SRC2513_2_2489_ppn_bounds",
        "path": "source-intake/local_bounds/PPN_bound_ledger_2489_NONCLAIM.csv",
        "needles": ["PBOUND2489_0_gamma", "PBOUND2489_4_alpha3"],
        "role": "source-backed PPN comparator bounds",
    },
    {
        "source_id": "SRC2513_3_2500_full_ppn",
        "path": "source-intake/local_bounds/Full_PPN_vector_requirements_2500_NONCLAIM.csv",
        "needles": ["VREQ2500_4_wR_source", "VREQ2500_6_total_no_cancellation"],
        "role": "full PPN vector requirements and absolute envelope",
    },
    {
        "source_id": "SRC2513_4_2500_beta_gate",
        "path": "source-intake/local_bounds/Beta_second_order_gate_2500_NONCLAIM.csv",
        "needles": ["BETA2500_2_source_coupling", "BETA2500_4_verdict"],
        "role": "second-order beta/source-coupling blocker",
    },
    {
        "source_id": "SRC2513_5_2322_tau_ppn",
        "path": "source-intake/beta-source/docs/TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT_2322_NONCLAIM.csv",
        "needles": ["TPA2322_3_readout_gauge_tail", "TPA2322_4_verdict"],
        "role": "tau_PPN/readout gauge tail refusal",
    },
    {
        "source_id": "SRC2513_6_2128_local_gr",
        "path": "source-intake/source-weight/docs/AFRAME_LOCAL_GR_GATE_MAP_2128_NONCLAIM.csv",
        "needles": ["LGR2128_2_Newton_GM_source_normalization", "LGR2128_8_total_verdict"],
        "role": "local GR/Newton gate map and measured-GM source-normalization blocker",
    },
    {
        "source_id": "SRC2513_7_2097_current_owner",
        "path": "source-intake/source-weight/docs/AFRAME_CURRENT_OWNER_NONHILBERT_2097_NONCLAIM.csv",
        "needles": ["CUR2097_7_verdict", "CM2097_0_relative_source_weight"],
        "role": "current-owner and relative source-weight countermodel",
    },
    {
        "source_id": "SRC2513_8_2127_ep_closure",
        "path": "source-intake/source-weight/docs/AFRAME_EP_CLOSURE_2127_NONCLAIM.csv",
        "needles": ["IAS2127_5_verdict", "EPC2127_1_common_quotient"],
        "role": "private source-side EP closure and measured-G common quotient guard",
    },
    {
        "source_id": "SRC2513_9_2510_bound_pack",
        "path": "source-intake/local_bounds/Source_weight_residual_bound_pack_2510_NONCLAIM.csv",
        "needles": ["ARENA2510_2_PPN", "without absorbing relative weights into fitted GM"],
        "role": "source-weight PPN arena row selected by the 2510 bound pack",
    },
    {
        "source_id": "SRC2513_10_2319_source_import",
        "path": "source-intake/beta-source/docs/PPN_VECTOR_SOURCE_IMPORT_2319_NONCLAIM.csv",
        "needles": ["PPN2319_0_gamma_source", "NONCLAIM_VECTOR_TARGET"],
        "role": "older source-backed comparator import, not a MTS component prediction",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def fixed_gm_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GM2513_0_common_mode",
            "object": "epsilon_common",
            "rule": "a constant, universal, range/time/species/frame independent source normalization may be absorbed into measured GM only after universality is proved",
            "mathematical_form": "U_obs := G_obs M_obs/r fixes one common multiplicative scale",
            "current_status": "EXACT_CONDITIONAL_CALIBRATION_RULE",
            "blocks": "cannot absorb relative or environment-dependent source weights",
        },
        {
            "gate_id": "GM2513_1_relative_weight",
            "object": "Delta_w_A",
            "rule": "relative species/source weights survive fixed-GM calibration",
            "mathematical_form": "epsilon_A - epsilon_ref remains in observables after one GM quotient",
            "current_status": "LIVE_RESIDUAL",
            "blocks": "WEP-clean or one-body calibrated source shifts cannot be treated as GR",
        },
        {
            "gate_id": "GM2513_2_range_time",
            "object": "epsilon(lambda,t,frame)",
            "rule": "range/time/frame/source-profile dependence cannot be hidden in a constant GM fit",
            "mathematical_form": "delta U(r,t)/U != constant over the comparison domain",
            "current_status": "LIVE_RESIDUAL",
            "blocks": "R10/orbital/PPN consistency if the same vector changes with scale",
        },
        {
            "gate_id": "GM2513_3_readout",
            "object": "alpha_readout_or_delta_GM",
            "rule": "PPN gauge/readout map must be fixed before comparing gamma/beta",
            "mathematical_form": "Delta_PPN_obs = Delta_PPN_field + T_readout[Delta_w_eff]",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "blocks": "fake beta/gamma closure by post-fit calibration",
        },
        {
            "gate_id": "GM2513_4_verdict",
            "object": "fixed measured-GM convention",
            "rule": "GM can remove only one proven common scalar; all other source-weight pieces require PPN response kernels",
            "mathematical_form": "Delta_PPN_abs uses componentwise post-GM residuals",
            "current_status": "FIXED_GM_RULE_WRITTEN_KERNELS_MISSING",
            "blocks": "local-GR claim",
        },
    ]
    return [
        base_row(score_ready=False, valid_prediction_row=False, **row)
        for row in rows
    ]


def ppn_kernel_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "PPNK2513_0_gamma_source_weight",
            "observable": "gamma_minus_1",
            "residual_law": "delta_gamma_source = C_gamma_w * Delta_w_eff + C_gamma_metric * delta_p + C_gamma_readout * alpha_readout",
            "required_kernel": "C_gamma_w;C_gamma_metric;C_gamma_readout in fixed GM convention",
            "comparator_bound": "2.3e-05",
            "units": "dimensionless",
            "current_status": "MISSING_GAMMA_SOURCE_RESPONSE_KERNEL",
        },
        {
            "kernel_id": "PPNK2513_1_beta_source_weight",
            "observable": "beta_minus_1",
            "residual_law": "delta_beta_total = C_beta_w * Delta_w_eff + C_beta_NH * J_NH + C_beta_readout * alpha_readout + second_order_operator_tail",
            "required_kernel": "second-order source-normalized field equation and readout/GM map",
            "comparator_bound": "7.8e-05",
            "units": "dimensionless",
            "current_status": "MISSING_BETA_SECOND_ORDER_SOURCE_KERNEL",
        },
        {
            "kernel_id": "PPNK2513_2_alpha1_source_frame",
            "observable": "alpha1",
            "residual_law": "alpha1_source = C_alpha1_frame * d_R + C_alpha1_w * Delta_w_eff + C_alpha1_endpoint * epsilon_endpoint",
            "required_kernel": "preferred-frame/disformal response matrix",
            "comparator_bound": "1e-04",
            "units": "dimensionless",
            "current_status": "MISSING_PREFERRED_FRAME_KERNEL",
        },
        {
            "kernel_id": "PPNK2513_3_alpha2_source_frame",
            "observable": "alpha2",
            "residual_law": "alpha2_source = C_alpha2_frame * d_R + C_alpha2_boundary * Q_edge + C_alpha2_projector * Delta_mu_projector",
            "required_kernel": "preferred-frame/domain/projector response matrix",
            "comparator_bound": "2e-09",
            "units": "dimensionless",
            "current_status": "MISSING_VECTOR_DOMAIN_KERNEL",
        },
        {
            "kernel_id": "PPNK2513_4_alpha3_source_exchange",
            "observable": "alpha3",
            "residual_law": "alpha3_source = C_alpha3_exchange * Delta_w_eff + C_alpha3_NH * J_NH + C_alpha3_boundary * Q_edge",
            "required_kernel": "source-current conservation/exchange response and no-Hilbert-current theorem or bound",
            "comparator_bound": "4e-20",
            "units": "dimensionless",
            "current_status": "MISSING_SOURCE_EXCHANGE_KERNEL_ULTRATIGHT",
        },
        {
            "kernel_id": "PPNK2513_5_xi_boundary",
            "observable": "xi",
            "residual_law": "xi_source = C_xi_boundary * Q_edge + C_xi_domain * Delta_worldtube + C_xi_projective * trace_projective",
            "required_kernel": "boundary/domain/preferred-location response",
            "comparator_bound": "4e-09",
            "units": "dimensionless",
            "current_status": "MISSING_BOUNDARY_DOMAIN_KERNEL",
        },
        {
            "kernel_id": "PPNK2513_6_total_abs",
            "observable": "Delta_PPN_abs",
            "residual_law": "sum_i abs(PPNK_i component_i) <= bound_i componentwise; no cancellation unless parent identity signs it",
            "required_kernel": "all component kernels and component values/theorem-zeros",
            "comparator_bound": "componentwise PPN ledger",
            "units": "dimensionless vector",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
        },
    ]
    return [
        base_row(score_ready=False, valid_prediction_row=False, **row)
        for row in rows
    ]


def ppn_bound_interface_rows() -> list[dict[str, Any]]:
    bounds = [
        ("PBOUND2513_0_gamma", "gamma_minus_1", "2.3e-05", "Cassini_Shapiro_gamma_2003"),
        ("PBOUND2513_1_beta", "beta_minus_1", "7.8e-05", "Will_2014_PPN_beta_table"),
        ("PBOUND2513_2_alpha1", "alpha1", "1e-04", "Will_2014_PPN_alpha1_table"),
        ("PBOUND2513_3_alpha2", "alpha2", "2e-09", "Will_2014_PPN_alpha2_table"),
        ("PBOUND2513_4_alpha3", "alpha3", "4e-20", "Will_2014_PPN_alpha3_table"),
        ("PBOUND2513_5_xi", "xi", "4e-09", "Will_2014_PPN_xi_table"),
    ]
    return [
        base_row(
            bound_id=bound_id,
            observable=observable,
            upper_bound=upper_bound,
            units="dimensionless",
            source_dataset=dataset,
            comparator_status="SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION",
            required_for_scoring="matching PPNK row numeric prediction in same fixed-GM convention",
            score_ready=False,
            valid_prediction_row=False,
        )
        for bound_id, observable, upper_bound, dataset in bounds
    ]


def no_absorb_guard_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "guard_id": "NAG2513_0_forbid_relative_G",
            "forbidden_move": "absorb Delta_w_A/Delta_w_B into measured G",
            "reason": "only a universal common scalar can define the measured GM quotient",
            "status": "FORBIDDEN",
        },
        {
            "guard_id": "NAG2513_1_forbid_bound_as_prediction",
            "forbidden_move": "treat PPN comparator bounds as MTS predictions",
            "reason": "bounds are external targets; MTS needs kernels and coefficients",
            "status": "FORBIDDEN",
        },
        {
            "guard_id": "NAG2513_2_forbid_GR_import",
            "forbidden_move": "import gamma=beta=1 from GR to close the MTS local branch",
            "reason": "the goal is to derive the GR/Newton limit or mark imported EH/GR explicitly",
            "status": "FORBIDDEN",
        },
        {
            "guard_id": "NAG2513_3_no_cancellation",
            "forbidden_move": "cancel gamma/beta/source/readout tails numerically without parent identity",
            "reason": "componentwise absolute envelope remains active",
            "status": "FORBIDDEN",
        },
        {
            "guard_id": "NAG2513_4_allow_common_GM",
            "forbidden_move": "none: one proven universal constant normalization may be quotient-calibrated",
            "reason": "this is a units/source convention, not a residual eraser",
            "status": "ALLOWED_ONLY_IF_UNIVERSALITY_PROVED",
        },
    ]
    return [base_row(**row) for row in rows]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2513_0_ppn_bounds_only",
            "case_description": "compare to PPN ledger without MTS response kernels",
            "result_status": "REFUSED_COMPARATOR_WITHOUT_PREDICTION",
            "blocking_markers": "MISSING_PPN_SOURCE_RESPONSE_KERNELS",
        },
        {
            "case_id": "DRY2513_1_absorb_relative_weights",
            "case_description": "hide relative source weights in measured GM",
            "result_status": "REFUSED_RELATIVE_GM_ABSORPTION",
            "blocking_markers": "RELATIVE_WEIGHTS_SURVIVE_FIXED_GM",
        },
        {
            "case_id": "DRY2513_2_import_GR_gamma_beta",
            "case_description": "set gamma=beta=1 by importing GR/EH result",
            "result_status": "REFUSED_GR_IMPORT_AS_DERIVATION",
            "blocking_markers": "EH_IMPORT_MUST_BE_LABELED;MISSING_MTS_OPERATOR_SELECTION",
        },
        {
            "case_id": "DRY2513_3_beta_from_gamma",
            "case_description": "infer beta closure from first-order gamma/source normalization",
            "result_status": "REFUSED_SECOND_ORDER_GAP",
            "blocking_markers": "MISSING_BETA_SECOND_ORDER_SOURCE_KERNEL",
        },
        {
            "case_id": "DRY2513_4_alpha3_ignore",
            "case_description": "ignore source-exchange alpha3 because WEP/product rows look clean",
            "result_status": "REFUSED_SOURCE_EXCHANGE_GAP",
            "blocking_markers": "MISSING_ALPHA3_SOURCE_EXCHANGE_KERNEL;BOUND_4E-20",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2513_0_gain",
            "decision": "FIXED_GM_RULE_LOCKED",
            "rationale": "Only one proven universal common source scale may be calibrated into GM; relative/range/readout/source pieces stay residual.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2513_1_kernel",
            "decision": "PPN_SOURCE_WEIGHT_KERNEL_MATRIX_STAGED",
            "rationale": "gamma, beta, alpha1, alpha2, alpha3, xi now each have explicit missing kernel rows and comparator bounds.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2513_2_beta",
            "decision": "BETA_SECOND_ORDER_IS_LEADING_GR_GATE",
            "rationale": "beta cannot be inferred from WEP or gamma; it needs a second-order source-normalized field equation or finite source kernel.",
            "status": "selected_next",
        },
        {
            "decision_id": "DEC2513_3_alpha3",
            "decision": "ALPHA3_SOURCE_EXCHANGE_IS_ULTRATIGHT",
            "rationale": "alpha3 has a 4e-20 comparator and catches source-current/nonconservation leaks that WEP can miss.",
            "status": "retained_parallel",
        },
        {
            "decision_id": "DEC2513_4_claim",
            "decision": "NO_PPN_OR_LOCAL_GR_CLAIM",
            "rationale": "All PPN response kernels are schema/nonclaim; no model row is score-ready.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2513_0_selected",
            selection_status="selected",
            target_file="2514-Y5-R2FR-beta-second-order-source-kernel-or-EH-operator-selection.md",
            target_script="scripts/Y5_R2FR_beta_second_order_source_kernel_or_EH_operator_selection_2514.py",
            objective="derive the second-order beta source kernel from the parent weak-field/operator equation, or keep EH/GR import explicit and write a finite beta-source bound row",
            success_condition="beta response has a source-normalized U^2 coefficient, fixed-GM/readout convention, units, comparator bound, and no GR import unless labeled",
            do_not_do="do not infer beta=1 from gamma, WEP, or imported Schwarzschild unless this is explicitly an EH-import branch",
        ),
        base_row(
            route_id="NEXT2513_1_parallel",
            selection_status="parallel_after_beta",
            target_file="2514b-Y5-R2FR-alpha3-source-exchange-current-owner-bound.md",
            target_script="scripts/Y5_R2FR_alpha3_source_exchange_current_owner_bound_2514b.py",
            objective="derive or bound the source-exchange/current-owner contribution to alpha3 under the no-Hilbert-current and no-cancellation gates",
            success_condition="alpha3 source-exchange row has current-owner status, kernel units, 4e-20 comparator, and no WEP-clean shortcut",
            do_not_do="do not ignore alpha3 because it is inconvenient; do not cancel current pieces without parent identity",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("ppn_kernel", OUTPUTS["ppn_kernel_matrix"], BRANCH_COPIES["ppn_kernel"]),
        ("gm_guard", OUTPUTS["fixed_gm_gate"], BRANCH_COPIES["gm_guard"]),
        ("bound_interface", OUTPUTS["ppn_bound_interface"], BRANCH_COPIES["bound_interface"]),
        ("next_beta", OUTPUTS["next_target"], BRANCH_COPIES["next_beta"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        ok, count, message = csv_rows_parse(dst)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(src.relative_to(ROOT)),
                destination=str(dst.relative_to(ROOT)),
                copied=dst.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "claim_pass"):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    add("VAL2513_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2513_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2513_02_fixed_gm_rule",
        any(row["gate_id"] == "GM2513_4_verdict" and row["current_status"] == "FIXED_GM_RULE_WRITTEN_KERNELS_MISSING" for row in rows_by_name["fixed_gm_gate"]),
        "fixed GM rule present",
    )
    add(
        "VAL2513_03_ppn_kernel_coverage",
        {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi"}.issubset(
            {row["observable"] for row in rows_by_name["ppn_kernel_matrix"]}
        ),
        "all major PPN observables covered",
    )
    add(
        "VAL2513_04_bounds_coverage",
        {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi"}.issubset(
            {row["observable"] for row in rows_by_name["ppn_bound_interface"]}
        ),
        "all comparator bounds imported",
    )
    add(
        "VAL2513_05_no_absorb_guard",
        any(row["guard_id"] == "NAG2513_0_forbid_relative_G" and row["status"] == "FORBIDDEN" for row in rows_by_name["no_absorb_guard"]),
        "relative GM absorption forbidden",
    )
    add(
        "VAL2513_06_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "all dry runs nonclaim",
    )
    add(
        "VAL2513_07_next_target",
        any(row["route_id"] == "NEXT2513_0_selected" for row in rows_by_name["next_target"]),
        "beta second-order target selected",
    )
    add("VAL2513_08_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2513_09_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2513*")) if formalization.exists() else []
    add(
        "VAL2513_10_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2513_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2513_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2513_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2513_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2513 locks fixed-GM guard, stages PPN source-weight kernel matrix, and selects beta second-order kernel next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2513 — Source-Weight PPN Response Kernel with Fixed-GM Map",
                "",
                "**Current verdict:** the local-GR bridge now has a stricter PPN interface. A single universal common source normalization may be calibrated into measured `GM`, but relative, source-dependent, range-dependent, time-dependent, frame-dependent, boundary, and readout pieces remain physical residuals.",
                "",
                "**No claim:** this is not a PPN pass. It is a response-kernel contract. Gamma, beta, preferred-frame terms, alpha3/source exchange, xi/boundary, and readout/GM tails all remain nonclaim until their kernels and coefficients are sourced or parent-zero.",
                "",
                "**Next pressure point:** beta is the leading GR gate because it needs the second-order `U^2` source-normalized field equation; gamma/WEP cannot give beta for free.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Fixed-GM Transfer Gate",
                md_table(rows_by_name["fixed_gm_gate"], ["gate_id", "object", "rule", "mathematical_form", "current_status", "blocks"]),
                "",
                "## PPN Source-Weight Kernel Matrix",
                md_table(rows_by_name["ppn_kernel_matrix"], ["kernel_id", "observable", "residual_law", "required_kernel", "comparator_bound", "current_status"]),
                "",
                "## PPN Bound Interface",
                md_table(rows_by_name["ppn_bound_interface"], ["bound_id", "observable", "upper_bound", "source_dataset", "comparator_status", "required_for_scoring"]),
                "",
                "## No-Absorb Guard",
                md_table(rows_by_name["no_absorb_guard"], ["guard_id", "forbidden_move", "reason", "status"]),
                "",
                "## Nonclaim Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail", "claim_pass"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "fixed_gm_gate": fixed_gm_gate_rows(),
        "ppn_kernel_matrix": ppn_kernel_matrix_rows(),
        "ppn_bound_interface": ppn_bound_interface_rows(),
        "no_absorb_guard": no_absorb_guard_rows(),
        "dryrun_results": dryrun_result_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
