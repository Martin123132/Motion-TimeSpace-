from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3201-Y5-R2FR-MTS-matter-stress-flux-four-channel-owner-or-rank-no-go-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3201_INPUTS.csv"
SEPARATION = OUT / "P8_Y5_R2FR_3201_SOURCE_RANK_SEPARATION_LEMMA.csv"
CHANNELS = OUT / "P8_Y5_R2FR_3201_STRESS_FLUX_CHANNEL_AUDIT.csv"
RANK_TESTS = OUT / "P8_Y5_R2FR_3201_FOUR_CHANNEL_RANK_TESTS.csv"
KPERP_GATE = OUT / "P8_Y5_R2FR_3201_KPERP_ELLIPTIC_OWNER_GATE.csv"
QUEUE = OUT / "P8_Y5_R2FR_3201_COEFFICIENT_ACQUISITION_QUEUE.csv"
DECISION = OUT / "P8_Y5_R2FR_3201_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3201_VALIDATION.csv"


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


def matrix_text(matrix: list[list[float]]) -> str:
    return ";".join(",".join(f"{value:.6g}" for value in row) for row in matrix)


SOURCES = [
    {
        "input_id": "SRC3201_00",
        "location": "post_checkpoint",
        "relative_path": "3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090.md",
        "role": "3200 Poynting demotion and next K_hat/T_MTS route",
        "terms": ["Rank-four", "Poynting", "K_hat", "matter stress-flux"],
    },
    {
        "input_id": "SRC3201_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3200_STRESS_FLUX_J_COEFFICIENT_TEMPLATE.csv",
        "role": "16 J_Aa coefficient slots",
        "terms": ["J3200", "MISSING_PARENT_COEFFICIENT"],
    },
    {
        "input_id": "SRC3201_02",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3200_RANK_CONTRIBUTION_AUDIT.csv",
        "role": "3200 rank audit rows",
        "terms": ["quiet_Poynting", "full_parent_flux_toy", "rank"],
    },
    {
        "input_id": "SRC3201_03",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "K_MTS/K_hat/q^nu parent equation scaffold",
        "terms": ["K_hat owns", "q^nu", "K_MTS", "local closure"],
    },
    {
        "input_id": "SRC3201_04",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "source-silence and K_perp elliptic boundary theorem target",
        "terms": ["source-support", "K_perp", "coercive", "zero modes"],
    },
    {
        "input_id": "SRC3201_05",
        "location": "formalization",
        "relative_path": "15-conservation-to-effective-gamma.md",
        "role": "total conservation and exchange current",
        "terms": ["T_MTS", "Q^ν", "T_flux", "conserve"],
    },
    {
        "input_id": "SRC3201_06",
        "location": "post_checkpoint",
        "relative_path": "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
        "role": "B_obs boundary/source/projector flux decomposition",
        "terms": ["B_obs", "source_measure", "projector", "Current MTS"],
    },
    {
        "input_id": "SRC3201_07",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "Bobs acquisition and coupling/source-normalization blocker",
        "terms": ["coupling", "source-normalization", "Bobs", "MISSING"],
    },
    {
        "input_id": "SRC3201_08",
        "location": "post_checkpoint",
        "relative_path": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090.md",
        "role": "rank-four stiffness theorem",
        "terms": ["rank(J)", "G_N", "K0", "positive"],
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


def separation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "lemma_id": "SRL3201_00",
            "lemma": "local_source_rank_separation",
            "statement": "For local-GR/PPN safety, matter-source flux and EM/Poynting flux must be theorem-zero or residual-bounded; therefore they cannot simultaneously be the unsuppressed rank-four owner of C1 gluing.",
            "proof_sketch": "If a source flux supplies an O(1) independent row of J_Aa in a quiet local test, then the same channel contributes to B_obs/M_H unless a parent cancellation/zero theorem exists. No-cancellation scoring forbids using it as both a hidden rank owner and a vanished residual.",
            "consequence": "rank-four ownership must come from parent-internal tensor response K_hat/K_perp, or the finite-layer route remains closure-only.",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "SRL3201_01",
            "lemma": "trace_scalar_rank_limit",
            "statement": "The scalar trace Gamma_eff can control the isotropic/exchange projection but cannot by itself own all four C1 mismatch slots.",
            "proof_sketch": "A single scalar normal response produces at most one independent row unless a parent operator supplies independent boundary value and derivative channels; that additional structure is K_hat/K_perp, not Gamma_eff alone.",
            "consequence": "do not relabel Gamma_eff as the missing four-channel tensor owner.",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "SRL3201_02",
            "lemma": "Kperp_possible_owner_condition",
            "statement": "A tensor elliptic boundary problem for K_perp can own rank-four only if left/right value and normal-derivative responses are independent, coercive, parent-derived, and free of zero modes.",
            "proof_sketch": "The rank-four condition reduces to invertibility of the Dirichlet-to-Neumann/Jacobian map from z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R) into four normal tensor-flux components.",
            "consequence": "the next derivation should target the K_perp operator and boundary map, not matter/Poynting flux.",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def channel_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "channel_id": "CH3201_00",
            "channel": "Gamma_eff trace projection",
            "source_equation": "K_MTS^{mu nu} = -Gamma_eff g^{mu nu} + K_hat^{mu nu}",
            "rank_role": "scalar_trace_only",
            "max_rank_without_extra_operator": 1,
            "local_safety_role": "must become constant or gradient-bounded",
            "current_status": "not_four_channel_owner",
            "next_action": "keep as exchange/trace source, not rank-four gluing owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CH3201_01",
            "channel": "K_hat / K_perp tensor stress-flux",
            "source_equation": "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "rank_role": "only_plausible_internal_four_channel_owner",
            "max_rank_without_extra_operator": "unknown",
            "local_safety_role": "must vanish, be elliptically controlled, or be residual-bounded",
            "current_status": "promising_conditional_not_parent_derived",
            "next_action": "derive coercive tensor boundary operator L_T and its four-channel response map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CH3201_02",
            "channel": "matter source flux",
            "source_equation": "q^nu = kappa_GR Q^nu = nabla_mu K_matter^{mu nu}",
            "rank_role": "local_residual_or_source_support_channel",
            "max_rank_without_extra_operator": "at_most_source_dependent",
            "local_safety_role": "must be source-silent or tightly bounded in local tested domains",
            "current_status": "cannot_be_unsuppressed_rank_owner",
            "next_action": "place in Bobs/source-measure bound ledger unless a source-silence theorem closes",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CH3201_03",
            "channel": "boundary/source/projector B_obs flux",
            "source_equation": "B_obs^nu = B_GK^nu + B_corner^nu + B_source_measure^nu + B_projector^nu",
            "rank_role": "leakage_not_owner",
            "max_rank_without_extra_operator": "not_applicable",
            "local_safety_role": "must vanish by reduced Ward/no-flux theorem or enter absolute residual sum",
            "current_status": "live_residual_blocker",
            "next_action": "do not use leakage as rank owner; source/bound it",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "channel_id": "CH3201_04",
            "channel": "EM/Poynting flux",
            "source_equation": "T_EM^{0i} target component with S=E x H",
            "rank_role": "quiet_zero_or_bound_channel",
            "max_rank_without_extra_operator": 1,
            "local_safety_role": "zero/bound in quiet local tests",
            "current_status": "demoted_by_3200",
            "next_action": "keep in residual bound schema, not owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def rank_test_rows() -> list[dict[str, object]]:
    now = stamp()
    tests = [
        (
            "FRT3201_00_exact_local_silence",
            "Gamma constant, K_hat divergence zero, source/Poynting/Bobs zero",
            [[0.0, 0.0, 0.0, 0.0] for _ in range(4)],
            "exact local-GR silence route; no finite-layer rank owner needed, but current corpus has not proved the zeros",
            "EXACT_ZERO_ROUTE_TARGET_NOT_RANK_OWNER",
        ),
        (
            "FRT3201_01_trace_scalar_only",
            "Gamma_eff scalar trace response only",
            [[1.0, 0.0, -1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.5, 0.0, -0.5, 0.0], [0.0, 0.0, 0.0, 0.0]],
            "scalar trace creates duplicated value response and cannot own derivative slots",
            "RANK_NO_GO_FOR_TRACE_ONLY",
        ),
        (
            "FRT3201_02_source_silent_plus_radial_Khat",
            "source-silent local branch plus one radial K_hat scalar and normal derivative",
            [[1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0], [1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0]],
            "spherical/radial symmetry duplicates left-right rows and gives rank two",
            "RANK_NO_GO_UNLESS_BOUNDARY_MAP_BREAKS_DUPLICACY",
        ),
        (
            "FRT3201_03_unsuppressed_matter_flux",
            "arbitrary matter/source flux supplies extra rows",
            [[1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0], [0.4, 0.8, 0.3, 0.2], [0.1, 0.2, 0.7, 0.9]],
            "rank can improve if unsuppressed source rows are admitted, but that reopens local PPN/source-coupling residuals",
            "REJECT_AS_LOCAL_SAFETY_OWNER",
        ),
        (
            "FRT3201_04_Kperp_independent_boundary_map",
            "coercive K_perp tensor elliptic Dirichlet/Neumann map with independent left/right slots",
            [[1.2, 0.1, 0.0, 0.0], [0.0, 1.1, 0.2, 0.0], [0.0, 0.3, 1.3, 0.1], [0.2, 0.0, 0.0, 1.4]],
            "rank four is possible if and only if the parent tensor boundary map supplies independent coefficients",
            "CONDITIONAL_BEST_ROUTE_NOT_PROVED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for test_id, hypothesis, matrix, interpretation, status in tests:
        rank = matrix_rank(matrix)
        rows.append(
            {
                "test_id": test_id,
                "hypothesis": hypothesis,
                "J_matrix_rows_semicolon_columns_comma": matrix_text(matrix),
                "rank": rank,
                "passes_rank4": b(rank == 4),
                "interpretation": interpretation,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def kperp_gate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "KPG3201_00",
            "gate": "parent_tensor_operator",
            "required_statement": "derive L_T[K_perp]=J_perp from parent action/coarse-graining, not postulated boundary smoothing",
            "current_status": "open",
            "failure_if_missing": "K_perp owner remains closure-only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "KPG3201_01",
            "gate": "coercive_positive_operator",
            "required_statement": "prove L_T is coercive/positive in the local static weak-field limit",
            "current_status": "open",
            "failure_if_missing": "no positive G_flux/G_N and no controlled Green function",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "KPG3201_02",
            "gate": "no_zero_modes",
            "required_statement": "exclude homogeneous transverse tensor modes/topological modes on the local domain",
            "current_status": "open",
            "failure_if_missing": "rank can be deficient or boundary response nonunique",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "KPG3201_03",
            "gate": "independent_boundary_response",
            "required_statement": "the Dirichlet/Neumann response map from four C1 mismatch slots to four tensor-flux components has rank four",
            "current_status": "open",
            "failure_if_missing": "symmetric/radial response stays rank two or less",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "KPG3201_04",
            "gate": "local_safety_compatibility",
            "required_statement": "the same K_perp response either vanishes in exact local GR or is bounded below PPN/source-coupling limits",
            "current_status": "open",
            "failure_if_missing": "rank owner creates a measurable local residual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def queue_rows() -> list[dict[str, object]]:
    now = stamp()
    slots = [
        ("left_value", "Delta_F_L"),
        ("left_derivative", "Delta_Fprime_L"),
        ("right_value", "Delta_F_R"),
        ("right_derivative", "Delta_Fprime_R"),
    ]
    rows: list[dict[str, object]] = []
    for index, (response_component, mismatch_slot) in enumerate(slots):
        rows.append(
            {
                "queue_id": f"ACQ3201_{index:02d}",
                "target_coefficient_family": f"partial C_{response_component}/partial {mismatch_slot}",
                "preferred_owner": "K_hat/K_perp tensor boundary response",
                "required_derivation_or_data": "parent L_T operator, boundary condition, Green/Dirichlet-to-Neumann coefficient, units, source path",
                "fallback_if_not_derived": "absolute residual-bound row with no cancellation credit",
                "current_status": "MISSING_KPERP_PARENT_COEFFICIENT",
                "priority": index,
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    rows.append(
        {
            "queue_id": "ACQ3201_04",
            "target_coefficient_family": "B_obs_source_measure/projector/boundary leakage",
            "preferred_owner": "theorem-zero or source-backed bound, not rank owner",
            "required_derivation_or_data": "Bobs component rows with M_H_ref denominator and source paths",
            "fallback_if_not_derived": "keep local finite route unscored",
            "current_status": "MISSING_BOBS_SOURCE_ROWS",
            "priority": 4,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    )
    return rows


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3201_00",
            "result": "CURRENT_MTS_MATTER_FLUX_DOES_NOT_CLOSE_RANK4_OWNER",
            "claim_status": "NO_LOCAL_GR_NEWTON_PPN_OR_RANK4_CLAIM",
            "decision": "matter/source/Poynting flux cannot honestly be used as unsuppressed rank-four owner in local tests; only K_hat/K_perp tensor boundary response remains a plausible internal owner",
            "best_next_route": "derive the K_perp elliptic boundary operator and Dirichlet-to-Neumann rank map, or demote finite-layer rank route and proceed with Bobs residual acquisition",
            "next_target": "3202-Y5-R2FR-Kperp-elliptic-boundary-operator-or-Bobs-residual-acquisition-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    channels: list[dict[str, object]],
    ranks: list[dict[str, object]],
    kperp_gates: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, SEPARATION, CHANNELS, RANK_TESTS, KPERP_GATE, QUEUE, DECISION]
    rank4_rows = [row for row in ranks if row["passes_rank4"] == "true"]
    allowed_rank4_statuses = {"CONDITIONAL_BEST_ROUTE_NOT_PROVED", "REJECT_AS_LOCAL_SAFETY_OWNER"}
    current_rank_claims = [row for row in rank4_rows if row["status"] not in allowed_rank4_statuses]
    source_owner_rows = [row for row in ranks if row["status"] == "REJECT_AS_LOCAL_SAFETY_OWNER"]
    return [
        {
            "check_id": "VAL3201_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_01_separation_lemma_present",
            "check": "source/rank separation lemma is recorded",
            "pass": b(any(row["lemma"] == "local_source_rank_separation" for row in lemmas)),
            "detail": "source flux cannot be both hidden rank owner and vanished residual",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_02_channels_cover_internal_and_source_flux",
            "check": "K_hat, matter source, Bobs, and Poynting channels are audited",
            "pass": b({row["channel"] for row in channels} >= {"K_hat / K_perp tensor stress-flux", "matter source flux", "boundary/source/projector B_obs flux", "EM/Poynting flux"}),
            "detail": f"channels={len(channels)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_03_rank4_only_conditional",
            "check": "rank-four rows are either rejected source flux or conditional K_perp target",
            "pass": b(
                len(rank4_rows) == 2
                and any(row["status"] == "REJECT_AS_LOCAL_SAFETY_OWNER" for row in rank4_rows)
                and any(row["status"] == "CONDITIONAL_BEST_ROUTE_NOT_PROVED" for row in rank4_rows)
                and not current_rank_claims
            ),
            "detail": ";".join(f"{row['test_id']}={row['status']}" for row in rank4_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_04_source_flux_rejected_as_owner",
            "check": "unsuppressed matter/source flux is rejected as local rank owner",
            "pass": b(len(source_owner_rows) == 1),
            "detail": source_owner_rows[0]["interpretation"] if source_owner_rows else "missing rejection row",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_05_kperp_gates_open",
            "check": "Kperp owner gates are explicit and open",
            "pass": b(len(kperp_gates) >= 5 and all(row["current_status"] == "open" for row in kperp_gates)),
            "detail": ";".join(row["gate"] for row in kperp_gates),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_06_queue_nonclaim",
            "check": "coefficient acquisition queue is nonclaim and targets Kperp/Bobs rows",
            "pass": b(len(queue) >= 5 and all(row["valid_for_claim"] == "false" for row in queue)),
            "detail": ";".join(row["queue_id"] for row in queue),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_07_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [lemmas, channels, ranks, kperp_gates, queue, decisions] for row in table)),
            "detail": "no local-GR, Newton, PPN, or rank-four claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3201_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    lemmas: list[dict[str, object]],
    channels: list[dict[str, object]],
    ranks: list[dict[str, object]],
    gates: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3201 - MTS Matter Stress-Flux Four-Channel Owner Or Rank No-Go Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, rank-four proof, Maxwell/EM derivation, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3201 makes the important separation:",
        "",
        "```text",
        "matter/source/Poynting flux = local residual or theorem-zero channel;",
        "K_hat/K_perp tensor response = only plausible internal four-channel owner.",
        "```",
        "",
        "This is not a defeat. It is a useful anti-cheat theorem: the same source flux cannot be both the hidden rank-four machinery and also absent from local tests.",
        "",
        "## Separation Lemmas",
        "",
    ]
    for row in lemmas:
        lines.extend(
            [
                f"### {row['lemma_id']} - {row['lemma']}",
                "",
                row["statement"],
                "",
                f"- Proof sketch: {row['proof_sketch']}",
                f"- Consequence: {row['consequence']}",
                "",
            ]
        )
    lines.extend(["## Channel Audit", ""])
    for row in channels:
        lines.append(f"- `{row['channel_id']}`: `{row['channel']}` -> `{row['current_status']}`; next: {row['next_action']}")
    lines.extend(["", "## Rank Tests", ""])
    for row in ranks:
        lines.append(f"- `{row['test_id']}`: rank `{row['rank']}`, passes rank-four `{row['passes_rank4']}` - {row['interpretation']}")
    lines.extend(
        [
            "",
            "There are two rank-four rows, and neither is a claim: arbitrary unsuppressed source flux is rejected by local-safety separation, while the `K_perp` independent boundary-map row is only a conditional target.",
            "",
            "## Kperp Owner Gates",
            "",
        ]
    )
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: `{row['gate']}` - {row['required_statement']}")
    lines.extend(["", "## Acquisition Queue", ""])
    for row in queue:
        lines.append(f"- `{row['queue_id']}`: `{row['target_coefficient_family']}` -> `{row['current_status']}`")
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
            f"- `{rel(SEPARATION)}`",
            f"- `{rel(CHANNELS)}`",
            f"- `{rel(RANK_TESTS)}`",
            f"- `{rel(KPERP_GATE)}`",
            f"- `{rel(QUEUE)}`",
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
    lemmas = separation_rows()
    channels = channel_rows()
    ranks = rank_test_rows()
    gates = kperp_gate_rows()
    queue = queue_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(SEPARATION, lemmas)
    write_csv(CHANNELS, channels)
    write_csv(RANK_TESTS, ranks)
    write_csv(KPERP_GATE, gates)
    write_csv(QUEUE, queue)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, lemmas, channels, ranks, gates, queue, decisions)
    write_csv(VALIDATION, validations)
    write_doc(lemmas, channels, ranks, gates, queue, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3201 validation failed: {detail}")
    print(f"3201 generated {DOC}")


if __name__ == "__main__":
    main()
