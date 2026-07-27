from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3202-Y5-R2FR-Kperp-elliptic-boundary-operator-or-Bobs-residual-acquisition-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3202_INPUTS.csv"
OPERATOR = OUT / "P8_Y5_R2FR_3202_KPERP_OPERATOR_DERIVATION_AUDIT.csv"
TRACE_RANK = OUT / "P8_Y5_R2FR_3202_TRACE_RANK_AUDIT.csv"
COERCIVITY = OUT / "P8_Y5_R2FR_3202_COERCIVITY_AND_ZERO_MODE_GATE.csv"
BOBS_FALLBACK = OUT / "P8_Y5_R2FR_3202_BOBS_FALLBACK_TRIGGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3202_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3202_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "formalization":
        return FW / relative_path
    if location == "post_checkpoint":
        return ROOT / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lower_terms = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lower_terms):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def b(value: bool) -> str:
    return "true" if value else "false"


def matrix_rank(matrix: list[list[float]], tolerance: float = 1.0e-10) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = max(range(rank, rows), key=lambda row: abs(work[row][column]))
        if abs(work[pivot][column]) <= tolerance:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        for entry in range(column, columns):
            work[rank][entry] /= pivot_value
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            for entry in range(column, columns):
                work[row][entry] -= factor * work[rank][entry]
        rank += 1
        if rank == rows:
            break
    return rank


def symmetric_eigenvalues(matrix: list[list[float]]) -> list[float]:
    work = [row[:] for row in matrix]
    size = len(work)
    for _ in range(100):
        pivot_row = 0
        pivot_column = 1
        max_value = 0.0
        for row in range(size):
            for column in range(row + 1, size):
                value = abs(work[row][column])
                if value > max_value:
                    max_value = value
                    pivot_row = row
                    pivot_column = column
        if max_value < 1.0e-14:
            break
        app = work[pivot_row][pivot_row]
        aqq = work[pivot_column][pivot_column]
        apq = work[pivot_row][pivot_column]
        angle = 0.5 * __import__("math").atan2(2.0 * apq, aqq - app)
        cosine = __import__("math").cos(angle)
        sine = __import__("math").sin(angle)
        for index in range(size):
            if index not in (pivot_row, pivot_column):
                aip = work[index][pivot_row]
                aiq = work[index][pivot_column]
                work[index][pivot_row] = cosine * aip - sine * aiq
                work[pivot_row][index] = work[index][pivot_row]
                work[index][pivot_column] = sine * aip + cosine * aiq
                work[pivot_column][index] = work[index][pivot_column]
        work[pivot_row][pivot_row] = cosine**2 * app - 2.0 * sine * cosine * apq + sine**2 * aqq
        work[pivot_column][pivot_column] = sine**2 * app + 2.0 * sine * cosine * apq + cosine**2 * aqq
        work[pivot_row][pivot_column] = 0.0
        work[pivot_column][pivot_row] = 0.0
    return sorted(work[index][index] for index in range(size))


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left_row[index] * right[index][column] for index in range(len(right))) for column in range(len(right[0]))]
        for left_row in left
    ]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def matrix_text(matrix: list[list[float]]) -> str:
    return ";".join(",".join(f"{value:.6g}" for value in row) for row in matrix)


SOURCES = [
    {
        "input_id": "SRC3202_00",
        "location": "post_checkpoint",
        "relative_path": "3201-Y5-R2FR-MTS-matter-stress-flux-four-channel-owner-or-rank-no-go-under-AX1090.md",
        "role": "3201 Kperp route and rank/source separation",
        "terms": ["K_hat/K_perp", "anti-cheat", "rank-four", "Kperp Owner Gates"],
    },
    {
        "input_id": "SRC3202_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3201_KPERP_ELLIPTIC_OWNER_GATE.csv",
        "role": "3201 Kperp owner gates",
        "terms": ["coercive", "zero_modes", "rank four", "open"],
    },
    {
        "input_id": "SRC3202_02",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "Kperp elliptic boundary-value law target",
        "terms": ["K_perp", "L_T", "coercive", "zero modes"],
    },
    {
        "input_id": "SRC3202_03",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "Khat/Kperp parent equation scaffold",
        "terms": ["K_hat", "q^nu", "Kperp", "local closure"],
    },
    {
        "input_id": "SRC3202_04",
        "location": "post_checkpoint",
        "relative_path": "3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090.md",
        "role": "fourth-order D2-dagger-D2 profile operator precedent",
        "terms": ["D2", "D2^dagger", "boundary", "EL"],
    },
    {
        "input_id": "SRC3202_05",
        "location": "post_checkpoint",
        "relative_path": "3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090.md",
        "role": "boundary momenta Pi0/Pi1 and need for boundary layer",
        "terms": ["Pi_1", "Pi_0", "boundary", "source action"],
    },
    {
        "input_id": "SRC3202_06",
        "location": "post_checkpoint",
        "relative_path": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090.md",
        "role": "rank-four positive pullback theorem",
        "terms": ["K0 = J^T", "rank(J)", "G_N", "positive"],
    },
]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "source_path": rel(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "generated_utc": now,
            }
        )
    return rows


