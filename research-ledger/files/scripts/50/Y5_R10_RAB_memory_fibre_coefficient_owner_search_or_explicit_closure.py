from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1347"
TITLE = "1347-Y5-R10-RAB-memory-fibre-coefficient-owner-search-or-explicit-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OWNER_SEARCH_PATH = OUT_DIR / f"{PACK_ID}_OWNER_SEARCH_LEDGER.csv"
COEFF_OWNER_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_OWNER_MATRIX.csv"
CLOSURE_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_EXPLICIT_CLOSURE_LEDGER.csv"
ROUTE_RANK_PATH = OUT_DIR / f"{PACK_ID}_ROUTE_RANKING.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1347_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def falsey(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "n", ""}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not falsey(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not falsey(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1347*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1347_0_1346_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1346_NEXT_TARGET.csv",
            "needle": "NEXT1346_0_1347",
            "role": "selected 1347 target",
        },
        {
            "source_id": "SRC1347_1_1346_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1346_SYMBOLIC_COEFFICIENT_PACK.csv",
            "needle": "COEFF1346_M_B",
            "role": "memory/fibre symbolic coefficient pack",
        },
        {
            "source_id": "SRC1347_2_1304_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
            "needle": "OO1304_2_owner_verdict",
            "role": "memory operator owner attempt",
        },
        {
            "source_id": "SRC1347_3_1304_gap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
            "needle": "ZPG1304_2_mass_gap",
            "role": "memory positive gap map",
        },
        {
            "source_id": "SRC1347_4_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "AA826_2_trace_projection_lock",
            "role": "memory branch extremum route",
        },
        {
            "source_id": "SRC1347_5_970_quadratic",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "QMA970_7_verdict",
            "role": "quadratic memory action construction",
        },
        {
            "source_id": "SRC1347_6_1049_symmetry",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
            "needle": "SBT1049_4_product_functor",
            "role": "symmetry/product-functor route",
        },
        {
            "source_id": "SRC1347_7_1219_counterexample",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_0_generic_scalar",
            "role": "active hidden scalar counterexample",
        },
        {
            "source_id": "SRC1347_8_1273_hcore",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv",
            "needle": "HCO1273_6_classification_verdict",
            "role": "fibre/H-core owner classification",
        },
        {
            "source_id": "SRC1347_9_1346_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1346_VALIDATION.csv",
            "needle": "VAL1346_9_overall",
            "role": "1346 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    owner_search = [
        {
            "owner_id": "OWN1347_0_memory_action_scaffold",
            "coefficient_family": "Z_mem;M2_mem;J_mem;Q_boundary_mem",
            "candidate_owner": "quadratic memory action / parent memory sector",
            "source_basis": "AA826_1_memory_sector;QMA970_0_action;OO1304_0_action_form",
            "owner_status": "SCAFFOLD_FOUND_NOT_PARENT_SIGNED",
            "what_it_owns_if_signed": "operator normalization, Hessian/gap, source decomposition, and boundary variation",
            "blocking_gap": "parent adoption, field domain, source/bath terms, boundary class, units, and signs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_1_memory_positive_gap",
            "coefficient_family": "Z_mem;M2_mem",
            "candidate_owner": "positive local operator / Hessian gap",
            "source_basis": "ZPG1304_0_Zm_positive;ZPG1304_2_mass_gap;MPO967_1_operator",
            "owner_status": "FORMULA_OWNER_FOUND_VALUES_MISSING",
            "what_it_owns_if_signed": "positive ellipticity and finite range lambda_mem",
            "blocking_gap": "Z_mem_min, M2_mem functional form, local branch extremum, zero-mode removal, and units missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_2_memory_branch_extremum",
            "coefficient_family": "B_mem",
            "candidate_owner": "trace projection / F1 zero route",
            "source_basis": "AA826_2_trace_projection_lock",
            "owner_status": "PROMISING_CONDITIONAL_ROUTE_NOT_DERIVED",
            "what_it_owns_if_signed": "linear memory-curvature vertex vanishes when m_L is an extremum and projection is parent-derived",
            "blocking_gap": "trace projection must be derived from K_MTS, not imposed; F'_mem=0 is not signed for the actual parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_3_memory_matter_vertex",
            "coefficient_family": "C_mem",
            "candidate_owner": "matter-blind/product-functor route",
            "source_basis": "SBT1049_4_product_functor;META1236_0_statement;HSC1219_4_source_weight",
            "owner_status": "CONDITIONAL_ROUTE_COUNTEREXAMPLE_LOCKED",
            "what_it_owns_if_signed": "same-frame matter blindness and no source-weight vertex",
            "blocking_gap": "product functor/meta-theorem premises are unsigned; hidden scalar/source-weight counterexamples remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_4_memory_source_boundary",
            "coefficient_family": "J_mem;Q_boundary_mem",
            "candidate_owner": "positive no-hair source/boundary silence",
            "source_basis": "QMA970_3_source_silence;QMA970_4_boundary_zero_mode;NHP1042_3_source_zero;NHP1042_4_boundary_flux_zero",
            "owner_status": "RELATIVE_LEMMA_READY_INPUTS_UNSIGNED",
            "what_it_owns_if_signed": "source-free compact branch and no exterior memory charge",
            "blocking_gap": "matter blindness, chi_D wall silence, readout source silence, boundary flux, and topology class missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_5_fibre_unique_gap",
            "coefficient_family": "Z_h;M2_h;J_h",
            "candidate_owner": "unique gapped source-independent fibre solution h0",
            "source_basis": "GE966_5_finite_fibre_spectrum;HCO1273_1_smooth_potential;HCO1273_6_classification_verdict",
            "owner_status": "FINITE_BRANCH_IF_CHOSEN_NOT_ZERO_OWNER",
            "what_it_owns_if_signed": "fibre gap/stiffness and source-independent constant renormalization",
            "blocking_gap": "parent fibre potential, mass gap, uniqueness theorem, and source independence missing; smooth potential gives finite residual if sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_6_fibre_curvature_vertex",
            "coefficient_family": "B_h",
            "candidate_owner": "no hidden-visible coefficient meta-theorem or multiplier constraint",
            "source_basis": "META1236_0_statement;HCO1273_4_linear_multiplier;HCO1273_5_unimodular_radial_cell",
            "owner_status": "EXACT_IF_PARENT_GRAMMAR_SIGNED_ELSE_UNSIGNED",
            "what_it_owns_if_signed": "forbids hR vertex or constrains fibre fluctuation to zero before it propagates",
            "blocking_gap": "parent grammar/unimodular cell or hidden-visible coefficient typing not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_7_fibre_matter_vertex",
            "coefficient_family": "C_h",
            "candidate_owner": "h-blind matter functor",
            "source_basis": "GE966_5_finite_fibre_spectrum;PAL703_2_matter_functor;OWN1224_6_verdict",
            "owner_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "what_it_owns_if_signed": "fibre spectrum does not affect clocks, masses, source maps, or composition",
            "blocking_gap": "matter functor descent, source-label forgetting, and action-scale owner remain conditional/open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "OWN1347_8_fibre_boundary",
            "coefficient_family": "Q_boundary_h",
            "candidate_owner": "boundary/projection flux no-hair",
            "source_basis": "HCO1273_3_boundary_current;NHP1042_4_boundary_flux_zero",
            "owner_status": "NO_ZERO_WITHOUT_NO_CHARGE",
            "what_it_owns_if_signed": "no exterior fibre charge from projection/boundary class",
            "blocking_gap": "parent boundary variational class and Q_h=0 charge theorem missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coeff_owner = [
        {
            "coeff_id": "COWN1347_0_Z_mem",
            "symbol": "Z_mem",
            "best_owner": "OWN1347_0_memory_action_scaffold;OWN1347_1_memory_positive_gap",
            "owner_quality": "SCAFFOLD_NOT_SIGNED",
            "postulate_if_closure": "Z_mem>0 with stated units and local branch domain",
            "next_derivation_test": "derive memory sector action and second variation from parent grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_1_M2_mem",
            "symbol": "M2_mem",
            "best_owner": "OWN1347_1_memory_positive_gap",
            "owner_quality": "FORMULA_OWNER_FOUND_VALUES_MISSING",
            "postulate_if_closure": "M2_mem>=m_min^2>0 or finite symbolic value with units",
            "next_derivation_test": "derive V_R Hessian at local memory branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_2_B_mem",
            "symbol": "B_mem",
            "best_owner": "OWN1347_2_memory_branch_extremum",
            "owner_quality": "PROMISING_CONDITIONAL_ROUTE_NOT_DERIVED",
            "postulate_if_closure": "B_mem=0 by local branch extremum, or finite symbolic B_mem retained",
            "next_derivation_test": "derive trace projection lock and F'_mem(M0)=0 from K_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_3_C_mem",
            "symbol": "C_mem",
            "best_owner": "OWN1347_3_memory_matter_vertex",
            "owner_quality": "COUNTEREXAMPLE_LOCKED",
            "postulate_if_closure": "C_mem=0 by product functor/matter blindness, or finite C_mem retained",
            "next_derivation_test": "prove product functor/no hidden-visible coefficient slot in same observed frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_4_J_mem_QB",
            "symbol": "J_mem;Q_boundary_mem",
            "best_owner": "OWN1347_4_memory_source_boundary",
            "owner_quality": "RELATIVE_LEMMA_READY_INPUTS_UNSIGNED",
            "postulate_if_closure": "J_mem=Q_boundary_mem=0 with source/boundary theorem, or finite charge retained",
            "next_derivation_test": "derive source silence and boundary no-hair after B_mem/C_mem are owned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_5_Zh_M2h_Jh",
            "symbol": "Z_h;M2_h;J_h",
            "best_owner": "OWN1347_5_fibre_unique_gap",
            "owner_quality": "FINITE_BRANCH_IF_CHOSEN_NOT_ZERO_OWNER",
            "postulate_if_closure": "unique gapped source-independent h0 or finite symbolic fibre gap/source",
            "next_derivation_test": "derive parent fibre potential, gap, and source independence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_6_Bh",
            "symbol": "B_h",
            "best_owner": "OWN1347_6_fibre_curvature_vertex",
            "owner_quality": "EXACT_IF_PARENT_GRAMMAR_SIGNED_ELSE_UNSIGNED",
            "postulate_if_closure": "B_h=0 by hidden-visible coefficient typing or finite B_h retained",
            "next_derivation_test": "prove no hidden-visible coefficient meta-theorem or fibre multiplier constraint from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_7_Ch",
            "symbol": "C_h",
            "best_owner": "OWN1347_7_fibre_matter_vertex",
            "owner_quality": "CONDITIONAL_NOT_PARENT_SIGNED",
            "postulate_if_closure": "C_h=0 by h-blind matter functor or finite composition/source coupling retained",
            "next_derivation_test": "derive matter functor descent and source-label forgetting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coeff_id": "COWN1347_8_QBh",
            "symbol": "Q_boundary_h",
            "best_owner": "OWN1347_8_fibre_boundary",
            "owner_quality": "NO_ZERO_WITHOUT_NO_CHARGE",
            "postulate_if_closure": "Q_boundary_h=0 by boundary variational class or finite boundary charge retained",
            "next_derivation_test": "derive Q_h=0 boundary/current theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_ledger = [
        {
            "closure_id": "CLOS1347_0_memory_minimal_closure",
            "branch": "memory_class_scalar",
            "closure_statement": "Adopt a parent memory sector with positive Z_mem, positive M2_mem, B_mem=0 by branch extremum, C_mem=0 by matter blindness, and J/Q_boundary silence.",
            "why_needed": "current corpus has scaffold but no signed parent owner",
            "public_status": "PRIVATE_CLOSURE_ONLY_NOT_CLAIM",
            "risk_if_used": "would smuggle local-GR scalar silence unless each clause is later derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1347_1_memory_finite_residual",
            "branch": "memory_class_scalar",
            "closure_statement": "Retain Z_mem, M2_mem, B_mem, C_mem, J_mem, Q_boundary_mem as symbolic finite branch coefficients.",
            "why_needed": "if extremum/matter-blind/source silence fail, memory is directly testable by R10/PPN/clock/Gdot",
            "public_status": "NONCLAIM_RESIDUAL_ROUTE",
            "risk_if_used": "requires real units and source/test normalization before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1347_2_fibre_minimal_closure",
            "branch": "finite_fibre_spectrum",
            "closure_statement": "Adopt a unique gapped source-independent h0 and no hR/hT vertices, so fibre renormalizes constants only.",
            "why_needed": "no parent fibre potential/gap/matter-blindness theorem is signed",
            "public_status": "PRIVATE_CLOSURE_ONLY_NOT_CLAIM",
            "risk_if_used": "would hide WEP/source-normalization and finite-range scalar risk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1347_3_fibre_finite_residual",
            "branch": "finite_fibre_spectrum",
            "closure_statement": "Retain Z_h, M2_h, B_h, C_h, J_h, Q_boundary_h as symbolic finite branch coefficients.",
            "why_needed": "ordinary smooth/kinetic H-core routes produce finite residuals, not theorem-zero",
            "public_status": "NONCLAIM_RESIDUAL_ROUTE",
            "risk_if_used": "needs fibre source/test charge normalization and body/composition model",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    route_ranking = [
        {
            "rank": 1,
            "route": "memory branch-extremum / trace projection lock",
            "why_ranked_here": "best chance to kill B_mem specifically without killing all memory dynamics",
            "source_basis": "AA826_2_trace_projection_lock",
            "next_action": "derive trace projection from K_MTS and F'_mem(M0)=0, or demote B_mem=0 to closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 2,
            "route": "memory operator/gap owner",
            "why_ranked_here": "needed for lambda_mem and positive nohair regardless of B_mem outcome",
            "source_basis": "OO1304;ZPG1304;QMA970",
            "next_action": "extract Z_mem and M2_mem signs/units from parent memory sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 3,
            "route": "product functor / no hidden-visible coefficient slot",
            "why_ranked_here": "would kill C_mem and C_h and protect matter frame",
            "source_basis": "SBT1049;META1236;HSC1219",
            "next_action": "prove hidden-visible coefficient meta-theorem or keep counterexample locked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rank": 4,
            "route": "fibre unique gapped source-independent h0",
            "why_ranked_here": "best fibre-specific route but currently lacks parent potential/gap",
            "source_basis": "GE966_5;HCO1273",
            "next_action": "derive fibre potential/gap/matter-blindness or retain finite fibre residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate = [
        {
            "gate_id": "GATE1347_0_owner_claim",
            "claim": "memory/fibre coefficient owner is claim-ready",
            "allowed_if": "at least one coefficient row has parent-signed owner, units, branch, and no active counterexample",
            "current_status": "BLOCKED",
            "reason": "owners are scaffolds/conditional routes, not signed owners",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1347_1_R2FR_zero",
            "claim": "direct scalar pressure rows are zero",
            "allowed_if": "B/C/J/boundary are zero-owned for memory and fibre and positive/gap owners exist",
            "current_status": "BLOCKED",
            "reason": "B_mem and B_h not zero-signed; matter/source/boundary gates open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1347_2_runner",
            "claim": "finite residual scoring may run",
            "allowed_if": "symbolic coefficients become numeric/source-backed with source/test normalization",
            "current_status": "BLOCKED",
            "reason": "1347 is owner search and closure ledger only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1347_0_memory",
            "decision": "memory has the best owner scaffold, but not a signed owner",
            "because": "AA826/QMA970/OO1304/ZPG1304 supply action/operator/gap shapes while leaving parent adoption, units, signs, source, and boundary clauses open",
            "effect": "next target should attack memory branch-extremum and operator-signature first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1347_1_fibre",
            "decision": "fibre has no ordinary theorem-zero owner yet",
            "because": "H-core/fibre classifications say smooth potentials or kinetic terms produce finite residuals unless a constraint/multiplier/grammar theorem is signed",
            "effect": "fibre remains retained residual unless no-hidden-visible grammar is proven later",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1347_2_closure",
            "decision": "explicit closure ledger is required if work proceeds without derivation",
            "because": "the missing coefficients are now named and cannot be silently set to zero",
            "effect": "future docs can distinguish theorem route from private closure route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1347_0_1348",
            "target_file": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
            "target_script": "scripts/Y5_R10_RAB_memory_branch_extremum_and_operator_signature_or_closure.py",
            "task": "attack the best owner route: derive the memory trace-projection/branch-extremum B_mem=0 condition and the Z_mem/M2_mem operator signature; if not derivable, write the exact memory closure contract",
            "success_condition": "B_mem or Z_mem/M2_mem parent-owned, or a precise private closure contract distinguishing B_mem=0 from finite B_mem residual",
            "do_not": "do not claim fibre zero, do not score R10/PPN, do not treat the memory scaffold as a signed derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        owner_search,
        coeff_owner,
        closure_ledger,
        route_ranking,
        claim_gate,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(OWNER_SEARCH_PATH, owner_search)
    write_csv(COEFF_OWNER_PATH, coeff_owner)
    write_csv(CLOSURE_LEDGER_PATH, closure_ledger)
    write_csv(ROUTE_RANK_PATH, route_ranking)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    memory_scaffold_found = any(row["owner_status"] == "SCAFFOLD_FOUND_NOT_PARENT_SIGNED" for row in owner_search)
    promising_bmem_route = any(row["owner_id"] == "OWN1347_2_memory_branch_extremum" and "PROMISING" in row["owner_status"] for row in owner_search)
    no_claim_ready_owner = all("CLAIM_READY" not in row["owner_status"] for row in owner_search)
    closure_complete = len(closure_ledger) == 4
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and memory_scaffold_found
        and promising_bmem_route
        and no_claim_ready_owner
        and closure_complete
        and claims_blocked
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1347_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1347_1_memory_scaffold_found",
            "memory action/operator scaffold is found but not signed",
            memory_scaffold_found,
            "OWN1347_0_memory_action_scaffold",
        ),
        validation_row(
            "VAL1347_2_bmem_route_found",
            "memory branch-extremum B_mem route is identified as the best next target",
            promising_bmem_route,
            "OWN1347_2_memory_branch_extremum",
        ),
        validation_row(
            "VAL1347_3_no_claim_ready_owner",
            "no coefficient owner is claim-ready",
            no_claim_ready_owner,
            ";".join(f"{row['owner_id']}={row['owner_status']}" for row in owner_search),
        ),
        validation_row(
            "VAL1347_4_closure_ledger_complete",
            "explicit closure/residual ledger covers memory and fibre",
            closure_complete,
            f"closure_rows={len(closure_ledger)}",
        ),
        validation_row(
            "VAL1347_5_claims_blocked",
            "owner, R2/fR zero, and runner claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1347_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1347_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1347_8_next_target_1348",
            "next target routes to memory branch-extremum/operator signature",
            next_target[0]["next_id"] == "NEXT1347_0_1348",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1347_9_overall",
            "overall 1347 validation",
            overall_ok,
            "1347 finds memory scaffold and B_mem extremum route, finds no claim-ready owner, and writes explicit closure ledger",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1347 finds owner scaffolds, not claim-ready owners. Memory has the strongest route: a parent memory action/operator scaffold plus a possible trace-projection branch-extremum route for `B_mem=0`. Fibre still lacks a zero owner unless a stronger parent grammar/constraint/matter-blindness theorem is derived.

**Main progress:** every memory/fibre coefficient now has a best available owner candidate and an explicit closure alternative. The work no longer says “coefficient missing” generically; it names exactly which mechanism would have to own each coefficient.

**Decision:** move to `1348`: attack the memory route first, because it is the only route with a concrete action/operator scaffold and a plausible `B_mem=0` branch-extremum mechanism. No R10/PPN/local-GR claim is made.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Owner Search Ledger
{markdown_table(owner_search, ["owner_id", "coefficient_family", "candidate_owner", "source_basis", "owner_status", "what_it_owns_if_signed", "blocking_gap", "valid_for_claim", "claim_allowed"])}

## Coefficient Owner Matrix
{markdown_table(coeff_owner, ["coeff_id", "symbol", "best_owner", "owner_quality", "postulate_if_closure", "next_derivation_test", "valid_for_claim", "claim_allowed"])}

## Explicit Closure Ledger
{markdown_table(closure_ledger, ["closure_id", "branch", "closure_statement", "why_needed", "public_status", "risk_if_used", "valid_for_claim", "claim_allowed"])}

## Route Ranking
{markdown_table(route_ranking, ["rank", "route", "why_ranked_here", "source_basis", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gate
{markdown_table(claim_gate, ["gate_id", "claim", "allowed_if", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
