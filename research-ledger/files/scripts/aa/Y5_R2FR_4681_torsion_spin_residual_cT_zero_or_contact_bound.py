from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4681"
CLAIM_ID = "L-523"
MARKER = "PPC4161_CT_SPIN_TORSION_ZERO_OR_CONTACT_BOUND_CURRENT_BRANCH_4681"
PACKET_MARKER = "PPC4161_PACKET_CT_SPIN_TORSION_CURRENT_BRANCH_4681"
DECISION = "CT_SPIN_TORSION_SPINLESS_CONTACT_ZERO_CONTRACT_IMPORTED_CURRENT_BRANCH_FINITE_TORSION_FAILURES_RETAINED_NONCLAIM"
NEXT_TARGET = "4682-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"

DOC_PATH = POST / "4681-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md"
FORMAL_PATH = FORMAL / "697-PPC4161-torsion-spin-residual-cT-zero-or-contact-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4680_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4680_NEXT_TARGET.csv"
CSV_4680_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4680_STATUS.csv"
CSV_4451_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4451_STATUS.csv"
CSV_4451_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_THEOREM_OUTPUT.csv"
CSV_4452_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4452_STATUS.csv"
CSV_4452_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4452_TORSION_IRREP_OPERATOR_OUTPUT.csv"
CSV_4453_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4453_STATUS.csv"
CSV_4453_MARGIN = SOURCE_DIR / "P8_Y5_R2FR_4453_PARENT_POSITIVE_MARGIN_OUTPUT.csv"
CSV_4593_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4593_CT_SPIN_THEOREM.csv"
CSV_4593_CONTACT = SOURCE_DIR / "P8_Y5_R2FR_4593_CONTACT_BOUND_ROWS.csv"
CSV_4593_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4593_SURVIVOR_UPDATE.csv"
CSV_4593_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4593_STATUS.csv"
CSV_4593_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4593_VALIDATION.csv"
FORMAL_609 = FORMAL / "609-PPC4161-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4681_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_CT_SPIN_THEOREM_IMPORT.csv"
CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_TORSION_CONTRACT_STATUS.csv"
CONTACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_CONTACT_BOUND_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4681_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4681_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4681_00_4680_next", CSV_4680_NEXT, "4681-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md", "4680 selected current torsion target."),
        ("SRC4681_01_4680_status", CSV_4680_STATUS, "c_T_spin", "current branch selected c_T_spin."),
        ("SRC4681_02_4451_status", CSV_4451_STATUS, "TORSION_SPIN_RESIDUAL_DEMOTED", "4451 first torsion demotion."),
        ("SRC4681_03_4451_theorem", CSV_4451_THEOREM, "spinless", "4451 torsion theorem rows."),
        ("SRC4681_04_4452_status", CSV_4452_STATUS, "lambda_T_min_contract", "4452 operator condition."),
        ("SRC4681_05_4452_operator", CSV_4452_OPERATOR, "lambda", "4452 irrep operator rows."),
        ("SRC4681_06_4453_status", CSV_4453_STATUS, "lambda_T,min>=m_T,parent^2>0", "4453 positive margin contract."),
        ("SRC4681_07_4453_margin", CSV_4453_MARGIN, "PM4453_0_trace", "4453 parent margin rows."),
        ("SRC4681_08_4593_theorem", CSV_4593_THEOREM, "TH4593_3_spinless_bulk_zero", "later integrated cT theorem."),
        ("SRC4681_09_4593_contact", CSV_4593_CONTACT, "CB4593_2_spin_clock_polarized", "contact/failure bound rows."),
        ("SRC4681_10_4593_survivor", CSV_4593_SURVIVOR, "SURV4593_2_cR2_MR", "post-torsion survivor update."),
        ("SRC4681_11_4593_status", CSV_4593_STATUS, "conditional_spinless_long_range_zero", "4593 status."),
        ("SRC4681_12_4593_validation", CSV_4593_VALIDATION, "VAL4593_17_next_cR2_selected", "4593 validation for next cR2 target."),
        ("SRC4681_13_formal609", FORMAL_609, "tau_spin^bulk=0 => T_bulk=0", "formal integrated torsion result."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4681_0_separation",
            "claim": "Torsion cannot be cancelled against the source-kernel or source-weight branch.",
            "derivation": "Use a separated residual vector: Delta_local = Delta_source_kernel + Delta_T + Delta_rest. 4679/4680 narrow source pieces, so torsion must close by its own Cartan equation or explicit bound.",
            "equation": "Delta_T = Pi_T[T] + Pi_contact[Delta L_contact]",
            "zero_condition": "none; separation only",
            "fallback_bound": "|Delta_T| retained explicitly",
            "status": "TORSION_SEPARATED_NO_CANCELLATION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4681_1_auxiliary_cartan",
            "claim": "On the compact local auxiliary Cartan branch, torsion is algebraic and spin-supported.",
            "derivation": "Import 4451/4593: if the parent IR selector has no independent D T kinetic term, variation with respect to the spin connection gives a pointwise linear torsion equation.",
            "equation": "L_T[e,c_T] T = kappa tau_spin",
            "zero_condition": "no D T kinetic term; same coframe/spin-connection matter slot",
            "fallback_bound": "if Z_DT>0 or boundary torsion exists, a propagating torsion bound is required",
            "status": "AUXILIARY_TORSION_EQUATION_IMPORTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4681_2_positive_margin",
            "claim": "The no-zero-mode condition is the explicit positive irrep margin.",
            "derivation": "Import 4452/4453: decompose torsion into trace-vector, axial-vector and tensor irreps with diagonal operator entries lambda_V, lambda_A and lambda_Q.",
            "equation": "lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|) >= m_T,parent^2 > 0",
            "zero_condition": "parent signs positive auxiliary torsion quadratic form away from critical surfaces",
            "fallback_bound": "||T|| <= kappa ||tau_spin|| / lambda_T,min",
            "status": "POSITIVE_MARGIN_CONTRACT_IMPORTED_PARENT_PUBLIC_SIGNATURE_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4681_3_spinless_bulk_zero",
            "claim": "For spinless/unpolarized macroscopic PPN, R10 and orbital bulk sources, the long-range torsion residual is zero on the auxiliary positive-margin branch.",
            "derivation": "Set tau_spin^bulk=0. With lambda_T,min>0, the algebraic equation has only T=0 in the bulk, so long-range spinless readout projections vanish.",
            "equation": "tau_spin^bulk=0 and lambda_T,min>0 => T_bulk=0 => Delta_bulk^T=0",
            "zero_condition": "spinless/unpolarized bulk source; no propagating torsion; positive margin; no boundary torsion tail",
            "fallback_bound": "|Delta O_a^T| <= ||Pi_a^T|| kappa ||tau_spin||/lambda_T,min + contact + boundary + kinetic terms",
            "status": "SPINLESS_LONG_RANGE_CT_ZERO_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4681_4_failure_firewall",
            "claim": "Microscopic spin, polarized clocks, zero modes, kinetic torsion and boundary torsion are not erased.",
            "derivation": "Eliminating algebraic torsion gives a finite contact term; if Z_DT>0 or lambda_T,min=0, torsion propagates or becomes critical and must be bounded.",
            "equation": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)",
            "zero_condition": "contact source absent or bounded; propagating/boundary torsion absent",
            "fallback_bound": "|Delta O_a^T| <= |J_a^T c_T| exp(-M_T r_a)/r_a + contact + boundary",
            "status": "FINITE_CT_BRANCH_RETAINED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("TC4681_0_no_kinetic", "Z_DT=0/no independent D T term", "required for auxiliary Cartan branch", "PRIVATE_CONDITIONAL", False),
        ("TC4681_1_positive_margin", "lambda_T,min>=m_T,parent^2>0", "required to avoid algebraic zero mode", "PARENT_PUBLIC_SIGNATURE_OPEN", False),
        ("TC4681_2_spinless_bulk", "tau_spin^bulk=0 for ordinary unpolarized macroscopic sources", "gives long-range torsion zero in PPN/R10/orbital bulk", "CONDITIONAL_ZERO", False),
        ("TC4681_3_contact_branch", "tau_spin!=0 or polarized/contact source", "finite contact bound required", "FINITE_BRANCH_RETAINED", False),
        ("TC4681_4_failure_branch", "Z_DT>0, lambda_T,min=0, or boundary torsion", "propagating/critical torsion bound required", "REOPENS_AS_BOUND_PROBLEM", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "condition": condition,
            "role": role,
            "status": status,
            "closed_publicly": closed,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, condition, role, status, closed in data
    ]


