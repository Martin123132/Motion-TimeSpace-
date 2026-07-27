from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ricci_survivor_ward_nohair_gate import evaluate_coverage_rows, evaluate_identity_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4411"
CLAIM_ID = "L-252"
MARKER = "PPC4161_TRANSITION_PARENT_WARD_NOHAIR_FOR_RICCI_SURVIVOR_VECTOR_OR_FIRST_REAL_RUU_ROW_4411"
PACKET_MARKER = "PPC4161_PACKET_PARENT_WARD_NOHAIR_FOR_RICCI_SURVIVOR_VECTOR_OR_FIRST_REAL_RUU_ROW_4411"
DECISION = "WARD_ONLY_GIVES_DIVERGENCE_POSITIVE_NOHAIR_CONTRACT_REQUIRED_FIRST_RUU_ROW_READY_NONCLAIM"
NEXT_TARGET = "4412-Y5-R2FR-transition-positive-operator-sector-map-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"

FORMAL_PATH = FORMAL / "427-PPC4161-transition-parent-Ward-nohair-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
DOC_PATH = POST / "4411-Y5-R2FR-transition-parent-Ward-nohair-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4411_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

IDENTITY_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4411_WARD_NOHAIR_IDENTITY_INPUT.csv"
IDENTITY_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4411_WARD_NOHAIR_IDENTITY_OUTPUT.csv"
COVERAGE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4411_SURVIVOR_COVERAGE_INPUT.csv"
COVERAGE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4411_SURVIVOR_COVERAGE_OUTPUT.csv"
FIRST_RUU_TEMPLATE = SOURCE_DIR / "P8_Y5_R2FR_4411_FIRST_REAL_RUU_ROW_TEMPLATE.csv"

