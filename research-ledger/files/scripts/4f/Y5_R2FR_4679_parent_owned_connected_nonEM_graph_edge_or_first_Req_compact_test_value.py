from __future__ import annotations

import csv
import io
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4679"
CLAIM_ID = "L-521"
BRANCH = "MTS_R2FR_Y5_PARENT_CONNECTED_NONEM_GRAPH_GR_PARITY_IMPORT_4679"
MARKER = "PPC4161_PARENT_CONNECTED_NONEM_GRAPH_GR_PARITY_IMPORT_4679"
PACKET_MARKER = "PPC4161_PACKET_PARENT_CONNECTED_NONEM_GRAPH_GR_PARITY_IMPORT_4679"
DECISION = "GR_PARITY_NONEM_SOURCE_SUBVECTOR_ZERO_IMPORTED_TO_4678_VECTOR_NON_SOURCE_RESIDUALS_REMAIN"
NEXT_TARGET = "4680-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"

DOC_PATH = POST / "4679-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
FORMAL_PATH = FORMAL / "695-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

FORMAL_459 = FORMAL / "459-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
FORMAL_460 = FORMAL / "460-PPC4161-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
FORMAL_461 = FORMAL / "461-PPC4161-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md"
FORMAL_462 = FORMAL / "462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
FORMAL_463 = FORMAL / "463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
FORMAL_694 = FORMAL / "694-PPC4161-source-charge-Htau-MHref-coupling-tail-or-Jsourceweight-nonEM-bound-row.md"

