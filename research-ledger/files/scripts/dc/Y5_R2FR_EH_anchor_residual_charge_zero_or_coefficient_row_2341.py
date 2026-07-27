from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EH_ANCHOR_RESIDUAL_CHARGE_ZERO_OR_COEFFICIENT_ROW_2341"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2341-Y5-R2FR-EH-anchor-residual-charge-zero-or-coefficient-row.md"

PATHS = {
    "2340_doc": ROOT / "2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
    "2340_validation": OUT / "P8_Y5_BRR545_2340_VALIDATION.csv",
    "2340_next": OUT / "P8_Y5_PARENT_QLOC_2340_NEXT_TARGET.csv",
    "2340_split": OUT / "P8_Y5_PARENT_QLOC_2340_EH_ANCHOR_RESIDUAL_SPLIT.csv",
    "2340_sector": OUT / "P8_Y5_PARENT_QLOC_2340_SECTOR_EXTRACTION_MATRIX.csv",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "2334_nogamma": OUT / "P8_Y5_PARENT_QLOC_2334_NO_GAMMA_THEOREM_STACK.csv",
    "2335_claims": OUT / "P8_Y5_PARENT_QLOC_2335_CLAIM_GATES.csv",
    "2336_naturality": OUT / "P8_Y5_PARENT_QLOC_2336_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv",
    "2338_bzero": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv",
    "1016_doc": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "1009_doc": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "rc994": OUT / "P8_Y5_R10_994_MTS_RESIDUAL_CURRENT_PACK.csv",
    "sce992": OUT / "P8_Y5_R10_992_CHARGE_CURRENT_RESIDUAL_LEDGER.csv",
    "lgr907": OUT / "P8_Y5_R10_907_LOCAL_GR_RESIDUAL_STACK_ROLLUP.csv",
}

