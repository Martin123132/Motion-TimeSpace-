from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4379"
CLAIM_ID = "L-220"
MARKER = "PPC4161_TRANSITION_HARMONIC_NULL_PARENT_SIGNATURE_OR_FIRST_NUMERIC_TOPOLOGICAL_MOMENT_INPUT_4379"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_HARMONIC_NULL_PARENT_SIGNATURE_OR_FIRST_NUMERIC_TOPOLOGICAL_MOMENT_INPUT_4379"
DECISION = "HARMONIC_NULL_SIGNATURE_SPLIT_INTO_LAPLACIAN_OR_L0_SYMMETRY_ROUTES_NUMERIC_MOMENT_INPUT_TEMPLATE_STAGED_NONCLAIM"
NEXT_TARGET = "4380-Y5-R2FR-transition-topological-moment-source-intake-or-l0-parent-symmetry-signature.md"

FORMAL_PATH = FORMAL / "395-PPC4161-transition-harmonic-null-parent-signature-or-first-numeric-topological-moment-input.md"
DOC_PATH = POST / "4379-Y5-R2FR-transition-harmonic-null-parent-signature-or-first-numeric-topological-moment-input.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4379_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
BOUND_ROWS_PATH = SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4379_00_4378_formal": (
        FORMAL / "394-PPC4161-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md",
        "delta rho_top = Delta u_top",
        "4378 derives the Laplacian/harmonic-null sufficient condition.",
    ),
    "SRC4379_01_4378_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_NEXT_TARGET.csv",
        "4379-Y5-R2FR-transition-harmonic-null-parent-signature-or-first-numeric-topological-moment-input.md",
        "4378 handoff naming this checkpoint.",
    ),
    "SRC4379_02_4378_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv",
        "HN4378_1_laplacian_null_sufficient_condition",
        "4378 theorem row for Laplacian/harmonic-null route.",
    ),
    "SRC4379_03_4378_bounds": (
        BOUND_ROWS_PATH,
        "TB4378_SUP4371_2_Sun_Earth_average_dipole",
        "4378 generated first dipole/quadrupole multipole bound rows.",
    ),
    "SRC4379_04_4356_static": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "Q_l>=1_tr = 0",
        "4356 already identifies static l=0 exterior uniqueness as the multipole-hair zero route.",
    ),
    "SRC4379_05_4356_common": (
        FORMAL / "372-PPC4161-transition-static-monopole-universal-rangefree-hair-zero-or-bound.md",
        "q_0^H :=",
        "4356 defines the common Hilbert monopole source dressing.",
    ),
    "SRC4379_06_4294_kernel": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube",
        "4294 defines the source-kernel projector containing the safe l=0 branch.",
    ),
    "SRC4379_07_4377_moments": (
        SOURCE_DIR / "P8_Y5_R2FR_4377_TEST_FUNCTION_MOMENT_GATE.csv",
        "MOM4377_2_dipole",
        "4377 defines the first missing dipole moment gate.",
    ),
    "SRC4379_08_hamiltonian_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Same-Object Glue",
        "Hamiltonian/worldtube glue is same-charge support but not itself moment-zero.",
    ),
    "SRC4379_09_boundary_topological": (
        FORMAL / "143-boundary-topological-backup-gate.md",
        "bulk metric-nullity passes formally, but is insufficient.",
        "boundary/topological metric-nullity does not prove local profile or moment safety.",
    ),
    "SRC4379_10_charge_status": (
        SOURCE_DIR / "P8_charge_current_equality_STATUS.csv",
        "charge-current equality parent-derived,fail",
        "current corpus keeps charge-current equality nonclaim.",
    ),
    "SRC4379_11_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "EM/Poynting must remain in Hilbert stress or boundary flux, not a fake topological moment.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_signature_audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "signature_id": "SIG4379_0_laplacian_null",
            "candidate_signature": "delta rho_top=Delta u_top with boundary-silent u_top",
            "mathematical_effect": "Green identity kills all exterior harmonic moments M_lm",
            "current_evidence": "4378 theorem gives sufficiency",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "generic topological/exact terms are not necessarily Laplacian-null",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "SIG4379_1_centered_l0_symmetry",
            "candidate_signature": "delta rho_top=f(r) in the same source center/frame with zero monopole",
            "mathematical_effect": "angular integral of Y_lm kills every l>=1 moment; monopole is zero by charge matching",
            "current_evidence": "4356/4294 source-kernel uses static l=0 common Hilbert monopole as the safe branch",
            "current_status": "CONDITIONAL_THEOREM_NOT_RAW_PARENT_SIGNED",
            "failure_mode": "off-center, anisotropic, readout-shifted or non-spherical topological profile creates dipole/quadrupole moments",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "SIG4379_2_distributional_equality",
            "candidate_signature": "rho_top=rho_H as distributions",
            "mathematical_effect": "stronger than exterior safety: E_top_profile=0 pointwise/distributionally",
            "current_evidence": "4377 all-test-function gate",
            "current_status": "NOT_PROVED",
            "failure_mode": "same total charge without profile equality",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "SIG4379_3_same_charge_only",
            "candidate_signature": "int_W delta rho_top dV=0",
            "mathematical_effect": "kills monopole only",
            "current_evidence": "186/187 same charge/worldtube support",
            "current_status": "INSUFFICIENT",
            "failure_mode": "dipole/quadrupole profile defects survive",
            "valid_for_claim": "False",
        },
        {
            "signature_id": "SIG4379_4_metric_null_topological",
            "candidate_signature": "delta_g S_top=0 or dJ_top=0",
            "mathematical_effect": "does not imply harmonic moment silence",
            "current_evidence": "143 and 4378 reject metric-null/closed shortcuts",
            "current_status": "INSUFFICIENT",
            "failure_mode": "metric-null or closed current can still be wrong density representative for Newton profile",
            "valid_for_claim": "False",
        },
    ]


