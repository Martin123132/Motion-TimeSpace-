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

CHECKPOINT = "4529"
CLAIM_ID = "L-371"
MARKER = "PPC4161_POSITIVE_SGK_PARENT_SIGNATURE_MAP_OR_EPSILONI_KVERT_VALUE_SOURCE_4529"
PACKET_MARKER = "PPC4161_PACKET_POSITIVE_SGK_PARENT_SIGNATURE_MAP_OR_EPSILONI_KVERT_VALUE_SOURCE_4529"
DECISION = "SGK_GIVES_A_REAL_LOCAL_ZERO_THEOREM_IF_PARENT_SIGNED_BUT_CURRENT_MTS_NEEDS_SOURCE_CURRENT_OR_KVERT_VALUES"
NEXT_TARGET = "4530-Y5-R2FR-SGK-source-current-zero-or-first-Kvert-eigenvalue-bound.md"

FORMAL_PATH = FORMAL / "545-PPC4161-positive-SGK-parent-signature-map-or-epsilonI-Kvert-value-source.md"
DOC_PATH = POST / "4529-Y5-R2FR-positive-SGK-parent-signature-map-or-epsilonI-Kvert-value-source.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4529_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_SGK_DESCENT_THEOREM.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_SGK_PARENT_SIGNATURE_MAP.csv"
VALUE_SOURCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_EPSILONI_KVERT_VALUE_SOURCE_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4529_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4529_VALIDATION.csv"