CSV_4678_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4678_JSOURCEWEIGHT_SOURCE_CHARGE_SPLIT.csv"
CSV_4678_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4678_NEXT_TARGET.csv"
CSV_4443_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_ROOT_EDGE_OUTPUT.csv"
CSV_4443_SPECIES = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_SPECIES_EDGE_OUTPUT.csv"
CSV_4443_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4443_DECISION.csv"
CSV_4444_COMPONENT = SOURCE_DIR / "P8_Y5_R2FR_4444_STANDARD_COMPONENT_EDGE_OUTPUT.csv"
CSV_4444_PARENT = SOURCE_DIR / "P8_Y5_R2FR_4444_PARENT_COMPONENT_CERT_OUTPUT.csv"
CSV_4444_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4444_DECISION.csv"
CSV_4445_IMPORT = SOURCE_DIR / "P8_Y5_R2FR_4445_GR_PARITY_SM_IMPORT_OUTPUT.csv"
CSV_4445_NOPREFAC = SOURCE_DIR / "P8_Y5_R2FR_4445_NO_SOURCE_PREFAC_OUTPUT.csv"
CSV_4445_COUNTER = SOURCE_DIR / "P8_Y5_R2FR_4445_COUNTERMODEL_ROWS.csv"
CSV_4445_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4445_DECISION.csv"
CSV_4446_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv"
CSV_4446_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv"
CSV_4446_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4446_DECISION.csv"
CSV_4447_PPN = SOURCE_DIR / "P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_OUTPUT.csv"
CSV_4447_ROLLUP = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"
CSV_4447_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4447_DECISION.csv"
CSV_4447_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4447_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4679_SOURCE_REGISTER.csv"
LADDER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_NONEM_GRAPH_GR_PARITY_LADDER.csv"
VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_JSOURCEWEIGHT_AFTER_GR_PARITY_IMPORT.csv"
PPN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_PPN_SOURCE_SUBVECTOR_ZERO_IMPORT.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_NON_SOURCE_SURVIVOR_VECTOR.csv"
TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_REQ_MATERIAL_TAIL_INPUTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4679_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4679_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4679_00_4678_next", CSV_4678_NEXT, "parent-sign a connected nonEM graph/current edge", "4678 selected connected nonEM graph/current target."),
        ("SRC4679_01_4678_vector", CSV_4678_VECTOR, "VEC4678_3_current_claim_safe_vector", "4678 current source-weight vector before graph/adoption import."),
        ("SRC4679_02_formal694", FORMAL_694, "J_source_weight_nonEM", "formal 4678 split."),
        ("SRC4679_03_4443_root", CSV_4443_ROOT, "ROOT4443_0_core_Lmatter_to_T_H", "total L_matter to Hilbert stress root edge signed."),
        ("SRC4679_04_4443_species", CSV_4443_SPECIES, "EDGE4443_3_future_component_edge_contract", "component edge contract after root edge."),
        ("SRC4679_05_4443_decision", CSV_4443_DECISION, "NONEM_HILBERT_STRESS_ROOT_EDGE_SIGNED", "4443 root-edge decision."),
        ("SRC4679_06_formal459", FORMAL_459, "L_matter -> T_H", "formal root edge checkpoint."),
        ("SRC4679_07_4444_component", CSV_4444_COMPONENT, "COMP4444_0_L_to_lepton_import", "standard component import graph rows."),
        ("SRC4679_08_4444_parent", CSV_4444_PARENT, "PARENT4444_2_future_parent_contract", "parent component contract row."),
        ("SRC4679_09_4444_decision", CSV_4444_DECISION, "STANDARD_LMATTER_COMPONENT_IMPORT_GRAPH_CONTRACT_WRITTEN", "4444 component expansion decision."),
        ("SRC4679_10_formal460", FORMAL_460, "standard component import graph contract written", "formal component import expansion."),
        ("SRC4679_11_4445_import", CSV_4445_IMPORT, "IMP4445_0_live_core_GR_parity_import", "GR-parity SM import theorem-ready row."),
        ("SRC4679_12_4445_noprefac", CSV_4445_NOPREFAC, "NP4445_0_live_no_source_prefac_route", "no-source-prefactor theorem-ready row."),
        ("SRC4679_13_4445_counter", CSV_4445_COUNTER, "CM4445_0_weighted_components", "weighted-component countermodel guard."),
        ("SRC4679_14_4445_decision", CSV_4445_DECISION, "GR_PARITY_STANDARD_MATTER_IMPORT_NO_SOURCE_PREFAC_THEOREM_READY", "4445 no-prefactor decision."),
        ("SRC4679_15_formal461", FORMAL_461, "MTS does not need to derive every Standard Model term", "formal GR-parity theorem."),
        ("SRC4679_16_4446_adoption", CSV_4446_ADOPTION, "ADOPT4446_0_PPC4161_GR_parity_import", "private branch adoption."),
        ("SRC4679_17_4446_residual", CSV_4446_RESIDUAL, "RU4446_0_Delta_w_A", "Delta_w_A zero inside private branch."),
        ("SRC4679_18_4446_decision", CSV_4446_DECISION, "GR_PARITY_STANDARD_MATTER_IMPORT_PRIVATE_BRANCH_ADOPTED", "4446 adoption decision."),
        ("SRC4679_19_formal462", FORMAL_462, "Delta_w_A=0 becomes branch-internal", "formal private adoption."),
        ("SRC4679_20_4447_ppn", CSV_4447_PPN, "PPN4447_0_WEP_eta_source_charge", "source-universality PPN pieces."),
        ("SRC4679_21_4447_rollup", CSV_4447_ROLLUP, "RU4447_0_source_weight_subvector", "source subvector zero rollup."),
        ("SRC4679_22_4447_decision", CSV_4447_DECISION, "SOURCE_UNIVERSALITY_PIECES_PROPAGATED", "4447 propagation decision."),
        ("SRC4679_23_4447_validation", CSV_4447_VALIDATION, "VAL4447_20_pycache_absent", "4447 validation."),
        ("SRC4679_24_formal463", FORMAL_463, "Delta_w_A = 0 and material-source reentry = 0", "formal source-subvector propagation."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def ladder_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LAD4679_0_total_root_edge", "L_matter -> T_H", "BRANCH_SIGNED", "total standard matter Hilbert stress/current exists before readout", "does not prove component weights"),
        ("LAD4679_1_component_import_graph", "L_matter -> lepton/quark/QCD component slots", "IMPORT_READY", "standard component graph is usable as GR-parity import", "not strict MTS microphysics derivation"),
        ("LAD4679_2_no_source_prefactor", "Hom(SpeciesLabel/MaterialLabel,Coeff_active_source)=empty", "THEOREM_READY", "forbids hidden w_A component source multipliers", "requires branch adoption"),
        ("LAD4679_3_private_adoption", "PPC4161 GR-parity SM import", "PRIVATE_BRANCH_ADOPTED", "Delta_w_A and material source reentry are zero in private branch", "not public/strict primitive proof"),
        ("LAD4679_4_ppn_propagation", "source-universality subvector", "ZERO_PRIVATE_SUBVECTOR", "source-weight/material-reentry pieces of WEP/PPN/Gdot/clock/orbital rows are zero", "non-source residuals remain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "ladder_id": row[0],
            "object": row[1],
            "status": row[2],
            "what_it_closes": row[3],
            "what_remains": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "VEC4679_0_input_from_4678",
            "J_source_weight_abs_4678_current",
            "|J_EM_open_dynamic| + |J_rel_nonEM_owner_gap| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "4678 current vector before adoption import",
            "INPUT_VECTOR",
        ),
        (
            "VEC4679_1_private_GR_parity_zero",
            "J_rel_nonEM_owner_gap",
            "0",
            "inside PPC4161 private GR-parity SM import/no-source-prefactor branch",
            "ZERO_INSIDE_PRIVATE_BRANCH",
        ),
        (
            "VEC4679_2_after_GR_parity_import",
            "J_source_weight_abs_after_GR_parity",
            "|J_EM_open_dynamic| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "relative nonEM source weights removed in private branch; same-current/common/open tails remain",
            "REDUCED_VECTOR_NONCLAIM",
        ),
        (
            "VEC4679_3_public_or_strict_control",
            "J_source_weight_abs_public_control",
            "|J_rel_nonEM_public_or_primitive_gap| + |J_EM_open_dynamic| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "public/strict primitive branch still carries the nonEM gap until strict origin or empirical values close",
            "PUBLIC_CONTROL_RETAINED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "vector_id": row[0],
            "symbol": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def ppn_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PPN4679_0_WEP_eta", "WEP eta_AB", "source-weight/material-reentry piece", "0", "material inventory values and direct matter-charge residuals remain empirical"),
        ("PPN4679_1_gamma", "gamma-1", "source-normalization piece", "0", "metric principal/scalar/domain residuals remain"),
        ("PPN4679_2_beta", "beta-1", "source-normalization piece", "0", "EH nonlinear readout/non-source clauses remain"),
        ("PPN4679_3_alpha_i", "alpha_i", "source-frame/source-split piece", "0", "domain/projector and boundary channels remain"),
        ("PPN4679_4_xi_zeta", "xi,zeta_i", "source-weight nonconservation piece", "0", "boundary/projector/Hilbert-conservation channels remain"),
        ("PPN4679_5_Gdot", "Gdot/G", "source-measure/material-reentry piece", "0", "memory/nonlocal kappa drift channels remain"),
        ("PPN4679_6_clock_orbital", "clock/orbital source charge", "material-reentry piece", "0", "clock/Hodge/EM and Hilbert-worldtube glue remain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "ppn_id": row[0],
            "observable": row[1],
            "zeroed_piece": row[2],
            "private_branch_value": row[3],
            "survivor": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4679_0_metric_principal", "metric principal/EH readout", "gamma/beta/nonlinear local GR", "same-metric EH readout and nonlinear GR limit still need survivor map"),
        ("SURV4679_1_domain_projector", "domain/projector vector drift", "alpha_i/xi/preferred-frame rows", "projector silence or finite bound rows still needed"),
        ("SURV4679_2_boundary_hilbert", "boundary flux/Hilbert conservation", "zeta_i/alpha3/source-current conservation", "boundary silence and conservation gates remain"),
        ("SURV4679_3_memory_kappa", "memory/nonlocal kappa drift", "Gdot/G and source normalization over time", "memory/kappa derivative rows remain"),
        ("SURV4679_4_EM_open", "open/dynamic EM and Poynting/Hilbert side channels", "clock/PPN/local source current", "fixed EM is narrowed but open/dynamic EM remains"),
        ("SURV4679_5_material_Req_values", "material inventory and R_eq values", "WEP/clock/orbital/Newton compact tests", "projection coefficient, residual value, arena bound and source path missing"),
        ("SURV4679_6_strict_primitive_origin", "motion/time/space primitive derivation of no-source-prefactor", "public theory claim", "private adoption does not prove strict primitive origin"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": row[0],
            "residual_class": row[1],
            "arena": row[2],
            "needed_to_close": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def tail_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("TAIL4679_0_R_eq_compact", "R_eq_compact_test", "R_eq[varphi]=<Pi_M J_H-J_M_top-dB_zero,varphi>", "MISSING_P_REQ_COMPACT", "MISSING_REQ_COMPACT_TEST_VALUE", "MISSING_ARENA_BOUND"),
        ("TAIL4679_1_material_projection", "material_projection_Req", "R_material=Pi_material(T_H)-Pi_material(T_inventory)", "MISSING_MATERIAL_PROJECTION_COEFF", "MISSING_MATERIAL_RESIDUAL_VALUE", "MISSING_ARENA_BOUND"),
        ("TAIL4679_2_Bzero_flux", "B_zero_boundary_flux", "Phi_B=int_partialW B_zero/M_H_ref", "MISSING_P_BZERO", "MISSING_BZERO_FLUX_VALUE", "MISSING_ARENA_BOUND"),
        ("TAIL4679_3_epsilon_HM", "Htau_MHref_mismatch", "epsilon_HM=|H_tau[S]-H_ref-M_H_ref|/M_H_ref", "MISSING_P_HM", "MISSING_HTAU_MHREF_VALUE", "MISSING_ARENA_BOUND"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "projection_coeff": row[3],
            "residual_value": row[4],
            "arena_bound": row[5],
            "numeric_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4679_0_private_not_public", "Private GR-parity adoption zeroes source weights only inside PPC4161; it is not public/strict primitive local-GR proof.", "ACTIVE"),
        ("CTRL4679_1_no_smuggling_full_ppn", "Do not erase metric, domain/projector, boundary, memory or EM/Poynting residuals with a source-universality theorem.", "ACTIVE"),
        ("CTRL4679_2_no_observed_GM_backfill", "Do not use observed GM, fitted G_N or comparator bounds as R_eq/material residual values.", "ACTIVE"),
        ("CTRL4679_3_standard_model_scope", "MTS does not need to derive the Standard Model for GR parity, but must state the import/no-source-prefactor invariant explicitly.", "ACTIVE"),
        ("CTRL4679_4_next_map", "Next work must rank non-source PPN survivors or source one material/R_eq tail value.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4679 imports the 4443-4447 graph/adoption trail into the post-4678 source-weight vector. The total Hilbert root edge is branch-signed; standard component import and no-source-prefactor theorem are ready; PPC4161 privately adopts the GR-parity import invariant; therefore J_rel_nonEM and material active-source reentry are zero inside the private branch. Non-source PPN/Newton residuals and material/R_eq numeric values remain live.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "total_Hilbert_root_edge_signed": True,
            "standard_component_import_ready": True,
            "GR_parity_private_adopted": True,
            "J_rel_nonEM_zero_private_branch": True,
            "PPN_source_subvector_zero_private_branch": True,
            "non_source_residuals_closed": False,
            "material_Req_values_sourced": False,
            "strict_primitive_origin_signed": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After source-universality pieces are zeroed privately, the useful next cut is the non-source residual survivor map and the first material/R_eq numeric acquisition route.",
            "derive_route": "Separate metric-principal, domain/projector, boundary/Hilbert conservation, memory/kappa and EM/Poynting residual classes; choose the cheapest exact zero proof.",
            "fallback_route": "Fill one material projection, R_eq compact-test, B_zero flux or epsilon_HM row with source path, units, projection coefficient, residual value, arena bound and no-cancellation guard.",
            "avoid": "Do not treat private source-universality as full local-GR/PPN proof, and do not use observed GM/fitted G_N as residual values.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    ladder: list[dict[str, Any]],
    vectors: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    tails: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    ladder_ok = any(row["ladder_id"] == "LAD4679_3_private_adoption" and row["status"] == "PRIVATE_BRANCH_ADOPTED" for row in ladder)
    vector_ok = any(row["vector_id"] == "VEC4679_2_after_GR_parity_import" for row in vectors)
    ppn_ok = len(ppn) >= 7 and all(row["private_branch_value"] == "0" for row in ppn)
    survivor_ok = any(row["survivor_id"] == "SURV4679_0_metric_principal" for row in survivors) and any(row["survivor_id"] == "SURV4679_5_material_Req_values" for row in survivors)
    tail_ok = all(any(row["tail_id"] == tail_id for row in tails) for tail_id in ["TAIL4679_0_R_eq_compact", "TAIL4679_1_material_projection"])
    nonclaim_ok = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in [*ladder, *vectors, *ppn, *survivors, *tails])
    checks = [
        ("RUN4679_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4679_1_ladder", ladder_ok, "GR-parity private adoption ladder present" if ladder_ok else "adoption ladder missing"),
        ("RUN4679_2_vector", vector_ok, "post-adoption vector written" if vector_ok else "vector update missing"),
        ("RUN4679_3_ppn_source", ppn_ok, "source PPN subvector zero rows written" if ppn_ok else "PPN source subvector incomplete"),
        ("RUN4679_4_survivors", survivor_ok, "non-source survivors preserved" if survivor_ok else "survivor map incomplete"),
        ("RUN4679_5_tails", tail_ok, "material/R_eq tail contracts written" if tail_ok else "tail contracts missing"),
        ("RUN4679_6_nonclaim", nonclaim_ok, "all generated rows remain nonclaim" if nonclaim_ok else "claim flag promoted"),
        ("RUN4679_7_next", True, "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": check_id,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def validation_rows(timestamp: str, csv_paths: list[Path], sources: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    rows.append({"validation_id": "VAL4679_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            passed = bool(parsed)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
        except Exception as exc:
            passed = False
            detail = repr(exc)
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4679_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4679_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    outputs_exist = all(path.exists() for path in [DOC_PATH, FORMAL_PATH, *csv_paths])
    rows.append({"validation_id": "VAL4679_2_outputs_exist", "passed": outputs_exist, "detail": "post/formal/csv outputs exist", "timestamp_utc": timestamp})
    claim_row = CLAIM_ID in read_text(CLAIMS_PATH)
    rows.append({"validation_id": "VAL4679_3_claim_row_exists", "passed": claim_row, "detail": f"{CLAIM_ID} present" if claim_row else f"{CLAIM_ID} missing", "timestamp_utc": timestamp})
    markers = MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)
    rows.append({"validation_id": "VAL4679_4_markers", "passed": markers, "detail": "spine and packet markers present" if markers else "marker missing", "timestamp_utc": timestamp})
    no_claim = "valid_for_claim,true" not in read_text(RUNNER_CSV).lower() and "claim_allowed,true" not in read_text(RUNNER_CSV).lower()
    rows.append({"validation_id": "VAL4679_5_no_claim_promotion", "passed": no_claim, "detail": "runner remains nonclaim", "timestamp_utc": timestamp})
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows.append({"validation_id": "VAL4679_6_pycache_absent", "passed": pycache_absent, "detail": "scripts __pycache__ absent" if pycache_absent else "scripts __pycache__ present", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and claim_row and markers and no_claim and pycache_absent
    rows.append({"validation_id": "VAL4679_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    ladder: list[dict[str, Any]],
    vectors: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4679 - Y5/R2FR Parent-Owned Connected nonEM Graph Edge or First Req Compact-Test Value

**Current verdict:** 4679 makes a private-branch reduction, not a public claim.

The 4443-4447 trail gives this ladder:

```text
L_matter -> T_H root edge branch-signed
+ standard component graph import-ready
+ GR-parity no-source-prefactor theorem ready
+ PPC4161 private adoption
=> Delta_w_A = 0 and material source re-entry = 0 inside the private branch.
```

Imported into the 4678 vector:

```text
J_source_weight_abs_4678_current
  = |J_EM_open_dynamic|
  + |J_rel_nonEM_owner_gap|
  + |J_common_derivative|
  + |R_eq|
  + |B_zero|
  + |epsilon_HM|

PPC4161 GR-parity private branch:
J_rel_nonEM_owner_gap = 0

J_source_weight_abs_after_GR_parity
  = |J_EM_open_dynamic|
  + |J_common_derivative|
  + |R_eq|
  + |B_zero|
  + |epsilon_HM|.
```

The source-weight/material-reentry pieces of WEP, PPN, `Gdot/G`, clock and orbital rows are zero inside the private branch. Metric principal, domain/projector, boundary, memory/kappa, open EM/Poynting, material inventory and `R_eq` numeric values remain live.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## nonEM graph / GR-parity ladder

{table(ladder)}

## Jsourceweight after GR-parity import

{table(vectors)}

## PPN source-subvector zero import

{table(ppn)}

## Non-source survivor vector

{table(survivors)}

## Req/material tail inputs

{table(tails)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4679 -", "# 695 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        append_once(
            CLAIMS_PATH,
            CLAIM_ID,
            csv_line(
                [
                    CLAIM_ID,
                    "local_gr_empirical_interface",
                    "4679 imports the 4443-4447 graph/adoption trail into the 4678 source-weight vector. The total L_matter to Hilbert stress root edge is branch-signed; standard component graph and GR-parity no-source-prefactor import are ready; PPC4161 privately adopts the invariant; therefore J_rel_nonEM and material active-source reentry are zero inside the private branch. Non-source PPN/Newton residuals and material/R_eq numeric values remain live.",
                    "Generated source register, nonEM graph/GR-parity ladder, after-GR-parity source-weight vector, PPN source-subvector zero rows, non-source survivor vector, Req/material tail inputs, controls, runner, decision, status, next target and validation.",
                    DECISION.lower(),
                    NEXT_TARGET,
                    "Treating private adoption as public local-GR proof, erasing non-source residuals, using fitted G_N/observed GM as residual values, or claiming strict MTS primitive derivation of Standard Model/no-source-prefactor.",
                    "local_gr",
                    str(DOC_PATH),
                    NEXT_TARGET,
                    "No public local-GR/Newton/PPN/R10 claim until non-source residuals are mapped/closed or source-backed material/R_eq values pass.",
                ]
            ),
        )

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4679 reduces the post-4678 source-weight vector inside the PPC4161 private GR-parity branch:

```text
J_source_weight_abs_after_GR_parity
  = |J_EM_open_dynamic| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|
```

The relative nonEM component-source weight gap is zero only inside the private branch because GR-parity SM import/no-source-prefactor/source-label forgetting is adopted. This also zeroes source-weight/material-reentry pieces of WEP/PPN/Gdot/clock/orbital rows, but non-source residuals remain live.

- checkpoint: `{DOC_PATH.name}`
- formal note: `{FORMAL_PATH.name}`
- decision: `{DECISION}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Packet update: the nonEM source-weight gap is no longer live inside PPC4161's private GR-parity import branch. Remaining local-GR work is now a non-source residual survivor map plus material/`R_eq` numeric acquisition.

- claim id: `{CLAIM_ID}`
- ladder csv: `{LADDER_CSV.name}`
- vector csv: `{VECTOR_CSV.name}`
- ppn csv: `{PPN_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    ladder = ladder_rows(timestamp)
    vectors = vector_rows(timestamp)
    ppn = ppn_rows(timestamp)
    survivors = survivor_rows(timestamp)
    tails = tail_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, ladder, vectors, ppn, survivors, tails)

    csv_paths = [
        SOURCE_REGISTER,
        LADDER_CSV,
        VECTOR_CSV,
        PPN_CSV,
        SURVIVOR_CSV,
        TAIL_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LADDER_CSV, ladder)
    write_csv(VECTOR_CSV, vectors)
    write_csv(PPN_CSV, ppn)
    write_csv(SURVIVOR_CSV, survivors)
    write_csv(TAIL_CSV, tails)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, ladder, vectors, ppn, survivors, tails, controls, runners, decisions, statuses, nexts, [])
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, ladder, vectors, ppn, survivors, tails, controls, runners, decisions, statuses, nexts, validations)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
