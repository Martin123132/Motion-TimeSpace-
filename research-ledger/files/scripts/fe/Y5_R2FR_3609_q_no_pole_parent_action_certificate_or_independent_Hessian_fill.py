from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3609"
BRANCH_ID = "MTS_R2FR_Y5_Q_NO_POLE_PARENT_ACTION_OR_INDEPENDENT_HESSIAN_3609"
DOC = ROOT / "3609-Y5-R2FR-q-no-pole-parent-action-certificate-or-independent-Hessian-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3608": (RESIDUALS / "P8_Y5_R2FR_3608_NEXT_TARGET.csv", "NEXT3608_0"),
        "status_3608": (RESIDUALS / "P8_Y5_R2FR_3608_STATUS.csv", "Q_OPERATOR_NORMAL_FORM_DERIVED_BUT_NOT_OWNED"),
        "route_3608": (RESIDUALS / "P8_Y5_R2FR_3608_Q_OPERATOR_ROUTE_AUDIT.csv", "QROUTE3608_1_no_pole_delete_route"),
        "input_3608": (RESIDUALS / "P8_Y5_R2FR_3608_Q_OPERATOR_INPUT_ROWS.csv", "QIN3608_0_Zq"),
        "no_pole_2755": (RESIDUALS / "P8_Y5_R2FR_2755_NO_POLE_ACTIVATION_GATE.csv", "NP2755_0_exact_contract"),
        "quotient_theorem_2486": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_THEOREM_ATTEMPT.csv", "THM2486_0_chain_rule_descent"),
        "vertical_ledger_2486": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2486_2_q_private"),
        "matter_descent_2486": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv", "MD2486_0_chain_rule"),
        "readout_order_2486": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_READOUT_ORDER_GATE.csv", "RO2486_0_variation_before_readout"),
        "coefficient_descent_2486": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_COEFFICIENT_DESCENT_GATE.csv", "CD2486_0_descent_theorem"),
        "qmap_3604": (RESIDUALS / "P8_Y5_R2FR_3604_QMAP_VERTICAL_THEOREM.csv", "DQV3604_3_vq_candidate"),
        "qap_status_3520": (RESIDUALS / "P8_EM_quotient_action_derives_q_normal_form_status.csv", "STAT3520_0_qap_to_normal_form"),
        "local_gr_map_3534": (RESIDUALS / "P8_local_GR_MTS_variable_quotient_double_zero_status.csv", "STAT3534_0_variable_map"),
        "hessian_pack_2755": (RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv", "IQH2755_0_Zq"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3609_SOURCE_REGISTER.csv",
        "no_pole_hessian_proof": RESIDUALS / "P8_Y5_R2FR_3609_NO_POLE_HESSIAN_PROOF.csv",
        "parent_action_certificate": RESIDUALS / "P8_Y5_R2FR_3609_PARENT_ACTION_CERTIFICATE.csv",
        "independent_hessian_fill_rows": RESIDUALS / "P8_Y5_R2FR_3609_INDEPENDENT_HESSIAN_FILL_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3609_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3609_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3609_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_q_no_pole_parent_action_certificate_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3609_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def proof_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QNP3609_0_setup",
            "parent quotient setup",
            "Let pi:C->C_red be the parent quotient/readout map, let v_q in ker(Dpi), and assume S_vis=Sbar∘pi plus descending boundary/matter/readout maps on one branch.",
            "DEFINITIONAL_SETUP",
            "This fixes the branch where q can be deleted instead of bounded.",
            "no_pole_2755",
        ),
        (
            "QNP3609_1_first_variation",
            "vertical first variation",
            "D S_vis[v_q] = D Sbar[Dpi(v_q)] = 0.",
            "PROVED_CONDITIONALLY",
            "A vertical representative direction cannot source the parent equations if the action descends through pi.",
            "quotient_theorem_2486",
        ),
        (
            "QNP3609_2_hessian_row",
            "on-shell Hessian row",
            "D^2(Sbar∘pi)[v_q,w]=D^2Sbar[Dpi(v_q),Dpi(w)] + DSbar[D^2pi(v_q,w)], so on a reduced solution and Dpi(v_q)=0 the row/column vanish.",
            "PROVED_CONDITIONALLY_WITH_ONSHELL_CAVEAT",
            "This is the actual no-pole algebra: the q row is zero before inversion, provided reduced equations and quotient descent are both true.",
            "no_pole_2755",
        ),
        (
            "QNP3609_3_schur_complement",
            "physical propagator after quotient",
            "The physical Hessian is the Hessian on C_red, not the singular unreduced block. Since q is not in C_red, no physical G_q pole appears in q-basic observables.",
            "PROVED_CONDITIONALLY",
            "Gauge-fixing may add an auxiliary inverse in the representative sector, but q-basic readouts have zero coupling to it.",
            "readout_order_2486",
        ),
        (
            "QNP3609_4_matter_boundary",
            "source and boundary silence",
            "D S_matter[v_q]=D B_boundary[v_q]=D O_arena[v_q]=0 if each map factors through the same pi.",
            "PROVED_CONDITIONALLY",
            "This is what removes J_q, boundary tails and P_arena leakage rather than merely setting a coefficient to zero.",
            "matter_descent_2486",
        ),
        (
            "QNP3609_5_failure_modes",
            "when no-pole proof fails",
            "If q has a parent kinetic term, non-descending boundary charge, non-q-basic matter coefficient, or arena readout coupling, then q is physical and must be Hessian-bounded.",
            "EXACT_COUNTERCONDITION",
            "This prevents deleting q by words: any non-descending row reactivates Z_q, M_q^2, J_q and P_arena.",
            "input_3608",
        ),
        (
            "QNP3609_6_current_application",
            "current MTS application",
            "The theorem is mathematically proved as a conditional no-pole lemma, but current MTS does not parent-sign pi, v_q, descent, or boundary silence.",
            "THEOREM_PROVED_CERTIFICATE_UNSIGNED",
            "Use the theorem as the target certificate; do not claim q deletion yet.",
            "qmap_3604",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "proof_id": proof_id,
            "piece": piece,
            "statement": statement,
            "proof_status": proof_status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for proof_id, piece, statement, proof_status, consequence, source_id in rows
    ]


