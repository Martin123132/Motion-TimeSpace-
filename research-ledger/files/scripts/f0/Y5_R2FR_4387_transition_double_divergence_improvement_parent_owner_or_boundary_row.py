from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from double_divergence_boundary_gate import evaluate_boundary_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4387"
CLAIM_ID = "L-228"
MARKER = "PPC4161_TRANSITION_DOUBLE_DIVERGENCE_IMPROVEMENT_PARENT_OWNER_OR_BOUNDARY_ROW_4387"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_DOUBLE_DIVERGENCE_IMPROVEMENT_PARENT_OWNER_OR_BOUNDARY_ROW_4387"
DECISION = "COVARIANT_IMPROVEMENT_OWNER_SHAPE_DERIVED_BIRTH_CERTIFICATE_FAILS_BOUNDARY_GATE_BUILT_NONCLAIM"
NEXT_TARGET = "4388-Y5-R2FR-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md"

FORMAL_PATH = FORMAL / "403-PPC4161-transition-double-divergence-improvement-parent-owner-or-boundary-row.md"
DOC_PATH = POST / "4387-Y5-R2FR-transition-double-divergence-improvement-parent-owner-or-boundary-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4387_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
BOUNDARY_RUNNER_PATH = SCRIPT_DIR / "double_divergence_boundary_gate.py"
BOUNDARY_SMOKE_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4387_BOUNDARY_GATE_SMOKE_INPUT.csv"
BOUNDARY_SMOKE_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4387_BOUNDARY_GATE_SMOKE_OUTPUT.csv"
BOUNDARY_SMOKE_ACCEPTANCE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4387_BOUNDARY_GATE_SMOKE_ACCEPTANCE.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4387_00_4386_formal": (
        FORMAL / "402-PPC4161-transition-affine-annihilator-parent-signature-or-real-profile-row.md",
        "rho_top-rho_H = partial_i partial_j S^{ij}",
        "4386 handoff: double-divergence mechanism.",
    ),
    "SRC4387_01_4386_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4386_NEXT_TARGET.csv",
        "4387-Y5-R2FR-transition-double-divergence-improvement-parent-owner-or-boundary-row.md",
        "Explicit 4387 target.",
    ),
    "SRC4387_02_4386_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4386_DOUBLE_DIVERGENCE_THEOREMS.csv",
        "DD4386_4_parent_owner_contract",
        "Parent owner contract to sharpen.",
    ),
    "SRC4387_03_4386_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4386_PARENT_SIGNATURE_AUDIT.csv",
        "PSA4386_0_source_object",
        "Missing parent density identity.",
    ),
    "SRC4387_04_185_hsrc": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "+ int dB_impr",
        "Private Hilbert source packet includes improvement slot.",
    ),
    "SRC4387_05_226_visible": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "+ dB_impr.",
        "Visible matter import allows calibrated improvement term.",
    ),
    "SRC4387_06_2220_birth_certificate": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "Prior trace-free improvement birth certificate failed.",
    ),
    "SRC4387_07_299_superpotential_guard": (
        FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md",
        "The generic boundary/topological route fails as a derivation",
        "Guard against generic superpotential promotion.",
    ),
    "SRC4387_08_192_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "Support-separated no-flux theorem gives a boundary-silence template.",
    ),
    "SRC4387_09_191_em": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Visible EM/Poynting guard.",
    ),
    "SRC4387_10_runner": (
        BOUNDARY_RUNNER_PATH,
        "def evaluate_boundary_rows",
        "Boundary gate runner added for source-backed rows.",
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


def owner_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "IO4387_0_covariant_improvement_shape",
            "statement": "A parent Hilbert/Noether improvement with local superpotential U^{mu alpha nu beta} has leading weak-local form Delta T^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}+curvature_commutator_terms.",
            "derivation": "The double derivative is the covariant stress-improvement species compatible with symmetric source stress. Curvature commutators are higher local-curvature residuals unless separately cancelled by the parent action.",
            "effect": "Identifies the covariant birth-certificate shape behind the 4386 S^{ij} mechanism.",
            "status": "EXACT_CONDITIONAL_SHAPE_CURVATURE_RESIDUAL_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "IO4387_1_newtonian_density_projection",
            "statement": "In the local weak-static Newtonian source limit, Delta rho = c^{-2} Delta T^{00}=partial_i partial_j S^{ij}+curvature/boundary residuals with S^{ij}=c^{-2}U^{0i0j}.",
            "derivation": "Spatial derivatives dominate the compact source density projection, and the affine test functions have zero second spatial derivatives.",
            "effect": "Connects a covariant improvement owner directly to rho_top-rho_H=partial_i partial_j S^{ij}.",
            "status": "LOCAL_WEAK_LIMIT_DENSITY_MAP_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "IO4387_2_affine_closure_if_birth_certified",
            "statement": "If rho_top-rho_H is exactly the Newtonian density projection of that parent improvement and affine boundary pairings vanish, then Delta_M=0 and B_top=0.",
            "derivation": "Combine IO4387_1 with DD4386_0.",
            "effect": "This would close the separated-center branch without full profile equality.",
            "status": "EXACT_COMPOSED_THEOREM_PARENT_CERTIFICATE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "IO4387_3_dB_impr_not_enough",
            "statement": "The presence of dB_impr in the source action is not sufficient by itself to identify rho_top-rho_H with a double-divergence density.",
            "derivation": "185/226 include improvement slots, but do not name U^{0i0j}, tie it to the topological/Hilbert residual, or prove boundary pairings.",
            "effect": "Prevents promoting existing improvement notation into a local-GR claim.",
            "status": "COUNTERCLAIM_RETAINED_EXISTING_SLOT_NOT_OWNER",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "IO4387_4_tracefree_improvement_warning",
            "statement": "The older Khat/trace-free improvement route has the right mathematical species but its birth certificate failed in the current corpus.",
            "derivation": "2220 records trace-free improvement conditional math but BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS.",
            "effect": "Reuse the shape, not the claim.",
            "status": "PRIOR_ROUTE_SUPPORTS_SHAPE_NOT_ADOPTION",
            "valid_for_claim": "False",
        },
    ]