DOC_4529 = DOC_PATH
DOC_4528 = POST / "4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md"
VALIDATION_4528 = SOURCE_DIR / "P8_Y5_BRR545_4528_VALIDATION.csv"
BOUND_4528 = SOURCE_DIR / "P8_Y5_R2FR_4528_EPSILONI_FIRST_BOUND_ROW.csv"
KVERT_4528 = SOURCE_DIR / "P8_Y5_R2FR_4528_KVERT_CLASSIFIER_INPUT_ROWS.csv"
DOC_1619 = POST / "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md"
NORMAL_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv"
GAPS_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv"
SILENCE_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_LOCAL_SILENCE_THEOREM.csv"
DOC_1621 = POST / "1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md"
GATE_1621 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv"
ACTION_4527 = SOURCE_DIR / "P8_Y5_R2FR_4527_ACTION_ODD_FORCE_THEOREM.csv"
PRINCIPAL_4527 = SOURCE_DIR / "P8_Y5_R2FR_4527_AUXILIARY_Z_PRINCIPAL_SYMBOL_TEST.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()[:360]
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, "")).replace("\n", "<br>")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4529_00_doc4528", "4528 source sweep verdict", DOC_4528, "NO_PARENT_SIGNED_AA0_KVERT0_FIRST_BOUND_ROWS_STAGED", "sets the immediate target"),
        ("SRC4529_01_val4528", "4528 validation", VALIDATION_4528, "VAL4528_OVERALL", "confirms prior step is clean"),
        ("SRC4529_02_bound4528", "4528 epsilon/Kvert bound schema", BOUND_4528, "EPS4528_3_finite_range_from_Kvert", "finite branch formula to refine"),
        ("SRC4529_03_kvert4528", "4528 Kvert classifier", KVERT_4528, "KVI4528_1_Kvert_zero", "rank-zero vs finite branch classifier"),
        ("SRC4529_04_doc1619", "1619 SGK normal-form document", DOC_1619, "positive auxiliary / response-doublet `S_GK` normal form", "main formal mechanism"),
        ("SRC4529_05_normal1619", "1619 normal-form rows", NORMAL_1619, "NF1619_1_parent_action_density", "explicit action density"),
        ("SRC4529_06_gaps1619", "1619 parent signature gap ledger", GAPS_1619, "GAP1619_1_exchange_symmetry", "open parent-signature clauses"),
        ("SRC4529_07_silence1619", "1619 local silence theorem", SILENCE_1619, "LS1619_2_zero_theorem", "zero-source rigidity theorem"),
        ("SRC4529_08_doc1621", "1621 constraint/no-pole document", DOC_1621, "NO_POLE_NOT_DERIVED_CURRENT_MTS", "alternative exact rank-zero path"),
        ("SRC4529_09_gate1621", "1621 no-pole gate", GATE_1621, "CFG1621_4_no_kinetic_pole", "keeps Kvert zero unsigned"),
        ("SRC4529_10_action4527", "4527 action-odd force theorem", ACTION_4527, "AOF4527_1_first_force", "A_A is the dangerous first variation"),
        ("SRC4529_11_symbol4527", "4527 vertical principal symbol test", PRINCIPAL_4527, "APS4527_1_principal_symbol", "Kvert is the kinetic/principal block"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle, role in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "label": label,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "snippet": snippet(path, needle),
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SGK4529_0_field_split",
            "object": "Z^A=(R_+^A-R_-^A)/2",
            "derivation": "Split local residual channels into exchange-even readout R_even and exchange-odd vertical residual Z.",
            "formula": "R_even^A=(R_+^A+R_-^A)/2, I_q: Z^A -> -Z^A",
            "condition": "R_+ and R_- must be actual parent variables, not post-hoc labels.",
            "result": "Z becomes the candidate physical local residual coordinate.",
            "status": "FORMAL_DERIVED_FROM_SGK_TEMPLATE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_1_exchange_kills_A",
            "object": "action-odd force A_A",
            "derivation": "If S_parent and S_matter descend through exchange-even variables, the integrand is even in Z and the first variation at Z=0 vanishes.",
            "formula": "S[Z]=S[-Z] => A_A=(delta S_odd/delta Z^A)|_0=0 and J_A=(delta S_matter/delta Z^A)|_0=0",
            "condition": "exact parent exchange symmetry plus matter/readout descent.",
            "result": "F_1=0 is not an axiom; it follows from parent evenness.",
            "status": "THEOREM_IF_PARENT_SIGNATURE_SIGNS",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_2_euler_operator",
            "object": "SGK residual equation",
            "derivation": "Vary the positive normal-form action with respect to Z on the gauge-reduced local branch.",
            "formula": "E_A=-nabla_mu(H_AB nabla^mu Z^B)+M_AB^2 Z^B+O(Z^2,Z nabla Z,nabla Z^2)-J_A-B_A=0",
            "condition": "H_AB and M_AB^2 are parent-owned tensors with declared signs and boundary convention.",
            "result": "The local residual is either killed by zero source/boundary or becomes a finite massive response.",
            "status": "FORMAL_VARIATION_DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_3_energy_identity",
            "object": "coercive local energy",
            "derivation": "Pair the Euler equation with Z and integrate over the local collar/domain.",
            "formula": "int(H_AB nabla Z^A nabla Z^B+M_AB^2 Z^A Z^B) <= |<J+B,Z>| + O(||Z||^3)",
            "condition": "positive H_AB, positive non-gauge M_AB^2, controlled boundary terms, small residual branch.",
            "result": "A quantitative suppression bound replaces the old plateau axiom.",
            "status": "FORMAL_ENERGY_BOUND_DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_4_zero_source_rigidity",
            "object": "local GR silence branch",
            "derivation": "Set J_A=0 and B_A=0 in the coercive identity.",
            "formula": "h0||nabla Z||^2 + m0^2||Z||^2 <= 0 => Z=0 modulo gauge zero modes",
            "condition": "h0>0, m0^2>0 on physical modes; gauge modes quotient out; no boundary/source re-entry.",
            "result": "q_loc^nu=P_loc(E_A nabla^nu Z^A+B_GK^nu)=0 and F_1=0.",
            "status": "LOCAL_ZERO_THEOREM_IF_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_5_finite_source_bound",
            "object": "finite residual response",
            "derivation": "Keep J_A or B_A nonzero and invert the coercive operator on the physical subspace.",
            "formula": "||Z||_{H1} <= C_L (||J||_{H-1}+||B||_{H-1}) + O((||J||+||B||)^2)",
            "condition": "Green/operator norm C_L sourced or bounded; no hidden cancellation between source classes.",
            "result": "If exact local GR fails, the branch becomes an empirical bound instead of a vague failure.",
            "status": "FINITE_BOUND_ROUTE_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_6_range_and_alpha",
            "object": "R10/local fifth-force observable",
            "derivation": "Diagonalize the positive physical SGK operator into modes with kinetic weight h_i and mass weight m_i^2.",
            "formula": "mu_i^2=m_i^2/h_i, lambda_i=1/mu_i, alpha_i=K_i Q_iS Q_iT/(G_N M_S m_T m_i^2)",
            "condition": "normalizations h_i,m_i,K_i,Q_iS,Q_iT must come from the parent action/source map.",
            "result": "Kvert positive rank is not fatal; it is a finite-range prediction row if sourced.",
            "status": "FINITE_RANGE_TRANSLATION_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SGK4529_7_branch_classifier",
            "object": "rank-zero versus SGK massive branch",
            "derivation": "Compare 1621 no-pole route with SGK positive operator route.",
            "formula": "Kvert=0 => constraint/rank-zero branch; Kvert>0 with m_i^2>0 => massive finite-source branch; Kvert<0 or ghost h_i<=0 => reject branch",
            "condition": "principal-symbol and Hessian signatures must be sourced.",
            "result": "The best route is not to pretend SGK proves Kvert=0; it proves a conditional zero-source theorem and a finite-bound fallback.",
            "status": "CLASSIFIER_DERIVED",
            "valid_for_claim": False,
        },
    ]


def signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "SIG4529_0_parent_doublets",
            "needed_signature": "Actual MTS local residual variables can be paired as R_+^A,R_-^A with Z^A odd and R_even readout.",
            "why_it_matters": "Without this, SGK is a useful normal form but not the MTS parent branch.",
            "current_source": str(GAPS_1619),
            "current_status": "not_derived",
            "closes": "field map from MTS residuals to SGK variables",
            "next_action": "construct explicit variable map or demote SGK to analogy only",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4529_1_exchange_even_action",
            "needed_signature": "S_parent[I_q Phi]=S_parent[Phi] through quadratic order and no odd Z invariants.",
            "why_it_matters": "This is the clean derivation of A_A=0 and F_1=0.",
            "current_source": str(GAPS_1619),
            "current_status": "conditional_template",
            "closes": "action-odd force zero",
            "next_action": "test candidate MTS action terms under I_q and write epsilon_I if not exact",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4529_2_even_matter_readout",
            "needed_signature": "Matter, clocks and source masses couple only through R_even/q(Phi), not directly to Z.",
            "why_it_matters": "Otherwise J_A survives even if the pure action is even.",
            "current_source": str(GAPS_1619),
            "current_status": "source_current_zero_not_derived",
            "closes": "J_A=0",
            "next_action": "write source-current zero lemma or first J_A norm row",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4529_3_boundary_silence",
            "needed_signature": "Odd boundary charge/symplectic flux vanishes on the local collar.",
            "why_it_matters": "Bulk zero theorem fails if a boundary term feeds Z.",
            "current_source": str(GAPS_1619),
            "current_status": "conditional_not_closed",
            "closes": "B_A=0",
            "next_action": "separate bound/local worldtube boundary from cosmological flux/Poynting-wave terms",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4529_4_positive_operator",
            "needed_signature": "H_AB positive and M_AB^2 nonnegative/positive after gauge and constraint removal.",
            "why_it_matters": "This supplies coercivity and rules out tachyon/ghost local residuals.",
            "current_source": str(GAPS_1619),
            "current_status": "formal_candidate_only",
            "closes": "energy estimate and finite range eigenvalues",
            "next_action": "extract or bound h0 and m0^2 from parent coefficients",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4529_5_PPN_source_lock",
            "needed_signature": "Z is the physical q_loc/PPN/source-normalization residual vector, not an unobserved auxiliary.",
            "why_it_matters": "Zeroing the wrong variable would not recover GR/Newton locally.",
            "current_source": str(GAPS_1619),
            "current_status": "not_derived",
            "closes": "observable PPN/local-GR readout",
            "next_action": "map Z readout to gamma_PPN, beta_PPN, G_N normalization and R10 alpha rows",
            "valid_for_claim": False,
        },
    ]


