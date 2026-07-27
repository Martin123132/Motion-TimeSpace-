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

from curvature_improvement_adoption_gate import evaluate_adoption_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4389"
CLAIM_ID = "L-230"
MARKER = "PPC4161_TRANSITION_CURVATURE_IMPROVEMENT_ACTION_ADOPTION_OR_REAL_BOUNDARY_PAIRING_ROW_4389"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_CURVATURE_IMPROVEMENT_ACTION_ADOPTION_OR_REAL_BOUNDARY_PAIRING_ROW_4389"
DECISION = "CURVATURE_ACTION_ADOPTION_PAYLOAD_DERIVED_PURE_00_CLOSURE_REJECTED_ADOPTION_GATE_BUILT_NONCLAIM"
NEXT_TARGET = "4390-Y5-R2FR-transition-U-action-owner-construction-or-pressure-curvature-bound-row.md"

FORMAL_PATH = FORMAL / "405-PPC4161-transition-curvature-improvement-action-adoption-or-real-boundary-pairing-row.md"
DOC_PATH = POST / "4389-Y5-R2FR-transition-curvature-improvement-action-adoption-or-real-boundary-pairing-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4389_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
ADOPTION_RUNNER_PATH = SCRIPT_DIR / "curvature_improvement_adoption_gate.py"
ADOPTION_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_GATE_INPUT.csv"
ADOPTION_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_GATE_OUTPUT.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4389_00_4388_formal": (
        FORMAL / "404-PPC4161-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md",
        "ACT4388_0_curvature_coupled_improvement",
        "4388 handoff: curvature-coupled action template.",
    ),
    "SRC4389_01_4388_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4388_NEXT_TARGET.csv",
        "4389-Y5-R2FR-transition-curvature-improvement-action-adoption-or-real-boundary-pairing-row.md",
        "Explicit 4389 target.",
    ),
    "SRC4389_02_4388_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv",
        "ACT4388_0_curvature_coupled_improvement",
        "Action template rows.",
    ),
    "SRC4389_03_4388_hunt": (
        SOURCE_DIR / "P8_Y5_R2FR_4388_SOURCE_HUNT_OUTPUT.csv",
        "CAND4388_00_4387_formal",
        "Source hunt found blocked candidates.",
    ),
    "SRC4389_04_gate": (
        ADOPTION_RUNNER_PATH,
        "def evaluate_adoption_rows",
        "Adoption gate runner added in 4389.",
    ),
    "SRC4389_05_191_em": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Visible EM/Poynting non-double-counting guard.",
    ),
    "SRC4389_06_2220": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
        "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
        "Prior trace-free improvement adoption failure.",
    ),
    "SRC4389_07_192": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "Support-separated no-flux boundary template.",
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


