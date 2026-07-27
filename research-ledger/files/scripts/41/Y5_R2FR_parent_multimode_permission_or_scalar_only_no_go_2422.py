from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_MULTIMODE_PERMISSION_OR_SCALAR_ONLY_NO_GO_2422"
CHECKPOINT_ID = "2422"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2422-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2422_SOURCE_REGISTER.csv",
    "multimode_gate": OUT / "P8_Y5_PARENT_QLOC_2422_MULTIMODE_PERMISSION_GATE.csv",
    "transport_gate": OUT / "P8_Y5_PARENT_QLOC_2422_WKB_TRANSPORT_Q_SELECTION_GATE.csv",
    "exchange_gate": OUT / "P8_Y5_PARENT_QLOC_2422_CARRIER_EXCHANGE_CONDITION_GATE.csv",
    "phase_operator": OUT / "P8_Y5_PARENT_QLOC_2422_PHASE_EXCHANGE_OR_Q_OPERATOR_LEDGER.csv",
    "parallel_local": OUT / "P8_Y5_PARENT_QLOC_2422_PARALLEL_SOURCE_READOUT_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2422_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2422_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2422_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2422_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2422_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2422_MULTIMODE_TRANSPORT_EXCHANGE_FRONTIER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2422_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_MULTIMODE_EXCHANGE_DECISION_2422_NONCLAIM.csv",
}


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
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2422_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2422-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2422*",
        "*P8_Y5_BRR545_2422*",
        "*Y5_R2FR_parent_multimode_permission_or_scalar_only_no_go_2422*",
        "*JR2422*",
        "*PARENT_QLOC_MULTIMODE_EXCHANGE_DECISION_2422*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("2421_handoff", ROOT / "2421-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md", ["FS2421_6_carrier_inventory", "NEXT2421_0_selected", "VAL2421_OVERALL"], "current handoff: multimode permission/scalar no-go selected."),
        ("2276_multimode", ROOT / "2276-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md", ["MPA2276_0_single_field_multimode", "WKB2276_2_smoothed_covariance", "VAL2276_OVERALL"], "scalar multimode WKB route conditionally open; single-mode scalar insufficient."),
        ("2277_transport", ROOT / "2277-Y5-R2FR-WKB-carrier-transport-or-q-zero-selection-gate.md", ["WTD2277_3_weight_transport", "QSG2277_3_residual_route", "VAL2277_OVERALL"], "equation-level WKB transport derived; q-zero not selected."),
        ("2278_exchange", ROOT / "2278-Y5-R2FR-carrier-exchange-law-or-q-transport-source-bound.md", ["EXC2278_2_tangent_lock", "RXS2278_2_one_parameter_family", "VAL2278_OVERALL"], "exact carrier exchange condition derived; parent exchange law unsigned."),
        ("2279_phase_operator", ROOT / "2279-Y5-R2FR-nonlinear-phase-exchange-coefficients-or-q-residual-operator.md", ["NPP2279_2_independent_phase_zero", "QOP2279_1_elliptic_stiffness", "VAL2279_OVERALL"], "random nonlinear phase exchange rejected; locked phase/operator route selected."),
        ("2368_coeff_functor", ROOT / "2368-Y5-R2FR-parent-coefficient-functor-or-finite-coupling-prior-runner.md", ["PCF2368_1_vertical_silence", "ROUTE2368_2_ppn_component", "NEXT2368_0_selected"], "parallel source-side coefficient functor and finite coupling anchors."),
        ("2369_alpha_cg", ROOT / "2369-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md", ["ACG2369_0_normal_form", "ART2369_5_verdict", "NEXT2369_0_selected"], "parallel local score object narrowed to alpha_cg/readout tail."),
        ("2370_readout_tail", ROOT / "2370-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md", ["ARZ2370_0_exact_zero", "EPS2370_5_verdict", "NEXT2370_0_selected"], "parallel readout-tail zero theorem/bound target."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(base_row(source_id=source_id, source_path=str(path), path_exists=path.exists(), required_needles=";".join(needles), found_needles=";".join(found), needles_found=path.exists() and len(found) == len(needles), role=role))
    return rows


def multimode_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="MMG2422_0_single_field_multimode", question="can scalar psi contain multiple local carriers?", result="YES_AS_WKB_ASYMPTOTIC_STRUCTURE", evidence="psi_epsilon=sum_I a_I cos(S_I/epsilon+theta_I)", implication="scalar-valued does not force rank-one covariance"),
        base_row(row_id="MMG2422_1_smoothed_covariance", question="does multimode psi recover carrier inventory?", result="CONDITIONALLY_YES", evidence="<partial_m psi partial_n psi>_smooth=sum_I W_I k_I,m k_I,n + R_mn", implication="temporal/radial carrier weights can be represented as smoothed phase covariance"),
        base_row(row_id="MMG2422_2_single_mode_no_go", question="does strict single-mode/static scalar derive local q branch?", result="NO", evidence="rank and C_tr constraints prevent independent C_tt/C_rr control over finite radial cell", implication="do not use single-mode scalar as local-GR derivation"),
        base_row(row_id="MMG2422_3_parent_permission", question="is the carrier inventory parent-signed?", result="NO_CURRENT_CLAIM", evidence="eikonal, weight transport, smoothing kernel, cone margins and q-selection not jointly parent-signed", implication="multimode route remains alive but nonclaim"),
        base_row(row_id="MMG2422_4_verdict", question="multimode permission or scalar-only no-go?", result="MULTIMODE_CONDITIONALLY_OPEN_SCALAR_ONLY_NO_GO_AVOIDED", evidence="2276/2422 synthesis", implication="advance to transport/exchange locks, not scalar-dead-end"),
    ]