def l0_symmetry_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "L0S4379_0_statement",
            "statement": "If delta rho_top(y)=f(|y-y_c|) in the same center/frame as rho_H and int_W delta rho_top dV=0, then all exterior moments M_lm vanish.",
            "proof": "M_lm=int dr r^{l+2} f(r) int dOmega Y_lm; the angular integral is zero for l>=1 and the monopole is zero by charge matching.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "exterior Newton/topological profile residual is zero without requiring pointwise rho_top=rho_H",
            "current_blocker": "the parent action has not signed centered l=0 symmetry for rho_top-rho_H",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "L0S4379_1_center_guard",
            "statement": "The same-center/frame condition is essential; a readout shift creates a dipole even if the profile is radial in its own coordinates.",
            "proof": "translation of a zero-monopole radial defect generically changes M_1m relative to the Hilbert source center.",
            "status": "GUARD_DERIVED",
            "what_it_buys": "prevents hiding dipole hair in a coordinate/source-center choice",
            "current_blocker": "source center and profile frame must be parent-owned before scoring",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "L0S4379_2_l0_not_distributional",
            "statement": "Centered l=0 zero-monopole safety is exterior Newton safety, not distributional equality inside W_H.",
            "proof": "a radial positive/negative shell with zero total mass can have rho_top != rho_H internally while producing no exterior Newton field.",
            "status": "FIREWALL_DERIVED",
            "what_it_buys": "keeps local-GR/profile claims narrower than exterior Newton/orbital safety",
            "current_blocker": "PPN/interior/source-structure uses may still need stronger profile equality",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "L0S4379_3_current_verdict",
            "statement": "The l=0 route is a good parent-signature target, but it is not active for the raw topological profile defect.",
            "proof": "4356/4294 identify static l=0 source-kernel safety conditionally, while 4378/4379 keep raw topological moments unfilled.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "what_it_buys": "gives a second exact theorem route besides Laplacian-null",
            "current_blocker": "need parent source-kernel/symmetry signature or finite moment input",
            "valid_for_claim": "False",
        },
    ]


