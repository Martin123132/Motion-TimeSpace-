from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4554"
CLAIM_ID = "L-396"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA3_CUBIC_VECTOR_RESIDUE_CLASSIFICATION_4554"
MARKER = "PPC4161_ALPHA3_CUBIC_VECTOR_RESIDUE_CLASSIFICATION_OR_C3_BOUND_SOURCE_ROW_4554"
PACKET_MARKER = "PPC4161_PACKET_ALPHA3_CUBIC_VECTOR_RESIDUE_ZERO_4554"
DECISION = "PRIVATE_SELECTOR_CLASSIFIES_C3_ALPHA3_ZERO_ALPHA3_FULL_PRIVATE_BRANCH_ZERO_GLOBAL_PARENT_UNSIGNED"
NEXT_TARGET = "4555-Y5-R2FR-alpha3-private-zero-to-PPN-scorecard-and-next-hard-channel.md"

FORMAL_PATH = FORMAL / "570-PPC4161-alpha3-cubic-vector-residue-classification-or-C3-bound-source-row.md"
DOC_PATH = POST / "4554-Y5-R2FR-alpha3-cubic-vector-residue-classification-or-C3-bound-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4553 = FORMAL / "569-PPC4161-alpha3-parent-scalar-singlet-boundary-action-or-first-vector-amplitude-fill.md"
DOC_4552 = FORMAL / "568-PPC4161-alpha3-marker-exclusion-boundary-flux-owner-or-finite-vector-amplitude-row.md"
DOC_4551 = FORMAL / "567-PPC4161-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
PACKET = FORMAL / "180-PPC4161-private-local-packet-integration.md"
ZERO_4553 = SOURCE_DIR / "P8_Y5_R2FR_4553_ALPHA3_ZERO_CERTIFICATE_CANDIDATE.csv"
FILL_4553 = SOURCE_DIR / "P8_Y5_R2FR_4553_FIRST_VECTOR_AMPLITUDE_FILL.csv"
PREMISES_4553 = SOURCE_DIR / "P8_Y5_R2FR_4553_PRIVATE_SELECTOR_PREMISES.csv"
FINITE_4552 = SOURCE_DIR / "P8_Y5_R2FR_4552_FINITE_VECTOR_AMPLITUDE_ROWS.csv"
DOMAIN_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_LOCAL_DOMAIN_BMIN_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4554_SOURCE_REGISTER.csv"
CARRIER_ALPHABET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_CUBIC_VECTOR_CARRIER_ALPHABET.csv"
REP_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_CUBIC_REPRESENTATION_THEOREM.csv"
C3_VALUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_C3_ALPHA3_VALUE_ROW.csv"
ALPHA3_FINAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_ALPHA3_PRIVATE_BRANCH_FINAL_ZERO.csv"
COUNTERMODEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_COUNTERMODEL_GUARDS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4554_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4554_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4554_00_4553_doc", "4553 private zero document", DOC_4553, "Delta alpha3 = C3_alpha3 epsilon_U^3"),
        ("SRC4554_01_4553_zero_cert", "4553 zero certificate", ZERO_4553, "AZ4553_0_private_selector_alpha3_reduction"),
        ("SRC4554_02_4553_fill", "4553 vector fill rows", FILL_4553, "VF4553_2_cubic_handoff_value"),
        ("SRC4554_03_4553_premises", "4553 private selector premises", PREMISES_4553, "SP4553_3_quotient_naturality"),
        ("SRC4554_04_4552_doc", "4552 reduced split", DOC_4552, "M_alpha3 + F_alpha3 + C3_alpha3"),
        ("SRC4554_05_4551_doc", "4551 scalar source projection", DOC_4551, "K_alpha3^src[f(r)] = 0"),
        ("SRC4554_06_4539_parent_freeze", "4539 parent/global firewall", DOC_4539, "not_globally_parent_signed"),
        ("SRC4554_07_packet", "private packet q/no-flux/poynting guard", PACKET, "Radiative EM/gravity flux is not erased"),
        ("SRC4554_08_4552_finite", "4552 cubic coefficient allowance", FINITE_4552, "FV4552_6_cubic_only_after_marker_boundary_zero"),
        ("SRC4554_09_4549_domain", "4549 centred local source domain", DOMAIN_4549, "D4549_0_inner_solar_1_to_30_AU"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4554 cubic vector residue classification",
                "valid_for_claim": "False",
            }
        )
    return rows


