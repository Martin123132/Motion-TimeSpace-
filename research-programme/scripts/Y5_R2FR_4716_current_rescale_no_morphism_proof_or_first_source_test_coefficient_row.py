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

CHECKPOINT = "4716"
CLAIM_ID = "L-558"
MARKER = "PPC4161_CURRENT_RESCALE_NO_MORPHISM_OR_FIRST_SOURCE_TEST_COEFFICIENT_4716"
PACKET_MARKER = "PPC4161_PACKET_CURRENT_RESCALE_NO_MORPHISM_OR_FIRST_SOURCE_TEST_COEFFICIENT_4716"
DECISION = "POST_VARIATION_CURRENT_RESCALE_CONDITIONALLY_DEMOTED_PREACTION_SOURCE_PREFACTOR_SURVIVES_NONCLAIM"
NEXT_TARGET = "4717-Y5-R2FR-no-preaction-source-prefactor-signature-or-deltaw-kernel-first-row.md"

DOC_PATH = POST / "4716-Y5-R2FR-current-rescale-no-morphism-proof-or-first-source-test-coefficient-row.md"
FORMAL_PATH = FORMAL / "732-PPC4161-current-rescale-no-morphism-proof-or-first-source-test-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4715_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4715_NEXT_TARGET.csv"
CSV_4715_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4715_SAME_CURRENT_CHARGE_LATTICE_THEOREM.csv"
CSV_4715_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4715_CURRENT_OWNER_RESIDUAL_ROWS.csv"
CSV_4715_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4715_SOURCE_TEST_ARENA_BOUND_ROWS.csv"
CSV_4715_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4715_VALIDATION.csv"
CSV_1815_RESCALE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"
CSV_1814_VISIBLE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv"
CSV_3508_WARD = SOURCE_DIR / "P8_EM_current_source_Ward_alpha_source_residual.csv"
CSV_3509_NOSOURCE = SOURCE_DIR / "P8_EM_no_source_only_matter_functor_residual.csv"
CSV_3510_COMMON = SOURCE_DIR / "P8_EM_common_action_density_line_universal_source_scale.csv"
CSV_3519_NORMAL = SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"
CSV_3520_QAP = SOURCE_DIR / "P8_EM_quotient_action_derives_q_normal_form_status.csv"
CSV_1889_WARD = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv"
CSV_1890_NOPREF = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1890_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv"
CSV_1891_MNO = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1891_MATTER_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
CSV_1891_AUDIT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1891_NONGRAV_STANDARD_OWNER_AUDIT.csv"
CSV_1892_SIG = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1892_ORDINARY_MATTER_ACTION_SIGNATURE_ATTEMPT.csv"
CSV_1892_MATRIX = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv"
CSV_1893_LFA = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv"
CSV_1893_SFL = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv"
CSV_1893_GATE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1893_CLAIM_GATE.csv"
CSV_765_RESCALE = SOURCE_DIR / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
CSV_1100_SIG = SOURCE_DIR / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4716_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_CURRENT_RESCALE_NO_MORPHISM_THEOREM.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_FIRST_SOURCE_TEST_COEFFICIENT_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_ARENA_PROJECTION_KERNEL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4716_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4716_VALIDATION.csv"


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
        "claim": "4716 conditionally demotes post-variation current rescaling and isolates pre-action source prefactors as the surviving no-morphism/current-coupling blocker.",
        "current_evidence": "Generated source register, no-morphism theorem rows, first source/test coefficient rows, arena projection kernels, gates, firewalls, decision, status, next target and validation.",
        "status": "post_variation_rescale_demoted_preaction_prefactor_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using variation-before-readout to erase source weights that were already present before variation.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Current rescale no-morphism proof or first source-test coefficient row",
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
        ("SRC4716_00_4715_next", CSV_4715_NEXT, "NT4715_0", "4715 handoff to current-rescale no-morphism proof"),
        ("SRC4716_01_4715_no_rescale", CSV_4715_THEOREM, "SCC4715_2_no_current_rescale_subtheorem", "post-variation rescale demotion"),
        ("SRC4716_02_4715_residual", CSV_4715_RESIDUAL, "CJ4715_4_current_morphism", "current morphism residual row"),
        ("SRC4716_03_4715_preweight", CSV_4715_RESIDUAL, "CJ4715_5_preweight", "prevariation weight survivor"),
        ("SRC4716_04_4715_arena", CSV_4715_ARENA, "AR4715_0_R10", "arena source/test rows"),
        ("SRC4716_05_4715_validation", CSV_4715_VALIDATION, "VAL4715_OVERALL", "4715 validation"),
        ("SRC4716_06_1815_target", CSV_1815_RESCALE, "NCR1815_0_target", "no-current-rescale theorem"),
        ("SRC4716_07_1815_post", CSV_1815_RESCALE, "NCR1815_1_post_variation_cA", "post-variation c_A demotion"),
        ("SRC4716_08_1815_pre", CSV_1815_RESCALE, "NCR1815_2_pre_variation_weight", "pre-variation weight survives"),
        ("SRC4716_09_1815_connected", CSV_1815_RESCALE, "NCR1815_3_connected_naturality", "connected matter category route"),
        ("SRC4716_10_1814_rescale", CSV_1814_VISIBLE, "VCC1814_3_rescaling_exclusion", "rescaling exclusion condition"),
        ("SRC4716_11_3508_post", CSV_3508_WARD, "CSR3508_4_postvariation_rescaling", "post-variation rescale row"),
        ("SRC4716_12_3508_pre", CSV_3508_WARD, "CSR3508_5_prevariation_weight", "pre-variation countermodel"),
        ("SRC4716_13_3509_deltaw", CSV_3509_NOSOURCE, "NSSR3509_0_delta_w_species", "delta_w_species route"),
        ("SRC4716_14_3509_kappa", CSV_3509_NOSOURCE, "NSSR3509_2_kappa_A_source", "kappa_A source route"),
        ("SRC4716_15_3509_hidden", CSV_3509_NOSOURCE, "NSSR3509_3_hidden_marker_source", "hidden marker source route"),
        ("SRC4716_16_3510_common", CSV_3510_COMMON, "UCSR3510_0_zeta_w_common", "common scale route"),
        ("SRC4716_17_3510_delta", CSV_3510_COMMON, "UCSR3510_1_delta_w_species", "species weight route"),
        ("SRC4716_18_3519_matter", CSV_3519_NORMAL, "NF3519_2_matter_functor", "typed matter functor normal form"),
        ("SRC4716_19_3519_scale", CSV_3519_NORMAL, "NF3519_4_universal_scale", "universal scale rule"),
        ("SRC4716_20_3520_prefactor", CSV_3520_QAP, "STAT3520_3_prefactor", "QAP prefactor limitation"),
        ("SRC4716_21_1889_target", CSV_1889_WARD, "SWO1889_0_target", "source-current Ward owner target"),
        ("SRC4716_22_1889_wardcounter", CSV_1889_WARD, "SWO1889_2_Ward_homogeneity", "Ward not species blind"),
        ("SRC4716_23_1889_weight", CSV_1889_WARD, "SWO1889_5_pre_action_weight_leak", "pre-action weight leak"),
        ("SRC4716_24_1890_target", CSV_1890_NOPREF, "NSP1890_0_target", "no source prefactor target"),
        ("SRC4716_25_1890_counter", CSV_1890_NOPREF, "NSP1890_6_countermodel", "prefactor countermodel"),
        ("SRC4716_26_1890_verdict", CSV_1890_NOPREF, "NSP1890_7_verdict", "no-prefactor not derived"),
        ("SRC4716_27_1891_double", CSV_1891_MNO, "MNO1891_1_conditional_double_counting", "double-counting lemma"),
        ("SRC4716_28_1891_counter", CSV_1891_MNO, "MNO1891_3_countermodel", "matter-normalization countermodel"),
        ("SRC4716_29_1891_audit", CSV_1891_AUDIT, "NSO1891_3_source_weight_exclusion", "nongrav standard source-weight audit"),
        ("SRC4716_30_1892_target", CSV_1892_SIG, "OMAS1892_0_target_signature", "ordinary matter action signature"),
        ("SRC4716_31_1892_clause", CSV_1892_MATRIX, "OMC1892_4_source_functor_label_forgetting", "source functor label forgetting clause"),
        ("SRC4716_32_1893_no_pref", CSV_1893_LFA, "LFA1893_2_no_prefactors", "no pre-action prefactor missing clause"),
        ("SRC4716_33_1893_ward", CSV_1893_SFL, "SFL1893_2_ward_countermodel", "Ward not label forgetting"),
        ("SRC4716_34_1893_pref", CSV_1893_SFL, "SFL1893_4_prefactor_obstruction", "prefactor obstruction"),
        ("SRC4716_35_1893_gate", CSV_1893_GATE, "CG1893_1_no_prefactors", "no-prefactor gate fail"),
        ("SRC4716_36_765_current", CSV_765_RESCALE, "RCE765_2_current_rescale", "current rescale counterexample"),
        ("SRC4716_37_1100_current", CSV_1100_SIG, "TQS1100_4_same_current_owner", "same current signature"),
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
            "theorem_id": "NCM4716_0_postvariation_rescale",
            "claim_piece": "post-variation current rescale demotion",
            "statement": "If the parent action is varied before readout and J_Q=delta S_matter/delta A_Q is fixed as the Noether/Ward current, then a later map J_A -> c_A J_A is not a parent source term and cannot alter the Euler/Maxwell source.",
            "derivation": "The source in the field equation is the variational derivative. Any coefficient introduced after solving belongs to readout/arena transfer unless the parent object language contains a source-current coefficient target.",
            "result": "post-variation c_A is demoted to readout/arena coefficient on this branch",
            "current_status": "EXACT_CONDITIONAL_THEOREM_READOUT_ORDER_UNSIGNED",
            "missing_for_claim": "variation-before-readout parent signature and arena transfer maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NCM4716_1_preaction_countermodel",
            "claim_piece": "pre-action source prefactor survives",
            "statement": "If S_matter already contains sum_A w_A S_A or S_int contains q_A(X) A_Q J_A before variation, then the varied Hilbert/Noether source inherits w_A or q_A; current ownership alone does not remove it.",
            "derivation": "Classical equations for matter fields may be insensitive to constant w_A, but metric/gauge variation, path-integral weight and source normalization are not. Ward conservation can hold for a weighted conserved sum.",
            "result": "pre-action source/current prefactors are the live blocker",
            "current_status": "COUNTERMODEL_RETAINED",
            "missing_for_claim": "parent no-source-prefactor/no-current-coefficient object-language theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NCM4716_2_no_morphism_exact_route",
            "claim_piece": "no current morphism theorem target",
            "statement": "If the parent matter functor accepts only fields, q-basic visible geometry/gauge data, fixed representation constants and one common action-density line, with no target object Coeff(J_Q), Coeff(S_A), source labels or hidden/material marker Hom into source coefficients, then c_A, q_A(X), kappa_A and relative w_A are ill-typed.",
            "derivation": "A relative current/source coefficient needs a parent-domain argument and a coefficient target. Removing both removes the morphism rather than tuning it. A common scalar line is not a composition/source-test current vector and is routed to calibration/Gdot rows.",
            "result": "E_current_morphism=E_preweight=0 conditionally, while common scale remains separate",
            "current_status": "EXACT_CONDITIONAL_OBJECT_LANGUAGE_THEOREM_UNSIGNED",
            "missing_for_claim": "parent-signed ordinary matter action signature, source-label forgetting, common action-density owner and radiative/readout stability",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NCM4716_3_finite_source_test_coefficients",
            "claim_piece": "first source/test coefficient rows",
            "statement": "If no-morphism is unsigned, define finite no-cancellation coefficients delta_w_species, kappa_A_source, c_A_current, q_A_current and hidden_marker_source, then project them into R10, WEP, PPN, clock and orbital arenas.",
            "derivation": "This is the finite branch of 4715 E_J_owner, using the 3508/3509/3510 and 1889-1893 source-current rows.",
            "result": "source/test coupling is now a scored coefficient vector, not an implicit closure",
            "current_status": "FINITE_COEFFICIENT_ROWS_STAGED_VALUES_MISSING",
            "missing_for_claim": "numeric/source-backed coefficient values or theorem-zero certificates plus arena K/tau/source maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NCM4716_4_verdict",
            "claim_piece": "4716 verdict",
            "statement": "4716 proves the useful part: post-variation current rescaling cannot change the parent current. It does not erase pre-action source/current prefactors; those are the next theorem target or first coefficient rows.",
            "derivation": "Combines 4715, 1815, 3508, 3519, 1889-1893 and 765. The same pattern repeats across all evidence: Ward/readout order is helpful but no-prefactor grammar is the actual missing theorem.",
            "result": DECISION,
            "current_status": "DERIVATION_ADVANCED_NONCLAIM",
            "missing_for_claim": "no pre-action source-prefactor signature or sourced delta_w/kappa/c_A/q_A rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_0_delta_w_species",
            "coefficient": "delta_w_species",
            "definition": "relative pre-action source/species prefactor D_X ln w_A - D_X ln w_B",
            "zero_condition": "connected ordinary matter category plus one parent action-density line and no source-only species prefactors",
            "bound_formula": "|delta_w_species| <= sourced finite coefficient; no cancellation against G_ref or common scale credited",
            "feeds": "WEP; R10; PPN source composition; Newton/source normalization",
            "status": "FIRST_COEFFICIENT_ROW_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_1_kappa_A_source",
            "coefficient": "kappa_A_source",
            "definition": "source-only active coupling F((T_A,A))->kappa_A T_A before source selection",
            "zero_condition": "source functor sees only T_total and has no A/source-label argument",
            "bound_formula": "|Delta kappa_AB| <= sourced source-label coefficient",
            "feeds": "WEP; R10; source composition; clock redshift through source calibration",
            "status": "FIRST_COEFFICIENT_ROW_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_2_cA_current",
            "coefficient": "c_A_current",
            "definition": "post-variation or parent-domain current multiplier J_A -> c_A J_A",
            "zero_condition": "post-variation only plus no parent current coefficient target",
            "bound_formula": "sup_A |c_A-1| if a parent/readout current coefficient target survives",
            "feeds": "R10 source/test charge; WEP current response; alpha/current readout",
            "status": "POSTVAR_ZERO_CONDITIONAL_PARENT_TARGET_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_3_qA_current",
            "coefficient": "q_A(X)",
            "definition": "hidden/material/source-dependent matter-current charge normalization in S_int",
            "zero_condition": "fixed representation labels n_A and no hidden/source-only argument in matter functor",
            "bound_formula": "sup_A |D_X ln q_A| with source path and units",
            "feeds": "EM Lorentz force; WEP/R10 source-test charge; clock/spectroscopy alpha-current products",
            "status": "VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_4_hidden_marker_source",
            "coefficient": "hidden_marker_source",
            "definition": "hidden/domain/material marker feeding active source coefficient",
            "zero_condition": "Hom_parent(HiddenMarker,C_source) is absent or common constant only",
            "bound_formula": "||D_marker C_source|| <= sourced hidden-marker coefficient",
            "feeds": "preferred-frame; PPN; source composition; local transition source",
            "status": "VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "COEF4716_5_w_common",
            "coefficient": "w_common",
            "definition": "common action-density/source-scale multiplier shared by all ordinary matter",
            "zero_condition": "one fixed parent action/phase/measure line or calibrated constant with no drift/range/frame/source dependence",
            "bound_formula": "D_X ln w_common maps to Gdot/G, Newton/source calibration, clocks and common action-scale rows, not WEP composition directly",
            "feeds": "Gdot; Newton G/GM; clock/action normalization; source calibration",
            "status": "COMMON_MODE_SEPARATE_FROM_RELATIVE_SOURCE_TEST_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    arenas = [
        ("KERN4716_0_R10", "R10 short-range", "B_R10,current <= |K_R10_w| |delta_w_species| + |K_R10_kappa||Delta kappa_AB| + |K_R10_q| sup|D_X ln q_A|", "K_R10_w, K_R10_kappa, K_R10_q, source/test material current map, lambda profile"),
        ("KERN4716_1_WEP", "WEP/source composition", "eta_AB_current <= |K_WEP_w| |delta_w_AB| + |K_WEP_kappa||Delta kappa_AB| + |K_WEP_hidden||hidden_marker_source|", "material-pair current labels and source composition tensors"),
        ("KERN4716_2_PPN", "PPN/source conservation", "delta_PPN_current <= |K_PPN_w| |delta_w_species| + |K_PPN_NH| |nonHilbert_source_bypass| + boundary/projector tails", "weak-field source projection and non-Hilbert/boundary maps"),
        ("KERN4716_3_clock", "clock/source calibration", "B_clock,current <= |K_clock_q| sup|D_X ln q_A| + |K_clock_readout| |c_A_readout-1| + common-scale clock row", "clock current/readout standards and alpha-current map"),
        ("KERN4716_4_orbital", "orbital GM/source response", "delta_GM_current <= |K_orb_w| |delta_w_species| + |K_orb_common| |D_X ln w_common| + worldtube/calibration tails", "source worldtube, measured-GM projector, common-scale separation"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "arena": arena,
            "projection_kernel": formula,
            "needed_inputs": needed,
            "status": "KERNEL_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, formula, needed in arenas
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE4716_0_variation_order", "variation before readout", "J_Q and T_H are varied before any arena/source readout coefficient", "UNSIGNED_BUT_CONDITIONAL_THEOREM_READY"),
        ("GATE4716_1_no_current_target", "no current coefficient target", "Coeff(J_Q) or Hom(marker,C_source) is absent or common constant only", "NOT_PARENT_SIGNED"),
        ("GATE4716_2_no_preaction_prefactor", "no pre-action source prefactor", "Allowed[S_matter] excludes w_A S_A and q_A(X) A_Q J_A source-only slots", "NEXT_TARGET"),
        ("GATE4716_3_connected_matter", "connected ordinary matter category", "ordinary matter species share one action-density line; relative automorphisms collapse", "UNSIGNED"),
        ("GATE4716_4_arena_coefficients", "source/test coefficient rows", "all surviving coefficients have source-backed values and arena kernels", "VALUES_MISSING"),
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
            "firewall_id": "FW4716_0_no_ward_species_blindness",
            "rule": "Do not infer species/source-test universality from Ward conservation; weighted conserved sums can still satisfy Ward identities.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4716_1_no_postvar_to_prevar",
            "rule": "Do not use the post-variation readout theorem to erase coefficients already present in S_matter before variation.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4716_2_no_G_absorption",
            "rule": "Do not absorb relative delta_w_species or kappa_A_source into measured G/GM; only a common mode may be calibration-like after drift/range/frame silence is signed.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4716_3_no_arena_claim",
            "rule": "No R10, WEP, PPN, clock or orbital claim until coefficient values or theorem-zero certificates and arena kernels exist.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4716_0_main",
            "decision": DECISION,
            "meaning": "The current-rescale problem is partly solved: post-variation rescaling is not a parent source. The live coupling blocker is the pre-action source/current prefactor grammar.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4716_1_next",
            "decision": "ATTACK_NO_PREACTION_SOURCE_PREFACTOR_SIGNATURE_NEXT",
            "meaning": "Next step is to prove the parent ordinary-matter/source functor has no w_A/kappa_A/q_A source-only slots, or fill delta_w projection kernels.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4716_0",
            "status": "PRIVATE_NONCLAIM",
            "summary": "Post-variation current rescale conditionally demoted; pre-action source prefactor and coefficient-vector fallback retained.",
            "postvariation_rescale_zero_claim": False,
            "preaction_prefactor_zero_claim": False,
            "local_gr_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4716_0",
            "target": NEXT_TARGET,
            "reason": "The only clean remaining route is a parent ordinary-matter/source-functor signature that forbids pre-action source prefactors; otherwise delta_w/kappa/current coefficient kernels must be filled.",
            "derive_first": "prove Allowed[S_matter] excludes source-only w_A, kappa_A, q_A(X), hidden-marker source coefficients and species labels before variation",
            "fallback": "fill first delta_w_species/kappa_A/q_A coefficient rows and project them into WEP/R10/PPN/clock/orbital kernels",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_body(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], coefficients: list[dict[str, Any]], arenas: list[dict[str, Any]], gates: list[dict[str, Any]], firewalls: list[dict[str, Any]]) -> str:
    return f"""# 4716 - Current-Rescale No-Morphism Proof or First Source/Test Coefficient Row

Generated: {timestamp}

Scope: local/private framework work only. No GitHub action.

## Result

This checkpoint separates two things that must not be mixed:

```text
post-variation c_A readout/current rescale
```

versus

```text
pre-action source/current prefactor w_A, kappa_A, q_A(X).
```

The useful theorem:

```text
J_Q := delta S_matter / delta A_Q
```

is fixed before readout. A later `J_A -> c_A J_A` cannot change the parent Euler/Maxwell source.

The surviving danger:

```text
S_matter = sum_A w_A S_A,
S_int = sum_A q_A(X) A_Q J_A,
F_src((T_A,A)) = kappa_A T_A.
```

If these are legal before variation, the source/test current is genuinely reweighted.

## Exact No-Morphism Route

```text
Allowed[S_matter] = S_matter[psi_A, Qvis, theta_A, A_obs]
```

with no `Coeff(J_Q)`, no source labels, no hidden/material Hom into source coefficients, and one common action-density line.

Then:

```text
E_current_morphism = E_preweight = 0
```

up to the separate common-scale/Gdot/calibration branch.

## Finite Coefficient Vector

```text
E_source_test_vector =
|delta_w_species| + |Delta kappa_AB| + sup|D_X ln q_A|
+ |hidden_marker_source| + readout/worldtube tails.
```

## Theorem Rows

{table(theorem)}

## First Source/Test Coefficient Rows

{table(coefficients)}

## Arena Projection Kernels

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
    return f"""# PPC4161 4716 - Current-Rescale No-Morphism / Source-Test Coefficients

