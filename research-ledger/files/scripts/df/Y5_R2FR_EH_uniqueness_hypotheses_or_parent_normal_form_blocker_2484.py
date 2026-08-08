from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EH_UNIQUENESS_OR_PARENT_NORMAL_FORM_2484"
CHECKPOINT_ID = "2484"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EH_UNIQUENESS_2484_SOURCE_REGISTER.csv",
    "hypothesis_audit": OUT / "P8_Y5_EH_UNIQUENESS_2484_HYPOTHESIS_AUDIT.csv",
    "theorem_attempt": OUT / "P8_Y5_EH_UNIQUENESS_2484_THEOREM_ATTEMPT.csv",
    "normal_form_blockers": OUT / "P8_Y5_EH_UNIQUENESS_2484_PARENT_NORMAL_FORM_BLOCKERS.csv",
    "residual_update": OUT / "P8_Y5_EH_UNIQUENESS_2484_RESIDUAL_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_EH_UNIQUENESS_2484_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EH_UNIQUENESS_2484_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EH_UNIQUENESS_2484_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EH_UNIQUENESS_2484_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2484_VALIDATION.csv",
}

COPY_TARGETS = {
    "hypothesis_audit": LOCAL_BOUNDS / "EH_uniqueness_hypothesis_audit_2484_NONCLAIM.csv",
    "normal_form_blockers": LOCAL_BOUNDS / "Parent_normal_form_blockers_2484_NONCLAIM.csv",
    "residual_update": LOCAL_BOUNDS / "EH_import_kappa_residual_update_2484_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2484_PARENT_NORMAL_FORM_FIELD_SYMMETRY_DERIVATIVE_GRAMMAR.csv",
}

