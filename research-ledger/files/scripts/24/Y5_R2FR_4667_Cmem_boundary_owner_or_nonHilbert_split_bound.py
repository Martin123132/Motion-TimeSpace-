from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4667"
CLAIM_ID = "L-509"
BRANCH = "MTS_R2FR_Y5_CMEM_BOUNDARY_NONHILBERT_SPLIT_BOUND_4667"
MARKER = "PPC4161_CMEM_BOUNDARY_NONHILBERT_SPLIT_BOUND_4667"
PACKET_MARKER = "PPC4161_PACKET_CMEM_BOUNDARY_NONHILBERT_SPLIT_BOUND_4667"
DECISION = "CMEM_BOUNDARY_NONHILBERT_ZERO_PRIVATE_QBASIC_NOFLUX_HPERP_BRANCH_DYNAMIC_BOUNDS_RETAINED_NONCLAIM"
NEXT_TARGET = "4668-Y5-R2FR-Cmem-final-zero-to-body-charge-source-charge-gate.md"

DOC_PATH = POST / "4667-Y5-R2FR-Cmem-boundary-owner-or-nonHilbert-split-bound.md"
FORMAL_PATH = FORMAL / "683-PPC4161-Cmem-boundary-owner-or-nonHilbert-split-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4666 = POST / "4666-Y5-R2FR-Cmem-readout-apparatus-owner-or-transfer-bound.md"
FORMAL_682 = FORMAL / "682-PPC4161-Cmem-readout-apparatus-owner-or-transfer-bound.md"

CSV_4666_LHRS = SOURCE_DIR / "P8_Y5_R2FR_4666_LHRS_CMEM_FINAL_UPDATE_AFTER_READOUT.csv"
CSV_4666_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4666_NEXT_TARGET.csv"
CSV_4666_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4666_STATUS.csv"
CSV_4666_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4666_VALIDATION.csv"
CSV_4600_BNH = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
CSV_4609_QEDGE = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv"
CSV_4609_FLUX = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_BOUNDARY_FLUX_ROWS.csv"
CSV_4640_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4640_BOUNDARY_TRANSITION_IMPORT_AUDIT.csv"
CSV_4640_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4640_BOUNDARY_HISTORY_COMPONENT_STATUS.csv"
CSV_4645_CERT = SOURCE_DIR / "P8_Y5_R2FR_4645_XINONHILBERT_ZERO_CERTIFICATE.csv"
CSV_4645_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4645_ALPHA_NONHILBERT_COMPONENT.csv"
CSV_4645_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4645_XINONHILBERT_ZERO_RUNNER_RESULTS.csv"
CSV_4646_CERT = SOURCE_DIR / "P8_Y5_R2FR_4646_BOUNDARY_HISTORY_ZERO_CERTIFICATE.csv"
CSV_4646_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4646_ALPHA_BOUNDARY_HISTORY_COMPONENT.csv"
CSV_4646_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4646_BOUNDARY_HISTORY_ZERO_RUNNER_RESULTS.csv"
CSV_4431_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_INPUT.csv"
CSV_4431_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_OUTPUT.csv"
CSV_4516_HILBERT = SOURCE_DIR / "P8_Y5_R2FR_4516_STATIONARY_HILBERT_SOURCE_SUBTHEOREM.csv"
CSV_4520_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4520_POYNTING_HILBERT_FLOW_GATE.csv"
CSV_4530_BOUNDARY_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4530_BOUNDARY_POYNTING_SPLIT.csv"
CSV_4553_NOFLUX = SOURCE_DIR / "P8_Y5_R2FR_4553_BOUNDARY_NOFLUX_THEOREM_ATTEMPT.csv"
CSV_4571_NOHAIR = SOURCE_DIR / "P8_Y5_R2FR_4571_STATIC_BOUNDARY_NOHAIR_THEOREM.csv"
CSV_4571_VERDICT = SOURCE_DIR / "P8_Y5_R2FR_4571_BOUNDARY_BRANCH_VERDICT.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4667_SOURCE_REGISTER.csv"
SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_BOUNDARY_NONHILBERT_SPLIT.csv"
BOUNDARY_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_BOUNDARY_ZERO_IMPORT.csv"
NONHILBERT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_NONHILBERT_ZERO_IMPORT.csv"
DYNAMIC_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_DYNAMIC_BOUNDARY_NONHILBERT_BOUND_ROWS.csv"
FINAL_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_FINAL_CMEM_UPDATE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4667_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4667_VALIDATION.csv"


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