def birth_certificate_rows() -> List[Dict[str, str]]:
    return [
        {
            "certificate_id": "BCERT4387_0_residual_identity",
            "clause": "rho_top-rho_H equals c^{-2}nabla_alpha nabla_beta U^{0 alpha 0 beta} plus explicitly bounded curvature residuals",
            "evidence_now": "4386 derives the target shape; no current source states this identity for rho_top-rho_H.",
            "status": "MISSING",
            "blocker": "MISSING_PARENT_RESIDUAL_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_1_parent_owner",
            "clause": "U^{mu alpha nu beta} or S^{ij} is a parent-owned field/function of the local source packet before readout",
            "evidence_now": "185/226 include dB_impr slots; 4384/4386 keep topological profile owner unsigned.",
            "status": "MISSING",
            "blocker": "MISSING_PARENT_U_OWNER",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_2_no_fit_recenter",
            "clause": "U/S is fixed before exterior/orbital/profile scoring and cannot be chosen to kill B_top after the fact",
            "evidence_now": "readout firewall exists, but no U/S owner has been adopted.",
            "status": "MISSING",
            "blocker": "MISSING_PRE_READOUT_LOCK_FOR_IMPROVEMENT",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_3_boundary_silence",
            "clause": "constant and linear affine boundary pairings vanish or are source-backed below tolerance",
            "evidence_now": "192 gives support-separated no-flux template; 299 rejects generic boundary/topological route through the shell.",
            "status": "MISSING",
            "blocker": "MISSING_AFFINE_BOUNDARY_PAIRING_ROWS",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_4_curvature_remainder",
            "clause": "curvature commutator terms are absent in the local branch or carried as explicit residuals",
            "evidence_now": "current 4387 theorem retains curvature residual rather than deleting it.",
            "status": "OPEN_RESIDUAL",
            "blocker": "MISSING_CURVATURE_REMAINDER_BOUND_OR_ZERO",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_5_visible_EM_guard",
            "clause": "visible EM/Poynting is not double-counted as topological residual",
            "evidence_now": "191 Hilbert-owns Maxwell/Poynting stress inside compact selector.",
            "status": "SUPPORTED_GUARD",
            "blocker": "does_not_supply_topological_improvement_owner",
            "valid_for_claim": "False",
        },
        {
            "certificate_id": "BCERT4387_6_verdict",
            "clause": "all owner, boundary, readout, and curvature clauses pass",
            "evidence_now": "mathematical owner shape derived; actual parent birth certificate missing.",
            "status": "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
            "blocker": "do_not_claim; source hunt or boundary row fill next",
            "valid_for_claim": "False",
        },
    ]