WARD_GATE_PATH = SCRIPT_DIR / "ricci_survivor_ward_nohair_gate.py"
SURVIVOR_GATE_PATH = SCRIPT_DIR / "ricci_survivor_vector_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4411_transition_parent_Ward_nohair_for_Ricci_survivor_vector_or_first_real_Ruu_row.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_426 = FORMAL / "426-PPC4161-transition-local-Ricci-survivor-vector-zero-or-first-real-Ruu-source-row.md"
NEXT_4410 = SOURCE_DIR / "P8_Y5_R2FR_4410_NEXT_TARGET.csv"
POST_1365 = POST / "1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair-or-q_loc-bound-source-row.md"
FORMAL_419 = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
FORMAL_420 = FORMAL / "420-PPC4161-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
FORMAL_421 = FORMAL / "421-PPC4161-transition-cGamma-Pleak-first-two-components-or-profile-bound.md"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
FORMAL_423 = FORMAL / "423-PPC4161-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
FORMAL_424 = FORMAL / "424-PPC4161-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"
FORMAL_425 = FORMAL / "425-PPC4161-transition-lambda-curvature-payload-cancellation-or-first-real-density-profile-row.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4411_00_4410_formal": (
        FORMAL_426,
        "Exact No-Cancellation Law",
        "4410 survivor-vector law to be zeroed or sourced.",
    ),
    "SRC4411_01_4410_next": (
        NEXT_4410,
        "parent Ward/no-hair identity",
        "4410 target selects parent Ward/no-hair or first real R_uu row.",
    ),
    "SRC4411_02_1365_ward": (
        POST_1365,
        "Conditional qloc-zero theorem",
        "Prior Ward/no-hair theorem ladder for q_loc.",
    ),
    "SRC4411_03_420_nohair": (
        FORMAL_420,
        "memory no-hair",
        "c_Gamma memory no-hair energy identity.",
    ),
    "SRC4411_04_421_Pleak": (
        FORMAL_421,
        "P_nonHilbert_action_domain q_tr = 0",
        "P_leak first-two clean/private branch.",
    ),
    "SRC4411_05_422_source": (
        FORMAL_422,
        "D_A ln kappa_eff = 0",
        "source-charge/coupling bridge.",
    ),
    "SRC4411_06_423_profile": (
        FORMAL_423,
        "rho_eff(y) = rho_H(y) on W_H",
        "density/profile shadow owner theorem.",
    ),
    "SRC4411_07_424_sigma": (
        FORMAL_424,
        "S_owner = int_W",
        "sigma/electric-U owner route.",
    ),
    "SRC4411_08_425_ricci": (
        FORMAL_425,
        "Ricci-normal payload R_uu",
        "4409 Ricci-normal rebase.",
    ),
    "SRC4411_09_ward_gate": (
        WARD_GATE_PATH,
        "def evaluate_identity_rows",
        "new Ward/no-hair gate.",
    ),
    "SRC4411_10_survivor_gate": (
        SURVIVOR_GATE_PATH,
        "def evaluate_aggregate_rows",
        "4410 survivor-vector aggregate gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for line_number, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, line_number
    return False, -1


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip() + "\n")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    current = text(path)
    if f"\n{claim_id}," in current:
        return
    if current and not current.endswith("\n"):
        current += "\n"
    write_text(path, current + csv_line(row))


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line_number = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "WNH4411_0_Ward_not_enough",
            "statement": "A parent Ward identity can make the survivor tensor owned/conserved, but conservation alone does not set R_uu to zero.",
            "derivation": "Diffeomorphism invariance gives nabla_mu E_surv^{mu nu}=sum_A E_A nabla^nu Phi^A plus source and boundary terms. On shell and with no flux this gives divergence silence. It still permits transverse-traceless, trace, Lambda, or homogeneous stress branches unless a positive no-hair identity kills the fields themselves.",
            "new_information": "This prevents the common cheat: Bianchi safety is necessary but not sufficient for local GR.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WNH4411_1_positive_nohair_lemma",
            "statement": "A clean zero theorem is available in conditional form if the survivor vector descends from positive auxiliary fields with no local source and no boundary flux.",
            "derivation": "For survivor variables Z^A with Euler equations L_AB Z^B=J_A and L positive self-adjoint, multiply by Z^A and integrate. If J_A=0, boundary flux vanishes, and zero modes are fixed or gapped, then int(|DZ|^2+M^2|Z|^2)=0. Hence Z=0 and the metric response of the survivor sector vanishes.",
            "new_information": "The route to local GR is not magic: it is a concrete positive-operator/no-source theorem.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WNH4411_2_vector_coverage_condition",
            "statement": "The no-hair lemma helps only if it covers every 4410 live slot: c_Gamma/P_leak, c_R2/M_R, spin/torsion, epsilon_Gsrc/E_profile, Lambda_eff and projector/boundary hair.",
            "derivation": "If any component is outside the parent positive sector, the aggregate bound remains |R_uu| <= sum_j(|S_j,uu|+1/2|S_j,tr|)+... and that component must be sourced as a finite row.",
            "new_information": "4411 converts 'derive it' into an exact component-coverage test.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WNH4411_3_current_verdict",
            "statement": "Current evidence supports the conditional theorem structure but not a current MTS claim.",
            "derivation": "The corpus has Ward and no-hair fragments, but the live parent action has not yet signed metric-response/Helmholtz closure, all component slots, source silence, boundary silence, and Lambda/projector silence at once.",
            "new_information": "Next work should attempt the positive-operator sector map, not another generic missing-source sweep.",
            "valid_for_claim": False,
        },
    ]


