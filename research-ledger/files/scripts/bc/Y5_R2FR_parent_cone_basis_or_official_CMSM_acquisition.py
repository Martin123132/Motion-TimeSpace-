from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1614"
INPUT_1614 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1614-Y5-R2FR-parent-cone-basis-or-official-CMSM-acquisition.md"

SOURCE_FILES = {
    "1613_doc": ROOT / "1613-Y5-R2FR-CMSM-file-drop-loader-or-signed-margin-bound.md",
    "1613_validation": OUT / "P8_Y5_BRR545_1613_VALIDATION.csv",
    "1613_next": OUT / "P8_Y5_PARENT_QLOC_1613_NEXT_TARGET.csv",
    "1613_theorem": OUT / "P8_Y5_PARENT_QLOC_1613_SIGNED_MARGIN_THEOREM_ATTEMPT.csv",
    "1613_gates": OUT / "P8_Y5_PARENT_QLOC_1613_CERTIFICATE_ACCEPTANCE_GATES.csv",
    "1613_loader": OUT / "P8_Y5_PARENT_QLOC_1613_CMSM_FILE_DROP_LOADER_DRY_RUN.csv",
    "1605_action_owner": OUT / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv",
    "1606_graph": OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv",
    "1606_edges": OUT / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv",
    "1607_material": OUT / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_CONTEXT_AUDIT.csv",
    "1610_positive_cone": OUT / "P8_Y5_PARENT_QLOC_1610_POSITIVE_CONE_THEOREM_ATTEMPT.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
}

