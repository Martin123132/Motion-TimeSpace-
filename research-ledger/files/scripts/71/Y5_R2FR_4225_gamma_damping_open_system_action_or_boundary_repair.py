from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4225"
CLAIM_ID = "L-066"
BRANCH = "MTS_R2FR_Y5_GAMMA_DAMPING_REPAIR_4225"
DECISION = "GAMMA_BOUNDARY_ROUTE_ENERGY_SAFE_BUT_NO_DAMPING_OPEN_SYSTEM_ROUTE_REQUIRES_BATH_CURRENT_AND_STRESS_GUARD_NONCLAIM"
MARKER = "PPC4161_GAMMA_DAMPING_REPAIR_4225"
PACKET_MARKER = "PPC4161_PACKET_GAMMA_DAMPING_REPAIR_4225"
NEXT_TARGET = "4226-Y5-R2FR-gamma-bath-energy-balance-source-row-or-boundary-branch-adoption.md"

FORMAL_PATH = FORMAL / "241-PPC4161-gamma-damping-open-system-action-or-boundary-repair.md"
DOC_PATH = POST / "4225-Y5-R2FR-gamma-damping-open-system-action-or-boundary-repair.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4225_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4225_00_4224_next": SourceSpec(
        "SRC4225_00_4224_next",
        SOURCE_DIR / "P8_Y5_R2FR_4224_NEXT_TARGET.csv",
        "4225-Y5-R2FR-gamma-damping-open-system-action-or-boundary-repair.md",
        "4224 selected gamma damping repair as the live core obstruction.",
    ),
    "SRC4225_01_4224_gamma": SourceSpec(
        "SRC4225_01_4224_gamma",
        SOURCE_DIR / "P8_Y5_R2FR_4224_GAMMA_FORK.csv",
        "GFR4224_1_no_damping_from_boundary",
        "4224 gamma fork rows.",
    ),
    "SRC4225_02_240_formal": SourceSpec(
        "SRC4225_02_240_formal",
        FORMAL / "240-PPC4161-lambda-gamma-core-action-sign-and-binding-bound-source-row.md",
        "Open-system route",
        "Formal 4224 statement of boundary versus open-system route.",
    ),
    "SRC4225_03_red_team": SourceSpec(
        "SRC4225_03_red_team",
        FORMAL / "06-consistency-red-team.md",
        "Ordinary dissipative equations",
        "Red-team warning about damping from a single-field conservative action.",
    ),
    "SRC4225_04_core_repair": SourceSpec(
        "SRC4225_04_core_repair",
        FORMAL / "10-core-consistency-repair.md",
        "open-system effective action",
        "Core repair route for open/dissipative theory.",
    ),
    "SRC4225_05_parent_options": SourceSpec(
        "SRC4225_05_parent_options",
        FORMAL / "35-parent-stress-energy-options.md",
        "damping follows from the written closed action",
        "Parent stress-energy audit explicitly forbids closed-action damping overclaim.",
    ),
    "SRC4225_06_parent_v0": SourceSpec(
        "SRC4225_06_parent_v0",
        FORMAL / "36-minimal-parent-equations-v0.md",
        "old damping-like term is not included",
        "Minimal parent equations route damping to open-system/memory sector.",
    ),
    "SRC4225_07_parent_v1": SourceSpec(
        "SRC4225_07_parent_v1",
        FORMAL / "83-parent-equations-v1.md",
        "damping-like terms do not belong",
        "Parent v1 repeats damping belongs only after valid open-system/action method.",
    ),
    "SRC4225_08_doubled": SourceSpec(
        "SRC4225_08_doubled",
        FORMAL / "140-doubled-open-system-metric-null-theorem.md",
        "Doubled/open-system machinery",
        "Doubled open-system route exists but pure route fails metric-null proof.",
    ),
    "SRC4225_09_owner": SourceSpec(
        "SRC4225_09_owner",
        FORMAL / "141-doubled-owner-connection-current-primitive.md",
        "projection theorem missing",
        "Owner-current primitive candidate with projection/solder blocker.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def route_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GDR4225_0_boundary_identity",
            "boundary repair",
            "-gamma psi psi_dot = -(gamma/2) d_t(psi^2)",
            "fixed gamma; fixed endpoints or no-flux boundary; no claim that gamma causes damping",
            "E_gamma_bath_or_open_abs=0 for local energy sign",
            "CONDITIONAL_ENERGY_SAFE_NO_DAMPING",
        ),
        (
            "GDR4225_1_boundary_cost",
            "boundary repair cost",
            "closed local core equation loses the gamma psi_dot damping term",
            "ordinary fixed-endpoint variation of a total derivative does not produce bulk damping",
            "damping/collapse/decoherence claims cannot use this route",
            "COST_EXPLICIT",
        ),
        (
            "GDR4225_2_open_system_action",
            "open-system repair",
            "S_total[psi,B,g]=S_cons[psi,g]+S_bath[B,g]+S_int[psi,B,g] or doubled/influence action",
            "bath/doubled variables must be parent-owned",
            "damping can be physical if total energy-momentum is conserved",
            "REPAIR_ROUTE_BUILT_NOT_SIGNED",
        ),
        (
            "GDR4225_3_energy_balance",
            "gamma bath balance",
            "dE_psi/dt = - int gamma psi_dot^2 dV - Phi_boundary; dE_bath/dt = + int gamma psi_dot^2 dV + Phi_boundary",
            "positive gamma and matched bath flux",
            "closed combined system can conserve energy while psi damps",
            "BALANCE_LAW_SCHEMA_READY",
        ),
        (
            "GDR4225_4_covariant_balance",
            "covariant exchange balance",
            "nabla_mu K_psi^{mu nu} = -q_gamma^nu; nabla_mu(K_bath+K_int)^{mu nu}=q_gamma^nu",
            "q_gamma and bath stress must be explicit",
            "Bianchi-safe route for damping in local/galaxy/cosmology branches",
            "COVARIANT_SCHEMA_READY",
        ),
        (
            "GDR4225_5_metric_guard",
            "local metric guard",
            "P_loc q_gamma^nu=0 or bounded; delta_g K_bath is boundary/gauge/PPN-null or bounded",
            "owner-current/solder projection still unsigned",
            "prevents bath from becoming hidden local fifth force",
            "GUARD_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "formula_or_statement": formula,
            "required_conditions": conditions,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, formula, conditions, effect, status in data
    ]


