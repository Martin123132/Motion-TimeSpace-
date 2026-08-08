from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_BOUNDARY_DOMAIN_SELECTOR_CONTINUITY_NO_CROSSING_OR_CLASS_LEAK_VALUES_2387"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2387-Y5-R2FR-boundary-domain-selector-continuity-no-crossing-or-class-leak-values.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2387_00_2386_doc",
            "source_key": "2386_doc",
            "source_path": POST_ROOT / "2386-Y5-R2FR-Ctop-superselection-from-parent-topology-or-class-leak-row.md",
            "needles": ["domain selector/no-crossing certificate", "Delta_ref_class_leak"],
            "source_role": "2386 selected domain/no-crossing as next gate",
        },
        {
            "row_id": "SRC2387_01_2386_certs",
            "source_key": "2386_certs",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2386_SELECTOR_CERTIFICATE_MATRIX.csv",
            "needles": ["CSC2386_0_domain_selector", "CSC2386_2_no_crossing"],
            "source_role": "domain/no-crossing certificate gaps",
        },
        {
            "row_id": "SRC2387_02_domain_parent_clause",
            "source_key": "domain_parent_clause",
            "source_path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
            "needles": ["C0_parent_domain_sector", "C4_topological_projector"],
            "source_role": "older parent domain selector clause",
        },
        {
            "row_id": "SRC2387_03_668_boundary_lock",
            "source_key": "668_boundary_lock",
            "source_path": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "needles": ["BCL668_2_relative_class", "BCL668_6_worldtube_linking_surfaces"],
            "source_role": "relative class and worldtube linking-surface lock",
        },
        {
            "row_id": "SRC2387_04_2183_doc",
            "source_key": "2183_doc",
            "source_path": POST_ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            "needles": ["W_source := supp(J_H[e_obs,tau])", "source-free annulus"],
            "source_role": "worldtube/Hilbert selector and source-free annulus route",
        },
        {
            "row_id": "SRC2387_05_1016_doc",
            "source_key": "1016_doc",
            "source_path": POST_ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "needles": ["W_source := closure(supp J_H[tau])", "linking surfaces are homologous"],
            "source_role": "parent worldtube/source-measure selector contract",
        },
        {
            "row_id": "SRC2387_06_61_doc",
            "source_key": "61_bound_domain",
            "source_path": POST_ROOT / "61-bound-domain-boundary-theorem-attempt.md",
            "needles": ["parent action still has to derive the boundary/domain selector", "exact domain selector is still not derived"],
            "source_role": "domain selector not derived precedent",
        },
        {
            "row_id": "SRC2387_07_1760_doc",
            "source_key": "1760_worldtube",
            "source_path": POST_ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["W_source=closure(supp J_H[tau])", "MISSING_PARENT_WORLDTUBE_SUPPORT_OWNER"],
            "source_role": "worldtube support owner open",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def domain_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNC2387_0_worldtube_selector",
            "step": "parent worldtube selector",
            "statement": "Define W_source := closure(supp J_H[tau]) before readout; admissible S_inner,S_outer link the same W_source.",
            "condition": "parent action owns J_H, tau, compact support and same-frame source measure",
            "result": "domain is selected by Hilbert support rather than fitted radius/mass",
            "current_gap": "J_H/worldtube owner remains unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNC2387_1_no_crossing",
            "step": "source-free annulus no-crossing",
            "statement": "If A is the annulus with boundary S_outer-S_inner and A cap W_source is empty, source variations that keep supp(J_H) inside W_source do not change the linking class.",
            "condition": "compact support, no source crossing S_inner/S_outer, fixed tau/frame and continuous source path",
            "result": "C_top is constant along that path",
            "current_gap": "no-crossing and support-continuity certificate missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNC2387_2_domain_continuity",
            "step": "domain continuity",
            "statement": "A continuous family of admissible domains in the same exterior homology class has no class jump unless support crosses the boundary or topology changes.",
            "condition": "domain selector is continuous and does not retune surfaces after readout",
            "result": "D_source C_top=0 conditionally follows from domain continuity",
            "current_gap": "parent continuity/no-retune rule missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNC2387_3_failure_modes",
            "step": "failure modes",
            "statement": "If support crosses the annulus, surfaces are retuned, J_H is not parent-owned, or a topology-changing event occurs, class leak rows are required.",
            "condition": "none",
            "result": "class leak is the honest fallback",
            "current_gap": "finite class-leak values missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNC2387_4_verdict",
            "step": "current verdict",
            "statement": "The domain/no-crossing theorem is sharp but conditional; current MTS does not parent-sign the worldtube/domain selector.",
            "condition": "J_H ownership, support compactness, no-crossing and same-frame M_H_ref remain missing",
            "result": "do not promote C_top superselection; keep class leak rows nonclaim",
            "current_gap": "parent worldtube selector and M_H_ref",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_0_JH",
            "certificate": "parent-owned Hilbert current J_H[tau]",
            "required_test": "J_H derived from parent matter variation before readout",
            "status": "MISSING_PARENT_JH_OWNER",
            "residual_if_missing": "worldtube_selector_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_1_support",
            "certificate": "compact regular source support",
            "required_test": "W_source compact/regular and selected before source/readout",
            "status": "MISSING_COMPACT_SUPPORT_CERTIFICATE",
            "residual_if_missing": "support_tail_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_2_linking_surfaces",
            "certificate": "linked homologous surfaces",
            "required_test": "S_inner and S_outer are homologous in the exterior and link the same W_source",
            "status": "MISSING_LINKING_SURFACE_CERTIFICATE",
            "residual_if_missing": "domain_linking_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_3_no_crossing",
            "certificate": "no source crossing annulus",
            "required_test": "A cap W_source remains empty along the allowed source-variation path",
            "status": "MISSING_NO_CROSSING_CERTIFICATE",
            "residual_if_missing": "class_jump_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_4_no_retune",
            "certificate": "no post-readout domain retune",
            "required_test": "domain/surface rule fixed before residual, GM, orbit or PPN readout",
            "status": "MISSING_NO_RETUNE_CERTIFICATE",
            "residual_if_missing": "domain_retune_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DCC2387_5_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "finite positive denominator in same tau/frame as domain and C_top",
            "status": "MISSING_POSITIVE_MHREF",
            "residual_if_missing": "all class leak rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_value_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DLV2387_0_worldtube_selector",
            "quantity": "epsilon_W_selector_class",
            "formula": "abs(Delta C_top_from_W_selector * K_class)/M_H_ref",
            "current_value": "MISSING_WORLDTUBE_SELECTOR_DELTA;MISSING_K_CLASS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DLV2387_1_crossing",
            "quantity": "epsilon_crossing_class",
            "formula": "abs(Delta C_top_crossing * K_crossing)/M_H_ref",
            "current_value": "MISSING_CROSSING_EVENT_SCALE;MISSING_K_CROSSING;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DLV2387_2_retune",
            "quantity": "epsilon_domain_retune",
            "formula": "abs(partial_readout C_top * readout_retune_scale)/M_H_ref",
            "current_value": "MISSING_RETUNE_DERIVATIVE;MISSING_RETUNE_SCALE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DLV2387_3_total",
            "quantity": "Delta_ref_class_domain_total_over_MH",
            "formula": "absolute sum of worldtube selector, crossing, topology-change and retune leaks over M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2387_0_conditional_gain",
            "decision": "accept no-crossing domain theorem as conditional route",
            "reason": "a parent-owned Hilbert worldtube and source-free annulus make the relative class locally constant",
            "consequence": "C_top zero route is tied to worldtube/Hilbert selector, not arbitrary topology words",
            "status": "CONDITIONAL_DOMAIN_THEOREM_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2387_1_no_promotion",
            "decision": "do not promote domain/no-crossing theorem",
            "reason": "parent-owned J_H, compact support, linking surfaces, no-crossing, no-retune and M_H_ref remain missing",
            "consequence": "class leak values remain nonclaim",
            "status": "DOMAIN_SELECTOR_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2387_2_next",
            "decision": "attack parent-owned J_H/worldtube support or fill values",
            "reason": "without J_H ownership, W_source is a label not a derived selector",
            "consequence": "2388 should try to derive parent Hilbert current/worldtube support or source-pack selector leak values",
            "status": "SELECT_2388_PARENT_JH_WORLDTUBE",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_0_no_crossing_shape",
            "gate": "domain no-crossing theorem shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "future route for C_top continuity",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_1_parent_JH",
            "gate": "parent-owned Hilbert current/worldtube selector",
            "gate_status": "FAIL",
            "claim_effect": "W_source not claim-grade",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_2_no_crossing",
            "gate": "no source crossing linked annulus",
            "gate_status": "FAIL",
            "claim_effect": "class jump leak remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_3_no_retune",
            "gate": "domain/surface rule fixed before readout",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "retune leak remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "domain leak rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2387_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "domain/source/reference gates remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2387_0_pick_domain",
            "claim": "choose source domain after readout and call C_top fixed",
            "allowed": "false",
            "reason": "domain must be selected by parent J_H/support before residual or orbital data",
            "blocking_rows": "DCC2387_0_JH;DCC2387_4_no_retune",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2387_1_ignore_crossing",
            "claim": "ignore source crossing/topology-change events",
            "allowed": "false",
            "reason": "class local constancy only holds within one admissible no-crossing component",
            "blocking_rows": "DNC2387_3_failure_modes;DCC2387_3_no_crossing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2387_2_score_leaks",
            "claim": "score class/domain leak rows now",
            "allowed": "false",
            "reason": "component values and M_H_ref are missing",
            "blocking_rows": "DLV2387_0_worldtube_selector;DLV2387_3_total;CG2387_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2387_0_selected",
            "next_file": "2388-Y5-R2FR-parent-Hilbert-current-worldtube-support-or-selector-leak-values.md",
            "success_condition": "derive parent-owned J_H[tau] and W_source=closure(supp J_H[tau]) with compact support before readout",
            "fallback_condition": "fill epsilon_W_selector_class and crossing/retune class leak values with units/source paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2387_1_parallel",
            "next_file": "2388b-Y5-R2FR-source-free-pairing-for-selector-or-pairing-stress-row.md",
            "success_condition": "prove selector pairing is topological/source-free and has no metric/readout stress",
            "fallback_condition": "retain selector_pairing_stress_leak row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2387_2_parallel",
            "next_file": "2388c-Y5-R2FR-MHref-sidecar-or-normalized-residual-stays-unscored.md",
            "success_condition": "derive positive same-frame M_H_ref",
            "fallback_condition": "keep normalized rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2387_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2387_DOMAIN_NO_CROSSING_THEOREM.csv": domain_theorem_rows,
    "P8_Y5_PARENT_QLOC_2387_DOMAIN_CERTIFICATE_MATRIX.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2387_CLASS_DOMAIN_LEAK_VALUES.csv": leak_value_rows,
    "P8_Y5_PARENT_QLOC_2387_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2387_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2387_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2387_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2387_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2387_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = domain_theorem_rows()
    add(
        "VAL2387_02_no_crossing_theorem_present",
        any(row["row_id"] == "DNC2387_1_no_crossing" for row in theorem),
        "no-crossing theorem row present",
    )
    certs = certificate_rows()
    add(
        "VAL2387_03_certificates_missing_explicit",
        all("MISSING" in row["status"] for row in certs),
        "JH/support/linking/no-crossing/no-retune/MHref gaps explicit",
    )
    values = leak_value_rows()
    add(
        "VAL2387_04_value_rows_nonready",
        all(row["score_ready"] == "false" for row in values),
        "class/domain leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2387_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2387_0_no_crossing_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2387_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2387_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2387_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2387_09_next_selected",
        any(row["row_id"] == "NEXT2387_0_selected" for row in next_target_rows()),
        "parent Hilbert current/worldtube support selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2387_OVERALL",
        overall,
        "2387 derives conditional domain/no-crossing route, refuses promotion without parent JH/worldtube/support/MHref, and selects parent Hilbert current next",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_DOMAIN_NO_CROSSING_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_DOMAIN_CERTIFICATE_MATRIX.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_CLASS_DOMAIN_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2387_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2387_VALIDATION.csv")

    body = f"""# 2387 - boundary-domain selector continuity no-crossing or class-leak values

## Result

2387 connects the `C_top` local-constancy route to the GR-like compact-source/worldtube route:

`W_source := closure(supp J_H[tau])`,

with linked surfaces `S_inner` and `S_outer` enclosing the same source and a source-free annulus between them.

If the parent action owns `J_H`, source support is compact, the linked surfaces are fixed before readout, and no source
support crosses the annulus along the allowed variation, then the linking/domain class is continuous and `C_top` cannot
jump.  That gives a conditional no-crossing route to `D_source C_top=0`.

But current MTS still lacks parent-owned `J_H`, compact support, linking/no-crossing/no-retune certificates, and
positive same-frame `M_H_ref`.  So this is not promoted.  The class/domain leak rows remain nonclaim.

No `C_top` pass, `Delta_ref=0`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Domain No-Crossing Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "condition", "result", "current_gap", "valid_for_claim"])}

## Domain Certificate Matrix

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Class Domain Leak Values

{markdown_table(values, ["row_id", "quantity", "formula", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

The no-crossing route is a serious bridge toward GR/Newton source normalization because it uses a parent Hilbert
worldtube rather than an arbitrary boundary.  But the next missing object is now unavoidable: parent-owned `J_H[tau]`
and `W_source`.  Without that, the domain is still a label and not a theorem.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2387_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2387_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
