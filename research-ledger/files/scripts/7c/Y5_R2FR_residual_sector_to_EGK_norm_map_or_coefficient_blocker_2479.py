from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_RESIDUAL_SECTOR_TO_EGK_NORM_MAP_2479"
CHECKPOINT_ID = "2479"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_SOURCE_REGISTER.csv",
    "coefficient_map": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_COEFFICIENT_MAP.csv",
    "egk_basis_audit": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_EGK_BASIS_AUDIT.csv",
    "cres_status": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_CRES_STATUS.csv",
    "blocker_ledger": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_BLOCKER_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_RESIDUAL_EGK_MAP_2479_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2479_VALIDATION.csv",
}

COPY_TARGETS = {
    "coefficient_map": LOCAL_BOUNDS / "Residual_sector_to_EGK_norm_map_2479_NONCLAIM.csv",
    "blocker_ledger": LOCAL_BOUNDS / "Local_residual_norm_extension_blocker_2479_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2479_EXTENDED_LOCAL_RESIDUAL_NORM_OR_ZERO_CERTIFICATES.csv",
}

SOURCES = [
    {
        "source_id": "SRC2479_00_2478_doc",
        "source_path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": ["NEXT2478_0_selected", "C_HD,C_aux,C_proj,C_mem,C_q,C_boundary,C_shadow,C_norm", "VAL2478_OVERALL"],
        "role": "handoff selecting residual-sector coefficient map",
    },
    {
        "source_id": "SRC2479_01_2405_residual_basis",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["OPB2405_0_total_DeltaE_MTS", "OPB2405_4_c_boundary_operator", "REF2405_2_conservation_as_zero"],
        "role": "operator-residual owners and anti-conservation shortcut",
    },
    {
        "source_id": "SRC2479_02_2406_sector_variation",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_6_verdict", "OBI2406_0_total_DeltaE_MTS", "VAL2406_02_sector_coefficients_present"],
        "role": "sector-by-sector local-scaling scoreboard",
    },
    {
        "source_id": "SRC2479_03_2473_EGK_basis",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["RPAR2473_0_energy_norm", "C_B*boundary_flux", "MISSING_COEFFICIENTS"],
        "role": "current E_GK_bound basis and missing coefficients",
    },
    {
        "source_id": "SRC2479_04_2466_source_norm",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["MISSING_PARENT_SCALE", "Do not define M_source by observed GM", "WT2466_2_surface_independence"],
        "role": "source normalization and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2479_05_2478_validation",
        "source_path": OUT / "P8_Y5_BRR545_2478_VALIDATION.csv",
        "needles": ["VAL2478_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic path
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def coefficient_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coefficient_id": "COEF2479_C_HD",
            "coefficient": "C_HD",
            "residual_sector": "higher-derivative curvature",
            "source_residual": "c_HD O_HD_00",
            "current_EGK_component": "none_declared",
            "proposed_extended_slot": "e_HD_curvature_operator",
            "map_attempt": "||c_HD O_HD_00|| <= C_HD*e_HD_curvature_operator",
            "units_status": "requires operator-norm units for O_HD and source units for S_res",
            "source_status": "MISSING_PARENT_GRAMMAR_OR_EMPIRICAL_COEFFICIENT_BOUND",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_aux",
            "coefficient": "C_aux",
            "residual_sector": "constraint/auxiliary metric stress",
            "source_residual": "lambda_C delta C/delta g + lambda_R delta R_AB/delta g + auxiliary elimination tails",
            "current_EGK_component": "negative_mode_defect_partial",
            "proposed_extended_slot": "e_aux_constraint_stress",
            "map_attempt": "||aux stress|| <= C_aux*(negative_mode_defect + e_aux_constraint_stress)",
            "units_status": "requires parent auxiliary stress normalization",
            "source_status": "MISSING_ZERO_STRESS_THEOREM_OR_AUX_TAIL_BOUND",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_proj",
            "coefficient": "C_proj",
            "residual_sector": "projector/domain/readout operator",
            "source_residual": "E_projector(Pi_M), [d,Pi_M]J_H, q-domain tail",
            "current_EGK_component": "projector_leak",
            "proposed_extended_slot": "none_if_projector_leak_is_parent-defined",
            "map_attempt": "||projector residual|| <= C_proj*projector_leak",
            "units_status": "plausible if projector_leak norm is defined in same frame",
            "source_status": "MISSING_PROJECTOR_DESCENT_AND_NORM_SOURCE",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_mem",
            "coefficient": "C_mem",
            "residual_sector": "memory/coframe/current-chain residual",
            "source_residual": "DeltaE_mem(theta,Q_tau,C_tau), preferred-frame current",
            "current_EGK_component": "source_tail_partial",
            "proposed_extended_slot": "e_tau_clock_frame_leak",
            "map_attempt": "||memory/frame residual|| <= C_mem*(source_tail + e_tau_clock_frame_leak)",
            "units_status": "requires tau/coframe residual norm and clock exchange convention",
            "source_status": "MISSING_CURRENT_CHAIN_VERTICAL_SILENCE_OR_TAU_BOUND",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_q",
            "coefficient": "C_q",
            "residual_sector": "q/reciprocal source-vector tails",
            "source_residual": "B_qW C_Weyl + B_qRic R_Ricci + C_qT T_H + Q_q[body] + Pi_q + tail_q",
            "current_EGK_component": "source_tail;topology_hair_amplitude;projector_leak_partial",
            "proposed_extended_slot": "e_q_weyl_spurion",
            "map_attempt": "||q residual|| <= C_q*(source_tail + topology_hair_amplitude + projector_leak + e_q_weyl_spurion)",
            "units_status": "requires q-sector basis and Weyl/Ricci coefficient normalization",
            "source_status": "MISSING_Q_FIRSTCLASS_NO_SPURION_OR_BQ_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_boundary",
            "coefficient": "C_boundary",
            "residual_sector": "boundary/reference/improvement metric stress",
            "source_residual": "DeltaE_boundary_00, delta Q_ref/delta g",
            "current_EGK_component": "boundary_flux",
            "proposed_extended_slot": "none_if_boundary_flux_is parent-defined",
            "map_attempt": "||DeltaE_boundary_00|| <= C_boundary*boundary_flux",
            "units_status": "plausible if local collar boundary flux norm is fixed",
            "source_status": "MISSING_BOUNDARY_CLASS_AND_REFERENCE_STRESS_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_shadow",
            "coefficient": "C_shadow",
            "residual_sector": "source-shadow and non-Hilbert source",
            "source_residual": "J_shadow_00",
            "current_EGK_component": "source_tail_partial",
            "proposed_extended_slot": "e_species_shadow_or_zero",
            "map_attempt": "||J_shadow_00|| <= C_shadow*(source_tail + e_species_shadow_or_zero)",
            "units_status": "requires same-frame Hilbert/current source units",
            "source_status": "MISSING_SOURCE_SHADOW_ZERO_OR_WEP_BOUND",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_norm",
            "coefficient": "C_norm",
            "residual_sector": "source normalization gap",
            "source_residual": "delta_G_source",
            "current_EGK_component": "none_declared",
            "proposed_extended_slot": "e_source_norm_gap",
            "map_attempt": "|delta_G_source| <= C_norm*e_source_norm_gap",
            "units_status": "requires ell_J, kappa0/G_ref and worldtube charge units in one frame",
            "source_status": "MISSING_ELLJ_WORLDTUBE_SURFACE_INDEPENDENCE_NO_FITTED_GM",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2479_C_Lambda",
            "coefficient": "C_Lambda",
            "residual_sector": "local cosmological/background subtraction",
            "source_residual": "Lambda*g_00 local term in S_res",
            "current_EGK_component": "none_declared",
            "proposed_extended_slot": "e_background_subtraction",
            "map_attempt": "||Lambda g_00|| <= C_Lambda*e_background_subtraction or subtract as fixed background",
            "units_status": "requires declared local subtraction convention",
            "source_status": "MISSING_BACKGROUND_SUBTRACTION_CERTIFICATE",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def egk_basis_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "basis_id": "BAS2479_0_current_EGK",
            "basis_object": "E_GK_bound",
            "basis_formula": "C_B*boundary_flux + C_S*source_tail + C_X*negative_mode_defect + C_H*topology_hair_amplitude + C_P*projector_leak",
            "covers": "boundary_flux;source_tail;negative_mode_defect;topology_hair_amplitude;projector_leak",
            "missing_slots": "e_HD_curvature_operator;e_aux_constraint_stress;e_tau_clock_frame_leak;e_q_weyl_spurion;e_species_shadow_or_zero;e_source_norm_gap;e_background_subtraction",
            "status": "INSUFFICIENT_FOR_FULL_SRES",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BAS2479_1_minimal_extension",
            "basis_object": "E_local_res",
            "basis_formula": "E_GK_bound + E_HD + E_aux + E_tau + E_qspur + E_shadow + E_norm + E_bg",
            "covers": "all 2479 residual slots if coefficients are parent-sourced",
            "missing_slots": "all new slot coefficients and zero/finite source paths",
            "status": "PROPOSED_NONCLAIM_EXTENSION",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BAS2479_2_zero_certificate_alternative",
            "basis_object": "zero theorem route",
            "basis_formula": "E_HD=E_aux=E_tau=E_qspur=E_shadow=E_norm=E_bg=0 by parent certificates",
            "covers": "cleanest local-GR route if proved",
            "missing_slots": "parent zero certificates for every non-EGK residual",
            "status": "PREFERRED_IF_DERIVABLE_BUT_UNSIGNED",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def cres_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "cres_id": "CRES2479_0_current_formula",
            "formula": "C_res=(c^2/2)*(kappa0*C_shadow+C_HD+C_aux+C_proj+C_mem+C_q+C_boundary+C_Lambda)+C_norm",
            "basis": "declared residual norm after splitting S_res",
            "status": "SYMBOLIC_ONLY",
            "why": "no coefficient row has source-backed units and parent provenance",
            "valid_for_claim": False,
        },
        {
            "cres_id": "CRES2479_1_EGK_only_result",
            "formula": "C_res*E_GK_bound cannot cover all S_res terms unless missing slots are zero",
            "basis": "compare coefficient map to 2473 E_GK_basis",
            "status": "EGK_ONLY_FAILS_AS_FULL_PROOF",
            "why": "C_HD, C_norm, C_Lambda and parts of C_aux/C_mem/C_shadow are outside current E_GK_bound",
            "valid_for_claim": False,
        },
        {
            "cres_id": "CRES2479_2_extended_result",
            "formula": "C_res_ext*E_local_res could cover all S_res terms if every new slot is sourced",
            "basis": "BAS2479_1_minimal_extension",
            "status": "EXTENSION_ROUTE_OPEN_NONCLAIM",
            "why": "the extension is honest but adds variables that must be derived or bounded",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "blocker_id": "BLK2479_0_EGK_insufficient",
            "missing_object": "full residual norm basis",
            "why_it_blocks": "Current E_GK_bound does not contain every S_res component needed for C_res.",
            "next_action": "either prove missing slots zero or promote an extended E_local_res norm with source paths",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2479_1_coefficient_sources",
            "missing_object": "C_HD,C_aux,C_proj,C_mem,C_q,C_boundary,C_shadow,C_norm source rows",
            "why_it_blocks": "All coefficient maps are symbolic; none have units/source provenance good enough for local tests.",
            "next_action": "attack the most derivable zero certificates before adding empirical coefficients",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2479_2_source_normalization",
            "missing_object": "ell_J and worldtube charge normalization",
            "why_it_blocks": "C_norm cannot be bounded by fitted GM without circularity.",
            "next_action": "retain Hilbert/worldtube source bridge as a parallel hard gate",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2479_3_background_subtraction",
            "missing_object": "local Lambda/background subtraction certificate",
            "why_it_blocks": "Even tiny background terms need an explicit subtraction convention in a proof ledger.",
            "next_action": "write background-subtraction row or show it is absorbed into the local reference solution",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2479_4_claim_discipline",
            "missing_object": "numeric C_res and E_local_res",
            "why_it_blocks": "Without numeric/source-backed residual coefficients, C_metric remains formal and R10/PPN cannot run as MTS predictions.",
            "next_action": "select zero-certificate vs extended-norm route for 2480",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2479_0_map_rows",
            "claim": "All requested C_* coefficient rows exist.",
            "gate_status": "PASS_STRUCTURE_NONCLAIM",
            "reason": "2479 writes C_HD,C_aux,C_proj,C_mem,C_q,C_boundary,C_shadow,C_norm plus C_Lambda.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2479_1_EGK_full_cover",
            "claim": "Current E_GK_bound covers all residual source terms.",
            "gate_status": "BLOCKED",
            "reason": "E_GK_bound lacks higher-derivative, normalization, background, species-shadow and some auxiliary/frame slots.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2479_2_Cres_numeric",
            "claim": "C_res is numeric/source-backed.",
            "gate_status": "BLOCKED",
            "reason": "Coefficient rows have no parent-signed numeric values or units.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2479_3_Cmetric",
            "claim": "C_metric can be used in local tests.",
            "gate_status": "BLOCKED",
            "reason": "C_res and E_local_res remain symbolic and C_Green/C_obs are also unresolved.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2479_4_local_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "Residual norm map exposes missing zero certificates rather than proving residual silence.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2479_5_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "Shortcut routes remain explicitly blocked.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2479_0_gain",
            "decision": "Accept the coefficient-map audit as progress.",
            "reason": "It proves the current E_GK_bound denominator is not broad enough for full S_res unless extra zeros are derived.",
            "effect": "The next route is sharper: zero certificates or explicit norm extension.",
        },
        {
            "decision_id": "DEC2479_1_prefer_zero_first",
            "decision": "Try zero certificates before adding many new empirical slots.",
            "reason": "A cleaner GR/Newton reduction should remove residual sectors, not merely fit a larger norm vector.",
            "effect": "2480 should attempt zero certificates for the non-EGK slots first.",
        },
        {
            "decision_id": "DEC2479_2_keep_private",
            "decision": "Keep this private and nonclaim.",
            "reason": "The result is a blocker map, not a local-test pass.",
            "effect": "No GitHub/public action.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2479_0_selected",
            "selection_status": "selected",
            "target_file": "2480-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-norm-vector.md",
            "target_script": "scripts/Y5_R2FR_non_EGK_residual_zero_certificates_or_extended_norm_vector_2480.py",
            "task": "attempt parent zero certificates for e_HD,e_aux,e_tau,e_qspur,e_shadow,e_norm,e_bg; if any fail, define an extended E_local_res norm vector without claiming local GR",
            "acceptance_target": "zero/retain decision for every missing slot, extended norm vector if needed, C_res remains nonclaim unless all slots are zero or sourced",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "coefficient_map": OUTPUTS["coefficient_map"],
        "blocker_ledger": OUTPUTS["blocker_ledger"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2479_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    required_coefficients = {"C_HD", "C_aux", "C_proj", "C_mem", "C_q", "C_boundary", "C_shadow", "C_norm"}
    found_coefficients = {row["coefficient"] for row in data["coefficients"]}

    add("VAL2479_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add("VAL2479_01_required_coefficients", required_coefficients <= found_coefficients, "all requested C_* coefficient rows exist", ";".join(sorted(found_coefficients)))
    add("VAL2479_02_all_coefficients_nonclaim", all(row["valid_for_claim"] is False for row in data["coefficients"]), "all coefficient rows remain nonclaim")
    add(
        "VAL2479_03_EGK_insufficiency_recorded",
        any(row["basis_id"] == "BAS2479_0_current_EGK" and row["status"] == "INSUFFICIENT_FOR_FULL_SRES" for row in data["basis"]),
        "current E_GK insufficiency is explicitly recorded",
    )
    add(
        "VAL2479_04_Cres_blocked",
        any(row["cres_id"] == "CRES2479_1_EGK_only_result" and row["status"] == "EGK_ONLY_FAILS_AS_FULL_PROOF" for row in data["cres"]),
        "C_res cannot be closed with current E_GK only",
    )
    add("VAL2479_05_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2479_06_next_target_written",
        any(row["route_id"] == "NEXT2479_0_selected" for row in data["next"]),
        "2480 zero-certificate or extended-norm route selected",
    )
    add("VAL2479_07_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2479*", "*P8_Y5_RESIDUAL_EGK_MAP_2479*", "*JR2479*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2479_08_no_formalization_artifacts", not formalization_artifacts, "no 2479 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2479_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2479_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2479_OVERALL",
        overall,
        "2479 maps residual-sector coefficients to the current E_GK basis, proves the basis is insufficient for full S_res, and selects zero certificates or extended norm next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2479 Y5 R2FR Residual-sector To EGK Norm Map Or Coefficient Blocker",
        "",
        "**Status:** coefficient map written, but no `C_res` claim. The current `E_GK_bound` basis covers some residual channels, but it does not cover the full `S_res` source unless several non-EGK slots are proved zero or an extended residual norm is introduced.",
        "",
        "**Main result:** `E_GK_bound` is not wrong; it is too narrow for the full local weak-field residual source. Boundary, projector, source-tail, topology and negative-mode pieces have homes, but higher-derivative curvature, source-normalization, background subtraction, species-shadow and some auxiliary/frame terms still need zero certificates or new norm slots.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Coefficient Map",
        markdown_table(data["coefficients"], ["coefficient_id", "coefficient", "residual_sector", "source_residual", "current_EGK_component", "proposed_extended_slot", "map_attempt", "units_status", "source_status", "valid_for_claim"]),
        "",
        "## EGK Basis Audit",
        markdown_table(data["basis"], ["basis_id", "basis_object", "basis_formula", "covers", "missing_slots", "status", "valid_for_claim"]),
        "",
        "## C_res Status",
        markdown_table(data["cres"], ["cres_id", "formula", "basis", "status", "why", "valid_for_claim"]),
        "",
        "## Blocker Ledger",
        markdown_table(data["blockers"], ["blocker_id", "missing_object", "why_it_blocks", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "coefficients": coefficient_map_rows(),
        "basis": egk_basis_audit_rows(),
        "cres": cres_status_rows(),
        "blockers": blocker_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["coefficient_map"], data["coefficients"])
    write_csv(OUTPUTS["egk_basis_audit"], data["basis"])
    write_csv(OUTPUTS["cres_status"], data["cres"])
    write_csv(OUTPUTS["blocker_ledger"], data["blockers"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