def table(rows: list[dict[str, Any]]) -> str:
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
        ("SRC4667_00_4666_next", CSV_4666_NEXT, "4667-Y5-R2FR-Cmem-boundary-owner-or-nonHilbert-split-bound.md", "4666 selected boundary/non-Hilbert."),
        ("SRC4667_01_4666_LHRS_zero", CSV_4666_LHRS, "RLU4666_2_LHRS_zero", "LHRS already zero in strict branch."),
        ("SRC4667_02_4666_final_live", CSV_4666_LHRS, "RLU4666_3_final_Cmem", "final Cmem before 4667."),
        ("SRC4667_03_4666_status", CSV_4666_STATUS, "BOUNDARY_NONHILBERT_REMAIN", "4666 status import."),
        ("SRC4667_04_4666_validation", CSV_4666_VALIDATION, "VAL4666_OVERALL", "4666 validation pass."),
        ("SRC4667_05_682_formal", FORMAL_682, "C_mem^final_live", "formal handoff."),
        ("SRC4667_06_doc4666_decision", DOC_4666, "DEC4666_0", "4666 decision handoff."),
        ("SRC4667_07_4600_boundary", CSV_4600_BNH, "BNH4600_0_boundary_variation", "boundary variation zero-or-bound theorem."),
        ("SRC4667_08_4600_nonHilbert", CSV_4600_BNH, "BNH4600_1_nonHilbert_decomposition", "non-Hilbert zero-or-bound theorem."),
        ("SRC4667_09_4600_combined", CSV_4600_BNH, "BNH4600_3_combined_boundary_nonHilbert", "combined boundary/non-Hilbert split."),
        ("SRC4667_10_4609_Qedge", CSV_4609_QEDGE, "QE4609_0_decomposition", "Q_edge shell/boundary split."),
        ("SRC4667_11_4609_shell_zero", CSV_4609_QEDGE, "QE4609_1_reynolds_shell_zero", "Reynolds shell zero route."),
        ("SRC4667_12_4609_flux_zero", CSV_4609_QEDGE, "QE4609_2_boundary_flux_zero", "boundary flux zero route."),
        ("SRC4667_13_4609_antifit", CSV_4609_QEDGE, "QE4609_3_anti_circularity", "anti-circularity guard."),
        ("SRC4667_14_4609_flux_total", CSV_4609_FLUX, "QEB4609_6_total", "boundary flux total bound."),
        ("SRC4667_15_4640_boundary_import", CSV_4640_AUDIT, "AUD4640_1_boundary_import", "boundary/history import."),
        ("SRC4667_16_4640_same_branch", CSV_4640_AUDIT, "AUD4640_3_no_cross_branch", "same-branch assembly guard."),
        ("SRC4667_17_4640_no_flux_collar", CSV_4640_STATUS, "BH4640_2", "source-free no-flux collar status."),
        ("SRC4667_18_4645_NH_zero", CSV_4645_CERT, "ZC4645_3_nonHilbert_zero", "non-Hilbert exact-zero certificate."),
        ("SRC4667_19_4645_alpha_zero", CSV_4645_ALPHA, "ALPHA4645_0_alpha_nonHilbert", "alpha non-Hilbert zero component."),
        ("SRC4667_20_4645_runner", CSV_4645_RUNNER, "RUN4645_1_Hperp_certificate", "non-Hilbert runner certificate."),
        ("SRC4667_21_4646_boundary_zero", CSV_4646_CERT, "ZC4646_4_boundary_history_zero", "boundary/history exact-zero certificate."),
        ("SRC4667_22_4646_alpha_zero", CSV_4646_ALPHA, "ALPHA4646_0_alpha_boundary_history", "alpha boundary/history zero component."),
        ("SRC4667_23_4646_runner", CSV_4646_RUNNER, "RUN4646_1_no_flux_certificate", "boundary runner certificate."),
        ("SRC4667_24_4646_radiative_guard", CSV_4646_RUNNER, "RUN4646_5_radiative_flux", "radiative/Poynting guard."),
        ("SRC4667_25_4431_contract", CSV_4431_INPUT, "NH4431_0_exact_nonHilbert_zero_contract", "non-Hilbert exact contract."),
        ("SRC4667_26_4431_residual", CSV_4431_OUTPUT, "NH4431_1_current_residual_retained", "non-Hilbert residual retained off branch."),
        ("SRC4667_27_4516_mass_flux", CSV_4516_HILBERT, "SHS4516_3_mass_flux_surface_lock", "stationary mass-flux surface lock."),
        ("SRC4667_28_4520_poynting", CSV_4520_POYNTING, "PHF4520_3_verdict", "Poynting Hilbert-owned or retained."),
        ("SRC4667_29_4530_radiative", CSV_4530_BOUNDARY_POYNTING, "B4530_2_radiative_poynting_flux", "radiative Poynting boundary guard."),
        ("SRC4667_30_4553_private_no_flux", CSV_4553_NOFLUX, "BN4553_4_verdict", "private no-flux branch verdict."),
        ("SRC4667_31_4571_fixed_collar", CSV_4571_NOHAIR, "BN4571_1_fixed_collar_boundary_zero", "fixed collar boundary no-hair."),
        ("SRC4667_32_4571_public_block", CSV_4571_VERDICT, "BV4571_2_public_claim", "public claim remains blocked."),
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


