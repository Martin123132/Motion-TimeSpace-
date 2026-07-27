from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
SOURCE_WEIGHT_DOCS = SOURCE_WEIGHT / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
HAMILTONIAN_SOURCE = ROOT / "source-intake" / "hamiltonian-source"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2978"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2978-Y5-R2FR-no-linear-source-JZ-BZ-theorem-or-source-bound-rows-under-AX1090.md"

SRC_2977_DOC = ROOT / "2977-Y5-R2FR-response-doublet-MAB-Zbasis-owner-and-no-linear-source-lock-or-DeltaK-deltaM-row-under-AX1090.md"
SRC_2977_NEXT = RESIDUALS / "P8_Y5_R2FR_2977_NEXT_TARGET.csv"
SRC_2977_NO_LINEAR = RESIDUALS / "P8_Y5_R2FR_2977_NO_LINEAR_SOURCE_JZ_BZ_AUDIT.csv"
SRC_2977_OWNER = RESIDUALS / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv"
SRC_2977_DELTAK = RESIDUALS / "P8_Y5_R2FR_2977_DELTAK_DELTAM_DELTAZ_BOUND_ROWS_NONCLAIM.csv"
SRC_2977_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2977_VALIDATION.csv"

SRC_2164_LOCK = SOURCE_WEIGHT_DOCS / "AFRAME_JZ_BZ_COUPLING_LOCK_2164_NONCLAIM.csv"
SRC_2891_NO_BOUNDARY = SOURCE_WEIGHT / "RAB_NO_BOUNDARY_SOURCE_THEOREM_2891_NONCLAIM.csv"
SRC_2956_DESCENT = PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv"
SRC_2940_CURRENT_CHAIN = PARENT_ACTION / "Minimal_parent_current_chain_action_synthesis_2940_NONCLAIM.csv"
SRC_2967_ADOPTION = PARENT_ACTION / "response_doublet_parent_density_adoption_2967_NOT_PROMOTED.csv"
SRC_2537_MATTER = BETA_DOCS / "Minimal_universal_matter_coupling_2537_PRIVATE_NONCLAIM.csv"
SRC_2538_NOETHER = BETA_DOCS / "Noether_source_charge_identity_2538_NONCLAIM.csv"
SRC_2356_DESCENT_CLAUSES = BETA_DOCS / "PARENT_DESCENT_CLAUSES_2356_NONCLAIM.csv"
SRC_2336_NATURALITY = BETA_DOCS / "DOWNSTREAM_NATURALITY_DERIVATION_AUDIT_2336_NONCLAIM.csv"
SRC_2446_CURRENT_PACK = HAMILTONIAN_SOURCE / "MTS_residual_current_pack_for_S_Eq_2446_NONCLAIM.csv"
SRC_2521_JMEM = BETA_DOCS / "Jmem_drive_bound_rows_2521_NONCLAIM.csv"
SRC_2522_JDIRECT = BETA_DOCS / "Jdirect_matter_bound_rows_2522_NONCLAIM.csv"
SRC_2523_JREADOUT = BETA_DOCS / "Jreadout_bound_rows_2523_NONCLAIM.csv"
SRC_2524_JPIM = BETA_DOCS / "JPiM_bound_rows_2524_NONCLAIM.csv"
SRC_2544_BZERO = BETA_DOCS / "Bzero_no_flux_theorem_audit_2544_NONCLAIM.csv"
SRC_2546_BOUNDARY = BETA_DOCS / "Boundary_term_classification_2546_NONCLAIM.csv"
SRC_2852_SYM = LOCAL_BOUNDS / "RAB_SOURCE_DOUBLET_SYMMETRY_CANDIDATES_2852_NONCLAIM.csv"
SRC_2857_OWNER = SOURCE_WEIGHT / "RAB_VERTICAL_GENERATOR_OWNERSHIP_GATE_2857_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2978_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2978_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv",
    "clauses": RESIDUALS / "P8_Y5_R2FR_2978_JZ_BZ_CLAUSE_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2978_JZ_BZ_SOURCE_BOUND_ROWS_NONCLAIM.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2978_QLOC_ENVELOPE_UPDATE_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2978_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2978_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2978_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2978_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2978_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "no_linear_source_JZ_BZ_theorem_attempt_2978_NOT_DERIVED.csv",
    "bounds_copy": LOCAL_BOUNDS / "JZ_BZ_source_boundary_bound_rows_2978_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2978_no_marker_source_covector_or_JZ_coefficients_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except Exception:
        return False
    return True