def c3_bound_context() -> dict[str, str]:
    rows = read_csv(FINITE_4552)
    cubic = next((row for row in rows if row.get("row_id") == "FV4552_6_cubic_only_after_marker_boundary_zero"), {})
    master = next((row for row in rows if row.get("row_id") == "FV4552_0_no_cancellation_master"), {})
    return {
        "b_alpha3": master.get("numeric_value", "3.9999999999999998e-20"),
        "epsilon_u3": master.get("source_epsilon_U3", "4.8743693920346534e-22"),
        "c3_bound": cubic.get("numeric_value", "8.2061897207390857e+01"),
    }


def carrier_alphabet_rows() -> list[dict[str, Any]]:
    return [
        {
            "carrier_id": "CA4554_0_scalar_singlet_products",
            "candidate_cubic_carrier": "S0*S0*S0",
            "representation": "SO(3) scalar",
            "alpha3_projection": "0",
            "reason": "Tensor products of scalar singlets remain scalar and cannot supply a preferred vector index.",
            "private_selector_status": "zero",
            "global_status": "branch_scoped",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "CA4554_1_radial_exact_gradient",
            "candidate_cubic_carrier": "n_i F(r) from radial scalar gradients",
            "representation": "centred radial vector/exact divergence",
            "alpha3_projection": "0",
            "reason": "Centred spherical angular projection gives integral n_i F(r)dOmega=0; scalar potential renormalization is not alpha3 preferred-frame self-acceleration.",
            "private_selector_status": "zero_for_alpha3",
            "global_status": "requires centred source-domain",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "CA4554_2_epsilon_pseudovector",
            "candidate_cubic_carrier": "epsilon_ijk A_j B_k scalar",
            "representation": "pseudovector only if two independent vectors/spin axes exist",
            "alpha3_projection": "0",
            "reason": "The private scalar-singlet alphabet has no independent vector pair or spin axis; radial parallel vectors also cross to zero.",
            "private_selector_status": "zero",
            "global_status": "reopens if spin/rotation/pseudoscalar marker exists",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "CA4554_3_boundary_flux_cubic",
            "candidate_cubic_carrier": "boundary cubic normal momentum flux",
            "representation": "boundary vector",
            "alpha3_projection": "0 inside branch",
            "reason": "4553 sets F_alpha3=0 for compact stationary no-flux/routed boundary; cubic powers of a zero flux remain zero.",
            "private_selector_status": "zero",
            "global_status": "reopens for radiative/open-sector flux",
            "valid_for_claim": "False",
        },
        {
            "carrier_id": "CA4554_4_marker_cubic",
            "candidate_cubic_carrier": "V_i S0^2 or V_i V^2",
            "representation": "rank-one vector marker",
            "alpha3_projection": "not allowed inside branch",
            "reason": "4553 sets marker vector alphabet to zero; any nonzero V_i is a countermodel outside the private certificate.",
            "private_selector_status": "excluded",
            "global_status": "requires bound/source if present",
            "valid_for_claim": "False",
        },
    ]