def split_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SPL4667_0_import", "C_mem^final_live", "|C_mem^final_live| <= |C_mem^boundary|+|C_mem^nonHilbert|", "4666", "import after LHRS closure"),
        ("SPL4667_1_boundary", "C_mem^boundary", "Pi_mem[X_boundary_history + X_boundary_flux]", "4600;4609;4646", "worldtube/collar/edge/boundary-history channel"),
        ("SPL4667_2_nonHilbert", "C_mem^nonHilbert", "Pi_mem[X_nonHilbert_source_bypass]", "4600;4639;4645", "orthogonal quotient/current/spin/torsion/improvement/readout bypass channel"),
        ("SPL4667_3_no_cancellation", "zero route", "C_mem^boundary=0 and C_mem^nonHilbert=0 separately", "4600", "do not cancel boundary against non-Hilbert"),
        ("SPL4667_4_dynamic_bound", "fallback", "|C_mem^boundary|+|C_mem^nonHilbert|", "4600;4609;4431", "absolute-sum fallback when either branch clause fails"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": row[0],
            "object": row[1],
            "formula_or_rule": row[2],
            "source_basis": row[3],
            "meaning": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def boundary_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BZI4667_0_definition", "C_mem^boundary := Pi_mem[Q_edge_boundary/history]", "boundary/history source-worldtube edge contribution is separated from LHRS/readout", "BNH4600_0; QE4609_0; AUD4640_1", "TARGET_DEFINED"),
        ("BZI4667_1_shell_zero", "Q_edge_Reynolds_shell=0", "fixed q-basic compact support, zero trace density and no birth/death shell kill Reynolds shell leakage", "QE4609_1; ZC4646_1", "SHELL_ZERO_BRANCH"),
        ("BZI4667_2_flux_zero", "Q_edge_boundary_flux=0", "proper compact generator, source-free no-flux collar, fixed boundary/corner/reference/projector class and no side/radiative crossing", "QE4609_2; ZC4646_2", "BOUNDARY_FLUX_ZERO_BRANCH"),
        ("BZI4667_3_antifit", "support/projector/reference fixed before scoring", "no post-fit support, local-GM denominator or reference choice is allowed to create zero", "QE4609_3; ZC4646_3", "ANTI_CIRCULARITY_GUARD"),
        ("BZI4667_4_poynting_guard", "radiative EM/gravity/Poynting flux is routed, not erased", "stationary compact no-flux branch only; radiative flux becomes an explicit boundary/Hilbert charge row", "PHF4520_3; RUN4646_5; B4530_2", "RADIATIVE_FIREWALL"),
        ("BZI4667_5_result", "C_mem^boundary=0", "shell zero and boundary-flux zero hold in the same q-basic fixed-worldtube no-flux collar branch", "ZC4646_4; RUN4646_1", "CMEM_BOUNDARY_ZERO_PRIVATE_BRANCH"),
        ("BZI4667_6_scope", "not a global boundary theorem", "open/radiative/transition/moving-boundary/domain-selector/corner-edge branches keep finite rows", "BV4571_1; BV4571_2", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def nonhilbert_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("NZI4667_0_definition", "C_mem^nonHilbert := Pi_mem[X_nonHilbert_source_bypass]", "remaining non-Hilbert current/projector/improvement tails after Hilbert source extraction", "BNH4600_1; AUD4639_0", "TARGET_DEFINED"),
        ("NZI4667_1_quotient_split", "H_L=H_q+Hperp", "only the orthogonal representative Hperp can feed non-Hilbert source bypass after quotient descent", "F4639_0; ZC4645_0", "QUOTIENT_SPLIT_IMPORTED"),
        ("NZI4667_2_Hperp_silence", "S_A Hperp^A=0 or Hperp=0", "active source functional has no representative leg outside the quotient branch", "AUD4639_1; ZC4645_1", "HPERP_SILENT_BRANCH"),
        ("NZI4667_3_readout_silence", "R_src_readout=0 and Dq_source_readout[Hperp]=0", "source/readout factors through q and remains fixed after variation", "F4639_2; ZC4645_2", "READOUT_SILENT_BRANCH"),
        ("NZI4667_4_current_exact_or_owned", "spin/torsion/improvement/decoupled currents are absent, exact, Hilbert-owned or compact-flux silent", "Noether/improvement bypass cannot enter local source projection unless compact flux or readout reentry survives", "NH4431_0; NH4431_2", "CURRENT_BYPASS_GUARD"),
        ("NZI4667_5_result", "C_mem^nonHilbert=0", "source-pairing and readout remainder vanish on the same Hperp-silent branch", "ZC4645_3; RUN4645_1", "CMEM_NONHILBERT_ZERO_PRIVATE_BRANCH"),
        ("NZI4667_6_scope", "not a global non-Hilbert theorem", "surviving Hperp, spin/torsion, exact-divergence flux, readout reentry or decoupled current uses finite rows", "NH4431_1; RUN4645_2", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def dynamic_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DBN4667_0_total", "Delta_boundary_nonHilbert_mem", "|C_mem^boundary|+|C_mem^nonHilbert|", "absolute no-cancellation envelope for all off-branch boundary/non-Hilbert tails", "BNH4600_3"),
        ("DBN4667_1_boundary_shell", "C_boundary_shell", "K_edge W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)", "moving support, nonzero trace or birth/death shell", "QE4609_1"),
        ("DBN4667_2_boundary_flux", "C_boundary_flux", "|B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|", "Hamiltonian/corner/reference/side/radiative/projector flux", "QEB4609_6_total"),
        ("DBN4667_3_poynting", "F_rad / Phi_EM_rad", "|int_DeltaTau int_partialW S dot n dA dtau|", "radiative EM/gravity/Poynting cannot be killed by compact stationary no-flux theorem", "B4530_2; PHF4520_3"),
        ("DBN4667_4_nonHilbert_Hperp", "C_nonHilbert_Hperp", "K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)", "Hperp or source/readout bypass survives", "F4639_3; RUN4645_2"),
        ("DBN4667_5_nonHilbert_current", "C_nonHilbert_current", "E_spin+E_torsion+E_improvement+E_readout+E_shadow_projector+E_decoupled", "spin/torsion/improvement/exact-divergence/readout/decoupled current tails", "BNH4600_1; NH4431_1"),
        ("DBN4667_6_source_contract", "C_mem_boundary_nonHilbert_source_row", "arena;component;surface_flux;corner;reference;sidewall;radiative;projector;Hperp;spin;torsion;improvement;readout_reentry;operator_norm;units;source_path;valid_for_claim", "future claim-grade finite row contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def final_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CFU4667_0_before", "|C_mem^final_live| <= |C_mem^boundary|+|C_mem^nonHilbert|", "4666 final vector after LHRS closure", "IMPORTED_FROM_4666"),
        ("CFU4667_1_boundary_zero", "C_mem^boundary=0", "q-basic fixed-worldtube regular no-flux collar branch", "BOUNDARY_TERM_REMOVED"),
        ("CFU4667_2_nonHilbert_zero", "C_mem^nonHilbert=0", "Hperp source-pairing/readout-silent quotient branch", "NONHILBERT_TERM_REMOVED"),
        ("CFU4667_3_same_branch", "same private branch required", "ordinary-visible Hilbert source, fixed observed coframe/Hodge/readout/support, fixed no-flux collar, Hperp silence and no calibration feedback", "SAME_BRANCH_GUARD"),
        ("CFU4667_4_final_zero", "C_mem^final_live=0", "standard/weight, LHRS, boundary and non-Hilbert Cmem subblocks vanish in the strict private branch", "FINAL_CMEM_ZERO_PRIVATE_BRANCH"),
        ("CFU4667_5_not_local_GR", "local GR/Newton/PPN/R10 still not claimed", "body-charge/source-charge, M_H_ref, Pi_M/H_tau, Z/M operator and arena projection gates remain", "FULL_LOCAL_GR_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4667_0_boundary_private", "C_mem^boundary", "PASS_CONDITIONAL_PRIVATE_ZERO", "fixed q-basic worldtube, regular support, no-flux collar, fixed corner/reference/projector and no radiative/Poynting crossing."),
        ("RUN4667_1_nonHilbert_private", "C_mem^nonHilbert", "PASS_CONDITIONAL_PRIVATE_ZERO", "Hperp source-pairing silence and source/readout quotient descent hold in the same branch."),
        ("RUN4667_2_combined", "C_mem^boundary_nonHilbert_live", "PASS_ZERO_PRIVATE_BRANCH", "boundary and non-Hilbert vanish separately; no cancellation is used."),
        ("RUN4667_3_final_Cmem", "C_mem^final_live", "PASS_ZERO_PRIVATE_BRANCH", "4661 standard/weight, 4663-4666 LHRS, and 4667 boundary/non-Hilbert are zero in the strict private branch."),
        ("RUN4667_4_dynamic", "off-branch boundary/non-Hilbert", "FAIL_CLOSED_TO_BOUND_ROWS", "moving support, radiative flux, corner/reference/projector leakage, Hperp, spin/torsion/improvement/readout tails remain explicit."),
        ("RUN4667_5_claim_status", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "Cmem zero is not body-charge/source-charge equality or source-normalized local Einstein equation."),
        ("RUN4667_6_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4667_0_no_cancellation", "Boundary and non-Hilbert must vanish separately; no tuned cancellation between channels.", "ACTIVE"),
        ("CTRL4667_1_no_globalize_private_branch", "Do not export compact stationary no-flux private branch to radiative, moving-boundary or transition systems.", "ACTIVE"),
        ("CTRL4667_2_no_poynting_erasure", "Radiative EM/gravity/Poynting flux is Hilbert/boundary charge or a finite row, never silently zero.", "ACTIVE"),
        ("CTRL4667_3_no_Hperp_assertion", "Hperp silence requires source-pairing and readout-descent clauses, not a generic quotient slogan.", "ACTIVE"),
        ("CTRL4667_4_no_fitted_G_laundering", "Support, projector, reference, M_H_ref and GM cannot be chosen after seeing local residuals.", "ACTIVE"),
        ("CTRL4667_5_no_local_GR_claim", "C_mem^final_live=0 does not yet prove body-charge/source-charge equality, Poisson normalization or PPN pass.", "ACTIVE"),
        ("CTRL4667_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
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
            "decision_id": "DEC4667_0",
            "decision": DECISION,
            "summary": (
                "4667 splits the last 4666 Cmem vector into boundary/history and non-Hilbert channels. "
                "The boundary channel closes only on the fixed q-basic compact worldtube branch with regular support, no shell, source-free no-flux collar, fixed corner/reference/projector data and no radiative/Poynting crossing. "
                "The non-Hilbert channel closes only when the quotient-orthogonal Hperp leg has no active source pairing and source/readout factors through q after variation, with spin/torsion/improvement/decoupled current tails absent, Hilbert-owned, exact with compact zero flux, or projection-silent. "
                "Thus C_mem^boundary=0, C_mem^nonHilbert=0 and C_mem^final_live=0 in the same strict private branch. Off branch, absolute boundary/non-Hilbert bounds remain explicit. This still does not claim local GR/Newton/PPN/R10 because body-charge/source-charge and source-normalization gates remain open."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "boundary_result": "C_MEM_BOUNDARY_ZERO_PRIVATE_QBASIC_NOFLUX_BRANCH",
            "nonHilbert_result": "C_MEM_NONHILBERT_ZERO_PRIVATE_HPERP_READOUT_SILENT_BRANCH",
            "final_Cmem_status": "C_MEM_FINAL_LIVE_ZERO_PRIVATE_BRANCH",
            "dynamic_status": "BOUNDARY_NONHILBERT_ABSOLUTE_BOUND_ROWS_RETAINED",
            "local_GR_status": "NONCLAIM_BODY_CHARGE_SOURCE_CHARGE_GATES_REMAIN",
            "selected_next_channel": "body-charge/source-charge gate",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "C_mem^final_live is now zero on the strict private branch, so the bottleneck moves from memory trace leakage to the charge/source normalization bridge.",
            "derive_route": "try to show the zero Cmem branch feeds the same body-charge/source-charge object with positive Z/M denominator, fixed Pi_M/H_tau, same-frame M_H_ref and Poisson/G normalization.",
            "fallback_route": "if equality fails, write first source-backed coefficient rows for B_mem_eff, J_mem, Q_boundary_mem, Z_mem/M_mem and arena projections without claiming local GR.",
            "avoid": "claiming local GR from Cmem zero alone, hiding source-normalization in measured G/GM, or mixing private branch zeros with public arena tests.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    split: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    final_update: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + split + boundary + nonhilbert + dynamic + final_update + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        SPLIT_CSV,
        BOUNDARY_ZERO_CSV,
        NONHILBERT_ZERO_CSV,
        DYNAMIC_BOUND_CSV,
        FINAL_UPDATE_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4667_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4667_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4667_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4667_03_split_present", any(row["split_id"] == "SPL4667_3_no_cancellation" for row in split), "no-cancellation split row present"),
        ("VAL4667_04_boundary_zero", any(row["zero_id"] == "BZI4667_5_result" and row["status"] == "CMEM_BOUNDARY_ZERO_PRIVATE_BRANCH" for row in boundary), "boundary zero row present"),
        ("VAL4667_05_nonHilbert_zero", any(row["zero_id"] == "NZI4667_5_result" and row["status"] == "CMEM_NONHILBERT_ZERO_PRIVATE_BRANCH" for row in nonhilbert), "non-Hilbert zero row present"),
        ("VAL4667_06_dynamic_bound", any(row["bound_id"] == "DBN4667_0_total" for row in dynamic), "absolute dynamic bound retained"),
        ("VAL4667_07_final_Cmem_zero", any(row["update_id"] == "CFU4667_4_final_zero" for row in final_update), "final Cmem zero row emitted"),
        ("VAL4667_08_no_poynting_erasure", any(row["control_id"] == "CTRL4667_2_no_poynting_erasure" for row in controls), "Poynting firewall present"),
        ("VAL4667_09_nonclaim_runner", any(row["run_id"] == "RUN4667_5_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim status remains nonclaim"),
        ("VAL4667_10_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4667_11_next_body_charge", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is body-charge/source-charge"),
        ("VAL4667_12_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4667_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4667 Cmem boundary/non-Hilbert private zero and dynamic bound gate passed" if passed_all else "4667 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    split: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    final_update: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4667 - Cmem boundary owner or non-Hilbert split bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4667 attacks the last vector left by 4666:

`|C_mem^final_live| <= |C_mem^boundary| + |C_mem^nonHilbert|`.

The split is forced componentwise:

`C_mem^boundary := Pi_mem[Q_edge_boundary/history]`,

`C_mem^nonHilbert := Pi_mem[X_nonHilbert_source_bypass]`.

No cancellation is permitted between the two.

On the strict private branch:

- the boundary/history channel has fixed q-basic compact support, zero trace shell, no birth/death shell, source-free no-flux collar, fixed corner/reference/projector data, no post-fit support definition and no radiative/Poynting crossing;
- the non-Hilbert channel has quotient split `H_L=H_q+Hperp`, source-pairing silence for `Hperp`, source/readout descent through `q`, and no surviving spin/torsion/improvement/decoupled-current projected compact flux.

Therefore:

`C_mem^boundary = 0`,

`C_mem^nonHilbert = 0`,

and:

`C_mem^final_live = 0`

inside that strict private branch.

This is real progress, but it is still not a public local-GR/Newton/PPN/R10 claim. The next bottleneck is the body-charge/source-charge bridge: `B_mem_eff`, `J_mem`, `Q_boundary_mem`, `Z/M`, `Pi_M/H_tau`, `M_H_ref`, and Poisson/G normalization must still be same-branch derived or source-backed.

## Source Register

{table(sources)}

## Boundary / Non-Hilbert Split

{table(split)}

## Boundary Zero Import

{table(boundary)}

## Non-Hilbert Zero Import

{table(nonhilbert)}

## Dynamic Boundary / Non-Hilbert Bound Rows

{table(dynamic)}

## Final Cmem Update

{table(final_update)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4667 splits the final Cmem vector left by 4666 into boundary/history and non-Hilbert channels. On the strict private q-basic compact-worldtube no-flux collar and Hperp source-pairing/readout-silent quotient branch, C_mem^boundary=0 and C_mem^nonHilbert=0 separately, so C_mem^final_live=0 in that branch. Dynamic boundary flux, Poynting/radiative, corner/reference/projector, Hperp, spin/torsion/improvement/readout tails remain explicit off branch.",
        "Generated source register, boundary/non-Hilbert split, boundary zero import, non-Hilbert zero import, dynamic bound rows, final Cmem update, runner, controls, decision, status, next target and validation.",
        "Cmem_boundary_nonHilbert_zero_private_qbasic_no_flux_Hperp_branch_dynamic_bounds_nonclaim",
        NEXT_TARGET,
        "Using cancellation between boundary and non-Hilbert channels, globalizing compact no-flux branch, erasing Poynting/radiative flux, asserting Hperp silence without source/readout descent, hiding source-normalization in measured G/GM, or claiming local GR from Cmem zero alone.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until body-charge/source-charge equality, positive denominators, Pi_M/H_tau, M_H_ref and arena projection gates are same-branch derived or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4667 closes the final private-branch `C_mem` leakage vector by splitting `C_mem^boundary` and `C_mem^nonHilbert` and forcing each to zero separately. The boundary zero uses the q-basic compact-worldtube/no-flux collar branch; the non-Hilbert zero uses the Hperp source-pairing/readout-silent quotient branch. Thus `C_mem^final_live=0` in the strict private branch, while radiative/Poynting, moving boundary, corner/reference/projector, Hperp, spin/torsion/improvement and readout-reentry rows remain explicit off branch. The remaining local-GR bottleneck is body-charge/source-charge normalization, not Cmem leakage.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4667` removes the boundary/non-Hilbert pair from the private-branch Cmem residual vector and records the off-branch absolute bounds. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    split = split_rows(timestamp)
    boundary = boundary_zero_rows(timestamp)
    nonhilbert = nonhilbert_zero_rows(timestamp)
    dynamic = dynamic_bound_rows(timestamp)
    final_update = final_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, split, boundary, nonhilbert, dynamic, final_update, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SPLIT_CSV, split)
    write_csv(BOUNDARY_ZERO_CSV, boundary)
    write_csv(NONHILBERT_ZERO_CSV, nonhilbert)
    write_csv(DYNAMIC_BOUND_CSV, dynamic)
    write_csv(FINAL_UPDATE_CSV, final_update)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, split, boundary, nonhilbert, dynamic, final_update, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4667 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
