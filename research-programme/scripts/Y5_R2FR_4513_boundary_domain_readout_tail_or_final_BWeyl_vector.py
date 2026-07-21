from __future__ import annotations

import csv
import io
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4513"
CLAIM_ID = "L-355"
MARKER = "PPC4161_BOUNDARY_DOMAIN_READOUT_TAIL_OR_FINAL_BWEYL_VECTOR_4513"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_DOMAIN_READOUT_TAIL_OR_FINAL_BWEYL_VECTOR_4513"
DECISION = "BOUNDARY_DOMAIN_READOUT_TAIL_THEOREM_DERIVED_FINAL_BWEYL_VECTOR_STAGED_NONCLAIM"
NEXT_TARGET = "4514-Y5-R2FR-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"

FORMAL_PATH = FORMAL / "529-PPC4161-boundary-domain-readout-tail-or-final-BWeyl-vector.md"
DOC_PATH = POST / "4513-Y5-R2FR-boundary-domain-readout-tail-or-final-BWeyl-vector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4513_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4513_SOURCE_REGISTER.csv"
TAIL_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4513_BOUNDARY_DOMAIN_READOUT_TAIL_THEOREM.csv"
TAIL_CLASSIFIER = SOURCE_DIR / "P8_Y5_R2FR_4513_TAIL_COMPONENT_CLASSIFIER.csv"
TAIL_INPUT_FILL = SOURCE_DIR / "P8_Y5_R2FR_4513_TAIL_INPUT_FILL_ROWS.csv"
TAIL_FINITE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4513_TAIL_FINITE_BOUND_ROWS.csv"
FINAL_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4513_FINAL_BWEYL_VECTOR.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4513_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4513_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4513_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4513_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4513_DECISION.csv"