def identity_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "identity_id": "WNH4411_0_current_Ward_only",
            "route": "current_corpus_Ward_Bianchi_fragments",
            "diffeo_parent_action": True,
            "observed_coframe_owned": False,
            "Hilbert_source_only": False,
            "Bianchi_Ward_identity_written": True,
            "metric_response_helmholtz_closed": False,
            "Euler_on_shell_closed": False,
            "positive_self_adjoint_operator": False,
            "mass_gap_or_fixed_zero_mode": False,
            "source_current_zero": False,
            "boundary_no_flux": False,
            "projector_domain_silent": False,
            "Lambda_eff_zero_or_bound": False,
            "component_vector_covered": False,
            "no_cross_cancellation": True,
            "source_path": str(POST_1365),
            "input_valid_for_claim": False,
            "notes": "Ward/Bianchi structure exists, but it gives divergence ownership only, not full zero.",
        },
        {
            "identity_id": "WNH4411_1_conditional_positive_nohair_schema",
            "route": "future_parent_positive_operator_nohair",
            "diffeo_parent_action": True,
            "observed_coframe_owned": True,
            "Hilbert_source_only": True,
            "Bianchi_Ward_identity_written": True,
            "metric_response_helmholtz_closed": True,
            "Euler_on_shell_closed": True,
            "positive_self_adjoint_operator": True,
            "mass_gap_or_fixed_zero_mode": True,
            "source_current_zero": True,
            "boundary_no_flux": True,
            "projector_domain_silent": True,
            "Lambda_eff_zero_or_bound": True,
            "component_vector_covered": True,
            "no_cross_cancellation": True,
            "source_path": str(FORMAL_426),
            "input_valid_for_claim": False,
            "notes": "Control row for the theorem we are trying to earn; intentionally nonclaim.",
        },
        {
            "identity_id": "WNH4411_2_bad_conservation_shortcut",
            "route": "Bianchi_conservation_only_shortcut",
            "diffeo_parent_action": True,
            "observed_coframe_owned": True,
            "Hilbert_source_only": True,
            "Bianchi_Ward_identity_written": True,
            "metric_response_helmholtz_closed": False,
            "Euler_on_shell_closed": False,
            "positive_self_adjoint_operator": False,
            "mass_gap_or_fixed_zero_mode": False,
            "source_current_zero": True,
            "boundary_no_flux": True,
            "projector_domain_silent": False,
            "Lambda_eff_zero_or_bound": False,
            "component_vector_covered": False,
            "no_cross_cancellation": True,
            "source_path": str(POST_1365),
            "input_valid_for_claim": False,
            "notes": "Explicit refusal row: conserved residual stress is not zero residual stress.",
        },
    ]


def coverage_input_rows() -> List[Dict[str, object]]:
    current = [
        ("WCV4411_0_current_cGamma", "c_Gamma/P_leak", FORMAL_420),
        ("WCV4411_1_current_cR2", "c_R2/M_R", FORMAL_419 if FORMAL_419.exists() else FORMAL_426),
        ("WCV4411_2_current_spin_torsion", "spin/torsion", FORMAL_426),
        ("WCV4411_3_current_source_profile", "epsilon_Gsrc/E_profile", FORMAL_422),
    ]
    rows: List[Dict[str, object]] = []
    for coverage_id, component, source in current:
        rows.append(
            {
                "coverage_id": coverage_id,
                "component": component,
                "required_by_vector": True,
                "represented_in_parent_identity": False,
                "positive_operator_slot": False,
                "no_independent_source_slot": False,
                "same_support": False,
                "boundary_projection_silent": False,
                "lambda_projector_silent": False,
                "identity_id": "WNH4411_0_current_Ward_only",
                "source_path": str(source),
                "input_valid_for_claim": False,
                "notes": "Current live component is not yet covered by a parent positive no-hair identity.",
            }
        )
    for component in ["c_Gamma/P_leak", "c_R2/M_R", "spin/torsion", "epsilon_Gsrc/E_profile"]:
        rows.append(
            {
                "coverage_id": f"WCV4411_schema_{component.replace('/', '_').replace(' ', '_')}",
                "component": component,
                "required_by_vector": True,
                "represented_in_parent_identity": True,
                "positive_operator_slot": True,
                "no_independent_source_slot": True,
                "same_support": True,
                "boundary_projection_silent": True,
                "lambda_projector_silent": True,
                "identity_id": "WNH4411_1_conditional_positive_nohair_schema",
                "source_path": str(FORMAL_426),
                "input_valid_for_claim": False,
                "notes": "Conditional schema row only; no current parent signature.",
            }
        )
    return rows