def transport_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="WTG2422_0_eikonal", object="carrier phases", formula="(partial_t S_I)^2-c^2|grad S_I|^2=0", status="DERIVED_CONDITIONALLY_FROM_EQUATION_LEVEL_WKB", blocker="parent action status of damping/nonlinear term still guarded"),
        base_row(row_id="WTG2422_1_weight_transport", object="carrier weights", formula="partial_t(W_I S_I,t)-c^2 div(W_I grad S_I)+gamma W_I S_I,t=R_W,I", status="EQUATION_LEVEL_TRANSPORT_FORM", blocker="gamma is not action-signed for constant gamma without open-system/dissipation principle"),
        base_row(row_id="WTG2422_2_independent_transport", object="q-zero preservation", formula="transport evolves W_T and W_R along their own rays", status="DOES_NOT_SELECT_Q_ZERO", blocker="no temporal/radial weight-lock by independent transport alone"),
        base_row(row_id="WTG2422_3_q_source", object="transport source", formula="S_q=Dq=-D C_tt/(1-C_tt)+D C_rr/(1+C_rr)", status="EXACT_SOURCE_DEFINITION", blocker="S_q is not zero unless exchange law closes"),
        base_row(row_id="WTG2422_4_verdict", object="WKB transport gate", formula="transport is real structure but not local-GR theorem", status="Q_SELECTION_BLOCKED", blocker="need exchange law or q residual operator"),
    ]


def exchange_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="EXG2422_0_q_zero_surface", object="q=0 target", formula="(1-C_tt)(1+C_rr)=1", status="EXACT_IDENTITY", claim_effect="target surface identified"),
        base_row(row_id="EXG2422_1_tangent_lock", object="q-zero preservation", formula="on q=0: D C_rr = D C_tt/(1-C_tt)^2", status="EXACT_EXCHANGE_CONDITION", claim_effect="the coupling lock is now one equation"),
        base_row(row_id="EXG2422_2_weight_form", object="carrier weights", formula="D(s_R W_R K_R^2)=D(s_T W_T Omega_T^2)/(1-s_T W_T Omega_T^2)^2", status="EXACT_WEIGHT_EXCHANGE_TARGET", claim_effect="parent dynamics must enforce this if q=0 is theorem"),
        base_row(row_id="EXG2422_3_underdetermination", object="exchange sources E_T,E_R", formula="general E_R=(1+C_rr)*(E_T/(1-C_tt)-S_q_free)", status="UNDERDETERMINED_WITHOUT_PARENT_BUDGET", claim_effect="cannot choose exchange after the fact"),
        base_row(row_id="EXG2422_4_verdict", object="carrier exchange law", formula="exact target known; parent source not derived", status="PARENT_EXCHANGE_UNSIGNED", claim_effect="local GR remains blocked"),
    ]