SOURCES = [
    {
        "source_id": "SRC2484_00_2483_doc",
        "source_path": ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
        "needles": ["NEXT2483_0_selected", "EH2483_2_parent_origin", "e_kappaG", "VAL2483_OVERALL"],
        "role": "handoff selecting EH uniqueness hypotheses and parent normal form",
    },
    {
        "source_id": "SRC2484_01_2404_first_variation",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["S_min=S_EH", "CANDIDATE_NOT_DERIVED", "REF2404_1_EH_import"],
        "role": "candidate EH variation and EH-import guardrail",
    },
    {
        "source_id": "SRC2484_02_2405_EH_dominance",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["EHD2405_4_current_verdict", "CG2405_0_EH_dominance", "OPB2405_0_total_DeltaE_MTS"],
        "role": "residual dominance gate below EH-leading origin",
    },
    {
        "source_id": "SRC2484_03_2406_sector_audit",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_0_higher_derivative", "SVC2406_6_verdict", "CG2406_0_EH_dominance"],
        "role": "live residual sectors that obstruct uniqueness promotion",
    },
    {
        "source_id": "SRC2484_04_2477_metric_response",
        "source_path": ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md",
        "needles": ["BLK2477_0_EH_origin", "THM2477_0_parent_candidate_equation", "GATE2477_3_local_GR"],
        "role": "weak-field route showing EH origin remains upstream of local GR",
    },
    {
        "source_id": "SRC2484_05_2482_kappa",
        "source_path": ROOT / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
        "needles": ["KAP2482_1_parent_origin", "EN2482_0_e_kappaG", "VAL2482_OVERALL"],
        "role": "coupling normalization blocker linked to parent EH coefficient",
    },
    {
        "source_id": "SRC2484_06_2236_derivative_grammar",
        "source_path": ROOT / "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "needles": ["GRAM2236_5_verdict", "SORT2236_0_auxiliary_coordinate", "VAL2236_OVERALL"],
        "role": "precedent that derivative bans require parent object-language proof",
    },
    {
        "source_id": "SRC2484_07_2483_validation",
        "source_path": OUT / "P8_Y5_BRR545_2483_VALIDATION.csv",
        "needles": ["VAL2483_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def hypothesis_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "hypothesis_id": "HYP2484_0_public_metric_or_coframe",
            "uniqueness_clause": "single public metric/coframe is the local gravitational readout",
            "MTS_evidence": "candidate branch uses e(q) and a terminal public coframe, but the parent field list is not fully signed",
            "status": "PARTIAL_CANDIDATE_NOT_PARENT_SIGNED",
            "blocker": "typed parent field list and quotient map q from private variables to public geometry",
            "effect_if_signed": "EH uniqueness can be asked in the correct variable rather than imported",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_1_local_diffeomorphism_invariance",
            "uniqueness_clause": "parent local branch is invariant under spacetime diffeomorphisms, not merely written covariantly after the fact",
            "MTS_evidence": "candidate EH template is covariant; parent MTS symmetry generator is not yet audited at the action level",
            "status": "UNSIGNED_PARENT_SYMMETRY",
            "blocker": "derive diffeomorphism generator/Noether identity from the MTS parent action and quotient map",
            "effect_if_signed": "Bianchi compatibility becomes a parent identity rather than a consistency wish",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_2_locality_and_derivative_order",
            "uniqueness_clause": "leading local metric/coframe equations contain no higher than second derivatives",
            "MTS_evidence": "2406 retains c_HD and 2236 shows derivative bans are conditional unless parent grammar forbids them",
            "status": "BLOCKED_BY_DERIVATIVE_GRAMMAR",
            "blocker": "no parent object-language theorem banning R^2/Ricci^2/boxR, vertical derivatives, and boundary derivative terms",
            "effect_if_signed": "Lovelock-like uniqueness can exclude higher-curvature residuals at leading local order",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_3_no_extra_local_tensors",
            "uniqueness_clause": "no q, projector, memory, tau, boundary, or auxiliary representative leaves a rank-2 local tensor in the public equation",
            "MTS_evidence": "2405/2406 retain projector, memory/coframe, q-source, boundary and auxiliary residual sectors",
            "status": "BLOCKED_BY_LIVE_RESIDUAL_SECTORS",
            "blocker": "sector zero/silence certificates or source-backed bounds for every retained non-EH operator",
            "effect_if_signed": "DeltaE_MTS can be removed from the uniqueness theorem rather than carried as an operator residual",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_4_matter_descent_and_conservation",
            "uniqueness_clause": "matter stress couples to the same public geometry and obeys the parent Noether conservation law",
            "MTS_evidence": "2481/2482 retain source normalization and dynamic worldtube exchange components",
            "status": "BLOCKED_BY_SOURCE_NORMALIZATION",
            "blocker": "Hilbert current descent, dynamic exchange identity, jump/support theorem, and no fitted-GM calibration",
            "effect_if_signed": "Newtonian source term can be read as a measurement of parent coupling, not a circular input",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_5_boundary_and_falloff_class",
            "uniqueness_clause": "boundary terms, references, corners and falloff are fixed before readout",
            "MTS_evidence": "2406 keeps boundary/reference operator and 2477 keeps Green/boundary conditions symbolic",
            "status": "BLOCKED_BY_BOUNDARY_CLASS",
            "blocker": "shared local boundary/falloff class plus GHY/reference/corner ownership",
            "effect_if_signed": "EH plus boundary can be separated from physical residual stress without laundering readout choices",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_6_coefficient_owner",
            "uniqueness_clause": "coefficient multiplying the EH-leading operator is owned by parent normalization",
            "MTS_evidence": "2482/2483 retain e_kappaG because kappa0=8*pi*G_ref/c^4 is conditional, not parent-derived",
            "status": "BLOCKED_BY_COUPLING_OWNER",
            "blocker": "derive kappa_MTS or primitive scale/coupling before using G_ref as a measurement",
            "effect_if_signed": "G_parent becomes downstream of the theory rather than an input smuggled from local gravity",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "HYP2484_7_no_hidden_preferred_frame",
            "uniqueness_clause": "local branch has no surviving preferred-frame/time/memory structure in PPN-sensitive equations",
            "MTS_evidence": "memory/coframe and clock/tau residuals remain live in 2406 and 2482",
            "status": "BLOCKED_BY_FRAME_TAU_LOCK",
            "blocker": "terminal public coframe, tau_source=tau_charge=tau_clock=tau_readout, and PPN residual vector",
            "effect_if_signed": "local GR can approach PPN gamma=beta=1 without hidden alpha_i leakage",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "THM2484_0_conditional_uniqueness_statement",
            "statement": "If HYP2484_0..7 are signed, then the local second-order diffeomorphism-invariant public metric/coframe equation has EH+Lambda as its leading rank-2 operator, up to boundary/topological terms and separately bounded residuals.",
            "derivation_status": "CONDITIONAL_THEOREM_SHAPE",
            "proof_content": "standard uniqueness logic: local diffeomorphism invariance plus metric/coframe field plus second-order equations plus no extra tensors leaves Einstein tensor, cosmological term, and boundary/topological improvements at leading order",
            "missing": "all MTS hypotheses are not parent-signed simultaneously",
            "claim_effect": "does not set e_EH_import=0 until hypotheses are supplied by MTS primitives",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2484_1_current_corpus_application",
            "statement": "Apply the conditional uniqueness theorem to current MTS checkpoint state.",
            "derivation_status": "FAILS_CURRENT_HYPOTHESIS_GATE",
            "proof_content": "HYP2484_2, HYP2484_3, HYP2484_4, HYP2484_5, HYP2484_6 and HYP2484_7 remain blocked; HYP2484_0 and HYP2484_1 remain partial/unsigned",
            "missing": "field list, symmetry generator, derivative grammar, residual silence, matter descent, boundary class, coefficient owner",
            "claim_effect": "EH remains a conditional candidate template, not a derived MTS leading operator",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2484_2_parent_normal_form_requirement",
            "statement": "A future parent action must reduce locally to S_parent = int sqrt(-g)[a0 + a1 R] + S_top + S_boundary + S_res, with every S_res coefficient zeroed by parent identity or carried to local tests.",
            "derivation_status": "EXACT_CONTRACT_WRITTEN_NONCLAIM",
            "proof_content": "normal form separates the desired EH-leading term from residual sectors instead of hiding them inside notation",
            "missing": "parent action that supplies a0, a1, field domains, derivative grammar, elimination map, and residual coefficient ownership",
            "claim_effect": "defines the contract required to make EH origin testable rather than philosophical",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def normal_form_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "blocker_id": "NFB2484_0_parent_field_list",
            "normal_form_slot": "Phi_parent -> {g/e, matter, auxiliary, q, tau, memory, projector/boundary data}",
            "required_signature": "which variables are physical, auxiliary, vertical, boundary, or readout-only",
            "current_status": "MISSING_TYPED_PARENT_FIELD_LIST",
            "source_evidence": "2483 EH parent origin and 2236 auxiliary sort remain unsigned",
            "next_action": "write the parent field/sort table before deriving any EH uniqueness claim",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_1_symmetry_generator",
            "normal_form_slot": "Diff(M) or equivalent parent gauge symmetry",
            "required_signature": "Noether identity whose public projection gives covariant conservation",
            "current_status": "MISSING_PARENT_DIFF_GENERATOR",
            "source_evidence": "2405 Bianchi condition is a compatibility filter, not a parent zero theorem",
            "next_action": "derive the local symmetry generator and its action on q/e/matter variables",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_2_derivative_order_grammar",
            "normal_form_slot": "allowed local operators",
            "required_signature": "ban or demote higher-curvature, vertical derivative, projector derivative and boundary derivative operators",
            "current_status": "MISSING_OPERATOR_GRAMMAR",
            "source_evidence": "2406 c_HD and 2236 no-derivative grammar remain conditional",
            "next_action": "prove the parent object language admits only the two-derivative public curvature scalar at leading local order",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_3_elimination_and_descent_map",
            "normal_form_slot": "integrate out or quotient auxiliary/private variables",
            "required_signature": "Hessian/constraint/vertical-null proof that eliminated variables leave no local stress tensor",
            "current_status": "MISSING_ELIMINATION_PROOF",
            "source_evidence": "2406 auxiliary, projector, q and memory sectors remain nonzero/nonbounded",
            "next_action": "construct descent map with explicit residual rows for anything not killed",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_4_boundary_variational_class",
            "normal_form_slot": "S_boundary, B_ref, corner/reference/falloff terms",
            "required_signature": "well-posed variation and zero physical boundary stress in local tests",
            "current_status": "MISSING_BOUNDARY_CLASS",
            "source_evidence": "2406 boundary/reference row and 2477 Green/boundary certificate remain open",
            "next_action": "fix boundary/falloff class before using local vacuum or worldtube limits",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_5_EH_coefficient_owner",
            "normal_form_slot": "a1 = 1/(2*kappa_MTS)",
            "required_signature": "parent normalization, primitive scale, or dimensionless coupling that determines kappa_MTS",
            "current_status": "MISSING_COEFFICIENT_OWNER",
            "source_evidence": "2482/2483 retain e_kappaG",
            "next_action": "derive a1 from parent normalization or declare it an empirical coupling parameter explicitly",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "NFB2484_6_residual_budget",
            "normal_form_slot": "S_res = sum_i c_i O_i",
            "required_signature": "all non-EH operators have zero certificates or source-backed local bounds",
            "current_status": "MISSING_RESIDUAL_BOUNDS",
            "source_evidence": "2405/2406 residual sectors retained; 2477 C_metric factors symbolic",
            "next_action": "keep residual vector explicit through PPN/R10/clocks/orbits instead of claiming local GR",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_update_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "ERES2484_0_e_EH_import",
            "symbol": "e_EH_import",
            "definition": "logic residual for using an EH template before deriving it from MTS parent primitives",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "HYP2484_0..7 signed plus parent normal form gives EH-leading operator",
            "reason_retained": "conditional uniqueness theorem cannot be applied to current corpus",
            "valid_for_claim": False,
        },
        {
            "residual_id": "ERES2484_1_e_kappaG",
            "symbol": "e_kappaG",
            "definition": "coupling residual between parent-derived kappa_MTS and measured kappa_ref",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "normal form supplies a1=1/(2*kappa_MTS) before G_ref is used as measurement",
            "reason_retained": "coefficient owner remains one of the unsigned uniqueness hypotheses",
            "valid_for_claim": False,
        },
        {
            "residual_id": "ERES2484_2_e_EH_hypotheses",
            "symbol": "e_EH_hyp",
            "definition": "aggregate residual for unsigned EH-uniqueness hypotheses",
            "status": "ADD_NONCLAIM_BOOKKEEPING",
            "zero_condition": "every HYP2484 row reaches parent-signed PASS with no residual sector escape",
            "reason_retained": "current failure is hypothesis-level, not just coefficient-level",
            "valid_for_claim": False,
        },
        {
            "residual_id": "ERES2484_3_DeltaE_MTS",
            "symbol": "DeltaE_MTS",
            "definition": "sum of retained non-EH operator residual sectors in the public field equation",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "normal form eliminates or bounds all residual sectors below local thresholds",
            "reason_retained": "2405/2406 no-sector-zero verdict still applies",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2484_0_conditional_uniqueness",
            "claim": "A Lovelock-like EH uniqueness route is mathematically available as a conditional theorem shape.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "The required hypothesis contract is now explicit.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2484_1_MTS_signs_hypotheses",
            "claim": "Current MTS corpus signs every EH-uniqueness hypothesis.",
            "gate_status": "BLOCKED",
            "reason": "field list, symmetry, derivative grammar, residual sectors, boundary class, source descent, and coefficient owner are not all signed.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2484_2_EH_origin",
            "claim": "MTS derives the EH-leading local operator.",
            "gate_status": "BLOCKED",
            "reason": "conditional theorem cannot be applied until HYP2484_0..7 close.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2484_3_kappa_owner",
            "claim": "kappa_MTS/G_parent is parent-owned.",
            "gate_status": "BLOCKED",
            "reason": "normal form coefficient a1 is not sourced.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2484_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived.",
            "gate_status": "BLOCKED",
            "reason": "EH origin, coupling owner, residual silence/bounds, source normalization, and PPN second-order equations remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2484_5_no_shortcuts",
            "claim": "No EH import, fitted GM, M_H_ref reuse, no-derivative-by-taste, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "2484 turns every shortcut into an explicit blocker/residual row.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2484_0_result",
            "decision": "Keep EH uniqueness as the best derivation route, but do not claim it yet.",
            "reason": "The route is legitimate only once MTS supplies its own hypothesis signatures.",
            "effect": "we have moved from vague EH/coupling fog to a finite parent-normal-form contract.",
        },
        {
            "decision_id": "DEC2484_1_best_next",
            "decision": "Attack the parent normal-form field/symmetry/derivative grammar first.",
            "reason": "Without the object language, individual residual zeros keep turning into conditional closures.",
            "effect": "2485 should write the parent normal-form skeleton and identify the first missing proof owner.",
        },
        {
            "decision_id": "DEC2484_2_fallback",
            "decision": "Keep EFT-leading-operator route as a fallback, not the main claim.",
            "reason": "EFT can honestly publish residual coefficients, but it is weaker than deriving GR from MTS primitives.",
            "effect": "public language should say conditional/effective unless 2485+ closes the normal form.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2484_0_selected",
            "selection_status": "selected",
            "target_file": "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
            "target_script": "scripts/Y5_R2FR_parent_normal_form_field_symmetry_derivative_grammar_2485.py",
            "task": "construct the minimal parent normal-form skeleton: typed fields/sorts, quotient map, symmetry generator, allowed derivative grammar, boundary class, coefficient slots, and residual sectors",
            "acceptance_target": "one normal-form contract with pass/block rows for every EH-uniqueness hypothesis and a clear next proof owner",
            "guardrails": "no EH import as proof; no fitted GM; no no-derivative-by-taste; no residual cancellation without parent identity; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "hypothesis_audit": OUTPUTS["hypothesis_audit"],
        "normal_form_blockers": OUTPUTS["normal_form_blockers"],
        "residual_update": OUTPUTS["residual_update"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2484_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2484_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2484_01_hypotheses_all_nonclaim",
        all(row["valid_for_claim"] is False for row in data["hypotheses"]),
        "all EH-uniqueness hypothesis rows remain nonclaim",
    )
    add(
        "VAL2484_02_derivative_grammar_blocked",
        any(row["hypothesis_id"] == "HYP2484_2_locality_and_derivative_order" and row["status"] == "BLOCKED_BY_DERIVATIVE_GRAMMAR" for row in data["hypotheses"]),
        "derivative-order uniqueness clause is explicitly blocked",
    )
    add(
        "VAL2484_03_residual_sectors_blocked",
        any(row["hypothesis_id"] == "HYP2484_3_no_extra_local_tensors" and row["status"] == "BLOCKED_BY_LIVE_RESIDUAL_SECTORS" for row in data["hypotheses"]),
        "live non-EH residual sectors block EH promotion",
    )
    add(
        "VAL2484_04_coupling_retained",
        any(row["symbol"] == "e_kappaG" and row["status"] == "RETAIN_NONCLAIM" for row in data["residuals"]),
        "e_kappaG remains retained",
    )
    add(
        "VAL2484_05_EH_import_retained",
        any(row["symbol"] == "e_EH_import" and row["status"] == "RETAIN_NONCLAIM" for row in data["residuals"]),
        "e_EH_import remains retained",
    )
    add(
        "VAL2484_06_normal_form_contract_written",
        any(row["theorem_id"] == "THM2484_2_parent_normal_form_requirement" for row in data["theorems"]),
        "parent normal-form contract is written",
    )
    add("VAL2484_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2484_08_next_target_written",
        any(row["route_id"] == "NEXT2484_0_selected" for row in data["next"]),
        "2485 parent normal-form skeleton target selected",
    )
    add("VAL2484_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2484*", "*P8_Y5_EH_UNIQUENESS_2484*", "*JR2484*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2484_10_no_formalization_artifacts", not formalization_artifacts, "no 2484 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2484_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2484_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2484_OVERALL",
        overall,
        "2484 writes the EH-uniqueness hypothesis contract, blocks current promotion, retains e_EH_import/e_kappaG, and selects parent normal form next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2484 Y5 R2FR EH Uniqueness Hypotheses Or Parent Normal Form Blocker",
        "",
        "**Status:** EH uniqueness is a viable derivation route, but current MTS sources do not yet sign the hypotheses required to use it as a GR-reduction proof.",
        "",
        "**Main result:** the route is no longer foggy. To earn EH rather than import it, MTS must provide a parent normal form with a public metric/coframe, local diffeomorphism symmetry, two-derivative leading grammar, no surviving extra local tensors, matter descent, boundary/falloff class, and coefficient owner. Current corpus fails that full gate, so `e_EH_import`, `e_kappaG`, `e_EH_hyp`, and `DeltaE_MTS` remain explicit nonclaim residuals.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## EH Uniqueness Hypothesis Audit",
        markdown_table(data["hypotheses"], ["hypothesis_id", "uniqueness_clause", "MTS_evidence", "status", "blocker", "effect_if_signed", "valid_for_claim"]),
        "",
        "## Conditional Theorem Attempt",
        markdown_table(data["theorems"], ["theorem_id", "statement", "derivation_status", "proof_content", "missing", "claim_effect", "valid_for_claim"]),
        "",
        "## Parent Normal Form Blockers",
        markdown_table(data["blockers"], ["blocker_id", "normal_form_slot", "required_signature", "current_status", "source_evidence", "next_action", "valid_for_claim"]),
        "",
        "## Residual Update",
        markdown_table(data["residuals"], ["residual_id", "symbol", "definition", "status", "zero_condition", "reason_retained", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "hypotheses": hypothesis_rows(),
        "theorems": theorem_attempt_rows(),
        "blockers": normal_form_blocker_rows(),
        "residuals": residual_update_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["hypothesis_audit"], data["hypotheses"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorems"])
    write_csv(OUTPUTS["normal_form_blockers"], data["blockers"])
    write_csv(OUTPUTS["residual_update"], data["residuals"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