def anchors_present(path: Path, anchors: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(anchor in text for anchor in anchors)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2978_0_2977_doc", SRC_2977_DOC, ["Status:", "Next target is narrower"], "2977 markdown handoff"),
        ("SRC2978_1_2977_next", SRC_2977_NEXT, ["NEXT2977_0_2978", "J_Z=B_Z=0"], "selected 2978 target"),
        ("SRC2978_2_2977_no_linear", SRC_2977_NO_LINEAR, ["NL2977_1_source_current", "NL2977_2_boundary", "NL2977_5_verdict"], "J_Z/B_Z retained blockers"),
        ("SRC2978_3_2977_owner", SRC_2977_OWNER, ["OWN2977_6_matter_descent", "OWN2977_7_verdict"], "owner lock blockers"),
        ("SRC2978_4_2977_deltak", SRC_2977_DELTAK, ["DK2977_2_JZ", "DK2977_3_BZ"], "J_Z/B_Z bound placeholders"),
        ("SRC2978_5_2977_validation", SRC_2977_VALIDATION, ["VAL2977_OVERALL"], "2977 validation"),
        ("SRC2978_6_2164_lock", SRC_2164_LOCK, ["SFE2164_1_bulk_theorem", "SFE2164_2_boundary_theorem", "SFE2164_5_Y5_Y6", "SFE2164_6_verdict"], "J_Z/B_Z conditional coupling lock"),
        ("SRC2978_7_2891_boundary", SRC_2891_NO_BOUNDARY, ["NBT2891_2_source_neutrality", "NBT2891_3_boundary_charge_zero", "NBT2891_5_verdict"], "no-boundary/source descent attempt"),
        ("SRC2978_8_2956_descent", SRC_2956_DESCENT, ["DESC2956_0_chain_rule", "DESC2956_4_constants", "DESC2956_7_verdict"], "matter pullback descent audit"),
        ("SRC2978_9_2940_current_chain", SRC_2940_CURRENT_CHAIN, ["SYN2940_2_universal_matter", "SYN2940_4_GK_current_law", "SYN2940_8_verdict"], "parent current-chain synthesis"),
        ("SRC2978_10_2967_adoption", SRC_2967_ADOPTION, ["RDA2967_5_source_boundary_silence", "RDA2967_7_verdict"], "response doublet adoption blocker"),
        ("SRC2978_11_2537_matter", SRC_2537_MATTER, ["MUC2537_1_source_blind_functor", "MUC2537_5_nonhilbert_policy", "MUC2537_6_verdict"], "minimal universal matter coupling"),
        ("SRC2978_12_2538_noether", SRC_2538_NOETHER, ["NSCI2538_5_nonhilbert_channels", "NSCI2538_7_verdict"], "Noether source charge identity"),
        ("SRC2978_13_2356_descent_clauses", SRC_2356_DESCENT_CLAUSES, ["PDC2356_2_matter_action_factorization", "PDC2356_5_no_source_only_slot", "PDC2356_9_verdict"], "parent descent clauses"),
        ("SRC2978_14_2336_naturality", SRC_2336_NATURALITY, ["DNF2336_2_downstream_separation", "DNF2336_6_boundary_projective_limit", "DNF2336_7_verdict"], "downstream naturality"),
        ("SRC2978_15_2446_current_pack", SRC_2446_CURRENT_PACK, ["RCS2446_3_matter_source_glue", "RCS2446_6_EM_clock_mass_coupling_guard", "RCS2446_7_verdict"], "residual current pack"),
        ("SRC2978_16_2521_jmem", SRC_2521_JMEM, ["JDRV2521_0_Jmem_total", "JDRV2521_9_Qmem_insertion"], "finite memory drive rows"),
        ("SRC2978_17_2522_jdirect", SRC_2522_JDIRECT, ["JDIR2522_0_total", "JDIR2522_7_Qmem_insertion"], "finite direct matter rows"),
        ("SRC2978_18_2523_jreadout", SRC_2523_JREADOUT, ["JRO2523_0_total", "JRO2523_10_Qmem_insertion"], "finite readout rows"),
        ("SRC2978_19_2524_jpim", SRC_2524_JPIM, ["JPIM2524_0_total", "JPIM2524_11_Jreadout_insertion"], "finite Pi_M rows"),
        ("SRC2978_20_2544_bzero", SRC_2544_BZERO, ["BZT2544_0_target", "BZT2544_6_verdict"], "B_zero no-flux audit"),
        ("SRC2978_21_2546_boundary", SRC_2546_BOUNDARY, ["exact", "corner"], "boundary classification"),
        ("SRC2978_22_2852_sym", SRC_2852_SYM, ["SYM2852_1_Z2_or_OE_evenness", "SYM2852_3_no_marker_object_language"], "source-doublet symmetry candidates"),
        ("SRC2978_23_2857_owner", SRC_2857_OWNER, ["OWN2857_4_boundary", "OWN2857_5_matter", "OWN2857_6_full_vector"], "vertical generator ownership gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "role": role,
                    "required_anchors": ";".join(anchors),
                    "exists": path.exists(),
                    "anchors_found": anchors_present(path, anchors),
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "THM2978_0_fixed_point_calculus",
            "object": "fixed-point derivative",
            "statement": "If E is an exact involution with E:Z->-Z and F(EZ)=F(Z), then dF/dZ|_{Z=0}=0.",
            "status": "MATHEMATICALLY_VALID_TEMPLATE",
            "proof_or_blocker": "ordinary parity/fixed-point calculus; this proves only the template derivative, not that all MTS source terms obey E",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_1_bulk_JZ",
            "object": "J_Z bulk source current",
            "statement": "J_Z := delta S_bulk/delta Z|_0 vanishes if the complete bulk source functional is exchange-even.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_blocker": "SFE2164_1 has the correct theorem shape, but exact source/readout/Y5/Y6 ownership is not closed",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_2_matter_pullback",
            "object": "ordinary matter source",
            "statement": "delta_v S_matter=0 if S_matter factors through q(Phi), Dq(v_Z)=0, and matter labels/constants are Z-silent.",
            "status": "CHAIN_RULE_VALID_PREMISES_UNSIGNED",
            "proof_or_blocker": "DESC2956_0 is valid, but q, no-marker constants, shadow frames and worldtube boundaries remain unsigned",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_3_readout_order",
            "object": "readout/projector source re-entry",
            "statement": "post-variation observations cannot source Z if readout is downstream/natural after the variational problem.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_blocker": "DNF2336 supplies the naturality shape, but boundary/projective and source-selector clauses remain open",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_4_no_source_covector",
            "object": "independent odd source covector",
            "statement": "A no-marker object-language theorem would forbid an independent source-doublet covector coupling linearly to Z.",
            "status": "BEST_ROUTE_NOT_PROVED",
            "proof_or_blocker": "SYM2852_3 identifies the route, but it is too broad in the current corpus and MUC/PDC clauses keep source-only slots live",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_5_boundary_BZ",
            "object": "B_Z boundary/source work",
            "statement": "B_Z=0 if boundary/linking functional is exchange-even, exact, no-flux, or a parent-owned proper charge.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "proof_or_blocker": "BZT2544/NBT2891 give conditional routes, but boundary charge/reference/worldtube ownership is not signed",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_6_Y5_Y6",
            "object": "Y5 source normalization and Y6 extra stress",
            "statement": "Y5/Y6 must be even, topological, gauge, exact, or explicitly bounded before J_Z/B_Z can be zero.",
            "status": "OPEN_HARD_BLOCK",
            "proof_or_blocker": "SFE2164_5 and BLK1712_2 style blockers survive; parity wording alone does not kill these channels",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "theorem_id": "THM2978_7_verdict",
            "object": "J_Z=B_Z no-linear-source theorem",
            "statement": "J_Z=B_Z=0 follows only if all bulk, matter, readout, no-marker, Y5/Y6 and boundary clauses close in one parent branch.",
            "status": "NOT_DERIVED_RETAIN_FINITE_SOURCE_BOUND_ROWS",
            "proof_or_blocker": "the fixed-point theorem is sound, but the physical coupling premises are not parent-signed",
            "parent_signed": False,
            "theorem_zero": False,
        },
    ]
    return [add_common(row) for row in rows]


def clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2978_0_exact_exchange", "exact E:Z->-Z symmetry of full source action", "SFE2164_1;RDT2800_1;SYM2852_1", "CONDITIONAL_ONLY", "does not yet own all source/readout variables"),
        ("CL2978_1_parent_q_kernel", "q exists before readout and v_Z in ker(Dq)", "PDC2356_0;PDC2356_1;OWN2857_1", "NOT_PARENT_SIGNED", "q/v_Z remains unsigned"),
        ("CL2978_2_matter_factorization", "ordinary matter action factors through q up to exact/proper boundary", "DESC2956_0;DESC2956_3;PDC2356_2", "CONDITIONAL_ONLY", "direct source/worldtube vertices remain legal"),
        ("CL2978_3_constants_markers", "masses, alpha, clocks, material labels and source constants are Z-silent", "DESC2956_4;MUC2537_3;PDC2356_4", "MISSING_NO_MARKER_THEOREM", "continuous constants and material/source markers survive"),
        ("CL2978_4_no_shadow_frame", "no hidden Weyl/disformal/source-only frame or active current slot", "DESC2956_5;MUC2537_5;NSCI2538_5", "MISSING_NO_SHADOW_FRAME_THEOREM", "non-Hilbert source-current channels remain legal"),
        ("CL2978_5_variation_before_readout", "source current extracted before material/readout projection", "DNF2336_2;PDC2356_6;SYN2940_4", "CONDITIONAL_ONLY", "readout/projector re-entry rows remain finite nonclaim"),
        ("CL2978_6_boundary_no_flux", "boundary/worldtube/support terms are zero, exact, proper, or bounded", "BZT2544_6;PDC2356_7;NBT2891_3", "NOT_PARENT_SIGNED", "boundary/reference/support ownership is missing"),
        ("CL2978_7_coupling_owner", "coupling/source normalization fixed before readout", "NBT2891_4;RCS2446_4;SYN2940_2", "REQUIRED_NOT_SIGNED", "kappa/source scale and measured GM conventions remain live"),
        ("CL2978_8_Y5", "source-normalization channel is even/topological/bounded", "SFE2164_5;RCS2446_4", "OPEN_HARD_BLOCK", "source normalization can masquerade as a linear source"),
        ("CL2978_9_Y6", "extra-stress channel is even/topological/bounded", "SFE2164_5;RCS2446_6", "OPEN_HARD_BLOCK", "visible coefficients and extra stress can source the residual"),
        ("CL2978_10_same_branch", "all clauses close in the same parent branch, not separately", "RDA2967_7;THM2978_7_verdict", "NOT_CLOSED", "no single branch signs every clause"),
    ]
    return [
        add_common(
            {
                "clause_id": clause_id,
                "required_clause": required_clause,
                "evidence_anchors": anchors,
                "status": status,
                "blocking_gap": blocker,
                "clause_closed": False,
            }
        )
        for clause_id, required_clause, anchors, status, blocker in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("JZ2978_0_total", "eps_JZ", "eps_JZ <= eps_direct + eps_mem + eps_readout + eps_PiM + eps_shadow + eps_Y5 + eps_Y6 + eps_coupling", "source norm", "MISSING_SOURCE_BACKED_COMPONENT_VALUES", "all J_Z component coefficients and norms", "JDRV2521_0_Jmem_total;JDIR2522_0_total;JRO2523_0_total;JPIM2524_0_total"),
        ("JZ2978_1_direct_matter", "eps_JZ_direct", "direct matter/source coupling contribution", "source norm", "MISSING_DIRECT_COEFFICIENT", "source-blind matter functor or finite direct coefficient", "JDIR2522_0_total;MUC2537_1_source_blind_functor"),
        ("JZ2978_2_memory_drive", "eps_JZ_mem", "memory/bath/domain/worldtube drive contribution", "source norm", "MISSING_MEMORY_DRIVE_COEFFICIENT", "Jmem component coefficients", "JDRV2521_0_Jmem_total;JDRV2521_9_Qmem_insertion"),
        ("JZ2978_3_readout", "eps_JZ_readout", "readout/projector/material/calibration re-entry contribution", "source norm", "MISSING_READOUT_COEFFICIENT", "J_readout component coefficients", "JRO2523_0_total;JRO2523_10_Qmem_insertion"),
        ("JZ2978_4_PiM", "eps_JZ_PiM", "mass-projector/source-normalization commutator contribution", "source norm", "MISSING_PIM_COEFFICIENT", "Pi_M commutator/source-normalization rows", "JPIM2524_0_total;JPIM2524_11_Jreadout_insertion"),
        ("JZ2978_5_shadow_marker", "eps_JZ_shadow", "hidden frame/source-only marker/non-Hilbert current contribution", "source norm", "MISSING_NO_MARKER_OR_BOUND", "no-marker theorem or finite shadow coefficient", "DESC2956_4;DESC2956_5;NSCI2538_5"),
        ("JZ2978_6_Y5", "eps_JZ_Y5", "source-normalization Y5 contribution", "source norm", "MISSING_Y5_ZERO_OR_BOUND", "Y5 even/topological proof or finite coefficient", "SFE2164_5_Y5_Y6;RCS2446_4_coupling_constant"),
        ("JZ2978_7_Y6", "eps_JZ_Y6", "extra-stress/visible-coefficient Y6 contribution", "source norm", "MISSING_Y6_ZERO_OR_BOUND", "Y6 even/topological proof or finite coefficient", "SFE2164_5_Y5_Y6;RCS2446_6_EM_clock_mass_coupling_guard"),
        ("BZ2978_0_total", "eps_BZ", "eps_BZ <= eps_no_flux + eps_ref + eps_worldtube + eps_endpoint + eps_corner + eps_coupling", "boundary/source norm", "MISSING_BOUNDARY_COMPONENT_VALUES", "all B_Z component coefficients and norms", "BZT2544_0_target;Boundary_term_classification_2546;NBT2891_3_boundary_charge_zero"),
        ("BZ2978_1_no_flux", "eps_BZ_no_flux", "boundary no-flux/exactness failure contribution", "boundary/source norm", "MISSING_NO_FLUX_CERTIFICATE", "parent symplectic extraction, compact support, denominator", "BZT2544_1_parent_symplectic;BZT2544_6_verdict"),
        ("BZ2978_2_reference", "eps_BZ_ref", "fixed reference/counterterm/corner leakage", "boundary/source norm", "MISSING_REFERENCE_OWNER", "fixed B_ref and exact/proper counterterm", "BZT2544_2_fixed_reference;Boundary_certificate_matrix_2546"),
        ("BZ2978_3_worldtube", "eps_BZ_worldtube", "source support/worldtube drift contribution", "boundary/source norm", "MISSING_WORLDTUBE_OWNER", "support/source selector owned before readout", "PDC2356_7_boundary_support_silence;DNF2336_4_source_selector"),
        ("BZ2978_4_endpoint_readout", "eps_BZ_endpoint", "readout endpoint/linking-surface leakage", "boundary/source norm", "MISSING_ENDPOINT_BOUND", "finite endpoint/readout coefficient", "JRO2523_8_boundary_endpoint;JPIM2524_6_Bzero"),
        ("BZ2978_5_coupling_owner", "eps_BZ_coupling", "coupling/source normalization boundary leakage", "boundary/source norm", "MISSING_COUPLING_OWNER", "kappa/source normalization fixed before readout", "NBT2891_4_coupling_owner;RCS2446_4_coupling_constant"),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "definition_or_bound": definition,
                "units": units,
                "status": status,
                "required_input": required_input,
                "source_anchors": anchors,
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "accepted_for_scoring": False,
            }
        )
        for bound_id, symbol, definition, units, status, required_input, anchors in rows
    ]


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "envelope_id": "ENV2978_0_q_loc_total",
            "quantity": "q_loc",
            "formula": "||q_loc|| <= ||q_formal|| + ||DeltaK_deltaM|| + ||DeltaK_deltaZ|| + eps_JZ + eps_BZ + eps_MAB_domain",
            "meaning": "2978 replaces hidden source silence with explicit J_Z/B_Z residual rows.",
            "status": "NONCLAIM_ABSOLUTE_ENVELOPE",
        },
        {
            "envelope_id": "ENV2978_1_JZ",
            "quantity": "eps_JZ",
            "formula": "eps_JZ <= eps_direct + eps_mem + eps_readout + eps_PiM + eps_shadow + eps_Y5 + eps_Y6 + eps_coupling",
            "meaning": "bulk/source current is not zero unless no-marker/source-evenness premises close.",
            "status": "FINITE_ROWS_REQUIRED",
        },
        {
            "envelope_id": "ENV2978_2_BZ",
            "quantity": "eps_BZ",
            "formula": "eps_BZ <= eps_no_flux + eps_ref + eps_worldtube + eps_endpoint + eps_corner + eps_coupling",
            "meaning": "boundary/source work is not zero unless no-flux/exact/proper boundary premises close.",
            "status": "FINITE_ROWS_REQUIRED",
        },
        {
            "envelope_id": "ENV2978_3_no_cancellation",
            "quantity": "absolute guardrail",
            "formula": "all residual rows enter by absolute value until a parent identity proves cancellation",
            "meaning": "prevents source-current or boundary leakage being hidden by sign choices.",
            "status": "NO_CANCELLATION_GUARD_ACTIVE",
        },
    ]
    return [add_common(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2978_0_fixed_point_math", "parity fixed-point derivative template", True, "mathematical template only", False),
        ("CG2978_1_JZ_zero", "J_Z=0 physical source-current theorem", False, "bulk/matter/readout/no-marker/Y5/Y6 premises unsigned", False),
        ("CG2978_2_BZ_zero", "B_Z=0 boundary/source theorem", False, "boundary/reference/worldtube/no-flux premises unsigned", False),
        ("CG2978_3_q_loc_zero", "q_loc local residual vanishes", False, "J_Z/B_Z and DeltaK rows retained", False),
        ("CG2978_4_local_GR", "local GR/Newton limit derived from MTS branch", False, "local residual suppression not proved", False),
        ("CG2978_5_empirical_claims", "R10/PPN/clock/orbital/WEP scoring claim", False, "no finite source-backed bounds and no theorem zero", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2978_0_math",
            "decision": "Keep the fixed-point derivative theorem as a valid lemma template.",
            "because": "an exact even functional has zero first Z-variation at the fixed point.",
            "next_action": "use it only after the physical source functional is parent-signed",
        },
        {
            "decision_id": "DEC2978_1_no_claim",
            "decision": "Do not claim J_Z=0 or B_Z=0.",
            "because": "matter descent, no-marker/source-only slot, Y5/Y6 and boundary ownership remain unsigned.",
            "next_action": "retain explicit J_Z/B_Z residual rows",
        },
        {
            "decision_id": "DEC2978_2_best_route",
            "decision": "Attack the independent source-covector/no-marker theorem next.",
            "because": "this is the most direct way to turn the coupling gut-feel into a derivable source silence condition.",
            "next_action": "try to forbid source-only covectors representation-theoretically; otherwise acquire finite J_Z coefficients",
        },
        {
            "decision_id": "DEC2978_3_boundary",
            "decision": "Keep B_Z as a separate boundary/source guard.",
            "because": "even a clean matter coupling theorem does not automatically prove no-flux or exact boundary charge.",
            "next_action": "carry B_Z rows forward until a boundary theorem or numeric bound exists",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2978_0_2979",
            "priority": "selected_primary",
            "next_doc": "2979-Y5-R2FR-no-marker-source-covector-theorem-or-JZ-component-coefficient-acquisition-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_no_marker_source_covector_theorem_or_JZ_component_coefficient_acquisition_under_AX1090_2979.py",
            "objective": "Try to prove that the parent object language forbids an independent source-doublet covector coupled linearly to Z; if not, acquire finite J_Z component coefficients.",
            "include": "source-only slot;no-marker theorem;source covector;matter constants;clock/material labels;hidden frame;Y5;Y6;J_direct;J_mem;J_readout;J_PiM",
            "exclude": "B_Z full boundary proof;full K_metric certificate;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
        }
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common({"copy_id": key, "path": str(path), "exists": path.exists()})
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    formalization_2978_count = 0
    if FORMALIZATION.exists():
        formalization_2978_count = sum(1 for path in FORMALIZATION.rglob("*2978*") if path.is_file())
    checks = [
        ("VAL2978_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2978_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2978_2_fixed_point_template", any(row["theorem_id"] == "THM2978_0_fixed_point_calculus" and row["status"] == "MATHEMATICALLY_VALID_TEMPLATE" for row in all_rows["theorem"]), "fixed-point parity template recorded", True),
        ("VAL2978_3_theorem_not_claimed", any(row["theorem_id"] == "THM2978_7_verdict" and row["status"].startswith("NOT_DERIVED") for row in all_rows["theorem"]), "J_Z/B_Z theorem remains unclaimed", True),
        ("VAL2978_4_clauses_open", all(not row["clause_closed"] for row in all_rows["clauses"]), "all physical source clauses remain open/nonclaim", True),
        ("VAL2978_5_bound_rows_nonclaim", all((not row["accepted_for_scoring"]) and row["valid_for_claim"] is False for row in all_rows["bounds"]), "J_Z/B_Z bound rows remain nonclaim", True),
        ("VAL2978_6_claims_blocked_except_template", all((row["claim_gate_id"] == "CG2978_0_fixed_point_math") or (row["claim_allowed"] is False) for row in all_rows["claims"]), "physics claim gates remain blocked", True),
        ("VAL2978_7_next_target_written", any(row["next_id"] == "NEXT2978_0_2979" for row in all_rows["next"]), "2979 no-marker/J_Z coefficient target selected", True),
        ("VAL2978_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2978_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2978_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2978_11_formalization_clean", formalization_2978_count == 0, f"no 2978 outputs were written to formalization-workbench (count={formalization_2978_count})", True),
        ("VAL2978_12_doc_written", DOC.exists(), "2978 markdown checkpoint exists", True),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2978_OVERALL", "passed": overall, "check": "2978 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2978 - No-Linear-Source J_Z/B_Z Theorem or Source-Bound Rows

Status: `Y5_R2FR_2978_fixed_point_JZ_BZ_template_valid_physical_source_theorem_not_parent_signed_bound_rows_written_nonclaim`

Claim ceiling: `no_JZ_zero_no_BZ_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The clean mathematical lemma is alive: an exact exchange-even functional has zero first derivative at the `Z=0` fixed point.
- The physical theorem does not close yet: source/readout descent, no-marker/source-only slot, hidden frame, Y5/Y6, and boundary ownership are not parent-signed.
- This is still progress: the coupling problem is now exposed as `J_Z` plus `B_Z`, instead of being hidden inside a vague local plateau axiom.
- The honest fallback is an absolute residual envelope with explicit `eps_JZ` and `eps_BZ` component rows.
- Best next attack: prove that a parent source-doublet covector is not an allowed object; otherwise acquire finite `J_Z` coefficients.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## Theorem Attempt

{md_table(all_rows["theorem"], ["theorem_id", "object", "statement", "status", "proof_or_blocker", "theorem_zero"])}

## Clause Audit

{md_table(all_rows["clauses"], ["clause_id", "required_clause", "evidence_anchors", "status", "blocking_gap", "clause_closed"])}

## J_Z / B_Z Bound Rows

{md_table(all_rows["bounds"], ["bound_id", "symbol", "definition_or_bound", "units", "status", "required_input", "upper_bound"])}

## q_loc Envelope Update

{md_table(all_rows["envelope"], ["envelope_id", "quantity", "formula", "meaning", "status"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "theorem": theorem_rows(),
        "clauses": clause_rows(),
        "bounds": bound_rows(),
        "envelope": envelope_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
    shutil.copyfile(OUTPUTS["bounds"], BRANCH_OUTPUTS["bounds_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2978 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