def adoption_theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "AD4389_0_variation_payload",
            "statement": "Adopting S_U=1/2 int sqrt(-g) U^{mu alpha nu beta}R_{mu alpha nu beta} produces a full Hilbert tensor payload, not only a 00 density correction.",
            "derivation": "Variation gives double-divergence improvement terms plus algebraic curvature, metric-dependence, and boundary terms. These feed 00, 0i, and ij components unless projected/bounded by parent clauses.",
            "effect": "Pure B_top closure cannot be claimed without pressure/aniso/curvature gates.",
            "status": "EXACT_ACTION_PAYLOAD_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AD4389_1_no_pure_00_closure",
            "statement": "A parent action cannot honestly be adopted as a source-density-only fix while discarding its stress, momentum, boundary, and curvature components.",
            "derivation": "Hilbert variation is tensorial and diffeomorphism-covariant; selecting only Delta T^{00} after variation would be a post-readout closure assumption.",
            "effect": "Rejects smuggling local-GR closure through a useful 00 component alone.",
            "status": "NO_GO_FOR_PURE_00_ADOPTION",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AD4389_2_bianchi_ward_payload",
            "statement": "If S_U is diffeomorphism invariant and U/Phi equations are included, its Hilbert contribution is conserved on shell; otherwise a residual exchange/current row is required.",
            "derivation": "Noether identity ties the divergence of the metric variation to the Euler-Lagrange equations for U/Phi. Off-shell or externally fixed U creates a conservation payload.",
            "effect": "Adds a conservation gate before local-GR promotion.",
            "status": "CONSERVATION_GATE_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AD4389_3_curvature_remainder_gate",
            "statement": "The local weak-static double-divergence limit is safe only after algebraic curvature and commutator terms are zero in the branch or explicitly bounded.",
            "derivation": "Covariant derivatives and metric variation commute only up to curvature; S_U also contains curvature contractions not captured by the flat partial_i partial_j S^{ij} term.",
            "effect": "Creates a curvature-bound row rather than deleting these terms.",
            "status": "CURVATURE_PAYLOAD_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "AD4389_4_trace_scalar_warning",
            "statement": "The scalar phi R subcase is useful but not free: it produces (g_{mu nu}Box-nabla_mu nabla_nu)phi plus phi G_{mu nu}, including pressure/aniso payload.",
            "derivation": "This is the known nonminimal scalar improvement form and matches earlier Khat-improvement warnings.",
            "effect": "PhiR can be a next construction route only with pressure, boundary, zero-mode, and curvature gates.",
            "status": "SCALAR_SUBCASE_RETAINED_AS_CONSTRUCTION_ROUTE_NOT_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def component_payload_rows() -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "PAY4389_0_density",
            "component": "Delta T^{00}/c^2",
            "needed_for": "rho_top-rho_H and B_top affine closure",
            "danger": "useful but insufficient alone",
            "required_gate": "residual identity plus boundary pairings",
            "status": "FORMULA_READY_OWNER_MISSING",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "PAY4389_1_momentum",
            "component": "Delta T^{0i}",
            "needed_for": "PPN preferred-frame/momentum source safety",
            "danger": "hidden momentum flux or alpha_i leakage",
            "required_gate": "stationary/local no-flux or explicit bound",
            "status": "BOUND_OR_ZERO_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "PAY4389_2_pressure_aniso",
            "component": "Delta T^{ij}",
            "needed_for": "PPN gamma/beta/stress source safety",
            "danger": "anisotropic stress changes metric potentials even if B_top=0",
            "required_gate": "pressure/aniso projection zero or bounded",
            "status": "BOUND_OR_ZERO_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "PAY4389_3_curvature",
            "component": "algebraic curvature and commutator terms",
            "needed_for": "local weak-flat reduction",
            "danger": "nonzero curvature residue masquerades as extra source",
            "required_gate": "curvature remainder zero theorem or bound row",
            "status": "BOUND_OR_ZERO_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "PAY4389_4_boundary",
            "component": "boundary terms from variation and integrations by parts",
            "needed_for": "affine annihilator and no hidden shell flux",
            "danger": "boundary flux survives even when bulk is a double divergence",
            "required_gate": "source-backed boundary pairings or support-separated no-flux",
            "status": "BOUNDARY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "PAY4389_5_conservation",
            "component": "nabla_mu Delta T^{mu nu}",
            "needed_for": "Bianchi/source consistency",
            "danger": "fixed U without field equation creates exchange current",
            "required_gate": "diffeomorphism Ward/on-shell U equation or explicit exchange current",
            "status": "WARD_OWNER_MISSING",
            "valid_for_claim": "False",
        },
    ]