def certificate_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QCERT3609_0_parent_pi",
            "parent quotient object pi",
            "pi or q_parent must be defined before variation with domain, units, field list and visible/reduced target.",
            "UNSIGNED",
            "P8_EM and 2486 provide candidate quotient language, not a parent-owned single pi.",
            "qap_status_3520",
        ),
        (
            "QCERT3609_1_vertical_generator",
            "v_q in ker(Dpi)",
            "Dpi[v_q]=0 plus actual residual basis and component Dq matrix on one branch.",
            "UNSIGNED",
            "3604 marks v_q as highest priority but not certified; R_AB is rejected under current observer map.",
            "qmap_3604",
        ),
        (
            "QCERT3609_2_first_class_degree_count",
            "first-class/removed degree count",
            "Omega, constraint generator, bracket closure and removed canonical-pair count must identify q as representative, not physical.",
            "UNSIGNED",
            "No current row owns the symplectic/constraint package for q deletion.",
            "vertical_ledger_2486",
        ),
        (
            "QCERT3609_3_action_descent",
            "parent action descent",
            "S_vis=Sbar∘pi on the local branch, including measure/coframe and allowed counterterms.",
            "PARTIAL_CONDITIONAL",
            "QAP gives conditional normal-form progress, but parent action/object-language exhaustion remains unsigned.",
            "qap_status_3520",
        ),
        (
            "QCERT3609_4_matter_descent",
            "ordinary matter descent",
            "S_matter=Sbar_matter∘pi with no hidden source-only prefactor, no species marker and same observed coframe.",
            "UNSIGNED",
            "2486 proves the chain-rule gate but source prefactors/constants owner remain open.",
            "matter_descent_2486",
        ),
        (
            "QCERT3609_5_coefficient_descent",
            "visible constants/couplings descent",
            "G_parent, kappa, alpha_EM, clock/mass/binding coefficients and source weights must be q-basic or parent normal-form slots.",
            "UNSIGNED",
            "Coefficient descent theorem is exact conditional but not parent-signed for every visible coefficient.",
            "coefficient_descent_2486",
        ),
        (
            "QCERT3609_6_readout_boundary_descent",
            "readout and boundary silence",
            "O_arena=Obar∘pi and B_boundary=Bbar∘pi, with projectors fixed before variation or retained as explicit obstructions.",
            "UNSIGNED",
            "Readout-order guard exists; boundary/reference/projector silence remains open.",
            "readout_order_2486",
        ),
        (
            "QCERT3609_7_local_GR_compatibility",
            "local GR reduction compatibility",
            "Deleting q must leave the EH/Hilbert/Newton branch rather than deleting the observed metric/coframe source.",
            "PARTIAL_MAP_ONLY",
            "3534 maps MTS variables into a local-EH quotient kernel but does not yet parent-own the double-zero origin.",
            "local_gr_map_3534",
        ),
        (
            "QCERT3609_8_activation",
            "activate q no-pole deletion",
            "All certificate rows above must pass simultaneously on one branch.",
            "NOT_ACTIVATED",
            "The no-pole theorem is proven conditionally, but the MTS parent certificate is not signed.",
            "no_pole_2755",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": certificate_id,
            "clause": clause,
            "required_evidence": required_evidence,
            "current_status": current_status,
            "current_read": current_read,
            "source_path": p[source_id],
            "clause_passed": current_status == "PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for certificate_id, clause, required_evidence, current_status, current_read, source_id in rows
    ]


