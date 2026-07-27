from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3200_INPUTS.csv"
POYNTING_THEOREM = OUT / "P8_Y5_R2FR_3200_POYNTING_ZERO_OR_BOUND_THEOREM.csv"
J_TEMPLATE = OUT / "P8_Y5_R2FR_3200_STRESS_FLUX_J_COEFFICIENT_TEMPLATE.csv"
RANK_AUDIT = OUT / "P8_Y5_R2FR_3200_RANK_CONTRIBUTION_AUDIT.csv"
BOUND_RUNNER = OUT / "P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv"
DECISION = OUT / "P8_Y5_R2FR_3200_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3200_VALIDATION.csv"


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
        "input_id": "SRC3200_00",
        "location": "post_checkpoint",
        "relative_path": "3199-Y5-R2FR-Poynting-source-coupling-domain-map-candidate-or-local-residual-bound-under-AX1090.md",
        "role": "3199 C^nu stress-flux target and next extractor decision",
        "terms": ["C^nu", "J_Aa", "Poynting", "rank"],
    },
    {
        "input_id": "SRC3200_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3199_RANK_POSITIVITY_AND_COUPLING_GATE.csv",
        "role": "rank, positive metric, and coupling gates",
        "terms": ["rank(J)", "Poynting", "tau_EM", "unproven"],
    },
    {
        "input_id": "SRC3200_02",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3199_LOCAL_RESIDUAL_BOUND_SCHEMA.csv",
        "role": "3199 Poynting residual fallback schema",
        "terms": ["B_obs_EM_Poynting_over_MH", "schema_only", "Poynting"],
    },
    {
        "input_id": "SRC3200_03",
        "location": "post_checkpoint",
        "relative_path": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090.md",
        "role": "rank-four J and positive metric theorem",
        "terms": ["K0 = J^T", "rank(J)", "G_N", "positive"],
    },
    {
        "input_id": "SRC3200_04",
        "location": "formalization",
        "relative_path": "29-em-maxwell-gate-audit.md",
        "role": "Maxwell/Poynting/stress-energy gate status",
        "terms": ["Maxwell recovery", "EM stress-energy", "radiation pressure", "Poynting"],
    },
    {
        "input_id": "SRC3200_05",
        "location": "formalization",
        "relative_path": "19-proof-obligations.md",
        "role": "Maxwell and local-limit proof obligations",
        "terms": ["Maxwell", "Gauge field", "conserved current", "K_hat"],
    },
    {
        "input_id": "SRC3200_06",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "K_hat as anisotropic stress/flux owner candidate",
        "terms": ["K_hat owns", "flux", "q^nu", "local closure"],
    },
    {
        "input_id": "SRC3200_07",
        "location": "post_checkpoint",
        "relative_path": "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
        "role": "observed boundary/source/projector flux decomposition",
        "terms": ["B_obs", "source_measure", "projector", "no-flux"],
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


def poynting_theorem_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "case_id": "PZT3200_00",
            "local_regime": "quiet_static_no_radiation_no_magnetic_flux",
            "assumptions": "observer split exists; fields stationary; H=0 or E cross H has zero normal projection; no radiation through local surface",
            "standard_target_statement": "S = E x H gives n dot S = 0, so T_EM^{0i} contributes no normal energy flux",
            "MTS_status": "target_theorem_not_MTS_Maxwell_claim",
            "J_EM_rank_contribution": 0,
            "important_caveat": "zero Poynting energy flux does not imply zero Maxwell spatial stress or zero EM self-energy",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "PZT3200_01",
            "local_regime": "electrostatic_bound_field",
            "assumptions": "E may be nonzero; B/H radiation part absent; local test body has EM self-energy",
            "standard_target_statement": "Poynting flux can vanish while T_EM^{ij} and energy density remain nonzero",
            "MTS_status": "Poynting_zero_only_not_full_EM_silence",
            "J_EM_rank_contribution": 0,
            "important_caveat": "composition/EM self-energy still belongs in WEP/PPN source-coupling bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "PZT3200_02",
            "local_regime": "static_crossed_fields_or_circulating_field_momentum",
            "assumptions": "E cross H nonzero but controlled; normal projection may vanish by geometry or averaging",
            "standard_target_statement": "|n dot S| <= |E||H| supplies a finite residual bound",
            "MTS_status": "finite_bound_route",
            "J_EM_rank_contribution": "at_most_low_rank_without_parent_field_response",
            "important_caveat": "circulating Poynting flow is not automatically a source of four independent C1 mismatch responses",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "case_id": "PZT3200_03",
            "local_regime": "radiative_or_time_dependent_EM",
            "assumptions": "radiation or time-dependent fields cross the local surface",
            "standard_target_statement": "Poynting flux is live and must be source-backed/bounded",
            "MTS_status": "residual_bound_required",
            "J_EM_rank_contribution": "not_claimed",
            "important_caveat": "using radiation flux to repair local static GR would be the wrong limit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def j_template_rows() -> list[dict[str, object]]:
    now = stamp()
    slots = [
        ("z0", "Delta_F_L", "left interface amplitude mismatch"),
        ("z1", "Delta_Fprime_L", "left interface derivative mismatch"),
        ("z2", "Delta_F_R", "right interface amplitude mismatch"),
        ("z3", "Delta_Fprime_R", "right interface derivative mismatch"),
    ]
    components = [
        ("C0", "left_normal_flux_value", "normal stress-flux coefficient conjugate to left value continuity"),
        ("C1", "left_normal_flux_derivative", "normal stress-flux coefficient conjugate to left derivative continuity"),
        ("C2", "right_normal_flux_value", "normal stress-flux coefficient conjugate to right value continuity"),
        ("C3", "right_normal_flux_derivative", "normal stress-flux coefficient conjugate to right derivative continuity"),
    ]
    rows: list[dict[str, object]] = []
    for component_id, component, component_role in components:
        for slot_id, slot, slot_role in slots:
            rows.append(
                {
                    "coefficient_id": f"J3200_{component_id}_{slot_id}",
                    "component": component,
                    "mismatch_slot": slot,
                    "definition": f"partial {component} / partial {slot} at z=0",
                    "central_difference_extractor": f"({component}(+epsilon {slot}) - {component}(-epsilon {slot}))/(2 epsilon)",
                    "required_source": "parent stress-flux evaluator C^nu[z] or source-backed finite-difference profile family",
                    "current_status": "MISSING_PARENT_COEFFICIENT",
                    "slot_role": slot_role,
                    "component_role": component_role,
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def rank_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    matrices = [
        (
            "RCA3200_00_quiet_Poynting_only",
            "quiet local Poynting flux only",
            [[0.0, 0.0, 0.0, 0.0] for _ in range(4)],
            "Poynting theorem-zero channel cannot own rank-four local gluing",
            "REJECT_AS_RANK_OWNER",
        ),
        (
            "RCA3200_01_single_live_Poynting_flux",
            "one live normal Poynting flux channel",
            [[1.0, 0.2, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
            "a single energy-flux channel gives at most rank one",
            "BOUND_CHANNEL_NOT_RANK_OWNER",
        ),
        (
            "RCA3200_02_symmetric_matter_shell",
            "spherically symmetric matter stress shell",
            [[1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0], [1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0]],
            "symmetric left/right response duplicates rows and cannot prove rank four",
            "INSUFFICIENT_WITHOUT_ASYMMETRIC_PARENT_CHANNELS",
        ),
        (
            "RCA3200_03_full_parent_flux_toy",
            "conditional full parent stress-flux response",
            [[2.0, 0.1, 0.0, 0.0], [0.2, 1.7, 0.1, 0.0], [0.0, 0.3, 1.4, 0.2], [0.1, 0.0, 0.2, 1.1]],
            "rank four is mathematically possible if parent MTS/matter stress supplies four independent coefficients",
            "CONDITIONAL_TARGET_ONLY",
        ),
    ]
    rows: list[dict[str, object]] = []
    for case_id, description, matrix, interpretation, status in matrices:
        rank = matrix_rank(matrix)
        rows.append(
            {
                "case_id": case_id,
                "description": description,
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


def bound_runner_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "bound_id": "PBR3200_00",
            "quantity": "normal_Poynting_flux_density",
            "inequality": "|n dot S| <= |E| |H|",
            "input_columns": "system_id;surface_id;E_bound;H_bound;normal_projection_bound;units;source_path;valid_for_claim",
            "output_column": "S_normal_bound",
            "claim_use": "finite residual input only",
            "current_status": "schema_only_no_numeric_data",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "PBR3200_01",
            "quantity": "dimensionless_EM_flux_residual",
            "inequality": "B_EM <= |tau_EM| S_normal_bound / M_H_ref",
            "input_columns": "tau_EM;S_normal_bound;M_H_ref;units;source_path;valid_for_claim",
            "output_column": "B_obs_EM_Poynting_over_MH_bound",
            "claim_use": "local residual bound only after tau_EM and M_H_ref are sourced",
            "current_status": "schema_only_no_numeric_data",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "PBR3200_02",
            "quantity": "quiet_zero_certificate",
            "inequality": "if H_radiative=0 and n dot(E x H_static)=0 then B_obs_EM_Poynting_over_MH=0 for the Poynting subchannel",
            "input_columns": "system_id;surface_id;field_regime;H_radiative_zero_certificate;normal_cross_flux_zero_certificate;source_path;valid_for_claim",
            "output_column": "Poynting_subchannel_zero",
            "claim_use": "subchannel zero only; does not zero EM spatial stress or full local residual",
            "current_status": "schema_only_no_certificate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3200_00",
            "result": "POYNTING_DEMOTED_FROM_RANK_OWNER_TO_ZERO_OR_BOUND_CHANNEL",
            "claim_status": "NO_LOCAL_GR_MAXWELL_PPN_OR_RANK4_CLAIM",
            "decision": "quiet local Poynting is a theorem-zero/bound target, while rank-four J_Aa must come from parent MTS/matter stress-flux coefficients",
            "best_next_route": "target K_hat/T_MTS plus matter-source flux as the possible four-channel owner; keep Poynting in the residual ledger",
            "next_target": "3201-Y5-R2FR-MTS-matter-stress-flux-four-channel-owner-or-rank-no-go-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    poynting: list[dict[str, object]],
    template: list[dict[str, object]],
    ranks: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, POYNTING_THEOREM, J_TEMPLATE, RANK_AUDIT, BOUND_RUNNER, DECISION]
    quiet = next(row for row in ranks if row["case_id"] == "RCA3200_00_quiet_Poynting_only")
    full = next(row for row in ranks if row["case_id"] == "RCA3200_03_full_parent_flux_toy")
    return [
        {
            "check_id": "VAL3200_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_01_poynting_zero_cases_recorded",
            "check": "quiet/static Poynting zero and finite-bound cases are separated",
            "pass": b(any(row["case_id"] == "PZT3200_00" for row in poynting) and any(row["case_id"] == "PZT3200_03" for row in poynting)),
            "detail": f"cases={len(poynting)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_02_j_template_complete",
            "check": "16 J_Aa coefficient slots are staged",
            "pass": b(len(template) == 16 and all(row["current_status"] == "MISSING_PARENT_COEFFICIENT" for row in template)),
            "detail": "4 components x 4 mismatch slots",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_03_quiet_poynting_rank_zero",
            "check": "quiet Poynting-only rank contribution is zero",
            "pass": b(int(quiet["rank"]) == 0 and quiet["passes_rank4"] == "false"),
            "detail": quiet["interpretation"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_04_full_rank_only_conditional",
            "check": "rank-four appears only in conditional toy parent-flux row",
            "pass": b(int(full["rank"]) == 4 and full["status"] == "CONDITIONAL_TARGET_ONLY"),
            "detail": full["interpretation"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_05_bound_schema_ready",
            "check": "Poynting finite-bound and zero-certificate schemas are present",
            "pass": b(any(row["bound_id"] == "PBR3200_01" for row in bounds) and any(row["bound_id"] == "PBR3200_02" for row in bounds)),
            "detail": "finite bound plus quiet zero certificate",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_06_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [poynting, template, ranks, bounds, decisions] for row in table)),
            "detail": "no local-GR, Maxwell, PPN, or rank-four claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3200_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    poynting: list[dict[str, object]],
    template: list[dict[str, object]],
    ranks: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3200 - Stress-Flux Rank Coefficient Extractor Or Poynting Residual Bound Runner Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, Maxwell derivation, EM unification claim, rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3200 separates two jobs that were getting tangled:",
        "",
        "```text",
        "Poynting flux: quiet local zero/bound channel.",
        "Rank-four J_Aa: parent MTS/matter stress-flux problem.",
        "```",
        "",
        "This is a useful narrowing. The Poynting vector belongs in the stress-energy flux story, but in quiet local PPN-style tests it should usually vanish or be small. If it were large and unsuppressed, it would damage local-GR safety rather than fix it.",
        "",
        "## Poynting Zero Or Bound Law",
        "",
    ]
    for row in poynting:
        lines.append(f"- `{row['case_id']}`: `{row['local_regime']}` - {row['standard_target_statement']} Caveat: {row['important_caveat']}")
    lines.extend(
        [
            "",
            "The clean quiet theorem target is:",
            "",
            "```text",
            "if H_radiative = 0 and n dot(E x H_static) = 0,",
            "then n dot S = 0 for the Poynting subchannel.",
            "```",
            "",
            "This does **not** zero full EM stress-energy. Electrostatic self-energy and Maxwell spatial stress remain separate source-coupling/WEP concerns.",
            "",
            "## J_Aa Extractor",
            "",
            "The four local gluing mismatch slots are:",
            "",
            "```text",
            "z = (Delta_F_L, Delta_Fprime_L, Delta_F_R, Delta_Fprime_R).",
            "```",
            "",
            "3200 stages all 16 coefficient slots:",
            "",
            "```text",
            "J_Aa = partial C_A / partial z^a at z=0.",
            "```",
            "",
            f"Template rows staged: {len(template)}.",
            "",
            "But every row is still `MISSING_PARENT_COEFFICIENT`; that is honest because no parent stress-flux evaluator exists yet.",
            "",
            "## Rank Audit",
            "",
        ]
    )
    for row in ranks:
        lines.append(f"- `{row['case_id']}`: rank `{row['rank']}`, passes rank-four `{row['passes_rank4']}` - {row['interpretation']}")
    lines.extend(
        [
            "",
            "The only rank-four row is a conditional toy target, not evidence. It shows the shape needed, not that MTS already owns it.",
            "",
            "## Bound Runner",
            "",
        ]
    )
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: `{row['quantity']}` - {row['inequality']}")
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
            f"- `{rel(POYNTING_THEOREM)}`",
            f"- `{rel(J_TEMPLATE)}`",
            f"- `{rel(RANK_AUDIT)}`",
            f"- `{rel(BOUND_RUNNER)}`",
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
    poynting = poynting_theorem_rows()
    template = j_template_rows()
    ranks = rank_audit_rows()
    bounds = bound_runner_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(POYNTING_THEOREM, poynting)
    write_csv(J_TEMPLATE, template)
    write_csv(RANK_AUDIT, ranks)
    write_csv(BOUND_RUNNER, bounds)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, poynting, template, ranks, bounds, decisions)
    write_csv(VALIDATION, validations)
    write_doc(poynting, template, ranks, bounds, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3200 validation failed: {detail}")
    print(f"3200 generated {DOC}")


if __name__ == "__main__":
    main()
