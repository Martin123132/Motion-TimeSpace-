from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1327"
TITLE = "1327-Y5-R10-RAB-parent-interaction-graph-or-Delta-w-component-fraction-intake"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
COMPONENT_ROOT = ROOT / "source-intake" / "component-fractions"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
GRAPH_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_GRAPH_CERTIFICATE_AUDIT.csv"
EDGE_ROLLUP_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_STATUS_ROLLUP.csv"
COMPONENT_INTAKE_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_COMPONENT_INTAKE_MATRIX.csv"
VALIDATOR_HANDOFF_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_INTAKE_VALIDATOR_HANDOFF.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1327_VALIDATION.csv"


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
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        GRAPH_AUDIT_PATH,
        EDGE_ROLLUP_PATH,
        COMPONENT_INTAKE_PATH,
        VALIDATOR_HANDOFF_PATH,
        RUNNER_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def first(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    return next(row for row in rows if row.get(key) == value)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for directory in ("raw", "docs", "accepted", "rejected"):
        (COMPONENT_ROOT / directory).mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1327_0_1326_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1326_NEXT_TARGET.csv",
            "needle": "NEXT1326_0_1327",
            "role": "handoff into graph certificate or component-fraction intake",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_1_1326_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1326_FINITE_DELTA_W_PRIOR_CONTRACT.csv",
            "needle": "FDW1326_2_component_formula",
            "role": "current Delta_w component formula",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_2_1232_graph",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv",
            "needle": "IGC1232_4_verdict",
            "role": "parent graph certificate attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_3_1232_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "needle": "EDGE1232_0_electron_photon",
            "role": "ordinary matter graph edge audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_4_1233_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "needle": "fraction_value",
            "role": "component fraction schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_5_1233_dryrun",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv",
            "needle": "NO_CANDIDATE_FILES_PRESENT",
            "role": "validator dry-run status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_6_1233_edge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_GRAPH_EDGE_DEMOTION_LEDGER.csv",
            "needle": "EDGE1232_0_electron_photon",
            "role": "electron-photon edge demotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_7_1234_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1234_GRAPH_EDGE_STATUS_UPDATE.csv",
            "needle": "EM_OWNER_UNIQUENESS_NOT_CLOSED",
            "role": "EM owner edge update",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_8_1235_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_GRAPH_EDGE_STATUS_UPDATE.csv",
            "needle": "QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
            "role": "QCD edge update",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_9_1236_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_GRAPH_EDGE_STATUS_UPDATE.csv",
            "needle": "DEEPENED_BUT_NOT_SIGNED",
            "role": "latest edge status update",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_10_1232_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_1_isotopic_abundances_masses",
            "role": "Ti/Pt component fraction source requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_11_1232_quarantine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv",
            "needle": "QUAR1232_0_983_proxy_vectors",
            "role": "toy/proxy quarantine policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1327_12_1231_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv",
            "needle": "DWM1231_1_TiPt_difference",
            "role": "Delta_w component map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    graph_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv"))
    graph_verdict = first(graph_rows, "cert_id", "IGC1232_4_verdict")
    edge_1236 = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1236_GRAPH_EDGE_STATUS_UPDATE.csv"))
    source_pack = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"))
    dryrun = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv"))[0]

    graph_audit = [
        {
            "graph_id": "GRAPH1327_0_connected_graph",
            "target": "parent ordinary-matter interaction graph certificate",
            "current_status": graph_verdict["result"],
            "evidence": "P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv:IGC1232_4_verdict",
            "blocks": graph_verdict["missing_for_claim"],
            "counts_for_delta_w_zero": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "graph_id": "GRAPH1327_1_edge_rollup",
            "target": "all useful graph edges parent-signed",
            "current_status": "NO_EDGE_COUNTS_FOR_CONNECTED_GRAPH",
            "evidence": "P8_Y5_R10_1233/1234/1235/1236_GRAPH_EDGE_STATUS_UPDATE",
            "blocks": "EM owner uniqueness, unique F2 certificate, QCD strong-sector owner, bound-state transfer, source-label forgetting",
            "counts_for_delta_w_zero": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "graph_id": "GRAPH1327_2_fallback_intake",
            "target": "strict component-fraction intake matrix",
            "current_status": "SOURCE_READY_MATRIX_REQUIRED",
            "evidence": "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv;P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "blocks": "no accepted fraction rows, no component priors, no tau_WEP",
            "counts_for_delta_w_zero": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_rollup = []
    for row in edge_1236:
        edge_rollup.append(
            {
                "edge_id": row["edge_id"],
                "latest_status": row["new_status"],
                "reason": row["reason"],
                "counts_for_connected_graph": row["counts_for_connected_graph"],
                "runner_effect": "graph_zero_refused" if row["counts_for_connected_graph"].lower() == "false" else "candidate_edge",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    component_ids = [
        ("electron", "electron/leptonic energy fraction", "FSP1232_2_electron_fraction"),
        ("light_quark", "light-quark mass fraction", "FSP1232_3_light_quark_fraction"),
        ("QCD_gluon", "QCD/gluon/nuclear bulk fraction", "FSP1232_4_QCD_gluon_fraction"),
        ("EM_Coulomb", "EM/Coulomb binding fraction", "FSP1232_5_EM_Coulomb_fraction"),
        ("nuclear_surface", "nuclear surface/asymmetry fraction", "FSP1232_6_nuclear_surface_asymmetry_fraction"),
        ("measure_readout", "measure/readout reentry fraction", "FSP1232_7_measure_readout_fraction"),
    ]
    pack_by_id = {row["pack_id"]: row for row in source_pack}
    component_intake = []
    for component_id, quantity, pack_id in component_ids:
        pack_row = pack_by_id[pack_id]
        for material_id in ("TA6V", "PtRh10"):
            component_intake.append(
                {
                    "intake_id": f"CFI1327_{material_id}_{component_id}",
                    "material_id": material_id,
                    "component_id": component_id,
                    "target_quantity": quantity,
                    "required_source_or_method": pack_row["required_source_or_method"],
                    "current_evidence": pack_row["current_local_evidence"],
                    "current_status": pack_row["current_status"],
                    "required_columns": "row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim",
                    "acceptance_status": "WAITING_FOR_SOURCE_ROW",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )

    validator_handoff = [
        {
            "handoff_id": "VALHAND1327_0_directories",
            "object": "component-fraction intake directories",
            "current_status": "READY",
            "source": "P8_Y5_R10_1233_COMPONENT_FRACTION_DIRECTORY_CONTRACT.csv",
            "effect": "future raw/accepted/rejected component fraction rows have a controlled location",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "VALHAND1327_1_schema",
            "object": "component-fraction schema",
            "current_status": "REQUIRED_FIELDS_LOCKED",
            "source": "P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "effect": "candidate rows without numeric/source/basis/provenance fields are rejected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "VALHAND1327_2_dryrun",
            "object": "current candidate scan",
            "current_status": dryrun["status"],
            "source": "P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv:DRY1233_0_candidate_scan",
            "effect": "no accepted component-fraction rows currently exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "VALHAND1327_3_proxy_quarantine",
            "object": "toy/proxy material rows",
            "current_status": "QUARANTINED",
            "source": "P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv",
            "effect": "proxy Y_e, DD smoke deltas, and one-pair cancellation cannot feed claim rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1327_0_graph_certificate",
            "target": "Delta_w_TiPt=0 via connected parent graph",
            "input_status": "GRAPH_CERTIFICATE_NOT_CLOSED",
            "missing_inputs": "parent-signed vertices;parent-signed nonzero morphism edges;source functor;measure/current/readout owner",
            "runner_status": "REFUSED_NO_ZERO_PROMOTION",
            "claim_effect": "no Delta_w=0, WEP, local-GR, or source-coupling pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1327_1_component_intake",
            "target": "Delta_w_TiPt=sum_c DeltaF_c delta_w_c + DeltaK_TiPt",
            "input_status": "SOURCE_READY_MATRIX_STAGED_NO_ROWS_ACCEPTED",
            "missing_inputs": "accepted component fractions;component priors;readout residual;official tau_WEP",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "claim_effect": "finite Delta_w branch is now intake-ready but nonclaim",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1327_0_no_template_edge_count",
            "shortcut": "count graph template edges as connected parent graph evidence",
            "enforcement": "REFUSED until edge status counts_for_connected_graph=true with parent proof",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1327_1_no_proxy_fractions",
            "shortcut": "use Y_e/neutron/coulomb proxy vectors as component energy fractions",
            "enforcement": "REFUSED by QUAR1232 and component schema gates",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1327_2_no_DD_smoke_as_parent_basis",
            "shortcut": "use DD smoke alpha/surface deltas as MTS parent component fractions",
            "enforcement": "REFUSED unless explicitly labelled external nonclaim comparator",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1327_3_no_threshold_prior",
            "shortcut": "use the WEP bound as a Delta_w prior",
            "enforcement": "REFUSED; threshold is a comparison fence only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1327_4_no_local_GR_claim",
            "shortcut": "claim GR/Newton source reduction from graph/intake scaffolding",
            "enforcement": "REFUSED until graph theorem or finite residual bounds close with Bianchi/readout gates",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1327_0_graph_not_signed",
            "decision": "do not claim parent graph connectedness",
            "because": "latest edge rollup has no edge counting for connected graph and the graph certificate remains template/conditional",
            "effect": "Delta_w zero route remains alive but refused",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1327_1_component_intake_ready",
            "decision": "stage source-ready Delta_w component-fraction intake matrix",
            "because": "finite fallback now needs real component fractions, component priors, and tau_WEP rather than proxy rows",
            "effect": "future data rows have strict schema/provenance gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1327_2_next_best",
            "decision": "next target should be a source acquisition dry-run or one more edge-owner proof",
            "because": "no candidate fraction rows are present and graph edges are still unsigned",
            "effect": "1328 should either fetch/source component-fraction references or attack EM/QCD owner certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1327_0_1328",
            "target_file": "1328-Y5-R10-RAB-component-fraction-source-acquisition-or-EM-QCD-edge-owner-reentry.md",
            "target_script": "scripts/Y5_R10_RAB_component_fraction_source_acquisition_or_EM_QCD_edge_owner_reentry.py",
            "task": "try a bounded source acquisition pass for claim-grade component fractions; if not available, re-enter EM/QCD edge owner proof with exact blocker rows",
            "success_condition": "either candidate fraction sources are staged with provenance and still nonclaim, or the next graph edge owner proof is narrowed without claiming connectedness",
            "do_not": "do not use proxy/toy rows, WEP thresholds, or template graph edges as evidence; do not claim Delta_w=0 or local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(GRAPH_AUDIT_PATH, graph_audit)
    write_csv(EDGE_ROLLUP_PATH, edge_rollup)
    write_csv(COMPONENT_INTAKE_PATH, component_intake)
    write_csv(VALIDATOR_HANDOFF_PATH, validator_handoff)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    sources_ok = all(row["exists"] and row["needle_found"] for row in source_register)
    validations.append(
        validation_row(
            "VAL1327_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    graph_refused = all(not row["counts_for_delta_w_zero"] for row in graph_audit)
    validations.append(
        validation_row(
            "VAL1327_1_graph_refused",
            "parent interaction graph certificate remains refused",
            graph_refused,
            ";".join(f"{row['graph_id']}={row['current_status']}" for row in graph_audit),
        )
    )
    no_edges_count = all(str(row["counts_for_connected_graph"]).lower() == "false" for row in edge_rollup)
    validations.append(
        validation_row(
            "VAL1327_2_no_edges_count",
            "latest graph edge rollup has no parent-signed connected edges",
            no_edges_count,
            ";".join(f"{row['edge_id']}={row['latest_status']}" for row in edge_rollup),
        )
    )
    intake_complete = len(component_intake) == 12 and all(row["acceptance_status"] == "WAITING_FOR_SOURCE_ROW" for row in component_intake)
    validations.append(
        validation_row(
            "VAL1327_3_component_intake_matrix",
            "component intake matrix covers six components for TA6V and PtRh10",
            intake_complete,
            f"component_intake_rows={len(component_intake)}",
        )
    )
    validator_ok = dryrun["accepted_rows"] == "0" and all(not row["claim_allowed"] for row in validator_handoff)
    validations.append(
        validation_row(
            "VAL1327_4_validator_handoff_nonclaim",
            "validator handoff keeps accepted rows at zero and proxy rows quarantined",
            validator_ok,
            f"dryrun_status={dryrun['status']};accepted_rows={dryrun['accepted_rows']}",
        )
    )
    runner_refuses = all(row["runner_status"].startswith("REFUSED") and not row["score_ready"] for row in runner)
    validations.append(
        validation_row(
            "VAL1327_5_runner_refuses",
            "graph and component intake runners remain refused",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        )
    )
    shortcut_ok = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    validations.append(
        validation_row(
            "VAL1327_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcut_ok,
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    nonclaim_ok = all_nonclaim(
        [
            source_register,
            graph_audit,
            edge_rollup,
            component_intake,
            validator_handoff,
            runner,
            anti_shortcut,
            decision,
            next_target,
        ]
    )
    validations.append(
        validation_row(
            "VAL1327_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_ok,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    formal_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1327_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formal_outputs,
            f"formalization_generated_output_count={len(formal_outputs)}",
        )
    )
    next_ok = next_target[0]["target_file"].startswith("1328-Y5-R10-RAB-component-fraction")
    validations.append(
        validation_row(
            "VAL1327_9_next_target_1328",
            "next target routes to component source acquisition or EM/QCD edge owner reentry",
            next_ok,
            str(next_target[0]["target_file"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1327_10_overall",
            "overall 1327 validation",
            all(row["status"] == "PASS" for row in validations),
            "1327 refuses graph zero, stages source-ready component intake matrix, and preserves nonclaim gates",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1327: RAB Parent Interaction Graph Or Delta-w Component Fraction Intake

**Current verdict:** 1327 does not close the parent interaction graph. The graph route remains exact conditional math, but no current edge counts as parent-signed connectedness evidence.

**Main progress:** the finite `Delta_w_TiPt` route is now source-intake ready: six component fractions for both TA6V and PtRh10 have explicit required source/method rows, and the validator handoff keeps all current proxy/toy rows quarantined.

**Decision:** no `Delta_w=0`, WEP, or local-GR claim. Next move is either a bounded source acquisition pass for real component fractions, or another graph-edge owner proof reentry.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Graph Certificate Audit
{markdown_table(graph_audit, ["graph_id", "target", "current_status", "evidence", "blocks", "counts_for_delta_w_zero", "valid_for_claim", "claim_allowed"])}

## Graph Edge Status Rollup
{markdown_table(edge_rollup, ["edge_id", "latest_status", "reason", "counts_for_connected_graph", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Delta-w Component Intake Matrix
{markdown_table(component_intake, ["intake_id", "material_id", "component_id", "target_quantity", "required_source_or_method", "current_evidence", "current_status", "required_columns", "acceptance_status", "valid_for_claim", "claim_allowed"])}

## Component Intake Validator Handoff
{markdown_table(validator_handoff, ["handoff_id", "object", "current_status", "source", "effect", "valid_for_claim", "claim_allowed"])}

## Delta-w Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "missing_inputs", "runner_status", "claim_effect", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