def hessian_fill_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QHESS3609_0_Zq",
            "Z_q",
            "Z_q := coefficient of (1/2) sqrt(-g) h_q^{mu nu} nabla_mu q nabla_nu q in delta_q^2 S_parent after branch normalization.",
            "operator_normalization",
            "REQUIRED_IF_Q_NOT_DELETED",
            "numeric/source-backed parent Hessian row or theorem zero",
            "hessian_pack_2755",
        ),
        (
            "QHESS3609_1_Mq2",
            "M_q^2",
            "M_q^2 := second derivative of the effective q potential plus branch curvature-mass terms in the same normalization as Z_q.",
            "mass_squared",
            "REQUIRED_IF_Q_NOT_DELETED",
            "numeric/source-backed mass gap or massless/no-hair theorem",
            "hessian_pack_2755",
        ),
        (
            "QHESS3609_2_lambda",
            "lambda_q",
            "lambda_q=sqrt(Z_q/M_q^2) for positive massive branch; if M_q^2=0, replace by massless domain/no-hair boundary theorem.",
            "length",
            "DERIVED_FORMULA_INPUTS_MISSING",
            "Z_q and M_q^2 in one unit convention",
            "hessian_pack_2755",
        ),
        (
            "QHESS3609_3_domain",
            "D(L_q)",
            "D(L_q) is the local function space, support class and regularity class on which L_q is inverted.",
            "domain_statement",
            "REQUIRED_IF_Q_NOT_DELETED",
            "domain and branch boundary conditions before norms",
            "input_3608",
        ),
        (
            "QHESS3609_4_boundary_operator",
            "B_q^bdry",
            "Boundary variation terms define the self-adjoint extension or finite boundary/source-tail rows of L_q.",
            "boundary_statement",
            "REQUIRED_IF_Q_NOT_DELETED",
            "fixed boundary class or explicit tail bound",
            "readout_order_2486",
        ),
        (
            "QHESS3609_5_Jq",
            "J_q",
            "J_q := -delta S_parent/delta q excluding the declared Weyl forcing terms; includes matter, source, boundary and readout residues.",
            "source_density",
            "REQUIRED_IF_Q_NOT_DELETED",
            "source-zero theorem or finite source-tail bound",
            "matter_descent_2486",
        ),
        (
            "QHESS3609_6_BqWeyl",
            "B_qWeyl",
            "B_qWeyl is the parent coefficient of a linear q-Weyl forcing channel; zero only follows from quotient/no-spurion certificate.",
            "parent_normalized",
            "REQUIRED_FOR_LINEAR_ROUTE",
            "parent coefficient or activated no-spurion/quotient theorem",
            "route_3608",
        ),
        (
            "QHESS3609_7_DqWeyl2",
            "D_qWeyl2",
            "D_qWeyl2 is the parent coefficient of q C_abcd C^abcd or the no-higher-curvature theorem-zero switch.",
            "parent_normalized_length_power",
            "REQUIRED_FOR_QUADRATIC_GUARD",
            "parent coefficient or activated no-tower theorem",
            "hessian_pack_2755",
        ),
        (
            "QHESS3609_8_Parena",
            "P_arena[q]",
            "P_arena maps q(r) or q[x] into R10 alpha(lambda), PPN gamma/beta/alpha_i, clocks, orbital precession or source-GM residuals.",
            "arena_projection",
            "REQUIRED_FOR_ANY_TEST",
            "arena projection with units and no fitted-GM/readout laundering",
            "input_3608",
        ),
        (
            "QHESS3609_9_runner_law",
            "finite q residual law",
            "||P_arena q|| <= ||P_arena G_q|| (|B_qWeyl| ||P*C|| + |D_qWeyl2| ||C^2|| + ||J_q|| + ||bdry||).",
            "bound_law",
            "FORMULA_READY_INPUTS_MISSING",
            "all preceding rows source-backed in one normalization",
            "status_3608",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "formula_or_definition": formula,
            "units": units,
            "current_status": current_status,
            "required_to_activate": required,
            "source_path": p[source_id],
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, formula, units, current_status, required, source_id in rows
    ]


