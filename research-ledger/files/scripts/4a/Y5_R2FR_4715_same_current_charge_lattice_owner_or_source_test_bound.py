from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4715"
CLAIM_ID = "L-557"
MARKER = "PPC4161_SAME_CURRENT_CHARGE_LATTICE_OWNER_OR_SOURCE_TEST_BOUND_4715"
PACKET_MARKER = "PPC4161_PACKET_SAME_CURRENT_CHARGE_LATTICE_OWNER_OR_SOURCE_TEST_BOUND_4715"
DECISION = "SAME_CURRENT_THEOREM_DERIVED_CONDITIONAL_CHARGE_LATTICE_PARTIAL_CURRENT_RESCALE_AND_SOURCE_TEST_BOUNDS_RETAINED_NONCLAIM"
NEXT_TARGET = "4716-Y5-R2FR-current-rescale-no-morphism-proof-or-first-source-test-coefficient-row.md"

DOC_PATH = POST / "4715-Y5-R2FR-same-current-charge-lattice-owner-or-source-test-bound.md"
FORMAL_PATH = FORMAL / "731-PPC4161-same-current-charge-lattice-owner-or-source-test-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4714_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4714_NEXT_TARGET.csv"
CSV_4714_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4714_CURRENT_CONSERVATION_EXCHANGE_ROWS.csv"
CSV_4714_SIDE = SOURCE_DIR / "P8_Y5_R2FR_4714_SIDECHANNEL_BOUND_ROWS.csv"
CSV_4714_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4714_VALIDATION.csv"
CSV_1100_THEOREM = SOURCE_DIR / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv"
CSV_1100_SIGNATURE = SOURCE_DIR / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv"
CSV_1100_ACQ = SOURCE_DIR / "P8_Y5_R10_1100_TQ_REQUIRED_SOURCE_ACQUISITION_LEDGER.csv"
CSV_1100_ALPHA = SOURCE_DIR / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv"
CSV_1100_DECISION = SOURCE_DIR / "P8_Y5_R10_1100_DECISION_LEDGER.csv"
CSV_1814_VISIBLE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv"
CSV_1815_RESCALE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"
CSV_1798_PARENT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1798_PARENT_CURRENT_OWNER_ATTEMPT.csv"
CSV_1779_CONV = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1779_PARENT_CURRENT_SOURCE_FUNCTOR_CONVERGENCE.csv"
CSV_1734_PROJECT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1734_PROJECTABLE_CURRENT_THEOREM.csv"
CSV_1733_DESCENT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv"
CSV_3503_BOUND = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_3508_WARD = SOURCE_DIR / "P8_EM_current_source_Ward_alpha_source_residual.csv"
CSV_3513_ELLJ = SOURCE_DIR / "P8_EM_ellJ_source_current_owner_residual_law.csv"
CSV_3527_STATUS = SOURCE_DIR / "P8_EM_alpha_level_current_owner_status.csv"
CSV_3601_STATUS = SOURCE_DIR / "P8_Y5_ellJ_source_current_normalization_status.csv"
CSV_SOURCE_WARD = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
CSV_765_MKI = SOURCE_DIR / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_765_RESCALE = SOURCE_DIR / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
CSV_988_LOCK = SOURCE_DIR / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"
CSV_4702_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4702_GAUGE_OWNER_CLAUSES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4715_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_SAME_CURRENT_CHARGE_LATTICE_THEOREM.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_CURRENT_OWNER_RESIDUAL_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_SOURCE_TEST_ARENA_BOUND_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4715_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4715_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
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
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once(timestamp: str) -> None:
    existing = text(CLAIMS_PATH)
    if existing.startswith(CLAIM_ID + ",") or f"\n{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4715 derives the exact same-current/charge-lattice owner theorem conditionally and stages finite source/test current mismatch bounds.",
        "current_evidence": "Generated source register, same-current theorem rows, current-owner residual rows, source/test arena bounds, gates, firewalls, decision, status, next target and validation.",
        "status": "same_current_charge_lattice_conditional_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking compact U(1) relative charge labels for a nonrescalable observed charge/current normalization.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Same-current charge-lattice owner or source-test bound",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or list(row)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writerow({field: row.get(field, "") for field in fields})


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4715_00_4714_next", CSV_4714_NEXT, "NT4714_0", "4714 handoff to same-current owner"),
        ("SRC4715_01_4714_current", CSV_4714_CURRENT, "CUR4714_0_same_current_identity", "same-current residual identity"),
        ("SRC4715_02_4714_arena", CSV_4714_CURRENT, "CUR4714_3_arena_source_coupling", "arena transfer schema"),
        ("SRC4715_03_4714_side", CSV_4714_SIDE, "SC4714_1_current_owner", "current owner side-channel row"),
        ("SRC4715_04_4714_validation", CSV_4714_VALIDATION, "VAL4714_OVERALL", "4714 validation"),
        ("SRC4715_05_1100_conditional", CSV_1100_THEOREM, "TQT1100_0_exact_conditional", "T_Q conditional theorem"),
        ("SRC4715_06_1100_compact", CSV_1100_THEOREM, "TQT1100_1_compact_U1_limit", "compact U1 partial support"),
        ("SRC4715_07_1100_rescale", CSV_1100_THEOREM, "TQT1100_2_rescaling_countermodel", "generator normalization countermodel"),
        ("SRC4715_08_1100_signature_current", CSV_1100_SIGNATURE, "TQS1100_4_same_current_owner", "same current owner signature"),
        ("SRC4715_09_1100_signature_verdict", CSV_1100_SIGNATURE, "TQS1100_6_verdict", "T_Q signature not derived"),
        ("SRC4715_10_1100_acq_current", CSV_1100_ACQ, "ACQ1100_5_current", "required current-owner source"),
        ("SRC4715_11_1100_alpha_total", CSV_1100_ALPHA, "Z1100_4_total", "alpha normalization finite branch"),
        ("SRC4715_12_1100_decision", CSV_1100_DECISION, "DEC1100_1_signature_result", "1100 decision"),
        ("SRC4715_13_1814_target", CSV_1814_VISIBLE, "VCC1814_0_target", "visible connection/current owner theorem"),
        ("SRC4715_14_1814_variation", CSV_1814_VISIBLE, "VCC1814_2_current_variation", "J_Q variation owner"),
        ("SRC4715_15_1814_rescale", CSV_1814_VISIBLE, "VCC1814_3_rescaling_exclusion", "current rescaling exclusion"),
        ("SRC4715_16_1815_post", CSV_1815_RESCALE, "NCR1815_0_target", "post-variation no-rescale theorem"),
        ("SRC4715_17_1815_pre", CSV_1815_RESCALE, "NCR1815_2_pre_variation_weight", "pre-variation weight survives"),
        ("SRC4715_18_1815_connected", CSV_1815_RESCALE, "NCR1815_3_connected_naturality", "connected matter naturality route"),
        ("SRC4715_19_1798_parent", CSV_1798_PARENT, "PCO1798_6_verdict", "parent current owner not signed"),
        ("SRC4715_20_1779_convergence", CSV_1779_CONV, "PCS1779_4_current_verdict", "source functor convergence fail"),
        ("SRC4715_21_1734_project", CSV_1734_PROJECT, "PCT1734_0_projectable_current_identity", "projectable current identity"),
        ("SRC4715_22_1733_descent", CSV_1733_DESCENT, "DCL1733_7_verdict", "descent current not signed"),
        ("SRC4715_23_3503_CJQ", CSV_3503_BOUND, "EMB3503_3_C_JQ", "charge/current normalization bound"),
        ("SRC4715_24_3508_zg", CSV_3508_WARD, "CSR3508_0_z_g", "current owner drift"),
        ("SRC4715_25_3508_preweight", CSV_3508_WARD, "CSR3508_5_prevariation_weight", "pre-variation current weight"),
        ("SRC4715_26_3513_total", CSV_3513_ELLJ, "EJR3513_0_total", "ell_J source-current residual law"),
        ("SRC4715_27_3513_Rmd", CSV_3513_ELLJ, "EJR3513_1_R_md", "matter descent/source-only multiplier obstruction"),
        ("SRC4715_28_3527_no_go", CSV_3527_STATUS, "STAT3527_1_no_go", "compact U1 plus Noether no-go"),
        ("SRC4715_29_3601_status", CSV_3601_STATUS, "ELLJ_SOURCE_CURRENT_NORMALIZATION_DECOMPOSED", "ell_J status"),
        ("SRC4715_30_sourceWard_SC3", CSV_SOURCE_WARD, "SC3_universal_kappa_coupling", "universal source coupling"),
        ("SRC4715_31_sourceWard_SC6", CSV_SOURCE_WARD, "SC6_closed_calibrated_mass_projector", "measured-GM source normalization"),
        ("SRC4715_32_765_same_current", CSV_765_MKI, "MKI765_3_same_current", "Maxwell kinetic inheritance same current gate"),
        ("SRC4715_33_765_rescale", CSV_765_RESCALE, "RCE765_2_current_rescale", "current rescale counterexample"),
        ("SRC4715_34_988_current", CSV_988_LOCK, "EMLOCK988_2_current_owner", "EM lock current owner"),
        ("SRC4715_35_4702_owner", CSV_4702_OWNER, "OWN4702_4_same_current", "4702 same current owner"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SCC4715_0_same_current_theorem",
            "claim_piece": "same-current owner theorem",
            "statement": "If A_parent=A_Q T_Q+A_perp is parent-defined before readout, T_Q belongs to a fixed nonrescalable charge lattice, matter couples through D[A_Q,T_Q] with fixed representation labels n_A, and J_Q=delta S_matter/delta A_Q is used in both Maxwell and matter equations, then the Maxwell source current and matter source/test charge current are the same variational object.",
            "derivation": "Varying the same matter action with respect to A_Q defines J_Q. Gauge/Noether variation gives the current Ward identity, while metric variation gives matter-EM exchange using that same J_Q. No independent source/test current normalization is available unless the parent action or readout admits an extra current morphism.",
            "result": "R_EM_current=0 and current rescaling is forbidden on the same-owner branch",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_SIGNATURE_UNSIGNED",
            "missing_for_claim": "parent T_Q object, fixed base charge/norm, matter functor coupling, no current morphism, readout order and source/test transfer maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SCC4715_1_compact_U1_limit",
            "claim_piece": "compact charge lattice partial support",
            "statement": "Compact U(1) representation theory can fix relative integer labels n_A, but it does not by itself fix the observed base charge Q_star, the gauge kinetic coefficient, or the matter-current normalization.",
            "derivation": "A simultaneous rescaling of T_Q, A_Q and current/charge units can preserve the observed differential form unless a parent norm, level, index, monopole condition or fixed representation unit forbids it.",
            "result": "relative charges are structured, absolute current normalization remains open",
            "current_status": "PARTIAL_DERIVATION_WITH_RESCALING_COUNTERMODEL",
            "missing_for_claim": "nonrescalable parent norm/level/base-unit owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SCC4715_2_no_current_rescale_subtheorem",
            "claim_piece": "post-variation current rescaling demoted",
            "statement": "If the parent matter action is varied before readout and J_Q is already fixed as delta S_matter/delta A_Q, a later J_A -> c_A J_A is not a parent source term; it can only be a readout/arena transfer coefficient unless a pre-variation current-weight slot exists.",
            "derivation": "The variational derivative is taken before observation or scoring. Postprocessing cannot change the source in the Euler equation. However a pre-action term sum_A w_A S_A survives because it changes the varied action itself.",
            "result": "post-variation rescale excluded conditionally; pre-variation weights remain a real residual",
            "current_status": "EXACT_CONDITIONAL_THEOREM_WITH_PREWEIGHT_COUNTERMODEL",
            "missing_for_claim": "variation-before-readout signature and no source-only pre-variation matter weights",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SCC4715_3_current_residual_law",
            "claim_piece": "finite current-owner residual",
            "statement": "When same-current ownership is unsigned, keep E_J_owner as an absolute no-cancellation residual containing charge-generator projection, lattice/norm, matter descent, current morphism, readout and source/test transfer pieces.",
            "derivation": "Combines 4714 R_EM_current, 1100 T_Q signature gaps, 1814/1815 no-rescale contracts, and 3503/3508/3513 current residual laws.",
            "result": "E_J_owner becomes a sourceable bound row rather than an implicit coupling gap",
            "current_status": "FINITE_BOUND_LAW_DERIVED_VALUES_MISSING",
            "missing_for_claim": "theorem-zero certificate or numeric/source-backed rows for all residual components",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SCC4715_4_verdict",
            "claim_piece": "same-current status",
            "statement": "The current corpus has a clean same-current theorem route, but it has not parent-signed the charge lattice/norm/current owner strongly enough to promote local-GR, R10, WEP, clock, PPN or orbital claims.",
            "derivation": "The exact theorem is conditional; every current public-source path still reports current owner, norm, no-extra-F2, readout or source/test transfer as unsigned.",
            "result": DECISION,
            "current_status": "DERIVATION_ADVANCED_NONCLAIM",
            "missing_for_claim": "no-current-rescale/no-morphism proof or first source-backed current mismatch coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_0_total",
            "quantity": "E_J_owner",
            "definition": "absolute same-current mismatch entering R_EM_current and arena source/test maps",
            "formula": "E_J_owner <= E_TQ_proj + E_Qstar_norm + E_matter_descent + E_current_morphism + E_preweight + E_readout_current + E_source_test",
            "zero_condition": "SCC4715_0 through SCC4715_2 parent-signed on one branch",
            "status": "TOTAL_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_1_TQ_projection",
            "quantity": "E_TQ_proj",
            "definition": "failure of A_Q/T_Q to be a parent connection projection before readout",
            "formula": "E_TQ_proj >= ||A_Q - proj_TQ(A_parent)|| in declared operator norm",
            "zero_condition": "T_Q parent object and A_parent projection signed",
            "status": "MISSING_PARENT_TQ_OBJECT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_2_norm",
            "quantity": "E_Qstar_norm",
            "definition": "base charge/generator norm/level remains rescalable",
            "formula": "E_Qstar_norm captures T_Q -> s T_Q, A_Q -> A_Q/s, J_Q -> s J_Q ambiguity",
            "zero_condition": "fixed nonrescalable norm/level/index/monopole/base-unit owner",
            "status": "MISSING_PARENT_NORM_OR_LEVEL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_3_matter_descent",
            "quantity": "E_matter_descent",
            "definition": "matter action current does not descend through fixed T_Q representation labels",
            "formula": "E_matter_descent >= ||delta S_matter/delta A_Q - J_Q^Noether(T_Q,n_A)||",
            "zero_condition": "matter functor uses D[A_Q,T_Q] with fixed n_A and no hidden/source-only argument",
            "status": "MATTER_FUNCTOR_CURRENT_DESCENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_4_current_morphism",
            "quantity": "E_current_morphism",
            "definition": "allowed parent morphism J_A -> c_A J_A or q_A(X) current weight",
            "formula": "E_current_morphism >= sup_A |c_A-1| + |D_X ln q_A|",
            "zero_condition": "no current coefficient target in parent object language",
            "status": "NEXT_TARGET_NO_MORPHISM_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_5_preweight",
            "quantity": "E_preweight",
            "definition": "pre-variation source/species/action weights already inside S_matter",
            "formula": "E_preweight >= sup_A |w_A-w_common| plus disconnected block/source-label terms",
            "zero_condition": "connected matter-action category has only common action-density scale and no source-label scalar",
            "status": "PRE_VARIATION_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CJ4715_6_readout_source_test",
            "quantity": "E_readout_current + E_source_test",
            "definition": "readout, worldtube, source/test material or calibration maps reweight the already varied current",
            "formula": "E_readout_current+E_source_test <= J_readout_current + J_worldtube_current + J_material_current + J_calibration_current",
            "zero_condition": "variation-before-readout plus source/test maps factor through the same J_Q",
            "status": "ARENA_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    arenas = [
        ("AR4715_0_R10", "R10 short-range force", "B_R10,current <= |K_R10_J(lambda)| * E_J_owner + E_R10_material_current", "K_R10_J(lambda), source/test composition current map, material profile"),
        ("AR4715_1_WEP", "WEP/source composition", "eta_current_AB <= |K_WEP_J| * (E_J_owner + E_source_test_AB + E_preweight_AB)", "source/test material current labels and no-preweight theorem"),
        ("AR4715_2_PPN", "PPN source/current conservation", "delta_PPN_current <= |K_PPN_J| * (E_J_owner + ||R_total_EM|| + boundary current flux)", "weak-field current projection and boundary/worldtube maps"),
        ("AR4715_3_clock", "clock/spectroscopy alpha-current transfer", "B_clock,current <= |K_clock_J| * (E_J_owner + E_readout_current)", "clock current/readout factorization and standards"),
        ("AR4715_4_orbital", "orbital GM/source response", "delta_GM_current <= |K_orb_J| * (E_J_owner + E_worldtube_current + E_calibration_current)", "source worldtube and measured-GM current projector"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "arena": arena,
            "bound_formula": formula,
            "needed_inputs": needed,
            "status": "TRANSFER_BOUND_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, formula, needed in arenas
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE4715_0_TQ_parent", "T_Q parent object and A_Q projection", "T_Q and A_parent=A_QT_Q+A_perp exist before readout", "PARTIAL_TEMPLATE_ONLY"),
        ("GATE4715_1_norm", "fixed charge norm/base unit", "T_Q norm/level/index/Q_star is nonrescalable", "MISSING_PARENT_NORM_OR_LEVEL"),
        ("GATE4715_2_matter_current", "Noether current owner", "J_Q=delta S_matter/delta A_Q with fixed representation labels", "UNSIGNED"),
        ("GATE4715_3_no_morphism", "no current rescaling morphism", "no c_A, q_A(X), kappa_A or source-only current target exists", "NEXT_TARGET"),
        ("GATE4715_4_source_test", "source/test arena transfer", "R10/WEP/PPN/clock/orbital maps use the same J_Q", "MAPS_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "required_condition": required,
            "current_status": status,
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, required, status in gates
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4715_0_no_compactU1_overclaim",
            "rule": "Do not claim compact U(1) fixes alpha or source/test current normalization; it gives relative labels unless base norm/level and current owner are signed.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4715_1_no_Ward_shortcut",
            "rule": "Do not use a Ward identity alone to prove source/test universality; projection, readout, pre-variation weights and worldtube maps can reweight the current.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4715_2_no_postreadout_source",
            "rule": "Post-variation readout cannot change the parent current, but if a current weight is already in S_matter before variation it must be theorem-zero or bounded.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4715_3_no_arena_transfer_without_maps",
            "rule": "Do not transfer same-current closure to R10, WEP, PPN, clock or orbital claims without the arena source/test current maps.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4715_0_main",
            "decision": DECISION,
            "meaning": "The same-current route is a precise theorem target, but current MTS still keeps current rescale/no-morphism and arena source/test transfer as active rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4715_1_next",
            "decision": "ATTACK_CURRENT_RESCALE_NO_MORPHISM_OR_FIRST_COEFFICIENT_NEXT",
            "meaning": "The immediate fork is whether parent object language forbids c_A/q_A current morphisms; if not, fill first source/test current coefficient rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4715_0",
            "status": "PRIVATE_NONCLAIM",
            "summary": "Same-current theorem derived conditionally; compact U1 partial support retained; current rescale and source/test bounds remain active.",
            "same_current_claim": False,
            "local_gr_claim": False,
            "r10_wep_ppn_orbital_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4715_0",
            "target": NEXT_TARGET,
            "reason": "The same-current theorem now reduces the blocker to the existence or absence of current-rescaling morphisms and source/test arena coefficient rows.",
            "derive_first": "prove no current coefficient target/morphism exists after parent variation, including no pre-variation source weights",
            "fallback": "fill first source/test current mismatch coefficient row for R10/WEP/PPN/clock/orbital transfer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_body(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], residuals: list[dict[str, Any]], arenas: list[dict[str, Any]], gates: list[dict[str, Any]], firewalls: list[dict[str, Any]]) -> str:
    return f"""# 4715 - Same-Current Charge-Lattice Owner or Source/Test Bound

Generated: {timestamp}

Scope: local/private framework work only. No GitHub action.

## Result

This checkpoint sharpens the current-coupling lock.

The exact route is:

```text
A_parent = A_Q T_Q + A_perp,
T_Q fixed by parent charge lattice/norm,
S_matter uses D[A_Q,T_Q] with fixed representation labels n_A,
J_Q := delta S_matter / delta A_Q,
same J_Q enters Maxwell and matter/source/test maps.
```

Then the current residual from 4714 closes:

```text
R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda = 0.
```

## Critical Limit

Compact `U(1)` gives useful relative/integer charge structure, but does **not** by itself fix the observed base charge, the fibre norm of `T_Q`, or the source/test current normalization. That rescaling gap remains real.

## Finite Residual

```text
E_J_owner <= E_TQ_proj + E_Qstar_norm + E_matter_descent
           + E_current_morphism + E_preweight
           + E_readout_current + E_source_test.
```

## Theorem Rows

{table(theorem)}

## Current Residual Rows

{table(residuals)}

## Arena Source/Test Rows

{table(arenas)}

## Promotion Gates

{table(gates)}

## Firewalls

{table(firewalls)}

## Source Register

{table(sources)}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`.
"""


def formal_body(timestamp: str) -> str:
    return f"""# PPC4161 4715 - Same-Current Charge-Lattice Owner or Source/Test Bound

Generated: {timestamp}

Private nonclaim checkpoint.

Exact route:

```text
A_parent = A_Q T_Q + A_perp,
J_Q := delta S_matter / delta A_Q,
same J_Q enters Maxwell, matter exchange, and source/test maps.
```

If parent-signed:

```text
R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda = 0.
```

Retained no-cancellation residual:

```text
E_J_owner <= E_TQ_proj + E_Qstar_norm + E_matter_descent
           + E_current_morphism + E_preweight
           + E_readout_current + E_source_test.
```

No local-GR/R10/WEP/PPN/orbital claim is allowed until current-rescale morphisms and arena source/test maps close.

Validation: `{VALIDATION_CSV}`.
Next: `{NEXT_TARGET}`.
"""


def write_resume(timestamp: str) -> None:
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: {timestamp}

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4715-Y5-R2FR-same-current-charge-lattice-owner-or-source-test-bound.md`

## What Changed

The same-current branch now has an exact conditional theorem:

```text
J_Q := delta S_matter / delta A_Q
```

must be the same current used by Maxwell, matter exchange, and source/test maps.

Compact `U(1)` is only partial support: it fixes relative labels, not the observed base current normalization by itself.

Retained residual:

```text
E_J_owner <= E_TQ_proj + E_Qstar_norm + E_matter_descent
           + E_current_morphism + E_preweight
           + E_readout_current + E_source_test.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not claim compact `U(1)` alone fixes alpha or source/test current normalization.
- Do not use Ward identity as a shortcut past projection/readout/source-test maps.
- Do not transfer same-current closure into R10/WEP/PPN/orbital claims without arena maps.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], residuals: list[dict[str, Any]], arenas: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4715_sources_exist", all(row["path_exists"] for row in sources), "all cited local source paths exist"),
        ("VAL4715_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4715_same_current_theorem", any(row["theorem_id"] == "SCC4715_0_same_current_theorem" for row in theorem), "same-current theorem present"),
        ("VAL4715_compact_limit", any(row["theorem_id"] == "SCC4715_1_compact_U1_limit" for row in theorem), "compact U1 limitation retained"),
        ("VAL4715_residual_total", any(row["row_id"] == "CJ4715_0_total" for row in residuals), "total current-owner residual present"),
        ("VAL4715_arena_rows", len(arenas) >= 5, "arena transfer rows present"),
        ("VAL4715_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in theorem + residuals + arenas), "no row allows a claim"),
        ("VAL4715_gates_not_passing", not all(bool(row["passes"]) for row in gates), "promotion gates not all passing"),
        ("VAL4715_doc_written", DOC_PATH.exists(), "checkpoint document written"),
        ("VAL4715_formal_written", FORMAL_PATH.exists(), "formal packet document written"),
        ("VAL4715_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4715_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "4715 artifacts validate as private nonclaim checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(timestamp)
    theorem = theorem_rows(timestamp)
    residuals = residual_rows(timestamp)
    arenas = arena_rows(timestamp)
    gates = promotion_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(ARENA_CSV, arenas)
    write_csv(PROMOTION_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    DOC_PATH.write_text(doc_body(timestamp, sources, theorem, residuals, arenas, gates, firewalls), encoding="utf-8")
    FORMAL_PATH.write_text(formal_body(timestamp), encoding="utf-8")
    append_claim_once(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: same-current ownership is now an exact conditional theorem: `J_Q := delta S_matter / delta A_Q` must be the same current used by Maxwell, matter exchange and source/test maps.
- Critical limit: compact `U(1)` gives relative charge labels but does not fix the observed base charge/current normalization without a parent norm/level/base-unit owner.
- Retained residual: `E_J_owner <= E_TQ_proj + E_Qstar_norm + E_matter_descent + E_current_morphism + E_preweight + E_readout_current + E_source_test`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts same-current/charge-lattice ownership into an exact theorem target plus source/test current mismatch bounds.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_resume(timestamp)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    validation = validation_rows(timestamp, sources, theorem, residuals, arenas, gates)
    write_csv(VALIDATION_CSV, validation)


if __name__ == "__main__":
    main()