def boundary_template_rows() -> List[Dict[str, str]]:
    return [
        {
            "field": "constant_pairing",
            "definition": "int_boundary n_i partial_j S^{ij} dS",
            "zero_effect": "kills Delta_M_top_H",
            "claim_rule": "numeric, source-backed, abs(value)<=tolerance",
            "valid_for_claim": "False",
        },
        {
            "field": "linear_x/y/z_pairing",
            "definition": "int_boundary y^k n_i partial_j S^{ij} dS - int_boundary n_j S^{kj} dS",
            "zero_effect": "kills B_top^k",
            "claim_rule": "numeric, source-backed, abs(value)<=tolerance for k=x,y,z",
            "valid_for_claim": "False",
        },
        {
            "field": "source_path",
            "definition": "path to derivation/profile/boundary computation",
            "zero_effect": "provenance gate",
            "claim_rule": "must exist and contain no synthetic/smoke/placeholder markers",
            "valid_for_claim": "False",
        },
    ]


def boundary_smoke_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "row_id": "BSM4387_0_zero_pairings",
            "object_id": "SYNTHETIC_DOUBLE_DIVERGENCE_BOUNDARY_ZERO",
            "constant_pairing": "0.0",
            "linear_x_pairing": "0.0",
            "linear_y_pairing": "0.0",
            "linear_z_pairing": "0.0",
            "units": "synthetic_affine_boundary_units",
            "source_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
            "input_valid_for_claim": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "BSM4387_1_nonzero_linear",
            "object_id": "SYNTHETIC_DOUBLE_DIVERGENCE_BOUNDARY_LEAK",
            "constant_pairing": "0.0",
            "linear_x_pairing": "1.0e-4",
            "linear_y_pairing": "0.0",
            "linear_z_pairing": "0.0",
            "units": "synthetic_affine_boundary_units",
            "source_path": "SYNTHETIC_SMOKE_NOT_PHYSICAL",
            "input_valid_for_claim": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def boundary_acceptance_rows(output_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    by_id = {row["row_id"]: row for row in output_rows}
    zero = by_id["BSM4387_0_zero_pairings"]
    leak = by_id["BSM4387_1_nonzero_linear"]
    return [
        {
            "accept_id": "BGA4387_0_zero_detected",
            "tested_output": "BSM4387_0_zero_pairings",
            "value": zero["max_abs_pairing"],
            "threshold": "1e-12",
            "passed": str(zero["boundary_silent"] == "True" and zero["valid_for_claim"] == "False"),
            "interpretation": "zero pairings score boundary-silent but remain nonclaim because synthetic source",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "BGA4387_1_leak_detected",
            "tested_output": "BSM4387_1_nonzero_linear",
            "value": leak["max_abs_pairing"],
            "threshold": "> 1e-12",
            "passed": str(leak["boundary_silent"] == "False" and float(leak["max_abs_pairing"]) > 1.0e-12),
            "interpretation": "nonzero linear boundary pairing fails the affine boundary gate",
            "valid_for_claim": "False",
        },
        {
            "accept_id": "BGA4387_2_all_nonclaim",
            "tested_output": "all smoke rows",
            "value": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "threshold": "True",
            "passed": str(all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in output_rows)),
            "interpretation": "synthetic boundary smoke cannot become evidence",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4387_0_owner_shape",
            "claim_tested": "covariant improvement shape implies double-divergence density",
            "required_inputs": "U owner and weak-static density projection tied to rho_top-rho_H",
            "status": "SHAPE_DERIVED_OWNER_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4387_1_birth_certificate",
            "claim_tested": "S^{ij}/U is parent birth-certified",
            "required_inputs": "BCERT4387_0 through BCERT4387_4 pass",
            "status": "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4387_2_boundary_rows",
            "claim_tested": "affine boundary pairings vanish",
            "required_inputs": "source-backed boundary gate rows with abs(pairings)<=tolerance",
            "status": "RUNNER_READY_SOURCE_ROWS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4387_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "owner, boundary, curvature, higher profile/rest/readout gates all closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4387_0",
            "decision": DECISION,
            "summary": (
                "4387 derives the covariant owner shape behind the 4386 double-divergence mechanism. A Hilbert/Noether stress improvement has leading local form Delta T^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}; in the weak-static Newtonian source limit this gives Delta rho=c^{-2}partial_i partial_j U^{0i0j}. "
                "That would birth the S^{ij} required by 4386 if and only if the parent action identifies rho_top-rho_H with that improvement before readout and the affine boundary pairings vanish. Existing dB_impr notation and the old Khat improvement route support the mathematical species but do not birth-certify the actual topological residual. "
                "So 4387 builds a boundary-pairing gate for source-backed rows and keeps the route nonclaim."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next real move is either source-hunt the U/S birth certificate or fill source-backed boundary-pairing rows; generic improvement language is no longer enough.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4387_0_owner_shape",
            "object": "covariant improvement U",
            "status": "SHAPE_DERIVED",
            "note": "weak-static density projection gives the 4386 S^{ij} route.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4387_1_birth_certificate",
            "object": "rho_top-rho_H owner identity",
            "status": "MISSING",
            "note": "dB_impr exists as a slot but not as the owner of the topological/Hilbert residual.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4387_2_boundary_runner",
            "object": "double_divergence_boundary_gate.py",
            "status": "BUILT_AND_SMOKE_TESTED",
            "note": "future boundary rows can now pass/fail affine boundary silence with provenance gates.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4387_3_next",
            "object": "next target",
            "status": "BIRTH_CERTIFICATE_OR_BOUNDARY_ROW_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4387_0",
            "target": NEXT_TARGET,
            "question": "Can a source file birth-certify U/S as the actual rho_top-rho_H owner, or can source-backed boundary pairings be filled?",
            "preferred_route": "search/derive a parent action clause where the topological/Hilbert residual is exactly the Newtonian density projection of an improvement superpotential.",
            "fallback_route": "fill real boundary-pairing rows for constant and linear affine tests, or import a real profile through the affine runner.",
            "avoid": "claiming from dB_impr notation alone, old Khat improvement shape alone, generic superpotential words, synthetic boundary smoke, or total charge.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    certificates: List[Dict[str, str]],
    template: List[Dict[str, str]],
    boundary_output: List[Dict[str, str]],
    boundary_acceptance: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: double-divergence improvement parent owner or boundary row

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4387 derives the covariant owner shape behind the `4386` double-divergence mechanism:

```text
Delta T^{{mu nu}} = nabla_alpha nabla_beta U^{{mu alpha nu beta}} + curvature_commutator_residuals.
```

In the local weak-static Newtonian source limit:

```text
rho_top-rho_H = c^-2 Delta T^{{00}}
              = partial_i partial_j S^{{ij}} + curvature/boundary residuals,
S^{{ij}} := c^-2 U^{{0i0j}}.
```

So the route is now genuinely field-theoretic: an improvement stress can birth the `S^{{ij}}` required by `4386`.

But this is not claimed. Existing `dB_impr` language provides an improvement slot, not an owner identity for `rho_top-rho_H`; older Khat-improvement work has the right mathematical species but failed its birth certificate. The parent action still has to identify the actual topological/Hilbert residual with this improvement and provide boundary silence.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Improvement Owner Theorems

{md_table(theorems, ["theorem_id", "statement", "derivation", "effect", "status"])}

## Birth-Certificate Clauses

{md_table(certificates, ["certificate_id", "clause", "evidence_now", "status", "blocker"])}

## Boundary Row Template

{md_table(template, ["field", "definition", "zero_effect", "claim_rule"])}

## Boundary Gate Smoke Output

{md_table(boundary_output, ["row_id", "object_id", "max_abs_pairing", "boundary_silent", "source_exists", "valid_for_claim", "current_status"])}

## Boundary Gate Smoke Acceptance

{md_table(boundary_acceptance, ["accept_id", "tested_output", "value", "threshold", "passed", "interpretation"])}

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
    text = f"""# 4387: double-divergence improvement parent owner or boundary row

Marker: `{MARKER}`

## What changed

- Derived the covariant improvement owner shape `Delta T = nabla nabla U`.
- Mapped its weak-static density projection to the `S^{{ij}}` double divergence from 4386.
- Audited the birth-certificate clauses and kept them unsigned.
- Added `double_divergence_boundary_gate.py` for future source-backed affine boundary rows.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4387 Transition double-divergence improvement parent owner or boundary row

Marker: `{MARKER}`

4387 identifies the covariant owner shape behind the 4386 affine-annihilator mechanism:

```text
Delta T^{{mu nu}} = nabla_alpha nabla_beta U^{{mu alpha nu beta}},
rho_top-rho_H = c^-2 Delta T^{{00}} -> partial_i partial_j S^{{ij}}
```

in the local weak-static source limit, with curvature and boundary residuals retained unless separately closed. This is the right field-theory species for `S^{{ij}}`, but existing `dB_impr` notation and older Khat improvement work do not birth-certify the actual topological/Hilbert residual. A boundary gate runner now exists for source-backed affine boundary rows.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4387 packet update: improvement owner birth-certificate

Marker: `{PACKET_MARKER}`

Packet update: `S^{{ij}}` can be field-theoretically born as the Newtonian density projection of a covariant improvement superpotential `U^{{mu alpha nu beta}}`. This remains nonclaim until the parent action identifies `rho_top-rho_H` with that improvement before readout and source-backed affine boundary pairings vanish.
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
                "4387 derives the covariant improvement owner shape behind the 4386 double-divergence affine mechanism. A Hilbert/Noether improvement has leading local form Delta T^{mu nu}=nabla_alpha nabla_beta U^{mu alpha nu beta}; in the weak-static Newtonian source limit this projects to rho_top-rho_H=c^{-2}Delta T^{00}=partial_i partial_j S^{ij} with S^{ij}=c^{-2}U^{0i0j}, up to retained curvature/boundary residuals. "
                "This supplies the correct field-theory species for the needed S^{ij}, but does not claim it: existing dB_impr and older Khat improvement rows do not birth-certify the actual topological/Hilbert residual. A boundary-pairing gate runner is added for source-backed affine boundary rows. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4387 source register, improvement owner theorem rows, birth-certificate clauses, boundary template, boundary smoke input/output/acceptance, claim gates, decision, status, next target and validation CSV.",
            "covariant_improvement_owner_shape_derived_birth_certificate_missing_boundary_gate_nonclaim",
            "Birth-certify U/S as the actual rho_top-rho_H owner or fill source-backed affine boundary/profile rows.",
            "Claiming from dB_impr notation alone, old Khat improvement shape alone, generic superpotential words, synthetic boundary smoke, or total charge.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4387_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4387_IMPROVEMENT_OWNER_THEOREMS.csv")
    certificates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4387_BIRTH_CERTIFICATE.csv")
    boundary_output = read_csv(BOUNDARY_SMOKE_OUTPUT_PATH)
    boundary_acceptance = read_csv(BOUNDARY_SMOKE_ACCEPTANCE_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4387_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4387_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4387_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add(
        "VAL4387_2_owner_shape",
        any(row["theorem_id"] == "IO4387_0_covariant_improvement_shape" for row in theorems)
        and any(row["theorem_id"] == "IO4387_1_newtonian_density_projection" for row in theorems),
        "covariant owner and density projection rows recorded",
    )
    add(
        "VAL4387_3_dB_not_promoted",
        any(row["theorem_id"] == "IO4387_3_dB_impr_not_enough" for row in theorems),
        "dB_impr slot not promoted to owner proof",
    )
    add(
        "VAL4387_4_birth_certificate_fails",
        any(row["certificate_id"] == "BCERT4387_6_verdict" and row["status"] == "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS" for row in certificates),
        "birth certificate failure recorded",
    )
    add(
        "VAL4387_5_boundary_smoke",
        any(row["row_id"] == "BSM4387_0_zero_pairings" and row["boundary_silent"] == "True" for row in boundary_output)
        and any(row["row_id"] == "BSM4387_1_nonzero_linear" and row["boundary_silent"] == "False" for row in boundary_output),
        "boundary gate distinguishes zero and nonzero pairings",
    )
    add("VAL4387_6_acceptance_passed", all(row["passed"] == "True" for row in boundary_acceptance), "all boundary smoke acceptance checks passed")
    add("VAL4387_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4387_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4387_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4387_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4387_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4387_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4387_13_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4387_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4387_15_runner_exists", BOUNDARY_RUNNER_PATH.exists() and "def evaluate_boundary_rows" in read_text(BOUNDARY_RUNNER_PATH), "boundary gate runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = owner_theorem_rows()
    certificates = birth_certificate_rows()
    template = boundary_template_rows()
    smoke_input = boundary_smoke_input_rows()
    write_csv(BOUNDARY_SMOKE_INPUT_PATH, smoke_input)
    boundary_output = evaluate_boundary_rows(BOUNDARY_SMOKE_INPUT_PATH, 1.0e-12)
    write_csv(BOUNDARY_SMOKE_OUTPUT_PATH, boundary_output)
    boundary_acceptance = boundary_acceptance_rows(boundary_output)
    write_csv(BOUNDARY_SMOKE_ACCEPTANCE_PATH, boundary_acceptance)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4387_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4387_IMPROVEMENT_OWNER_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4387_BIRTH_CERTIFICATE.csv": certificates,
        "P8_Y5_R2FR_4387_BOUNDARY_ROW_TEMPLATE.csv": template,
        "P8_Y5_R2FR_4387_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4387_DECISION.csv": decisions,
        "P8_Y5_R2FR_4387_STATUS.csv": statuses,
        "P8_Y5_R2FR_4387_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [BOUNDARY_SMOKE_INPUT_PATH, BOUNDARY_SMOKE_OUTPUT_PATH, BOUNDARY_SMOKE_ACCEPTANCE_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, certificates, template, boundary_output, boundary_acceptance, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
