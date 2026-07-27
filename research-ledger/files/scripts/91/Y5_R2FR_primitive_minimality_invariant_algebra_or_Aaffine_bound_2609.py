from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_PRIMITIVE_PACKAGE_GATE_2609"
CHECKPOINT_ID = "2609"

DOC = ROOT / "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_LINEAGE_LEDGER.csv",
    "primitive_minimality": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
    "invariant_algebra": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_INVARIANT_ALGEBRA_AUDIT.csv",
    "constant_source": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
    "aaffine_interface": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_AAFFINE_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2609_VALIDATION.csv",
}

COPY_TARGETS = {
    "primitive_minimality": LOCAL_BOUNDS / "Primitive_minimality_attempt_2609_NONCLAIM.csv",
    "invariant_algebra": LOCAL_BOUNDS / "Invariant_algebra_debts_2609_NONCLAIM.csv",
    "aaffine_interface": LOCAL_BOUNDS / "Aaffine_bound_interface_2609_NONCLAIM.csv",
    "next_target": QUEUE / "JR2609_COUPLING_CHAIN_DOUBLE_ZERO_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2609_00_2608_handoff_doc",
            "source_path": ROOT / "2608-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md",
            "needles": ["NEXT2608_0_selected", "CO2608_5_verdict", "NLM2608_6_verdict", "VAL2608_OVERALL"],
            "role": "current handoff selecting primitive-minimality/invariant-algebra gate",
        },
        {
            "source_id": "SRC2609_01_2608_obligations",
            "source_path": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_PRIMITIVE_PACKAGE_OBLIGATIONS.csv",
            "needles": ["PO2608_2_primitive_minimality", "PO2608_4_invariant_algebra_triviality", "PO2608_5_constant_source_universality"],
            "role": "current primitive package obligations",
        },
        {
            "source_id": "SRC2609_02_2608_affine_interface",
            "source_path": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_AFFINE_SOURCE_BOUND_ROWS.csv",
            "needles": ["ASB2608_0_A_shift", "ASB2608_2_A_affine", "ASB2608_3_R_source_affine"],
            "role": "current affine source fallback interface",
        },
        {
            "source_id": "SRC2609_03_1758_doc",
            "source_path": ROOT / "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
            "needles": ["PM1758_4_promotion", "IA1758_5_species_constants", "VAL1758_OVERALL"],
            "role": "prior primitive minimality/invariant algebra proof attempt",
        },
        {
            "source_id": "SRC2609_04_1758_primitive",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1758_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
            "needles": ["PM1758_0_target", "PM1758_2_material_marker_no_extension", "PM1758_4_promotion"],
            "role": "prior primitive minimality rows",
        },
        {
            "source_id": "SRC2609_05_1758_invariant",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1758_INVARIANT_ALGEBRA_AUDIT.csv",
            "needles": ["IA1758_0_target", "IA1758_3_chiD", "IA1758_6_readout_projector"],
            "role": "prior local invariant algebra generator debts",
        },
        {
            "source_id": "SRC2609_06_1758_constant",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
            "needles": ["CS1758_0_representation_data", "CS1758_4_universal_kappa", "CS1758_6_verdict"],
            "role": "prior constant/source universality audit",
        },
        {
            "source_id": "SRC2609_07_1758_aaffine",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1758_AAFFINE_BOUND_INTERFACE.csv",
            "needles": ["AAI1758_0_zero_condition", "AAI1758_3_A_affine", "AAI1758_4_R_affine"],
            "role": "prior A_affine finite fallback interface",
        },
        {
            "source_id": "SRC2609_08_1759_next_doc",
            "source_path": ROOT / "1759-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "needles": ["CCS1759_0_target", "DEC1759_4_best_next", "VAL1759_OVERALL"],
            "role": "prior next hidden source route: coupling-chain double-zero",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2609_0_2608",
            "checkpoint": "2608",
            "question": "What common parent package would kill A_shift and A_marker?",
            "result": "Primitive minimality plus invariant-algebra triviality plus constant/source universality would force X0(q)=0 and ell_marker=0.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "primitive minimality and generator-debt audit",
        },
        {
            "step_id": "LIN2609_1_1758_minimality",
            "checkpoint": "1758",
            "question": "Does primitive minimality forbid marker quotient extensions?",
            "result": "No. Fixed spurions can be conditionally excluded, but co-moving material/domain markers and quotient extensions remain legal.",
            "status": "MINIMALITY_NOT_PROVED",
            "next_dependency": "A_shift/A_marker remain live",
        },
        {
            "step_id": "LIN2609_2_1758_invariant",
            "checkpoint": "1758",
            "question": "Is the local invariant algebra trivial?",
            "result": "No. Fibre spectrum, domain class, chi_D, memory scalar, species constants and readout projectors remain generator debts.",
            "status": "GENERATOR_DEBTS_RETAINED",
            "next_dependency": "A_marker component rows or generator-by-generator proof",
        },
        {
            "step_id": "LIN2609_3_1758_constant",
            "checkpoint": "1758",
            "question": "Are matter constants/source weights universally source-blind?",
            "result": "Only relatively. Representation data and universal kappa route is coherent but not parent-derived.",
            "status": "CONSTANT_SOURCE_UNIVERSALITY_UNSIGNED",
            "next_dependency": "WEP/clock/source normalization source envelope remains live",
        },
        {
            "step_id": "LIN2609_4_1759_preview",
            "checkpoint": "1759",
            "question": "What hidden source comes after affine package failure?",
            "result": "Coupling-chain source requires double-zero or selector independence; it is the next derivation-first target.",
            "status": "NEXT_ROUTE_IMPORTED",
            "next_dependency": "2610 coupling-chain double-zero proof or A_chain bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def primitive_minimality_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PM2609_0_target",
            "primitive parent configuration has no extended marker quotient",
            "Conf_parent=Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel",
            "TARGET_EXACT",
            "would block co-moving material/domain markers from generating X0(q), ell_marker, theta_A(m), or direct marker charge",
            "parent minimality is a contract, not a theorem forbidding all quotient extensions",
        ),
        (
            "PM2609_1_fixed_spurions",
            "fixed external labels are excluded",
            "m_fixed is not a function on Q=Phi/G_rep",
            "CONDITIONAL_PASS_IF_STRICT_QUOTIENT",
            "fixed non-orbit covectors cannot source X",
            "does not exclude co-moving material markers or quotient-invariant class scalars",
        ),
        (
            "PM2609_2_material_marker_no_extension",
            "co-moving material markers are forbidden",
            "no natural extension Q_tilde=(Q_MTS,m)/G_rel with m carrying material/domain/source data",
            "NOT_DERIVED",
            "would remove theta_A(m(X)), direct marker covectors, and some qbar_XT source charges",
            "current corpus has a minimality contract but no theorem excluding extended quotient objects",
        ),
        (
            "PM2609_3_no_natural_marker_functor",
            "no nonconstant marker functor on local branch",
            "Nat(Q_MTS,Marker)_loc=constants",
            "REDUCED_TO_INVARIANT_ALGEBRA_TRIVIALITY",
            "partial_X theta_A=0 if constants factor through marker-free functors",
            "local invariant algebra still has uneliminated candidate generators",
        ),
        (
            "PM2609_4_zero_section_support",
            "primitive minimality supports centered origin",
            "if no natural section Q_MTS->E_X exists except 0_X, then X0(q)=0",
            "EXACT_CONDITIONAL_THEOREM",
            "would close A_shift with the 2608 norm-square kinetic owner",
            "requires invariant-algebra triviality and no quotient extension theorem",
        ),
        (
            "PM2609_5_promotion",
            "primitive minimality promotes A_shift=A_marker=0",
            "primitive minimality + no marker functors + no invariant dual => X0=0 and ell_marker=0",
            "BLOCKED_FOR_CLAIM",
            "would close the leading affine F_1 obstruction",
            "primitive minimality and invariant algebra triviality are not parent-derived",
        ),
    ]
    return [
        with_stamp(
            {
                "attempt_id": attempt_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "derived_effect": derived_effect,
                "gap": gap,
                **false_flags(),
            }
        )
        for attempt_id, claim_piece, mathematical_form, status, derived_effect, gap in rows
    ]


