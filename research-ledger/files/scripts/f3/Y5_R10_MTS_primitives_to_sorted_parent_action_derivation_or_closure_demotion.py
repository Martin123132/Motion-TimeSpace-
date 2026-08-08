from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1237"
TITLE = "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PRIMITIVE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_MTS_PRIMITIVE_DERIVATION_AUDIT.csv"
GRAMMAR_CHAIN_PATH = OUT_DIR / f"{PACK_ID}_SORTED_GRAMMAR_DERIVATION_CHAIN.csv"
CLOSURE_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_DEMOTION_LEDGER.csv"
LOCAL_GR_STATUS_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_CONNECTION_STATUS.csv"
FINITE_TEST_TRACK_PATH = OUT_DIR / f"{PACK_ID}_FINITE_RESIDUAL_TEST_TRACK.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1237_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1237_0_1236_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_NEXT_TARGET.csv",
            "needle": "NEXT1236_0_1237",
            "purpose": "1236 handoff to MTS primitive derivation or closure demotion",
        },
        {
            "source_id": "SRC1237_1_1236_certificate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERT1236_6_current_verdict",
            "purpose": "typed certificate schema valid but not parent-derived",
        },
        {
            "source_id": "SRC1237_2_1236_meta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv",
            "needle": "META1236_3_public_status",
            "purpose": "private closure route is not public evidence",
        },
        {
            "source_id": "SRC1237_3_motion_contract",
            "local_path": "01-motion-load-route-contract.md",
            "needle": "The contract is to derive `p=1`, not fit it.",
            "purpose": "motion-load primitive scaffold and GR-lane target",
        },
        {
            "source_id": "SRC1237_4_local_GR_conditional",
            "local_path": "02-motion-load-local-GR-reduction.md",
            "needle": "yes conditionally, but not yet fundamentally.",
            "purpose": "local GR recovery conditional on reciprocity",
        },
        {
            "source_id": "SRC1237_5_reciprocity_not_derived",
            "local_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "reciprocity itself is not parent-derived",
            "purpose": "reciprocity parent-origin obstruction",
        },
        {
            "source_id": "SRC1237_6_nonpropagating_open",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "purpose": "clean nonpropagating route still lacks parent origin",
        },
        {
            "source_id": "SRC1237_7_observer_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "observer_map_contract_written_not_satisfied",
            "purpose": "observer map no-smuggling contract",
        },
        {
            "source_id": "SRC1237_8_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "cell current gives Q_R hair rather than R_AB=0",
        },
        {
            "source_id": "SRC1237_9_gauge_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "gauge/Noether route demotes local reciprocity to closure-only",
        },
        {
            "source_id": "SRC1237_10_parent_action_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv",
            "needle": "CG1009_0_total_parent_action",
            "purpose": "total parent action current-chain gate remains false",
        },
        {
            "source_id": "SRC1237_11_parent_sector_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            "needle": "PCS1009_9_total_parent_contract",
            "purpose": "parent sector contract is unsigned",
        },
        {
            "source_id": "SRC1237_12_object_typing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
            "needle": "OLT1066_6_verdict",
            "purpose": "object-language typing kills source scalars only conditionally",
        },
        {
            "source_id": "SRC1237_13_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "purpose": "source scalar exclusion remains not parent-derived",
        },
        {
            "source_id": "SRC1237_14_master_morphism",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "MHM1105_6_verdict",
            "purpose": "master no-hidden-visible morphism theorem demoted to explicit closure",
        },
        {
            "source_id": "SRC1237_15_object_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "EXH1107_6_verdict",
            "purpose": "object-language exhaustion not derived from parent primitives",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    primitive_audit = [
        {
            "primitive_id": "PRIM1237_0_motion_load_capacity",
            "primitive_route": "c^2 = v_space^2 + v_clock^2 + v_load^2 with v_load^2=2GM/r",
            "what_it_supplies": "a clean local clock/load scaffold and Newtonian leading limit target",
            "attempt_to_derive_sorted_grammar": "does not define visible coefficient domains, hidden-object exclusion, EM norm, or source-label forgetting",
            "result": "PARTIAL_QOBS_SCAFFOLD_ONLY",
            "source": source_ref("01-motion-load-route-contract.md", "The contract is to derive `p=1`, not fit it."),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_1_reciprocity",
            "primitive_route": "T^2 S = 1 / R_AB=0",
            "what_it_supplies": "selects p=1 and the GR-like radial routing lane if derived",
            "attempt_to_derive_sorted_grammar": "constrains observer radial cell but does not type EM/matter coefficient constructors",
            "result": "LOCAL_GR_ROUTE_CONDITIONAL_NOT_GRAMMAR",
            "source": source_ref("02-motion-load-local-GR-reduction.md", "yes conditionally, but not yet fundamentally."),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_2_nonpropagating_constraint",
            "primitive_route": "nonpropagating reciprocal strain",
            "what_it_supplies": "best known route to suppress reciprocal hair",
            "attempt_to_derive_sorted_grammar": "would impose a local routing closure but still does not derive no-hidden-visible coefficient syntax",
            "result": "CLEAN_CLOSURE_ROUTE_PARENT_ORIGIN_OPEN",
            "source": source_ref("07-nonpropagating-reciprocity-constraint.md", "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_3_observer_map",
            "primitive_route": "theta_0=T c dt, theta_1=sqrt(S)dr, J_q=T sqrt(S)",
            "what_it_supplies": "a concrete observed coframe/readout map for the local branch",
            "attempt_to_derive_sorted_grammar": "supplies Q_obs-like readout variables but not the parent action domain or coefficient exhaustion",
            "result": "READOUT_SORT_PARTIAL_CONTRACT_NOT_SATISFIED",
            "source": source_ref("10-observer-map-symplectic-contract.md", "observer_map_contract_written_not_satisfied"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_4_cell_current",
            "primitive_route": "partial_r(W partial_r R_AB)=0",
            "what_it_supplies": "a conserved reciprocal-cell charge equation",
            "attempt_to_derive_sorted_grammar": "produces Q_R hair and does not derive coefficient-domain syntax",
            "result": "FAILS_ZERO_CHARGE_AND_GRAMMAR",
            "source": source_ref("11-cell-current-origin-attempt.md", "cell_current_origin_no_charge_obstruction"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_5_gauge_noether",
            "primitive_route": "observer-splitting gauge/Noether identity",
            "what_it_supplies": "checks whether R_AB=0 is a first-class/gauge constraint",
            "attempt_to_derive_sorted_grammar": "current scaffold does not supply the gauge constraint and does not derive sorted action syntax",
            "result": "LOCAL_RECIPROCITY_CLOSURE_ONLY",
            "source": source_ref("12-gauge-noether-origin-audit.md", "gauge_noether_origin_not_derived_closure_only"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_6_total_parent_action",
            "primitive_route": "sector-by-sector parent action/current-chain contract",
            "what_it_supplies": "candidate action blocks and guardrails against shortcuts",
            "attempt_to_derive_sorted_grammar": "total parent action, sector certificates, stress closure, and variation order are incomplete",
            "result": "TOTAL_PARENT_ACTION_NOT_SIGNED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv", "CG1009_0_total_parent_action"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_7_object_language_typing",
            "primitive_route": "typed parent arguments / source scalar exclusion",
            "what_it_supplies": "the exact rule that would exclude inert source scalars and hidden-visible coefficient maps",
            "attempt_to_derive_sorted_grammar": "already identified as conditional, not derived from deeper MTS primitives",
            "result": "TYPING_RULE_CONDITIONAL_NOT_DERIVED",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv", "OLT1066_6_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "primitive_id": "PRIM1237_8_verdict",
            "primitive_route": "MTS primitives to sorted parent action grammar",
            "what_it_supplies": "motion-load/observer map gives promising local GR scaffolding, and typed object language gives a clean closure rule",
            "attempt_to_derive_sorted_grammar": "no inspected route derives the sorted grammar, unique F2, readout closure, or source-label forgetting from MTS primitives",
            "result": "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED",
            "source": "PRIM1237_0 through PRIM1237_7",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    grammar_chain = [
        {
            "chain_id": "CHAIN1237_0_Qobs",
            "required_piece": "derive observed geometry/readout sort Q_obs",
            "current_evidence": "observer coframe and motion-load readout are explicit",
            "status": "PARTIAL_SUCCESS",
            "failure_or_gap": "readout sort is not yet backed by a total parent action and radiative closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_1_Chid_disjoint",
            "required_piece": "derive hidden/local branch sort C_hid and prove it is disjoint from visible coefficient domains",
            "current_evidence": "hidden scalar counterexamples and invariant obstructions remain active",
            "status": "FAIL",
            "failure_or_gap": "no MTS primitive proves hidden invariant algebra triviality or no-extension marker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_2_visible_coeff_domain",
            "required_piece": "derive Arg(Coeff_vis[O_vis]) subset Q_obs x Theta_rep x Top_level",
            "current_evidence": "typed-domain theorem exists as exact conditional",
            "status": "FAIL",
            "failure_or_gap": "membership in parent-generated image is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_3_unique_curvature_norm",
            "required_piece": "derive unique EM curvature norm and no independent F_Q^2 constructor",
            "current_evidence": "EM lock audit keeps unique-F2 failed current corpus",
            "status": "FAIL",
            "failure_or_gap": "T_Q owner/fixed norm/no-counterterm theorem not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_4_readout_radiative",
            "required_piece": "derive readout/radiative closure preserving sorted domains",
            "current_evidence": "readout closure is an explicit 1236 certificate clause",
            "status": "FAIL",
            "failure_or_gap": "no RG/readout theorem; finite transfer priors remain mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_5_source_label_forgetting",
            "required_piece": "derive total Hilbert source functor with no per-species source-only weights",
            "current_evidence": "source scalar exclusion and source-label forgetting are conditional",
            "status": "FAIL",
            "failure_or_gap": "matter category, action-scale normalization, and variation-before-readout are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_6_parent_action",
            "required_piece": "derive one total parent action owning geometry, matter, EM, readout, source, and residual sectors",
            "current_evidence": "1009 sector contract has guardrails but total parent action gate is false",
            "status": "FAIL",
            "failure_or_gap": "sector variation certificates and stress/conservation closure remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "CHAIN1237_7_verdict",
            "required_piece": "derive sorted parent action grammar from MTS primitives",
            "current_evidence": "only Q_obs/readout scaffolding is partial; all grammar-exclusion clauses are unsigned",
            "status": "FAIL_DEMOTE_TO_CLOSURE",
            "failure_or_gap": "the exact certificate is useful but not derivable from inspected current-state sources",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_demotion = [
        {
            "closure_id": "CLOSE1237_0_typed_object_language",
            "closure": "visible coefficients may depend only on Q_obs, fixed representation data, and topological levels",
            "why_demoted": "not derived from MTS primitives; it is a grammar contract",
            "allowed_private_use": "discipline future model building and forbid smuggled hidden-visible coefficients in closure benchmark branches",
            "not_allowed_use": "public theorem-zero, EM-lock claim, or local-GR proof",
            "status": "EXPLICIT_CLOSURE_ASSUMPTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOSE1237_1_local_reciprocity",
            "closure": "R_AB=ln(T^2 S)=0 / T^2 S=1",
            "why_demoted": "cell-current and gauge/Noether routes do not derive zero reciprocal charge",
            "allowed_private_use": "GR-like local benchmark branch with p=1",
            "not_allowed_use": "derived GR reduction, PPN pass, or replacement for field equations",
            "status": "EXPLICIT_CLOSURE_ASSUMPTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOSE1237_2_unique_F2",
            "closure": "no hidden f(I_hid)F_Q^2 and no independent lambda_A F_Q^2",
            "why_demoted": "typed certificate and curvature norm are not parent-derived",
            "allowed_private_use": "zero-residual comparison branch only when labelled closure",
            "not_allowed_use": "alpha prediction or WEP/R10 local-GR evidence",
            "status": "EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOSE1237_3_source_label_forgetting",
            "closure": "source coupling sees total Hilbert stress only, not species source weights",
            "why_demoted": "parent matter category/action-scale normalization and variation-before-readout are unsigned",
            "allowed_private_use": "GR/WEP benchmark branch",
            "not_allowed_use": "Delta_w=0 theorem or R10/WEP claim",
            "status": "EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOSE1237_4_readout_radiative",
            "closure": "loops/readouts preserve visible coefficient domains",
            "why_demoted": "no radiative/readout theorem exists",
            "allowed_private_use": "idealized tree-level benchmark",
            "not_allowed_use": "clock/spectroscopy alpha-transfer closure claim",
            "status": "EXPLICIT_CLOSURE_OR_FINITE_TRANSFER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_status = [
        {
            "local_id": "LGR1237_0_Newtonian_clock_load",
            "requirement": "recover Newtonian clock/load side",
            "current_status": "PARTIAL_CONDITIONAL",
            "reason": "motion-load scaffold supplies T^2=1-L leading behavior but parent source normalization remains open",
            "what_is_missing": "measured GM/source bridge and total Hilbert source functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "local_id": "LGR1237_1_gamma",
            "requirement": "PPN gamma=1",
            "current_status": "CLOSURE_ONLY",
            "reason": "gamma-like routing follows if R_AB=0, but R_AB=0 is not derived",
            "what_is_missing": "zero reciprocal charge or first-class constraint theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "local_id": "LGR1237_2_beta",
            "requirement": "PPN beta=1",
            "current_status": "MISSING",
            "reason": "valid second-order PPN coordinate construction is not supplied by the closure grammar",
            "what_is_missing": "full local field equations, conservation identity, and second-order metric solution",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "local_id": "LGR1237_3_equivalence_principle",
            "requirement": "all matter sectors couple to same observed coframe/source",
            "current_status": "MISSING",
            "reason": "source-label forgetting and no-source-only slots are conditional",
            "what_is_missing": "parent matter category and action-scale normalization owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "local_id": "LGR1237_4_Bianchi_conservation",
            "requirement": "Bianchi-like consistency and stress conservation",
            "current_status": "MISSING",
            "reason": "total parent action/current-chain sector variation is not signed",
            "what_is_missing": "one parent variational action and sector stress closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "local_id": "LGR1237_5_verdict",
            "requirement": "derived GR/Newton local reduction",
            "current_status": "NOT_DERIVED",
            "reason": "Newtonian and gamma lanes are promising only under closure; beta, EP, and conservation remain missing",
            "what_is_missing": "first-class R_AB constraint plus total Hilbert source and full PPN field equations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_test_track = [
        {
            "track_id": "TEST1237_0_QR_hair",
            "quantity": "Q_R or gamma-1 reciprocal-hair residual",
            "why_needed": "local reciprocity is not derived; cell-current route permits exterior hair",
            "test_arena": "PPN/light bending/Shapiro/orbital local tests",
            "status": "FINITE_RESIDUAL_REQUIRED_UNLESS_FIRST_CLASS_CONSTRAINT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "track_id": "TEST1237_1_alpha_EM",
            "quantity": "b_alpha or c_alpha_DD",
            "why_needed": "unique-F2 and hidden-visible coefficient exclusion are closure-only",
            "test_arena": "clock/alpha/R10/WEP transfer",
            "status": "FINITE_RESIDUAL_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "track_id": "TEST1237_2_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "why_needed": "current/source normalization and source-label forgetting are unsigned",
            "test_arena": "R10/WEP/material comparison",
            "status": "FINITE_RESIDUAL_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "track_id": "TEST1237_3_readout_alpha",
            "quantity": "tau_clock/tau_WEP/readout alpha transfer",
            "why_needed": "radiative/readout closure is not derived",
            "test_arena": "clock/spectroscopy/WEP transfer kernels",
            "status": "FINITE_TRANSFER_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "track_id": "TEST1237_4_QCD_components",
            "quantity": "F_B,q, F_B,g, delta w_q, delta w_g",
            "why_needed": "QCD color edge and source component transfer are not signed",
            "test_arena": "WEP/R10/material energy fractions",
            "status": "FINITE_SOURCE_ROWS_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1237_0_derivation_failed",
            "decision": "do not claim the sorted parent grammar is derived",
            "because": "MTS primitive route supplies only partial observer/readout scaffolding; all exclusion clauses remain unsigned",
            "next_action": "separate derivation track from closure benchmark track",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1237_1_demote_closure",
            "decision": "demote typed grammar and R_AB=0 to explicit closures",
            "because": "current state supports them as disciplined private contracts but not theorem consequences",
            "next_action": "label any zero-residual branch as closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1237_2_keep_derivation_route",
            "decision": "keep first-class constraint / total parent action as the derivation route",
            "because": "that is the only route left that could make local GR reduction structural rather than benchmark closure",
            "next_action": "attempt first-class R_AB constraint or prepare closure benchmark scorecard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1237_3_testing_track_needed",
            "decision": "retain finite residual test track",
            "because": "without theorem-zeroes, the honest path is bounded coefficients and empirical robustness",
            "next_action": "prioritize Q_R/PPN, alpha, source beta, readout transfer, and QCD component rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1237_0_sorted_grammar",
            "claim": "sorted parent action grammar derived from MTS primitives",
            "status": "BLOCKED",
            "reason": "CHAIN1237_7 status=FAIL_DEMOTE_TO_CLOSURE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1237_1_no_hidden_visible",
            "claim": "no hidden-visible coefficient morphisms as theorem",
            "status": "BLOCKED",
            "reason": "typed grammar is closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1237_2_unique_F2",
            "claim": "unique F_Q^2 theorem",
            "status": "BLOCKED",
            "reason": "hidden branch, independent F2 branch, and readout branch remain open unless closure is adopted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1237_3_RAB_zero",
            "claim": "R_AB=0 derived from parent MTS",
            "status": "BLOCKED",
            "reason": "cell-current and gauge/Noether attempts fail; first-class constraint not supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1237_4_local_GR",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "LGR1237_5 verdict=NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1237_5_WEP_R10_PPN_clock",
            "claim": "WEP/R10/PPN/clock local tests pass structurally",
            "status": "BLOCKED",
            "reason": "finite residual test track remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1237_0_1238",
            "target_file": "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard.md",
            "target_script": "scripts/Y5_R10_first_class_RAB_constraint_or_local_GR_closure_benchmark_scorecard.py",
            "task": "attempt the last clean derivation route: a first-class parent constraint that enforces R_AB=0 and source-label forgetting; if it fails, build an explicit local-GR closure benchmark scorecard and finite residual testing priority list",
            "success_condition": "either R_AB=0 and total Hilbert source are parent-derived without GR import, or the local-GR branch is cleanly labelled closure-only with Q_R/alpha/source/QCD residuals ready for empirical scoring",
            "do_not_do": "do not claim derived GR, EM lock, graph connectedness, Delta_w=0, WEP, PPN, clock, R10, or public victory from closure assumptions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        PRIMITIVE_AUDIT_PATH,
        GRAMMAR_CHAIN_PATH,
        CLOSURE_DEMOTION_PATH,
        LOCAL_GR_STATUS_PATH,
        FINITE_TEST_TRACK_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PRIMITIVE_AUDIT_PATH, primitive_audit)
    write_csv(GRAMMAR_CHAIN_PATH, grammar_chain)
    write_csv(CLOSURE_DEMOTION_PATH, closure_demotion)
    write_csv(LOCAL_GR_STATUS_PATH, local_gr_status)
    write_csv(FINITE_TEST_TRACK_PATH, finite_test_track)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            primitive_audit,
            grammar_chain,
            closure_demotion,
            local_gr_status,
            finite_test_track,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    primitive_verdict = any(
        row["primitive_id"] == "PRIM1237_8_verdict"
        and row["result"] == "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED"
        for row in primitive_audit
    )
    grammar_demoted = any(
        row["chain_id"] == "CHAIN1237_7_verdict" and row["status"] == "FAIL_DEMOTE_TO_CLOSURE"
        for row in grammar_chain
    )
    closures_explicit = len(closure_demotion) == 5 and all("CLOSURE" in row["status"] for row in closure_demotion)
    local_gr_not_derived = any(
        row["local_id"] == "LGR1237_5_verdict" and row["current_status"] == "NOT_DERIVED"
        for row in local_gr_status
    )
    finite_track_ready = len(finite_test_track) == 5 and any(row["quantity"].startswith("Q_R") for row in finite_test_track)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1238 = next_target[0]["target_file"].startswith("1238-Y5-R10-first-class-RAB")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1237_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1237_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1237_2_primitive_derivation_failed",
            "MTS primitive route does not derive sorted grammar",
            primitive_verdict,
            "PRIM1237_8 result=DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED",
        ),
        validation_row(
            "VAL1237_3_grammar_demoted",
            "sorted grammar derivation is demoted to closure",
            grammar_demoted,
            "CHAIN1237_7 status=FAIL_DEMOTE_TO_CLOSURE",
        ),
        validation_row(
            "VAL1237_4_closures_explicit",
            "closure assumptions are explicitly labelled",
            closures_explicit,
            f"closure_rows={len(closure_demotion)}",
        ),
        validation_row(
            "VAL1237_5_local_GR_not_derived",
            "local GR/Newton reduction is not promoted",
            local_gr_not_derived,
            "LGR1237_5 current_status=NOT_DERIVED",
        ),
        validation_row(
            "VAL1237_6_finite_test_track",
            "finite residual test track is retained",
            finite_track_ready,
            f"finite_test_rows={len(finite_test_track)} including Q_R",
        ),
        validation_row(
            "VAL1237_7_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1237_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1237_9_next_target_1238",
            "next target is first-class R_AB constraint or closure benchmark scorecard",
            next_is_1238,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1237_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1237_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1237_12_overall",
            "overall 1237 validation",
            all(row["status"] == "PASS" for row in validation),
            "1237 attempts the MTS-primitives-to-grammar derivation, fails it cleanly, demotes closure assumptions, and keeps finite residual tests alive",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1237 does **not** derive the sorted parent action grammar from the inspected MTS primitive route. The motion-load/observer-map branch gives a promising local-GR scaffold, but the grammar that kills hidden-visible coefficients remains a closure assumption.",
        "",
        "**Main progress:** the work is cleaner now: `R_AB=0`, typed visible coefficient domains, unique `F_Q^2`, source-label forgetting, and readout closure are separated as explicit closures unless a future first-class parent constraint/total action derives them.",
        "",
        "**No-claim guard:** no derived GR, EM lock, graph connectedness, `Delta_w=0`, R10, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## MTS Primitive Derivation Audit",
        markdown_table(primitive_audit, list(primitive_audit[0].keys())),
        "",
        "## Sorted Grammar Derivation Chain",
        markdown_table(grammar_chain, list(grammar_chain[0].keys())),
        "",
        "## Closure Demotion Ledger",
        markdown_table(closure_demotion, list(closure_demotion[0].keys())),
        "",
        "## Local GR Connection Status",
        markdown_table(local_gr_status, list(local_gr_status[0].keys())),
        "",
        "## Finite Residual Test Track",
        markdown_table(finite_test_track, list(finite_test_track[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
