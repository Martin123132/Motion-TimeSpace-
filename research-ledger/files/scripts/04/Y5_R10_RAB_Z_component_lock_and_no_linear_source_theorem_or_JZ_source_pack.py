from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1353"
TITLE = "1353-Y5-R10-RAB-Z-component-lock-and-no-linear-source-theorem-or-JZ-source-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMPONENT_LOCK_PATH = OUT_DIR / f"{PACK_ID}_Z_COMPONENT_LOCK_ATTEMPT.csv"
NO_LINEAR_PATH = OUT_DIR / f"{PACK_ID}_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv"
JZ_SOURCE_PACK_PATH = OUT_DIR / f"{PACK_ID}_JZ_BZ_SOURCE_PACK.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1353_VALIDATION.csv"


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1353_0_1352_doc",
            "source_path": "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md",
            "required_anchor": "Current verdict",
            "purpose": "1352 says the physical coupling map is the missing piece.",
        },
        {
            "source_id": "SRC1353_1_1352_blockers",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1352_CONJUGACY_BLOCKER_AUDIT.csv",
            "required_anchor": "BLK1352_0_component_lock",
            "purpose": "handoff blockers: component lock and no-linear-source theorem.",
        },
        {
            "source_id": "SRC1353_2_response_contract",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "required_anchor": "RD516_4_zero_odd_source",
            "purpose": "source-normalization and Y6 extra-stress remain hard blocks.",
        },
        {
            "source_id": "SRC1353_3_response_variation",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "required_anchor": "AV517_4_Euler_equation",
            "purpose": "Z Euler equation blocked by source-current rows.",
        },
        {
            "source_id": "SRC1353_4_1011_qbound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
            "required_anchor": "QBF1011_6_Y6_extra_stress",
            "purpose": "Y5 and Y6 retained q_loc/source rows.",
        },
        {
            "source_id": "SRC1353_5_1012_y5",
            "source_path": "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            "required_anchor": "Y5C1012_0_radial_Meff_hair",
            "purpose": "Y5 source-normalization eight-channel obstruction.",
        },
        {
            "source_id": "SRC1353_6_1345_source_charge",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1345_SOURCE_CHARGE_RUNNER_INPUTS.csv",
            "required_anchor": "QIN1345_4_4_memory_class_scalar",
            "purpose": "current source-charge rows reject symbolic closure-only inputs.",
        },
        {
            "source_id": "SRC1353_7_1352_profile",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1352_QLOC_PROFILE_SOURCE_ROW.csv",
            "required_anchor": "QPROF1352_0_minimal_residual_source",
            "purpose": "first q_loc finite source vector row.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def component_lock_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "lock_id": "ZLOCK1353_0_definition",
            "claim_piece": "Z^A is a response doublet coordinate",
            "required_map": "Z^A=(R_+^A-R_-^A)/2 is parent-defined before readout",
            "current_evidence": "AV517_0 conditional_not_component_derived",
            "status": "CONDITIONAL_ONLY",
            "failure_mode": "formal coordinate may not equal physical local residual",
        },
        {
            "lock_id": "ZLOCK1353_1_component_coverage",
            "claim_piece": "Z^A covers Y0-Y6 physical leakage channels",
            "required_map": "Z^A -> {PPN, source-normalization, extra-stress, clock/readout, R10, orbital} components",
            "current_evidence": "RD516_0 partial_from_494_Y2_Y3_only_conditional",
            "status": "NOT_COVERED",
            "failure_mode": "source normalization and extra stress can sit outside the doublet",
        },
        {
            "lock_id": "ZLOCK1353_2_observable_lock",
            "claim_piece": "Z^A equals q_loc/PPN/source-normalization residual vector",
            "required_map": "Z^A=Y_loc^A through beta,gamma,alpha_i,xi,Gdot,R11,R10,clock,orbital order",
            "current_evidence": "RD516_5 not_derived; 1351 q_loc rows template-only",
            "status": "NOT_DERIVED",
            "failure_mode": "double-zero may erase a shadow variable while physical residual remains",
        },
        {
            "lock_id": "ZLOCK1353_3_readout_order",
            "claim_piece": "component map is fixed before readout/reduction",
            "required_map": "parent variation sees the same fields that the observable projection later measures",
            "current_evidence": "source/readout rows remain unsigned across 1012 and 1345",
            "status": "UNSIGNED",
            "failure_mode": "post-readout projection can regenerate linear source terms",
        },
        {
            "lock_id": "ZLOCK1353_4_verdict",
            "claim_piece": "component lock theorem",
            "required_map": "ZLOCK1353_0..3 all source-backed",
            "current_evidence": "component coverage and observable lock fail",
            "status": "COMPONENT_LOCK_NOT_PROVED",
            "failure_mode": "cannot use formal F1=0 as physical q_loc/local-GR zero",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def no_linear_source_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "theorem_id": "NLS1353_0_exchange_symmetry",
            "premise": "source and matter functionals are even under R_+ <-> R_-",
            "required_condition": "S_source[R_+,R_-]=S_source[R_-,R_+] with no odd spurion labels",
            "current_status": "NOT_PARENT_SIGNED",
            "consequence_if_true": "delta S_source/delta Z^A at Z=0 vanishes",
        },
        {
            "theorem_id": "NLS1353_1_source_pullback",
            "premise": "ordinary matter/source normalization pulls back only through R_even/q_loc-visible data",
            "required_condition": "no source measures, masses, clocks, or boundary references depend linearly on Z",
            "current_status": "FAILED_CURRENT_EVIDENCE",
            "consequence_if_true": "J_Z=0 for matter/source channels",
        },
        {
            "theorem_id": "NLS1353_2_boundary_exactness",
            "premise": "boundary/source-current terms are exchange-even or exact with zero linked flux",
            "required_condition": "B_Z=0 or fixed topological subtraction before readout",
            "current_status": "OPEN",
            "consequence_if_true": "boundary term cannot reintroduce linear q_loc force",
        },
        {
            "theorem_id": "NLS1353_3_Y5_source_normalization",
            "premise": "measured-GM/source-normalization is exchange-even and parent-owned",
            "required_condition": "Y5 eight-channel vector has theorem-zero or numeric bound rows",
            "current_status": "NOT_DERIVED_HARD_BLOCK",
            "consequence_if_true": "Y5 does not act as J_Z source charge",
        },
        {
            "theorem_id": "NLS1353_4_Y6_extra_stress",
            "premise": "extra-stress response is invisible/topological or bounded",
            "required_condition": "T_extra has no linear Z response in PPN/source-normalization channels",
            "current_status": "NOT_DERIVED_HARD_BLOCK",
            "consequence_if_true": "Y6 does not spoil Khat/Ward silence",
        },
        {
            "theorem_id": "NLS1353_5_verdict",
            "premise": "no-linear-source theorem",
            "required_condition": "NLS1353_0..4 all pass with source paths",
            "current_status": "THEOREM_NOT_PROVED",
            "consequence_if_true": "response-doublet F1=0 could become physical rather than formal",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def jz_source_pack() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "JZ1353_0_bulk_JZ",
            "symbol": "J_Z^A",
            "definition": "delta S_source/delta Z_A evaluated at Z=0",
            "affected_gate": "q_loc zero; PPN; R10; source-normalization",
            "required_to_score": "numeric vector or theorem-zero certificate with source path",
            "current_status": "MISSING_JZ_THEOREM_OR_VALUE",
        },
        {
            "source_id": "JZ1353_1_boundary_BZ",
            "symbol": "B_Z^A",
            "definition": "linear boundary/source-current term from integrations by parts and linking-sphere flux",
            "affected_gate": "boundary force; M_eff; orbital/source closure",
            "required_to_score": "zero-flux theorem or boundary profile/bound",
            "current_status": "MISSING_BZ_THEOREM_OR_VALUE",
        },
        {
            "source_id": "JZ1353_2_Y5_source_normalization",
            "symbol": "J_Z[Y5]",
            "definition": "measured-GM/source-normalization response projected onto Z",
            "affected_gate": "Newton/GR reduction; R11; Gdot; beta/gamma; alpha(lambda)",
            "required_to_score": "Y5 eight-channel theorem-zero or numeric coefficient vector",
            "current_status": "RETAINED_NONCLAIM_HARD_BLOCK",
        },
        {
            "source_id": "JZ1353_3_Y6_extra_stress",
            "symbol": "J_Z[Y6]; Delta_K[Y6]",
            "definition": "extra stress response that can enter Khat/Ward/q_loc at linear order",
            "affected_gate": "PPN/local-GR; preferred-frame; source stress",
            "required_to_score": "topological invisibility theorem or PPN/source-stress bound",
            "current_status": "RETAINED_NONCLAIM_HARD_BLOCK",
        },
        {
            "source_id": "JZ1353_4_readout_backreaction",
            "symbol": "J_Z[readout]",
            "definition": "post-readout/reduced-action backreaction linear in Z",
            "affected_gate": "clock; EM; WEP; source composition",
            "required_to_score": "readout-after-variation theorem or finite counterterm prior",
            "current_status": "MISSING_READOUT_ZERO_OR_BOUND",
        },
        {
            "source_id": "JZ1353_5_species_material_sources",
            "symbol": "J_Z[species]",
            "definition": "species/source charge vector from visible matter composition",
            "affected_gate": "WEP; clock; source normalization",
            "required_to_score": "parent species-blind theorem or source-backed component charge map",
            "current_status": "MISSING_SPECIES_SOURCE_MAP",
        },
    ]
    for row in rows:
        row["accepted_for_scoring"] = False
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1353_0_component_lock",
            "claim": "Z^A is the physical local residual vector",
            "current_status": "BLOCKED",
            "reason": "component coverage and observable lock are not derived",
        },
        {
            "gate_id": "GATE1353_1_no_linear_source",
            "claim": "J_Z=B_Z=0 for local compact branch",
            "current_status": "BLOCKED",
            "reason": "source pullback, boundary exactness, Y5, and Y6 are not parent-signed",
        },
        {
            "gate_id": "GATE1353_2_response_doublet_local_GR",
            "claim": "response-doublet double-zero proves local GR",
            "current_status": "BLOCKED",
            "reason": "formal F1=0 lacks physical component/source lock",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1353_0_coupling_is_root",
            "decision": "The coupling/source side is now the root obstruction for the response-doublet route.",
            "why": "the quadratic action gives formal double-zero, but Y5/Y6/source/readout can generate linear J_Z terms",
            "next_action": "derive source-functional evenness or fill J_Z/B_Z coefficients",
        },
        {
            "decision_id": "DEC1353_1_no_theory_promotion",
            "decision": "No response-doublet local-GR promotion is allowed.",
            "why": "component lock and no-linear-source theorem both fail current evidence",
            "next_action": "keep all claim gates false",
        },
        {
            "decision_id": "DEC1353_2_best_next_target",
            "decision": "Attack source-functional evenness before empirical scoring.",
            "why": "if the parent source functional is even in Z, J_Z=0 could be derived cleanly; if not, coefficient rows are unavoidable",
            "next_action": "run 1354 source-functional evenness theorem or Y5/Y6 JZ coefficient fill",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1353_0_1354",
            "target_file": "1354-Y5-R10-RAB-source-functional-evenness-theorem-or-Y5Y6-JZ-coefficient-fill.md",
            "target_script": "scripts/Y5_R10_RAB_source_functional_evenness_theorem_or_Y5Y6_JZ_coefficient_fill.py",
            "task": "try to prove the parent source functional is exchange-even in Z for matter, measured-GM, boundary, and extra-stress channels; if not, fill Y5/Y6 J_Z coefficient rows as nonclaim",
            "success_condition": "source-functional evenness theorem, or explicit nonclaim Y5/Y6 J_Z coefficient pack with units/source requirements",
            "do_not": "do not treat exchange symmetry of Gamma_eff as source symmetry; do not ignore Y5/Y6; do not edit formalization-workbench or use GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    locks: list[dict[str, object]],
    theorem: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1353_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    lock_verdict = next(row for row in locks if row["lock_id"] == "ZLOCK1353_4_verdict")
    add(
        "VAL1353_1_component_lock_not_proved",
        "component lock theorem is not promoted",
        lock_verdict["status"] == "COMPONENT_LOCK_NOT_PROVED" and not lock_verdict["claim_allowed"],
        str(lock_verdict["failure_mode"]),
    )

    theorem_verdict = next(row for row in theorem if row["theorem_id"] == "NLS1353_5_verdict")
    add(
        "VAL1353_2_no_linear_source_not_proved",
        "no-linear-source theorem is not promoted",
        theorem_verdict["current_status"] == "THEOREM_NOT_PROVED" and not theorem_verdict["claim_allowed"],
        str(theorem_verdict["required_condition"]),
    )

    required_sources = {"JZ1353_2_Y5_source_normalization", "JZ1353_3_Y6_extra_stress"}
    present_sources = {str(row["source_id"]) for row in source_pack}
    add(
        "VAL1353_3_Y5_Y6_rows_present",
        "JZ source pack includes Y5 and Y6 rows",
        required_sources.issubset(present_sources),
        f"missing={sorted(required_sources - present_sources)}",
    )

    add(
        "VAL1353_4_source_pack_nonclaim",
        "all source-pack rows are rejected for scoring",
        all(not row["accepted_for_scoring"] and not row["claim_allowed"] for row in source_pack),
        f"rows={len(source_pack)}",
    )

    add(
        "VAL1353_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_rows = sources + locks + theorem + source_pack + gates + decisions + next_target
    add(
        "VAL1353_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1353*", "*1353-Y5-R10-RAB-Z-component*", "*Y5_R10_RAB_Z_component*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1353_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1353_8_next_target_1354",
        "next target routes to source-functional evenness theorem",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1354-Y5-R10-RAB-source-functional-evenness"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1353_9_overall",
        "overall 1353 validation",
        all(row["status"] == "PASS" for row in validations),
        "1353 identifies coupling/source evenness as root response-doublet obstruction",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    locks: list[dict[str, object]],
    theorem: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1353 does not prove the response-doublet route. It finds the coupling obstruction precisely: `Z^A` is not yet locked to the physical local residual vector, and `J_Z/B_Z` source terms are not forbidden.",
            "**Main progress:** the failure is useful, not vague. The next theorem must act on the source functional itself: `Gamma_eff` being even in `Z` is not enough unless matter, measured-GM/source-normalization, boundary flux, readout, and extra-stress channels are also exchange-even or theorem-zero.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Z component-lock attempt",
            table(["lock_id", "claim_piece", "required_map", "current_evidence", "status", "failure_mode"], locks),
            "## No-linear-source theorem attempt",
            table(["theorem_id", "premise", "required_condition", "current_status", "consequence_if_true"], theorem),
            "## JZ/BZ source pack",
            table(["source_id", "symbol", "definition", "affected_gate", "current_status", "accepted_for_scoring"], source_pack),
            "## Claim gates",
            table(["gate_id", "claim", "current_status", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    locks = component_lock_attempt()
    theorem = no_linear_source_attempt()
    source_pack = jz_source_pack()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, locks, theorem, source_pack, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(COMPONENT_LOCK_PATH, locks)
    write_csv(NO_LINEAR_PATH, theorem)
    write_csv(JZ_SOURCE_PACK_PATH, source_pack)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, locks, theorem, source_pack, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