Generated: {timestamp}

Private nonclaim checkpoint.

Key result:

```text
J_Q := delta S_matter / delta A_Q
```

is fixed before readout, so post-variation `J_A -> c_A J_A` cannot alter the parent source.

But pre-action prefactors survive unless forbidden:

```text
S_matter = sum_A w_A S_A,
S_int = sum_A q_A(X) A_Q J_A,
F_src((T_A,A)) = kappa_A T_A.
```

Finite vector:

```text
E_source_test_vector =
|delta_w_species| + |Delta kappa_AB| + sup|D_X ln q_A|
+ |hidden_marker_source| + readout/worldtube tails.
```

No local-GR/R10/WEP/PPN/orbital claim is allowed until the no-prefactor theorem or coefficient values close.

Validation: `{VALIDATION_CSV}`.
Next: `{NEXT_TARGET}`.
"""


def write_resume(timestamp: str) -> None:
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: {timestamp}

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4716-Y5-R2FR-current-rescale-no-morphism-proof-or-first-source-test-coefficient-row.md`

## What Changed

Post-variation current rescaling is conditionally demoted:

```text
J_Q := delta S_matter / delta A_Q
```

is fixed before readout.

But pre-action prefactors remain the live source-coupling gap:

```text
S_matter = sum_A w_A S_A,
S_int = sum_A q_A(X) A_Q J_A,
F_src((T_A,A)) = kappa_A T_A.
```

Finite vector:

```text
E_source_test_vector =
|delta_w_species| + |Delta kappa_AB| + sup|D_X ln q_A|
+ |hidden_marker_source| + readout/worldtube tails.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not use Ward conservation to erase species/source weights.
- Do not confuse post-variation readout rescale with pre-action source prefactors.
- Do not absorb relative source/test coefficients into measured `G` or `GM`.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], coefficients: list[dict[str, Any]], arenas: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4716_sources_exist", all(row["path_exists"] for row in sources), "all cited local source paths exist"),
        ("VAL4716_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4716_postvar_theorem", any(row["theorem_id"] == "NCM4716_0_postvariation_rescale" for row in theorem), "post-variation rescale theorem present"),
        ("VAL4716_preaction_countermodel", any(row["theorem_id"] == "NCM4716_1_preaction_countermodel" for row in theorem), "pre-action countermodel retained"),
        ("VAL4716_coeff_delta_w", any(row["row_id"] == "COEF4716_0_delta_w_species" for row in coefficients), "delta_w coefficient row present"),
        ("VAL4716_arena_kernels", len(arenas) >= 5, "arena projection kernels present"),
        ("VAL4716_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in theorem + coefficients + arenas), "no row allows a claim"),
        ("VAL4716_gates_not_passing", not all(bool(row["passes"]) for row in gates), "promotion gates not all passing"),
        ("VAL4716_doc_written", DOC_PATH.exists(), "checkpoint document written"),
        ("VAL4716_formal_written", FORMAL_PATH.exists(), "formal packet document written"),
        ("VAL4716_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
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
            "validation_id": "VAL4716_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "4716 artifacts validate as private nonclaim checkpoint",
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
    coefficients = coefficient_rows(timestamp)
    arenas = arena_rows(timestamp)
    gates = promotion_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(COEFFICIENT_CSV, coefficients)
    write_csv(ARENA_CSV, arenas)
    write_csv(PROMOTION_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    DOC_PATH.write_text(doc_body(timestamp, sources, theorem, coefficients, arenas, gates, firewalls), encoding="utf-8")
    FORMAL_PATH.write_text(formal_body(timestamp), encoding="utf-8")
    append_claim_once(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: post-variation current rescaling is conditionally demoted because `J_Q := delta S_matter / delta A_Q` is fixed before readout.
- Survivor: pre-action `w_A`, `kappa_A`, `q_A(X)` source/current prefactors remain live unless the parent object language forbids their coefficient targets.
- Finite vector: `E_source_test_vector = |delta_w_species| + |Delta kappa_AB| + sup|D_X ln q_A| + |hidden_marker_source| + readout/worldtube tails`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: separates post-variation readout current rescale from pre-action source/current prefactors and stages the first source/test coefficient vector.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_resume(timestamp)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    validation = validation_rows(timestamp, sources, theorem, coefficients, arenas, gates)
    write_csv(VALIDATION_CSV, validation)


if __name__ == "__main__":
    main()
