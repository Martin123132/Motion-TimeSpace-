from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_CTOP_SUPERSELECTION_FROM_PARENT_TOPOLOGY_OR_CLASS_LEAK_ROW_2386"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2386-Y5-R2FR-Ctop-superselection-from-parent-topology-or-class-leak-row.md"
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
            "row_id": "SRC2386_00_2385_doc",
            "source_key": "2385_doc",
            "source_path": POST_ROOT / "2385-Y5-R2FR-selector-functional-from-relative-boundary-class-or-Delta-ref-values.md",
            "needles": ["`C_top` superselection", "Delta_ref_class_leak_over_MH"],
            "source_role": "2385 handoff to C_top superselection or class-leak row",
        },
        {
            "row_id": "SRC2386_01_2385_gates",
            "source_key": "2385_component_gates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2385_COMPONENT_GATES.csv",
            "needles": ["RCG2385_0_Crel", "C_TOP_CONTRACT_NOT_PARENT_SELECTED"],
            "source_role": "machine-readable C_rel/C_top blocker",
        },
        {
            "row_id": "SRC2386_02_2385_values",
            "source_key": "2385_value_rows",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2385_DELTA_REF_VALUE_ROWS.csv",
            "needles": ["DRV2385_0_class_leak", "MISSING_CREL_SOURCE_DERIVATIVE"],
            "source_role": "class-leak row template from 2385",
        },
        {
            "row_id": "SRC2386_03_60_doc",
            "source_key": "60_relative_contract",
            "source_path": POST_ROOT / "60-relative-cohomology-boundary-contract.md",
            "needles": ["stationary bound domains carry trivial relative memory class", "relative_boundary_contract_written_not_derived"],
            "source_role": "relative memory class contract",
        },
        {
            "row_id": "SRC2386_04_61_doc",
            "source_key": "61_bound_domain",
            "source_path": POST_ROOT / "61-bound-domain-boundary-theorem-attempt.md",
            "needles": ["parent action still has to derive the boundary/domain selector", "bound_domain_parent_variation_derived"],
            "source_role": "domain selector still missing",
        },
        {
            "row_id": "SRC2386_05_71_doc",
            "source_key": "71_relative_current",
            "source_path": POST_ROOT / "71-relative-boundary-current-construction-attempt.md",
            "needles": ["a formal relative current can be written, but it is not parent-derived yet", "relative_pair_written"],
            "source_role": "relative current written but not parent-derived",
        },
        {
            "row_id": "SRC2386_06_996_doc",
            "source_key": "996_relative_owner",
            "source_path": POST_ROOT / "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
            "needles": ["RBO996_1_Ctop_superselection", "parent Euler/Ward/topological selector fixing C_top before the branch is fitted"],
            "source_role": "older C_top owner theorem failure",
        },
        {
            "row_id": "SRC2386_07_1020_doc",
            "source_key": "1020_domain_certificate",
            "source_path": POST_ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needles": ["relative edge cohomology", "fail_current_claim"],
            "source_role": "boundary domain/cohomology certificate blocker",
        },
        {
            "row_id": "SRC2386_08_1020_domain_csv",
            "source_key": "1020_domain_csv",
            "source_path": RESIDUALS / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv",
            "needles": ["BDC1020_1_boundary_class", "BDC1020_2_relative_cohomology"],
            "source_role": "machine-readable boundary class and cohomology certificate",
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


def superselection_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTS2386_0_discrete_class",
            "step": "discrete relative class",
            "statement": "C_top is a relative cohomology/topological class valued in a discrete or locally constant class set on the selected boundary domain.",
            "condition": "boundary domain and relative class space are parent-selected before readout",
            "result": "continuous source variations inside one connected component cannot change C_top",
            "current_gap": "parent selection of domain/class not derived",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTS2386_1_local_constancy",
            "step": "local constancy theorem",
            "statement": "If C_top is locally constant on the admissible source-variation path, D_source C_top=0.",
            "condition": "no topology-changing event, no source support crosses the annulus, no retuned boundary representative",
            "result": "the C_top part of Delta_ref_class_leak vanishes conditionally",
            "current_gap": "no parent no-crossing/no-topology-change certificate",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTS2386_2_local_FLRW_split",
            "step": "local/FLRW class split",
            "statement": "Stationary local bound domains may carry trivial relative class while coherent FLRW domains carry a nontrivial expansion class.",
            "condition": "domain selector distinguishes stationary bound domains from coherent expansion domains without source fitting",
            "result": "MTS can keep local silence and cosmological memory distinct as a conditional class architecture",
            "current_gap": "domain selector still not parent-derived",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTS2386_3_event_source_law",
            "step": "class-changing events",
            "statement": "Collapse, merger, boundary crossing, or topology-changing events are not zeroed by superselection; they require a class-jump/source law.",
            "condition": "none",
            "result": "class-leak source rows remain necessary for nonstationary or crossing cases",
            "current_gap": "event/source law not derived",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CTS2386_4_verdict",
            "step": "current theorem verdict",
            "statement": "The discrete/local-constancy theorem is valid as a conditional route, but C_top superselection is not parent-owned in current MTS.",
            "condition": "domain/class selector and no-event certificates remain unsigned",
            "result": "do not promote D_source C_top=0; stage Delta_ref_class_leak row",
            "current_gap": "parent topology/Ward selector and no-crossing certificate",
            "valid_for_claim": no_claim(),
        },
    ]


