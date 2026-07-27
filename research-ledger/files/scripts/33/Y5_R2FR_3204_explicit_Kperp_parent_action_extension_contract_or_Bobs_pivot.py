from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3204-Y5-R2FR-explicit-Kperp-parent-action-extension-contract-or-Bobs-pivot-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3204_INPUTS.csv"
ACTION_EXTENSION = OUT / "P8_Y5_R2FR_3204_EXPLICIT_ACTION_EXTENSION.csv"
DIMENSIONS = OUT / "P8_Y5_R2FR_3204_DIMENSION_AND_NORMALIZATION_AUDIT.csv"
VARIATION = OUT / "P8_Y5_R2FR_3204_NORMAL_VARIATION_MOMENTA.csv"
SAFETY_GATES = OUT / "P8_Y5_R2FR_3204_EXTENSION_SAFETY_GATES.csv"
PIVOT = OUT / "P8_Y5_R2FR_3204_EXTENSION_OR_BOBS_PIVOT.csv"
DECISION = OUT / "P8_Y5_R2FR_3204_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3204_VALIDATION.csv"


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


SOURCES = [
    {
        "input_id": "SRC3204_00",
        "location": "post_checkpoint",
        "relative_path": "3203-Y5-R2FR-parent-origin-of-Kperp-L4-operator-or-demote-to-Bobs-under-AX1090.md",
        "role": "3203 parent-action contract and nonclaim verdict",
        "terms": ["S_Kperp", "L_T", "boundary", "CONTRACT_WRITTEN_NOT_PROMOTED"],
    },
    {
        "input_id": "SRC3204_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3203_PARENT_ACTION_CONTRACT.csv",
        "role": "3203 parent action contract rows",
        "terms": ["minimal Kperp", "positive tensor", "local safety"],
    },
    {
        "input_id": "SRC3204_02",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "K_hat dimensions and K_MTS scaffold",
        "terms": ["[Gamma_eff]", "[K_hat]", "[q^nu]", "K_MTS"],
    },
    {
        "input_id": "SRC3204_03",
        "location": "formalization",
        "relative_path": "05-equation-register.md",
        "role": "registered dimensions and local safety red flags",
        "terms": ["[K_MTS", "[K_hat", "Kperp", "closure target"],
    },
    {
        "input_id": "SRC3204_04",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "Kperp source/boundary elliptic estimate",
        "terms": ["L_T K_perp", "coercive", "K_perp|boundary", "zero modes"],
    },
    {
        "input_id": "SRC3204_05",
        "location": "formalization",
        "relative_path": "07-unification-spine.md",
        "role": "spine status for Kperp zero/suppressed/bounded route",
        "terms": ["K_perp", "PPN-bounded", "coercive", "parent"],
    },
    {
        "input_id": "SRC3204_06",
        "location": "post_checkpoint",
        "relative_path": "3202-Y5-R2FR-Kperp-elliptic-boundary-operator-or-Bobs-residual-acquisition-under-AX1090.md",
        "role": "3202 L4 rank-four conditional owner",
        "terms": ["fourth-order", "rank(R)=4", "conditional mathematical owner"],
    },
    {
        "input_id": "SRC3204_07",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "Bobs residual fallback route",
        "terms": ["Bobs", "M_H_ref", "source-measure", "components"],
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


def action_extension_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "term_id": "EXT3204_00_action",
            "object": "Kperp local-static extension action",
            "formula": "S_ext = (1/(2 kappa_GR)) int sqrt(-g) eta_T ell_T^2 <D_T K_perp, D_T K_perp> d^4x",
            "definition": "D_T = Pi_perp (1 - ell_T^2 Delta_perp) Pi_perp",
            "role": "makes D_T^dagger D_T K_perp a fourth-order elliptic/coarse-grained owner of C1 trace data",
            "status": "PRIVATE_EXTENSION_CANDIDATE_NOT_PARENT_PROMOTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "term_id": "EXT3204_01_source",
            "object": "optional projected tensor source",
            "formula": "S_src = -(1/kappa_GR) int sqrt(-g) eta_T ell_T^2 <K_perp, Sigma_perp> d^4x",
            "definition": "[Sigma_perp]=L^-2 and Sigma_perp must vanish/suppress in local source-silent domains",
            "role": "allows D_T^dagger D_T K_perp = Sigma_perp without inventing unsuppressed local source flux",
            "status": "CONDITIONAL_SOURCE_CHANNEL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "term_id": "EXT3204_02_projection",
            "object": "transverse/traceless local projection",
            "formula": "K_perp = Pi_perp[K_hat], with g_mu_nu K_perp^{mu nu}=0 and gauge/trace kernel fixed",
            "definition": "Pi_perp must be parent-owned or its commutator enters Bobs/projector leakage",
            "role": "prevents scalar Gamma_eff or gauge modes from being counted as tensor rank owner",
            "status": "OPEN_PARENT_PROJECTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "term_id": "EXT3204_03_trace",
            "object": "C1 trace map",
            "formula": "R z = (K_L, partial_n K_L, K_R, partial_n K_R), z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R)",
            "definition": "rank(R)=4 required; otherwise K0=R^T G_trace R is degenerate",
            "role": "connects abstract H2 trace capacity to actual MTS mismatch variables",
            "status": "OPEN_PARENT_TRACE_MAP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "term_id": "EXT3204_04_scope",
            "object": "no-ghost scope restriction",
            "formula": "Delta_perp is spatial/domain-normal elliptic in the local static/coarse-grained sector, not a covariant Box creating fourth-time dynamics",
            "definition": "hyperbolic fourth-time promotion is forbidden unless a separate ghost-free parent construction exists",
            "role": "keeps the extension as an elliptic constraint/boundary sector rather than a propagating Ostrogradsky ghost",
            "status": "MANDATORY_SAFETY_RESTRICTION",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def dimension_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "dim_id": "DIM3204_00_Kperp",
            "quantity": "K_perp",
            "dimension_L_power": -2,
            "source_or_reason": "inherits [K_hat]=L^-2 from parent-equations v1",
            "gate_status": "source_backed_dimension",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "dim_id": "DIM3204_01_ellT",
            "quantity": "ell_T",
            "dimension_L_power": 1,
            "source_or_reason": "new tensor smoothing/coarse-graining length in private extension candidate",
            "gate_status": "new_parameter_needs_parent_or_empirical_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "dim_id": "DIM3204_02_DT",
            "quantity": "D_T = 1 - ell_T^2 Delta_perp",
            "dimension_L_power": 0,
            "source_or_reason": "Delta_perp has L^-2, so ell_T^2 Delta_perp is dimensionless",
            "gate_status": "dimensionally_consistent",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "dim_id": "DIM3204_03_action_bracket",
            "quantity": "eta_T ell_T^2 <D_T K_perp,D_T K_perp>",
            "dimension_L_power": -2,
            "source_or_reason": "ell_T^2 gives L^2 and <K,K> gives L^-4; bracket matches curvature dimension L^-2 before 1/kappa_GR",
            "gate_status": "dimensionally_consistent",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "dim_id": "DIM3204_04_sigma",
            "quantity": "Sigma_perp",
            "dimension_L_power": -2,
            "source_or_reason": "D_T^dagger D_T K_perp has L^-2, so source must match",
            "gate_status": "dimensionally_consistent_but_unsourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "dim_id": "DIM3204_05_eta",
            "quantity": "eta_T",
            "dimension_L_power": 0,
            "source_or_reason": "dimensionless positive stiffness weight",
            "gate_status": "new_parameter_needs_parent_normalization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def variation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "variation_id": "NM3204_00_define_Y",
            "normal_reduction": "Y = D_T K = K - ell_T^2 K''",
            "bulk_or_boundary": "definition",
            "formula": "S_normal = (eta_T ell_T^2/2) int Y^2 d rho",
            "derivation_status": "local_static_normal_reduction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "variation_id": "NM3204_01_bulk",
            "normal_reduction": "delta S_bulk",
            "bulk_or_boundary": "bulk",
            "formula": "eta_T ell_T^2 int (Y - ell_T^2 Y'') delta K d rho = eta_T ell_T^2 int D_T^dagger D_T K delta K d rho",
            "derivation_status": "derives_fourth_order_operator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "variation_id": "NM3204_02_Pi1",
            "normal_reduction": "Pi_1 conjugate to delta K'",
            "bulk_or_boundary": "boundary",
            "formula": "Pi_1 = - eta_T ell_T^4 Y",
            "derivation_status": "C1_boundary_momentum_present",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "variation_id": "NM3204_03_Pi0",
            "normal_reduction": "Pi_0 conjugate to delta K",
            "bulk_or_boundary": "boundary",
            "formula": "Pi_0 = eta_T ell_T^4 Y'",
            "derivation_status": "C1_boundary_momentum_present",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "variation_id": "NM3204_04_source",
            "normal_reduction": "with projected source Sigma_perp",
            "bulk_or_boundary": "bulk",
            "formula": "D_T^dagger D_T K_perp = Sigma_perp",
            "derivation_status": "conditional_on_source_descent",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def safety_gate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "SAFE3204_00_no_ghost",
            "gate": "elliptic_not_fourth_time_dynamics",
            "required_condition": "Delta_perp is a spatial/domain-normal elliptic operator in the local static/coarse-grained sector",
            "current_status": "passes_as_contract_restriction_not_parent_proof",
            "failure_action": "if promoted to covariant Box^2 without ghost-free construction, reject extension and pivot to Bobs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SAFE3204_01_parent_frame",
            "gate": "parent-owned observer/environment frame",
            "required_condition": "the split defining Delta_perp and Pi_perp descends from parent matter/environment frame, not arbitrary coordinates",
            "current_status": "open",
            "failure_action": "projector/frame leakage becomes Bobs_projector_commutator component",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SAFE3204_02_positive_eta",
            "gate": "positive stiffness weight",
            "required_condition": "eta_T>0 and tensor inner product positive on physical Kperp components",
            "current_status": "contract_pass_unsourced",
            "failure_action": "negative/indefinite sector rejected as ghost/instability",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SAFE3204_03_no_zero_modes",
            "gate": "zero modes fixed",
            "required_condition": "kernel of D_T on Kperp sector is removed by mass term, boundary condition, gauge fixing, or topology",
            "current_status": "open",
            "failure_action": "rank map nonunique; pivot to Bobs or add explicit zero-mode ledger",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SAFE3204_04_local_suppression",
            "gate": "local safety",
            "required_condition": "Sigma_perp and boundary traces vanish/suppress with U_B powers or are bounded below PPN/clock/orbital limits",
            "current_status": "open",
            "failure_action": "extension may exist but only as residual component, not local-GR proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SAFE3204_05_no_tuned_rank",
            "gate": "no tuned trace map",
            "required_condition": "rank(R)=4 follows from parent projection/trace structure, not manually chosen to force rank",
            "current_status": "open",
            "failure_action": "rank-four owner remains closure-only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def pivot_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "pivot_id": "PIV3204_00_continue_extension",
            "route": "continue Kperp extension",
            "condition": "use only as private candidate if no-ghost restriction, dimensional audit, positive eta, and variation gates pass",
            "current_result": "PASS_AS_PRIVATE_EXTENSION_CANDIDATE_ONLY",
            "next_action": "screen parent frame, zero modes, trace map, and local suppression in 3205",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "pivot_id": "PIV3204_01_demote_to_Bobs",
            "route": "Bobs residual acquisition",
            "condition": "trigger if parent frame, zero-mode, trace-map, or local-suppression gates cannot be closed",
            "current_result": "STAGED_NOT_TRIGGERED_THIS_CHECKPOINT",
            "next_action": "prepare M_H_ref and Bobs source-measure/boundary/projector component rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "pivot_id": "PIV3204_02_public_claim",
            "route": "public/local-GR claim",
            "condition": "requires parent-signed action, rank map, positive operator, zero modes, and local bounds",
            "current_result": "FORBIDDEN",
            "next_action": "no claim; no workbench promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3204_00",
            "result": "KPERP_EXTENSION_ADMISSIBLE_AS_PRIVATE_CANDIDATE_ONLY",
            "claim_status": "NO_PARENT_PROMOTION_LOCAL_GR_NEWTON_OR_PPN_CLAIM",
            "decision": "the explicit Kperp action extension is dimensionally consistent and derives the L4/C1-boundary mechanism, but it remains a private candidate because parent frame, projector, zero modes, trace map, and local suppression are not closed",
            "best_next_route": "run a hard safety screen on frame/projector/zero-mode/trace/local-suppression gates; if any fail without repair, pivot to Bobs residual acquisition",
            "next_target": "3205-Y5-R2FR-Kperp-extension-safety-screen-or-Bobs-pivot-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    actions: list[dict[str, object]],
    dimensions: list[dict[str, object]],
    variations: list[dict[str, object]],
    safety: list[dict[str, object]],
    pivots: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, ACTION_EXTENSION, DIMENSIONS, VARIATION, SAFETY_GATES, PIVOT, DECISION]
    dimension_passes = [row for row in dimensions if "dimensionally_consistent" in row["gate_status"] or row["gate_status"] == "source_backed_dimension"]
    open_safety = [row for row in safety if row["current_status"] == "open"]
    return [
        {
            "check_id": "VAL3204_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_01_action_explicit",
            "check": "explicit Kperp action, source, projection, trace, and no-ghost scope rows exist",
            "pass": b({row["object"] for row in actions} >= {"Kperp local-static extension action", "optional projected tensor source", "transverse/traceless local projection", "C1 trace map", "no-ghost scope restriction"}),
            "detail": f"action_rows={len(actions)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_02_dimensions_consistent",
            "check": "dimensions for Kperp, DT, bracket, and source are consistent or source-backed",
            "pass": b(len(dimension_passes) >= 4 and all(row["valid_for_claim"] == "false" for row in dimensions)),
            "detail": ";".join(f"{row['quantity']}={row['gate_status']}" for row in dimensions),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_03_variation_has_C1_momenta",
            "check": "normal variation contains fourth-order bulk operator and Pi0/Pi1 boundary momenta",
            "pass": b(
                any(row["derivation_status"] == "derives_fourth_order_operator" for row in variations)
                and sum(1 for row in variations if row["derivation_status"] == "C1_boundary_momentum_present") == 2
            ),
            "detail": ";".join(row["variation_id"] for row in variations),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_04_safety_open_not_claimed",
            "check": "hard safety gates remain open/nonclaim where appropriate",
            "pass": b(len(open_safety) >= 4 and all(row["valid_for_claim"] == "false" for row in safety)),
            "detail": ";".join(f"{row['gate']}={row['current_status']}" for row in safety),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_05_pivot_logic",
            "check": "extension continues only as private candidate and Bobs pivot is staged",
            "pass": b(
                any(row["current_result"] == "PASS_AS_PRIVATE_EXTENSION_CANDIDATE_ONLY" for row in pivots)
                and any(row["current_result"] == "STAGED_NOT_TRIGGERED_THIS_CHECKPOINT" for row in pivots)
                and any(row["current_result"] == "FORBIDDEN" for row in pivots)
            ),
            "detail": ";".join(f"{row['route']}={row['current_result']}" for row in pivots),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_06_decision_nonclaim",
            "check": "decision keeps extension private and nonclaim",
            "pass": b(decisions[0]["result"] == "KPERP_EXTENSION_ADMISSIBLE_AS_PRIVATE_CANDIDATE_ONLY" and decisions[0]["valid_for_claim"] == "false"),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_07_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [actions, dimensions, variations, safety, pivots, decisions] for row in table)),
            "detail": "no parent promotion, local-GR, Newton, PPN, or rank-four claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3204_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    actions: list[dict[str, object]],
    dimensions: list[dict[str, object]],
    variations: list[dict[str, object]],
    safety: list[dict[str, object]],
    pivots: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3204 - Explicit Kperp Parent Action Extension Contract Or Bobs Pivot Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, parent-action promotion, rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3204 writes the explicit extension in a form that is respectable enough to keep testing privately:",
        "",
        "```text",
        "S_ext = (1/(2 kappa_GR)) int sqrt(-g) eta_T ell_T^2 <D_T K_perp, D_T K_perp> d^4x",
        "D_T = Pi_perp (1 - ell_T^2 Delta_perp) Pi_perp",
        "K_perp = Pi_perp[K_hat],",
        "D_T^dagger D_T K_perp = Sigma_perp.",
        "```",
        "",
        "The important restriction is that `Delta_perp` is elliptic/spatial/domain-normal in the local static coarse-grained sector. A covariant fourth-time-derivative `Box^2` promotion is rejected unless a separate ghost-free construction exists.",
        "",
        "## Action Extension",
        "",
    ]
    for row in actions:
        lines.append(f"- `{row['term_id']}`: `{row['object']}` -> `{row['status']}`")
    lines.extend(["", "## Dimension Audit", ""])
    for row in dimensions:
        lines.append(f"- `{row['dim_id']}`: `{row['quantity']}` has `L^{row['dimension_L_power']}` -> `{row['gate_status']}`")
    lines.extend(["", "## Normal Variation", ""])
    for row in variations:
        lines.append(f"- `{row['variation_id']}`: {row['formula']} -> `{row['derivation_status']}`")
    lines.extend(["", "## Safety Gates", ""])
    for row in safety:
        lines.append(f"- `{row['gate_id']}`: `{row['gate']}` -> `{row['current_status']}`; fail action: {row['failure_action']}")
    lines.extend(["", "## Pivot Logic", ""])
    for row in pivots:
        lines.append(f"- `{row['pivot_id']}`: `{row['route']}` -> `{row['current_result']}`")
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
            f"- `{rel(ACTION_EXTENSION)}`",
            f"- `{rel(DIMENSIONS)}`",
            f"- `{rel(VARIATION)}`",
            f"- `{rel(SAFETY_GATES)}`",
            f"- `{rel(PIVOT)}`",
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
    actions = action_extension_rows()
    dimensions = dimension_rows()
    variations = variation_rows()
    safety = safety_gate_rows()
    pivots = pivot_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(ACTION_EXTENSION, actions)
    write_csv(DIMENSIONS, dimensions)
    write_csv(VARIATION, variations)
    write_csv(SAFETY_GATES, safety)
    write_csv(PIVOT, pivots)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, actions, dimensions, variations, safety, pivots, decisions)
    write_csv(VALIDATION, validations)
    write_doc(actions, dimensions, variations, safety, pivots, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3204 validation failed: {detail}")
    print(f"3204 generated {DOC}")


if __name__ == "__main__":
    main()