NEEDLES = {
    "1613_doc": ["SMT1613_1_compact_kernel_theorem", "NEXT_1614_PARENT_CONE_BASIS_OR_OFFICIAL_CMSM_ACQUISITION"],
    "1613_validation": ["VAL1613_OVERALL", "PASS"],
    "1613_next": ["1614-Y5-R2FR-parent-cone-basis-or-official-CMSM-acquisition.md", "parent allowed cone"],
    "1613_theorem": ["SMT1613_1_compact_kernel_theorem", "EXACT_IFF_THEOREM"],
    "1613_gates": ["CAC1613_2_parent_basis", "BLOCKED"],
    "1613_loader": ["LOA1613_0_1613_source_pack_filelist", "MISSING_INPUT_FILE"],
    "1605_action_owner": ["ADO1605_1_naturality_lemma", "EXACT_CONDITIONAL_LEMMA"],
    "1606_graph": ["POG1606_4_verdict", "PARENT_OWNED_GRAPH_NOT_DERIVED"],
    "1606_edges": ["EDGE1606_7_verdict", "NOT_PARENT_CERTIFIED"],
    "1607_material": ["MTA1607_5_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1610_positive_cone": ["PCN1610_1_positive_functional_lemma", "EXACT_CONDITIONAL_LEMMA"],
    "1456_worldtube": ["SWP1456_4_mask_orbit_limit", "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1614_SOURCE_REGISTER.csv"
OFFICIAL_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1614_OFFICIAL_CMSM_ACQUISITION_STATUS.csv"
PARENT_CONE = OUT / "P8_Y5_PARENT_QLOC_1614_PARENT_CONE_BASIS_THEOREM_ATTEMPT.csv"
GENERATOR_CERT = OUT / "P8_Y5_PARENT_QLOC_1614_GENERATOR_POSITIVITY_CERTIFICATE_CONTRACT.csv"
BLOCKER_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1614_PARENT_CONE_BLOCKER_AUDIT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1614_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1614_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1614_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1614_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1614_VALIDATION.csv"

COPY_TARGETS = {
    OFFICIAL_ACQUISITION: [
        QUARANTINE / "OFFICIAL_CMSM_ACQUISITION_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_official_CMSM_acquisition_status_nonclaim_1614.csv",
    ],
    PARENT_CONE: [
        QUARANTINE / "PARENT_CONE_BASIS_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_cone_basis_theorem_attempt_nonclaim_1614.csv",
    ],
    GENERATOR_CERT: [
        QUARANTINE / "GENERATOR_POSITIVITY_CERTIFICATE_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_generator_positivity_certificate_contract_nonclaim_1614.csv",
    ],
    BLOCKER_AUDIT: [
        QUARANTINE / "PARENT_CONE_BLOCKER_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_cone_blocker_audit_nonclaim_1614.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1614.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1614_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1614_parent_cone_basis_or_official_CMSM_acquisition_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def official_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": "OCA1614_0_ONERA_pointer",
            "object": "ONERA MICROSCOPE data pointer",
            "source_url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "current_status": "PUBLIC_POINTER_KNOWN",
            "captured_file": "",
            "why_not_enough": "pointer is not the CMSM source-pack/readout/material/alignment arrays",
            "source_acquired": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": "OCA1614_1_CMSM_module",
            "object": "CMSM MICROSCOPE module",
            "source_url": "https://cmsm-ds.onera.fr/user/microscope/modules/7",
            "current_status": "AUTH_OR_TIMEOUT_NO_ROWS_CAPTURED",
            "captured_file": "",
            "why_not_enough": "no authenticated source-pack filelist, checksum, HAR, or science table is present in quarantine",
            "source_acquired": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": "OCA1614_2_quarantine_1613",
            "object": "quarantine/1613/input",
            "source_url": "",
            "current_status": "NO_ACCEPTED_FILES",
            "captured_file": rel(INPUT_1614),
            "why_not_enough": "1613 loader accepted zero real CMSM rows",
            "source_acquired": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": "OCA1614_3_required_pack",
            "object": "minimal official pack",
            "source_url": "",
            "current_status": "MISSING_K_V_ALIGNMENT_MATERIAL_MASKS",
            "captured_file": "",
            "why_not_enough": "need K_CMSM_readout, source_worldtube, material_tensor, mask_orbit, alignment_result and provenance",
            "source_acquired": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_cone_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_0_target",
            "statement": "derive the parent allowed source-material cone C and parent basis B such that C cap ker(K_CMSM)=empty",
            "status": "TARGET_SHARPENED",
            "proof_result": "this is exactly the remaining no-cancellation route for c_min>0",
            "blocking_gap": "basis B, cone C and K_CMSM sign are not parent-owned",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_1_generator_positivity_lemma",
            "statement": "If C=cone{g_i} on the unit sphere, K(g_i)>=k_i>0 for every generator, and omitted corrections are nonnegative/bounded, then C cap ker(K)=empty and c_min>0.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "proof_result": "a parent generator certificate would close the signed-margin theorem without fitting tau_eff",
            "blocking_gap": "no parent-owned generator list or K(g_i) lower bounds exist",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_2_action_graph_link",
            "statement": "1605/1606 graph naturality can collapse action weights only after the parent action-density line and all source-relevant edges are signed.",
            "status": "UPSTREAM_CONDITIONAL_ONLY",
            "proof_result": "connected graph logic supports the cone idea but does not supply parent ownership",
            "blocking_gap": "parent-owned matter graph and edge certificates remain unproved",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_3_material_basis_problem",
            "statement": "Ti/Pt differential material response must be expressed in the same parent basis as K_CMSM, with covariance/no-double-counting rules.",
            "status": "MATERIAL_BASIS_NOT_SIGNED",
            "proof_result": "external composition/proxy rows cannot define the parent cone",
            "blocking_gap": "full parent material-response tensor remains missing",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_4_domain_order_problem",
            "statement": "masks, orbit windows and readout projections must be downstream maps, not parent-domain selectors.",
            "status": "DOMAIN_ORDER_NOT_SIGNED",
            "proof_result": "otherwise C can be changed by the readout and the cone theorem is circular",
            "blocking_gap": "source-worldtube/readout arrays and parent readout-order theorem are absent",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCB1614_5_verdict",
            "statement": "1614 does not derive the parent cone/basis theorem; it reduces the route to a generator positivity certificate or official CMSM computation.",
            "status": "PARENT_CONE_BASIS_NOT_DERIVED",
            "proof_result": "the exact sufficient clauses are now separated from data acquisition",
            "blocking_gap": "parent-owned generators, readout signs, material basis and covariance are unsigned",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def generator_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GPC1614_0_parent_basis", "basis_id;component_id;basis_definition;source_path", "defines one parent basis B for K and V", "MISSING_PARENT_BASIS"),
        ("GPC1614_1_generators", "generator_id;component_coefficients;nonnegative_coefficients;normalization", "defines C=cone{g_i} without hidden signed components", "MISSING_GENERATOR_LIST"),
        ("GPC1614_2_readout_sign", "generator_id;K_g_lower_bound;sign_convention;units;source_path", "certifies K(g_i)>=k_i>0 or signed equivalent", "MISSING_K_GENERATOR_BOUNDS"),
        ("GPC1614_3_material_projection", "material_pair;generator_id;projection_interval;basis;source_path", "maps Ti/Pt source-material response into C", "MISSING_PARENT_MATERIAL_PROJECTION"),
        ("GPC1614_4_covariance", "covariance_rule;omitted_terms_bound;no_double_counting;source_path", "prevents hidden cancellation from corrections/tails", "MISSING_COVARIANCE_RULE"),
        ("GPC1614_5_domain_order", "mask_orbit_rule;downstream_only;variation_domain;source_path", "keeps readout windows from defining the parent domain", "MISSING_DOMAIN_ORDER_CERTIFICATE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "required_fields": fields,
            "purpose": purpose,
            "current_status": status,
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, fields, purpose, status in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("PBL1614_0_basis_duality", "K and V may be represented in different bases", "inner product/projection not meaningful", "same parent basis map"),
        ("PBL1614_1_signed_material", "Ti/Pt material response has signed component contrasts", "positive bulk density does not imply V in positive cone", "parent material tensor/covariance"),
        ("PBL1614_2_readout_sign", "K_CMSM may include signed orbit/window/correction weights", "positive generators can cancel", "official K arrays or parent sign theorem"),
        ("PBL1614_3_graph_ownership", "physical matter graph is connected but not parent-owned", "action-weight/cone generators may be independent", "parent-owned edge certificate"),
        ("PBL1614_4_domain_selector", "masks/windows may select support", "readout can define C circularly", "downstream-only domain-order proof"),
        ("PBL1614_5_official_files", "CMSM source pack still absent", "cannot compute c_min empirically", "official filelist/readout/material/alignment acquisition"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": effect,
            "required_fix": fix,
            "status": "OPEN_BLOCKER",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, blocker, effect, fix in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1614_0_parent_cone",
            "input_state": "parent basis/generator/readout/material/covariance clauses unsigned",
            "runner_result": "REJECT_PARENT_CONE_PROOF",
            "effect": "no c_min theorem is promoted",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1614_1_official_acquisition",
            "input_state": "ONERA pointer known but no CMSM source-pack rows captured",
            "runner_result": "NO_OFFICIAL_CMSM_ARRAYS_ACCEPTED",
            "effect": "empirical c_min computation remains blocked",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1614_0_parent_basis", "parent basis/cone proof", "BLOCKED", "generator positivity certificate not parent-signed"),
        ("CG1614_1_official_arrays", "official CMSM c_min computation", "BLOCKED", "K/V/material/mask/alignment files absent"),
        ("CG1614_2_no_cancellation", "C cap ker(K)=empty", "BLOCKED", "basis/sign/covariance blockers remain open"),
        ("CG1614_3_WEP", "WEP score", "BLOCKED", "tau/readout/material/source gates open"),
        ("CG1614_4_local_GR", "R10/Newton/local-GR claim", "BLOCKED", "source-normalization/local branch unresolved"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1614_0_parent_cone",
            "decision": "PARENT_CONE_BASIS_NOT_DERIVED",
            "reason": "the generator positivity theorem is exact but its physical clauses are unsigned",
            "next_action": "try to source/derive a generator positivity certificate rather than claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1614_1_official_acquisition",
            "decision": "OFFICIAL_CMSM_ARRAYS_NOT_ACQUIRED",
            "reason": "public pointer exists but no source-pack/readout/material/alignment rows are captured",
            "next_action": "use authenticated browser/HAR route or manual CMSM export if available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1614_2_next",
            "decision": "NEXT_1615_GENERATOR_POSITIVITY_CERTIFICATE_OR_LOCAL_BRANCH_DEMOTION",
            "reason": "if parent generator positivity cannot be signed, the local branch must be closure/source-data only",
            "next_action": "attempt the generator positivity certificate; otherwise demote local-GR route to explicit closure/data dependency",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1615-Y5-R2FR-generator-positivity-certificate-or-local-branch-demotion.md",
            "script": "scripts/Y5_R2FR_generator_positivity_certificate_or_local_branch_demotion.py",
            "objective": "try to sign the parent generator positivity certificate; if it fails, demote local-GR proof route to closure/source-data dependency",
            "success_condition": "parent-signed generator/readout/material/covariance certificate with c_min>0, or explicit demotion ledger that prevents accidental local-GR claims",
            "do_not": "do not use tau_eff=1, symbolic K alone, surrogate arrays, bound inversion, closure-only zero, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("source_acquired", "parent_signed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1614() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1614-Y5",
        "P8_Y5_PARENT_QLOC_1614",
        "P8_Y5_BRR545_1614",
        "Y5_R2FR_parent_cone_basis_or_official_CMSM_acquisition",
        "R2FR_parent_cone",
        "R2FR_generator_positivity",
        "R2FR_official_CMSM",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    acquisition = read_csv(OFFICIAL_ACQUISITION)
    parent_cone = read_csv(PARENT_CONE)
    generator = read_csv(GENERATOR_CERT)
    blockers = read_csv(BLOCKER_AUDIT)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1614_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1614 local source paths exist"),
        ("VAL1614_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1614 source needles found"),
        ("VAL1614_2_input_dir_ready", INPUT_1614.exists(), "1614 quarantine input directory exists"),
        ("VAL1614_3_acquisition_status", len(acquisition) >= 4 and all(row["source_acquired"].lower() == "false" for row in acquisition), "official CMSM acquisition status recorded without claiming files"),
        ("VAL1614_4_generator_lemma", any(row["theorem_id"] == "PCB1614_1_generator_positivity_lemma" and row["status"] == "EXACT_CONDITIONAL_LEMMA" for row in parent_cone), "generator positivity lemma recorded"),
        ("VAL1614_5_parent_cone_not_derived", any(row["theorem_id"] == "PCB1614_5_verdict" and row["status"] == "PARENT_CONE_BASIS_NOT_DERIVED" for row in parent_cone), "parent cone/basis theorem remains unproved"),
        ("VAL1614_6_contract_complete", len(generator) >= 6 and all(row["parent_signed"].lower() == "false" for row in generator), "generator positivity contract is complete and unsigned"),
        ("VAL1614_7_blockers_open", len(blockers) >= 6 and all(row["status"] == "OPEN_BLOCKER" for row in blockers), "parent cone blockers remain explicit"),
        ("VAL1614_8_runner_refuses", any(row["runner_id"] == "RUN1614_0_parent_cone" and row["runner_result"] == "REJECT_PARENT_CONE_PROOF" for row in runner), "runner rejects parent cone proof"),
        ("VAL1614_9_claim_gates_closed", gates and all(row["status"] == "BLOCKED" and row["claim_allowed"].lower() == "false" for row in gates), "all 1614 claim gates remain closed"),
        ("VAL1614_10_decision_next", any(row["decision"] == "NEXT_1615_GENERATOR_POSITIVITY_CERTIFICATE_OR_LOCAL_BRANCH_DEMOTION" for row in decisions), "decision selects 1615 generator positivity or demotion"),
        ("VAL1614_11_csv_parse", csv_parses(generated_csvs), "all generated 1614 CSVs parse"),
        ("VAL1614_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1614 rows are source-acquired, parent-signed, score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1614_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1614_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1614_15_formalization_untouched", no_formalization_1614(), "no 1614 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1614_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1614 parent cone/basis or official CMSM acquisition validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    parent_cone: list[dict[str, Any]],
    generator: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1614 - R2/fR Parent Cone Basis Or Official CMSM Acquisition",
                "## Verdict\n"
                "- 1614 tries to upgrade the signed-margin route into a parent cone/basis theorem.\n"
                "- The exact sufficient result is clean: a parent generator set with `K(g_i)>0` would prove `C cap ker(K)=empty` and give `c_min>0`.\n"
                "- The theorem is not physically closed: parent basis, generator list, readout signs, Ti/Pt material projection, covariance, and downstream-domain order are still unsigned.\n"
                "- Official CMSM acquisition remains live, but no source-pack/readout/material/alignment rows are captured into quarantine.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Official CMSM Acquisition Status",
                md_table(acquisition, ["acquisition_id", "object", "current_status", "why_not_enough", "source_acquired"]),
                "## Parent Cone/Basis Theorem Attempt",
                md_table(parent_cone, ["theorem_id", "status", "proof_result", "blocking_gap", "theorem_closed"]),
                "## Generator Positivity Certificate Contract",
                md_table(generator, ["contract_id", "required_fields", "purpose", "current_status", "parent_signed"]),
                "## Parent Cone Blocker Audit",
                md_table(blockers, ["blocker_id", "blocker", "effect", "required_fix", "status"]),
                "## Runner",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1614.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    acquisition = official_acquisition_rows()
    parent_cone = parent_cone_rows()
    generator = generator_certificate_rows()
    blockers = blocker_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        OFFICIAL_ACQUISITION,
        PARENT_CONE,
        GENERATOR_CERT,
        BLOCKER_AUDIT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(OFFICIAL_ACQUISITION, acquisition)
    write_csv(PARENT_CONE, parent_cone)
    write_csv(GENERATOR_CERT, generator)
    write_csv(BLOCKER_AUDIT, blockers)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, acquisition, parent_cone, generator, blockers, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