def value_rows() -> list[dict[str, Any]]:
    return [
        {
            "value_id": "VALSRC4529_0_epsilon_I",
            "quantity": "epsilon_I",
            "meaning": "normalized parent action asymmetry under I_q",
            "formula": "epsilon_I=||S_parent[Phi]-S_parent[I_q Phi]||/(V_loc E_ref)",
            "needed_for": "if exchange symmetry is approximate rather than exact",
            "current_value": "MISSING_PARENT_ACTION_DENSITY_AND_IQ_MAP",
            "units": "dimensionless",
            "valid_for_claim": False,
        },
        {
            "value_id": "VALSRC4529_1_h0",
            "quantity": "h0",
            "meaning": "minimum positive eigenvalue of H_AB on physical local modes",
            "formula": "H_AB xi^A xi^B >= h0 |xi|^2",
            "needed_for": "coercive energy identity and lambda_i normalization",
            "current_value": "MISSING_HESSIAN_KINETIC_SIGNATURE",
            "units": "action-density kinetic normalization",
            "valid_for_claim": False,
        },
        {
            "value_id": "VALSRC4529_2_m0sq",
            "quantity": "m0^2",
            "meaning": "minimum positive non-gauge mass/stiffness eigenvalue",
            "formula": "M_AB^2 xi^A xi^B >= m0^2 |xi|^2",
            "needed_for": "Z=0 rigidity and finite range lambda_i",
            "current_value": "MISSING_MASS_STIFFNESS_SIGNATURE",
            "units": "action-density mass normalization",
            "valid_for_claim": False,
        },
        {
            "value_id": "VALSRC4529_3_Jnorm",
            "quantity": "||J||",
            "meaning": "source-current norm feeding the odd local residual",
            "formula": "J_A=(delta S_matter/delta Z^A)|_0",
            "needed_for": "decide exact silence versus finite sourced hair",
            "current_value": "MISSING_SOURCE_CURRENT_ZERO_OR_BOUND",
            "units": "H^-1 force/source norm",
            "valid_for_claim": False,
        },
        {
            "value_id": "VALSRC4529_4_Bnorm",
            "quantity": "||B||",
            "meaning": "boundary, flux, Poynting/wave, or worldtube tail norm in the Z equation",
            "formula": "B_A = boundary/symplectic/radiative contribution to E_A",
            "needed_for": "avoid hiding local residual in boundary conditions",
            "current_value": "MISSING_BOUNDARY_AND_WAVE_FLUX_BOUND",
            "units": "H^-1 boundary/source norm",
            "valid_for_claim": False,
        },
        {
            "value_id": "VALSRC4529_5_alpha_mode",
            "quantity": "alpha_i(lambda_i)",
            "meaning": "finite-range local fifth-force comparator row",
            "formula": "lambda_i=sqrt(h_i)/m_i; alpha_i=K_i Q_iS Q_iT/(G_N M_S m_T m_i^2)",
            "needed_for": "R10/PPN/clocks/orbital local bound testing if exact local GR remains unsigned",
            "current_value": "MISSING_K_Q_SOURCE_AND_BOUND_CURVE",
            "units": "dimensionless alpha at length lambda_i",
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4529_0_formal_derivation",
            "gate": "derive SGK zero-source theorem and finite-source bound",
            "status": "PASS_FORMAL",
            "detail": "4529 derives the variation, energy identity, zero-source rigidity and finite response formula.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4529_1_parent_signature",
            "gate": "parent-sign exchange, matter descent, boundary silence and positivity",
            "status": "BLOCKED_UNSIGNED",
            "detail": "1619 gap ledger remains open for actual MTS variables.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4529_2_exact_local_GR",
            "gate": "claim exact local GR/q_loc=0",
            "status": "BLOCKED",
            "detail": "requires J_A=0, B_A=0 and positive operator signatures from parent sources.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4529_3_finite_bound",
            "gate": "score finite Kvert branch against local tests",
            "status": "BLOCKED_VALUES_MISSING",
            "detail": "requires h_i, m_i, K_i, Q_iS, Q_iT and bound curves.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4529_4_no_magic_auxiliary",
            "gate": "avoid forcing GR with an inserted multiplier",
            "status": "PASS_FIREWALL",
            "detail": "4529 keeps 1621 no-pole route as separate conditional, not a hidden axiom.",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4529_0",
            "decision": DECISION,
            "meaning": "The leap forward is real but conditional: SGK supplies a mathematically clean local-zero theorem when parent exchange, matter descent, boundary silence and positivity are signed. If those fail, the same derivation gives a finite massive residual branch with concrete values to source.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "first try source-current zero J_A=0 and boundary silence B_A=0; if not exact, fill first h_i/m_i/K_i/Q_i rows for finite Kvert branch",
            "why": "This is the fastest path from formal mechanism to either derived local GR or an empirical local bound.",
            "valid_for_claim": False,
        }
    ]