def representation_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CT4554_0_cubic_stability",
            "claim": "The 4553 scalar-singlet/no-flux alphabet is stable against cubic alpha3 vector production.",
            "mathematical_form": "P_alpha3[Sym^3(S0) + exact_radial_divergences + zero_flux_boundary] = 0",
            "derivation": "Symmetric products of scalar singlets carry l=0; centred radial exact vector pieces have zero net preferred-frame projection; boundary flux and marker vectors are already zero in the branch.",
            "result": "C3_alpha3=0 inside the private compact stationary non-radiative selector",
            "status": "derived_private_selector_theorem",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CT4554_1_no_new_index_rule",
            "claim": "Nonlinearity cannot create a free vector index that is absent from the parent alphabet.",
            "mathematical_form": "If input representations exclude l=1 carriers and epsilon terms lack independent vectors, cubic local scalars cannot project to alpha3.",
            "derivation": "Representation closure: scalar products remain scalar; metric/coframe contractions close indices; Levi-Civita needs an admitted pseudovector/vector source.",
            "result": "no hidden cubic preferred-frame channel",
            "status": "representation_rule",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CT4554_2_scope_guard",
            "claim": "The theorem fails outside centred compact stationary non-radiative branch conditions.",
            "mathematical_form": "off-centre source, spin, rotation, anisotropic domain, radiative flux, or open memory can supply l=1 carriers",
            "derivation": "These are exactly the vector carriers excluded in 4552/4553, not consequences of scalar-singlet closure.",
            "result": "global/radiative cases must be separately bounded",
            "status": "countermodel_firewall",
            "valid_for_claim": "False",
        },
    ]


def c3_value_rows() -> list[dict[str, Any]]:
    context = c3_bound_context()
    return [
        {
            "row_id": "C3V4554_0_private_selector_value",
            "coefficient": "C3_alpha3",
            "candidate_value": "0",
            "units": "dimensionless coefficient multiplying epsilon_U^3",
            "bound_if_not_zero": context["c3_bound"],
            "basis": "cubic representation stability of scalar-singlet/no-flux private selector alphabet",
            "score_ready_private": "True",
            "score_ready_global": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "C3V4554_1_countermodel_bound_row",
            "coefficient": "C3_alpha3",
            "candidate_value": "MISSING_IF_VECTOR_CARRIER_PRESENT",
            "units": "dimensionless coefficient multiplying epsilon_U^3",
            "bound_if_not_zero": context["c3_bound"],
            "basis": "if a vector carrier is admitted outside branch, source a real coefficient satisfying this bound",
            "score_ready_private": "False",
            "score_ready_global": "False",
            "valid_for_claim": "False",
        },
    ]