def numeric_moment_input_template_rows() -> List[Dict[str, str]]:
    priority_supports = {"SUP4371_2_Sun_Earth_average", "SUP4371_4_Earth_Moon_average"}
    rows: List[Dict[str, str]] = []
    for bound in read_csv(BOUND_ROWS_PATH):
        if bound["support_id"] not in priority_supports:
            continue
        rows.append(
            {
                "input_id": f"MIN4379_{bound['support_id']}_l{bound['multipole_l']}",
                "bound_row": bound["bound_id"],
                "support_id": bound["support_id"],
                "multipole_l": bound["multipole_l"],
                "needed_quantity": "E_l^top or all M_lm values",
                "required_fields": "source_profile_path; rho_H_path; rho_top_path; W_H_definition; center_frame; M_H; R; M_lm_values_or_bound; extraction_method",
                "current_value": "MISSING_MOMENT_VALUE",
                "units": "dimensionless E_l^top or mass*length^l M_lm",
                "score_formula": bound["score_formula"],
                "pass_formula": bound["pass_formula"],
                "acceptance_rule": "valid only if profile paths exist, center/frame fixed before scoring, monopole subtracted, and no fitted cancellation is used",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def scoring_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for bound in read_csv(BOUND_ROWS_PATH):
        if bound["support_id"] not in {"SUP4371_2_Sun_Earth_average", "SUP4371_4_Earth_Moon_average"}:
            continue
        geometry = float(bound["geometry_factor_s_l"])
        rows.append(
            {
                "score_id": f"SCR4379_{bound['support_id']}_l{bound['multipole_l']}",
                "support_id": bound["support_id"],
                "source_body": bound["source_body"],
                "test_body_or_readout": bound["test_body_or_readout"],
                "multipole_l": bound["multipole_l"],
                "geometry_factor": f"{geometry:.12g}",
                "if_theorem_signed": "E_l^top=0",
                "if_numeric_input": bound["score_formula"],
                "pass_condition": bound["pass_formula"],
                "current_status": "WAITING_FOR_PARENT_SIGNATURE_OR_NUMERIC_MOMENT",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4379_0_laplacian_null",
            "claim_tested": "topological moments zero by Laplacian/harmonic-null parent signature",
            "required_inputs": "delta rho_top=Delta u_top plus boundary silence signed by parent source construction",
            "status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4379_1_l0_symmetry",
            "claim_tested": "topological moments zero by centered static l=0 symmetry",
            "required_inputs": "same-center/frame radial defect, zero monopole, source-kernel l=0 parent ownership before readout",
            "status": "BLOCKED_PARENT_SYMMETRY_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4379_2_numeric_moment",
            "claim_tested": "finite topological dipole/quadrupole row can be scored",
            "required_inputs": "source-backed E_l^top/M_lm values and arena delta_N bound",
            "status": "INPUT_TEMPLATE_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4379_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "topological moment route plus E_shadow/E_nonHilbert/E_readout and all remaining E_perp components closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4379_0",
            "decision": DECISION,
            "summary": (
                "4379 splits the parent harmonic-null target into two exact theorem routes. The Laplacian route from 4378 remains sufficient: delta rho_top=Delta u_top with boundary silence kills every exterior harmonic moment. "
                "A second exact route is now added: a centered static l=0 zero-monopole topological defect has no exterior Newton multipoles by angular orthogonality, though it is not full distributional equality inside W_H. "
                "Neither parent signature is currently signed for the raw topological/Hamiltonian defect, so 4379 stages the first numeric moment input templates for Sun-Earth and Earth-Moon dipole/quadrupole rows."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "it either signs one exact theorem route or fills the first real moment value; no more total-charge/topology shortcuts.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4379_0_laplacian",
            "object": "Laplacian/harmonic-null route",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "note": "strong route from 4378 remains open as a parent signature target.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4379_1_l0",
            "object": "centered static l=0 zero-monopole route",
            "status": "EXACT_CONDITIONAL_THEOREM_ADDED",
            "note": "safe for exterior Newton moments if same-center/frame and zero monopole are parent-owned.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4379_2_numeric",
            "object": "first numeric moment input",
            "status": "TEMPLATE_STAGED_VALUES_MISSING",
            "note": "Sun-Earth and Earth-Moon dipole/quadrupole inputs are staged as the first concrete source rows.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4379_3_next",
            "object": "next derivation",
            "status": "SOURCE_INTAKE_OR_L0_SIGNATURE_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4379_0",
            "target": NEXT_TARGET,
            "question": "Can the parent source-kernel sign centered l=0/harmonic-null topological safety, or must a real source profile/moment value be ingested?",
            "preferred_route": "derive same-center static l=0 zero-monopole ownership or Laplacian-null boundary silence from the parent topological/Hamiltonian source construction.",
            "fallback_route": "fill one Sun-Earth or Earth-Moon M_1m/M_2m/E_l^top row from an explicit profile or a conservative source-backed upper bound.",
            "avoid": "using same total charge, metric-nullity, exact divergence, topological class or post-readout coordinate centering as moment-zero evidence.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    signatures: List[Dict[str, str]],
    l0_rows: List[Dict[str, str]],
    templates: List[Dict[str, str]],
    scores: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: harmonic-null parent signature or first numeric topological moment input

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4379 sharpens the 4378 fork into two exact theorem routes plus a concrete source-input fallback.

Route A is the Laplacian/harmonic-null signature:

```text
delta rho_top = Delta u_top,
boundary[h partial_n u_top - u_top partial_n h] = 0
=> M_lm=0 for every exterior harmonic h_lm.
```

Route B is the centered static `l=0` route:

```text
delta rho_top(y)=f(|y-y_c|),
int_W delta rho_top dV=0,
same center/frame as rho_H before readout
=> M_lm=0 for all l>=1,m and M_0=0.
```

This is a real new option: it can make the exterior Newton/orbital topological defect harmless without proving pointwise profile equality inside the source. But it is narrower than local-GR profile equality, so it is not overclaimed.

Neither route is parent-signed for the raw topological/Hamiltonian defect. Therefore 4379 stages the first concrete source rows: Sun-Earth and Earth-Moon dipole/quadrupole moment inputs, using the 4378 scoring law:

```text
|delta a_l|/|a_N| <= E_l^top (R/r)^l.
```

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Parent Signature Audit

{md_table(signatures, ["signature_id", "candidate_signature", "mathematical_effect", "current_evidence", "current_status", "failure_mode"])}

## Centered l=0 Symmetry Theorem

{md_table(l0_rows, ["theorem_id", "statement", "proof", "status", "what_it_buys", "current_blocker"])}

## Numeric Moment Input Template

{md_table(templates, ["input_id", "bound_row", "support_id", "multipole_l", "needed_quantity", "required_fields", "current_value", "score_formula", "pass_formula", "acceptance_rule"])}

## Scoring Rows

{md_table(scores, ["score_id", "support_id", "source_body", "test_body_or_readout", "multipole_l", "geometry_factor", "if_theorem_signed", "if_numeric_input", "pass_condition", "current_status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4379: harmonic-null parent signature or first numeric topological moment input

Marker: `{MARKER}`

## What changed

- Split harmonic-null safety into two theorem routes: Laplacian-null and centered static `l=0` zero-monopole symmetry.
- Added a guard: centered `l=0` is exterior Newton safety, not full distributional profile equality.
- Staged first numeric/source input templates for Sun-Earth and Earth-Moon dipole/quadrupole rows.
- Kept all local-GR/Newton/PPN claim gates false until a parent signature or real moment value exists.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4379 Transition harmonic-null signature or numeric moment input

Marker: `{MARKER}`

4379 splits the topological moment-zero target into two exact routes:

```text
delta rho_top = Delta u_top with boundary silence
```

or

```text
delta rho_top=f(|y-y_c|), int delta rho_top dV=0,
same center/frame as rho_H before readout.
```

The second route is new and useful: centered static `l=0` zero-monopole structure kills all exterior Newton multipoles by angular orthogonality. It is not full internal profile equality, so it stays arena-limited. Since neither route is parent-signed, 4379 stages Sun-Earth and Earth-Moon dipole/quadrupole source-input templates.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4379 packet update: harmonic-null splits into Laplacian or l=0 symmetry

Marker: `{PACKET_MARKER}`

Packet update: topological profile safety now has two exact parent-signature targets. A Laplacian-null defect with boundary silence kills all harmonic moments; so does a same-center static `l=0` zero-monopole defect for exterior Newton/orbital scoring. Neither is signed for the raw topological/Hamiltonian profile defect, so the packet carries first numeric moment input templates for Sun-Earth and Earth-Moon dipole/quadrupole rows.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4379 splits the topological harmonic-null target into two exact theorem routes. The Laplacian route remains: delta rho_top=Delta u_top with boundary silence kills every exterior harmonic moment. "
                "A second exact centered l=0 route is added: if delta rho_top is radial in the same source center/frame and has zero monopole, then every l>=1 moment vanishes by angular orthogonality. "
                "This is exterior Newton/orbital safety, not full distributional profile equality. Neither parent signature is signed for the raw topological/Hamiltonian defect, so 4379 stages first numeric/source moment templates for Sun-Earth and Earth-Moon dipole/quadrupole rows. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4379 source register, parent signature audit, centered l0 theorem rows, numeric moment input template, scoring rows, claim gates, decision, status, next target and validation CSV.",
            "harmonic_null_split_laplacian_or_l0_symmetry_numeric_moment_template_nonclaim",
            "Parent-sign the centered l0/harmonic-null source-kernel route or fill one real Sun-Earth/Earth-Moon topological moment input.",
            "Using same total charge, metric-nullity, exact divergence, topological class or post-readout centering as moment-zero evidence.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_SOURCE_REGISTER.csv")
    signatures = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_PARENT_SIGNATURE_AUDIT.csv")
    l0_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_L0_SYMMETRY_THEOREM.csv")
    templates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_NUMERIC_MOMENT_INPUT_TEMPLATE.csv")
    scores = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_SCORING_ROWS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4379_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4379_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4379_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4379_2_signature_audit",
        any(row["signature_id"] == "SIG4379_0_laplacian_null" for row in signatures)
        and any(row["signature_id"] == "SIG4379_1_centered_l0_symmetry" for row in signatures),
        "Laplacian and centered l0 signature routes are both audited",
    )
    add(
        "VAL4379_3_l0_theorem",
        any(row["theorem_id"] == "L0S4379_0_statement" and "EXACT_CONDITIONAL_THEOREM" in row["status"] for row in l0_rows),
        "centered l0 theorem exists",
    )
    add(
        "VAL4379_4_template_missing_values",
        len(templates) >= 4 and all(row["current_value"] == "MISSING_MOMENT_VALUE" for row in templates),
        "numeric moment templates are staged as missing-value nonclaim rows",
    )
    add(
        "VAL4379_5_scoring_positive",
        len(scores) >= 4 and all(float(row["geometry_factor"]) > 0 for row in scores),
        "scoring rows have positive geometry factors",
    )
    add("VAL4379_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4379_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4379_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4379_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4379_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4379_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4379_12_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4379_13_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    signatures = parent_signature_audit_rows()
    l0_rows = l0_symmetry_theorem_rows()
    templates = numeric_moment_input_template_rows()
    scores = scoring_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4379_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4379_PARENT_SIGNATURE_AUDIT.csv": signatures,
        "P8_Y5_R2FR_4379_L0_SYMMETRY_THEOREM.csv": l0_rows,
        "P8_Y5_R2FR_4379_NUMERIC_MOMENT_INPUT_TEMPLATE.csv": templates,
        "P8_Y5_R2FR_4379_SCORING_ROWS.csv": scores,
        "P8_Y5_R2FR_4379_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4379_DECISION.csv": decisions,
        "P8_Y5_R2FR_4379_STATUS.csv": statuses,
        "P8_Y5_R2FR_4379_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, signatures, l0_rows, templates, scores, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