def obligation_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GDO4225_0_gamma_mode",
            "gamma_mode",
            "choose boundary_route or open_system_route for the local packet",
            "MISSING_BRANCH_ADOPTION",
            "declared",
        ),
        (
            "GDO4225_1_bath_variables",
            "B_gamma",
            "explicit bath/doubled/influence variables and action terms",
            "MISSING_OPEN_SYSTEM_PARENT",
            "field_declared",
        ),
        (
            "GDO4225_2_energy_balance",
            "E_gamma_bath_or_open_abs",
            "zero under boundary route or source-backed bath energy balance under open route",
            "MISSING_ZERO_OR_BOUND",
            "energy",
        ),
        (
            "GDO4225_3_exchange_current",
            "q_gamma^nu",
            "covariant exchange current generated by gamma damping",
            "MISSING_CURRENT_SOURCE",
            "L^-3 curvature_scaled",
        ),
        (
            "GDO4225_4_bath_stress_guard",
            "K_bath_gamma^{mu nu}",
            "bath stress is boundary/gauge/PPN-null or finite bounded in local tests",
            "MISSING_STRESS_GUARD",
            "L^-2 curvature_scaled",
        ),
        (
            "GDO4225_5_solder_projection",
            "owner_spacetime_solder",
            "projection from owner/bath current to spacetime conservation without reintroducing metric stress",
            "MISSING_SOLDER_THEOREM",
            "map",
        ),
        (
            "GDO4225_6_demote_if_missing",
            "damped_core_status",
            "if open-system owner fails, damped psi equation is phenomenological closure outside local-GR proof",
            "DEMOTION_RULE_READY",
            "status",
        ),
    ]
    return [
        {
            **common(),
            "obligation_id": obligation_id,
            "quantity": quantity,
            "required_row": required_row,
            "current_status": status,
            "units": units,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for obligation_id, quantity, required_row, status, units in data
    ]


def updated_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GDB4225_0_boundary_energy",
            "boundary_route",
            "E_gamma_bath_or_open_abs=0",
            "if gamma is boundary-routed and no damping is claimed from it",
            "CONDITIONAL_ZERO_ROUTE_NOT_ADOPTED",
        ),
        (
            "GDB4225_1_open_energy",
            "open_system_route",
            "E_gamma_bath_or_open_abs <= int_W dt dV |gamma| psi_dot^2 + |Phi_boundary_gamma| + |Delta_bath_mismatch|",
            "if physical damping is retained",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "GDB4225_2_core_bound",
            "core_energy_bound",
            "E_MTS_core_neg_abs <= E_gamma_bath_or_open_abs + E_signature_mismatch_abs",
            "after 4224 lambda sign reduction",
            "BOUND_RETAINED_NOT_SCORE_READY",
        ),
        (
            "GDB4225_3_local_projection",
            "local_projection_bound",
            "|P_loc q_gamma| + |P_loc delta_g K_bath| <= source-backed local tolerance",
            "needed if open-system damping touches local branch",
            "LOCAL_PROJECTION_BOUND_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "branch": branch,
            "formula_or_bound": formula,
            "condition": condition,
            "status": status,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, branch, formula, condition, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "boundary_route_energy_safe": "True",
            "boundary_route_damping_owned": "False",
            "open_system_route_schema_ready": "True",
            "open_system_route_parent_owned": "False",
            "gamma_mode_available": "False",
            "E_gamma_bound_available": "False",
            "local_projection_available": "False",
            "M_EH_positive_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "choose_boundary_branch_or_fill_open_system_bath_current_stress_rows",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("GDF4225_0_no_magic_damping", "derive damping from fixed gamma total derivative", "blocked", "fixed-boundary total derivative cannot supply bulk damping"),
        ("GDF4225_1_no_free_boundary_adoption", "use boundary route while keeping damping claims", "blocked", "boundary route is energy-safe only by not claiming damping from gamma"),
        ("GDF4225_2_no_bath_without_stress", "add bath/doubled variables without stress/current rows", "blocked", "open-system route requires q_gamma and K_bath guards"),
        ("GDF4225_3_no_metric_dumping", "hide local residuals in an unobservable bath", "blocked", "bath projection must be PPN-null, boundary, gauge, or bounded"),
        ("GDF4225_4_no_local_GR_claim", "promote gamma repair to M_EH/local-GR pass", "blocked", "branch choice, bath/stress rows, binding and remaining epsilon_E inputs are still open"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "GDS4225_STATUS",
            "decision": DECISION,
            "summary": "Gamma has two honest routes: boundary route is local-energy safe but gives up damping; open-system route can keep damping only with bath/current/stress/projection rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4225 converts the gamma fork into a branch decision plus exact bath-current/stress row obligations.",
            "derive_first": "try open-system bath balance with q_gamma and K_bath stress guard",
            "fill_second": "if open route fails, explicitly adopt boundary branch for local-GR energy and demote damping claims out of the local proof",
            "fallback": "retain E_gamma_bath_or_open_abs as an unscored bound row and keep M_EH unavailable",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 241 - PPC4161 Gamma Damping Open-System Action Or Boundary Repair

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## The fork

From 4224:

```text
-gamma psi psi_dot = -(gamma/2) d_t(psi^2).
```

So a fixed-`gamma` single-field conservative action gives a boundary term, not physical damping.

There are only two honest routes.

## Route A: conservative boundary repair

Adopt:

```text
E_gamma_bath_or_open_abs = 0.
```

This is safe for the local `M_EH` sign gate if endpoint/boundary data are fixed or no-flux. But the cost is explicit:

```text
gamma psi_dot damping is not derived in the closed local core.
```

Quantum/collapse/decoherence/damping language cannot use this route as evidence.

## Route B: open-system damping repair

Keep damping only by adding parent-owned bath/doubled/influence variables:

```text
S_total[psi,B,g] = S_cons[psi,g] + S_bath[B,g] + S_int[psi,B,g].
```

The minimal energy balance is:

```text
dE_psi/dt = - int gamma psi_dot^2 dV - Phi_boundary,
dE_bath/dt = + int gamma psi_dot^2 dV + Phi_boundary.
```

The covariant version must satisfy:

```text
nabla_mu K_psi^{{mu nu}} = -q_gamma^nu,
nabla_mu(K_bath+K_int)^{{mu nu}} = q_gamma^nu.
```

For local-GR safety:

```text
P_loc q_gamma^nu = 0 or bounded,
delta_g K_bath = boundary/gauge/PPN-null or bounded.
```

## Updated bound

After the 4224 lambda sign reduction:

```text
E_MTS_core_neg_abs <= E_gamma_bath_or_open_abs + E_signature_mismatch_abs.
```

## Next target

`{NEXT_TARGET}` should either fill the bath/current/stress rows or adopt the boundary route explicitly for the local-GR proof while quarantining damping claims.
"""


def checkpoint_doc() -> str:
    return f"""# 4225 - Gamma Damping Open-System Action Or Boundary Repair

**Status:** `{DECISION}`.

## Main move

`gamma` is no longer a vague problem. It has two allowed routes:

- boundary route: energy-safe, sets `E_gamma_bath_or_open_abs=0`, but does not derive damping;
- open-system route: keeps damping, but requires bath variables, `q_gamma^nu`, `K_bath`, and local projection/stress guards.

## No claim

No `M_EH`, `M_H_ref`, local-GR, Newton or PPN claim is made. The next task is a branch decision or a real bath/current source row.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The gamma damping obstruction is reduced to a strict two-route fork: the conservative boundary route is local-energy safe but cannot claim damping, while the open-system route can retain damping only with parent-owned bath/doubled variables, q_gamma exchange current, K_bath stress guard, and local projection bounds.",'
        f'"4225 source audit, route split, obligation rows, updated gamma bound rows, decision and firewall.",'
        f'private_gamma_boundary_or_open_system_repair_nonclaim,'
        f'"Either fill the gamma bath/current/stress source rows or explicitly adopt boundary gamma for the local-GR energy proof and quarantine damping claims.",'
        f'"This is a route fork, not an M_EH/local-GR proof; branch choice and rows remain unscored."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 100. Gamma Boundary Or Open-System Repair

Marker: `{MARKER}`

4225 resolves the gamma ambiguity into two non-cheating routes:

```text
E_gamma_bath_or_open_abs = 0
```

only on the boundary route, which gives up damping as a closed-action result; or:

```text
nabla_mu K_psi^{{mu nu}} = -q_gamma^nu,
nabla_mu(K_bath+K_int)^{{mu nu}} = q_gamma^nu
```

on the open-system route, which must own bath stress and local projection bounds.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Gamma Repair Fork

Marker: `{PACKET_MARKER}`

The packet may use the gamma boundary route for local energy safety only if damping claims are quarantined. If damping is retained, bath/current/stress rows must be filled before `M_EH` positivity can score.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4225_SOURCE_REGISTER.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4225_ROUTE_SPLIT.csv"]
    obligations = rows_by_file["P8_Y5_R2FR_4225_OPEN_SYSTEM_OBLIGATIONS.csv"]
    bounds = rows_by_file["P8_Y5_R2FR_4225_UPDATED_BOUND_ROWS.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4225_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4225_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4225_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]

    checks = [
        ("VAL4225_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4225_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4225_2_route_split",
            "route rows include boundary repair, open-system action, energy balance and metric guard",
            {"GDR4225_0_boundary_identity", "GDR4225_2_open_system_action", "GDR4225_3_energy_balance", "GDR4225_5_metric_guard"}.issubset({row["route_id"] for row in routes}),
        ),
        (
            "VAL4225_3_obligations",
            "obligations include gamma mode, bath variables, energy, current, stress and solder",
            {"gamma_mode", "B_gamma", "E_gamma_bath_or_open_abs", "q_gamma^nu", "K_bath_gamma^{mu nu}", "owner_spacetime_solder"}.issubset({row["quantity"] for row in obligations}),
        ),
        (
            "VAL4225_4_bounds",
            "bounds include boundary zero, open energy, core bound and local projection",
            {"GDB4225_0_boundary_energy", "GDB4225_1_open_energy", "GDB4225_2_core_bound", "GDB4225_3_local_projection"}.issubset({row["bound_id"] for row in bounds}),
        ),
        (
            "VAL4225_5_decision_nonclaim",
            "decision records boundary-safe/no-damping and open-system-not-owned",
            decision["boundary_route_energy_safe"] == "True"
            and decision["boundary_route_damping_owned"] == "False"
            and decision["open_system_route_parent_owned"] == "False"
            and decision["local_GR_claim"] == "False",
        ),
        (
            "VAL4225_6_firewall",
            "firewall blocks magic damping, free boundary adoption, bath without stress, metric dumping and local-GR claim",
            {"GDF4225_0_no_magic_damping", "GDF4225_1_no_free_boundary_adoption", "GDF4225_2_no_bath_without_stress", "GDF4225_3_no_metric_dumping", "GDF4225_4_no_local_GR_claim"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4225_7_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4225_8_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4225_9_claim_register", "claim register contains L-066", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4225_10_spine_packet", "spine and packet contain 4225 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4225_11_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4225_12_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4225_gamma_damping_open_system_action_or_boundary_repair.py").exists()),
        ("VAL4225_13_status", "status records nonclaim route split", rows_by_file["P8_Y5_R2FR_4225_STATUS.csv"][0]["decision"] == DECISION),
        (
            "VAL4225_14_boundary_cost",
            "boundary route explicitly costs damping ownership",
            any(row["route_id"] == "GDR4225_1_boundary_cost" and row["status"] == "COST_EXPLICIT" for row in routes),
        ),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4225_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4225_ROUTE_SPLIT.csv": route_rows(),
        "P8_Y5_R2FR_4225_OPEN_SYSTEM_OBLIGATIONS.csv": obligation_rows(),
        "P8_Y5_R2FR_4225_UPDATED_BOUND_ROWS.csv": updated_bound_rows(),
        "P8_Y5_R2FR_4225_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4225_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4225_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4225_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