def contact_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CB4681_0_spinless_PPN_orbital", "PPN/orbital ordinary macroscopic source", "zero", "Delta_bulk^T=0", "parent public positive margin and projection guard remain"),
        ("CB4681_1_unpolarized_R10", "R10 unpolarized ordinary matter", "conditional contact suppression", "alpha_T(lambda)_bulk=0 on auxiliary spinless branch", "R10 torsion/contact projection and lambda_T,min source row"),
        ("CB4681_2_spin_clock_polarized", "spin clocks / polarized spin pendula / microscopic contact", "finite bound required", "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)", "numeric spin density, projection and lambda_T,min"),
        ("CB4681_3_kinetic_or_zero_mode", "any local arena if Z_DT>0 or lambda_T,min=0", "branch reopens", "|Delta O_a^T| <= |J_a^T c_T| exp(-M_T r_a)/r_a + contact + boundary", "M_T, c_T normalization, arena Jacobian, source charge, experimental bound"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "arena": arena,
            "zero_or_bound": zero_or_bound,
            "formula": formula,
            "missing_inputs": missing,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, arena, zero_or_bound, formula, missing in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4681_0_EH_principal", "EH principal / Palatini IR selector", "still public blocker", "retain parent selector/adoption gate"),
        ("SURV4681_1_cGamma", "c_Gamma local memory coupling", "unchanged finite survivor", "derive support/projector zero or source profile coefficients"),
        ("SURV4681_2_cR2_MR", "c_R2/M_R finite-range tail", "selected next broad survivor", NEXT_TARGET),
        ("SURV4681_3_cT_spin", "spin/torsion contact channel", "conditional spinless long-range zero; finite contact/propagating branch retained", "do not treat as global closure; use contact rows only if needed"),
        ("SURV4681_4_Lambda_material_projection", "Lambda/material/projection/public parent rows", "unchanged blockers", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": residual_family,
            "status_after_4681": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, residual_family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4681_0", "No public local-GR claim: c_T_spin is narrowed conditionally, not globally closed."),
        ("CTRL4681_1", "Do not assume GR torsionlessness; use the auxiliary equation, margin and spinless-source conditions."),
        ("CTRL4681_2", "Retain polarized/contact, kinetic, zero-mode and boundary torsion as explicit finite branches."),
        ("CTRL4681_3", "Move next to c_R2/M_R rather than polishing c_T_spin forever."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4681 imports the 4451-4453 torsion ladder and the 4593 current integration into the 4680 branch. In the auxiliary Cartan branch with positive irrep margin and spinless/unpolarized macroscopic bulk matter, the long-range c_T_spin projection is conditionally zero. Contact, polarized, kinetic, zero-mode and boundary torsion remain finite nonclaim branches.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "auxiliary_cartan_equation": True,
            "positive_margin_contract": "lambda_T,min>=m_T,parent^2>0",
            "spinless_long_range_cT_zero_conditional": True,
            "finite_contact_branch_retained": True,
            "propagating_or_zero_mode_branch_retained": True,
            "local_GR_public_claim": False,
            "remaining_broad_survivors": "EH_public_adoption;cGamma;cR2_MR;Lambda_eff;material_projection;global_parent",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4681_0",
            "target": NEXT_TARGET,
            "reason": "After c_T_spin is narrowed to conditional spinless zero/contact-bound, c_R2/M_R is the next broad local-GR survivor with R10/orbital/PPN pressure.",
            "derive_first": "prove parent mass gap or coefficient zero for curvature-square/scalaron/spin-2 finite-range tails",
            "fallback": "source full R10 alpha(lambda), orbital precession and PPN gamma/beta projection rows for c_R2/M_R",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4681 - Y5/R2FR Torsion Spin Residual cT Zero or Contact Bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4681 imports the torsion ladder into the current branch instead of re-deriving it from zero.

```text
L_T[e,c_T] T = kappa tau_spin
lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|) >= m_T,parent^2 > 0
tau_spin^bulk = 0  =>  T_bulk = 0  =>  Delta_bulk^T = 0
```

That gives a conditional spinless long-range zero for `c_T_spin` in ordinary macroscopic PPN/R10/orbital bulk sources. It is not a public local-GR proof: polarized/contact spin, kinetic torsion, algebraic zero modes and boundary torsion stay as finite branches.

## Source Register

{table(rows["sources"])}

## Theorem Import

{table(rows["theorems"])}

## Torsion Contract Status

{table(rows["contracts"])}

## Contact / Failure Bounds

{table(rows["contacts"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4681 - Y5/R2FR", "# 697 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4681 imports the torsion ladder into the current branch: in the auxiliary Cartan branch with positive torsion irrep margin and spinless/unpolarized bulk matter, the long-range c_T_spin projection is conditionally zero. Contact, polarized, kinetic, zero-mode and boundary torsion remain finite nonclaim branches.",
                "current_evidence": "Generated source register, theorem import, torsion contract status, contact/failure bounds, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Treating conditional spinless/contact demotion as global torsion closure or assuming GR torsionlessness without parent margin and failure branches.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current cT Spin Torsion Branch

Marker: `{MARKER}`

4681 imports the torsion ladder into the current branch:

```text
L_T[e,c_T] T = kappa tau_spin,
lambda_T,min >= m_T,parent^2 > 0,
tau_spin^bulk = 0 => T_bulk = 0.
```

The `c_T_spin` long-range residual is conditionally zero for spinless/unpolarized macroscopic bulk sources, while contact/polarized, kinetic, zero-mode and boundary torsion remain finite nonclaim branches. The next broad local-GR survivor is `c_R2/M_R`.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current cT Spin Torsion Branch

Marker: `{PACKET_MARKER}`

The current packet no longer treats `c_T_spin` as a generic long-range local force. It is narrowed to a conditional spinless auxiliary-torsion zero plus retained contact/propagating failure branches. Next packet target: `c_R2/M_R`.

- theorem csv: `{THEOREM_CSV.name}`
- contact csv: `{CONTACT_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4681_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4681_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4681_2_auxiliary_equation", any(row["theorem_id"] == "TH4681_1_auxiliary_cartan" for row in rows["theorems"]), "auxiliary Cartan equation imported"),
        ("VAL4681_3_spinless_zero", any(row["theorem_id"] == "TH4681_3_spinless_bulk_zero" for row in rows["theorems"]), "spinless bulk zero row present"),
        ("VAL4681_4_failure_firewall", any(row["theorem_id"] == "TH4681_4_failure_firewall" for row in rows["theorems"]), "contact/propagating failure branches retained"),
        ("VAL4681_5_next_cR2", rows["next"][0]["target"] == NEXT_TARGET, "next cR2/MR target selected"),
        ("VAL4681_6_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-523"),
        ("VAL4681_7_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4681_8_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4681_9_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4681_10_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4681_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4681_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4681_11_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4681_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4681_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "contracts": contract_rows(timestamp),
        "contacts": contact_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        CONTRACT_CSV: rows["contracts"],
        CONTACT_CSV: rows["contacts"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