def operator_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "operator_id": "OP3202_00_second_order_scalar",
            "candidate_operator": "L2 K = (-partial_rho^2 + m_T^2) K",
            "energy_form": "int[(partial_rho K)^2 + m_T^2 K^2] d rho",
            "boundary_trace_capacity": "two traces per scalar component: K(left), K(right)",
            "rank_owner_status": "INSUFFICIENT_FOR_C1_FOUR_SLOTS",
            "derivation_status": "standard_elliptic_template_not_parent_signed",
            "local_safety_comment": "can bound K_perp amplitude but cannot own derivative mismatch slots by itself",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "operator_id": "OP3202_01_two_component_second_order_tensor",
            "candidate_operator": "L2 K_A = J_A for A=1,2 independent tensor components",
            "energy_form": "sum_A int[(partial_rho K_A)^2 + m_A^2 K_A^2] d rho",
            "boundary_trace_capacity": "four traces total if two components are genuinely independent",
            "rank_owner_status": "CONDITIONAL_IF_PARENT_MAPS_VALUE_AND_DERIVATIVE_SLOTS_TO_INDEPENDENT_COMPONENTS",
            "derivation_status": "not_found_in_current_corpus",
            "local_safety_comment": "needs a parent projection from scalar C1 mismatch into two tensor channels",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "operator_id": "OP3202_02_fourth_order_clamped_trace",
            "candidate_operator": "L4 K = (-partial_rho^2 + m_T^2)^2 K or D2^dagger D2 analogue",
            "energy_form": "int[(K'')^2 + 2 m_T^2 (K')^2 + m_T^4 K^2] d rho",
            "boundary_trace_capacity": "four traces per component: K(left), K'(left), K(right), K'(right)",
            "rank_owner_status": "BEST_ABSTRACT_RANK4_OWNER",
            "derivation_status": "conditional_not_parent_signed",
            "local_safety_comment": "can own C1 interface data if parent action really contains this H2/coercive tensor sector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "operator_id": "OP3202_03_Bobs_residual_fallback",
            "candidate_operator": "no parent Kperp operator; use Bobs component ledger",
            "energy_form": "not applicable",
            "boundary_trace_capacity": "does not own rank; bounds leakage instead",
            "rank_owner_status": "FALLBACK_IF_PARENT_OPERATOR_NOT_DERIVED",
            "derivation_status": "ready_as_schema_not_score",
            "local_safety_comment": "requires M_H_ref and source-backed component rows before empirical scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def trace_rank_rows() -> list[dict[str, object]]:
    now = stamp()
    cases = [
        (
            "TRA3202_00_second_order_one_component",
            "single second-order component with only endpoint values",
            [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]],
            "rank two: endpoint values duplicate; derivative slots unowned",
            "REJECT_AS_C1_RANK_OWNER",
        ),
        (
            "TRA3202_01_second_order_cauchy_forced",
            "single second-order component forced to accept value+derivative data at both ends",
            [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
            "rank four algebraically, but rejected because generic Cauchy data overdetermine a second-order elliptic boundary problem",
            "REJECT_AS_NOT_WELL_POSED_FOR_L2",
        ),
        (
            "TRA3202_02_two_component_second_order",
            "two independent tensor components each own two endpoint traces",
            [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
            "rank four if the parent supplies two independent tensor channels and a slot-to-component map",
            "CONDITIONAL_COMPONENT_ROUTE",
        ),
        (
            "TRA3202_03_fourth_order_clamped",
            "fourth-order/coercive Kperp operator with clamped trace",
            [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
            "rank four naturally: H2 trace map contains value and normal derivative at both interfaces",
            "CONDITIONAL_BEST_ROUTE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for case_id, hypothesis, response, interpretation, status in cases:
        rank = matrix_rank(response)
        g_trace = [
            [2.0, 0.1, 0.0, 0.0],
            [0.1, 1.5, 0.0, 0.0],
            [0.0, 0.0, 2.0, 0.1],
            [0.0, 0.0, 0.1, 1.5],
        ]
        k0 = matmul(transpose(response), matmul(g_trace, response))
        eig = symmetric_eigenvalues(k0)
        rows.append(
            {
                "case_id": case_id,
                "hypothesis": hypothesis,
                "response_matrix_rows_semicolon_columns_comma": matrix_text(response),
                "rank": rank,
                "passes_rank4": b(rank == 4),
                "K0_pullback_matrix": matrix_text(k0),
                "min_eigenvalue_K0": f"{min(eig):.12g}",
                "positive_pullback_if_Gtrace_positive": b(min(eig) > 1.0e-10),
                "interpretation": interpretation,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def coercivity_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "COG3202_00_parent_origin",
            "gate": "parent_origin_of_L4_or_two_component_L2",
            "required_statement": "the Kperp operator follows from the parent MTS action/coarse-graining, not a hand-added boundary smoother",
            "current_status": "open",
            "why_it_matters": "without parent origin, rank-four ownership is closure-only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "COG3202_01_coercive_energy",
            "gate": "coercive_positive_energy",
            "required_statement": "energy controls H2 norm for L4, or H1 norms for two independent L2 tensor components",
            "current_status": "conditional_mathematical_pass_not_parent_signed",
            "why_it_matters": "positive energy gives the normal metric G_trace/G_N used by K0=J^T G J",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "COG3202_02_no_zero_modes",
            "gate": "no_zero_modes_or_fixed_gauge",
            "required_statement": "kernel of the operator is removed by boundary conditions, mass term, gauge fixing, or topology restriction",
            "current_status": "open",
            "why_it_matters": "zero modes make boundary response nonunique and can destroy positivity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "COG3202_03_parent_trace_map",
            "gate": "parent_trace_map_to_C1_slots",
            "required_statement": "parent variables map z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R) into Kperp trace slots with full rank",
            "current_status": "open",
            "why_it_matters": "rank four of a toy trace map is not enough unless actual MTS variables feed it",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "COG3202_04_local_safety",
            "gate": "local_safety_or_decay",
            "required_statement": "Kperp response decays, zeroes, or is bounded below PPN/orbital/clock residual limits in local domains",
            "current_status": "open",
            "why_it_matters": "a rank owner that leaves a large Kperp residual fails local GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bobs_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "fallback_id": "BOF3202_00",
            "trigger": "no parent origin for L4/two-component Kperp",
            "action": "demote finite-layer rank route to explicit closure and move to Bobs residual acquisition",
            "required_rows": "M_H_ref;B_obs_source_measure;B_obs_boundary_improvement;B_obs_projector_commutator;B_obs_total_no_cancellation",
            "status": "not_triggered_yet_derivation_route_still_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "fallback_id": "BOF3202_01",
            "trigger": "Kperp operator derived but local safety/decay gate fails",
            "action": "keep Kperp coefficients as residual components, not local-GR proof",
            "required_rows": "Kperp_amplitude_bound;domain_length;coercivity_constant;M_H_ref;PPN_projection",
            "status": "schema_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3202_00",
            "result": "ABSTRACT_KPERP_RANK4_OWNER_CONSTRUCTED_CONDITIONALLY",
            "claim_status": "NO_LOCAL_GR_NEWTON_PPN_OR_PARENT_RANK4_CLAIM",
            "decision": "a fourth-order/coercive Kperp trace operator can own the four C1 boundary slots in principle; a second-order scalar cannot; current corpus has not parent-signed the required operator or trace map",
            "best_next_route": "try to parent-sign the L4/two-component Kperp operator from K_MTS/K_hat action terms before switching to Bobs residual acquisition",
            "next_target": "3203-Y5-R2FR-parent-origin-of-Kperp-L4-operator-or-demote-to-Bobs-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    operators: list[dict[str, object]],
    traces: list[dict[str, object]],
    coercivity: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, OPERATOR, TRACE_RANK, COERCIVITY, BOBS_FALLBACK, DECISION]
    second_order_reject = next(row for row in traces if row["case_id"] == "TRA3202_00_second_order_one_component")
    forced_reject = next(row for row in traces if row["case_id"] == "TRA3202_01_second_order_cauchy_forced")
    l4_best = next(row for row in traces if row["case_id"] == "TRA3202_03_fourth_order_clamped")
    return [
        {
            "check_id": "VAL3202_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_01_second_order_scalar_rejected",
            "check": "single second-order scalar operator is not promoted to C1 rank-four owner",
            "pass": b(second_order_reject["rank"] == 2 and second_order_reject["status"] == "REJECT_AS_C1_RANK_OWNER"),
            "detail": second_order_reject["interpretation"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_02_forced_cauchy_rejected",
            "check": "rank-four Cauchy forcing of second-order elliptic problem is rejected",
            "pass": b(forced_reject["passes_rank4"] == "true" and forced_reject["status"] == "REJECT_AS_NOT_WELL_POSED_FOR_L2"),
            "detail": forced_reject["interpretation"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_03_l4_conditional_rank4_positive",
            "check": "fourth-order clamped trace row has rank four and positive pullback",
            "pass": b(l4_best["passes_rank4"] == "true" and l4_best["positive_pullback_if_Gtrace_positive"] == "true"),
            "detail": f"min_eig={l4_best['min_eigenvalue_K0']}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_04_parent_gates_not_claimed",
            "check": "parent origin, zero-mode, trace-map, and local-safety gates remain open/nonclaim",
            "pass": b(all(row["valid_for_claim"] == "false" for row in coercivity) and any(row["current_status"] == "open" for row in coercivity)),
            "detail": ";".join(f"{row['gate']}={row['current_status']}" for row in coercivity),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_05_bobs_fallback_staged",
            "check": "Bobs fallback trigger is staged if parent Kperp origin fails",
            "pass": b(len(fallbacks) >= 2 and all(row["valid_for_claim"] == "false" for row in fallbacks)),
            "detail": ";".join(row["trigger"] for row in fallbacks),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_06_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [operators, traces, coercivity, fallbacks, decisions] for row in table)),
            "detail": "no local-GR, Newton, PPN, or parent rank-four claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3202_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    operators: list[dict[str, object]],
    traces: list[dict[str, object]],
    coercivity: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3202 - Kperp Elliptic Boundary Operator Or Bobs Residual Acquisition Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, parent rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3202 finds the clean mathematical route:",
        "",
        "```text",
        "A single second-order scalar K_perp operator is too small.",
        "A forced second-order Cauchy rank-four map is not well-posed.",
        "A fourth-order/coercive K_perp trace operator can own value + derivative data at both interfaces.",
        "```",
        "",
        "So the finite-layer rank route is not dead. But it is still conditional because the current corpus has not parent-signed the required `L4`/tensor operator or the trace map from MTS variables.",
        "",
        "## Operator Audit",
        "",
    ]
    for row in operators:
        lines.append(f"- `{row['operator_id']}`: `{row['rank_owner_status']}` - {row['candidate_operator']}")
    lines.extend(["", "## Trace Rank Audit", ""])
    for row in traces:
        lines.append(
            f"- `{row['case_id']}`: rank `{row['rank']}`, positive pullback `{row['positive_pullback_if_Gtrace_positive']}` - {row['interpretation']}"
        )
    lines.extend(
        [
            "",
            "The useful theorem target is:",
            "",
            "```text",
            "L4 K_perp = (-partial_rho^2 + m_T^2)^2 K_perp,",
            "tr(K_perp) = (K_L, partial_n K_L, K_R, partial_n K_R),",
            "K0 = R^T G_trace R,",
            "rank(R)=4 and G_trace>0 => K0>0.",
            "```",
            "",
            "This is a conditional mathematical owner. It becomes physics only if the parent MTS action supplies `L4`, the trace map, and local safety.",
            "",
            "## Coercivity And Parent Gates",
            "",
        ]
    )
    for row in coercivity:
        lines.append(f"- `{row['gate_id']}`: `{row['gate']}` -> `{row['current_status']}`; {row['why_it_matters']}")
    lines.extend(["", "## Bobs Fallback", ""])
    for row in fallbacks:
        lines.append(f"- `{row['fallback_id']}`: if `{row['trigger']}`, then {row['action']}")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"`{decisions[0]['result']}`.",
            "",
            f"Claim status: `{decisions[0]['claim_status']}`.",
            "",
            f"Decision: {decisions[0]['decision']}",
            "",
            f"Best next route: {decisions[0]['best_next_route']}",
            "",
            "Next target:",
            "",
            "```text",
            str(decisions[0]["next_target"]),
            "```",
            "",
            "## Generated Evidence",
            "",
            f"- `{rel(INPUTS)}`",
            f"- `{rel(OPERATOR)}`",
            f"- `{rel(TRACE_RANK)}`",
            f"- `{rel(COERCIVITY)}`",
            f"- `{rel(BOBS_FALLBACK)}`",
            f"- `{rel(DECISION)}`",
            f"- `{rel(VALIDATION)}`",
            "",
            "## Validation",
            "",
        ]
    )
    for row in validations:
        lines.append(f"- `{row['check_id']}`: `{row['pass']}` - {row['detail']}")
    lines.extend(["", "All generated rows remain `valid_for_claim=false`.", ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = input_rows()
    operators = operator_rows()
    traces = trace_rank_rows()
    coercivity = coercivity_rows()
    fallbacks = bobs_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(OPERATOR, operators)
    write_csv(TRACE_RANK, traces)
    write_csv(COERCIVITY, coercivity)
    write_csv(BOBS_FALLBACK, fallbacks)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, operators, traces, coercivity, fallbacks, decisions)
    write_csv(VALIDATION, validations)
    write_doc(operators, traces, coercivity, fallbacks, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3202 validation failed: {detail}")
    print(f"3202 generated {DOC}")


if __name__ == "__main__":
    main()
