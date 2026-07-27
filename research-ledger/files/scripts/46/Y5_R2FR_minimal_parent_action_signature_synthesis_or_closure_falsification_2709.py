from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2709"
BRANCH_ID = "Y5_R2FR_MINIMAL_PARENT_ACTION_SIGNATURE_SYNTHESIS_OR_CLOSURE_FALSIFICATION_2709"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2709-Y5-R2FR-minimal-parent-action-signature-synthesis-or-closure-falsification.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2709_SOURCE_REGISTER.csv",
    "candidate_signatures": RESIDUALS / "P8_Y5_R2FR_2709_MINIMAL_PARENT_SIGNATURE_CANDIDATES.csv",
    "theorem_target": RESIDUALS / "P8_Y5_R2FR_2709_PARENT_SIGNATURE_THEOREM_TARGET.csv",
    "clause_audit": RESIDUALS / "P8_Y5_R2FR_2709_CLAUSE_AUDIT.csv",
    "falsifier_ledger": RESIDUALS / "P8_Y5_R2FR_2709_FALSIFIER_LEDGER.csv",
    "reentry_rules": RESIDUALS / "P8_Y5_R2FR_2709_REENTRY_RULES.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2709_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2709_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2709_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2709_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2709_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_clause_audit": LOCAL_BOUNDS / "minimal_parent_signature_clause_audit_2709_NONCLAIM.csv",
    "source_weight_candidate": SOURCE_WEIGHT / "MINIMAL_PARENT_SIGNATURE_CANDIDATE_2709_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2709_PARENT_SIGNATURE_SOURCE_HUNT_OR_FALSIFIER_TEST_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2709_2708_HANDOFF",
        "relative_path": "2708-Y5-R2FR-parent-quotient-no-pole-certificate-or-closure-reentry.md",
        "required_needles": ["LGR2708_0_name", "CG2708_0_certificate", "NEXT2708_0_selected"],
        "purpose": "imports the exact local-GR re-entry axiom and 2709 handoff",
    },
    {
        "source_id": "SRC2709_423_NO_EXTENSION",
        "relative_path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "required_needles": ["parent_universal_property_derived", "material_marker_extension_blocked", "Q_tilde=(Q,m)/G_rel"],
        "purpose": "imports no-extension failure and legal material-marker countermodel",
    },
    {
        "source_id": "SRC2709_622_MATTER_CONTRACT",
        "relative_path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
        "required_needles": ["PMC622_0_parent_split", "PMC622_8_contract_verdict", "residual-prior smoke runner"],
        "purpose": "imports the parent matter-sector split and residual-prior discipline",
    },
    {
        "source_id": "SRC2709_624_COFRAME",
        "relative_path": "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
        "required_needles": ["SIG624_0_parent_quotient", "SIG624_7_signature_verdict", "c_g=d ln A_g/dXhat"],
        "purpose": "imports observed coframe factorization and common-frame leakage gate",
    },
    {
        "source_id": "SRC2709_626_DESCENT",
        "relative_path": "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "required_needles": ["QIM626_0_descent_equivalence", "QIM626_5_signature_verdict", "quotient_invariant_matter_action_signed"],
        "purpose": "imports quotient-invariant matter-action descent criterion",
    },
    {
        "source_id": "SRC2709_990_PARENT_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "required_needles": ["PAC990_0_parent_fields_and_quotient", "PAC990_5_Ward_Bianchi", "PAC990_6_PPN_readout"],
        "purpose": "imports parent action and GR/Newton/PPN requirements",
    },
    {
        "source_id": "SRC2709_990_REENTRY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv",
        "required_needles": ["LAD990_1_operator", "LAD990_2_source_mass", "LAD990_4_PPN"],
        "purpose": "imports the weak-field re-entry ladder",
    },
    {
        "source_id": "SRC2709_1087_DESCENT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
        "required_needles": ["PMD1087_0_target", "PMD1087_5_hidden_domain_boundary", "PMD1087_6_verdict"],
        "purpose": "imports parent matter descent blockers",
    },
    {
        "source_id": "SRC2709_1087_ZERO_CURRENT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
        "required_needles": ["ZCC1087_0_object_language", "ZCC1087_2_variation_order", "ZCC1087_4_constant_superselection"],
        "purpose": "imports zero-current parent contracts",
    },
    {
        "source_id": "SRC2709_1088_MOMS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
        "required_needles": ["MOMS1088_0_action_form", "MOMS1088_6_no_shadow_domain", "MOMS1088_7_verdict"],
        "purpose": "imports minimal ordinary-matter signature clauses",
    },
    {
        "source_id": "SRC2709_1088_THEOREM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
        "required_needles": ["THM1088_1_visible_fields", "THM1088_5_conclusion", "THM1088_6_current_corpus_verdict"],
        "purpose": "imports conditional qbar_XT/J_matter zero theorem",
    },
    {
        "source_id": "SRC2709_1088_COUNTERS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
        "required_needles": ["CM1088_0_species_weight", "CM1088_2_shadow_frame", "CM1088_4_boundary_domain_marker"],
        "purpose": "imports retained matter countermodels",
    },
    {
        "source_id": "SRC2709_2158_SOURCE_ZERO",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_PREMISE_GATE.csv",
        "required_needles": ["SPG2158_0_vertical_kernel", "SPG2158_6_boundary_domain_silence", "SPG2158_7_verdict"],
        "purpose": "imports local source-zero premise gate",
    },
    {
        "source_id": "SRC2709_991_GUARD",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_991_THEOREM_ROUTE_AUDIT.csv",
        "required_needles": ["HPT991_5_representative_zero_not_enough", "HPT991_6_coupling_descent", "HPT991_7_verdict"],
        "purpose": "imports representative-zero overcredit guard",
    },
    {
        "source_id": "SRC2709_2106_NO_POLE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2106_NO_POLE_RETURN_LEDGER.csv",
        "required_needles": ["NPR2106_1_no_pole_route", "NPR2106_3_required_certificate", "NPR2106_4_fallback_if_fails"],
        "purpose": "imports no-pole/source-zero route and fallback",
    },
    {
        "source_id": "SRC2709_1082_UNITS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv",
        "required_needles": ["CUC1082_3_C_parent", "MISSING_PARENT_COEFFICIENT_VECTOR", "MISSING_FOR_CLAIM"],
        "purpose": "imports coefficient/source-readout nonclaim status for finite fallback",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def candidate_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "MPS2709_A_strict_quotient_EH_topological_vertical",
            "candidate_status": "COHERENT_THEOREM_TARGET_NOT_SIGNED",
            "parent_action_skeleton": "S_parent=S_EH[g_obs(q(Phi))]+S_GHY+S_top[V,lambda]+S_constraint[Dq[V]=0,deg(V)=0]+sum_A S_A[Psi_A,E(q(Phi)),Omega(E),A_obs(q(Phi)),theta_A]+B_exact",
            "owned_objects": "q:Phi->Q_obs; V=ker(Dq); E(q); Omega(E); A_obs(q); theta_A; boundary class; source charge H_tau",
            "intended_zero_route": "V is quotient-vertical/topological/constrained, ordinary matter descends through q, boundary/projector tails vanish or are retained, so C_X and qbar_XT are zero only if every clause is parent-signed",
            "why_minimal": "keeps one observed metric/coframe, EH weak-field core, no matter-visible representative frame, and routes every extra local variable into gauge/topological/constraint/residual status",
            "current_corpus_fit": "matches 2708/LGR closure axiom and 990/1088 contracts, but the action and degree count are not extracted from a parent derivation",
            "hard_contradiction_found": "false",
            "promotion_status": "not_promoted_closure_axiom_remains_explicit",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "candidate_id": "MPS2709_B_primitive_minimal_no_marker_parent",
            "candidate_status": "STRONGER_NO_EXTENSION_TARGET_UNSIGNED",
            "parent_action_skeleton": "same as A plus primitive-minimal object language: allowed local action terms are natural functions only of Q_obs, observed bundles, gauge data, and universal constants",
            "owned_objects": "free/minimal quotient object Q_obs and a proof that no nonconstant material marker functor exists",
            "intended_zero_route": "kills species weights, shadow frames, marker domains, and variable constants by parent grammar rather than by empirical smallness",
            "why_minimal": "would make MTS less like a patchwork EFT by forbidding extra sectors before they appear",
            "current_corpus_fit": "423 explicitly says universal-property/no-natural-marker theorem is not derived; Q_tilde=(Q,m)/G_rel remains legal",
            "hard_contradiction_found": "false",
            "promotion_status": "not_promoted_no_extension_closure_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "candidate_id": "MPS2709_C_finite_residual_reentry_fallback",
            "candidate_status": "NON_DERIVATION_FALLBACK_ONLY",
            "parent_action_skeleton": "retain finite R11/R10/WEP/clock/orbital residual operators with sourced coefficients and arena projections",
            "owned_objects": "Z_X; M_X^2; J_X; Qbar_XH(lambda); qbar_XT; K_X; tau_arena; source paths; units",
            "intended_zero_route": "none; this scores finite residuals only after real coefficients and local bounds are sourced",
            "why_minimal": "not a GR-reduction proof, but prevents false closure if A/B fail",
            "current_corpus_fit": "consistent with 2106 fallback and 1082 missing parent coefficient vector",
            "hard_contradiction_found": "false",
            "promotion_status": "not_promoted_finite_rows_nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def theorem_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "THM2709_0_parent_action",
            "theorem_step": "write one parent branch",
            "required_statement": "There exists one parent action of candidate A with q, V, observed metric/coframe/gauge data, matter functor, boundary class, and H_tau all owned before variation.",
            "if_proven": "local branch has a single arena for GR/Newton/PPN/WEP/R10 rather than stitched closures",
            "current_status": "THEOREM_TARGET_WRITTEN_NOT_DERIVED",
            "missing_for_claim": "explicit L_parent, variation owner, source charge owner, and object language",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "THM2709_1_vertical_no_pole",
            "theorem_step": "remove Xhat from local Hilbert spectrum",
            "required_statement": "For every local X direction, v_X in V=ker(Dq) and the Hessian/symplectic degree count makes V gauge, topological, constrained, or retained; no physical X pole remains.",
            "if_proven": "finite c_g/R10/PPN scoring of the X pole is no longer needed for the strict quotient branch",
            "current_status": "MISSING_DEGREE_COUNT_AND_SYMPLECTIC_OWNER",
            "missing_for_claim": "constraint algebra, presymplectic null proof, and boundary domain class",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "THM2709_2_matter_descent",
            "theorem_step": "derive MOMS from action",
            "required_statement": "Ordinary matter terms depend on v_X only through q(Phi), fixed/gauge lifts, and X-trivial theta_A; no w_A(X), shadow frame, marker, or post-variation selector exists.",
            "if_proven": "J_X^matter=0, qbar_XT=0, common-frame c_g=0, and local WEP/clock/source-current branches become structural zeros",
            "current_status": "CONDITIONAL_ZERO_THEOREM_ONLY",
            "missing_for_claim": "parent matter bundle functor, constant superselection, no-species-weight grammar, no-shadow/domain theorem",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "THM2709_3_boundary_readout",
            "theorem_step": "make representative zero observable",
            "required_statement": "Boundary charges, support shifts, projectors, domain selectors, and non-Hilbert tails vanish by parent theorem or are retained as explicit bounded residuals before any observed claim.",
            "if_proven": "vertical representative silence can be converted into observed local-source silence without overcredit",
            "current_status": "MISSING_BOUNDARY_DOMAIN_SILENCE",
            "missing_for_claim": "boundary flux certificate, readout-before/after variation rule, and source support projection",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "THM2709_4_weak_field_reentry",
            "theorem_step": "recover GR/Newton",
            "required_statement": "The observed field equation is EH-only in the local branch, with selected Hamiltonian source charge H_tau, giving Poisson/Newton and PPN gamma=beta=1, alpha_i=xi=0, no Gdot, and no finite-range residue.",
            "if_proven": "this is the real local-GR/Newton pass rather than a plateau axiom",
            "current_status": "NOT_REACHED",
            "missing_for_claim": "EH-only/R11 decision, measured GM source equality, PPN residual vector, and finite-range bound ledger",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "AUD2709_0_qmap",
            "candidate_clause": "parent-owned q:Phi->Q_obs",
            "source_support": "2708 LGR; 990 PAC990_0; 624 SIG624_0",
            "audit_result": "COHERENT_BUT_NOT_PARENT_SIGNED",
            "blocks_claim_if_missing": "no common observed arena",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_1_vertical_kernel",
            "candidate_clause": "local v_X belongs to V=ker(Dq)",
            "source_support": "2158 SPG2158_0; 1088 THM1088_1",
            "audit_result": "CONDITIONAL_ONLY",
            "blocks_claim_if_missing": "geometry/source-current chain-rule zero is not usable",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_2_action_descent",
            "candidate_clause": "S_parent has no local Hilbert dependence on V except topological/constraint/exact pieces",
            "source_support": "2708 LGR2708_1; 2106 NPR2106_1; 991 HPT991_0",
            "audit_result": "MISSING_PARENT_LAGRANGIAN_AND_DEGREE_COUNT",
            "blocks_claim_if_missing": "Xhat may be a physical finite pole",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_3_matter_functor",
            "candidate_clause": "S_matter=sum_A S_A[Psi_A,E(q),Omega(E),A_obs(q),theta_A]",
            "source_support": "622 PMC622_0; 626 QIM626_0; 1088 MOMS1088_0",
            "audit_result": "EXACT_CONTRACT_NOT_DERIVED",
            "blocks_claim_if_missing": "qbar_XT and WEP/current channels remain active",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_4_no_marker_no_weight",
            "candidate_clause": "no w_A(X), source-only multiplier, marker, shadow frame, or variable theta_A",
            "source_support": "423 no-extension failure; 1087 ZCC; 1088 countermodels",
            "audit_result": "UNSIGNED_AND_COUNTERMODELS_RETAINED",
            "blocks_claim_if_missing": "species weights, variable constants, and marker domains survive",
            "candidate_A_survives": "true_but_only_as_closure",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_5_boundary_domain",
            "candidate_clause": "boundary/support/domain/projector tails are zero or retained",
            "source_support": "626 QIM626_4; 2158 SPG2158_6; 991 HPT991_5",
            "audit_result": "MISSING_BOUNDARY_DOMAIN_CERTIFICATE",
            "blocks_claim_if_missing": "representative zero cannot become observed zero",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_6_Ward_Bianchi",
            "candidate_clause": "all selectors/boundaries/hidden variables are varied, on shell, topological, or retained",
            "source_support": "990 PAC990_5",
            "audit_result": "OPEN",
            "blocks_claim_if_missing": "silent Euler leaks can violate conservation",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_7_GR_Newton_readout",
            "candidate_clause": "EH-only observed weak-field operator plus owned H_tau source charge reaches GR/Newton/PPN",
            "source_support": "990 PAC990_1/PAC990_4/PAC990_6; LAD990_1..4",
            "audit_result": "NOT_REACHED",
            "blocks_claim_if_missing": "local-GR/Newton remains unproven even if source-zero theorem improves",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2709_8_verdict",
            "candidate_clause": "all clauses close in one parent action signature",
            "source_support": "2709 integrated audit",
            "audit_result": "CANDIDATE_SURVIVES_AS_THEOREM_TARGET_CERTIFICATE_NOT_CLOSED",
            "blocks_claim_if_missing": "LGR2708 remains closure axiom; no C_X/qbar_XT/local-GR claim",
            "candidate_A_survives": "true",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def falsifier_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "falsifier_id": "FAL2709_0_no_single_parent_owner",
            "possible_falsifier": "no explicit parent Lagrangian/variation owner signs q, V, matter, boundary, and H_tau together",
            "falsifies": "current local-GR theorem claim, not candidate A as a future theorem target",
            "evidence": "990 PAC clauses open; 2708 certificate not closed; 991 parent L owner not signed",
            "response": "keep LGR2708 explicit; next step must source or write the parent action owner",
            "status": "ACTIVE_BLOCKER",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_1_material_marker_extension",
            "possible_falsifier": "Q_tilde=(Q,m)/G_rel legal extended parent with material marker m",
            "falsifies": "primitive-minimal no-marker proof",
            "evidence": "423 says material_marker_extension_blocked fails and no-natural-marker theorem is not derived",
            "response": "derive universal-property/no-natural-marker theorem or retain marker residual tax",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_2_species_or_source_weights",
            "possible_falsifier": "S_matter -> sum_A w_A(X) S_A",
            "falsifies": "matter source-zero without MOMS",
            "evidence": "1088 CM1088_0 and 2158 SPG2158_4 retain species/source weights",
            "response": "derive object-language/action-measure exclusion or finite source-weight bounds",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_3_variable_constants",
            "possible_falsifier": "theta_A(X) changes masses, charges, alpha_EM, clocks, or representation labels",
            "falsifies": "constant-channel zero theorem",
            "evidence": "1087 ZCC1087_4 and 1088 CM1088_1 retain constant superselection gap",
            "response": "derive constant superselection or retain alpha/mass/clock residual rows",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_4_shadow_or_disformal_frame",
            "possible_falsifier": "matter sees A_A(X)^2 g_obs or disformal/source-only metric data",
            "falsifies": "common-frame c_g=0 and observed coframe factorization",
            "evidence": "624 SIG624_7 not signed; 1088 CM1088_2 retained",
            "response": "derive no representative Weyl/disformal theorem or source c_g/d_g bounds",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_5_boundary_readout_flux",
            "possible_falsifier": "boundary charge, support shift, domain selector, or post-variation readout tail survives",
            "falsifies": "representative zero -> observed zero promotion",
            "evidence": "991 HPT991_5 guard; 2158 SPG2158_6 missing; 626 QIM626_4 unsigned",
            "response": "prove boundary/domain silence or create absolute residual source rows",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "FAL2709_6_non_EH_or_unowned_source_charge",
            "possible_falsifier": "observed weak-field operator is not EH-only or measured GM/H_tau source charge is not owned",
            "falsifies": "GR/Newton re-entry, even if no-pole/source-zero clauses improve",
            "evidence": "990 LAD990_1 operator blocked and LAD990_2 source mass best_live_edge not closed",
            "response": "after parent signature source hunt, attack EH-only/R11 and H_tau source equality",
            "status": "REENTRY_BLOCKER_RETAINED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def reentry_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "RULE2709_0_allowed_language",
            "rule": "Say candidate A is a coherent parent-signature theorem target, not a signed local-GR proof.",
            "forbidden_language": "MTS locally reduces to GR/Newton",
            "replacement_language": "MTS local-GR route requires the MPS2709/LGR2708 parent-signature closure theorem",
            "active": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "rule_id": "RULE2709_1_no_branch_mixing",
            "rule": "Do not combine quotient no-pole/source-zero rows with finite residual coefficients unless the parent action states which branch is physical.",
            "forbidden_language": "Xhat is both gauge-zero and finite fifth-force evidence",
            "replacement_language": "strict quotient branch or finite residual fallback, never both as positive evidence",
            "active": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "rule_id": "RULE2709_2_next_derivation_order",
            "rule": "Attack the parent action owner before scoring local empirical arenas.",
            "forbidden_language": "R10/PPN pass from placeholder c_g/qbar rows",
            "replacement_language": "source or derive q/V/matter/boundary/H_tau first, then run local empirical comparators",
            "active": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2709_0_candidate_written",
            "gate": "minimal parent action signature candidate exists",
            "status": "PASS_THEOREM_TARGET_ONLY",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "candidate A is coherent but not parent-derived",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2709_1_parent_signed",
            "gate": "candidate A signed by parent variation, degree count, and source charge",
            "status": "FAIL_NOT_SIGNED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "no explicit parent Lagrangian/constraint/symplectic/source owner closes all clauses",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2709_2_countermodels_killed",
            "gate": "species weights, variable constants, shadow frames, marker domains, and boundary/readout tails killed",
            "status": "FAIL_COUNTERMODELS_RETAINED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "423/1088/991 countermodels remain legal without stronger parent grammar",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2709_3_GR_Newton_reentry",
            "gate": "EH weak-field operator plus H_tau source gives GR/Newton/PPN",
            "status": "FAIL_NOT_REACHED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "operator/source/PPN readout remains downstream of the parent-signature gate",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2709_4_private",
            "gate": "GitHub/public action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2709_0_main",
            "decision": "CANDIDATE_A_SURVIVES_AS_COHERENT_THEOREM_TARGET",
            "rationale": "strict quotient EH/topological-vertical parent action is internally coherent and matches the closure axiom shape",
            "claim_effect": "no local-GR/Newton claim; theorem target only",
            "next_action": "source or construct the parent action owner for q, V, matter, boundary, Ward/Bianchi, and H_tau",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2709_1_no_hard_contradiction",
            "decision": "NO_HARD_FALSIFIER_OF_CANDIDATE_A_FOUND",
            "rationale": "retained countermodels block promotion but do not logically contradict the strict candidate because it explicitly excludes or retains them",
            "claim_effect": "project is not dead at this gate; it remains an unsigned closure theorem target",
            "next_action": "test the highest-risk exclusions rather than rerun broad audits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2709_2_best_route",
            "decision": "PARENT_ACTION_OWNER_SOURCE_HUNT_NEXT",
            "rationale": "the central missing object is no longer a vague coupling; it is one parent action signature that owns variation order and source charge",
            "claim_effect": "finite local scoring remains deferred",
            "next_action": "2710 parent action owner construction/source hunt or falsifier test",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2709_0_selected",
            "selection": "selected_primary",
            "target_doc": "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md",
            "target_script": "scripts/Y5_R2FR_parent_action_owner_construction_source_hunt_or_falsifier_test_2710.py",
            "task": "try to write or source the actual parent action owner behind MPS2709_A: q, V=ker(Dq), EH observed operator, topological/constraint vertical sector, MOMS matter functor, boundary/readout order, Ward/Bianchi identity, and H_tau source charge; if one clause cannot be owned, record the exact falsifier and keep LGR2708 closure explicit",
            "success_condition": "either extract a parent-owned action/variation signature for at least the q/V/matter/boundary substack, or identify the first irreducible contradiction requiring finite residual fallback",
            "forbidden_shortcuts": "claim local GR/Newton; adopt primitive minimality as taste; reuse representative zero as observed zero; run empirical local passes with placeholder coefficients; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2709_0_project_position",
            "topic": "local GR/Newton programme",
            "status": "INTEGRATED_PARENT_SIGNATURE_TARGET_WRITTEN",
            "meaning": "we now have a single candidate action signature to aim at rather than scattered coupling gates",
            "next_action": "construct/source parent action owner",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2709_1_grimness",
            "topic": "risk",
            "status": "HARD_BUT_NOT_FALSIFIED_AT_THIS_GATE",
            "meaning": "the gap is severe because the parent owner is unsigned, but no direct contradiction with the strict candidate was found",
            "next_action": "attack no-extension/material-marker and boundary/source owner first",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2709_2_empirical",
            "topic": "local tests",
            "status": "DEFERRED_UNTIL_PARENT_OR_FINITE_ROWS",
            "meaning": "R10/PPN/WEP/clock/orbital tests remain blocked for the local branch until coefficients are derived or sourced",
            "next_action": "do not run local passes with placeholders",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2709_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all artifacts remain private in post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    count = 0
    threshold = START_UTC.timestamp() - 2.0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                count += 1
        except OSError:
            continue
    return count


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2709_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2709_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    candidates = rows_by_name["candidate_signatures"]
    add(
        "VAL2709_2_candidate_A_written",
        any(row["candidate_id"] == "MPS2709_A_strict_quotient_EH_topological_vertical" and row["candidate_status"] == "COHERENT_THEOREM_TARGET_NOT_SIGNED" for row in candidates),
        "candidate A strict quotient EH/topological vertical parent signature written",
    )
    add("VAL2709_3_candidates_nonclaim", all(row["valid_for_claim"] == "false" for row in candidates), "all parent-signature candidates remain nonclaim")

    theorem = rows_by_name["theorem_target"]
    add("VAL2709_4_theorem_target_complete", len(theorem) >= 5 and all(row["current_status"] != "" for row in theorem), "theorem target covers parent action, no-pole, matter, boundary, weak-field re-entry")
    add("VAL2709_5_theorem_not_promoted", all(row["valid_for_claim"] == "false" for row in theorem), "theorem target is not promoted")

    audit = rows_by_name["clause_audit"]
    add("VAL2709_6_clause_audit_verdict", any(row["clause_id"] == "AUD2709_8_verdict" and "CERTIFICATE_NOT_CLOSED" in row["audit_result"] for row in audit), "clause audit keeps certificate not closed")
    add("VAL2709_7_no_claim_passes", all(row["claim_pass"] == "false" and row["valid_for_claim"] == "false" for row in audit), "no clause audit row claims a pass")

    falsifiers = rows_by_name["falsifier_ledger"]
    add("VAL2709_8_falsifiers_retained", len(falsifiers) >= 6 and all(row["valid_for_claim"] == "false" for row in falsifiers), "falsifier/countermodel ledger retained")
    add("VAL2709_9_no_hard_candidate_contradiction", any(row["decision"] == "NO_HARD_FALSIFIER_OF_CANDIDATE_A_FOUND" for row in rows_by_name["decision_ledger"]), "no hard contradiction to candidate A recorded")

    add("VAL2709_10_claims_blocked", all(row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates keep claim_allowed=false")
    add("VAL2709_11_next_2710", any(row["next_id"] == "NEXT2709_0_selected" and "2710" in row["target_doc"] for row in rows_by_name["next_target"]), "2710 target selected")
    add("VAL2709_12_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2709_13_no_formalization_recent_changes", formalization_recent_change_count() == 0, f"formalization_recent_changed_count={formalization_recent_change_count()}")
    add("VAL2709_14_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2709_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2709_PARSE_validation")]
    add(
        "VAL2709_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2709 writes a coherent minimal parent-action signature theorem target, records the unsigned clauses and retained falsifiers, blocks all local-GR/Newton claims, and selects parent-action owner construction/source hunt for 2710",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Minimal Parent Signature Candidates", rows_by_name["candidate_signatures"]),
        ("Parent Signature Theorem Target", rows_by_name["theorem_target"]),
        ("Clause Audit", rows_by_name["clause_audit"]),
        ("Falsifier Ledger", rows_by_name["falsifier_ledger"]),
        ("Re-Entry Rules", rows_by_name["reentry_rules"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2709: Minimal Parent Action Signature Synthesis Or Closure Falsification",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2709 takes the leap forward rather than circling the same coupling gate. The best strict route is now a concrete theorem target: one parent action with an EH observed branch, a quotient map `q`, vertical sector `V=ker(Dq)` that is gauge/topological/constrained or retained, MOMS ordinary matter descent, boundary/readout silence, Ward/Bianchi retention, and an owned Hamiltonian source charge. That candidate is coherent and no hard contradiction was found, but it is not parent-signed. The closure axiom therefore remains explicit and no local GR/Newton claim is promoted.",
        "",
        "## Bottom Line",
        "",
        "- Good news: the local route is no longer foggy; it has a single parent-action signature target.",
        "- Bad news: the signature is still unsigned, especially at no-extension/material markers, boundary/readout silence, and H_tau source ownership.",
        "- Claim discipline: no C_X, qbar_XT, R10, PPN, WEP, clock, orbital, Newton, or local-GR pass is allowed from 2709.",
        "- Best next move: 2710 tries to construct or source the actual parent action owner; if that fails, identify the first irreducible falsifier and route to finite residual fallback.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "candidate_signatures": candidate_signature_rows(),
        "theorem_target": theorem_target_rows(),
        "clause_audit": clause_audit_rows(),
        "falsifier_ledger": falsifier_ledger_rows(),
        "reentry_rules": reentry_rule_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_clause_audit"], rows_by_name["clause_audit"])
    write_csv(BRANCH_OUTPUTS["source_weight_candidate"], rows_by_name["candidate_signatures"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
