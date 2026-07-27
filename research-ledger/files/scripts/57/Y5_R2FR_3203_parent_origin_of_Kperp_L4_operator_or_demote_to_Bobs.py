from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3203-Y5-R2FR-parent-origin-of-Kperp-L4-operator-or-demote-to-Bobs-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3203_INPUTS.csv"
ACTION_CONTRACT = OUT / "P8_Y5_R2FR_3203_PARENT_ACTION_CONTRACT.csv"
VARIATION = OUT / "P8_Y5_R2FR_3203_L4_VARIATION_AND_BOUNDARY_MOMENTA.csv"
SIGNATURE_AUDIT = OUT / "P8_Y5_R2FR_3203_PARENT_SIGNATURE_AUDIT.csv"
PROMOTION_GATE = OUT / "P8_Y5_R2FR_3203_PROMOTION_OR_BOBS_GATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3203_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3203_VALIDATION.csv"


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
        "input_id": "SRC3203_00",
        "location": "post_checkpoint",
        "relative_path": "3202-Y5-R2FR-Kperp-elliptic-boundary-operator-or-Bobs-residual-acquisition-under-AX1090.md",
        "role": "3202 conditional L4 rank-four owner",
        "terms": ["L4 K_perp", "parent MTS action", "conditional mathematical owner", "3203"],
    },
    {
        "input_id": "SRC3203_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3202_COERCIVITY_AND_ZERO_MODE_GATE.csv",
        "role": "3202 parent origin and coercivity gates",
        "terms": ["parent_origin", "coercive", "zero_modes", "trace_map"],
    },
    {
        "input_id": "SRC3203_02",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "K_MTS/K_hat parent equation scaffold",
        "terms": ["K_MTS", "K_hat", "q^nu", "action"],
    },
    {
        "input_id": "SRC3203_03",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "current Kperp elliptic boundary theorem target",
        "terms": ["K_perp", "L_T", "coercive", "not derived"],
    },
    {
        "input_id": "SRC3203_04",
        "location": "post_checkpoint",
        "relative_path": "3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090.md",
        "role": "squared-operator D2daggerD2 precedent",
        "terms": ["J[F]", "D2^dagger", "boundary", "operator"],
    },
    {
        "input_id": "SRC3203_05",
        "location": "post_checkpoint",
        "relative_path": "3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090.md",
        "role": "boundary momenta Pi0/Pi1 precedent",
        "terms": ["Pi_1", "Pi_0", "boundary", "source action"],
    },
    {
        "input_id": "SRC3203_06",
        "location": "post_checkpoint",
        "relative_path": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090.md",
        "role": "positive pullback stiffness theorem",
        "terms": ["K0 = J^T", "rank(J)", "G_N", "positive"],
    },
    {
        "input_id": "SRC3203_07",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "fallback Bobs acquisition route",
        "terms": ["Bobs", "M_H_ref", "source-measure", "fallback"],
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


def action_contract_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "contract_id": "PAC3203_00_minimal_parent_term",
            "contract_piece": "minimal Kperp L4 parent action term",
            "required_form": "S_Kperp = 1/2 int sqrt(g) w_T <L_T K_perp, L_T K_perp> d^4x",
            "local_static_reduction": "L_T -> (-partial_rho^2 + m_T^2) on projected transverse/tensor channel",
            "what_it_derives": "Euler operator L_T^dagger w_T L_T K_perp plus boundary momenta for K_perp and normal derivative",
            "status": "PROPOSED_EXTENSION_CONTRACT_NOT_EXISTING_PARENT_SIGNATURE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PAC3203_01_projection",
            "contract_piece": "Kperp projection and gauge/fixed-kernel rule",
            "required_form": "K_perp = Pi_perp K_hat with trace and pure-gauge parts removed",
            "local_static_reduction": "Pi_perp commutes with the local normal operator up to bounded/projector-commutator residuals",
            "what_it_derives": "prevents trace Gamma_eff or gauge modes from masquerading as Kperp rank owner",
            "status": "OPEN_PROJECTOR_PARENT_SIGNATURE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PAC3203_02_positive_weight",
            "contract_piece": "positive tensor weight",
            "required_form": "w_T>0 in the observer/local static sector with units fixed by K_MTS normalization",
            "local_static_reduction": "G_trace induced by the quadratic form is positive",
            "what_it_derives": "the normal metric needed for K0 = J^T G_trace J",
            "status": "OPEN_NORMALIZATION_AND_UNITS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PAC3203_03_trace_map",
            "contract_piece": "C1 trace map from MTS variables",
            "required_form": "R: z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R) -> tr(K_perp) has rank 4",
            "local_static_reduction": "R maps to (K_L, partial_n K_L, K_R, partial_n K_R) or two independent L2 tensor components",
            "what_it_derives": "turns abstract L4 trace capacity into the actual parent domain map",
            "status": "OPEN_ACTUAL_MTS_TRACE_MAP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PAC3203_04_safety",
            "contract_piece": "local safety compatibility",
            "required_form": "Kperp exact zero, U_B^n suppressed, or source-bounded below PPN/clock/orbital limits in local domains",
            "local_static_reduction": "rank owner does not leave an observable local residual",
            "what_it_derives": "prevents the owner term from solving rank while failing local GR",
            "status": "OPEN_LOCAL_SAFETY",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def variation_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "step_id": "VAR3203_00_action",
            "object": "quadratic squared-operator action",
            "formula": "S_K = 1/2 int <L K, W L K>",
            "derivation": "choose K=K_perp, L second-order elliptic, W positive tensor metric",
            "owned_gate": "parent action form",
            "status": "abstract_derivation_valid",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "VAR3203_01_bulk_variation",
            "object": "bulk Euler equation",
            "formula": "delta S_bulk = int <L^dagger W L K, delta K>",
            "derivation": "integrate by parts twice for L and once more through the adjoint; local static self-adjoint case gives L W L K",
            "owned_gate": "fourth-order L4 operator",
            "status": "abstract_derivation_valid",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "VAR3203_02_boundary_momenta",
            "object": "C1 boundary momenta",
            "formula": "delta S_boundary = [Pi_1 delta(partial_n K) + Pi_0 delta K]_left^right",
            "derivation": "fourth-order actions naturally carry two boundary momenta, matching value and normal derivative traces",
            "owned_gate": "C1 trace ownership",
            "status": "abstract_derivation_valid",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "VAR3203_03_positive_pullback",
            "object": "normal stiffness",
            "formula": "K0 = R^T G_trace R",
            "derivation": "if W>0, L elliptic/coercive, no zero modes, and rank(R)=4, then K0 is positive on C1 mismatch slots",
            "owned_gate": "positive domain stiffness",
            "status": "conditional_on_parent_contract",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def signature_audit_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "SIG3203_00_existing_Khat_scaffold",
            "source_path": "formalization-workbench/83-parent-equations-v1.md",
            "needed_signature": "K_hat is derived from a parent action with a metric/tensor Hessian",
            "current_evidence": "K_hat is defined by trace/tensor decomposition and exchange-current identity",
            "verdict": "SCAFFOLD_ONLY_NOT_L4_PARENT_ACTION",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3203_01_existing_Kperp_law",
            "source_path": "formalization-workbench/75-projected-source-laws.md",
            "needed_signature": "L_T K_perp = J_perp is parent-derived and coercive with exact boundary data",
            "current_evidence": "file names L_T coercive/positive as a conditional route and says Kperp needs its own theorem",
            "verdict": "CONDITIONAL_BOUNDARY_LAW_NOT_PARENT_SIGNED",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3203_02_D2_precedent",
            "source_path": "post-checkpoint-work/3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090.md",
            "needed_signature": "squared-operator action exists for actual Kperp tensor sector",
            "current_evidence": "D2^dagger D2 shows a fourth-order squared-operator mechanism for profile F only",
            "verdict": "USEFUL_PRECEDENT_NOT_KPERP_SIGNATURE",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3203_03_boundary_momenta",
            "source_path": "post-checkpoint-work/3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090.md",
            "needed_signature": "Kperp parent action supplies Pi0/Pi1-like boundary reaction",
            "current_evidence": "Pi0/Pi1 boundary momenta were derived for the profile functional, but a parent boundary/interface action was still required",
            "verdict": "BOUNDARY_PRECEDENT_NOT_PARENT_SOURCE",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "SIG3203_04_current_contract",
            "source_path": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3203_PARENT_ACTION_CONTRACT.csv",
            "needed_signature": "future parent action explicitly adopts S_Kperp and trace map with units/safety",
            "current_evidence": "this checkpoint writes the exact contract but does not install it into the parent theory",
            "verdict": "CONTRACT_WRITTEN_NOT_PROMOTED",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def promotion_gate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "POB3203_00_promote_L4",
            "route": "promote Kperp L4 route",
            "required_to_pass": "all PAC3203 contract pieces become parent-signed with source paths, units, and local-safety theorem",
            "current_status": "FAIL_CURRENT_CORPUS",
            "next_action": "attempt explicit parent action extension in a new checkpoint; do not edit main workbench yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "POB3203_01_two_component_L2",
            "route": "two independent second-order tensor components",
            "required_to_pass": "parent supplies two independent Kperp components and a full-rank slot-to-component map",
            "current_status": "NO_SOURCE_IN_CURRENT_CORPUS",
            "next_action": "only revisit if parent tensor decomposition exposes two physical transverse components",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "POB3203_02_Bobs_fallback",
            "route": "demote rank route and acquire Bobs residual rows",
            "required_to_pass": "M_H_ref plus source-measure, boundary, projector, corner, and total no-cancellation rows become source-backed",
            "current_status": "READY_IF_PARENT_ACTION_EXTENSION_REFUSED_OR_FAILS",
            "next_action": "prepare Bobs acquisition runner if no parent-action extension is adopted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3203_00",
            "result": "KPERP_L4_PARENT_ACTION_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "claim_status": "NO_LOCAL_GR_NEWTON_PPN_OR_PARENT_ACTION_CLAIM",
            "decision": "a squared-operator parent action would derive the required L4 operator and C1 boundary momenta, but the current corpus only contains scaffolds/precedents, not a signed Kperp parent action",
            "best_next_route": "one more constructive attempt: write a proposed parent-action extension checkpoint with units/projection/safety gates; if not accepted, demote to Bobs residual acquisition",
            "next_target": "3204-Y5-R2FR-explicit-Kperp-parent-action-extension-contract-or-Bobs-pivot-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    contracts: list[dict[str, object]],
    variations: list[dict[str, object]],
    signatures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, ACTION_CONTRACT, VARIATION, SIGNATURE_AUDIT, PROMOTION_GATE, DECISION]
    missing_parent = [row for row in signatures if row["blocks_claim"] == "true"]
    return [
        {
            "check_id": "VAL3203_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_01_contract_complete",
            "check": "minimum parent-action contract covers action, projection, positivity, trace map, and safety",
            "pass": b({row["contract_piece"] for row in contracts} >= {"minimal Kperp L4 parent action term", "Kperp projection and gauge/fixed-kernel rule", "positive tensor weight", "C1 trace map from MTS variables", "local safety compatibility"}),
            "detail": f"contract_rows={len(contracts)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_02_variation_derives_L4_boundary",
            "check": "variation table contains bulk L4 and C1 boundary momenta",
            "pass": b(any(row["owned_gate"] == "fourth-order L4 operator" for row in variations) and any(row["owned_gate"] == "C1 trace ownership" for row in variations)),
            "detail": ";".join(row["step_id"] for row in variations),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_03_no_existing_parent_signature",
            "check": "signature audit blocks promotion from current corpus",
            "pass": b(len(missing_parent) == len(signatures) and all(row["valid_for_claim"] == "false" for row in signatures)),
            "detail": ";".join(f"{row['audit_id']}={row['verdict']}" for row in signatures),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_04_promotion_or_bobs_gate",
            "check": "promotion and Bobs fallback gates are both explicit",
            "pass": b(any(row["route"] == "promote Kperp L4 route" for row in gates) and any(row["route"] == "demote rank route and acquire Bobs residual rows" for row in gates)),
            "detail": ";".join(f"{row['route']}={row['current_status']}" for row in gates),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_05_decision_nonclaim",
            "check": "decision records contract-written but not parent-signed",
            "pass": b(decisions[0]["result"] == "KPERP_L4_PARENT_ACTION_CONTRACT_WRITTEN_NOT_PARENT_SIGNED" and decisions[0]["valid_for_claim"] == "false"),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_06_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [contracts, variations, signatures, gates, decisions] for row in table)),
            "detail": "no parent action, local-GR, Newton, PPN, or rank-four claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3203_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    contracts: list[dict[str, object]],
    variations: list[dict[str, object]],
    signatures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3203 - Parent Origin Of Kperp L4 Operator Or Demote To Bobs Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, parent-action claim, rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3203 writes the exact parent-action contract that would make the 3202 `L4 K_perp` route real:",
        "",
        "```text",
        "S_Kperp = 1/2 int sqrt(g) w_T <L_T K_perp, L_T K_perp> d^4x,",
        "L_T -> (-partial_rho^2 + m_T^2) in the local static normal direction,",
        "EL: L_T^dagger w_T L_T K_perp = source,",
        "boundary: [Pi_1 delta(partial_n K_perp) + Pi_0 delta K_perp]_{left}^{right}.",
        "```",
        "",
        "That is a real mechanism: a squared second-order tensor operator gives a fourth-order bulk equation and two boundary momenta, exactly the C1 data route we needed.",
        "",
        "But the current corpus does **not** already parent-sign this action. So this is a proposed extension contract, not a hidden completed derivation.",
        "",
        "## Parent Action Contract",
        "",
    ]
    for row in contracts:
        lines.append(f"- `{row['contract_id']}`: `{row['contract_piece']}` -> `{row['status']}`")
    lines.extend(["", "## Variation", ""])
    for row in variations:
        lines.append(f"- `{row['step_id']}`: {row['formula']} -> `{row['status']}`")
    lines.extend(["", "## Signature Audit", ""])
    for row in signatures:
        lines.append(f"- `{row['audit_id']}`: `{row['verdict']}` from `{row['source_path']}`")
    lines.extend(
        [
            "",
            "## Promotion Or Bobs Gate",
            "",
        ]
    )
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: `{row['route']}` -> `{row['current_status']}`; next: {row['next_action']}")
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
            f"- `{rel(ACTION_CONTRACT)}`",
            f"- `{rel(VARIATION)}`",
            f"- `{rel(SIGNATURE_AUDIT)}`",
            f"- `{rel(PROMOTION_GATE)}`",
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
    contracts = action_contract_rows()
    variations = variation_rows()
    signatures = signature_audit_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(ACTION_CONTRACT, contracts)
    write_csv(VARIATION, variations)
    write_csv(SIGNATURE_AUDIT, signatures)
    write_csv(PROMOTION_GATE, gates)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, contracts, variations, signatures, gates, decisions)
    write_csv(VALIDATION, validations)
    write_doc(contracts, variations, signatures, gates, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3203 validation failed: {detail}")
    print(f"3203 generated {DOC}")


if __name__ == "__main__":
    main()