def selector_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_0_domain_selector",
            "certificate": "parent boundary-domain selector",
            "required_test": "parent action/Ward/topology selects D or S0 before source/readout",
            "status": "MISSING_DOMAIN_SELECTOR",
            "if_missing": "C_top can be selected after seeing the source",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_1_class_space",
            "certificate": "discrete relative class space",
            "required_test": "C_top belongs to fixed relative cohomology/topological class set, not a continuous fitted amplitude",
            "status": "CONTRACT_NOT_PARENT_SIGNED",
            "if_missing": "D_source C_top may be continuous and nonzero",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_2_no_crossing",
            "certificate": "no source crosses annulus",
            "required_test": "source support remains inside linked worldtube and does not cross S_inner/S_outer under source variation",
            "status": "MISSING_NO_CROSSED_SOURCE_CERTIFICATE",
            "if_missing": "boundary class can jump or acquire flux",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_3_no_topology_change",
            "certificate": "no topology-changing event",
            "required_test": "no collapse/merger/domain surgery/class-changing event in the variation family",
            "status": "MISSING_EVENT_SOURCE_LAW",
            "if_missing": "class jump must be source-packed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_4_no_marker",
            "certificate": "no material/source marker in class selector",
            "required_test": "partial_(m_A,kappa_A,composition,GM_obs) C_top=0 before source-measure equality",
            "status": "MISSING_NO_MARKER_CERTIFICATE",
            "if_missing": "C_top can encode source composition or fitted GM",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CSC2386_5_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "finite positive denominator with tau/frame shared by class-leak row",
            "status": "MISSING_POSITIVE_MHREF",
            "if_missing": "Delta_ref_class_leak cannot be scored",
            "valid_for_claim": no_claim(),
        },
    ]