SOURCES = [
    ("SRC2341_00_2340_doc", "2340_doc", PATHS["2340_doc"], ["ERS2340_0_EH_anchor_law", "DEC2340_1_real_progress"], "2340 EH-anchor residual split"),
    ("SRC2341_01_2340_validation", "2340_validation", PATHS["2340_validation"], ["VAL2340_OVERALL", "PASS"], "2340 validation"),
    ("SRC2341_02_2340_next", "2340_next", PATHS["2340_next"], ["NEXT2340_0", "EH-anchor-residual-charge-zero"], "machine-readable 2341 target"),
    ("SRC2341_03_2340_split", "2340_split", PATHS["2340_split"], ["Delta_Q_res", "epsilon_Hres_abs"], "EH-anchor split rows"),
    ("SRC2341_04_2340_sector", "2340_sector", PATHS["2340_sector"], ["SEM2340_6_total", "epsilon_parent_charge_abs"], "sector residual map"),
    ("SRC2341_05_1010_doc", "1010_doc", PATHS["1010_doc"], ["QRES1010_0_q_loc_vector", "retained_until_S_GK_proved"], "GK/q_loc retained residual"),
    ("SRC2341_06_2334_nogamma", "2334_nogamma", PATHS["2334_nogamma"], ["NGT2334_4_result", "CONDITIONAL_THEOREM_NOT_CORPUS_PROMOTED"], "conditional no-Gamma theorem"),
    ("SRC2341_07_2335_claims", "2335_claims", PATHS["2335_claims"], ["CG2335_4_local_GR_Newton", "false"], "SRNG claim gates"),
    ("SRC2341_08_2336_naturality", "2336_naturality", PATHS["2336_naturality"], ["DNF2336_7_verdict", "PARTIAL_DERIVATION"], "downstream observation naturality limit"),
    ("SRC2341_09_2338_bzero", "2338_bzero", PATHS["2338_bzero"], ["BZR2338_0_first_row", "MISSING_B_ZERO_FLUX"], "Bzero boundary numerator row"),
    ("SRC2341_10_1016_doc", "1016_doc", PATHS["1016_doc"], ["FIS1016_0_M_H_ref", "DEC1016_2_first_input_order"], "source-measure/M_H_ref bridge"),
    ("SRC2341_11_1009_doc", "1009_doc", PATHS["1009_doc"], ["PCS1009_6_mass_projector_PiM", "CG1009_4_PiM_source_measure"], "parent projector/source-measure blocker"),
    ("SRC2341_12_rc994", "rc994", PATHS["rc994"], ["RC994_0_reference_boundary", "RC994_6_EM_clock_coupling_guard"], "residual current pack"),
    ("SRC2341_13_sce992", "sce992", PATHS["sce992"], ["SCE992_Delta_nonEH", "SCE992_Delta_cal"], "charge-current residual ledger"),
    ("SRC2341_14_lgr907", "lgr907", PATHS["lgr907"], ["LGR907_2_source_GM", "LGR907_5_PPN_vector"], "local-GR residual rollup"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2341_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_PARENT_QLOC_2341_RESIDUAL_CHARGE_ZERO_AUDIT.csv",
    "component_map": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COMPONENT_MAP.csv",
    "coefficient_rows": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COEFFICIENT_ROWS.csv",
    "observable_map": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_OBSERVABLE_MAP.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2341_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2341_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2341_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2341_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2341_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2341_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2341_0_zero_audit", OUTPUTS["zero_audit"], BETA_DOCS / "RESIDUAL_CHARGE_ZERO_AUDIT_2341_NONCLAIM.csv"),
    ("COPY2341_1_coefficients", OUTPUTS["coefficient_rows"], MICRO_RESIDUALS / "DELTA_QRES_COEFFICIENT_ROWS_2341_NONCLAIM.csv"),
    ("COPY2341_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2341_DELTA_QRES_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_0_target",
            "clause": "residual charge zero target",
            "zero_statement": "Delta_Q_res=0 and Delta_H_res=0 for the local compact source-free branch.",
            "current_evidence": "2340 wrote Q_tau^MTS=Q_tau^EH+Delta_Q_res and selected this zero theorem next",
            "status": "TARGET_SHARPENED",
            "obstruction": "must prove every retained non-EH sector is zero/topological/fixed or source-bounded",
            "fallback": "absolute coefficient vector epsilon_Qres_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_1_no_gamma_help",
            "clause": "no-Gamma/SRNG contribution",
            "zero_statement": "ordinary source/readout Gamma slot can vanish if all source, clock, light, orbit, boundary and projector maps descend through observed variables.",
            "current_evidence": "2334-2336 give exact conditional lemmas but keep source/readout/boundary/projector slots unsigned",
            "status": "PARTIAL_CONDITIONAL_ZERO_NOT_GLOBAL",
            "obstruction": "boundary/projector/source-measure re-entry still open",
            "fallback": "Delta_frame_source and B_obs_source_measure coefficients",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_2_boundary",
            "clause": "boundary/reference residual",
            "zero_statement": "Q_tau^boundary/ref plus Delta_ref, B_zero_flux and Delta_symp vanish or are fixed topological data before readout.",
            "current_evidence": "2338 retains B_zero_flux/M_H_ref first row with MISSING_B_ZERO_FLUX and MISSING_M_H_REF",
            "status": "ZERO_NOT_DERIVED",
            "obstruction": "fixed reference, boundary no-flux and positive M_H_ref are missing",
            "fallback": "c_boundary_ref coefficient row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_3_GK_qloc",
            "clause": "Gamma/Khat/q_loc residual",
            "zero_statement": "S_GK plus metric-response K_hat plus Helmholtz plus Euler/double-zero imply q_loc^nu=0 and no extra charge.",
            "current_evidence": "1010 keeps q_loc retained until S_GK/metric response/Helmholtz/Euler/double-zero/boundary are signed",
            "status": "ZERO_NOT_DERIVED",
            "obstruction": "q_loc remains an explicit residual, not a theorem-zero",
            "fallback": "c_GK_q_loc coefficient row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_4_projector",
            "clause": "projector/source-measure residual",
            "zero_statement": "C_projector+[d,Pi_M]J_H and Pi_M J_H-J_M_parent vanish by parent symplectic projector algebra.",
            "current_evidence": "1009 and 1016 keep Pi_M/source-measure and R_eq/I_commutator unsigned",
            "status": "ZERO_NOT_DERIVED",
            "obstruction": "projector origin, product variation, worldtube selector and M_H_ref are missing",
            "fallback": "c_projector and c_source_glue coefficient rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_5_coupling",
            "clause": "coupling/source-measure equality",
            "zero_statement": "the Hamiltonian charge equals the measured Hilbert/source charge and reduces to orbital GM only after the Poisson/Gauss bridge.",
            "current_evidence": "2340 marks coupling/source-measure as structural; 1016 keeps M_H_ref and source-measure first input blocked",
            "status": "ZERO_NOT_DERIVED",
            "obstruction": "measured GM cannot fill M_H_ref without circularity",
            "fallback": "c_coupling_G and c_calibration coefficient rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCZ2341_6_verdict",
            "clause": "Delta_Q_res=Delta_H_res=0 now",
            "zero_statement": "RCZ2341_1 through RCZ2341_5 all parent-signed would promote the EH anchor to a local GR/Newton branch.",
            "current_evidence": "current corpus has conditional lemmas and residual ledgers, not global residual-charge silence",
            "status": "ZERO_THEOREM_NOT_DERIVED_RETAIN_COEFFICIENT_ROWS",
            "obstruction": "the missing clauses are independent, so sign cancellation is not allowed",
            "fallback": "stage epsilon_Qres_abs and component coefficient rows",
            "valid_for_claim": "false",
        },
    ]


def build_component_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_0_boundary_ref",
            "delta_component": "Delta_Q_boundary_ref",
            "source_residual": "RC994_0_reference_boundary;SCE992_Delta_symp",
            "formula": "Q_boundary + delta B_ref + C_ref",
            "zero_condition": "fixed H_ref plus boundary/improvement no-flux before readout",
            "fallback": "abs(Delta_Q_boundary_ref)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_1_GK_extra",
            "delta_component": "Delta_Q_GK_extra",
            "source_residual": "RC994_1_extra_nonEH;QRES1010_0_q_loc_vector",
            "formula": "Q_extra + C_extra from Gamma/Khat/q_loc and retained non-EH sectors",
            "zero_condition": "S_GK metric-response Helmholtz Euler double-zero boundary theorem",
            "fallback": "abs(Delta_Q_GK_extra)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_2_projector",
            "delta_component": "Delta_Q_projector",
            "source_residual": "RC994_2_projector_domain;SCE992_Delta_PiM",
            "formula": "C_projector + [d,Pi_M]J_H + delta Pi_M terms",
            "zero_condition": "parent Pi_M chain-map variation and R_eq/I_commutator zero",
            "fallback": "abs(Delta_Q_projector)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_3_source_glue",
            "delta_component": "Delta_Q_source_glue",
            "source_residual": "RC994_3_matter_source_glue;SCE992_Delta_flux",
            "formula": "C_matter[J_H] + worldtube source-measure glue residual",
            "zero_condition": "source support selector, same coframe/tau and compact linked surfaces parent-signed",
            "fallback": "abs(Delta_Q_source_glue)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_4_coupling_constant",
            "delta_component": "Delta_Q_coupling_G",
            "source_residual": "RC994_4_coupling_constant;SCE992_Delta_G",
            "formula": "C_Geff + C_kappa + source-normalization drift",
            "zero_condition": "constant universal coupling descent and no source/range/domain dependence",
            "fallback": "abs(Delta_Q_coupling_G)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_5_readout_tail",
            "delta_component": "Delta_Q_readout_PPN",
            "source_residual": "RC994_5_readout_PPN_tail;SCE992_Delta_PPN",
            "formula": "C_readout + second-order PPN source-response tail",
            "zero_condition": "readout downstream naturality plus PPN residual vector zero/bounded",
            "fallback": "abs(Delta_Q_readout_PPN)/M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQC2341_6_EM_clock",
            "delta_component": "Delta_Q_EM_clock",
            "source_residual": "RC994_6_EM_clock_coupling_guard",
            "formula": "C_EM/clock/source readout leakage",
            "zero_condition": "EM/clock coupling descends through the same observed variables with no hidden source channel",
            "fallback": "abs(Delta_Q_EM_clock)/M_H_ref",
            "valid_for_claim": "false",
        },
    ]