def invariant_algebra_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "IA2609_0_target",
            "target algebra",
            "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const",
            "TARGET_EXACT",
            "would block local marker functors",
            "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
        ),
        (
            "IA2609_1_fibre",
            "finite_cell_fibre_spectrum",
            "finite fibre spectrum can act as material/source marker or effective charge label",
            "NOT_TRIVIALIZED",
            "can build ell_marker or source weights",
            "MISSING_FIBRE_SPECTRUM_UNIVERSAL_OR_GAUGE_PROOF",
        ),
        (
            "IA2609_2_domain_class",
            "relative_boundary_domain_class",
            "relative/domain class can carry local source/class marker",
            "NOT_DERIVED",
            "can create boundary/domain charge",
            "MISSING_LOCAL_TRIVIAL_CLASS_OR_CLASS_NOHAIR",
        ),
        (
            "IA2609_3_chiD",
            "chi_D/domain_selector",
            "domain selector can become preferred-frame/source-normalization/R10/R11 marker",
            "NOT_DERIVED",
            "can create source/projector dependence",
            "MISSING_SELECTOR_GAUGE_OR_LOCAL_TRIVIAL_BRANCH",
        ),
        (
            "IA2609_4_memory_scalar",
            "memory_or_class_scalar",
            "memory/class scalar can enter clock/source/fifth-force channels",
            "NOT_SILENCED_AS_THEOREM",
            "can generate ell_marker or A_mu_even",
            "MISSING_LOCAL_VALUE_GRADIENT_ZERO_OR_BOUND",
        ),
        (
            "IA2609_5_species_constants",
            "species_charge_constants",
            "species constants can act as WEP/source-charge/clock markers",
            "NOT_UNIVERSALIZED",
            "can generate theta_A(X), kappa_A, and source weights",
            "MISSING_CONSTANT_SOURCE_UNIVERSALITY",
        ),
        (
            "IA2609_6_readout_projector",
            "post_readout_projector",
            "post-readout projector can re-enter as reduced-action source if not kept after variation",
            "NO_CHEAT_RULE_ONLY",
            "fake closure zeros can become EFT sources",
            "MISSING_FULL_PARENT_DOMAIN_READOUT_AUDIT",
        ),
        (
            "IA2609_7_no_invariant_dual",
            "dual representation",
            "(E_X*)^{G_X}=0",
            "RELATIVE_THEOREM_NOT_PARENT_SIGNED",
            "would kill quotient-compatible fixed linear covectors",
            "MISSING_GX_EX_AND_NO_TRIVIAL_DUAL_PROOF",
        ),
        (
            "IA2609_8_verdict",
            "local invariant algebra verdict",
            "candidate marker/source generators remain legal in the current parent package",
            "NOT_TRIVIALIZED",
            "A_marker remains live",
            "GENERATOR_DEBTS_RETAINED",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "generator": generator,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "risk": risk,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, generator, mathematical_form, current_status, risk, gap in rows
    ]