def decision_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QDEC3609_0_math_theorem",
            "conditional no-pole theorem",
            "PASS_CONDITIONAL",
            "The Hessian proof is complete: quotient descent plus on-shell reduced equations delete the q row from physical propagators.",
            "no_pole_2755",
        ),
        (
            "QDEC3609_1_mts_certificate",
            "MTS parent certificate",
            "FAIL_CURRENT",
            "pi, v_q, first-class degree count, descent and boundary/readout silence are not all signed on one branch.",
            "qmap_3604",
        ),
        (
            "QDEC3609_2_delete_route",
            "delete q operator",
            "NOT_ACTIVATED",
            "Do not delete G_q from B_qWeyl/D_qWeyl2 runners yet.",
            "route_3608",
        ),
        (
            "QDEC3609_3_bound_route",
            "independent Hessian route",
            "FORMULAS_FILLED_NOT_NUMERIC",
            "The exact rows needed for Z_q, M_q^2, lambda, domain, boundary, J_q, coefficients and P_arena are now defined.",
            "hessian_pack_2755",
        ),
        (
            "QDEC3609_4_next_route",
            "next best attack",
            "SELECTED_PARENT_PI_OR_ZQ",
            "Either construct the single parent pi/v_q certificate from actual MTS symbols, or extract Z_q and J_q from the parent action candidate.",
            "local_gr_map_3534",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for decision_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "NO_POLE_THEOREM_PROVED_CONDITIONALLY_MTS_CERTIFICATE_UNSIGNED_HESSIAN_ROWS_FILLED",
            "strongest_result": "3609 proves the exact parent-action no-pole lemma at Hessian level: for S=Sbar∘pi, v_q in ker(Dpi), and on-shell reduced equations, the q Hessian row/column vanish and q-basic observables contain no physical q pole.",
            "decision": "do not claim q deletion for MTS yet; the theorem is real but pi/v_q/descent/boundary certificate rows are unsigned. If this certificate cannot be built, use the independent Hessian fill rows to bound q as physical.",
            "framework_progress": "The fork is now mathematically clean: either q is a quotient representative and disappears from physical local GR, or q is a physical residual with explicit Z_q/M_q/J_q/P_arena rows.",
            "still_missing": "parent-owned pi, actual v_q in ker(Dpi), first-class degree count, action/matter/coefficient/readout/boundary descent, or numeric/source-backed Hessian rows",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["no_pole_2755"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3609_0",
            "target_doc": "3610-Y5-R2FR-parent-pi-vq-certificate-or-Zq-Jq-extraction.md",
            "target_script": "scripts/Y5_R2FR_3610_parent_pi_vq_certificate_or_Zq_Jq_extraction.py",
            "objective": "attempt the concrete parent pi/v_q certificate from actual MTS symbols; if any clause fails, immediately extract or bound Z_q and J_q from the parent action candidate instead of producing another target ledger",
            "success_gate": "must either sign pi and v_q in ker(Dpi) with descent clauses, or produce source-backed/nonclaim numeric-ready rows for Z_q and J_q",
            "reason": "3609 proves the no-pole math; the remaining work is attaching it to actual MTS symbols or treating q as a physical residual",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    proof: list[dict[str, object]],
    cert: list[dict[str, object]],
    hessian: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3609_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3609 source paths exist"))
    validations.append(("VAL3609_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3609 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3609_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3609 csv outputs written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3609_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(
        (
            "VAL3609_4_hessian_proof_present",
            any(row["proof_id"] == "QNP3609_2_hessian_row" and "PROVED_CONDITIONALLY" in str(row["proof_status"]) for row in proof),
            "on-shell Hessian row no-pole proof is present",
        )
    )
    required_cert = {
        "parent quotient object pi",
        "v_q in ker(Dpi)",
        "first-class/removed degree count",
        "parent action descent",
        "ordinary matter descent",
        "visible constants/couplings descent",
        "readout and boundary silence",
        "activate q no-pole deletion",
    }
    validations.append(
        (
            "VAL3609_5_certificate_complete",
            required_cert.issubset({str(row["clause"]) for row in cert}),
            "all no-pole parent certificate clauses represented",
        )
    )
    required_hessian = {"Z_q", "M_q^2", "lambda_q", "D(L_q)", "B_q^bdry", "J_q", "B_qWeyl", "D_qWeyl2", "P_arena[q]"}
    validations.append(
        (
            "VAL3609_6_hessian_rows_filled",
            required_hessian.issubset({str(row["symbol"]) for row in hessian}),
            "independent q Hessian fill rows present",
        )
    )
    validations.append(
        (
            "VAL3609_7_no_deletion_claim",
            any(row["certificate_id"] == "QCERT3609_8_activation" and row["current_status"] == "NOT_ACTIVATED" for row in cert),
            "q no-pole deletion remains unactivated for current MTS",
        )
    )
    validations.append(
        (
            "VAL3609_8_no_claim_flags",
            not any(str(row.get("claim_allowed", "False")) == "True" or str(row.get("valid_for_claim", "False")) == "True" for table in [proof, cert, hessian, decisions, status, next_target] for row in table),
            "all generated physics rows remain nonclaim",
        )
    )
    validations.append(
        (
            "VAL3609_9_next_target_selected",
            next_target[0]["next_id"] == "NEXT3609_0",
            "3610 pi/vq certificate or Zq/Jq extraction target selected",
        )
    )
    formalization_leaks: list[str] = []
    if FORMALIZATION.exists():
        for pattern in ["*3609*", "P8_Y5_R2FR_3609*", "P8_Y5_BRR545_3609*"]:
            formalization_leaks.extend(str(path) for path in FORMALIZATION.rglob(pattern) if ".venv" not in path.parts and "__pycache__" not in path.parts)
    validations.append(
        (
            "VAL3609_10_formalization_workbench_untouched",
            len(formalization_leaks) == 0,
            "no 3609 checkpoint output appears in formalization-workbench outside package/venv noise",
        )
    )
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    proof: list[dict[str, object]],
    cert: list[dict[str, object]],
    hessian: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    status_row = status[0]
    lines = [
        "# 3609 - q no-pole parent-action certificate or independent Hessian fill",
        "",
        "## Verdict",
        "3609 makes the fork honest and mathematical.",
        "",
        "The no-pole side is no longer hand-waving: if `S=Sbar∘pi`, `v_q in ker(Dpi)`, and the reduced equations hold, then",
        "",
        "`D^2(Sbar∘pi)[v_q,w]=D^2Sbar[Dpi(v_q),Dpi(w)] + DSbar[D^2pi(v_q,w)] = 0`",
        "",
        "for every physical direction `w`.  Therefore the `q` row/column is not part of the physical Hessian on the quotient, and q-basic observables contain no physical `G_q` pole.",
        "",
        "But the current MTS corpus does not yet sign the parent `pi`, actual `v_q in ker(Dpi)`, first-class degree count, matter/coefficient/readout descent, and boundary silence on one branch.  So this is a proved conditional theorem, not a local-GR claim.",
        "",
        "If that certificate cannot be built, the alternative is now explicit: treat `q` as physical and fill `Z_q`, `M_q^2`, `lambda_q`, `J_q`, boundary, coefficient, and `P_arena` rows.",
        "",
        "## No-Pole Hessian Proof",
    ]
    for row in proof:
        lines.append(f"- `{row['proof_id']}` / `{row['piece']}`: {row['proof_status']} - {row['consequence']}")
    lines.extend(["", "## Parent Certificate"])
    for row in cert:
        lines.append(f"- `{row['certificate_id']}` / `{row['clause']}`: {row['current_status']} - {row['current_read']}")
    lines.extend(["", "## Independent Hessian Fill"])
    for row in hessian:
        lines.append(f"- `{row['input_id']}` / `{row['symbol']}`: {row['current_status']} - {row['formula_or_definition']}")
    lines.extend(["", "## Decision Gates"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}` / `{row['gate']}`: {row['status']} - {row['consequence']}")
    lines.extend(
        [
            "",
            "## Status",
            f"- `{status_row['status']}`: {status_row['strongest_result']}",
            f"- Decision: {status_row['decision']}",
            f"- Framework progress: {status_row['framework_progress']}",
            f"- Still missing: {status_row['still_missing']}",
            "",
            "## Validation",
        ]
    )
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    next_row = next_target[0]
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_row['next_id']}` -> `{next_row['target_doc']}`",
            f"- Objective: {next_row['objective']}",
            f"- Success gate: {next_row['success_gate']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    source_rows = source_register_rows(source_map)
    proof = proof_rows(source_map)
    cert = certificate_rows(source_map)
    hessian = hessian_fill_rows(source_map)
    decisions = decision_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], source_rows)
    write_csv(out_paths["no_pole_hessian_proof"], proof)
    write_csv(out_paths["parent_action_certificate"], cert)
    write_csv(out_paths["independent_hessian_fill_rows"], hessian)
    write_csv(out_paths["decision_gates"], decisions)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, proof, cert, hessian, decisions, status, next_target)
    write_doc(proof, cert, hessian, decisions, status, next_target, validation)
    write_csv(out_paths["validation"], validation)

    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        for failure in failures:
            print(f"{failure['validation_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote 3609 q no-pole/Hessian outputs under {RESIDUALS}")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
