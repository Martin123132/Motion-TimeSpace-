from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_RESIDUAL_SOURCE_NORM_AND_GREEN_BOUND_CERTIFICATE_2478"
CHECKPOINT_ID = "2478"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_RESIDUAL_GREEN_2478_SOURCE_REGISTER.csv",
    "residual_decomposition": OUT / "P8_Y5_RESIDUAL_GREEN_2478_RESIDUAL_DECOMPOSITION.csv",
    "green_certificate": OUT / "P8_Y5_RESIDUAL_GREEN_2478_GREEN_CERTIFICATE.csv",
    "cmetric_candidate": OUT / "P8_Y5_RESIDUAL_GREEN_2478_CMETRIC_CANDIDATE.csv",
    "blocker_ledger": OUT / "P8_Y5_RESIDUAL_GREEN_2478_BLOCKER_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_RESIDUAL_GREEN_2478_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_RESIDUAL_GREEN_2478_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_RESIDUAL_GREEN_2478_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_RESIDUAL_GREEN_2478_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2478_VALIDATION.csv",
}

COPY_TARGETS = {
    "cmetric_candidate": LOCAL_BOUNDS / "Cmetric_residual_Green_candidate_2478_NONCLAIM.csv",
    "blocker_ledger": LOCAL_BOUNDS / "Residual_source_norm_Green_blocker_2478_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2478_RESIDUAL_SECTOR_TO_EGK_NORM_MAP.csv",
}