def constant_source_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CS2609_0_representation_data",
            "matter constants are representation/superselection data",
            "theta_A in Rep_A, not theta_A(X,I_Q,m,h)",
            "VALID_RELATIVE_THEOREM",
            "would stop constants becoming local MTS marker channels",
            "parent representation bundle not fully signed",
        ),
        (
            "CS2609_1_trivial_MTS_action",
            "MTS selectors/invariants/markers/memory/fibre directions act trivially on constants",
            "L_X theta_A=L_IQ theta_A=L_m theta_A=L_h theta_A=0",
            "NOT_PARENT_DERIVED",
            "would close theta_A(I_Q), theta_A(m), theta_A(h) counterexamples",
            "constant-sector trivial action remains unsigned",
        ),
        (
            "CS2609_2_no_direct_constant_vertices",
            "no direct MTS-dependent matter constants",
            "no alpha_EM(X)F^2, no m_A(X), no q_A X_mu J_A^mu",
            "FORBIDDEN_VERTEX_POLICY_ONLY",
            "would block clock, WEP, and fifth-force marker vertices",
            "policy is not yet a parent theorem",
        ),
        (
            "CS2609_3_Hilbert_source",
            "ordinary active source is the Hilbert/coframe current",
            "tau_a^mu=det(e)^-1 delta S_m/delta e_mu^a",
            "CONDITIONAL_STANDARD_IDENTITY",
            "would prevent fitted/readout-defined source charge from replacing Hilbert source",
            "matter descent through q and source owner remain unsigned",
        ),
        (
            "CS2609_4_universal_kappa",
            "field equation uses one universal coupling for Hilbert current",
            "E_munu=kappa_univ T_munu, not sum_A kappa_A T_A_munu",
            "NOT_PARENT_DERIVED",
            "would block species-weighted active source charge",
            "universal coupling not parent-owned",
        ),
        (
            "CS2609_5_Bianchi_limit",
            "do not overclaim Bianchi",
            "nabla_mu E^{mu nu}=0 exposes grad(kappa) residual unless no-exchange/source owner closes",
            "OVERCLAIM_BLOCKER_RETAINED",
            "prevents hiding exchange/source terms by notation",
            "Bianchi alone does not derive constant/source universality",
        ),
        (
            "CS2609_6_verdict",
            "constant/source universality certificate",
            "theta_A fixed representation data + one global kappa + Hilbert current => b_theta=b_kappa=0",
            "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "would shrink WEP/clock/source-normalization marker channels",
            "finite qbar/source envelope remains live",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "derived_effect": derived_effect,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, current_status, derived_effect, gap in rows
    ]


