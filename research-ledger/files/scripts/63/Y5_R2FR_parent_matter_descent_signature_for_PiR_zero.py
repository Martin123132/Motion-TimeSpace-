from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1635"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md"

SOURCE_FILES = {
    "1634_doc": ROOT / "1634-Y5-R2FR-massless-tail-PPN-envelope-or-zero-mode-proof.md",
    "1634_validation": OUT / "P8_Y5_BRR545_1634_VALIDATION.csv",
    "1634_next": OUT / "P8_Y5_PARENT_QLOC_1634_NEXT_TARGET.csv",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "10_observer_map": ROOT / "10-observer-map-symplectic-contract.md",
    "1575_rab_descent": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1575_mds_csv": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
    "1628_source_owner": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
    "1628_certificate_csv": OUT / "P8_Y5_PARENT_QLOC_1628_SOURCE_OWNER_CERTIFICATE_ATTEMPT.csv",
    "760_quotient_descent": ROOT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
    "760_attempt_csv": OUT / "P8_Y5_R10_760_QUOTIENT_DESCENT_PROOF_ATTEMPT.csv",
    "410_functor": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
    "1045_matter_functor": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
    "1309_counterexamples": ROOT / "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual.md",
    "898_trace_descent": ROOT / "898-Y5-R10-trace-vertical-generator-matter-descent-signature-or-residual-vector.md",
}