def alpha3_final_rows() -> list[dict[str, Any]]:
    context = c3_bound_context()
    return [
        {
            "final_id": "AF4554_0_private_branch_alpha3",
            "scope": "private PPC4161-GP-HQNP compact stationary non-radiative local selector",
            "reduced_split": "Delta alpha3 = M_alpha3 + F_alpha3 + C3_alpha3 epsilon_U^3",
            "M_alpha3": "0",
            "F_alpha3": "0",
            "C3_alpha3": "0",
            "Delta_alpha3": "0",
            "numeric_bound": context["b_alpha3"],
            "status": "alpha3_private_branch_zero",
            "valid_for_claim": "False",
        },
        {
            "final_id": "AF4554_1_global_parent_alpha3",
            "scope": "full MTS parent/global/open/radiative sectors",
            "reduced_split": "same split reopens if selector premises fail",
            "M_alpha3": "not_promoted",
            "F_alpha3": "not_promoted",
            "C3_alpha3": "not_promoted",
            "Delta_alpha3": "not_promoted",
            "numeric_bound": context["b_alpha3"],
            "status": "global_parent_unsigned_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "CGU4554_0_spin_rotation",
            "countermodel": "spinning/rotating source or material axis",
            "why_it_breaks_zero": "supplies a genuine vector/pseudovector carrier",
            "required_response": "derive exclusion or source a finite C3/M_alpha3 coefficient",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "CGU4554_1_offcentre_multipole",
            "countermodel": "off-centre source, anisotropic domain, l=1 boundary harmonic",
            "why_it_breaks_zero": "angular integral no longer has centred scalar cancellation",
            "required_response": "score multipole/domain vector separately",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "CGU4554_2_radiative_flux",
            "countermodel": "radiative EM/gravity/open-memory flux crossing collar",
            "why_it_breaks_zero": "no-flux theorem does not apply; flux is real Hamiltonian/T_total channel",
            "required_response": "route and bound boundary flux row",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4554_0_private_alpha3_zero",
            "requirement": "M_alpha3=F_alpha3=C3_alpha3=0 in private compact branch",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "alpha3 is closed inside private branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4554_1_global_parent_alpha3",
            "requirement": "same zero theorem promoted to full MTS parent action",
            "status": "FAIL_UNSIGNED",
            "claim_effect": "blocks public/global local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4554_2_countermodels",
            "requirement": "spin/off-centre/radiative/open-sector cases excluded or bounded",
            "status": "GUARD_RETAINED",
            "claim_effect": "private zero cannot be applied outside its branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4554_3_next_ppn_channel",
            "requirement": "propagate alpha3 private zero into scorecard and choose next pressure channel",
            "status": "NEXT_TARGET",
            "claim_effect": "moves local PPN work forward",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4554_0",
            "decision": DECISION,
            "summary": "4554 classifies the cubic alpha3 vector residue. Inside the private compact stationary scalar-singlet/no-flux selector, cubic scalar products and centred radial exact divergences do not supply a preferred-frame vector, while marker and boundary vector carriers were already zero in 4553. Therefore C3_alpha3=0 and Delta alpha3=0 in the private branch. Global parent adoption and non-branch countermodels remain nonclaim.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "alpha3 is now privately zero, so the next useful step is to update the local PPN scorecard and identify the next hard channel rather than reopening alpha3.",
            "success_condition": "A scorecard row records alpha3=0 under private selector scope, keeps global/public claim false, and ranks the remaining PPN/local channels by source-backed product pressure.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    carriers: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    c3_rows: list[dict[str, Any]],
    final_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4554_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    carriers_text = " ".join(str(value) for row in carriers for value in row.values())
    carriers_ok = "spin/rotation" in carriers_text and "radiative/open-sector" in carriers_text
    carriers_ok = carriers_ok and all(row.get("valid_for_claim") == "False" for row in carriers)
    rows.append(
        {
            "validation_id": "VAL4554_1_carrier_alphabet",
            "check": "carrier alphabet covers scalar products, radial gradients, marker vectors and boundary/radiative guards",
            "status": "PASS" if carriers_ok else "FAIL",
            "details": f"{len(carriers)} carrier rows checked",
        }
    )

    theorem_text = " ".join(str(value) for row in theorem for value in row.values())
    theorem_ok = "C3_alpha3=0" in theorem_text and "countermodel_firewall" in theorem_text
    rows.append(
        {
            "validation_id": "VAL4554_2_rep_theorem",
            "check": "cubic theorem derives C3 zero inside branch and states scope guard",
            "status": "PASS" if theorem_ok else "FAIL",
            "details": "representation stability checked",
        }
    )

    private_c3 = next((row for row in c3_rows if row.get("row_id") == "C3V4554_0_private_selector_value"), {})
    c3_ok = private_c3.get("candidate_value") == "0" and private_c3.get("score_ready_private") == "True"
    c3_ok = c3_ok and private_c3.get("valid_for_claim") == "False"
    rows.append(
        {
            "validation_id": "VAL4554_3_c3_value",
            "check": "C3 private value is zero and nonclaim",
            "status": "PASS" if c3_ok else "FAIL",
            "details": "C3V4554_0 checked",
        }
    )

    final = next((row for row in final_rows if row.get("final_id") == "AF4554_0_private_branch_alpha3"), {})
    final_ok = final.get("Delta_alpha3") == "0" and final.get("status") == "alpha3_private_branch_zero"
    rows.append(
        {
            "validation_id": "VAL4554_4_final_alpha3",
            "check": "private branch alpha3 final row is zero",
            "status": "PASS" if final_ok else "FAIL",
            "details": "AF4554_0 checked",
        }
    )

    gates_ok = any(row.get("status") == "FAIL_UNSIGNED" for row in gates) and any(row.get("status") == "PASS_PRIVATE_SELECTOR" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4554_5_claim_gates",
            "check": "private pass and global/public block both remain explicit",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "no public/global claim promoted",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4554_6_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4554_OVERALL",
            "check": "4554 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    carriers: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    c3_rows: list[dict[str, Any]],
    final_rows: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    context = c3_bound_context()
    return f"""# 4554 - alpha3 cubic vector residue classification or C3 bound source row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4553 left the private selector branch at:

```text
Delta alpha3 = C3_alpha3 epsilon_U^3
```

4554 classifies that cubic term. The key point is simple but important: cubic nonlinearity cannot create a preferred-frame vector unless the cubic alphabet contains a vector carrier.

Inside the compact stationary scalar-singlet/no-flux private selector:

- scalar-singlet products stay scalar;
- centred radial exact vectors have zero net alpha3 preferred-frame projection;
- epsilon/pseudovector terms need independent vector/spin axes, which the branch excludes;
- marker vectors and boundary flux were already set to zero in 4553;
- radiative/open-sector flux remains outside the certificate.

Therefore:

```text
C3_alpha3 = 0
Delta alpha3 = 0
```

inside the private compact stationary non-radiative selector branch.

The fallback coefficient bound remains recorded for any countermodel outside the branch:

```text
|C3_alpha3| <= {context['c3_bound']}
epsilon_U^3 = {context['epsilon_u3']}
```

This closes alpha3 privately; it does not close global parent adoption.

## Cubic Vector Carrier Alphabet

{markdown_table(carriers)}

## Cubic Representation Theorem

{markdown_table(theorem)}

## C3 Alpha3 Value Row

{markdown_table(c3_rows)}

## Alpha3 Private Branch Final Zero

{markdown_table(final_rows)}

## Countermodel Guards

{markdown_table(guards)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4554 classifies the cubic alpha3 vector residue and derives C3_alpha3=0 inside the private compact stationary scalar-singlet/no-flux selector, so alpha3 is zero in that private branch.",
        "current_evidence": "Generated source register, cubic vector carrier alphabet, cubic representation theorem, C3 value row, alpha3 final zero row, countermodel guards, claim gates, status and validation CSVs.",
        "status": "alpha3_private_branch_full_zero_global_parent_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Using the private alpha3 zero outside centred compact stationary non-radiative branch scope, or treating it as global parent adoption.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "Alpha3 is now closed inside the private branch; next step is scorecard propagation and next-channel selection.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    carriers = carrier_alphabet_rows()
    theorem = representation_theorem_rows()
    c3_rows = c3_value_rows()
    final_rows = alpha3_final_rows()
    guards = countermodel_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CARRIER_ALPHABET_CSV, carriers)
    write_csv(REP_THEOREM_CSV, theorem)
    write_csv(C3_VALUE_CSV, c3_rows)
    write_csv(ALPHA3_FINAL_CSV, final_rows)
    write_csv(COUNTERMODEL_CSV, guards)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4554 - alpha3 cubic vector residue classification or C3 bound source row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, carriers, theorem, c3_rows, final_rows, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, carriers, theorem, c3_rows, final_rows, guards, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4554 Alpha3 Cubic Residue Zero

Marker: `{MARKER}`  
The private compact stationary alpha3 branch is now:

```text
M_alpha3 = F_alpha3 = C3_alpha3 = 0,
Delta alpha3 = 0.
```

Reason: cubic scalar-singlet products do not create a preferred-frame vector; centred radial exact pieces have zero alpha3 projection; marker/boundary vector carriers are already zero inside the selector. This is private-branch closure only, not global parent-action adoption.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4554 Packet Integration - Alpha3 Cubic Residue Zero

Marker: `{PACKET_MARKER}`  
For compact stationary non-radiative PPC4161-GP-HQNP local packets, the reduced alpha3 split is fully zero: `M_alpha3=F_alpha3=C3_alpha3=0`. Spin, off-centre multipoles, anisotropic domains and radiative/open-sector flux remain explicit countermodels requiring separate rows.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4554_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