def aaffine_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AAI2609_0_zero_condition",
            "Z_affine",
            "Z_affine=True only if primitive minimality, invariant algebra triviality, no trivial dual, and constant/source universality all pass",
            "FALSE_PARENT_UNSIGNED",
            "Z_affine = Z_shift and Z_marker",
        ),
        (
            "AAI2609_1_A_shift",
            "A_shift",
            "||L_X X0(q)||_{E*}, or theorem-zero from parent zero section",
            "MISSING_CENTERED_ORIGIN_ZERO_OR_A_SHIFT",
            "A_shift >= 0 in declared E* norm",
        ),
        (
            "AAI2609_2_A_marker",
            "A_marker",
            "||ell_marker||_{E*}, or theorem-zero from no-marker package",
            "MISSING_NO_MARKER_THEOREM_OR_A_MARKER",
            "A_marker <= A_fibre + A_domain + A_chiD + A_memory + A_species + A_readout",
        ),
        (
            "AAI2609_3_A_affine",
            "A_affine",
            "A_affine <= A_shift + A_marker in one declared E* norm",
            "MISSING_COMMON_ESTAR_NORM_AND_COMPONENT_VALUES",
            "||J_affine||_{E*} <= A_affine",
        ),
        (
            "AAI2609_4_R_source_affine",
            "R_source_affine",
            "||R_source,affine||_{E*} <= U_B A_affine",
            "MISSING_AAFFINE_AND_ESTAR_UNITS",
            "retains repaired p_total=1 for affine p_int=0 source residual",
        ),
        (
            "AAI2609_5_R_affine_arena",
            "R_affine_arena",
            "||R_affine,arena|| <= U_B ||P_arena L_X^{-1}|| A_affine",
            "MISSING_OPERATOR_INVERSE_ARENA_PROJECTION_AND_UNITS",
            "source residual response to affine hidden current",
        ),
    ]
    return [
        with_stamp(
            {
                "interface_id": interface_id,
                "quantity": quantity,
                "definition": definition,
                "current_status": current_status,
                "notes": notes,
                **false_flags(),
            }
        )
        for interface_id, quantity, definition, current_status, notes in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SZ2609_0_affine",
            "J_affine",
            "NOT_ZEROED",
            "primitive minimality and invariant algebra triviality fail current claim",
            "A_shift, A_marker, A_affine remain missing/nonclaim",
        ),
        (
            "SZ2609_1_marker_package",
            "marker/source package",
            "REDUCED_TO_NAMED_GENERATOR_DEBTS",
            "finite fibre, domain class, chi_D, memory scalar, species constants and readout projector retained",
            "eliminate each generator or bound its marker covector",
        ),
        (
            "SZ2609_2_constant_source",
            "constant/source universality",
            "RELATIVE_NOT_PARENT_SIGNED",
            "Hilbert source/universal kappa route is coherent but unsigned",
            "species/source-weight envelope remains live",
        ),
        (
            "SZ2609_3_Aaffine",
            "A_affine interface",
            "FINITE_INTERFACE_STAGED_NONCLAIM",
            "A_affine<=A_shift+A_marker and ||R_source,affine||<=U_B A_affine",
            "numeric/source-backed E* values and projection norms missing",
        ),
        (
            "SZ2609_4_source_silence",
            "S_cg(D_L=0,Y)",
            "NOT_DERIVED",
            "affine source not zeroed and other hidden channels remain",
            "J_hidden not zero; coupling chain is next derivation target",
        ),
        (
            "SZ2609_5_GR_Newton",
            "local GR/Newton bridge",
            "CLOSER_BUT_BLOCKED",
            "affine package is named and nonclaim; no local-GR source silence follows",
            "coupling chain, matter/worldtube, boundary/history, tower, mu_even, kernel and projection rows remain open",
        ),
    ]
    return [
        with_stamp(
            {
                "status_id": status_id,
                "quantity": quantity,
                "current_status": current_status,
                "evidence": evidence,
                "remaining_gap": remaining_gap,
                **false_flags(),
            }
        )
        for status_id, quantity, current_status, evidence, remaining_gap in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2609_0_primitive_minimality", "primitive minimality forbids all marker quotient extensions", "BLOCKED_CO_MOVING_MARKER_AND_QUOTIENT_EXTENSION_THEOREM_MISSING"),
        ("GATE2609_1_invariant_algebra", "local invariant algebra has no marker/source generators", "BLOCKED_GENERATOR_DEBTS_RETAINED"),
        ("GATE2609_2_constant_source", "matter constants and source weights are universally source-blind", "BLOCKED_CONSTANT_SOURCE_UNIVERSALITY_PARENT_SIGNATURE"),
        ("GATE2609_3_Aaffine_zero", "A_affine=0 is parent-derived", "BLOCKED_A_SHIFT_A_MARKER_LIVE"),
        ("GATE2609_4_Aaffine_score", "A_affine can be scored in local arenas", "BLOCKED_ESTAR_OPERATOR_PROJECTION_UNITS_MISSING"),
        ("GATE2609_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2609_0_minimality",
            "decision": "primitive minimality not proved",
            "reason": "fixed spurions are conditionally excluded, but co-moving material/domain markers and quotient extensions remain legal",
            "effect": "do not set A_shift or A_marker to zero from minimality",
        },
        {
            "decision_id": "DEC2609_1_invariant_algebra",
            "decision": "local invariant algebra not trivialized",
            "reason": "finite fibre spectrum, domain class, chi_D, memory scalar, species constants and readout projector generators remain",
            "effect": "retain A_marker component rows or eliminate generators one by one",
        },
        {
            "decision_id": "DEC2609_2_constant_source",
            "decision": "constant/source universality remains relative",
            "reason": "representation-data and universal-kappa route is coherent but not derived from primitives",
            "effect": "keep WEP/clock/source-normalization source envelope live",
        },
        {
            "decision_id": "DEC2609_3_Aaffine",
            "decision": "write A_affine interface as nonclaim residual",
            "reason": "the zero theorem failed, so A_shift/A_marker/A_affine must remain explicit residual inputs",
            "effect": "do not claim F_1=0; use interface only if numerical/source-envelope pass is needed",
        },
        {
            "decision_id": "DEC2609_4_best_next",
            "decision": "select coupling-chain source double-zero proof or A_chain bound",
            "reason": "affine source is now fully named and nonclaim; the next hidden source is f'(0) C_obs partial_X chi_D plus f(0) delta_X C_obs",
            "effect": "2610 should attack the coupling-chain source before matter/worldtube vertex cleanup",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2609_0_selected",
            "selection_status": "selected",
            "target_file": "2610-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "target_script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound_2610.py",
            "task": "try to derive f(0)=f'(0)=0 or delta_X chi_D=0 at the local fixed point; otherwise carry A_chain as finite nonclaim residual",
            "success_condition": "observable coupling-chain source is theorem-zero or explicit finite A_chain residual in E* units",
            "fallback_condition": "if chain source is ledgered but not zeroed, move to matter/worldtube quotient descent or A_matter bound",
            "guardrails": "no tuning f after local tests; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2609_1_Aaffine_fallback",
            "selection_status": "held_fallback",
            "target_file": "2610b-Y5-R2FR-Aaffine-E-star-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_Aaffine_E_star_bound_runner_2610b.py",
            "task": "turn A_shift/A_marker/A_affine into a runnable nonclaim source-envelope interface with units and operator/projection norms",
            "success_condition": "finite affine residual can be evaluated as nonclaim input",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "score only after units, E* norm, operator inverse and arena projections are real",
        },
        {
            "route_id": "NEXT2609_2_matter_fallback",
            "selection_status": "held_fallback",
            "target_file": "2610c-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "target_script": "scripts/Y5_R2FR_matter_worldtube_quotient_descent_or_Amatter_bound_2610c.py",
            "task": "prove ordinary matter/worldtube terms descend through q and carry no direct X vertex; otherwise carry A_matter",
            "success_condition": "matter/worldtube hidden source is theorem-zero or finite bounded",
            "fallback_condition": "source-zero route remains finite-residual only",
            "guardrails": "do not hide material source charge inside readout definitions",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2609_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2609_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2609_01_lineage_complete", {"2608", "1758", "1759"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff, prior primitive package and next coupling route")
    add("VAL2609_02_minimality_not_proved", any(row["attempt_id"] == "PM2609_5_promotion" and row["status"] == "BLOCKED_FOR_CLAIM" for row in data["primitive_minimality"]), "primitive minimality remains unproved")
    add("VAL2609_03_fixed_spurion_limited", any(row["attempt_id"] == "PM2609_1_fixed_spurions" and row["status"] == "CONDITIONAL_PASS_IF_STRICT_QUOTIENT" for row in data["primitive_minimality"]), "fixed-spurion pass is limited and conditional")
    add("VAL2609_04_generator_debts_retained", any(row["audit_id"] == "IA2609_8_verdict" and row["current_status"] == "NOT_TRIVIALIZED" for row in data["invariant_algebra"]), "invariant-generator debts retained")
    add("VAL2609_05_constant_source_unsigned", any(row["audit_id"] == "CS2609_6_verdict" and row["current_status"] == "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED" for row in data["constant_source"]), "constant/source universality remains parent unsigned")
    add("VAL2609_06_aaffine_interface_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["aaffine_interface"]), "A_affine interface remains nonclaim")
    add("VAL2609_07_U_B_power_retained", any(row["interface_id"] == "AAI2609_4_R_source_affine" and "U_B A_affine" in row["definition"] for row in data["aaffine_interface"]), "explicit U_B source-residual factor retained")
    add("VAL2609_08_source_zero_blocked", any(row["status_id"] == "SZ2609_0_affine" and row["current_status"] == "NOT_ZEROED" for row in data["source_zero"]), "affine source zero remains blocked")
    add("VAL2609_09_source_silence_blocked", any(row["status_id"] == "SZ2609_4_source_silence" and row["current_status"] == "NOT_DERIVED" for row in data["source_zero"]), "source silence remains blocked")
    add("VAL2609_10_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2609_11_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2609_12_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*PRIMITIVE_PACKAGE_GATE_2609*", "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md", "*JR2609_COUPLING_CHAIN_DOUBLE_ZERO_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2609_13_no_formalization_artifacts", not formalization_artifacts, "no 2609 primitive-package artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2609_14_decision_next", any(row["decision_id"] == "DEC2609_4_best_next" for row in data["decisions"]), "decision selects coupling-chain source route")
    add("VAL2609_15_next_selected", any(row["route_id"] == "NEXT2609_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2609_16_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2609_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2609_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2609_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2609_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2609 primitive-minimality/invariant-algebra gate keeps A_affine nonclaim and selects coupling-chain next", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2609: R2FR Primitive Minimality / Invariant Algebra Or Aaffine Bound",
        "",
        "**Status:** private nonclaim current-branch primitive-package checkpoint. This does not claim `A_shift=0`, `A_marker=0`, `A_affine=0`, `F_1=0`, source silence, local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the common parent package behind the affine-source zero route does not close in the current corpus. Fixed spurions are conditionally excluded by a strict quotient, but co-moving material/domain markers and quotient extensions remain legal. The local invariant algebra is not trivialized: finite fibre spectrum, relative/domain class, `chi_D`, memory/class scalars, species constants, and readout projector debts remain. Constant/source universality is a good relative certificate but not parent-signed. Therefore `A_shift`, `A_marker`, and `A_affine<=A_shift+A_marker` stay live nonclaim residuals, with the repaired source factor `||R_source,affine||<=U_B A_affine`. The next derivation-first target is the coupling-chain source: prove a parent double-zero/selector-independence law, or carry `A_chain` explicitly.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Primitive Minimality Attempt",
        markdown_table(data["primitive_minimality"], ["attempt_id", "claim_piece", "mathematical_form", "status", "derived_effect", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Invariant Algebra Audit",
        markdown_table(data["invariant_algebra"], ["audit_id", "generator", "mathematical_form", "current_status", "risk", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Constant / Source Universality Audit",
        markdown_table(data["constant_source"], ["audit_id", "claim_piece", "mathematical_form", "current_status", "derived_effect", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Aaffine Bound Interface",
        markdown_table(data["aaffine_interface"], ["interface_id", "quantity", "definition", "current_status", "notes", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source-Zero Status",
        markdown_table(data["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This one is not a miracle checkpoint, but it is useful physics hygiene. We now know exactly why the affine source cannot be zeroed yet: not because the idea is vague, but because the parent package still permits marker quotient extensions and invariant generators. That means the honest route is either a later generator-by-generator proof, or explicit `A_affine` scoring. For derivation momentum, the next better punch is the coupling-chain double-zero law.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "primitive_minimality": primitive_minimality_rows(),
        "invariant_algebra": invariant_algebra_rows(),
        "constant_source": constant_source_rows(),
        "aaffine_interface": aaffine_interface_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["primitive_minimality"], data["primitive_minimality"])
    write_csv(OUTPUTS["invariant_algebra"], data["invariant_algebra"])
    write_csv(OUTPUTS["constant_source"], data["constant_source"])
    write_csv(OUTPUTS["aaffine_interface"], data["aaffine_interface"])
    write_csv(OUTPUTS["source_zero"], data["source_zero"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2609_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()