def class_leak_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLR2386_0_continuous_leak",
            "quantity": "Delta_ref_class_leak_over_MH",
            "formula": "abs(partial_source C_rel * K_class)/M_H_ref",
            "source_of_leak": "continuous class dependence if C_top is not discrete/locally constant",
            "current_value": "MISSING_PARTIAL_SOURCE_CREL;MISSING_K_CLASS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLR2386_1_jump_leak",
            "quantity": "Delta_ref_class_jump_over_MH",
            "formula": "abs(Delta C_top_event * K_class_event)/M_H_ref",
            "source_of_leak": "collapse/merger/crossing/topology-change event",
            "current_value": "MISSING_EVENT_CLASS_JUMP;MISSING_EVENT_SCALE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLR2386_2_marker_leak",
            "quantity": "Delta_ref_class_marker_leak_over_MH",
            "formula": "sum_abs(partial_marker C_top * marker_scale)/M_H_ref",
            "source_of_leak": "material/composition/GM labels hidden in class selector",
            "current_value": "MISSING_MARKER_DERIVATIVES;MISSING_MARKER_SCALES;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLR2386_3_total",
            "quantity": "Delta_ref_class_total_over_MH",
            "formula": "absolute sum of continuous, jump and marker class leaks over M_H_ref",
            "source_of_leak": "failed C_top superselection",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2386_0_conditional_theorem",
            "decision": "keep discrete/local-constancy C_top theorem as conditional route",
            "reason": "topological/relative classes are locally constant under continuous variations inside one selected domain component",
            "consequence": "D_source C_top=0 has a legitimate future proof shape",
            "status": "CONDITIONAL_CTOP_THEOREM_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2386_1_no_promotion",
            "decision": "do not promote C_top superselection",
            "reason": "domain selector, no-crossing/no-event certificate, no-marker certificate and M_H_ref are missing",
            "consequence": "Delta_ref_class_leak rows remain live",
            "status": "CTOP_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2386_2_next",
            "decision": "attack parent domain selector/no-crossing certificate next",
            "reason": "without a parent-selected domain, C_top can still be a post-readout branch choice",
            "consequence": "2387 should derive boundary-domain selector continuity/no-source-crossing or fill class leak values",
            "status": "SELECT_2387_DOMAIN_SELECTOR",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_0_local_constancy",
            "gate": "discrete class local-constancy theorem shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "future route for D_source C_top=0",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_1_domain_selector",
            "gate": "parent boundary/domain selector",
            "gate_status": "FAIL",
            "claim_effect": "C_top not parent-selected before readout",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_2_no_crossing_event",
            "gate": "no source crossing/topology-change certificate",
            "gate_status": "FAIL",
            "claim_effect": "class jumps remain possible",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_3_no_marker",
            "gate": "no material/GM/source marker in C_top selector",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "class selector may encode source labels",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "class leak rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2386_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "selector/reference/source-measure gates remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2386_0_topology_by_name",
            "claim": "declare C_top source-blind because it is called topological",
            "allowed": "false",
            "reason": "the domain/class selector and no-event/no-marker certificates are missing",
            "blocking_rows": "CSC2386_0_domain_selector;CSC2386_2_no_crossing;CSC2386_4_no_marker",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2386_1_ignore_events",
            "claim": "ignore collapse/merger/crossing class jumps",
            "allowed": "false",
            "reason": "topological class is locally constant only inside one admissible component",
            "blocking_rows": "CTS2386_3_event_source_law;CLR2386_1_jump_leak",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2386_2_score_class_leak",
            "claim": "score Delta_ref_class_leak_over_MH now",
            "allowed": "false",
            "reason": "class derivatives/event scales/marker scales and M_H_ref are missing",
            "blocking_rows": "CLR2386_0_continuous_leak;CLR2386_3_total;CG2386_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2386_0_selected",
            "next_file": "2387-Y5-R2FR-boundary-domain-selector-continuity-no-crossing-or-class-leak-values.md",
            "success_condition": "derive parent-owned boundary/domain selector with continuous source path, no source crossing, no topology change and D_source C_top=0",
            "fallback_condition": "fill Delta_ref_class_leak rows with finite source derivatives/event scales/units/source paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2386_1_parallel",
            "next_file": "2387b-Y5-R2FR-source-free-pairing-for-selector-or-pairing-stress-row.md",
            "success_condition": "prove selector pairing is topological/source-free and has no metric/readout stress",
            "fallback_condition": "retain selector_pairing_stress_leak row",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2386_2_parallel",
            "next_file": "2387c-Y5-R2FR-MHref-sidecar-or-normalized-residual-stays-unscored.md",
            "success_condition": "derive positive same-frame M_H_ref for class/reference residual normalization",
            "fallback_condition": "keep class/reference residuals non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2386_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2386_CTOP_SUPERSELECTION_THEOREM.csv": superselection_theorem_rows,
    "P8_Y5_PARENT_QLOC_2386_SELECTOR_CERTIFICATE_MATRIX.csv": selector_certificate_rows,
    "P8_Y5_PARENT_QLOC_2386_CLASS_LEAK_ROWS.csv": class_leak_rows,
    "P8_Y5_PARENT_QLOC_2386_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2386_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2386_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2386_NEXT_TARGET.csv": next_target_rows,
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
    add("VAL2386_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2386_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = superselection_theorem_rows()
    add(
        "VAL2386_02_local_constancy_present",
        any(row["row_id"] == "CTS2386_1_local_constancy" for row in theorem),
        "local constancy theorem row present",
    )
    certs = selector_certificate_rows()
    add(
        "VAL2386_03_missing_certificates_explicit",
        all("MISSING" in row["status"] or "CONTRACT" in row["status"] for row in certs),
        "domain/class/no-crossing/no-marker/MHref certificate gaps explicit",
    )
    leaks = class_leak_rows()
    add(
        "VAL2386_04_class_leak_rows_nonready",
        all(row["score_ready"] == "false" for row in leaks),
        "class leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2386_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2386_0_local_constancy"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2386_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2386_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2386_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2386_09_next_selected",
        any(row["row_id"] == "NEXT2386_0_selected" for row in next_target_rows()),
        "domain selector/no-crossing selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2386_OVERALL",
        overall,
        "2386 derives conditional C_top local-constancy route, refuses promotion without parent domain/no-crossing/no-marker/MHref certificates, and stages class-leak rows",
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
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_CTOP_SUPERSELECTION_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_SELECTOR_CERTIFICATE_MATRIX.csv")
    leaks = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_CLASS_LEAK_ROWS.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2386_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2386_VALIDATION.csv")

    body = f"""# 2386 - Ctop superselection from parent topology or class-leak row

## Result

2386 gives `C_top` a real conditional theorem shape:

If `C_top` is a discrete relative/topological class selected before readout, and the source variation stays inside one
connected admissible boundary-domain component, then `C_top` is locally constant and `D_source C_top = 0`.

That is useful.  It means the class part of the reference selector can be silent without a fitted cancellation, but only
inside a parent-selected domain with no source crossing, no topology-changing event, and no material/GM marker hidden in
the class selector.

Current MTS does **not** yet supply those certificates.  Therefore `C_top` superselection is not promoted, and
`Delta_ref_class_leak_over_MH` remains a nonclaim source-pack row.

No `Delta_ref=0`, `B_zero_flux=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Ctop Superselection Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "condition", "result", "current_gap", "valid_for_claim"])}

## Selector Certificate Matrix

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "if_missing", "valid_for_claim"])}

## Class Leak Rows

{markdown_table(leaks, ["row_id", "quantity", "formula", "source_of_leak", "current_value", "score_ready", "valid_for_claim"])}

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

This is a good tightening.  The class route is not mystical anymore: discrete topology gives local constancy, but only
after the parent theory selects the domain and excludes crossing/topology-changing events.  The next honest attack is
the domain selector/no-crossing certificate.  If that cannot be derived, `Delta_ref_class_leak` becomes a real residual.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2386_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2386_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