def build_coefficient_rows() -> list[dict[str, Any]]:
    rows = []
    for component in build_component_map_rows():
        suffix = component["row_id"].replace("DQC2341_", "")
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"CQR2341_{suffix}",
                "coefficient": f"c_{component['delta_component'].replace('Delta_Q_', '')}",
                "quantity": component["delta_component"],
                "formula": component["fallback"],
                "required_columns": "system_id;component_id;coefficient_value;coefficient_units;M_H_ref;M_H_ref_units;source_path;equation_ref;zero_certificate;observable_map;valid_for_claim",
                "current_value": "MISSING_COEFFICIENT;MISSING_M_H_REF;MISSING_SOURCE_PATH",
                "score_ready": "false",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "CQR2341_7_abs_sum",
            "coefficient": "epsilon_Qres_abs",
            "quantity": "absolute residual charge envelope",
            "formula": "epsilon_Qres_abs >= sum_i abs(Delta_Q_i)/M_H_ref",
            "required_columns": "system_id;component_values;M_H_ref;component_sources;no_cancellation_guard;observable_map;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": "false",
        }
    )
    return rows


def build_observable_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOM2341_0_local_GR",
            "arena": "local GR/Newton",
            "mapped_components": "all Delta_Q_i plus M_H_ref",
            "observable_effect": "failure of EH local field equation/source normalization and Newtonian inverse-square readout",
            "claim_gate": "requires epsilon_Qres_abs=0 or bounded below local threshold plus source-measure bridge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOM2341_1_PPN",
            "arena": "PPN/Cassini/local clocks",
            "mapped_components": "Delta_Q_GK_extra;Delta_Q_projector;Delta_Q_readout_PPN;Delta_Q_EM_clock",
            "observable_effect": "gamma-1, beta-1, alpha_i, xi, clock/WEP residual vector",
            "claim_gate": "requires component projection coefficients and absolute bounds",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOM2341_2_source_GM",
            "arena": "orbital/source normalization",
            "mapped_components": "Delta_Q_source_glue;Delta_Q_coupling_G;Delta_Q_projector;Delta_Q_boundary_ref",
            "observable_effect": "closed charge differs from measured GM or drifts with radius/source/readout",
            "claim_gate": "requires M_H_ref, Poisson/Gauss bridge, R_eq and I_commutator gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QOM2341_3_R10_R11",
            "arena": "R10/R11/local fifth-force",
            "mapped_components": "Delta_Q_GK_extra;Delta_Q_coupling_G;Delta_Q_source_glue",
            "observable_effect": "finite-range or source-dependent residual force if q_loc/source coupling is nonzero",
            "claim_gate": "requires coefficient rows plus real bound data and no missing parent inputs",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2341_0_zero_result",
            "decision": "do not claim Delta_Q_res=0 or Delta_H_res=0",
            "reason": "no-Gamma/SRNG is conditional and the boundary, GK, projector, coupling and source-measure clauses remain unsigned",
            "consequence": "EH anchor remains a comparison spine, not a completed local-GR proof",
            "status": "ZERO_THEOREM_FAILED_CLEANLY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2341_1_coefficients",
            "decision": "stage Delta_Q_res coefficient rows",
            "reason": "the residual theorem failed by independent components, so the honest fallback is an absolute coefficient vector",
            "consequence": "future work can fill or zero one component at a time without hiding sign cancellations",
            "status": "COEFFICIENT_ROWS_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2341_2_next",
            "decision": "prioritize source-charge equals measured-GM bridge next",
            "reason": "even if residual charge silence improves, local Newton recovery still needs the Hamiltonian charge to be the observed source charge",
            "consequence": "next target attacks coupling/source-measure equality, with residual coefficients retained",
            "status": "SELECT_SOURCE_MEASURE_BRIDGE_NEXT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2341_3_public_policy",
            "decision": "no GitHub update from 2341",
            "reason": "this is private theorem triage and residual plumbing, not a public claim checkpoint",
            "consequence": "continue private derivation/testing sequence",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2341_0_Delta_Q_zero", "Delta_Q_res=0 theorem", "false", "independent residual channels remain unsigned"),
        ("CG2341_1_Delta_H_zero", "Delta_H_res=0 theorem", "false", "theta_res and Q_res are not parent-silenced"),
        ("CG2341_2_coefficients_score", "Delta_Q coefficient vector score-ready", "false", "coefficients, M_H_ref and source paths are missing"),
        ("CG2341_3_source_measure", "Hamiltonian charge equals measured source charge", "false", "source-measure bridge remains next target"),
        ("CG2341_4_local_GR_Newton", "local GR/Newton recovery derived", "false", "EH anchor residual and source-GM bridge remain open"),
        ("CG2341_5_github", "safe public GitHub update", "false", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "passed": passed,
            "claim_effect": effect,
            "valid_for_claim": "false",
        }
        for row_id, gate, passed, effect in gates
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2341_0_EH_anchor_total",
            "claim": "treat EH anchor as full MTS charge because Delta_Q_res is unnamed",
            "allowed": "false",
            "reason": "Delta_Q_res is now explicitly decomposed into named components",
            "blocking_rows": "RCZ2341_6_verdict;DQC2341_0_boundary_ref;DQC2341_6_EM_clock",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2341_1_no_gamma_overreach",
            "claim": "use conditional no-Gamma/SRNG to erase all residual charge components",
            "allowed": "false",
            "reason": "no-Gamma helps a slot but does not close boundary, projector, source-measure or GK residuals globally",
            "blocking_rows": "RCZ2341_1_no_gamma_help;RCZ2341_2_boundary;RCZ2341_4_projector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2341_2_sign_cancellation",
            "claim": "let residual components cancel by signs in Delta_Q_res",
            "allowed": "false",
            "reason": "independent missing clauses require an absolute-sum envelope unless a parent identity proves cancellation",
            "blocking_rows": "CQR2341_7_abs_sum",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2341_3_orbital_denominator",
            "claim": "score coefficient rows using orbital GM before M_H_ref is derived",
            "allowed": "false",
            "reason": "using observed GM now would be circular for the GR/Newton bridge",
            "blocking_rows": "DEC2341_2_next;CG2341_3_source_measure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2341_4_local_claim",
            "claim": "2341 proves local GR/Newton recovery",
            "allowed": "false",
            "reason": "2341 only decomposes the residual charge and stages nonclaim coefficient rows",
            "blocking_rows": "CG2341_4_local_GR_Newton;DEC2341_0_zero_result",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2341_0",
            "next_target": "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
            "why": "local Newton recovery needs the Hamiltonian/EH-anchor charge to equal the measured source charge; residual silence alone is not enough.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2341_1",
            "next_target": "2342b-Y5-R2FR-DeltaQres-largest-component-zero-or-bound.md",
            "why": "parallel route: attack the largest live coefficient channel, probably boundary/projector/GK depending on source-measure outcome.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2341_2",
            "next_target": "2342c-Y5-R2FR-DeltaQres-coefficient-source-row-runner.md",
            "why": "fallback route: fill the staged coefficient rows with units, source paths and observable maps.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied_rows = read_csv_rows(destination)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": str(len(copied_rows)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    component_map: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    observable_map: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL2341_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"))
    validations.append(("VAL2341_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"))
    validations.append(("VAL2341_02_zero_not_promoted", any(row["status"] == "ZERO_THEOREM_NOT_DERIVED_RETAIN_COEFFICIENT_ROWS" for row in zero_audit), "residual charge zero theorem not promoted"))
    validations.append(("VAL2341_03_component_map_complete", len(component_map) >= 7 and any(row["delta_component"] == "Delta_Q_EM_clock" for row in component_map), "Delta_Q_res component map covers all RC994 channels"))
    validations.append(("VAL2341_04_coefficients_nonready", len(coefficient_rows) >= 8 and all(row["score_ready"] == "false" for row in coefficient_rows), "coefficient rows remain non-score-ready"))
    validations.append(("VAL2341_05_observable_map_written", len(observable_map) >= 4 and any(row["arena"] == "local GR/Newton" for row in observable_map), "observable map includes local GR/Newton"))
    validations.append(("VAL2341_06_claim_gates_blocked", all(row["passed"] == "false" for row in claims), "all claim gates remain blocked"))
    validations.append(("VAL2341_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal), "shortcut claims refused"))
    validations.append(("VAL2341_08_next_selected", any("2342-Y5-R2FR-source-charge-equals-measured-GM" in row["next_target"] for row in next_rows), "2342 source-charge measured-GM next target recorded"))
    validations.append(("VAL2341_09_github_blocked", any(row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision), "public GitHub update not recommended from 2341"))
    validations.append(("VAL2341_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copies), "branch copies exist and parse"))

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths.extend(destination for _, _, destination in BRANCH_COPY_SPECS)
    validations.append(("VAL2341_11_outputs_exist", all(path.exists() for path in generated_paths), "CSV outputs and branch copies exist before doc render"))

    no_claim_flags = True
    for path in [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]:
        if path.exists() and path.suffix == ".csv":
            rows = read_csv_rows(path)
            if any(row.get("valid_for_claim", "").lower() == "true" for row in rows):
                no_claim_flags = False
                break
    validations.append(("VAL2341_12_no_claim_flags", no_claim_flags, "no generated row is valid_for_claim=true"))

    formalization_clean = not any(FORMALIZATION.rglob("*2341*")) if FORMALIZATION.exists() else True
    validations.append(("VAL2341_13_formalization_untouched_by_2341", formalization_clean, "no 2341 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in validations
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2341_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2341 attempts Delta_Q_res/Delta_H_res zero, rejects promotion, stages absolute coefficient rows, and selects source-charge measured-GM bridge next.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    component_map: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    observable_map: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2341 - EH-anchor residual charge zero or coefficient row

## Summary

2341 tries the theorem route:

`Delta_Q_res = 0` and `Delta_H_res = 0`.

It does not close. The useful result is sharper: the residual charge is now decomposed into independent channels
instead of being a vague "non-EH remainder". No-Gamma/SRNG helps one part of the route, but boundary/reference,
Gamma-Khat/q_loc, projector/source-measure, coupling, readout, and EM/clock leakage remain separate gates.

So the honest fallback is:

`epsilon_Qres_abs >= sum_i abs(Delta_Q_i)/M_H_ref`.

No sign cancellation, no orbital-GM denominator backfill, and no EH-anchor-as-total-charge shortcut.

## Source Register

{markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Residual Charge Zero Audit

{markdown_table(zero_audit, ["row_id", "clause", "zero_statement", "current_evidence", "status", "obstruction", "fallback", "valid_for_claim"])}

## Delta_Q_res Component Map

{markdown_table(component_map, ["row_id", "delta_component", "source_residual", "formula", "zero_condition", "fallback", "valid_for_claim"])}

## Coefficient Rows

{markdown_table(coefficient_rows, ["row_id", "coefficient", "quantity", "formula", "current_value", "score_ready", "valid_for_claim"])}

## Observable Map

{markdown_table(observable_map, ["row_id", "arena", "mapped_components", "observable_effect", "claim_gate", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claims, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(copies, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> int:
    sources = build_sources()
    zero_audit = build_zero_audit_rows()
    component_map = build_component_map_rows()
    coefficient_rows = build_coefficient_rows()
    observable_map = build_observable_map_rows()
    decision = build_decision_rows()
    claims = build_claim_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero_audit"], zero_audit)
    write_csv(OUTPUTS["component_map"], component_map)
    write_csv(OUTPUTS["coefficient_rows"], coefficient_rows)
    write_csv(OUTPUTS["observable_map"], observable_map)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    copies = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copies)

    validation = build_validation(sources, zero_audit, component_map, coefficient_rows, observable_map, decision, claims, refusal, next_rows, copies)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(sources, zero_audit, component_map, coefficient_rows, observable_map, decision, claims, refusal, next_rows, copies, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"2341 validation failed: {len(failed)} failed rows")
        for row in failed:
            print(f"{row['row_id']}: {row['detail']}")
        return 1

    print(f"2341 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