FORMAL_528 = FORMAL / "528-PPC4161-Khat-trace-match-or-RKtrace-finite-row.md"
POST_4512 = POST / "4512-Y5-R2FR-Khat-trace-match-or-RKtrace-finite-row.md"
COMBINED_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_COMBINED_ZERO_THEOREM.csv"
BDR_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_BOUNDARY_DOMAIN_READOUT_GATE.csv"
BWEYL_NUMERIC_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_BWEYL_NUMERIC_ACQUISITION_ROW.csv"
FILL_4510 = SOURCE_DIR / "P8_Y5_R2FR_4510_BWEYL_INPUT_FILL_ROWS.csv"
WFM_4511 = SOURCE_DIR / "P8_Y5_R2FR_4511_WFM_INPUT_FILL_ROWS.csv"
RK_4512 = SOURCE_DIR / "P8_Y5_R2FR_4512_RKTRACE_INPUT_FILL_ROWS.csv"
BOUNDARY_ALPHA3 = SOURCE_DIR / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
ALPHA3_GATE = SOURCE_DIR / "P8_ALPHA3_THEOREM_ZERO_GATE.csv"
BOUNDARY_MEM_2627 = SOURCE_DIR / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_BOUNDARY_ZERO_GATE.csv"
BOUNDARY_COHOM = SOURCE_DIR / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv"
BOUNDARY_FLUX = SOURCE_DIR / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv"
DOMAIN_NOLEAK = SOURCE_DIR / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
DOMAIN_NOVECTOR = SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv"
DOMAIN_PARENT_GATE = SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv"
DOMAIN_CHAIN = SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv"
FIXED_DOMAIN_2355 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2355_FIXED_DOMAIN_THEOREM_AUDIT.csv"
DOMAIN_BOUND_2356 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv"
DOMAIN_ENV_2356 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2356_SOURCE_DOMAIN_ENVELOPE.csv"
READOUT_EXCL_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_EXCLUSION_CERTIFICATE.csv"
READOUT_POLICY_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_CLOSURE_POLICY.csv"
VBR_1816 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv"
RNE_2353 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2353_READOUT_NO_REENTRY_ZERO_AUDIT.csv"
RNG_2418 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv"
SRNG_2335 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv"
CBP_2419 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_READOUT_BOUND_PACK.csv"
BP_2354 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2354_READOUT_REENTRY_BOUND_PACK.csv"
READOUT_TAIL_2369 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2369_READOUT_TAIL_MATRIX.csv"
READOUT_ZERO_2370 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2370_ALPHA_READOUT_ZERO_AUDIT.csv"
READOUT_BOUND_2370 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2370_FIRST_ALPHA_READOUT_BOUND_ROW.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def falseish(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "none", ""}


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4513_00_formal528", "4512 formal handoff", FORMAL_528, "Khat Trace Match", "previous B_Weyl leg"),
        ("SRC4513_01_post4512", "4512 post handoff", POST_4512, "NT4512_0", "declares tail target"),
        ("SRC4513_02_combined4509", "4509 combined zero theorem", COMBINED_4509, "CZT4509_4_boundary_clause", "tail clause"),
        ("SRC4513_03_bdr4509_boundary", "4509 boundary/domain/readout gate", BDR_4509, "BDR4509_0_boundary", "boundary tail gate"),
        ("SRC4513_04_bdr4509_domain", "4509 boundary/domain/readout gate", BDR_4509, "BDR4509_1_domain", "domain tail gate"),
        ("SRC4513_05_bdr4509_readout", "4509 boundary/domain/readout gate", BDR_4509, "BDR4509_2_readout", "readout tail gate"),
        ("SRC4513_06_numeric_boundary", "4509 numeric acquisition", BWEYL_NUMERIC_4509, "BWN4509_10_Bboundary", "boundary finite row"),
        ("SRC4513_07_numeric_domain", "4509 numeric acquisition", BWEYL_NUMERIC_4509, "BWN4509_11_Bdomain", "domain finite row"),
        ("SRC4513_08_numeric_readout", "4509 numeric acquisition", BWEYL_NUMERIC_4509, "BWN4509_12_Breadout", "readout finite row"),
        ("SRC4513_09_fill4510", "4510 source-root input fill", FILL_4510, "BWF4510_02_Lcg_chain", "Lcg chain filled conditionally"),
        ("SRC4513_10_fill4511", "4511 W_F,m input fill", WFM_4511, "WFF4511_00_WFm", "W_F,m filled conditionally"),
        ("SRC4513_11_fill4512", "4512 R_K trace input fill", RK_4512, "RKF4512_00_RKtrace", "R_K trace filled conditionally"),
        ("SRC4513_12_boundary_alpha3", "boundary no-flux theorem attempt", BOUNDARY_ALPHA3, "T7_conclusion", "boundary no-flux conditional verdict"),
        ("SRC4513_13_alpha3_gate_boundary", "alpha3 theorem zero gate", ALPHA3_GATE, "TG_boundary_zero", "boundary theorem gate"),
        ("SRC4513_14_alpha3_gate_domain", "alpha3 theorem zero gate", ALPHA3_GATE, "TG_domain_zero", "domain theorem gate"),
        ("SRC4513_15_boundary_mem2627", "memory boundary zero gate", BOUNDARY_MEM_2627, "BZ2627_5_current_verdict", "boundary zero not parent-derived"),
        ("SRC4513_16_boundary_cohom", "boundary cohomology/no-hair", BOUNDARY_COHOM, "BCT549_6_certificate_verdict", "boundary cohomology verdict"),
        ("SRC4513_17_boundary_flux", "boundary flux fallback", BOUNDARY_FLUX, "FB549_0_boundary_flux_bound", "boundary finite input row"),
        ("SRC4513_18_domain_noleak", "domain no-leak theorem", DOMAIN_NOLEAK, "N7_no_leak_verdict", "domain no-leak verdict"),
        ("SRC4513_19_domain_novector", "domain no-vector theorem", DOMAIN_NOVECTOR, "T6_no_vector_verdict", "domain no-vector verdict"),
        ("SRC4513_20_domain_parent_gate", "domain parent action gate", DOMAIN_PARENT_GATE, "G5_coefficients_retained", "domain coefficients retained"),
        ("SRC4513_21_domain_chain", "domain variation chain", DOMAIN_CHAIN, "V3_Ward_force", "domain Ward force conditional"),
        ("SRC4513_22_fixed_domain2355", "fixed domain theorem audit", FIXED_DOMAIN_2355, "FDT2355_6_current_corpus_verdict", "fixed domain not signed"),
        ("SRC4513_23_domain_bound2356", "domain motion bound rows", DOMAIN_BOUND_2356, "DMB2356_0_total", "domain motion envelope"),
        ("SRC4513_24_domain_env2356", "source domain envelope", DOMAIN_ENV_2356, "ENV2356_1_bound_path", "domain bound path"),
        ("SRC4513_25_readout_excl2625", "readout exclusion certificate", READOUT_EXCL_2625, "REC2625_1_solution_space_readout", "pure readout theorem"),
        ("SRC4513_26_readout_policy2625", "readout closure policy", READOUT_POLICY_2625, "POL2625_1_reduced_action_retention", "reduced action retained"),
        ("SRC4513_27_vbr1816", "variation-before-readout theorem", VBR_1816, "VBR1816_0_target", "variation order theorem"),
        ("SRC4513_28_rne2353", "readout no-reentry audit", RNE_2353, "RNE2353_7_verdict", "general readout zero not derived"),
        ("SRC4513_29_rng2418", "readout no-reentry gate", RNG_2418, "RNG2418_3_source_worldtube_projector", "worldtube/projector countermodel"),
        ("SRC4513_30_srng2335", "source-readout argument certificate", SRNG_2335, "SRNG2335_5_boundary", "boundary/readout certificate gap"),
        ("SRC4513_31_cbp2419", "chainmap readout bound pack", CBP_2419, "CBP2419_0_total", "chainmap absolute envelope"),
        ("SRC4513_32_bp2354", "readout reentry bound pack", BP_2354, "BP2354_0_total", "readout reentry finite envelope"),
        ("SRC4513_33_readout_tail2369", "readout tail matrix", READOUT_TAIL_2369, "ART2369_5_verdict", "readout tail selected"),
        ("SRC4513_34_readout_zero2370", "readout zero audit", READOUT_ZERO_2370, "ARZ2370_4_verdict", "readout zero not derived"),
        ("SRC4513_35_readout_bound2370", "first readout bound row", READOUT_BOUND_2370, "ARB2370_2_triangle_bound", "readout finite triangle bound"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def tail_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "BDR4513_0_tail_definition",
            "object": "T_tail,m",
            "statement": "The remaining 4509 surface/readout obstruction is the no-cancellation tail T_tail,m:=W_boundary,m+W_domain,m+W_readout,m.",
            "formula": "Theta_W,m = previous_filled_terms + T_tail,m",
            "result": "4513 isolates the last B_Weyl component after source-root, no-spurion and Khat-trace conditional fills",
            "status": "DERIVED_DECOMPOSITION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDR4513_1_boundary_zero",
            "object": "W_boundary,m",
            "statement": "Boundary tail vanishes if the parent branch has fixed/reference boundary data before variation, no memory-dependent boundary embedding or flux, and any boundary action is scalar stationary or exact/topological with zero local linked-sphere flux.",
            "formula": "D_m B_boundary=0 and n_mu P_loc_nu T_boundary^{mu nu}=0 => W_boundary,m=0",
            "result": "boundary hair is killed by owned no-flux/no-hair clauses, not by ignoring surface terms",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDR4513_2_domain_zero",
            "object": "W_domain,m",
            "statement": "Domain tail vanishes if the integration domain, source worldtube, support mask and projector are q-basic/fixed before readout, metric-independent or topological where required, and no local vector/flux/STF domain stress survives.",
            "formula": "D_m chi_D=0, [D_m,Pi_D]J=0, I_boundary_crossing=0 => W_domain,m=0",
            "result": "moving-domain and projector stress are not vague blockers; they are a fixed-domain/commutator theorem target",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDR4513_3_readout_zero",
            "object": "W_readout,m",
            "statement": "Readout tail vanishes only for pure postprocessing R_post:Sol(S_parent)/G->Data, or fixed external protocols/q,e_obs,theta-descendant maps that do not enter S_parent, S_eff, source normalization, coefficient extraction or calibration.",
            "formula": "R_post absent from variation domain => D_m(delta S_parent/delta fields)_readout=0",
            "result": "readout is harmless as reporting, but harmful as a varied reduced action, moving support mask or calibration feedback",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDR4513_4_combined_tail_zero",
            "object": "T_tail,m",
            "statement": "If BDR4513_1 through BDR4513_3 hold in the same parent branch, then the full boundary/domain/readout tail is zero termwise.",
            "formula": "W_boundary,m=W_domain,m=W_readout,m=0 => T_tail,m=0",
            "result": "the last B_Weyl tail gate has a real theorem shape with no cancellation between channels",
            "status": "COMBINED_TAIL_THEOREM_EXACT_BUT_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BDR4513_5_failure_bound",
            "object": "finite tail",
            "statement": "If any tail theorem clause remains unsigned, the tail is retained as an absolute finite vector.",
            "formula": "|B_Weyl_tail| <= 1/4(|W_boundary,m|+|W_domain,m|+|W_readout,m|)",
            "result": "fallback is sourced finite components, not a closure axiom or fitted cancellation",
            "status": "FINITE_NO_CANCELLATION_BOUND_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def tail_classifier_rows() -> List[Dict[str, object]]:
    return [
        {
            "class_id": "TCL4513_0_boundary_allowed",
            "tail": "boundary",
            "allowed_zero_class": "fixed reference boundary; scalar stationary marker-free collar; exact/topological primitive with zero local flux",
            "counterbranch": "normal exchange, tangential vector/shear, moving boundary, nontrivial boundary charge or derivative-silent monopole failure",
            "finite_component": "W_boundary,m / epsilon_B_flux_abs",
            "valid_for_claim": False,
        },
        {
            "class_id": "TCL4513_1_domain_allowed",
            "tail": "domain",
            "allowed_zero_class": "q-basic fixed support; metric-independent topological projector; scalar stationary selector; local trivial representative",
            "counterbranch": "Hodge/metric projector, moving support mask, domain vector/flux/STF stress, R11/source-normalization operator",
            "finite_component": "W_domain,m / epsilon_source_domain_motion_abs",
            "valid_for_claim": False,
        },
        {
            "class_id": "TCL4513_2_readout_allowed",
            "tail": "readout",
            "allowed_zero_class": "pure post-solution reporting or fixed external protocol after variation",
            "counterbranch": "readout-reduced action, source-worldtube projector, calibration/material feedback, fitted GM/orbit/support mask",
            "finite_component": "W_readout,m / epsilon_chainmap_readout_abs",
            "valid_for_claim": False,
        },
        {
            "class_id": "TCL4513_3_physical_EM_flux",
            "tail": "flux/Poynting side-channel",
            "allowed_zero_class": "physical stress counted in matter/EM Hilbert stress rather than hidden in readout/domain tail",
            "counterbranch": "wave/EM flux inserted as boundary/readout closure without current owner",
            "finite_component": "R_flux/current/source-normalization row",
            "valid_for_claim": False,
        },
        {
            "class_id": "TCL4513_4_no_cancellation",
            "tail": "combined",
            "allowed_zero_class": "each component zero termwise or independently bounded below arena thresholds",
            "counterbranch": "parent identity cancellation between boundary/domain/readout channels not supplied",
            "finite_component": "absolute sum vector",
            "valid_for_claim": False,
        },
    ]


def tail_input_fill_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "TIF4513_00_boundary",
            "source_4509_row": "BWN4509_10_Bboundary",
            "symbol": "W_boundary,m",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "fixed/reference boundary before variation; no memory-dependent boundary flux; scalar/exact/topological no-hair branch parent-signed",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "TIF4513_01_domain",
            "source_4509_row": "BWN4509_11_Bdomain",
            "symbol": "W_domain,m",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "domain/support/projector fixed or q-basic before readout; no domain vector/flux/STF stress; no R11/source-normalization leakage",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "TIF4513_02_readout",
            "source_4509_row": "BWN4509_12_Breadout",
            "symbol": "W_readout,m",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "pure postprocessing or fixed protocol/readout descended through q,e_obs,theta; no varied reduced action, source calibration, or projector reentry",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "TIF4513_03_tail_switch",
            "source_4509_row": "CZT4509_4_boundary_clause",
            "symbol": "Z_tail_BDR",
            "filled_value": "TRUE_CONDITIONAL",
            "fill_type": "ZERO_SWITCH_IF_PARENT_SIGNATURES_PASS",
            "condition": "boundary, domain and readout zero theorems hold in the same branch as source-root, no-spurion and Khat trace",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def tail_finite_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "TFB4513_0_tail_total",
            "quantity": "B_Weyl_tail",
            "formula": "|B_Weyl_tail| <= 1/4(|W_boundary,m|+|W_domain,m|+|W_readout,m|)",
            "required_inputs": "boundary flux/no-hair certificate or value; domain motion/projector envelope; readout chainmap envelope; common normalization; arena projections",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TFB4513_1_boundary",
            "quantity": "W_boundary,m",
            "formula": "|W_boundary,m| <= C_Bflux |epsilon_B_flux_abs| + |partial_m B_ref| + |B_normal_exchange| + |B_marker_vector|",
            "required_inputs": "epsilon_B_flux_abs or no-flux theorem; boundary reference derivative; normal exchange; marker/vector/shear exclusion",
            "current_status": "MISSING_BOUNDARY_CERTIFICATE_OR_NUMERIC_ROW",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TFB4513_2_domain",
            "quantity": "W_domain,m",
            "formula": "|W_domain,m| <= C_D(|I_domain_mask|+|I_boundary_crossing|+|E_projector_stress|+|E_domain_motion|+|R11_domain|)",
            "required_inputs": "fixed domain theorem or DMB2356 components; projector stress; domain vector/flux/STF row; R11/source-normalization row",
            "current_status": "MISSING_DOMAIN_COMPONENT_VALUES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TFB4513_3_readout",
            "quantity": "W_readout,m",
            "formula": "|W_readout,m| <= C_R(|C_feedback|+|C_protocol|+|Delta_cal|+|Delta_PPN|+|epsilon_chainmap_readout_abs|)",
            "required_inputs": "pure readout theorem or readout chainmap/source-worldtube/calibration component values",
            "current_status": "MISSING_READOUT_COMPONENT_VALUES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TFB4513_4_arena_projection",
            "quantity": "E_tail[arena]",
            "formula": "E_tail[arena] <= tau_tail_arena |B_Weyl_tail| + source/readout transfer terms",
            "required_inputs": "tau_R10; tau_PPN; tau_clock; tau_orbital; same-frame source normalization; no-cancellation envelope",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def final_vector_rows() -> List[Dict[str, object]]:
    return [
        {
            "vector_id": "BWFV4513_0_Lcg_chain",
            "component": "-2 L_cg^-3(F_m W_L+F W_L,m)",
            "status": "CONDITIONAL_ZERO_FROM_4510",
            "zero_condition": "source-root/double-zero parent lock signs F=F_m=0",
            "finite_fallback": "4509 BWN4509_00 through BWN4509_04",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_1_WFm",
            "component": "L_cg^-2 W_F,m",
            "status": "CONDITIONAL_ZERO_FROM_4511",
            "zero_condition": "no-spurion/readout grammar signs W_F,m=0",
            "finite_fallback": "4511 W_F,m finite rows plus B_qWeyl rows",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_2_RKtrace",
            "component": "R_K_trace,m",
            "status": "CONDITIONAL_ZERO_FROM_4512",
            "zero_condition": "Khat trace match signs D_m Tr(K_hat-Kmetric)=0",
            "finite_fallback": "4512 R_K trace finite bound rows",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_3_boundary",
            "component": "W_boundary,m",
            "status": "CONDITIONAL_ZERO_FROM_4513",
            "zero_condition": "fixed scalar/exact/topological boundary no-flux/no-hair",
            "finite_fallback": "TFB4513_1_boundary",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_4_domain",
            "component": "W_domain,m",
            "status": "CONDITIONAL_ZERO_FROM_4513",
            "zero_condition": "fixed q-basic domain/projector and no local domain vector/flux/STF stress",
            "finite_fallback": "TFB4513_2_domain",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_5_readout",
            "component": "W_readout,m",
            "status": "CONDITIONAL_ZERO_FROM_4513",
            "zero_condition": "pure postprocessing/fixed readout with no source calibration or reduced-action reentry",
            "finite_fallback": "TFB4513_3_readout",
            "valid_for_claim": False,
        },
        {
            "vector_id": "BWFV4513_6_combined",
            "component": "B_Weyl=-Theta_W,m/4",
            "status": "FULL_CONDITIONAL_ZERO_VECTOR_WRITTEN_NOT_PARENT_SIGNED",
            "zero_condition": "all six components zero in the same branch",
            "finite_fallback": "|B_Weyl| absolute sum over nonzero components; arena transfer still required",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4513_0_tail_theorem",
            "claim": "boundary/domain/readout tails have exact conditional zero theorems",
            "status": "DERIVED_CONDITIONALLY",
            "effect": "tail problem is split into boundary no-flux, fixed-domain and pure-readout no-reentry clauses",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4513_1_same_branch",
            "claim": "tail zero clauses are signed in the same active branch as 4510-4512",
            "status": "NOT_PROVEN",
            "effect": "full B_Weyl zero remains private/nonclaim",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4513_2_counterbranches",
            "claim": "all counterbranches are excluded",
            "status": "NOT_PROVEN",
            "effect": "normal boundary flux, moving domain masks, projector stress and readout calibration feedback remain finite rows",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4513_3_final_vector",
            "claim": "final B_Weyl vector is now complete as a theorem/fallback object",
            "status": "DERIVED_NONCLAIM_VECTOR",
            "effect": "next work can insert B_Weyl into B_mem_eff/body-charge without another generic tail audit",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4513_4_arena",
            "claim": "R10/PPN/clock/orbital arena projections are score-ready",
            "status": "NOT_READY",
            "effect": "tau arena transfer and same-frame source normalization still required before empirical local claims",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4513_0_tail_zero",
            "gate": "T_tail,m=0 live in active branch",
            "derived_now": False,
            "blocked_by": "boundary/domain/readout parent signatures not jointly signed",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4513_1_full_BWeyl_zero",
            "gate": "full B_Weyl=0",
            "derived_now": False,
            "blocked_by": "all six component zeros must hold in same parent branch; current active branch signatures remain unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4513_2_Bmem_eff",
            "gate": "B_mem_eff/body-charge local branch closed",
            "derived_now": False,
            "blocked_by": "B_Weyl vector must be inserted into B_mem_eff with same-frame normalization and body-charge/source coupling gates",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4513_3_local_GR",
            "gate": "local GR/PPN/R10 promotion",
            "derived_now": False,
            "blocked_by": "same-branch parent signature, arena transfer, source coupling and empirical projections remain open",
            "claim_allowed": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "boundary/domain/readout tail zero theorem and final no-cancellation B_Weyl vector",
            "not_derived": "active same-branch parent signatures and numeric/source-backed tail component values",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4513_0",
            "decision": DECISION,
            "because": "the last B_Weyl obstruction is not generic missingness; it is exactly boundary no-flux, fixed-domain/projector and pure-readout no-reentry in one branch",
            "effect": "the B_Weyl vector is now complete as a conditional theorem/fallback object; next target is B_mem_eff/body-charge insertion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4513_0",
            "target_file": NEXT_TARGET,
            "task": "insert the completed B_Weyl zero/fallback vector into B_mem_eff and the 4506 memory/fibre body-charge gate",
            "success_condition": "B_mem_eff has a single same-branch theorem condition or a finite body-charge bound vector using the complete B_Weyl components",
            "do_not": "restart a generic boundary/domain/readout audit or claim local GR from a private conditional vector",
            "valid_for_claim": False,
        }
    ]


def all_generated_csvs() -> List[Path]:
    return [
        SOURCE_REGISTER,
        TAIL_THEOREM,
        TAIL_CLASSIFIER,
        TAIL_INPUT_FILL,
        TAIL_FINITE_BOUND,
        FINAL_VECTOR,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    parsed = True
    details: List[str] = []
    for path in all_generated_csvs():
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    theorem_ok = any(row.get("theorem_id") == "BDR4513_4_combined_tail_zero" for row in all_rows["theorem"])
    fill_symbols = {row.get("symbol") for row in all_rows["fill"]}
    fill_ok = {"W_boundary,m", "W_domain,m", "W_readout,m"}.issubset(fill_symbols)
    final_vector_ok = any(row.get("vector_id") == "BWFV4513_6_combined" for row in all_rows["vector"])
    bound_ok = any(row.get("bound_id") == "TFB4513_0_tail_total" for row in all_rows["bound"])
    gates_blocked = all(falseish(row.get("claim_allowed")) for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            if "valid_for_claim" in row and not falseish(row["valid_for_claim"]):
                flags_false = False
            if "claim_allowed" in row and not falseish(row["claim_allowed"]):
                flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4513_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4513_01_tail_theorem", theorem_ok, "combined boundary/domain/readout tail theorem row exists"),
        ("VAL4513_02_tail_fills", fill_ok, "boundary, domain and readout tail conditional fill rows exist"),
        ("VAL4513_03_final_vector", final_vector_ok, "final B_Weyl vector row exists"),
        ("VAL4513_04_finite_bound", bound_ok, "tail absolute finite bound row staged"),
        ("VAL4513_05_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4513_06_nonclaim_flags", flags_false, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4513_07_csv_parse", parsed, ";".join(details)),
        ("VAL4513_08_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4513_09_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4513_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4513 boundary/domain/readout tail or final B_Weyl vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_final_BWeyl_tail_vector",
            "4513 derives the final boundary/domain/readout tail theorem for B_Weyl: W_boundary,m, W_domain,m and W_readout,m vanish termwise only under fixed/no-flux boundary ownership, q-basic fixed-domain/projector ownership, and pure postprocessing or fixed-protocol readout with no source-calibration/reduced-action reentry. The full B_Weyl component vector is now written, but same-branch parent signatures and numeric tail values remain unsigned.",
            "4513 source register, boundary/domain/readout tail theorem, tail classifier, tail input fills, finite tail bounds, final B_Weyl vector, parent audit, claim gates, status and validation.",
            "private_final_BWeyl_tail_vector_conditional_nonclaim",
            NEXT_TARGET,
            "claiming local GR/B_Weyl zero from private tail theorems, cancelling boundary/domain/readout components against each other, or hiding readout-reduced action/source calibration as postprocessing.",
            "local_gr_newton_r2fr_final_BWeyl_tail_vector",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "insert the completed B_Weyl vector into B_mem_eff/body-charge or source a finite body-charge bound.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    classifier: Sequence[Mapping[str, object]],
    fill: Sequence[Mapping[str, object]],
    bound: Sequence[Mapping[str, object]],
    vector: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4513 - Boundary Domain Readout Tail Or Final B_Weyl Vector

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4513 finishes the `B_Weyl` component split instead of circling another generic "boundary/readout missing" note.

After 4510, 4511 and 4512, the remaining tail is:

`T_tail,m := W_boundary,m + W_domain,m + W_readout,m`.

The exact zero route is termwise:

- `W_boundary,m=0` from fixed/reference boundary data plus no-flux/no-hair boundary ownership.
- `W_domain,m=0` from q-basic fixed domain/support/projector ownership plus no local domain vector, flux or STF stress.
- `W_readout,m=0` from pure postprocessing or fixed-protocol readout with no reduced-action, source-calibration or projector reentry.

If these hold in the same branch as the source-root, no-spurion and Khat-trace clauses, then the complete private vector gives:

`Theta_W,m=0`, hence `B_Weyl=-Theta_W,m/4=0`.

This is still not a public/local-GR claim. The same-branch parent signatures are not signed, and if any tail clause fails the fallback is the absolute no-cancellation row:

`|B_Weyl_tail| <= 1/4(|W_boundary,m|+|W_domain,m|+|W_readout,m|)`.

## Source Register

{table(sources)}

## Boundary Domain Readout Tail Theorem

{table(theorem)}

## Tail Component Classifier

{table(classifier)}

## Tail Input Fill Rows

{table(fill)}

## Tail Finite Bound Rows

{table(bound)}

## Final B_Weyl Vector

{table(vector)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    theorem = tail_theorem_rows()
    classifier = tail_classifier_rows()
    fill = tail_input_fill_rows()
    bound = tail_finite_bound_rows()
    vector = final_vector_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "classifier": classifier,
        "fill": fill,
        "bound": bound,
        "vector": vector,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TAIL_THEOREM, theorem)
    write_csv(TAIL_CLASSIFIER, classifier)
    write_csv(TAIL_INPUT_FILL, fill)
    write_csv(TAIL_FINITE_BOUND, bound)
    write_csv(FINAL_VECTOR, vector)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(
        sources,
        theorem,
        classifier,
        fill,
        bound,
        vector,
        parent,
        gates,
        status,
        decisions,
        next_target,
        validation,
    )
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4513 Boundary Domain Readout Tail Or Final B_Weyl Vector

Marker: `{MARKER}`  
4513 derives the final boundary/domain/readout tail theorem for `B_Weyl`. The remaining tail is `T_tail,m=W_boundary,m+W_domain,m+W_readout,m`; it vanishes termwise only with fixed/no-flux boundary ownership, q-basic fixed-domain/projector ownership, and pure postprocessing or fixed-protocol readout with no source-calibration/reduced-action reentry. The complete `B_Weyl` vector is now written as a private conditional theorem/fallback object. Same-branch parent signatures and arena projections remain unsigned.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4513 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now has the complete `B_Weyl` component vector: source-root/Lcg chain, no-spurion `W_F,m`, Khat trace, boundary, domain and readout. The next packet step is to insert this vector into `B_mem_eff` and the memory/fibre body-charge gate rather than repeating the tail audit.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