def phase_operator_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="POL2422_0_random_phase", target="random nonlinear phase exchange", result="DIRECTED_EXCHANGE_ZERO", evidence="<N(sum a_J cos phi_J) sin(phi_I)>=0 by parity for independent uniform phases", consequence="generic smoothing/random nonlinearity cannot be magic coupling"),
        base_row(row_id="POL2422_1_locked_phase", target="locked phase or memory distribution", result="OPEN_UNSOURCED", evidence="E_A^lambda=lambda <P_A N(psi)>_locked", consequence="needs P_locked, P_T/P_R projectors, amplitude scaling, regularization"),
        base_row(row_id="POL2422_2_boundary_memory", target="boundary/memory exchange", result="OPEN_UNSOURCED", evidence="E_A^bdry=<J_A^cell · n> or memory-kernel transfer", consequence="needs cell current, no-flux/reciprocal-flux theorem or memory kernel"),
        base_row(row_id="POL2422_3_transport_operator", target="first-order q relaxation", result="TEMPLATE_ONLY", evidence="Dq+kappa_q q=S_q", consequence="needs kappa_q owner, sign and boundary/observable map"),
        base_row(row_id="POL2422_4_elliptic_operator", target="local stiffness residual", result="TEMPLATE_ONLY", evidence="L_q q=-nabla_i(Z_q nabla^i q)+M_q^2 q=S_q", consequence="needs Z_q>0, M_q^2>0, boundary conditions and P_obs"),
        base_row(row_id="POL2422_5_verdict", target="phase exchange or q operator", result="PHASE_LOCK_OR_OPERATOR_OWNER_NEXT", evidence="random exchange rejected; locked/operator routes open", consequence="next target 2423"),
    ]


