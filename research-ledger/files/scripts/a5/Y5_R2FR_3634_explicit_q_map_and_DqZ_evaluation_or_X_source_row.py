from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3634"
BRANCH_ID = "MTS_R2FR_Y5_EXPLICIT_Q_MAP_DQZ_EVALUATION_OR_X_SOURCE_ROW_3634"
DOC = ROOT / "3634-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-X-source-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3634_SOURCE_REGISTER.csv",
        "q_norm_definition": RESIDUALS / "P8_Y5_R2FR_3634_QMAP_COMPONENT_NORM.csv",
        "no_cancellation_lemma": RESIDUALS / "P8_Y5_R2FR_3634_DQZ_NO_CANCELLATION_LEMMA.csv",
        "component_evaluation": RESIDUALS / "P8_Y5_R2FR_3634_DQZ_COMPONENT_EVALUATION.csv",
        "filled_dqz_row": RESIDUALS / "P8_Y5_R2FR_3634_FILLED_DQZ_ROW.csv",
        "branch_split": RESIDUALS / "P8_Y5_R2FR_3634_STRICT_VS_RESIDUAL_BRANCH_SPLIT.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3634_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3634_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3634_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_DqZ_component_norm_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3634_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3633",
            RESIDUALS / "P8_Y5_R2FR_3633_NEXT_TARGET.csv",
            "explicit ordinary-matter quotient q",
            "3633 handoff: construct q enough to evaluate Dq[partial_Z].",
        ),
        (
            "q_map_3633",
            RESIDUALS / "P8_Y5_R2FR_3633_CANDIDATE_Q_MAP.csv",
            "QMAP3633_4_excluded_residual_fibre",
            "candidate q components and excluded fibre condition.",
        ),
        (
            "dqz_target_3633",
            RESIDUALS / "P8_Y5_R2FR_3633_BOUND_PACK_FILL_TARGETS.csv",
            "Dq_Z_norm",
            "first selected non-vague target from the absent-pole audit.",
        ),
        (
            "q_audit_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
            "PARTIAL_PRIOR_CONTRACT",
            "prior q audit showing q is not computable yet.",
        ),
        (
            "field_chart_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
            "R_phys",
            "field chart separating visible quotient data from residual vector candidates.",
        ),
        (
            "dq_tests_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
            "DQT1667_1_Z_normal_form",
            "existing Dq_Z test says Z basis and q dependence are missing.",
        ),
        (
            "retained_dq_leaks_1667",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
            "Dq_Z_norm",
            "older retained Dq leak row now upgraded from missing formula to component norm.",
        ),
        (
            "status_3633",
            RESIDUALS / "P8_Y5_R2FR_3633_STATUS.csv",
            "Dq_Z_norm",
            "3633 status selecting Dq_Z_norm as the next exact test.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def q_norm_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "norm_id": "NORM3634_0_full_definition",
            "component": "Dq_Z_norm",
            "definition": "||Dq[partial_Z]||_Q^2 = w_G||partial_Z G_obs||^2 + w_M||partial_Z M_obs||^2 + w_T||partial_Z Theta_obs||^2 + w_B||partial_Z B_obs||^2",
            "normalization": "each norm is dimensionless after dividing by its arena reference scale; weights w_i are strictly positive",
            "zero_condition": "Dq_Z_norm=0 iff every component derivative is zero",
            "no_cancellation_guard": "positive weights forbid source/boundary cancellation against geometry",
            "status": "EXACT_COMPONENT_NORM_DEFINITION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM3634_1_geometry",
            "component": "G_obs=(e_obs,g_obs,nabla_obs)",
            "definition": "||partial_Z G_obs||^2_G",
            "normalization": "coframe/metric/connection norm in observed local frame",
            "zero_condition": "partial_Z e_obs=0, partial_Z g_obs=0, and partial_Z nabla_obs=0",
            "no_cancellation_guard": "geometry cannot cancel source or boundary components",
            "status": "COMPONENT_DEFINED_NOT_EVALUATED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM3634_2_source_readout",
            "component": "M_obs=(mu_obs, GM readout, source mass, orbit/Hamiltonian normalization)",
            "definition": "||partial_Z M_obs||^2_M",
            "normalization": "dimensionless source/readout norm after dividing by measured reference mass or Hamiltonian scale",
            "zero_condition": "partial_Z mu_obs=0 and no Z-dependence in GM calibration/source charge",
            "no_cancellation_guard": "source coupling cannot be hidden by a geometry zero",
            "status": "COMPONENT_DEFINED_NOT_EVALUATED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM3634_3_clock_marker",
            "component": "Theta_obs=(clock map, constants, material markers)",
            "definition": "||partial_Z Theta_obs||^2_T",
            "normalization": "dimensionless marker/clock norm",
            "zero_condition": "clock rate, constants, and material labels are q-owned or externally fixed",
            "no_cancellation_guard": "clock/marker leakage is independently bounded",
            "status": "COMPONENT_DEFINED_NOT_EVALUATED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM3634_4_boundary_projector",
            "component": "B_obs=(boundary class, Pi_M, reference term)",
            "definition": "||partial_Z B_obs||^2_B",
            "normalization": "dimensionless boundary/projector norm on compact local collar",
            "zero_condition": "Q_boundary[partial_Z]=0, exact, or proper and Pi_M has no Z leakage",
            "no_cancellation_guard": "edge charge is not allowed to compensate bulk silence",
            "status": "COMPONENT_DEFINED_NOT_EVALUATED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def no_cancellation_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "lemma_id": "LEM3634_0_positive_norm",
            "statement": "For positive weights and positive-definite component norms, Dq_Z_norm=0 is equivalent to componentwise zero.",
            "derivation": "A sum of nonnegative terms w_i||A_i||^2 can vanish only when each A_i vanishes.",
            "use_in_framework": "This prevents a fake local-GR pass where source or boundary leakage is cancelled by a tuned geometry sign.",
            "status": "PROVED_CONDITIONAL_ON_NORM_CHOICE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lemma_id": "LEM3634_1_component_zero_contract",
            "statement": "The strict quotient route must prove four separate zeros: geometry, source/readout, clock/marker, and boundary/projector.",
            "derivation": "Dq[partial_Z]=(partial_Z G_obs, partial_Z M_obs, partial_Z Theta_obs, partial_Z B_obs).",
            "use_in_framework": "A geometry-only proof is insufficient; the coupling/source block is a first-class target, not an afterthought.",
            "status": "PROVED_AS_DEFINITIONAL_SPLIT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "lemma_id": "LEM3634_2_failure_mode",
            "statement": "If any component derivative is nonzero or unsigned, Z cannot be promoted to an absent quotient fibre for local tests.",
            "derivation": "nonzero partial_Z component implies Dq[partial_Z] != 0, so Z is visible to at least one physical readout.",
            "use_in_framework": "The branch then moves to J_X/Dq leak coefficient rows instead of another theorem-zero attempt.",
            "status": "PROVED_DECISION_RULE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def component_evaluation_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "component_id": "DQZ3634_0_geometry",
            "component": "partial_Z G_obs",
            "current_best_case": "zero if the observed metric/coframe are defined wholly from q and Z is only representative fibre",
            "live_evidence": "field-chart 1667 gives partial alignment but not action/coframe ownership",
            "evaluation": "UNSIGNED_ZERO_CANDIDATE",
            "needed_to_close": "explicit e_obs(Phi), g_obs(Phi), and nabla_obs(Phi) with no Z dependence",
            "opens_if_fails": "R0 direct geometry and PPN geometry residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DQZ3634_1_source_readout",
            "component": "partial_Z M_obs",
            "current_best_case": "zero only if source mass, GM calibration, Hamiltonian normalization, and orbit readouts descend through q",
            "live_evidence": "retained Dsource_readout leak row and 3629 source-coupling obstruction",
            "evaluation": "OPEN_HIGHEST_PRESSURE_COMPONENT",
            "needed_to_close": "derive source/readout descent or compute nonzero source leakage",
            "opens_if_fails": "J_X, R1 WEP source charge, R10/R11 source normalization, orbital/clock leakage",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DQZ3634_2_clock_marker",
            "component": "partial_Z Theta_obs",
            "current_best_case": "zero if clocks/constants/material markers are fixed standards or q-owned",
            "live_evidence": "retained Dtheta_marker leak row",
            "evaluation": "OPEN",
            "needed_to_close": "explicit clock and marker map independent of Z",
            "opens_if_fails": "clock redshift, constants/material marker, EM/fine-structure style channels",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DQZ3634_3_boundary_projector",
            "component": "partial_Z B_obs",
            "current_best_case": "zero/exact/proper if boundary class and Pi_M are q-owned",
            "live_evidence": "3632 boundary charge owner missing; boundary_projector_Dq_leak retained",
            "evaluation": "OPEN",
            "needed_to_close": "boundary charge and projector silence on local collar",
            "opens_if_fails": "preferred-frame alpha3/xi, memory flux, source normalization edge rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DQZ3634_4_verdict",
            "component": "Dq_Z_norm",
            "current_best_case": "exact norm formula exists and prevents cancellations",
            "live_evidence": "component zeros are not signed, especially source/readout",
            "evaluation": "FORMULA_FILLED_BUT_NOT_THEOREM_ZERO",
            "needed_to_close": "prove all four components zero or score first nonzero component",
            "opens_if_fails": "source/readout descent or J_X residual row is the next attack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def filled_dqz_row(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "DQL3634_0_Dq_Z_filled_formula",
            "source_prior_row": "DQL1667_0_Dq_Z;DQL3632_0_Dq_Z",
            "symbol": "Dq_Z_norm",
            "value_or_formula": "sqrt(w_G||partial_Z G_obs||^2 + w_M||partial_Z M_obs||^2 + w_T||partial_Z Theta_obs||^2 + w_B||partial_Z B_obs||^2)",
            "units": "dimensionless after component normalization",
            "no_cancellation_guard": "w_G,w_M,w_T,w_B > 0; all component norms positive-definite",
            "zero_condition": "partial_Z G_obs=partial_Z M_obs=partial_Z Theta_obs=partial_Z B_obs=0",
            "fill_level": "symbolic_formula_filled_not_numeric_not_claim",
            "score_status": "not_scoreable_until_component_zeros_or_bounds",
            "source_paths": f"{RESIDUALS / 'P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv'};{RESIDUALS / 'P8_Y5_R2FR_3634_QMAP_COMPONENT_NORM.csv'}",
            "next_measurement": "source/readout component partial_Z M_obs is highest pressure",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def branch_split_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "branch_id_local": "BR3634_A_strict_quotient",
            "condition": "all four component derivatives vanish and boundary charge is zero/exact/proper",
            "result": "Z is absent quotient fibre; J_Z/J_X=0; no X/Z pole; R10 X-sector silent",
            "current_status": "BEST_ROUTE_NOT_SIGNED",
            "next_test": "prove partial_Z M_obs=0 after geometry candidate is written",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id_local": "BR3634_B_source_leak",
            "condition": "geometry component may vanish but source/readout or marker component is nonzero/unsigned",
            "result": "coupling is physical or closure-assumed; open J_X and source-charge residual rows",
            "current_status": "MOST_LIKELY_LIVE_BOTTLENECK",
            "next_test": "derive source/readout descent or fill J_X with units/projection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id_local": "BR3634_C_boundary_leak",
            "condition": "bulk components vanish but boundary/projector component survives",
            "result": "bulk no-pole theorem is not enough; preferred-frame/source normalization edge channels remain",
            "current_status": "BOUNDARY_RISK_OPEN",
            "next_test": "prove Q_boundary[partial_Z]=0/exact/proper or score boundary_flux_X",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id_local": "BR3634_D_physical_XZ",
            "condition": "Z/X is retained as a physical local mode",
            "result": "must score Z_X, M_X^2, K_X, qbar_XT, Qbar_XH, lambda_X, J_X",
            "current_status": "FALLBACK_EMPIRICAL_BRANCH",
            "next_test": "do not claim GR reduction; run residual coefficient acquisition",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3634_0_formula_filled",
            "decision": "Dq_Z_norm is no longer just a missing placeholder; it has an exact positive component norm with a no-cancellation lemma.",
            "status": "SYMBOLIC_ROW_FILLED",
            "next_action": "evaluate the four component derivatives instead of repeating broad q-owner audits",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3634_1_coupling_focus",
            "decision": "The source/readout component partial_Z M_obs is the highest-pressure coupling target because geometry-only verticality cannot kill source charges.",
            "status": "SOURCE_READOUT_NEXT",
            "next_action": "attempt source/readout descent theorem or open J_X row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3634_2_claim_ceiling",
            "decision": "No local-GR or R10 pass is promoted because component zeros are not signed.",
            "status": "NO_CLAIM",
            "next_action": "keep strict quotient as route A and residual coefficient scoring as route B",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "DQZ_COMPONENT_NORM_DERIVED_SOURCE_READOUT_NEXT",
            "summary": "3634 converts Dq_Z_norm from a missing placeholder into an exact positive component norm. The no-cancellation lemma says local verticality requires four zeros, not a tuned sum: geometry, source/readout, clock/marker, and boundary/projector. The strongest next attack is the coupling block partial_Z M_obs, because source/readout leakage reopens J_X even if geometry looks vertical.",
            "claim_ceiling": "no DqZ theorem-zero, local-GR, PPN, R10/R11, WEP, clock, or Newton claim is allowed from 3634",
            "useful_result": "the coupling bottleneck is now a calculable component: partial_Z M_obs=0 or J_X/source-charge residuals must be scored",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3634_0",
            "target_doc": "3635-Y5-R2FR-source-readout-descent-zero-or-JX-residual-row.md",
            "target_script": "scripts/Y5_R2FR_3635_source_readout_descent_zero_or_JX_residual_row.py",
            "objective": "try to prove partial_Z M_obs=0 for source mass, GM calibration, Hamiltonian normalization, and orbit/readout maps; if not, create the first J_X/source-charge residual row with units/projection requirements",
            "success_gate": "either source/readout descent is theorem-zero from q, or a nonclaim J_X/Dsource_readout row is executable enough to drive R1/R10/R11 comparisons later",
            "reason": "3634 identifies source/readout coupling as the highest-pressure term in Dq_Z_norm.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "Dq_Z_norm_component_gate",
            "canonical_status": "SYMBOLIC_FORMULA_FILLED_NOT_ZERO",
            "usable_result": "Dq_Z_norm has an exact no-cancellation form: sqrt(w_G||partial_Z G_obs||^2+w_M||partial_Z M_obs||^2+w_T||partial_Z Theta_obs||^2+w_B||partial_Z B_obs||^2). Local verticality requires all four zeros.",
            "hard_block": "prove partial_Z M_obs=0 or open J_X/source-charge residual row",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    norm: list[dict[str, object]],
    lemma: list[dict[str, object]],
    components: list[dict[str, object]],
    filled: list[dict[str, object]],
    branches: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3634 Y5 R2FR explicit q-map and DqZ evaluation or X source row",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The first real calculation target is now in a form we can actually attack:\n\n"
                "```text\n"
                "||Dq[partial_Z]||_Q^2 = w_G||partial_Z G_obs||^2\n"
                "                       + w_M||partial_Z M_obs||^2\n"
                "                       + w_T||partial_Z Theta_obs||^2\n"
                "                       + w_B||partial_Z B_obs||^2,\n"
                "w_i > 0.\n"
                "```\n\n"
                "Therefore `Dq_Z_norm=0` requires componentwise zero. No cancellation trick is allowed. This is useful because it says exactly where the coupling hunt goes next: the source/readout block `partial_Z M_obs`."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## q-map component norm",
            table(norm, ["norm_id", "component", "definition", "normalization", "zero_condition", "no_cancellation_guard", "status"]),
            "## No-cancellation lemma",
            table(lemma, ["lemma_id", "statement", "derivation", "use_in_framework", "status"]),
            "## Component evaluation",
            table(components, ["component_id", "component", "current_best_case", "live_evidence", "evaluation", "needed_to_close", "opens_if_fails"]),
            "## Filled DqZ row",
            table(filled, ["row_id", "symbol", "value_or_formula", "units", "zero_condition", "fill_level", "score_status", "next_measurement"]),
            "## Branch split",
            table(branches, ["branch_id_local", "condition", "result", "current_status", "next_test"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3634_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3634_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3634_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3634_3_csv_parse", parse_ok, "; ".join(details))

    norm = read_csv(outputs["q_norm_definition"])
    lemma = read_csv(outputs["no_cancellation_lemma"])
    components = read_csv(outputs["component_evaluation"])
    filled = read_csv(outputs["filled_dqz_row"])
    branches = read_csv(outputs["branch_split"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3634_4_norm_formula_has_all_components", any("w_G" in row["definition"] and "w_M" in row["definition"] and "w_T" in row["definition"] and "w_B" in row["definition"] for row in norm), "DqZ component norm includes geometry/source/marker/boundary")
    add("VAL3634_5_no_cancellation_proved", any("sum of nonnegative terms" in row["derivation"] for row in lemma), "positive no-cancellation lemma present")
    add("VAL3634_6_componentwise_verdict", any(row["component_id"] == "DQZ3634_4_verdict" and row["evaluation"] == "FORMULA_FILLED_BUT_NOT_THEOREM_ZERO" for row in components), "component verdict keeps no-claim state")
    add("VAL3634_7_filled_dqz_not_missing_formula", bool(filled) and "MISSING" not in filled[0]["value_or_formula"] and "w_G" in filled[0]["value_or_formula"], "DqZ row formula filled, not placeholder")
    add("VAL3634_8_source_readout_selected", any(row["status"] == "SOURCE_READOUT_NEXT" for row in decisions) and "partial_Z M_obs" in status[0]["useful_result"], "source/readout coupling selected next")
    add("VAL3634_9_branch_split_complete", len(branches) == 4 and any(row["branch_id_local"] == "BR3634_B_source_leak" for row in branches), "strict/source/boundary/physical branches present")
    add("VAL3634_10_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in norm + lemma + components + filled + branches + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3634*")) if FORMALIZATION.exists() else []
    add("VAL3634_11_no_formalization_leak", not leaks, "no 3634 files in formalization-workbench")
    add("VAL3634_12_next_target_written", bool(nxt) and "3635" in nxt[0]["target_doc"], "3635 source/readout target written")
    add("VAL3634_13_doc_written", DOC.exists() and "partial_Z M_obs" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with source/readout target")
    add("VAL3634_14_canonical_status_written", outputs["canonical_status"].exists() and "SYMBOLIC_FORMULA_FILLED_NOT_ZERO" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical DqZ status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    norm = q_norm_rows(t)
    lemma = no_cancellation_rows(t)
    components = component_evaluation_rows(t)
    filled = filled_dqz_row(t)
    branches = branch_split_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["q_norm_definition"], norm)
    write_csv(outputs["no_cancellation_lemma"], lemma)
    write_csv(outputs["component_evaluation"], components)
    write_csv(outputs["filled_dqz_row"], filled)
    write_csv(outputs["branch_split"], branches)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, norm, lemma, components, filled, branches, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3634 validation failed: {failures}")
    print(f"wrote 3634 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