NEEDLES = {
    "1634_doc": [
        "NEXT_1635_PARENT_MATTER_DESCENT_SIGNATURE_FOR_PIR_ZERO",
        "Q_R=0 -> GR-safe R_AB sector",
    ],
    "1634_validation": ["VAL1634_OVERALL", "PASS"],
    "1634_next": [
        "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md",
        "do not infer Pi_R=0",
    ],
    "06_source_neutrality": ["Q_R = -Pi_R", "Pi_R = 0 -> Q_R = 0"],
    "10_observer_map": ["R_AB = ln(T^2 S) = 2 ln(J_q).", "derive R_AB=0 from the parent theory"],
    "1575_rab_descent": [
        "exact beta-zero theorem survives",
        "Matter Descent Signature",
        "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED",
    ],
    "1575_mds_csv": [
        "MDS1575_0_action_form",
        "MDS1575_4_boundary",
        "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED",
    ],
    "1628_source_owner": ["PIR_ZERO_NOT_PARENT_SIGNED", "source-owner route gives a narrow conditional win"],
    "1628_certificate_csv": [
        "SOC1628_5_PiR_boundary",
        "PIR_ZERO_NOT_PARENT_SIGNED",
        "EXACT_CONTRACT_NOT_PARENT_SIGNED",
    ],
    "760_quotient_descent": ["QMD760_0_descent_equivalence", "quotient_matter_descent_not_parent_signed"],
    "760_attempt_csv": [
        "QMD760_0_descent_equivalence",
        "QMD760_5_boundary_projection",
        "quotient_matter_descent_not_parent_signed",
    ],
    "410_functor": ["delta S_matter / delta Z_I | e_obs = 0", "conditional_theorem_not_parent_derivation"],
    "1045_matter_functor": [
        "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
        "MFS1045_0_parent_field_quotient",
    ],
    "1309_counterexamples": ["QCE1309_0_hidden_alpha", "CG1309_0_qc_zero"],
    "898_trace_descent": [
        "S_matter[Phi,Psi]=Sbar_matter[q_loc(Phi),Psi,theta]",
        "This is the coupling bottleneck",
    ],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1635_SOURCE_REGISTER.csv"
PIR_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1635_PIR_ZERO_THEOREM_CONTRACT.csv"
DESCENT_GATE = OUT / "P8_Y5_PARENT_QLOC_1635_MATTER_DESCENT_SIGNATURE_GATE.csv"
COUNTEREXAMPLES = OUT / "P8_Y5_PARENT_QLOC_1635_COUNTEREXAMPLE_LEDGER.csv"
PIR_RESIDUAL = OUT / "P8_Y5_PARENT_QLOC_1635_PIR_RESIDUAL_ENVELOPE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1635_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1635_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1635_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1635_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PIR_THEOREM,
    DESCENT_GATE,
    COUNTEREXAMPLES,
    PIR_RESIDUAL,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PIR_THEOREM,
    DESCENT_GATE,
    COUNTEREXAMPLES,
    PIR_RESIDUAL,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(PIR_THEOREM, QUEUE / "JR1635_PIR_ZERO_THEOREM_CONTRACT_NONCLAIM.csv")
    shutil.copy2(PIR_RESIDUAL, QUEUE / "JR1635_PIR_RESIDUAL_ENVELOPE_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1635_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": key,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1635 Pi_R zero theorem / matter descent signature input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def pir_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_0_boundary_relation",
            "statement": "Q_R=-Pi_R",
            "status": "SOURCE_RELATION_STAGED",
            "proof_role": "connects source boundary reciprocal momentum to exterior reciprocal hair",
            "missing_for_promotion": "Pi_R=0 theorem or sourced Pi_R envelope",
            "source_basis": str(SOURCE_FILES["06_source_neutrality"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_1_chain_rule_bulk",
            "statement": "if v_R in ker(Dq) and S_matter=Sbar[q(Phi),Psi,theta], then delta_{v_R} S_matter_bulk=0",
            "status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "proof_role": "bulk source charge cannot see a pure quotient representative direction",
            "missing_for_promotion": "parent-signed q, v_R, observed coframe, matter functor, and theta invariance",
            "source_basis": str(SOURCE_FILES["410_functor"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_2_boundary_momentum",
            "statement": "Pi_R=i_{v_R}Theta_matter[worldtube]+delta_{v_R}B_matter, so Pi_R=0 only for proper/exact/zero-projection boundary variation",
            "status": "BOUNDARY_CONDITION_REQUIRED",
            "proof_role": "prevents a symmetry of the bulk from hiding a nonzero edge/source momentum",
            "missing_for_promotion": "parent-signed compact-support/proper boundary silence or an absolute Pi_R tail bound",
            "source_basis": str(SOURCE_FILES["1575_mds_csv"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_3_source_owner",
            "statement": "a common pre-readout Hilbert matter action blocks post-variation source rescaling but not pre-action R_AB weights",
            "status": "NARROW_CONDITIONAL_WIN",
            "proof_role": "rules out one class of source cheats after the common action is fixed",
            "missing_for_promotion": "no direct R_AB argument, no pre-action source weights, and no hidden/source/domain/boundary tails",
            "source_basis": str(SOURCE_FILES["1628_certificate_csv"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_4_result_if_all_signed",
            "statement": "v_R vertical + matter/constant/no-marker descent + proper boundary silence => Pi_R=0 => Q_R=0 => R_AB=0 under infinity condition",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PROMOTED",
            "proof_role": "this is the wanted GR-safe reciprocal-hair theorem",
            "missing_for_promotion": "every required parent signature remains unsigned in current corpus",
            "source_basis": str(SOURCE_FILES["1575_rab_descent"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PIRZ1635_5_verdict",
            "statement": "Pi_R zero theorem",
            "status": "PIR_ZERO_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_role": "blocks promotion of local GR/Newton recovery from the R_AB sector",
            "missing_for_promotion": "parent object-language/quotient certificate or explicit Pi_R residual bound pack",
            "source_basis": "1635 synthesis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def descent_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_0_verticality",
            "required_clause": "v_R in ker(Dq) or R_AB eliminated by parent constraint/no-pole before matter variation",
            "current_status": "BLOCKED_VERTICALITY_NOT_SIGNED",
            "evidence": "1575 says R_AB is coframe-visible unless quotient/constraint route removes it",
            "if_signed": "bulk matter derivative can be evaluated as a pure representative variation",
            "if_unsigned": "R_AB remains a physical local/PPN residual channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_1_parent_quotient",
            "required_clause": "q:Phi_parent->Q_MTS exists before ordinary matter action/readout",
            "current_status": "CONTRACT_ONLY",
            "evidence": "760/410 provide quotient-descent criterion, not parent construction",
            "if_signed": "matter-descent theorem has a domain",
            "if_unsigned": "vertical language is closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_2_matter_functor",
            "required_clause": "S_matter=sum_A Sbar_A[Psi_A,e_obs(q(Phi)),omega(e_obs),theta_A]+dB_A",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "1575/1045 write the action-form contract but do not derive it",
            "if_signed": "bulk delta_{v_R}S_matter vanishes by chain rule when Dq[v_R]=0",
            "if_unsigned": "direct R_AB matter argument remains legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_3_geometry_stack",
            "required_clause": "matter measure, coframe/metric, spin connection, and derivative operator all descend through q",
            "current_status": "GEOMETRY_STACK_UNSIGNED",
            "evidence": "760 and 898 keep measure/coframe/connection descent unsigned",
            "if_signed": "representative Weyl/disformal leakage closes",
            "if_unsigned": "rod/clock/derivative frame leakage can source Pi_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_4_constants_no_marker",
            "required_clause": "Lie_{v_R}theta_A=0 and no marker/source/readout coefficient depends on R_AB",
            "current_status": "NO_MARKER_CONSTANT_OWNER_UNSIGNED",
            "evidence": "1309 counterexamples keep alpha, mass, markers, and source weights legal",
            "if_signed": "constant/material/source beta channels vanish",
            "if_unsigned": "hidden constants can generate composition, clock, EM, and WEP residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_5_source_owner",
            "required_clause": "one common pre-readout matter action owns the Hilbert source and forbids source-only/pre-action weights",
            "current_status": "PARTIAL_CONDITIONAL_PRE_ACTION_LEAK_SURVIVES",
            "evidence": "1628 kills only post-variation rescaling once common-action premises are fixed",
            "if_signed": "source-current normalization cannot hide Pi_R",
            "if_unsigned": "w_A(R_AB)S_A and reciprocal source prefactors remain legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_6_boundary_projection",
            "required_clause": "vertical boundary/worldtube/readout terms are proper, exact, zero projection, or explicitly bounded",
            "current_status": "PIR_BOUNDARY_ZERO_UNSIGNED",
            "evidence": "1575/1628 name boundary Pi_R as the missing piece",
            "if_signed": "Pi_R=0 can be promoted after bulk descent closes",
            "if_unsigned": "nonzero Pi_R keeps Q_R/r hair alive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MDSG1635_7_all_clauses",
            "required_clause": "all descent, no-marker, source-owner, and boundary clauses close together",
            "current_status": "PIR_ZERO_STACK_NOT_CLOSED_CURRENT_CORPUS",
            "evidence": "1635 synthesis of 410/760/1575/1628/1309/1045/898",
            "if_signed": "Pi_R=0 and Q_R=0 become a parent theorem",
            "if_unsigned": "stage Pi_R residual envelope and keep local GR blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def counterexample_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_0_physical_RAB",
            "legal_if_unsigned": "R_AB remains an observed coframe/metric residual rather than a representative fibre coordinate",
            "residual_opened": "q_R PPN/local metric residual",
            "blocked_by": "parent-signed v_R in ker(Dq) or nonpropagating constraint/no-pole theorem",
            "source_basis": str(SOURCE_FILES["10_observer_map"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_1_direct_RAB_matter_argument",
            "legal_if_unsigned": "S_matter[Psi,e_obs,q,R_AB] contains an independent R_AB argument",
            "residual_opened": "Pi_R bulk matter source",
            "blocked_by": "ordinary matter functor has no independent R_AB representative argument",
            "source_basis": str(SOURCE_FILES["1628_certificate_csv"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_2_hidden_frame",
            "legal_if_unsigned": "matter sees A_R(R_AB)^2 e_obs or a disformal/connection shadow frame",
            "residual_opened": "WEP, clock, PPN, and R10-like frame leakage",
            "blocked_by": "geometry-stack descent and no-shadow-frame theorem",
            "source_basis": str(SOURCE_FILES["760_attempt_csv"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_3_constants_markers",
            "legal_if_unsigned": "alpha_EM, mass ratios, clock standards, isotope/material labels, or binding terms depend on R_AB",
            "residual_opened": "composition, EM, clock, and source/test charge residuals",
            "blocked_by": "constant superselection and no-marker theorem",
            "source_basis": str(SOURCE_FILES["1309_counterexamples"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_4_source_only_weight",
            "legal_if_unsigned": "relative source prefactor w_A(R_AB)S_A is inserted before variation",
            "residual_opened": "Hilbert source normalization and Pi_R source charge",
            "blocked_by": "parent action object-language excluding pre-action source-only weights",
            "source_basis": str(SOURCE_FILES["1628_source_owner"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_5_boundary_worldtube",
            "legal_if_unsigned": "boundary/worldtube/readout term B_R[R_AB] has nonzero local projection",
            "residual_opened": "Pi_R boundary momentum and Q_R/r hair",
            "blocked_by": "proper/exact/zero-projection boundary certificate or absolute bound",
            "source_basis": str(SOURCE_FILES["1575_mds_csv"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1635_6_post_readout_EFT",
            "legal_if_unsigned": "radiative/readout EFT terms reintroduce R_AB after the bare matter action is quotient-silent",
            "residual_opened": "clock, EM, WEP, and local force residuals",
            "blocked_by": "readout-after-variation closure plus radiative no-extension theorem",
            "source_basis": str(SOURCE_FILES["1309_counterexamples"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def pir_residual_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_0_verticality",
            "quantity": "Pi_R_vertical_abs",
            "symbolic_envelope": "|Pi_R_vertical| from Dq[v_R] != 0 or observed coframe response",
            "status": "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
            "arena_links": "PPN;local_GR;Newton;clock;WEP",
            "next_action": "source parent q/v_R certificate or coefficient bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_1_geometry_stack",
            "quantity": "Pi_R_geometry_abs",
            "symbolic_envelope": "|delta_R e_m|+|delta_R omega_m|+|delta_R D_m| weighted by matter stress/spin currents",
            "status": "MISSING_GEOMETRY_STACK_BOUND",
            "arena_links": "PPN;clock;WEP;orbital",
            "next_action": "derive stack descent or acquire frame-leak bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_2_constants_markers",
            "quantity": "Pi_R_constants_abs",
            "symbolic_envelope": "|partial_R alpha|+sum_A|partial_R ln m_A|+marker/source-label terms",
            "status": "MISSING_CONSTANT_MARKER_ZERO_OR_VALUES",
            "arena_links": "EM;clock;WEP;R10;local_GR",
            "next_action": "prove no-marker constant owner or source residual coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_3_source_weight",
            "quantity": "Pi_R_source_weight_abs",
            "symbolic_envelope": "sum_A |partial_R w_A| |S_A| or equivalent source-only prefactor",
            "status": "MISSING_NO_SOURCE_WEIGHT_THEOREM",
            "arena_links": "Newton_GM;WEP;R10;orbital",
            "next_action": "derive source-label forgetting/no-pre-action-weight clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_4_boundary",
            "quantity": "Pi_R_boundary_abs",
            "symbolic_envelope": "|i_{v_R}Theta_matter[worldtube]+delta_{v_R}B_matter| projected to local source",
            "status": "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL",
            "arena_links": "local_GR;PPN;R10;orbital",
            "next_action": "derive proper boundary silence or acquire tail bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_5_readout_EFT",
            "quantity": "Pi_R_readout_abs",
            "symbolic_envelope": "absolute retained radiative/readout/post-variation R_AB sensitivity",
            "status": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "arena_links": "clock;EM;WEP;local_GR",
            "next_action": "derive readout closure or retain as residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_6_total",
            "quantity": "Pi_R_abs_total",
            "symbolic_envelope": "Pi_R_abs_total <= sum of verticality, geometry, constants, source-weight, boundary, and readout absolute pieces",
            "status": "TOTAL_TEMPLATE_NONCLAIM_MISSING_COMPONENTS",
            "arena_links": "local_GR;Newton;PPN;WEP;clock;EM;R10;orbital",
            "next_action": "either theorem-zero all pieces or fill source-backed component bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRRES1635_7_qR_link",
            "quantity": "q_R / Delta gamma",
            "symbolic_envelope": "Q_R=-Pi_R and R_AB=q_R L_N imply Delta gamma ~= q_R after a missing local normalization N_R is supplied",
            "status": "LOCAL_PPN_LINK_SYMBOLIC_ONLY",
            "arena_links": "PPN;local_GR;Newton",
            "next_action": "derive N_R and q_R amplitude law, or prove Pi_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1635_0_theorem_shape",
            "decision": "PIR_ZERO_THEOREM_SHAPE_VALID",
            "reason": "chain-rule matter descent plus proper boundary silence would force Pi_R=0 and Q_R=0",
            "next_action": "do not lose this theorem; make the missing parent signatures explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1635_1_current_status",
            "decision": "PIR_ZERO_NOT_PARENT_SIGNED",
            "reason": "verticality, parent quotient, matter functor, constants/no-marker, source-owner, and boundary projection are not jointly signed",
            "next_action": "no local-GR/Newton/PPN claim from R_AB sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1635_2_best_route",
            "decision": "NEXT_1636_RAB_PARENT_OBJECT_LANGUAGE_OR_PIR_RESIDUAL_BOUND_PACK",
            "reason": "matter descent alone cannot close while R_AB verticality/object-language and boundary properness are unsigned",
            "next_action": "try to derive the parent action object-language that excludes independent R_AB matter/source slots; otherwise build Pi_R residual bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1635_0_PiR_zero",
            "claim": "Pi_R=0 theorem",
            "status": "BLOCKED",
            "blocker": "parent descent stack and boundary projection are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1635_1_QR_zero",
            "claim": "Q_R=0 reciprocal hair removal",
            "status": "BLOCKED",
            "blocker": "Q_R=-Pi_R only helps after Pi_R=0 closes",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1635_2_local_GR",
            "claim": "local GR/Newton recovery",
            "status": "BLOCKED",
            "blocker": "q_R residual envelope remains symbolic and unbounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1635_3_PPN",
            "claim": "PPN pass",
            "status": "BLOCKED",
            "blocker": "Delta gamma ~= q_R has no zero theorem or numeric amplitude",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1635_4_R10",
            "claim": "R10 branch",
            "status": "BLOCKED",
            "blocker": "massless R_AB tail remains not a finite-lambda R10 object",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
            "script": "scripts/Y5_R2FR_RAB_parent_object_language_or_PiR_residual_bound_pack.py",
            "objective": "derive the parent action object-language/quotient certificate that makes R_AB a proper representative direction with no independent matter/source/boundary slot; if not, build source-ready Pi_R residual bound rows",
            "success_condition": "either the R_AB object-language closes verticality, matter descent, no-marker/source-owner, and boundary silence together, or Pi_R_abs_total is decomposed into explicit nonclaim bound-input rows",
            "guardrails": "do not claim Pi_R=0 from bulk descent alone, do not ignore boundary/worldtube terms, do not use R10 for Q_R/r, do not claim local GR until Q_R or q_R closes",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: Iterable[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for field in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if field in row and row[field] != "False":
                    return False
    return True


def validation_rows() -> list[dict[str, object]]:
    source_rows = source_register_rows()
    gate_ids = {row["gate_id"] for row in descent_gate_rows()}
    counterexample_ids = {row["counterexample_id"] for row in counterexample_rows()}
    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1635_0_sources_exist",
            all(row["path_exists"] for row in source_rows),
            "all cited 1635 source paths exist",
        ),
        (
            "VAL1635_1_needles_found",
            all(row["needles_found"] for row in source_rows),
            "all required 1635 source needles found",
        ),
        (
            "VAL1635_2_conditional_theorem",
            any(row["status"] == "PIR_ZERO_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED" for row in pir_theorem_rows()),
            "Pi_R zero theorem is conditional and not promoted",
        ),
        (
            "VAL1635_3_boundary_required",
            any(row["gate_id"] == "MDSG1635_6_boundary_projection" for row in descent_gate_rows()),
            "boundary/properness clause is required explicitly",
        ),
        (
            "VAL1635_4_gate_coverage",
            gate_ids
            == {
                "MDSG1635_0_verticality",
                "MDSG1635_1_parent_quotient",
                "MDSG1635_2_matter_functor",
                "MDSG1635_3_geometry_stack",
                "MDSG1635_4_constants_no_marker",
                "MDSG1635_5_source_owner",
                "MDSG1635_6_boundary_projection",
                "MDSG1635_7_all_clauses",
            },
            "descent gate covers verticality, quotient, matter, geometry, constants, source owner, and boundary",
        ),
        (
            "VAL1635_5_counterexamples",
            counterexample_ids
            == {
                "CE1635_0_physical_RAB",
                "CE1635_1_direct_RAB_matter_argument",
                "CE1635_2_hidden_frame",
                "CE1635_3_constants_markers",
                "CE1635_4_source_only_weight",
                "CE1635_5_boundary_worldtube",
                "CE1635_6_post_readout_EFT",
            },
            "counterexample ledger includes direct, hidden, marker, source-weight, boundary, and readout leaks",
        ),
        (
            "VAL1635_6_residual_total",
            any(row["quantity"] == "Pi_R_abs_total" for row in pir_residual_rows()),
            "Pi_R residual envelope includes total no-cancellation row",
        ),
        (
            "VAL1635_7_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gate_rows()),
            "all 1635 claim gates remain blocked",
        ),
        (
            "VAL1635_8_next_target_selected",
            next_target_rows()[0]["next_target"] == "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
            "next target selects parent object-language or Pi_R residual bound pack",
        ),
        (
            "VAL1635_9_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1635 CSVs parse",
        ),
        (
            "VAL1635_10_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1635 generated decision rows remain nonclaim",
        ),
        (
            "VAL1635_11_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1635_12_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1635_PIR_ZERO_THEOREM_CONTRACT_NONCLAIM.csv",
                    QUEUE / "JR1635_PIR_RESIDUAL_ENVELOPE_NONCLAIM.csv",
                    QUEUE / "JR1635_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1635_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1635_14_formalization_untouched",
            not any(FORMALIZATION.rglob("*1635*")) if FORMALIZATION.exists() else True,
            "no 1635 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1635_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1635 parent matter descent signature for Pi_R zero validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    theorem_rows = csv_rows(PIR_THEOREM)
    gate_rows = csv_rows(DESCENT_GATE)
    counterexamples = csv_rows(COUNTEREXAMPLES)
    residuals = csv_rows(PIR_RESIDUAL)
    decisions = csv_rows(DECISION)
    claims = csv_rows(CLAIM_GATE)
    next_rows = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1635 — Parent Matter Descent Signature For Pi_R Zero

**Private status:** nonclaim checkpoint. No `Pi_R=0`, `Q_R=0`, local-GR, Newton, PPN, WEP, clock, orbital, EM, or R10 pass is claimed.

## Verdict

The proof shape is good but not closed. If `R_AB` is a proper quotient-representative direction and ordinary matter descends through the quotient with silent constants, no hidden source weights, and zero/proper boundary variation, then:

```text
delta_vR S_matter = 0
Pi_R = 0
Q_R = -Pi_R = 0
R_AB = 0 under R_AB(infinity)=0
```

But the current parent corpus does **not** jointly sign the required object-language, verticality, matter functor, no-marker/source-owner, and boundary clauses. Bulk chain-rule descent alone is not enough: a boundary/worldtube `Pi_R` can still carry the reciprocal hair. The next route is therefore upstream: derive the parent action object-language that forbids independent `R_AB` matter/source/boundary slots, or stage explicit `Pi_R` residual bounds.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Pi_R Zero Theorem Contract

{markdown_table(theorem_rows, ["theorem_id", "statement", "status", "proof_role", "missing_for_promotion"])}

## Matter Descent Signature Gate

{markdown_table(gate_rows, ["gate_id", "required_clause", "current_status", "evidence", "if_unsigned"])}

## Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "legal_if_unsigned", "residual_opened", "blocked_by"])}

## Pi_R Residual Envelope

{markdown_table(residuals, ["row_id", "quantity", "symbolic_envelope", "status", "arena_links", "next_action"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claims, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        PIR_THEOREM: pir_theorem_rows(),
        DESCENT_GATE: descent_gate_rows(),
        COUNTEREXAMPLES: counterexample_rows(),
        PIR_RESIDUAL: pir_residual_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