def parallel_local_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="PLS2422_0_coefficient_functor", branch="source-side coefficients", status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED", retained_blocker="visible coefficients descend only if parent target category/functor is signed"),
        base_row(row_id="PLS2422_1_jq", branch="j_q numerator", status="LIVE_SOURCE_SIDE_BOTTLENECK", retained_blocker="hidden-visible coefficient leakage and readout/source weights can feed q_R"),
        base_row(row_id="PLS2422_2_alpha_cg", branch="PPN alpha_cg score object", status="NORMAL_FORM_LOCKED_NOT_SCORE_READY", retained_blocker="same-branch owner, Z_X, M_X^2, S_PPN, common frame and readout tails missing"),
        base_row(row_id="PLS2422_3_alpha_readout", branch="readout tail", status="EXACT_CONDITIONAL_ZERO_NOT_ACTIVE", retained_blocker="Delta_cal, Delta_PPN, C_feedback, C_protocol and epsilon_sigma source-feedback missing"),
        base_row(row_id="PLS2422_4_empirical", branch="R10/PPN/clock/orbital tests", status="DEFER", retained_blocker="no parent-owned q prediction vector or completed local residual vector yet"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2422_0_scalar_no_go", gate="scalar-only route impossible", passed=False, reason="single-mode scalar fails, but multimode WKB scalar remains conditionally viable"),
        base_row(gate_id="CG2422_1_parent_multimode", gate="parent MTS signs multimode carrier inventory", passed=False, reason="WKB/multiphase interpretation is conditional; kernel/transport/weights not fully parent-signed"),
        base_row(gate_id="CG2422_2_parent_transport", gate="WKB transport is parent-action theorem", passed=False, reason="damping/action consistency and nonlinear residual terms remain guarded"),
        base_row(gate_id="CG2422_3_exchange_law", gate="carrier exchange law preserves q=0", passed=False, reason="exact condition known but E_T/E_R budget and coefficients underdetermined"),
        base_row(gate_id="CG2422_4_phase_exchange", gate="nonlinear phase exchange closes coupling", passed=False, reason="random phases give directed zero; locked distribution/projectors missing"),
        base_row(gate_id="CG2422_5_q_operator", gate="q residual operator maps S_q to bounded q_R", passed=False, reason="kappa_q/L_q/G_q, positivity, boundary and observable maps unsourced"),
        base_row(gate_id="CG2422_6_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, reason="no q-zero exchange theorem and no finite q_R bound"),
        base_row(gate_id="CG2422_7_public_GitHub", gate="public/GitHub update allowed", passed=False, reason="private nonclaim derivation checkpoint"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2422_0_result", decision="SCALAR_MULTIMODE_ROUTE_CONDITIONALLY_OPEN", rationale="one scalar can carry multiple WKB phase modes, so scalar-valued does not kill the carrier route", consequence="do not demote local branch to scalar-only no-go"),
        base_row(decision_id="DEC2422_1_single_mode", decision="STRICT_SINGLE_MODE_SCALAR_INSUFFICIENT", rationale="one coherent/static scalar cannot generically tune C_tt/C_rr while keeping C_tr silent", consequence="single-mode arguments cannot derive local GR"),
        base_row(decision_id="DEC2422_2_transport", decision="WKB_TRANSPORT_REAL_BUT_NOT_Q_ZERO", rationale="carrier weights obey transport, but independent W_T/W_R transport does not preserve q=0", consequence="exchange law is the coupling lock"),
        base_row(decision_id="DEC2422_3_exchange", decision="EXACT_Q_ZERO_EXCHANGE_CONDITION_KNOWN", rationale="on q=0, D C_rr = D C_tt/(1-C_tt)^2", consequence="any parent exchange law must hit this target"),
        base_row(decision_id="DEC2422_4_nonlinear", decision="RANDOM_NONLINEAR_EXCHANGE_REJECTED", rationale="independent random phase averaging gives zero directed exchange by parity", consequence="need locked phase/memory distribution or q residual operator"),
        base_row(decision_id="DEC2422_5_next", decision="PHASE_LOCK_DISTRIBUTION_OR_Q_OPERATOR_OWNER_NEXT", rationale="this is the least ambiguous remaining coupling gate", consequence="target 2423"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2422_0_selected", selection_status="selected", target_file="2423-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md", target_script="scripts/Y5_R2FR_phase_lock_distribution_or_q_residual_operator_owner_2423.py", objective="derive a parent phase-lock/memory distribution and carrier projectors that make nonlinear exchange nonzero and test the exact q-zero exchange condition, or derive the owner of kappa_q/L_q/G_q for residual q_R bounds", success_condition="locked-phase coefficients close q-zero exchange, or a sourced q residual operator maps S_q to q_R without claiming a pass", do_not_do="do not use random smoothing/nonlinearity as magic exchange, choose E_T/E_R after the fact, or claim GR from equation-level transport"),
        base_row(route_id="NEXT2422_1_parallel", selection_status="held_parallel", target_file="2423b-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md", target_script="scripts/Y5_R2FR_source_feedback_epsilon_sigma_or_PPN_gauge_bound_row_2423b.py", objective="continue source/readout local-score branch by proving epsilon_sigma/source-feedback zero or staging first alpha_readout bound row", success_condition="readout/support/projector descent closes or alpha_readout stays finite nonclaim with source-backed bound inputs", do_not_do="do not treat PPN target ceiling as an MTS prediction"),
    ]


def copy_branch_rows(multimode: list[dict[str, Any]], gates: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["multimode_gate"], BRANCH_COPIES["queue"], multimode),
        ("branch_wep", OUTPUTS["claim_gates"], BRANCH_COPIES["branch_wep"], gates),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2422_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2422_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    multimode_text = " ".join(str(row) for row in data["multimode_gate"])
    rows.append(base_row(validation_id="VAL2422_02_multimode_open", status="PASS" if "MULTIMODE_CONDITIONALLY_OPEN_SCALAR_ONLY_NO_GO_AVOIDED" in multimode_text and "rank-one covariance" in multimode_text else "FAIL", detail="scalar multimode route open, strict single-mode no-go separated"))

    transport_text = " ".join(str(row) for row in data["transport_gate"])
    rows.append(base_row(validation_id="VAL2422_03_transport_gate", status="PASS" if "S_q=Dq" in transport_text and "DOES_NOT_SELECT_Q_ZERO" in transport_text else "FAIL", detail="WKB transport recorded and q-zero selection blocked"))

    exchange_text = " ".join(str(row) for row in data["exchange_gate"])
    rows.append(base_row(validation_id="VAL2422_04_exchange_condition", status="PASS" if "D C_rr = D C_tt/(1-C_tt)^2" in exchange_text and "UNDERDETERMINED_WITHOUT_PARENT_BUDGET" in exchange_text else "FAIL", detail="exact exchange condition derived and not promoted"))

    phase_text = " ".join(str(row) for row in data["phase_operator"])
    rows.append(base_row(validation_id="VAL2422_05_phase_operator", status="PASS" if "DIRECTED_EXCHANGE_ZERO" in phase_text and "PHASE_LOCK_OR_OPERATOR_OWNER_NEXT" in phase_text else "FAIL", detail="random phase exchange rejected and locked/operator route selected"))

    parallel_text = " ".join(str(row) for row in data["parallel_local"])
    rows.append(base_row(validation_id="VAL2422_06_parallel_local_retained", status="PASS" if "j_q" in parallel_text and "alpha_readout" in parallel_text and "DEFER" in parallel_text else "FAIL", detail="source/readout local-score branch retained without shortcut"))
    rows.append(base_row(validation_id="VAL2422_07_claim_gates_blocked", status="PASS" if all(not bool(row["passed"]) for row in data["claim_gates"]) else "FAIL", detail="all local-GR/public claim gates remain blocked"))
    rows.append(base_row(validation_id="VAL2422_08_next_target", status="PASS" if any(row["route_id"] == "NEXT2422_0_selected" and "phase-lock" in row["target_file"] for row in data["next_target"]) else "FAIL", detail="2423 phase-lock/q-operator target selected"))

    parse_details: list[str] = []
    parse_ok_all = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    rows.append(base_row(validation_id="VAL2422_09_csv_parse", status="PASS" if parse_ok_all else "FAIL", detail="; ".join(parse_details)))

    branch_ok = all(row["copied"] and row["parse_ok"] for row in data["branch_copies"])
    rows.append(base_row(validation_id="VAL2422_10_branch_copies", status="PASS" if branch_ok else "FAIL", detail=";".join(str(row["target_path"]) for row in data["branch_copies"])))

    generated = all_generated_rows(data)
    no_claim_flags = all(str(row.get("valid_for_claim")).lower() == "false" and str(row.get("claim_allowed")).lower() == "false" for row in generated)
    rows.append(base_row(validation_id="VAL2422_11_no_claim_flags", status="PASS" if no_claim_flags else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    formalization_dirty = formalization_has_2422_artifacts()
    rows.append(base_row(validation_id="VAL2422_12_formalization_untouched_by_outputs", status="PASS" if not formalization_dirty else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(base_row(validation_id="VAL2422_OVERALL", status="PASS" if overall else "FAIL", detail="2422 keeps scalar multimode permission conditionally open, rejects scalar-only dead end and random nonlinear exchange, records exact q-zero exchange condition, and selects phase-lock distribution or q residual operator owner next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2422 — Parent Multimode Permission Or Scalar-Only No-Go

## Result

This is a real forward step, not a loop.

The scalar-only dead end is avoided: a scalar-valued `psi` can still carry a high-frequency multimode/WKB phase inventory, and after smoothing it gives the carrier covariance form needed for the q-lift:

`C_mn = sum_I W_I k_I,m k_I,n + R_mn`.

But that does **not** derive local GR.  The WKB transport law exists at equation level, yet independent temporal/radial carrier transport does not preserve `q=0`.  The exact coupling lock is now:

`S_q = Dq = -D C_tt/(1-C_tt) + D C_rr/(1+C_rr)`,

and on the q-zero surface:

`D C_rr = D C_tt/(1-C_tt)^2`.

Generic nonlinear/random phase averaging does not save the theory; directed exchange vanishes by phase parity for independent random phases.  The live route is narrower: derive a parent phase-lock/memory distribution with carrier projectors, or derive a real `kappa_q/L_q/G_q` residual operator that maps `S_q` into bounded finite `q_R`.

No local-GR/Newton claim, no empirical pass, no GitHub/public claim.

## Source Register

{md_table(data["source_register"], ["source_id", "path_exists", "needles_found", "role", "source_path"])}

## Multimode Permission Gate

{md_table(data["multimode_gate"], ["row_id", "question", "result", "evidence", "implication"])}

## WKB Transport / q Selection Gate

{md_table(data["transport_gate"], ["row_id", "object", "formula", "status", "blocker"])}

## Carrier Exchange Condition Gate

{md_table(data["exchange_gate"], ["row_id", "object", "formula", "status", "claim_effect"])}

## Phase Exchange Or q Operator Ledger

{md_table(data["phase_operator"], ["row_id", "target", "result", "evidence", "consequence"])}

## Parallel Source / Readout Ledger

{md_table(data["parallel_local"], ["row_id", "branch", "status", "retained_blocker"])}

## Claim Gates

{md_table(data["claim_gates"], ["gate_id", "gate", "passed", "reason"])}

## Decision Ledger

{md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"])}

## Generated Files

{md_table([base_row(output_id=key, path=str(path), exists=path.exists()) for key, path in OUTPUTS.items()], ["output_id", "path", "exists"])}

## Branch Copies

{md_table(data["branch_copies"], ["copy_id", "copied", "parse_ok", "row_count", "target_path"])}

## Validation

{md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Practical Status

- The route is healthier than scalar-only collapse: multimode scalar covariance can represent the q carrier inventory.
- The local-GR bottleneck is now precise: parent dynamics must make carrier exchange tangent to `q=0`, or `S_q` must be bounded through a sourced q residual operator.
- The easy nonlinear hope is rejected: random phases do not generate the required directed exchange.
- The next attack is `2423`: phase-lock/memory distribution or q residual operator owner.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    remove_pycache()
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "multimode_gate": multimode_gate_rows(),
        "transport_gate": transport_gate_rows(),
        "exchange_gate": exchange_gate_rows(),
        "phase_operator": phase_operator_rows(),
        "parallel_local": parallel_local_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in data.items():
        write_csv(OUTPUTS[key], rows)

    data["branch_copies"] = copy_branch_rows(data["multimode_gate"], data["claim_gates"], data["decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2422_OVERALL")
    print(f"{overall['validation_id']},{overall['status']},{overall['detail']}")
    print(str(DOC))


if __name__ == "__main__":
    main()
