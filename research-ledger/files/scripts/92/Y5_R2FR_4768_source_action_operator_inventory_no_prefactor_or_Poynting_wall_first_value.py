from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4768"
CLAIM_ID = "L-610"
MARKER = "PPC4161_SOURCE_ACTION_OPERATOR_INVENTORY_NO_PREFACTOR_OR_POYNTING_WALL_FIRST_VALUE_4768"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_ACTION_OPERATOR_INVENTORY_NO_PREFACTOR_OR_POYNTING_WALL_FIRST_VALUE_4768"
DECISION = "PRIVATE_GR_PARITY_NO_SOURCE_PREFACTOR_IMPORTED_INTO_SOURCE_QBASIC_CONTRACT_PUBLIC_PARENT_OPERATOR_INVENTORY_STILL_UNSIGNED_POYNTING_ZERO_CANDIDATE_STAGED_NONCLAIM"
NEXT_TARGET = "4769-Y5-R2FR-private-branch-source-qbasic-rollup-or-public-parent-operator-inventory-gap.md"

DOC_PATH = POST / "4768-Y5-R2FR-source-action-operator-inventory-no-prefactor-or-Poynting-wall-first-value.md"
FORMAL_PATH = FORMAL / "784-PPC4161-source-action-operator-inventory-no-prefactor-or-Poynting-wall-first-value.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_SOURCE_REGISTER.csv"
OPERATOR_INVENTORY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_SOURCE_ACTION_OPERATOR_INVENTORY.csv"
NO_PREFACTOR_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_NO_SOURCE_PREFACTOR_IMPORT_AUDIT.csv"
PRIVATE_BRANCH_ROLLUP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_PRIVATE_SOURCE_QBASIC_ROLLUP.csv"
PUBLIC_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_PUBLIC_PARENT_GAP_VECTOR.csv"
POYNTING_FIRST_VALUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_POYNTING_WALL_FIRST_VALUE_CANDIDATE.csv"
QEDGE_QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_QEDGE_QBAR_SOURCE_CONTRACT_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4768_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4768_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4768_0_4767_decision", SOURCE_DIR / "P8_Y5_R2FR_4767_DECISION.csv", "PARENT_SOURCE_QBASIC_CONTRACT_DERIVED", "4767 handoff decision"),
    ("SRC4768_1_4767_contract", SOURCE_DIR / "P8_Y5_R2FR_4767_PARENT_SOURCE_QBASIC_CONTRACT.csv", "PSC4767_3_measure_qbasic", "4767 source-qbasic contract"),
    ("SRC4768_2_4767_signature", SOURCE_DIR / "P8_Y5_R2FR_4767_SINGLE_PARENT_SIGNATURE_AUDIT.csv", "SIG4767_3_no_prefactor", "4767 no-prefactor signature gate"),
    ("SRC4768_3_4534_grammar", SOURCE_DIR / "P8_Y5_R2FR_4534_STRICT_MTS_PRIMITIVE_GRAMMAR.csv", "GRAM4534_2_forbidden_constructors", "4534 strict grammar forbidden constructors"),
    ("SRC4768_4_4534_induction", SOURCE_DIR / "P8_Y5_R2FR_4534_CONSTRUCTOR_EXHAUSTION_INDUCTION.csv", "IND4534_0_theorem", "4534 no-wA induction theorem"),
    ("SRC4768_5_4535_owner", SOURCE_DIR / "P8_Y5_R2FR_4535_OWNER_DERIVATION_SPLIT.csv", "OWN4535_0_root_edge_theorem", "4535 total Hilbert-source root edge"),
    ("SRC4768_6_4536_rank", SOURCE_DIR / "P8_Y5_R2FR_4536_CONNECTED_GRAPH_RANK_THEOREM.csv", "CGRT4536_0_exact_rank_statement", "4536 connected graph rank theorem"),
    ("SRC4768_7_4537_rank_results", SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv", "RR4537_2_GR_parity_adopted_branch", "4537 GR parity rank pass"),
    ("SRC4768_8_4537_adoption", SOURCE_DIR / "P8_Y5_R2FR_4537_GR_PARITY_ADOPTION_CERTIFICATE.csv", "AD4537_1_no_source_prefactor", "4537 private adoption certificate"),
    ("SRC4768_9_4445_no_prefac", SOURCE_DIR / "P8_Y5_R2FR_4445_NO_SOURCE_PREFAC_OUTPUT.csv", "NP4445_0_live_no_source_prefac_route", "4445 no source-prefactor route"),
    ("SRC4768_10_4446_adoption", SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv", "ADOPT4446_0_PPC4161_GR_parity_import", "4446 private GR parity adoption"),
    ("SRC4768_11_4446_residual", SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv", "RU4446_0_Delta_w_A", "4446 source-universality residual vector"),
    ("SRC4768_12_4447_rollup", SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv", "RU4447_0_source_weight_subvector", "4447 source-weight rollup"),
    ("SRC4768_13_4695_poynting", SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv", "FX4695_0_stationary_zero", "4695 Poynting stationary zero theorem"),
    ("SRC4768_14_4714_owner", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_4_no_double_count", "4714 Poynting no-double-count theorem"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OPERATOR_INVENTORY_CSV,
    NO_PREFACTOR_IMPORT_CSV,
    PRIVATE_BRANCH_ROLLUP_CSV,
    PUBLIC_GAP_CSV,
    POYNTING_FIRST_VALUE_CSV,
    QEDGE_QBAR_UPDATE_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| "
        + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def operator_inventory_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OP4768_0_total_Lmatter", "L_matter under one measure", "allowed root Hilbert source owner", "4535 signs root edge; component internals still audited", "ROOT_EDGE_SIGNED_PRIVATE"),
        ("OP4768_1_standard_component_graph", "lepton/quark/QCD/EM/binding component graph", "allowed only as one imported GR-parity matter functor with fixed theta", "4537 rank pass kills non-common weights inside private branch", "PRIVATE_GR_PARITY_ALLOWED"),
        ("OP4768_2_common_weight", "w_star S_matter", "calibration-only common mode", "harmless only if universal and derivative/source/frame/range silent", "COMMON_CALIBRATION_GUARDED"),
        ("OP4768_3_relative_weight", "sum_A w_A S_A with P_perp Delta_w_A != 0", "forbidden in private branch; retained public/off-branch", "source/species/material active-mass weight would be a real residual", "FORBIDDEN_PRIVATE_RETAINED_PUBLIC"),
        ("OP4768_4_source_label_Hom", "SpeciesLabel or MaterialLabel -> Coeff_active_source", "forbidden by strict grammar/no-Hom route", "not globally parent-derived; private GR-parity import forbids it", "FORBIDDEN_PRIVATE_UNDERIVED_PUBLIC"),
        ("OP4768_5_hidden_marker", "masses charges alpha_EM clock/material labels depending on parent vertical field", "retained unless fixed or quotient-owned theta", "feeds E_constant_marker and beta/source sensitivities", "RETAINED_PUBLIC_GAP"),
        ("OP4768_6_shadow_frame", "A_g(X)^2 g_obs or B_dis(X)dX dX", "retained unless no-shadow branch is signed", "would reintroduce scalar/disformal source coupling", "RETAINED_PUBLIC_GAP"),
        ("OP4768_7_EM_Hodge_owner", "independent Hodge/constitutive/current owner", "allowed only if same observed Maxwell-Hodge branch; otherwise retained", "feeds E_Hodge_EM and Poynting/EM residuals", "CONDITIONAL_OR_RETAINED"),
        ("OP4768_8_Poynting_wall", "radiative/open Poynting wall flux", "not an extra bulk force; boundary value or zero theorem", "stationary closed collar gives zero candidate; open collar needs values", "EXPLICIT_BOUNDARY_ROW"),
        ("OP4768_9_readout_reentry", "post-variation material/readout/source normalization re-entry", "forbidden in private branch; retained public/off-branch", "prevents source fitting after seeing local tests", "FORBIDDEN_PRIVATE_RETAINED_PUBLIC"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": operator_id,
            "operator_or_slot": operator,
            "inventory_class": inventory_class,
            "current_evidence": evidence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for operator_id, operator, inventory_class, evidence, status in specs
    ]


def no_prefactor_import_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("NPI4768_0_strict_grammar", "Strict MTS primitive grammar forbids SpeciesLabel -> Coeff_active_source", "4534 proves by induction if strict grammar uniqueness is signed", "CONDITIONAL_PUBLIC_THEOREM_UNSIGNED"),
        ("NPI4768_1_root_edge", "one L_matter and one measure derive total Hilbert source root edge", "4535 signs the literal root but not component no-wA", "ROOT_EDGE_SIGNED_COMPONENT_OPEN"),
        ("NPI4768_2_rank_theorem", "full rank on P_perp component-weight subspace kills relative weights", "4536 derives exact rank condition", "RANK_THEOREM_DERIVED"),
        ("NPI4768_3_rank_result", "standard visible template / private GR-parity import has zero P_perp kernel", "4537 rank results pass for private branch and fail for current parent-owned graph", "PRIVATE_PASS_PUBLIC_UNSIGNED"),
        ("NPI4768_4_private_adoption", "PPC4161 private branch adopts GR-parity no-source-prefactor invariant", "4446 sets Delta_w_A=0 and material reentry=0 inside private branch", "PRIVATE_BRANCH_ZERO_IMPORTED"),
        ("NPI4768_5_current_4767_insert", "source-qbasic contract PSC4767 can import Delta_w_A=0 only inside private branch", "public parent operator inventory remains unsigned", "INSERTED_PRIVATE_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "import_id": import_id,
            "statement": statement,
            "evidence": evidence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for import_id, statement, evidence, status in specs
    ]


def private_branch_rollup_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PBR4768_0_Delta_w_A", "Delta_w_A", "0", "private GR-parity source-universality branch", "closes relative component source weights inside private branch"),
        ("PBR4768_1_material_reentry", "material active-source reentry", "0", "private GR-parity source-universality branch", "material labels are readout inventory, not active-source coefficients"),
        ("PBR4768_2_E_source_prefactor", "E_source_prefactor", "0_private", "imports NPI4768_4 into 4767 source-qbasic contract", "removes one residual from private source-qbasic branch"),
        ("PBR4768_3_E_constant_marker", "E_constant_marker", "open_or_private_fixed", "needs fixed/quotient-owned theta and no alpha/mass drift", "not closed globally by no-prefactor alone"),
        ("PBR4768_4_E_Hodge_EM", "E_Hodge_EM", "open_or_private_same_Hodge", "needs Maxwell-Hodge/current owner", "not closed by no-prefactor alone"),
        ("PBR4768_5_E_Poynting_wall", "E_Poynting_wall", "zero_candidate_or_value_needed", "stationary collar zero candidate; open collar values missing", "explicit boundary row remains"),
        ("PBR4768_6_private_verdict", "source-qbasic private branch", "partially_reduced", "source-prefactor leg closed private; public parent and boundary/EM/denominator gates remain", "nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "rollup_id": rollup_id,
            "quantity": quantity,
            "branch_value": branch_value,
            "basis": basis,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for rollup_id, quantity, branch_value, basis, meaning in specs
    ]


def public_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PGV4768_0_strict_grammar_uniqueness", "strict MTS primitive grammar uniqueness", "not derived from parent action line", "needed for public no-wA theorem"),
        ("PGV4768_1_component_graph_parent_edges", "current MTS parent-owned component graph", "rank fails because signed edges absent", "needed to avoid GR-parity import closure"),
        ("PGV4768_2_fixed_theta_constants", "fixed/quotient-owned masses charges alpha_EM standards", "unsigned as one parent branch", "needed for q-basic source measure"),
        ("PGV4768_3_same_Hodge_current", "same Maxwell-Hodge/current owner", "conditional only", "needed for EM/Poynting Hilbert ownership"),
        ("PGV4768_4_boundary_Poynting", "stationary/no-flux collar or finite wall flux", "zero candidate staged; values missing for open collars", "needed for boundary silence or finite scoring"),
        ("PGV4768_5_denominator_projector", "M0 epsilon PiM Ecomm", "still source-value missing", "needed before Qbar/local scoring"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": gap_id,
            "gap": gap,
            "current_status": status,
            "why_it_matters": why,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gap_id, gap, status, why in specs
    ]


def poynting_first_value_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PFV4768_0_candidate_branch", "closed_stationary_same_Hodge_collar", "branch selector", "stationary isolated collar with no incoming/apparatus/radiative flux", "CANDIDATE_EXACT_ZERO_BRANCH_NOT_INSTANCE"),
        ("PFV4768_1_dUdt", "dU_EM_dt_abs", "0", "time-averaged stationary EM energy in collar", "EXACT_ZERO_IF_BRANCH_SIGNED"),
        ("PFV4768_2_JdotE", "JdotE_abs", "0", "no net internal work term over declared stationary averaging window", "EXACT_ZERO_IF_BRANCH_SIGNED"),
        ("PFV4768_3_incoming", "Phi_incoming_abs", "0", "no incoming/background radiation through collar", "EXACT_ZERO_IF_BRANCH_SIGNED"),
        ("PFV4768_4_apparatus", "Phi_apparatus_abs", "0", "no apparatus/support flux through collar", "EXACT_ZERO_IF_BRANCH_SIGNED"),
        ("PFV4768_5_total", "Phi_wall_Poynting_abs", "0", "sum of exact zero components", "ZERO_CANDIDATE_NONCLAIM_SOURCE_INSTANCE_MISSING"),
        ("PFV4768_6_open_fallback", "Phi_wall_Poynting_abs", "|dU_EM/dt|+|int_W J.E dV|+|Phi_incoming|+|Phi_apparatus|", "if branch is open/radiative/nonstationary", "BOUND_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "value_id": value_id,
            "quantity": quantity,
            "candidate_value_or_formula": value,
            "condition_or_evidence_needed": evidence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for value_id, quantity, value, evidence, status in specs
    ]


def qedge_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QQU4768_0_private_no_prefactor", "E_source_prefactor=0 inside private GR-parity branch", "removes source-weight leg from E_source_qbasic_open only inside private branch", "PRIVATE_INSERT_NONCLAIM"),
        ("QQU4768_1_public_no_prefactor", "E_source_prefactor remains open for public/global parent", "strict primitive or parent component graph proof still unsigned", "PUBLIC_GAP_RETAINED"),
        ("QQU4768_2_poynting_zero", "Phi_wall_Poynting_abs=0 candidate on closed stationary same-Hodge collar", "can zero Poynting boundary leg only if source instance/branch is declared", "CANDIDATE_ZERO_NONCLAIM"),
        ("QQU4768_3_qedge_shell", "Q_edge_shell_abs=0 needs source-qbasic measure plus support selector", "private source-prefactor closure helps but does not alone sign full source-qbasic measure", "SHELL_ZERO_STILL_CONDITIONAL"),
        ("QQU4768_4_qbar_score", "Qbar_XH score remains blocked by boundary/shadow/denominator/projector gates", "no local-GR/Newton/PPN score fires", "PRODUCT_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "rule": rule,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, rule, meaning, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4768_0_operator_inventory", "source action/operator inventory", "built; hidden source-weight slots are now typed and ranked", "COMPLETED"),
        ("ROUTE4768_1_no_prefactor_import", "import GR-parity no-source-prefactor into 4767", "closes Delta_w_A/E_source_prefactor inside private branch only", "COMPLETED_PRIVATE"),
        ("ROUTE4768_2_public_parent_gap", "strict primitive or parent component graph public proof", "still required for global/public source-qbasic theorem", "SELECTED_NEXT"),
        ("ROUTE4768_3_poynting_first_value", "closed stationary Poynting zero candidate", "staged exact-zero candidate; open-collar numeric values still missing", "PARALLEL"),
        ("ROUTE4768_4_denominator_projector", "M0 epsilon PiM Ecomm", "still mandatory before local score", "PARALLEL_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4768_0_private_scope", "Private GR-parity import cannot be promoted to public primitive derivation.", "blocks overclaim"),
        ("GATE4768_1_no_prefactor_scope", "Delta_w_A=0 is private-branch only unless strict grammar or parent component graph is signed.", "blocks source-weight smuggling"),
        ("GATE4768_2_poynting_instance", "Poynting zero candidate needs an actual closed stationary source collar declaration.", "blocks fake numeric zero"),
        ("GATE4768_3_no_double_count", "Poynting is Hilbert stress once or explicit wall flux, never both.", "blocks EM double count"),
        ("GATE4768_4_no_score", "No local-GR/Newton/R10/PPN/WEP/clock/orbital/Maxwell claim from 4768.", "keeps checkpoint private/nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4768_0_no_public_no_prefactor", "Do not claim public/global no-source-prefactor theorem from private GR-parity import.", "NONCLAIM"),
        ("FW4768_1_no_parent_SM_derivation", "Do not claim MTS derives the Standard Model or all matter constants.", "NONCLAIM"),
        ("FW4768_2_no_poynting_numeric_claim", "Do not treat the closed-collar zero candidate as measured/source-instance value.", "NONCLAIM"),
        ("FW4768_3_no_Qbar_score", "Do not score QbarXH without denominator/projector/boundary/shadow closure.", "NONCLAIM"),
        ("FW4768_4_local_only", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4768_0",
            "decision": DECISION,
            "summary": "4768 integrates the older no-source-prefactor/rank ladder into the current source-qbasic contract. Delta_w_A and material active-source reentry are zero inside the private GR-parity branch, so the source-prefactor leg is closed privately. The public/global parent proof remains unsigned because strict primitive grammar uniqueness or parent component graph ownership is not derived. A closed stationary Poynting wall zero candidate is staged, while open-collar numeric values remain missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4768_0",
            "state": "completed_nonclaim",
            "meaning": "Private branch source-prefactor closure is imported into the current source-qbasic contract; public parent proof and Poynting instance values remain live.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Roll up the private source-qbasic branch to see exactly which gates remain before local GR scoring, or attack the public parent operator-inventory gap by strict grammar/component graph ownership.",
            "route_priority": "private_branch_source_qbasic_rollup_then_public_parent_operator_inventory_gap_parallel_Poynting_instance_values",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    inventory: list[dict[str, Any]],
    no_prefactor: list[dict[str, Any]],
    private_rollup: list[dict[str, Any]],
    public_gap: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    qedge: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4768: Source Action Operator Inventory, No-Prefactor Import, or Poynting Wall First Value

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4768 imports the older no-source-prefactor/rank work into the current 4767 source-qbasic contract.

- Inside the private GR-parity standard-matter branch, `Delta_w_A=0` and material active-source reentry is zero.
- Therefore the `E_source_prefactor` leg of the 4767 source-qbasic residual vector is closed inside that private branch.
- This is not a public/global parent theorem: strict MTS primitive grammar uniqueness and current parent-owned component graph rank remain unsigned.
- A closed stationary same-Hodge Poynting collar gives a staged zero candidate `Phi_wall_Poynting_abs=0`; open/radiative collars still require values for `dU_EM_dt`, `JdotE`, `Phi_incoming`, and `Phi_apparatus`.
- No local-GR, Newton, R10, PPN, WEP, clock, orbital or Maxwell pass is claimed.

## Source Action Operator Inventory

{markdown_table(inventory, ["operator_id", "operator_or_slot", "inventory_class", "status"])}

## No-Source-Prefactor Import Audit

{markdown_table(no_prefactor, ["import_id", "statement", "status"])}

## Private Source-Qbasic Rollup

{markdown_table(private_rollup, ["rollup_id", "quantity", "branch_value", "meaning"])}

## Public Parent Gap Vector

{markdown_table(public_gap, ["gap_id", "gap", "current_status", "why_it_matters"])}

## Poynting Wall First-Value Candidate

{markdown_table(poynting, ["value_id", "quantity", "candidate_value_or_formula", "status"])}

## Qedge/Qbar Source Contract Update

{markdown_table(qedge, ["update_id", "rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4768: Source Operator Inventory and Private No-Prefactor Import

Generated: `{timestamp}`

## Core Result

The current source-qbasic contract can import the old no-source-prefactor ladder as follows:

```text
strict grammar / GR-parity imported matter functor
  -> no SpeciesLabel/MaterialLabel -> Coeff_active_source
  -> P_perp Delta_w_A = 0
  -> E_source_prefactor = 0
```

This import is valid only inside the private GR-parity standard-matter branch. It is not a public primitive derivation of matter from MTS.

Public/global gap:

```text
strict grammar uniqueness OR parent-owned component graph rank
```

is still unsigned.

Poynting candidate:

```text
closed stationary same-Hodge collar
  -> dU_EM_dt_abs=0
  -> JdotE_abs=0
  -> Phi_incoming_abs=0
  -> Phi_apparatus_abs=0
  -> Phi_wall_Poynting_abs=0.
```

Open/radiative collars keep:

```text
|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV|
                       + |Phi_incoming| + |Phi_apparatus|.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4768 imports the prior no-source-prefactor/rank ladder into the current source-qbasic contract.
- Inside the private GR-parity standard-matter branch, `Delta_w_A=0` and material active-source reentry is zero, so `E_source_prefactor=0` for that branch.
- The public/global parent proof remains unsigned: strict MTS primitive grammar uniqueness or current parent-owned component graph rank is still required.
- A closed stationary same-Hodge Poynting collar gives a staged zero candidate `Phi_wall_Poynting_abs=0`; open/radiative collars retain finite value rows.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4768 packet update: the source-prefactor leg is closed only inside the private GR-parity source branch. Public parent adoption remains an operator-inventory gap, not a theorem. Poynting has an exact closed-collar zero candidate and an open-collar finite-value route.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4768-Y5-R2FR-source-action-operator-inventory-no-prefactor-or-Poynting-wall-first-value.md`

## Decision

`{DECISION}`

## What moved forward

- Imported the prior no-source-prefactor/rank theorem into the current 4767 source-qbasic contract.
- Closed `Delta_w_A` and material active-source reentry only inside the private GR-parity branch.
- Kept public/global source-qbasic proof open until strict grammar uniqueness or parent component graph ownership is signed.
- Staged a closed-stationary Poynting zero candidate and retained open-collar value rows.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_source_operator_inventory_private_no_prefactor",
        "4768 imports the prior no-source-prefactor/rank ladder into the current source-qbasic contract, closing source-prefactor only inside the private GR-parity branch.",
        "Generated source register, source action operator inventory, no-prefactor import audit, private source-qbasic rollup, public parent gap vector, Poynting wall first-value candidate, Qedge/Qbar update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "private_GR_parity_no_source_prefactor_imported_public_parent_gap_retained_nonclaim",
        NEXT_TARGET,
        "Promoting private GR-parity import as public primitive MTS derivation or treating a Poynting zero candidate as a measured source value.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need private source-qbasic rollup or public parent operator-inventory gap closure.",
        "Source action operator inventory no-prefactor or Poynting wall first value",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    no_prefactor: list[dict[str, Any]],
    private_rollup: list[dict[str, Any]],
    public_gap: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    qedge: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4768_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4768_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4768_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4768_2_inventory", "operator inventory contains relative weight and Poynting rows", any(row["operator_id"] == "OP4768_3_relative_weight" for row in inventory) and any(row["operator_id"] == "OP4768_8_Poynting_wall" for row in inventory), str(OPERATOR_INVENTORY_CSV)))
    checks.append(("VAL4768_3_no_prefactor_import", "no-prefactor import closes private branch but not public", any(row["status"] == "PRIVATE_BRANCH_ZERO_IMPORTED" for row in no_prefactor) and any(row["status"] == "CONDITIONAL_PUBLIC_THEOREM_UNSIGNED" for row in no_prefactor), str(NO_PREFACTOR_IMPORT_CSV)))
    checks.append(("VAL4768_4_private_rollup", "private rollup sets Delta_w_A and source prefactor private zero", any(row["quantity"] == "Delta_w_A" and row["branch_value"] == "0" for row in private_rollup) and any(row["quantity"] == "E_source_prefactor" for row in private_rollup), str(PRIVATE_BRANCH_ROLLUP_CSV)))
    checks.append(("VAL4768_5_public_gap", "public gap retains strict grammar and parent component graph", any("strict" in row["gap"] for row in public_gap) and any("component graph" in row["gap"] for row in public_gap), str(PUBLIC_GAP_CSV)))
    checks.append(("VAL4768_6_poynting_candidate", "Poynting candidate has exact zeros and open fallback", any(row["quantity"] == "Phi_wall_Poynting_abs" and row["candidate_value_or_formula"] == "0" for row in poynting) and any(row["status"] == "BOUND_VALUES_MISSING" for row in poynting), str(POYNTING_FIRST_VALUE_CSV)))
    checks.append(("VAL4768_7_qedge_nonclaim", "Qedge update keeps private/public distinction", any(row["status"] == "PRIVATE_INSERT_NONCLAIM" for row in qedge) and any(row["status"] == "PUBLIC_GAP_RETAINED" for row in qedge), str(QEDGE_QBAR_UPDATE_CSV)))
    checks.append(("VAL4768_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4768_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4768_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4768_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4768_12_claim_row", "claim row L-610 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4768_13_resume", "resume points from 4768 to 4769", "4768-Y5" in resume_text and "4769-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4768_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4768_OVERALL",
            "check": "all 4768 operator-inventory/no-prefactor/Poynting checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    inventory = operator_inventory_rows(timestamp)
    no_prefactor = no_prefactor_import_rows(timestamp)
    private_rollup = private_branch_rollup_rows(timestamp)
    public_gap = public_gap_rows(timestamp)
    poynting = poynting_first_value_rows(timestamp)
    qedge = qedge_update_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OPERATOR_INVENTORY_CSV, inventory)
    write_csv(NO_PREFACTOR_IMPORT_CSV, no_prefactor)
    write_csv(PRIVATE_BRANCH_ROLLUP_CSV, private_rollup)
    write_csv(PUBLIC_GAP_CSV, public_gap)
    write_csv(POYNTING_FIRST_VALUE_CSV, poynting)
    write_csv(QEDGE_QBAR_UPDATE_CSV, qedge)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, inventory, no_prefactor, private_rollup, public_gap, poynting, qedge, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, inventory, no_prefactor, private_rollup, public_gap, poynting, qedge, gates, timestamp))


if __name__ == "__main__":
    main()
