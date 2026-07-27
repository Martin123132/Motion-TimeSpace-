from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1986-Y5-R2FR-memory-route-finite-residual-vector-pack.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1986_VALIDATION.csv"

SOURCES = {
    "1985_doc": {
        "path": ROOT / "1985-Y5-R2FR-minimal-signature-source-boundary-consistency-gate.md",
        "needles": ["RES1985_0_Jc", "NEXT1985_0_primary"],
    },
    "1985_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1985_VALIDATION.csv",
        "needles": ["VAL1985_OVERALL", "PASS"],
    },
    "1027_qbar": {
        "path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["BQT1027_3_total_abs_guard", "qbar_XT_bound_abs"],
    },
    "1043_jx_phi": {
        "path": ROOT / "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
        "needles": ["RHS1043_3_no_cancellation", "R_X_ZERO_BLOCKED_CURRENT_CORPUS"],
    },
    "1387_weights": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
        "needles": ["DWB1387_4_beta_product_guard", "PRODUCT_FORMULA_READY_VALUES_MISSING"],
    },
    "1012_newton": {
        "path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["GM1012_1_Meff_conservation", "RETAINED_NONCLAIM_CONSTANT_GM_ROW"],
    },
    "1013_flux": {
        "path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_8_verdict", "fail_current_claim"],
    },
    "1033_r10": {
        "path": ROOT / "1033-Y5-R10-tau-R10-projection-derivation-or-source-acquisition.md",
        "needles": ["TAUR1033_5_universal_cg_limit", "R10PC1033_2_KX"],
    },
    "1034_bound": {
        "path": ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
        "needles": ["R10P1034_1_KX_lambda", "MISSING_KERNEL_NORMALIZATION"],
    },
    "1592_signature": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["PSA1592_7_verdict", "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_SOURCE_REGISTER.csv",
    "component_catalog": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_RESIDUAL_COMPONENT_CATALOG.csv",
    "vector_norm": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_NO_CANCELLATION_VECTOR_NORM.csv",
    "arena_matrix": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_ARENA_PROJECTION_MATRIX.csv",
    "source_slots": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_SOURCE_SLOT_TEMPLATE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MEMORY_ROUTE_FINITE_RESIDUAL_VECTOR_1986_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1986_FIRST_BOUND_COMPONENT_SELECTION_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    defaults = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**defaults, **values}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, config in SOURCES.items():
        path = config["path"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in config["needles"] if needle not in text]
        rows.append(
            row(
                {
                    "id": f"SRC1986_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing else "MISSING: " + "; ".join(missing),
                    "role": "finite memory-route residual vector source",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    component_catalog = [
        row(
            {
                "id": "RC1986_0_Jc",
                "component": "J_c_abs",
                "meaning": "absolute bound on canonical memory source after source decomposition",
                "zero_condition": "all J_m channels theorem-zero including matter, source-worldtube, projector/domain, memory/history, source-normalization, constants",
                "bound_formula": "abs_Jc_total >= sum_channel abs(Jc_channel)",
                "units": "canonical field source density or declared arena-normalized source units",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_1_beta",
                "component": "beta_source_abs;beta_test_abs;qbar_XT_abs",
                "meaning": "ordinary source/test coupling of memory scalar to matter/readout",
                "zero_condition": "same-parent q-kernel, observed coframe descent, matter functor, constants and hidden tails close",
                "bound_formula": "abs_qbar_XT <= abs_qbar_geom + abs_qbar_marker + abs_qbar_nonH + abs_qbar_hidden",
                "units": "dimensionless beta or declared canonical inverse-field convention",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_2_boundary",
                "component": "Phi_boundary_abs",
                "meaning": "boundary/readout/projector/topology/history flux contribution",
                "zero_condition": "all Phi components theorem-zero channelwise",
                "bound_formula": "abs_Phi_total >= abs(Phi_edge)+abs(Phi_ref)+abs(Phi_corner)+abs(Phi_kernel)+abs(Phi_source_norm)",
                "units": "boundary action or arena projection units",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_3_action_weight",
                "component": "Delta_w_abs;beta_w_source_abs;beta_w_test_abs",
                "meaning": "pre-variation action-weight/source-normalization obstruction",
                "zero_condition": "object-language/action-measure theorem excludes independent w_A or makes them common",
                "bound_formula": "alpha_w(lambda)=K_w(lambda)*abs(beta_w_source*beta_w_test)+epsilon_tail_abs",
                "units": "dimensionless weights and beta convention",
                "status": "FIRST_FILL_READY_VALUES_MISSING",
            }
        ),
        row(
            {
                "id": "RC1986_4_conservation",
                "component": "q_nonH_abs;q_loc_abs;source_current_abs",
                "meaning": "non-Hilbert current or response-doublet/source-current obstruction to Bianchi/Newton closure",
                "zero_condition": "same-parent Ward/Bianchi closure including memory/bath/source terms",
                "bound_formula": "abs_q_current <= abs(q_nonH)+abs(q_loc)+abs(source_current_tail)",
                "units": "current divergence / force-density / normalized residual units",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_5_measured_GM",
                "component": "GM_source_norm_abs",
                "meaning": "measured-GM / Poisson-Gauss / orbital calibration residual",
                "zero_condition": "Pi_M J_H flux closure and worldtube glue prove same source charge",
                "bound_formula": "abs_GM_resid >= abs(dln_Meff_dt)+abs(radial)+abs(range)+abs(species)+abs(frame)",
                "units": "dimensionless, yr^-1, or arena-normalized GM residual by component",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_6_arena",
                "component": "Delta_arena_abs",
                "meaning": "same-parent law mismatch across local/cosmology/galaxy/clock/orbital arenas",
                "zero_condition": "one parent coefficient map evaluates all arenas before data scoring",
                "bound_formula": "abs_Delta_arena >= sum_arena abs(theta_arena - theta_parent_map(arena))",
                "units": "parameter-dependent; must be declared per coefficient",
                "status": "MISSING_SOURCE_BACKED_ZERO_OR_BOUND",
            }
        ),
        row(
            {
                "id": "RC1986_7_kernel_projection",
                "component": "K_alpha_abs;K_PPN_abs;K_clock_abs;K_orbital_abs",
                "meaning": "arena projection/kernel normalization from memory residual vector to observable bounds",
                "zero_condition": "projection kernel is irrelevant only if all upstream residuals are theorem-zero",
                "bound_formula": "observable_residual_i <= K_i * vector_norm_abs with finite-size/profile corrections",
                "units": "arena-specific kernel units",
                "status": "MISSING_KERNEL_NORMALIZATION",
            }
        ),
    ]

    vector_norm = [
        row(
            {
                "id": "VN1986_0_abs_rule",
                "norm": "memory_residual_vector_L1_abs",
                "formula": "R_mem_abs := abs_Jc_total + abs_qbar_XT + abs_Phi_boundary + abs_Delta_w + abs_q_current + abs_GM_resid + abs_Delta_arena",
                "rule": "absolute values only; no sign, branch, arena, or boundary/source cancellation",
                "claim_status": "FORMULA_READY_VALUES_MISSING",
            }
        ),
        row(
            {
                "id": "VN1986_1_claim_condition",
                "norm": "zero_or_bounded_condition",
                "formula": "claim_ready iff every component is theorem-zero or source-backed finite with units, source path, branch id, and projection kernel",
                "rule": "missing or placeholder component blocks local-GR and empirical pass",
                "claim_status": "BLOCKED_BY_MISSING_COMPONENTS",
            }
        ),
        row(
            {
                "id": "VN1986_2_arena_projection",
                "norm": "observable_projection",
                "formula": "Obs_i_abs <= K_i(lambda,profile,frame) * R_mem_abs + tail_i_abs",
                "rule": "R10/PPN/clock/orbital/cosmology projections require separate K_i normalization",
                "claim_status": "MISSING_KERNELS",
            }
        ),
    ]

    arena_matrix = [
        row({"id": "ARENA1986_0_R10", "arena": "R10/R11 short range", "components": "beta/qbar;boundary;action_weight;kernel_projection", "needed_output": "alpha_predicted(lambda) with source/test/kernel normalization", "status": "SCHEMA_READY_VALUES_MISSING"}),
        row({"id": "ARENA1986_1_PPN", "arena": "PPN gamma/beta/preferred-frame", "components": "Jc;boundary;conservation;GM_source_norm", "needed_output": "gamma_minus_1, beta_minus_1, alpha3-like rows", "status": "SCHEMA_READY_VALUES_MISSING"}),
        row({"id": "ARENA1986_2_clocks", "arena": "clock/fine-structure/material constants", "components": "beta/qbar;action_weight;arena;kernel_projection", "needed_output": "clock drift/composition response rows", "status": "SCHEMA_READY_VALUES_MISSING"}),
        row({"id": "ARENA1986_3_orbital", "arena": "orbital/Newton/source-normalization", "components": "GM_source_norm;conservation;boundary;arena", "needed_output": "Gdot/GM/radial/orbital residual rows", "status": "SCHEMA_READY_VALUES_MISSING"}),
        row({"id": "ARENA1986_4_cosmology", "arena": "cosmology/growth/background", "components": "Jc;arena;canonical_gap;source_boundary", "needed_output": "same-parent coefficient map with no prior-edge hiding", "status": "SCHEMA_READY_VALUES_MISSING"}),
        row({"id": "ARENA1986_5_galaxy", "arena": "galaxy empirical pillar", "components": "arena;canonical_transfer;source law", "needed_output": "same-parent mapping to galaxy parameters without retuning", "status": "SCHEMA_READY_VALUES_MISSING"}),
    ]

    source_slots = [
        row({"id": "SLOT1986_0_required_columns", "slot": "minimum claim-grade row columns", "required": "component_id;branch_id;symbol;value_or_zero_theorem;units;source_path;equation_ref;domain;frame;valid_for_claim", "status": "TEMPLATE_READY"}),
        row({"id": "SLOT1986_1_zero_theorem", "slot": "zero theorem row", "required": "must name parent theorem and all clauses; no missing premises; no cancellation", "status": "TEMPLATE_READY"}),
        row({"id": "SLOT1986_2_finite_bound", "slot": "finite bound row", "required": "must give positive numeric/symbolic upper bound, units, source path, and arena projection", "status": "TEMPLATE_READY"}),
        row({"id": "SLOT1986_3_placeholder_policy", "slot": "placeholder rule", "required": "MISSING, TEMPLATE, FORMULA_ONLY, CLOSURE_ONLY, or UNSIGNED keeps valid_for_claim=false", "status": "TEMPLATE_READY"}),
    ]

    runner_dryrun = [
        row({"id": "RUN1986_0_components", "check": "all residual components present", "result": "PASS_SCHEMA", "claim_ready": "false", "reason": "component catalog has all seven 1985 residual families plus projection kernels"}),
        row({"id": "RUN1986_1_values", "check": "all components theorem-zero or bounded", "result": "FAIL_VALUES_MISSING", "claim_ready": "false", "reason": "every component still requires source-backed zero/bound rows"}),
        row({"id": "RUN1986_2_no_cancellation", "check": "absolute norm guard", "result": "PASS_GUARD", "claim_ready": "false", "reason": "L1 absolute norm written, but values missing"}),
        row({"id": "RUN1986_3_observable_projection", "check": "arena kernels supplied", "result": "FAIL_KERNELS_MISSING", "claim_ready": "false", "reason": "K_alpha/K_PPN/K_clock/K_orbital/cosmology kernels are not sourced"}),
        row({"id": "RUN1986_4_verdict", "check": "memory route local-GR/test pass", "result": "BLOCKED_NONCLAIM_VECTOR_READY", "claim_ready": "false", "reason": "residual vector is ready for filling, not scoring"}),
    ]

    claim_gate = [
        row({"id": "GATE1986_0_vector_claim", "gate": "memory residual vector claim-ready", "status": "BLOCKED", "reason": "component values/zero theorems and kernels missing", "required_to_open": "all source slots filled with claim-grade rows"}),
        row({"id": "GATE1986_1_local_GR", "gate": "derived local GR/Newton", "status": "BLOCKED", "reason": "finite residual vector is schema-only and nonclaim", "required_to_open": "all residual components theorem-zero or bounded below observational thresholds"}),
        row({"id": "GATE1986_2_empirical_pass", "gate": "R10/PPN/clock/orbital/cosmology pass", "status": "BLOCKED", "reason": "arena projection kernels and component values missing", "required_to_open": "run scored vector against source-backed bounds"}),
    ]

    decision = [
        row({"id": "DEC1986_0_vector_written", "decision": "FINITE_RESIDUAL_VECTOR_PACK_WRITTEN", "because": "1985 open gates are now one no-cancellation component catalog", "next_action": "choose first component to fill with actual zero theorem or source-bound"}),
        row({"id": "DEC1986_1_no_score", "decision": "DO_NOT_SCORE_YET", "because": "every component is missing source-backed values/theorems", "next_action": "fill one high-pressure component rather than pretending vector is predictive"}),
        row({"id": "DEC1986_2_best_next", "decision": "FIRST_COMPONENT_SELECTION", "because": "action-weight and source/test coupling are the hardest Newton/R10 seams; choose one and fill theorem-or-bound row", "next_action": "1987-Y5-R2FR-first-residual-component-fill-selector.md"}),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1986_0_primary",
                "status": "selected",
                "target_doc": "1987-Y5-R2FR-first-residual-component-fill-selector.md",
                "target_script": "scripts/Y5_R2FR_first_residual_component_fill_selector_1987.py",
                "task": "choose the first residual component to fill: action-weight Delta_w/beta_w, qbar_XT source/test coupling, or boundary Phi; then create a theorem-zero or finite-bound row.",
                "success_condition": "one component gets a strict source-slot fill plan with units, source paths, no-cancellation guard, and target arena",
            }
        )
    ]

    snapshot = [
        row({"id": "SNAP1986_0_status", "area": "testability", "status": "VECTOR_SCHEMA_READY_NONCLAIM", "summary": "Open local-GR derivation gates are now a single absolute residual-vector schema."}),
        row({"id": "SNAP1986_1_claim", "area": "claim status", "status": "NO_CLAIM", "summary": "No component has claim-grade values or zero theorems; local GR remains blocked."}),
        row({"id": "SNAP1986_2_next", "area": "next move", "status": "FILL_FIRST_COMPONENT", "summary": "Pick one high-pressure residual component and try to fill it rather than widening the schema further."}),
    ]

    source_weight = [
        row({"id": "SW1986_0", "doc": DOC_PATH.name, "weight": "private_nonclaim_residual_vector_schema", "claim_safety": "all claim flags false; runner dryrun blocks scoring", "use": "organizes finite residuals for empirical robustness passes"}),
    ]

    queue = [
        row({"id": "Q1986_0_first_component", "quantity": "first source-backed residual component", "priority": "highest", "why": "vector cannot score until at least one component has a real zero theorem or bound", "target": "1987 first fill selector"}),
    ]

    return {
        "source_register": source_register_rows(),
        "component_catalog": component_catalog,
        "vector_norm": vector_norm,
        "arena_matrix": arena_matrix,
        "source_slots": source_slots,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    return all(
        item.get("valid_for_claim") == "false" and item.get("public_claim") == "false"
        for rows in tables.values()
        for item in rows
    )


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def formalization_1986_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1986*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_ok = all(row_data["exists"] == "true" and row_data["needle_status"] == "PASS" for row_data in tables["source_register"])
    components_ok = len(tables["component_catalog"]) >= 8
    norm_guard_ok = tables["vector_norm"][0]["rule"].startswith("absolute values only")
    runner_blocks = tables["runner_dryrun"][-1]["result"] == "BLOCKED_NONCLAIM_VECTOR_READY"
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1987-Y5-R2FR-first-residual-component-fill-selector.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1986_artifact_count()
    specs = [
        ("VAL1986_00_sources", sources_ok, "all source paths exist and needles found"),
        ("VAL1986_01_components", components_ok, "residual component catalog covers required families"),
        ("VAL1986_02_abs_guard", norm_guard_ok, "absolute no-cancellation vector norm written"),
        ("VAL1986_03_runner_blocks", runner_blocks, "runner dryrun blocks scoring"),
        ("VAL1986_04_claim_gates", gates_blocked, "all claim gates blocked"),
        (
            "VAL1986_05_decision",
            tables["decision"][-1]["decision"] == "FIRST_COMPONENT_SELECTION",
            "decision selects first component fill",
        ),
        ("VAL1986_06_next_target", next_selected, "1987 target selected"),
        ("VAL1986_07_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1986_08_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1986_09_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1986_10_formalization_untouched", formalization_count == 0, f"formalization_1986_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in specs
    ]
    rows.append(
        {
            "validation_id": "VAL1986_OVERALL",
            "status": "PASS" if all(row_data["status"] == "PASS" for row_data in rows) else "FAIL",
            "detail": "1986 memory-route finite residual vector pack",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for item in rows:
        values = [item.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Residual Component Catalog", tables["component_catalog"]),
        ("No-Cancellation Vector Norm", tables["vector_norm"]),
        ("Arena Projection Matrix", tables["arena_matrix"]),
        ("Source Slot Template", tables["source_slots"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1986 Y5 R2FR: Memory Route Finite Residual Vector Pack",
        "",
        "Private checkpoint. This converts the 1985 open source/boundary/conservation/Newton gates into a single finite residual vector with absolute no-cancellation bookkeeping.",
        "",
        "Verdict: the residual vector schema is ready, but it is nonclaim. Every component still needs a parent theorem-zero row or a source-backed finite bound with units and arena projection. The local-GR route remains blocked; the next useful step is to fill one high-pressure component rather than widening the schema again.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, cosmology, galaxy, or public claim follows from 1986.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1986_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