def first_ruu_template_rows() -> List[Dict[str, object]]:
    components = ["c_Gamma/P_leak", "c_R2/M_R", "spin/torsion", "epsilon_Gsrc/E_profile", "Lambda_eff", "projector_boundary"]
    return [
        {
            "row_id": f"RUU4411_{index}_{component.replace('/', '_')}",
            "component": component,
            "required_quantity_uu": f"|{component}|_uu on same worldtube",
            "required_quantity_trace": f"|{component}|_trace on same worldtube",
            "units": "curvature_or_residual_stress_units_to_match_R_uu",
            "support_requirements": "same_tau;same_coframe;same_worldtube;before_readout;no_cross_cancellation",
            "source_path": "MISSING_REAL_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "status": "MISSING_REAL_COMPONENT_ROW",
            "valid_for_claim": False,
        }
        for index, component in enumerate(components)
    ]


def source_register_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4411_SOURCE_REGISTER.csv"


def derivation_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4411_DERIVATIONS.csv"


def claim_gate_rows(identity_rows: List[Dict[str, str]], coverage_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    current_identity = next(row for row in identity_rows if row["identity_id"] == "WNH4411_0_current_Ward_only")
    return [
        {
            "gate_id": "CG4411_0_Ward_only",
            "claim": "Ward/Bianchi identity zeros local Ricci survivor vector",
            "claim_allowed": False,
            "reason": f"current status is {current_identity['current_status']}; Ward conservation alone does not imply zero.",
        },
        {
            "gate_id": "CG4411_1_positive_nohair",
            "claim": "positive no-hair theorem zeros all live components",
            "claim_allowed": False,
            "reason": "the theorem schema is coherent but intentionally nonclaim until parent action, source silence and coverage are signed.",
        },
        {
            "gate_id": "CG4411_2_component_coverage",
            "claim": "all 4410 components are covered by parent identity",
            "claim_allowed": False,
            "reason": "current live coverage rows are not represented in the parent identity.",
        },
        {
            "gate_id": "CG4411_3_first_Ruu_row",
            "claim": "finite R_uu row ready for empirical scoring",
            "claim_allowed": False,
            "reason": "first real component rows remain missing; only the source template is created.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4411_0",
            "decision": DECISION,
            "summary": "4411 proves the important negative/positive split: Ward/Bianchi ownership alone gives divergence silence, not R_uu=0. A clean local-GR route needs a parent positive no-hair identity covering every 4410 survivor component on the same support. The conditional theorem is mathematically coherent, but current MTS has not signed metric-response/Helmholtz closure, full component coverage, source silence, boundary silence, Lambda/projector silence, or support lock. The fallback first-real-R_uu row schema is now explicit.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "claim_id": CLAIM_ID,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4411_0",
            "target": NEXT_TARGET,
            "question": "Can the 4410 survivor components be represented as a positive self-adjoint parent operator sector with no source/no flux, or must the first real R_uu row be filled?",
            "preferred_route": "construct the sector map Z^A -> {c_Gamma/Pleak, c_R2/M_R, spin/torsion, epsilon_Gsrc/E_profile} with positive Hessian/operator, metric response, no independent source, and same-support boundary silence.",
            "fallback_route": "fill the first real R_uu component row from the 4411 template with source paths, units, support certificates, uu/trace bounds and no-cancellation rules.",
            "avoid": "using Bianchi/Ward conservation as zero, treating private selector zeros as public proof, or letting a component sit outside the no-hair vector.",
            "valid_for_claim": False,
        }
    ]


def compact_rows(rows: List[Dict[str, str]], fields: List[str]) -> List[Dict[str, str]]:
    return [{field: row.get(field, "") for field in fields} for row in rows]


def render_document(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    identities: List[Dict[str, str]],
    coverage: List[Dict[str, str]],
    first_ruu: List[Dict[str, object]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 427 PPC4161 transition: parent Ward no-hair for Ricci survivor vector or first real Ruu row

Marker: `{MARKER}`

Generated: `{STAMP}`

Decision: `{DECISION}`

## Result

4411 makes the key distinction sharp:

- Ward/Bianchi identity can own/conserve the residual.
- Positive no-hair is what would actually kill the residual.

So the route to local GR is now:

`Ward ownership + metric response + positive operator + no source/no flux + full survivor coverage => R_uu_survivor = 0`.

Without that, the theory owes a real same-support `R_uu` component row.

## Source Audit

{markdown_table(sources)}

## Derivations

{markdown_table(derivations)}

## Ward/No-Hair Identity Gate

{markdown_table(compact_rows(identities, ["identity_id", "current_status", "ward_identity_ready", "metric_response_ready", "nohair_energy_ready", "theorem_output", "valid_for_claim"]))}

## Survivor Coverage Gate

{markdown_table(compact_rows(coverage, ["coverage_id", "component", "identity_id", "current_status", "component_covered", "coverage_ready", "valid_for_claim"]))}

## First Real Ruu Row Template

{markdown_table(first_ruu)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_target_rows())}
"""


def append_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4411 local spine update: Ward is ownership, no-hair is zero

Marker: `{MARKER}`

4411 separates two ideas that must not be conflated. A parent Ward/Bianchi identity can make the local survivor residual owned and divergence-safe, but it does not force `R_uu=0`. The clean branch now requires a positive no-hair identity covering every survivor slot from 4410 on the same support. If that cannot be parent-signed, the fallback is a first real `R_uu` component row with `uu` and trace bounds.
""",
    )


def append_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4411 packet update: Ward/no-hair split

Marker: `{PACKET_MARKER}`

The local-GR branch has advanced from vague residual closure to a theorem contract: Ward ownership plus a positive no-hair energy identity can kill the Ricci survivor vector, but Ward alone cannot. The next target is the positive-operator sector map, or the first real `R_uu` row.
""",
    )


def append_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4411 proves the Ward/no-hair split for the local Ricci survivor route. Ward/Bianchi ownership gives divergence silence but not R_uu=0. A clean local-GR branch requires parent metric-response/Helmholtz closure plus a positive no-hair identity covering c_Gamma/Pleak, c_R2/M_R, spin/torsion, epsilon_Gsrc/E_profile, Lambda_eff and projector/boundary terms on the same support. The fallback first-real-R_uu row template is explicit. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4411 source register, derivation rows, Ward/no-hair identity gate, survivor coverage gate, first-real-R_uu row template, claim gates, decision, status, next target and validation CSV.",
            "Ward_nohair_contract_ready_nonclaim_Ward_only_not_zero",
            "Construct the positive-operator sector map or fill the first real same-support R_uu component row.",
            "Using Bianchi/Ward conservation as zero, private selector zeros as public proof, or uncovered components outside the no-hair vector.",
        ],
    )


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, object]]:
    sources = read_csv(paths["source_register"])
    identities = read_csv(IDENTITY_OUTPUT)
    coverage = read_csv(COVERAGE_OUTPUT)
    first_ruu = read_csv(FIRST_RUU_TEMPLATE)
    current_identity = next(row for row in identities if row["identity_id"] == "WNH4411_0_current_Ward_only")
    schema_identity = next(row for row in identities if row["identity_id"] == "WNH4411_1_conditional_positive_nohair_schema")
    all_outputs = identities + coverage
    checks = [
        ("VAL4411_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4411_1_source_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle was found"),
        ("VAL4411_2_current_Ward_not_zero", current_identity["current_status"] == "WARD_NOHAIR_ZERO_BLOCKED" or current_identity["current_status"] == "WARD_IDENTITY_DIVERGENCE_ONLY_NOT_ZERO", "current route does not promote Ward to zero"),
        ("VAL4411_3_schema_zero_nonclaim", schema_identity["current_status"] == "WARD_NOHAIR_ZERO_SCHEMA_READY_NONCLAIM", "conditional no-hair theorem schema is wired but nonclaim"),
        ("VAL4411_4_current_components_not_covered", all(row["current_status"] == "COMPONENT_REQUIRED_BUT_NOT_IN_IDENTITY" for row in coverage if row["coverage_id"].startswith("WCV4411_") and "_current_" in row["coverage_id"]), "current live components are not covered by parent identity"),
        ("VAL4411_5_schema_components_nonclaim", all(row["current_status"] == "COMPONENT_COVERAGE_SCHEMA_READY_NONCLAIM" for row in coverage if row["coverage_id"].startswith("WCV4411_schema_")), "schema coverage rows are nonclaim"),
        ("VAL4411_6_first_Ruu_template_complete", len(first_ruu) == 6 and all(row["status"] == "MISSING_REAL_COMPONENT_ROW" for row in first_ruu), "first real R_uu row template covers all required slots"),
        ("VAL4411_7_no_output_claims", not any(bool_text(row.get("claim_allowed", "False")) or bool_text(row.get("valid_for_claim", "False")) for row in all_outputs), "no generated gate output is claim-valid"),
        ("VAL4411_8_claim_row_exists", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claims register contains L-252"),
        ("VAL4411_9_spine_marker_exists", MARKER in text(SPINE_PATH), "spine update marker exists"),
        ("VAL4411_10_packet_marker_exists", PACKET_MARKER in text(PACKET_PATH), "packet update marker exists"),
        ("VAL4411_11_formal_doc_exists", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4411_12_post_doc_exists", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post-checkpoint doc exists with marker"),
        ("VAL4411_13_next_target_exists", paths["next_target"].exists() and NEXT_TARGET in text(paths["next_target"]), "next target file exists"),
        ("VAL4411_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    paths = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4411_SOURCE_REGISTER.csv",
        "derivations": SOURCE_DIR / "P8_Y5_R2FR_4411_DERIVATIONS.csv",
        "claim_gates": SOURCE_DIR / "P8_Y5_R2FR_4411_CLAIM_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4411_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4411_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4411_NEXT_TARGET.csv",
    }
    source_register = source_rows()
    derivations = derivation_rows()
    first_ruu = first_ruu_template_rows()
    write_csv(paths["source_register"], source_register)  # type: ignore[arg-type]
    write_csv(paths["derivations"], derivations)  # type: ignore[arg-type]
    write_csv(IDENTITY_INPUT, identity_input_rows())  # type: ignore[arg-type]
    identities = evaluate_identity_rows(IDENTITY_INPUT)
    write_csv(IDENTITY_OUTPUT, identities)
    write_csv(COVERAGE_INPUT, coverage_input_rows())  # type: ignore[arg-type]
    coverage = evaluate_coverage_rows(COVERAGE_INPUT, IDENTITY_OUTPUT)
    write_csv(COVERAGE_OUTPUT, coverage)
    write_csv(FIRST_RUU_TEMPLATE, first_ruu)  # type: ignore[arg-type]

    claim_gates = claim_gate_rows(identities, coverage)
    write_csv(paths["claim_gates"], claim_gates)  # type: ignore[arg-type]
    write_csv(paths["decision"], decision_rows())  # type: ignore[arg-type]
    write_csv(paths["status"], status_rows())  # type: ignore[arg-type]
    write_csv(paths["next_target"], next_target_rows())  # type: ignore[arg-type]

    doc = render_document(source_register, derivations, identities, coverage, first_ruu, claim_gates)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_spine()
    append_packet()
    append_claim()

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(VALIDATION_PATH, validation_rows(paths))  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