def adoption_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "ADOPT4389_0_current_SU_template",
            "residual_identity_signed": "False",
            "parent_u_owner_signed": "False",
            "riemann_symmetry_signed": "False",
            "metric_variation_owned": "False",
            "pre_readout_lock_signed": "False",
            "affine_boundary_pairings_pass": "False",
            "curvature_remainder_zero_or_bounded": "False",
            "pressure_anisotropy_zero_or_bounded": "False",
            "conservation_ward_owned": "False",
            "visible_em_not_double_counted": "True",
            "source_path": str(FORMAL / "404-PPC4161-transition-improvement-birth-certificate-source-hunt-or-boundary-row-fill.md"),
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def route_rows(adoption_gate: List[Dict[str, str]]) -> List[Dict[str, str]]:
    adoption_pass = any(row["adoption_pass"] == "True" for row in adoption_gate)
    return [
        {
            "route_id": "ROUTE4389_0_adopt_SU",
            "route": "Parent-adopt S_U as the actual rho_top-rho-H residual owner",
            "evidence": "adoption gate pass exists" if adoption_pass else "adoption gate fails; only EM non-double-counting is currently closed",
            "status": "PASS" if adoption_pass else "BLOCKED_ADOPTION_PAYLOAD_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4389_1_construct_phiR_subcase",
            "route": "Try scalar phi R trace subcase as a narrower construction",
            "evidence": "known species, but 2220 birth certificate failed and pressure/zero-mode payload remains",
            "status": "CONSTRUCTION_ROUTE_OPEN_NOT_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4389_2_real_boundary_or_profile",
            "route": "Fill source-backed boundary/profile rows instead of adopting action",
            "evidence": "boundary/profile templates exist; values missing",
            "status": "VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4389_0_pure_00",
            "claim_tested": "S_U can be used only as a 00 density fix",
            "required_inputs": "not allowed; action variation is tensorial",
            "status": "REJECTED_NO_PURE_00_CLOSURE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4389_1_action_adoption",
            "claim_tested": "S_U is adopted as parent action owner",
            "required_inputs": "all adoption gate clauses pass",
            "status": "ADOPTION_GATE_BLOCKED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4389_2_payload_bounds",
            "claim_tested": "pressure/aniso/curvature/boundary/conservation payloads are safe",
            "required_inputs": "PAY4389 rows zeroed or source bounded",
            "status": "PAYLOAD_ROWS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4389_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "adoption or real rows plus all local payload and profile gates",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4389_0",
            "decision": DECISION,
            "summary": (
                "4389 tests the curvature-improvement action as a real adoption candidate. The key result is a no-pure-00 theorem: S_U cannot honestly be used only to fix rho_top-rho_H/B_top while ignoring the rest of its Hilbert tensor. "
                "Adopting S_U brings momentum, pressure/anisotropy, curvature, boundary, and conservation payloads. The adoption gate therefore requires residual identity, parent U owner, Riemann symmetries, owned metric variation, pre-readout lock, affine boundary pass, curvature bound, pressure/aniso bound, Ward conservation, and visible EM non-double-counting. "
                "The current template closes only the EM guard; all other adoption clauses remain open. Therefore S_U remains a promising construction route, not a claim."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "The next useful work is to construct U/action ownership directly or bound the pressure/curvature payload; broad source-hunting has already failed.",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4389_0_action",
            "object": "S_U curvature improvement",
            "status": "PROMISING_CONSTRUCTION_NOT_ADOPTED",
            "note": "right species for double-divergence, but full tensor payload must be owned.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4389_1_no_pure_00",
            "object": "density-only closure",
            "status": "REJECTED",
            "note": "Hilbert variation cannot be truncated to the useful 00 component after the fact.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4389_2_gate",
            "object": "curvature_improvement_adoption_gate.py",
            "status": "BUILT_AND_FAILS_CLOSED",
            "note": "current S_U template fails adoption because owner/boundary/curvature/pressure/Ward clauses are open.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4389_3_next",
            "object": "next target",
            "status": "U_OWNER_OR_PAYLOAD_BOUND_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4389_0",
            "target": NEXT_TARGET,
            "question": "Can U/action ownership be constructed without hidden pressure/curvature payload, or must those payloads become bound rows?",
            "preferred_route": "construct a parent U/Phi sector with Riemann symmetries, residual identity, Ward conservation, and controlled pressure/curvature projections.",
            "fallback_route": "fill source-backed bounds for pressure/aniso, curvature remainder, boundary pairings, or import real profiles.",
            "avoid": "using S_U as a density-only fix, treating phiR/Khat shapes as adoption, or ignoring Bianchi/stress payload.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    payloads: List[Dict[str, str]],
    adoption_output: List[Dict[str, str]],
    routes: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: curvature improvement action adoption or real boundary pairing row

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4389 tests the `4388` action template as an actual adoption candidate:

```text
S_U = 1/2 int sqrt(-g) U^{{mu alpha nu beta}} R_{{mu alpha nu beta}}.
```

The useful density piece is still:

```text
Delta rho_U = c^-2 Delta T_U^{{00}} ~ partial_i partial_j S^{{ij}}.
```

But the action cannot be adopted as a density-only trick. Its Hilbert variation is a tensor payload:

```text
Delta T_U^{{mu nu}}
= double-divergence improvement
 + pressure/aniso/momentum components
 + curvature/metric-dependence residuals
 + boundary terms.
```

Therefore 4389 rejects pure `00` closure. To use `S_U`, MTS must own the full action and its payload: residual identity, parent `U`, Riemann symmetries, pre-readout lock, affine boundary pairings, curvature residual, pressure/aniso residual, Ward conservation, and visible EM non-double-counting.

No claim fires. The current template closes only visible EM non-double-counting; every other adoption clause remains open.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Adoption Theorems

{md_table(theorems, ["theorem_id", "statement", "derivation", "effect", "status"])}

## Component Payload Rows

{md_table(payloads, ["payload_id", "component", "needed_for", "danger", "required_gate", "status"])}

## Adoption Gate Output

{md_table(adoption_output, ["candidate_id", "source_exists", "closed_clause_count", "total_clause_count", "failed_clauses", "adoption_pass", "current_status"])}

## Route Rows

{md_table(routes, ["route_id", "route", "evidence", "status", "claim_allowed"])}

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
    text = f"""# 4389: curvature improvement action adoption or real boundary pairing row

Marker: `{MARKER}`

## What changed

- Derived the full adoption payload for `S_U`.
- Rejected density-only / pure `00` closure.
- Added `curvature_improvement_adoption_gate.py`.
- Kept `S_U` as a construction route, not a local-GR claim.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4389 Transition curvature improvement action adoption or real boundary pairing row

Marker: `{MARKER}`

4389 rejects using the curvature-coupled improvement action as a pure density/`00` trick. If adopted, `S_U=1/2 int sqrt(-g) U Riemann` brings a full Hilbert tensor payload: density, momentum, pressure/aniso, curvature, boundary, and conservation terms. The double-divergence density mechanism remains promising, but local-GR promotion now requires full action ownership or explicit payload bounds.

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4389 packet update: no pure 00 action adoption

Marker: `{PACKET_MARKER}`

Packet update: `S_U` is retained as a serious construction route, but not as a density-only closure. Adoption requires residual identity, parent `U`, Riemann symmetries, owned metric variation, pre-readout lock, affine boundary pass, curvature bound, pressure/aniso bound, Ward conservation, and EM non-double-counting. Current template closes only the EM guard.
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
                "4389 tests the curvature-coupled improvement action S_U=1/2 int sqrt(-g) U^{mu alpha nu beta}R_{mu alpha nu beta} as an adoption candidate. It derives the key no-pure-00 result: S_U cannot honestly be used only to fix the useful density component rho_top-rho_H/B_top while discarding the rest of its Hilbert tensor. "
                "Adoption brings momentum, pressure/anisotropy, curvature, boundary, and conservation payloads. A new adoption gate requires residual identity, parent U ownership, Riemann symmetries, owned metric variation, pre-readout lock, affine boundary pass, curvature bound, pressure/aniso bound, Ward conservation, and visible EM non-double-counting. "
                "The current template closes only the EM guard, so S_U remains a construction route, not a local-GR/Newton/PPN/clock/orbital claim."
            ),
            "4389 source register, adoption theorem rows, component payload rows, adoption gate input/output, route rows, claim gates, decision, status, next target and validation CSV.",
            "curvature_action_payload_derived_pure00_rejected_adoption_gate_nonclaim",
            "Construct parent U/action ownership or fill pressure/aniso, curvature, boundary, conservation, or profile bound rows.",
            "Using S_U as a density-only fix, treating phiR/Khat shapes as adoption, or ignoring Bianchi/stress payload.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4389_SOURCE_REGISTER.csv")
    theorems = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_THEOREMS.csv")
    payloads = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4389_COMPONENT_PAYLOADS.csv")
    adoption = read_csv(ADOPTION_OUTPUT_PATH)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4389_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4389_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4389_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add(
        "VAL4389_2_no_pure_00",
        any(row["theorem_id"] == "AD4389_1_no_pure_00_closure" and row["status"] == "NO_GO_FOR_PURE_00_ADOPTION" for row in theorems),
        "pure 00 closure rejected",
    )
    add(
        "VAL4389_3_payload_rows",
        len(payloads) >= 6 and all(row["valid_for_claim"] == "False" for row in payloads),
        "component payload rows staged nonclaim",
    )
    add(
        "VAL4389_4_adoption_fails_closed",
        all(row["adoption_pass"] == "False" and row["valid_for_claim"] == "False" for row in adoption),
        "current adoption candidates fail closed",
    )
    add("VAL4389_5_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4389_6_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4389_7_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4389_8_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4389_9_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4389_10_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4389_11_rows_nonclaim",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4389_12_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4389_13_runner_exists", ADOPTION_RUNNER_PATH.exists() and "def evaluate_adoption_rows" in read_text(ADOPTION_RUNNER_PATH), "adoption runner exists")
    return validations


def main() -> None:
    sources = source_register_rows()
    theorems = adoption_theorem_rows()
    payloads = component_payload_rows()
    adoption_input = adoption_input_rows()
    write_csv(ADOPTION_INPUT_PATH, adoption_input)
    adoption_output = evaluate_adoption_rows(ADOPTION_INPUT_PATH)
    write_csv(ADOPTION_OUTPUT_PATH, adoption_output)
    routes = route_rows(adoption_output)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4389_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4389_ADOPTION_THEOREMS.csv": theorems,
        "P8_Y5_R2FR_4389_COMPONENT_PAYLOADS.csv": payloads,
        "P8_Y5_R2FR_4389_ROUTE_ROWS.csv": routes,
        "P8_Y5_R2FR_4389_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4389_DECISION.csv": decisions,
        "P8_Y5_R2FR_4389_STATUS.csv": statuses,
        "P8_Y5_R2FR_4389_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [ADOPTION_INPUT_PATH, ADOPTION_OUTPUT_PATH]
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorems, payloads, adoption_output, routes, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