def validate(sources: list[dict[str, Any]], theorem: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    source_failures = [row["source_id"] for row in sources if not row["path_exists"] or not row["needle_found"]]
    checks.append(
        {
            "validation_id": "VAL4529_00_sources",
            "status": "PASS" if not source_failures else "FAIL",
            "detail": "all source paths exist and needles found" if not source_failures else ";".join(source_failures),
        }
    )

    theorem_ids = {row["theorem_id"] for row in theorem}
    required_theorem = {"SGK4529_1_exchange_kills_A", "SGK4529_4_zero_source_rigidity", "SGK4529_6_range_and_alpha"}
    checks.append(
        {
            "validation_id": "VAL4529_01_theorem_rows",
            "status": "PASS" if required_theorem <= theorem_ids else "FAIL",
            "detail": "exchange-zero, local-rigidity and finite alpha theorem rows present",
        }
    )

    blocked_gates = [row for row in gates if row["valid_for_claim"] is False]
    checks.append(
        {
            "validation_id": "VAL4529_02_claims_blocked",
            "status": "PASS" if len(blocked_gates) == len(gates) else "FAIL",
            "detail": "all gates remain private nonclaim until parent signatures/values exist",
        }
    )

    csv_files = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        SIGNATURE_CSV,
        VALUE_SOURCE_CSV,
        GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
    ]
    parse_failures = []
    for path in csv_files:
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                parse_failures.append(path.name)
        except Exception as exc:  # pragma: no cover
            parse_failures.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4529_03_csv_parse",
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": "all generated CSV files parse and have rows" if not parse_failures else ";".join(parse_failures),
        }
    )

    checks.append(
        {
            "validation_id": "VAL4529_04_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        }
    )

    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4529_OVERALL",
            "status": overall,
            "detail": "4529 SGK descent theorem and finite Kvert source contract" if overall == "PASS" else "4529 validation failed",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    values: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> str:
    return f"""# 4529 — Positive SGK Parent Signature Map Or EpsilonI Kvert Value Source

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Generated: `{now()}`

## What Moved

- This is not another missing-list pass. It makes the mathematical leap explicit: the `S_GK` normal form gives an actual local-zero theorem if the parent signatures sign.
- The key fork is now clean: either MTS parent-signs exchange-even action/matter/boundary/positivity and obtains `Z=0`, `q_loc^nu=0`, `F_1=0`; or the same formalism becomes a finite massive residual branch with `lambda_i, alpha_i` rows.
- SGK does **not** honestly prove `Kvert=0`. It proves a positive-operator route. Exact rank-zero/no-pole remains the separate 1621 route.
- The next work is therefore source-current first: prove `J_A=0` and `B_A=0`, or fill `h_i, m_i, K_i, Q_iS, Q_iT` for a real local bound.

## Derived SGK Contract

```text
I_q: Z^A -> -Z^A
S[Z]=S[-Z] and S_matter=S_matter[R_even,q(Phi),theta]
    => A_A=(delta S_odd/delta Z^A)|_0=0
    => J_A=(delta S_matter/delta Z^A)|_0=0

E_A = -nabla_mu(H_AB nabla^mu Z^B)+M_AB^2 Z^B+O(Z^2,Z nabla Z,nabla Z^2)-J_A-B_A = 0

int(H_AB nabla Z^A nabla Z^B + M_AB^2 Z^A Z^B)
    <= |<J+B,Z>| + O(||Z||^3)

J_A=B_A=0, H>0, M^2>0
    => Z=0 modulo gauge
    => q_loc^nu=P_loc(E_A nabla^nu Z^A+B_GK^nu)=0
```

## SGK Descent Theorem Rows

{md_table(theorem)}

## Parent Signature Map

{md_table(signatures)}

## EpsilonI / Kvert Value Source Rows

{md_table(values)}

## Claim Gates

{md_table(gates)}

## Decision

{md_table(decisions)}

## Source Register

{md_table(sources)}

## Validation

{md_table(validation)}
"""


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n")
        handle.write(block.strip())
        handle.write("\n")


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_sgk_descent",
        "claim": "4529 derives the SGK local-zero theorem/finite massive residual fork and maps the parent signatures needed to promote it.",
        "current_evidence": "Generated SGK descent theorem rows, parent signature map, epsilonI/Kvert value source rows, claim gates and validation P8_Y5_BRR545_4529_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_sgk_derivation_values_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the formal SGK zero theorem as current MTS local GR before parent exchange, source-current zero, boundary silence and positivity are signed.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Pretending positive SGK proves Kvert=0; it instead gives zero-source rigidity or finite massive residual bounds.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    signatures = signature_rows()
    values = value_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(SIGNATURE_CSV, signatures)
    write_csv(VALUE_SOURCE_CSV, values)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, signatures, values, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4529 Positive SGK Parent Signature Map Or EpsilonI Kvert Value Source

Marker: `{MARKER}`  
The local-GR derivation fork is sharper: SGK gives a formal theorem, not just a vibe. If parent exchange symmetry, matter descent, boundary silence and positive operator signatures are signed, then `A_A=0`, `J_A=0`, `B_A=0`, `Z=0`, `q_loc^nu=0`, and `F_1=0`. If those are not signed, the same operator gives a finite massive residual branch with `lambda_i`/`alpha_i` values to source.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4529 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now treats SGK as a conditional theorem/fork: exact local silence if source-current and boundary terms vanish, finite local-test residuals if they do not. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