SOURCES = [
    {
        "source_id": "SRC2478_00_2477_doc",
        "source_path": ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md",
        "needles": ["NEXT2477_0_selected", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "VAL2477_OVERALL"],
        "role": "handoff selecting C_res/C_Green certificate",
    },
    {
        "source_id": "SRC2478_01_2405_residual_basis",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["OPB2405_0_total_DeltaE_MTS", "DeltaE_boundary", "CG2405_4_local_GR_Newton"],
        "role": "residual operator basis for C_res",
    },
    {
        "source_id": "SRC2478_02_2473_EGK",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["E_GK_bound", "C_B*boundary_flux", "MISSING_COEFFICIENTS"],
        "role": "stress-bound norm components to map residuals onto",
    },
    {
        "source_id": "SRC2478_03_2466_source",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["J_M^nu = ell_J T_matter", "MISSING_PARENT_SCALE", "Do not define M_source by observed GM"],
        "role": "Hilbert source-normalization and fitted-GM guardrail",
    },
    {
        "source_id": "SRC2478_04_2477_validation",
        "source_path": OUT / "P8_Y5_BRR545_2477_VALIDATION.csv",
        "needles": ["VAL2477_OVERALL", "PASS"],
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


def residual_decomposition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "RES2478_0_definition",
            "symbol": "S_res",
            "formula": "S_res=(c^2/2)*(kappa0*J_shadow_00-DeltaE_MTS_00-DeltaE_boundary_00-Lambda*g_00)+delta_G_source",
            "bound_route": "decompose every term into a signed residual coefficient times a controlled norm",
            "candidate_bound_piece": "C_res*E_GK_bound",
            "status": "FORMAL_DECOMPOSITION_FROM_2477",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2478_1_DeltaE_MTS",
            "symbol": "DeltaE_MTS_00",
            "formula": "DeltaE_MTS=sum_i c_i O_i with sectors c_HD,c_aux,c_projector,c_memory,c_q_source",
            "bound_route": "||DeltaE_MTS_00|| <= C_HD*e_HD + C_aux*e_aux + C_proj*projector_leak + C_mem*source_tail + C_q*source_tail",
            "candidate_bound_piece": "part of C_res if each C_i and e_i is parent-sourced",
            "status": "BLOCKED_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2478_2_boundary",
            "symbol": "DeltaE_boundary_00",
            "formula": "boundary/reference/improvement metric stress",
            "bound_route": "||DeltaE_boundary_00|| <= C_boundary*boundary_flux",
            "candidate_bound_piece": "maps to 2473 boundary_flux only if C_boundary is signed",
            "status": "BLOCKED_BOUNDARY_CLASS",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2478_3_shadow",
            "symbol": "J_shadow_00",
            "formula": "non-Hilbert, post-readout, frame, species, or source-shadow residual",
            "bound_route": "||J_shadow_00|| <= C_shadow*source_tail + C_species*species_leak",
            "candidate_bound_piece": "must vanish for clean Hilbert route or remain WEP-bounded",
            "status": "BLOCKED_SOURCE_SHADOW",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2478_4_normalization",
            "symbol": "delta_G_source",
            "formula": "mismatch between kappa0/G_ref/Hilbert mass and local source charge",
            "bound_route": "|delta_G_source| <= C_norm*source_norm_gap, with source_norm_gap not orbital-G-fitted",
            "candidate_bound_piece": "separate normalization blocker unless ell_J/worldtube bridge closes",
            "status": "BLOCKED_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2478_5_Cres_formula",
            "symbol": "C_res",
            "formula": "C_res=(c^2/2)*(kappa0*C_shadow+C_MTS+C_boundary+C_Lambda)+C_norm in the declared norm",
            "bound_route": "valid only after every C_* has a source path, units, and no fitted-GM dependence",
            "candidate_bound_piece": "symbolic C_res only",
            "status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def green_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "green_id": "GRN2478_0_poisson_inverse",
            "domain_contract": "local exterior collar Omega with selected gauge, boundary conditions, and no zero mode",
            "formula": "nabla^2 deltaU=S_res; deltaU(x)=-(1/4*pi)*int_Omega S_res(y)/|x-y| d^3y + boundary/harmonic terms",
            "certificate": "standard Green representation gives a conditional inverse once Omega and boundary data are fixed",
            "missing_input": "OMEGA;BOUNDARY_CONDITION;HARMONIC_ZERO_MODE_CONTROL",
            "status": "PASS_CONDITIONAL_MATH_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "green_id": "GRN2478_1_sup_kernel_bound",
            "domain_contract": "bounded source support separated from observation by d_min>0 and volume V_eff",
            "formula": "||deltaU||_inf <= V_eff/(4*pi*d_min)*||S_res||_inf + ||boundary/harmonic||_inf",
            "certificate": "explicit pointwise kernel bound",
            "missing_input": "V_eff;d_min;boundary_harmonic_bound",
            "status": "DERIVED_FORMULA_NEEDS_GEOMETRY",
            "valid_for_claim": False,
        },
        {
            "green_id": "GRN2478_2_elliptic_norm_bound",
            "domain_contract": "regular bounded collar with Dirichlet/Neumann/falloff package and fixed gauge",
            "formula": "||deltaU||_H2(Omega) <= C_ell(Omega,BC)*||S_res||_L2(Omega)",
            "certificate": "elliptic estimate supplies C_Green=C_ell in normed form",
            "missing_input": "C_ell;gauge_certificate;domain_regularization",
            "status": "DERIVED_STANDARD_CERTIFICATE_SHAPE",
            "valid_for_claim": False,
        },
        {
            "green_id": "GRN2478_3_exterior_monopole_tail",
            "domain_contract": "spherical exterior after source/worldtube matching",
            "formula": "deltaU(r)=-deltaM_res/r + multipoles + boundary_hair",
            "certificate": "Newton tail follows from Poisson Green function, but deltaM_res must be parent-source-defined",
            "missing_input": "deltaM_res_not_orbital_GM;worldtube_surface_independence;multipole_bound",
            "status": "CONDITIONAL_NOT_SOURCE_NORMALIZED",
            "valid_for_claim": False,
        },
        {
            "green_id": "GRN2478_4_Cgreen_status",
            "domain_contract": "generic local arena",
            "formula": "C_Green can be a real coefficient only after choosing one of GRN2478_1/2/3 with sourced geometry and boundary data",
            "certificate": "Green theorem shape is derived; numeric coefficient is not acquired",
            "missing_input": "ARENA_DOMAIN_PACKAGE",
            "status": "C_GREEN_SYMBOLIC_ONLY",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def cmetric_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "CMET2478_0_formal_metric_bound",
            "relation": "||delta g_00||_obs <= C_metric*E_GK_bound",
            "coefficient": "C_metric=(2/c^2)*C_obs*C_Green*C_res",
            "available_now": "C_metric factorisation plus conditional Green formulas",
            "missing_now": "C_res numeric/source map; C_Green domain coefficient; C_obs arena projection; E_GK numeric bound",
            "status": "FORMAL_CANDIDATE_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CMET2478_1_sup_norm_variant",
            "relation": "||delta g_00||_inf <= (2/c^2)*C_obs*(V_eff/(4*pi*d_min))*C_res*E_GK_bound plus boundary",
            "coefficient": "C_metric_sup=(2/c^2)*C_obs*V_eff*C_res/(4*pi*d_min)",
            "available_now": "algebraic kernel coefficient shape",
            "missing_now": "V_eff,d_min,boundary_harmonic_bound,C_res,C_obs",
            "status": "GEOMETRY_SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CMET2478_2_H2_variant",
            "relation": "||delta g_00||_obs <= (2/c^2)*C_obs*C_ell*C_res*E_GK_bound",
            "coefficient": "C_metric_H2=(2/c^2)*C_obs*C_ell*C_res",
            "available_now": "standard elliptic-estimate coefficient shape",
            "missing_now": "C_ell,gauge/domain package,C_res,C_obs",
            "status": "ELLIPTIC_SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "blocker_id": "BLK2478_0_Cres_coefficients",
            "missing_object": "source-backed residual coefficients for C_res",
            "why_it_blocks": "The residual source can be decomposed, but DeltaE_MTS, boundary, shadow, and normalization coefficients are not bounded by E_GK_bound.",
            "next_action": "derive residual-sector-to-EGK norm map: C_HD,C_aux,C_proj,C_mem,C_q,C_boundary,C_shadow,C_norm",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2478_1_EGK_numeric",
            "missing_object": "numeric/source-backed E_GK_bound",
            "why_it_blocks": "2473 defines E_GK_bound symbolically with missing C_B,C_S,C_X,C_H,C_P.",
            "next_action": "keep all local bound rows nonclaim until parent signs or real bounds fix these coefficients",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2478_2_domain_geometry",
            "missing_object": "local collar domain package for C_Green",
            "why_it_blocks": "The Green theorem is standard only after gauge, boundary, harmonic mode, and domain geometry are declared.",
            "next_action": "after C_res, build arena-specific domain packages for R10/PPN/clocks/orbits",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2478_3_source_normalization",
            "missing_object": "ell_J/worldtube/source-charge normalization",
            "why_it_blocks": "delta_G_source cannot be zeroed by fitted orbital GM without circularity.",
            "next_action": "retain no-fitted-GM guardrail and source-normalization blocker",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLK2478_4_Cobs_Karena",
            "missing_object": "observable projection C_obs and arena kernels",
            "why_it_blocks": "R10, PPN, clock, orbit, and WEP observables project different pieces of the same metric residual.",
            "next_action": "do not build K_R10 until C_res/C_Green are at least conditionally sourced",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2478_0_Sres_decomposition",
            "claim": "Residual source S_res is decomposed into named operator/source pieces.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2478 writes the residual source pieces explicitly from 2477/2405.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_1_Green_shape",
            "claim": "Green-bound shapes exist for Poisson residuals.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2478 derives pointwise and elliptic estimate forms, but no geometry/domain constants are sourced.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_2_Cres",
            "claim": "C_res is numeric/source-backed.",
            "gate_status": "BLOCKED",
            "reason": "Residual coefficients are symbolic and not mapped to E_GK_bound.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_3_Cgreen",
            "claim": "C_Green is numeric/source-backed for a local arena.",
            "gate_status": "BLOCKED",
            "reason": "Domain/gauge/boundary constants are not supplied.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_4_Newton_local_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "Formal residual and Green bounds do not zero/bound every residual nor prove PPN spatial/second-order equations.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_5_R10",
            "claim": "R10 can be run as an MTS prediction.",
            "gate_status": "BLOCKED",
            "reason": "C_metric remains symbolic and K_R10 remains downstream.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2478_6_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "All shortcut routes remain explicit blockers or guardrails.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2478_0_gain",
            "decision": "Accept the residual/Green certificate as real structural progress.",
            "reason": "C_Green now has standard mathematical forms and C_res is decomposed into named source terms.",
            "effect": "The local branch is less foggy, but still nonclaim.",
        },
        {
            "decision_id": "DEC2478_1_priority",
            "decision": "Prioritize C_res over arena kernels.",
            "reason": "A perfect R10 geometry kernel cannot help if the residual source norm is not mapped to E_GK_bound.",
            "effect": "Next target moves to residual-sector coefficients.",
        },
        {
            "decision_id": "DEC2478_2_no_public_claim",
            "decision": "Do not update GitHub or public spine with local-test claims.",
            "reason": "The current win is internal derivation scaffolding, not an empirical pass.",
            "effect": "Private checkpoint only.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2478_0_selected",
            "selection_status": "selected",
            "target_file": "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md",
            "target_script": "scripts/Y5_R2FR_residual_sector_to_EGK_norm_map_or_coefficient_blocker_2479.py",
            "task": "derive or block the coefficient map from DeltaE_MTS, DeltaE_boundary, J_shadow, and delta_G_source into E_GK_bound, producing C_res or an explicit source-coefficient blocker",
            "acceptance_target": "C_HD,C_aux,C_proj,C_mem,C_q,C_boundary,C_shadow,C_norm rows with units, source paths, valid_for_claim=false unless fully sourced",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "cmetric_candidate": OUTPUTS["cmetric_candidate"],
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
                    "copy_id": f"COPY2478_{key}",
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

    add("VAL2478_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2478_01_Sres_decomposed",
        any(row["residual_id"] == "RES2478_5_Cres_formula" for row in data["residuals"]),
        "C_res symbolic formula row exists",
    )
    add(
        "VAL2478_02_Green_shapes",
        any(row["green_id"] == "GRN2478_1_sup_kernel_bound" for row in data["greens"]) and any(row["green_id"] == "GRN2478_2_elliptic_norm_bound" for row in data["greens"]),
        "pointwise and elliptic Green-bound shapes exist",
    )
    add(
        "VAL2478_03_candidates_nonclaim",
        all(row["valid_for_claim"] is False for row in data["candidates"]),
        "all C_metric candidate rows remain nonclaim",
    )
    add(
        "VAL2478_04_blockers_present",
        len(data["blockers"]) >= 5 and all(row["valid_for_claim"] is False for row in data["blockers"]),
        "blockers cover C_res, E_GK, C_Green domain, normalization and observable projection",
    )
    add(
        "VAL2478_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "no gate allows Newton/local-GR/R10 claim",
    )
    add(
        "VAL2478_06_next_target_written",
        any(row["route_id"] == "NEXT2478_0_selected" for row in data["next"]),
        "2479 residual-sector-to-EGK map selected",
    )
    add(
        "VAL2478_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )
    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2478*", "*P8_Y5_RESIDUAL_GREEN_2478*", "*JR2478*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2478_08_no_formalization_artifacts", not formalization_artifacts, "no 2478 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2478_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2478_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2478_OVERALL",
        overall,
        "2478 derives conditional Green-bound forms, decomposes C_res, keeps C_metric nonclaim, and selects residual-sector-to-EGK coefficients next",
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
        "# 2478 Y5 R2FR Residual-source Norm And Green-bound Certificate",
        "",
        "**Status:** conditional certificate, not a claim. The Green-bound side is now mathematically shaped, and `S_res` is decomposed into source/operator pieces, but `C_res`, `C_Green`, `C_obs`, and `E_GK_bound` remain nonnumeric and unsourced.",
        "",
        "**Main result:** the bridge is no longer fog. `S_res` must be bounded by `C_res E_GK_bound`, and the Poisson residual has standard Green bounds such as `||deltaU||_inf <= V_eff/(4*pi*d_min)||S_res||_inf + boundary` or `||deltaU||_H2 <= C_ell||S_res||_L2`. These are real mathematical shapes, but still not live local-test inputs.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Residual Decomposition",
        markdown_table(data["residuals"], ["residual_id", "symbol", "formula", "bound_route", "candidate_bound_piece", "status", "valid_for_claim"]),
        "",
        "## Green Certificate",
        markdown_table(data["greens"], ["green_id", "domain_contract", "formula", "certificate", "missing_input", "status", "valid_for_claim"]),
        "",
        "## Cmetric Candidate",
        markdown_table(data["candidates"], ["candidate_id", "relation", "coefficient", "available_now", "missing_now", "status", "valid_for_claim"]),
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
        "residuals": residual_decomposition_rows(),
        "greens": green_certificate_rows(),
        "candidates": cmetric_candidate_rows(),
        "blockers": blocker_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["residual_decomposition"], data["residuals"])
    write_csv(OUTPUTS["green_certificate"], data["greens"])
    write_csv(OUTPUTS["cmetric_candidate"], data["candidates"])
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
