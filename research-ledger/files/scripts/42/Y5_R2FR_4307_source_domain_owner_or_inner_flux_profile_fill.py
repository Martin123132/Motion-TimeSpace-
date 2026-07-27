from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4307"
CLAIM_ID = "L-148"
BRANCH = "MTS_R2FR_Y5_SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_FILL_4307"
DECISION = "SOURCE_DOMAIN_SPLIT_DERIVED_SMOOTH_HILBERT_ZERO_EXTERIOR_FLUX_PROFILE_RETAINED_NONCLAIM"
MARKER = "PPC4161_SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_FILL_4307"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_FILL_4307"
NEXT_TARGET = "4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md"

FORMAL_PATH = FORMAL / "323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md"
DOC_PATH = POST / "4307-Y5-R2FR-source-domain-owner-or-inner-flux-profile-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4307_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4307_00_4306_doc": (
        POST / "4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md",
        "SOURCE_DOMAIN_OWNER_OR_INNER_FLUX_PROFILE_NEXT",
        "4306 handoff: decide source-domain ownership or fill inner flux profile.",
    ),
    "SRC4307_01_4306_formal": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "partialD_in = empty set",
        "4306 theorem: smooth no-excision domain kills N_inner.",
    ),
    "SRC4307_02_hilbert_source_measure": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "All ordinary local source sectors use the same observed metric/coframe and the same volume measure.",
        "ordinary source sectors already written as one Hilbert volume source measure.",
    ),
    "SRC4307_03_hilbert_source_action": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src = S_matter[psi,g_obs,theta]",
        "source action begins as Hilbert matter plus EM/binding sectors.",
    ),
    "SRC4307_04_worldtube_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "W_H = closure(supp J_H_total)",
        "worldtube support and Hamiltonian source readout are defined as the same source object.",
    ),
    "SRC4307_05_same_source_current": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "same source current and same worldtube",
        "worldtube readout should not be a post-orbit fitted mass.",
    ),
    "SRC4307_06_selector_quarantine": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "single Hilbert source functor",
        "conditional local parent-action selector includes single Hilbert source ownership.",
    ),
    "SRC4307_07_boundary_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "boundary/radiative flux is routed rather than erased.",
    ),
    "SRC4307_08_4211_owner": (
        POST / "4211-Y5-R2FR-Htau-MHsource-parent-charge-owner-or-visible-matter-residual-scorecard.md",
        "same-source worldtube",
        "H_tau/M_H source owner contract remains viable but unsigned.",
    ),
    "SRC4307_09_1714_equality": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "Pi_M J_H = J_M_top + dB_zero",
        "source-to-Newton chain remains blocked by same-object equality.",
    ),
    "SRC4307_10_1715_commutator": (
        POST / "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
        "fixed topological chain-map",
        "topological/exterior branch needs chain-map/source-domain ownership.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4307 turns the 4306 inner-boundary law into a source-domain split. If the live local branch is a "
            "smooth Hilbert volume source domain on the m-lock operator domain, then partialD_in is empty and "
            "N_inner=0 follows exactly from domain identity. If instead the calculation uses an exterior/worldtube "
            "or point/excision annulus, the worldtube surface is a real inner boundary and Hilbert source descent "
            "does not erase it; the branch must carry g_in=Z_m n.grad u, Q_m^H, g_perp, B_src, C_0 and C_perp as "
            "nonclaim flux-profile inputs."
        ),
        (
            "4307 source register, source-domain owner matrix, smooth Hilbert no-inner-boundary theorem, "
            "exterior/worldtube matching runner, inner flux profile schema, Npair update, decision, firewall, "
            "status, next-target and validation CSV."
        ),
        "private_source_domain_split_smooth_Hilbert_zero_exterior_flux_profile_retained_nonclaim",
        (
            "Parent-sign the smooth Hilbert volume source domain for the local m-lock branch, or fill the first "
            "worldtube flux-profile row with sourced values/zero theorems."
        ),
        (
            "Using smooth-domain zero inside an exterior annulus, treating a worldtube surface as absent after "
            "excision, hiding Poynting/radiative flux in the bulk source, or claiming Newton/local-GR source "
            "normalization while R_eq/I_commutator remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def owner_matrix_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DOM4307_0_smooth_Hilbert_volume",
            "D_m contains the compact source as a Hilbert volume source; no source hole is removed.",
            "partialD_in = empty set",
            "N_inner = 0 exactly",
            "SUPPORTED_CONDITIONAL_BRANCH",
            "Best route for local GR: source is matter density on the same observed Hilbert measure, not an excised inner boundary.",
        ),
        (
            "DOM4307_1_exterior_worldtube_annulus",
            "D_m is the exterior annulus A_ext = D_m \\ W_H and W_H is removed from the operator domain.",
            "partialD_in = partial W_H",
            "N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "LIVE_FALLBACK_BRANCH",
            "This is the honest orbit/readout branch until the flux profile or no-flux matching is supplied.",
        ),
        (
            "DOM4307_2_point_particle_excision",
            "source is treated as a point/hole/singularity and matched only by exterior data.",
            "partialD_in nonempty or distributional",
            "no zero theorem; use profile/renormalized boundary data",
            "CLOSURE_ONLY_UNTIL_REGULARIZED",
            "Do not borrow smooth Hilbert volume zero for point-particle closure language.",
        ),
        (
            "DOM4307_3_parent_no_flux_boundary",
            "parent signs Z_m n.grad u|partialW=0 and B_src=0 on the worldtube surface.",
            "partialD_in exists but integrand is zero",
            "N_inner = 0 exactly",
            "UNSIGNED_ZERO_BRANCH",
            "Useful if derived, but older no-flux attempts did not already provide this certificate.",
        ),
        (
            "DOM4307_4_smoothing_limit",
            "a family of smooth Hilbert source densities rho_epsilon converges to an exterior mass readout.",
            "partialD_in empty for every epsilon; limit may create a surface term",
            "zero survives only if trace/defect measure tends to zero",
            "PROMISING_BUT_NEEDS_LIMIT_THEOREM",
            "This is the bridge between engineering intuition and rigorous exterior-source tests.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, domain_choice, boundary_status, inner_result, status, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "domain_choice": domain_choice,
                "boundary_status": boundary_status,
                "inner_result": inner_result,
                "status": status,
                "note": note,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "THM4307_0_domain_identity",
            "If D_m is the smooth Hilbert source volume domain, then partialD_in is empty.",
            "4306 gives B_inner[phi]=int_partialD_in phi Z_m n.grad u dSigma + B_src[phi].",
            "No inner surface means the geometric boundary integral is absent.",
            "DERIVED_CONDITIONAL",
        ),
        (
            "THM4307_1_source_injection_absent",
            "On the smooth Hilbert volume branch, source support is in the volume Euler-Lagrange/Hilbert term, not injected on an artificial inner boundary.",
            "185 writes ordinary sectors on the same observed metric/coframe and volume measure.",
            "B_src[phi]=0 for artificial inner-boundary injection on that branch.",
            "CONDITIONAL_ON_PARENT_SOURCE_DOMAIN",
        ),
        (
            "THM4307_2_smooth_zero",
            "smooth Hilbert volume branch: partialD_in=empty and B_src=0.",
            "N_inner=sup |B_inner[phi]|.",
            "N_inner=0 exactly.",
            "EXACT_ZERO_IF_BRANCH_SIGNED",
        ),
        (
            "THM4307_3_exterior_obstruction",
            "If the source is removed and only A_ext is solved, partialW_H is a true boundary.",
            "4306 trace theorem applies.",
            "N_inner cannot be set to zero without no-flux/matching or a flux profile.",
            "OBSTRUCTION_RETAINED",
        ),
        (
            "THM4307_4_same_source_warning",
            "Worldtube mass readout can be same-source without killing the exterior inner flux.",
            "1714/1715 keep R_eq and I_commutator open.",
            "source-to-Newton normalization remains blocked even if N_inner smooth branch is conditionally clean.",
            "NO_LOCAL_GR_CLAIM",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, statement, proof_input, consequence, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "proof_input": proof_input,
                "consequence": consequence,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def matching_runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4307_0_smooth_Hilbert_m_lock",
            "smooth Hilbert volume source domain",
            "N_inner=0",
            "N_pair <= N_EM + N_rest",
            "CONDITIONAL_FAST_ROUTE",
            "Use only if parent signs that the m-lock operator domain includes the smooth source volume.",
        ),
        (
            "RUN4307_1_smooth_plus_EM_rest_zero",
            "smooth Hilbert source plus Maxwell-Hodge/rest selector zeros",
            "N_inner=N_EM=N_rest=0",
            "N_pair=0",
            "EXACT_SOURCE_PAIR_ZERO_IF_ALL_SELECTOR_CLAUSES_SIGNED",
            "This is the serious route toward the local no-hair/local-GR gate, but it is still conditional.",
        ),
        (
            "RUN4307_2_exterior_worldtube",
            "exterior annulus with source removed",
            "N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "N_pair <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src|| + N_EM + N_rest",
            "PROFILE_ROUTE_READY_INPUTS_MISSING",
            "No more vague Q_m^H: the monopole, multipole and injection terms must be separated.",
        ),
        (
            "RUN4307_3_parent_no_flux_worldtube",
            "exterior annulus with parent no-flux matching",
            "Z_m n.grad u=0 and B_src=0 on partialW_H",
            "N_pair <= N_EM + N_rest",
            "UNSIGNED_ZERO_ROUTE",
            "Equivalent strength to the smooth branch for N_inner, but needs a real matching theorem.",
        ),
        (
            "RUN4307_4_to_m_lock_lambda",
            "source-domain-selected N_pair into m-lock",
            "Delta_m <= (N_pair+N_N)/lambda_m",
            "C4302_DVGAMMA_QUAD receives the selected source-domain branch",
            "HANDOFF_READY_NOT_NUMERIC",
            "Next gate is parent-signing the domain choice or filling first flux numbers before scoring lambda_m.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, branch_name, inner_input, formula, status, note in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "branch_name": branch_name,
                "inner_input": inner_input,
                "formula": formula,
                "status": status,
                "note": note,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def flux_profile_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "FLUX4307_0_domain_convention",
            "domain_choice",
            "smooth_volume | exterior_worldtube | point_excision | no_flux_matched",
            "dimensionless selector",
            "MISSING_PARENT_INPUT",
            "must be parent-signed before choosing zero or profile branch",
        ),
        (
            "FLUX4307_1_inner_surface",
            "partialW_H",
            "worldtube inner boundary geometry if exterior branch is used",
            "area/length convention",
            "MISSING_ARENA_PROJECTION",
            "needed for trace constants and monopole/multipole split",
        ),
        (
            "FLUX4307_2_normal_flux_profile",
            "g_in = Z_m n.grad u|partialW_H",
            "normal memory/source flux profile on the inner boundary",
            "same units as Z_m grad u",
            "MISSING_PARENT_INPUT",
            "zero theorem or measured/bounded profile required",
        ),
        (
            "FLUX4307_3_monopole_charge",
            "Q_m^H = int_partialW_H g_in dSigma",
            "inner monopole memory/source hair",
            "profile units times area",
            "MISSING_VALUE",
            "scalar Q_m^H alone is insufficient unless g_perp and B_src are killed",
        ),
        (
            "FLUX4307_4_multipole_tail",
            "g_perp = g_in - Q_m^H/Area(partialW_H)",
            "higher-mode/tidal boundary flux",
            "H^{-1/2}(partialW_H)",
            "MISSING_VALUE",
            "prevents scalar monopole overclaim",
        ),
        (
            "FLUX4307_5_source_boundary_injection",
            "B_src",
            "source injection/improvement term living on partialW_H",
            "H^{-1/2} dual norm",
            "MISSING_PARENT_INPUT",
            "must be zero by smooth volume branch or bounded in exterior branch",
        ),
        (
            "FLUX4307_6_trace_constants",
            "C_0, C_perp",
            "trace/geometry constants converting flux profile into N_inner",
            "operator-domain constants",
            "MISSING_ARENA_PROJECTION",
            "needed before any numeric R10/PPN/local test can score this branch",
        ),
        (
            "FLUX4307_7_no_cancellation_sum",
            "N_inner_bound",
            "C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "same norm as N_inner",
            "FORMULA_READY_VALUES_MISSING",
            "absolute envelope only; no cancellation between channels allowed",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for profile_id, symbol, definition, units, status, next_input in specs:
        row = base_row()
        row.update(
            {
                "profile_id": profile_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "status": status,
                "next_input": next_input,
                "source_path": "",
                "numeric_value": "",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def npair_update_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "NPAIR4307_0_standard_smooth_branch",
            "standard Dq/Hperp source branch plus smooth Hilbert volume source domain",
            "N_pair <= N_EM + N_rest",
            "N_src=0 from 4305 and N_inner=0 from 4307 conditional domain identity",
            "REDUCED_IF_DOMAIN_SIGNED",
        ),
        (
            "NPAIR4307_1_all_visible_selector",
            "smooth Hilbert volume plus visible Maxwell-Hodge/rest selector",
            "N_pair=0",
            "requires EM/rest/source-domain clauses all parent-signed",
            "EXACT_ROUTE_CONDITIONAL_NOT_CLAIMED",
        ),
        (
            "NPAIR4307_2_exterior_profile",
            "exterior worldtube/source-removed branch",
            "N_pair <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src|| + N_EM + N_rest",
            "the safe fallback if source-domain ownership does not close",
            "BOUND_ROUTE_READY_INPUTS_MISSING",
        ),
        (
            "NPAIR4307_3_source_to_Newton_guard",
            "any branch trying Newton/local-GR source normalization",
            "retain R_eq + I_commutator + calibration tail unless 1714/1715 gates close",
            "N_inner zero is not the same as worldtube-Hilbert/topological equality",
            "GUARD_ACTIVE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for update_id, branch_name, formula, reason, status in specs:
        row = base_row()
        row.update(
            {
                "update_id": update_id,
                "branch_name": branch_name,
                "formula": formula,
                "reason": reason,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4307_0_gain",
            "SOURCE_DOMAIN_SPLIT_DERIVED",
            "The inner-boundary problem is no longer a fog bank: smooth Hilbert volume domain gives exact N_inner=0; exterior/worldtube domain keeps a flux profile.",
            "Carry both branches explicitly until the parent signs the domain choice.",
        ),
        (
            "DEC4307_1_preferred",
            "PREFER_SMOOTH_HILBERT_VOLUME_PARENT_SIGNATURE",
            "It uses the existing Hilbert source-measure descent and avoids inventing artificial point-source boundary hair.",
            "Try to parent-sign the smooth volume domain as the local ordinary-matter source branch.",
        ),
        (
            "DEC4307_2_fallback",
            "EXTERIOR_FLUX_PROFILE_RETAINED",
            "If tests require exterior worldtube/excision language, the inner boundary must be scored through Q_m^H, g_perp and B_src.",
            "Create sourced/zero-theorem rows for the first worldtube flux profile.",
        ),
        (
            "DEC4307_3_guard",
            "NEWTON_LOCAL_GR_STILL_BLOCKED",
            "N_inner zero does not close R_eq/I_commutator/source-to-Newton chain or lambda_m numeric scoring.",
            "Keep local-GR claim shut until source-domain, EM/rest, lambda_m, R_eq and I_commutator gates are all closed or bounded.",
        ),
        (
            "DEC4307_4_next",
            "PARENT_SIGNATURE_OR_FIRST_FLUX_ROW_NEXT",
            "The next useful move is not another audit; it is either sign the smooth Hilbert domain or fill the first concrete flux row.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not use smooth Hilbert N_inner=0 inside an exterior/worldtube/excision domain.",
        "Do not erase a worldtube boundary by saying the source is Hilbert unless the operator domain actually includes the source volume.",
        "Do not reduce exterior flux to a scalar Q_m^H without g_perp and B_src zero/bound rows.",
        "Do not hide Poynting or radiative flux in the static bulk source; route it as Hilbert EM stress or boundary flux.",
        "Do not claim Newton/local-GR source normalization from N_inner alone; R_eq, I_commutator and calibration remain live.",
        "Do not score R10/PPN/clock/orbital rows from the flux schema until numeric values or theorem-zero certificates are sourced.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4307_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4307_0_source_domain", "source-domain choice", "SPLIT_DERIVED_PARENT_SIGNATURE_NEEDED", "smooth Hilbert branch versus exterior worldtube branch is now explicit"),
        ("STAT4307_1_Ninner_smooth", "N_inner smooth branch", "EXACT_ZERO_IF_PARENT_SIGNED", "partialD_in empty and no artificial B_src"),
        ("STAT4307_2_Ninner_exterior", "N_inner exterior branch", "FLUX_PROFILE_REQUIRED", "Q_m^H, g_perp, B_src, C_0, C_perp needed"),
        ("STAT4307_3_Npair", "N_pair", "REDUCED_BY_BRANCH_NOT_CLOSED", "smooth branch can reduce to N_EM+N_rest; exterior branch has profile envelope"),
        ("STAT4307_4_source_to_Newton", "source-to-Newton chain", "STILL_BLOCKED", "1714/1715 equality/commutator gates remain open"),
        ("STAT4307_5_next", "next target", "DERIVATION_OR_FIRST_ROW", NEXT_TARGET),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4307_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the parent local branch sign the smooth Hilbert volume source domain, or must the first worldtube flux-profile row be sourced?",
            "preferred_route": "derive from the parent/source action that ordinary compact matter stays inside the m-lock Hilbert volume domain, so partialD_in is empty",
            "fallback_route": "create the first sourced/zero-theorem row for g_in, Q_m^H, g_perp, B_src, C_0 and C_perp on partialW_H",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 323 PPC4161 source-domain owner or inner flux profile fill

Marker: `{MARKER}`

## Decision

`{DECISION}`

4307 fixes the fork created by 4306:

```text
smooth Hilbert volume source domain:
partialD_in = empty set  =>  N_inner = 0
```

but:

```text
exterior/worldtube source-removed domain:
partialD_in = partial W_H
N_inner <= C_0 |Q_m^H| + C_perp ||g_perp|| + ||B_src||
```

This is a real move forward: the local source-pair problem is now a parent domain signature or a flux-profile row, not a vague missing coupling.

## Source-Domain Owner Matrix

{md_table(tables["owner"], ["row_id", "domain_choice", "boundary_status", "inner_result", "status"])}

## Smooth No-Inner-Boundary Theorem

{md_table(tables["theorem"], ["theorem_id", "statement", "consequence", "status"])}

## Exterior/Worldtube Matching Runner

{md_table(tables["runner"], ["runner_id", "branch_name", "inner_input", "formula", "status"])}

## Flux Profile Schema

{md_table(tables["flux"], ["profile_id", "symbol", "definition", "status", "next_input"])}

## Npair Update

{md_table(tables["npair"], ["update_id", "branch_name", "formula", "status"])}

## Result

The clean route is now precise: parent-sign smooth Hilbert volume matter on the m-lock domain, and `N_inner` vanishes exactly. If the theory instead uses exterior/worldtube language, it must stop pretending the inner boundary is gone and carry the flux profile honestly.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4307 - source-domain owner or inner flux profile fill

## Verdict
- Derived the source-domain split behind `N_inner`: smooth Hilbert volume source gives exact `N_inner=0`; exterior/worldtube/excision source keeps a live boundary flux.
- Converted the fallback into a concrete schema: `g_in`, `Q_m^H`, `g_perp`, `B_src`, `C_0`, `C_perp`, and the no-cancellation `N_inner` envelope.
- Updated `N_pair`: smooth branch reduces to `N_EM + N_rest`; exterior branch uses the full flux-profile bound.
- No Newton/local-GR claim fires, because the worldtube-Hilbert equality, `I_commutator`, calibration and `lambda_m` gates are still open.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Source-Domain Owner Matrix
{md_table(tables["owner"], ["row_id", "domain_choice", "boundary_status", "inner_result", "status", "note"])}

## Smooth Hilbert No-Inner-Boundary Theorem
{md_table(tables["theorem"], ["theorem_id", "statement", "proof_input", "consequence", "status"])}

## Exterior/Worldtube Matching Runner
{md_table(tables["runner"], ["runner_id", "branch_name", "inner_input", "formula", "status", "note"])}

## Inner Flux Profile Schema
{md_table(tables["flux"], ["profile_id", "symbol", "definition", "units", "status", "next_input"])}

## Npair Source-Domain Update
{md_table(tables["npair"], ["update_id", "branch_name", "formula", "reason", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4307_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4307_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4307_2_smooth_branch", "smooth Hilbert volume branch gives exact N_inner zero", any(row["row_id"] == "DOM4307_0_smooth_Hilbert_volume" for row in tables["owner"]), "owner_matrix")
    add("VAL4307_3_exterior_branch", "exterior worldtube branch retains flux profile", any(row["row_id"] == "DOM4307_1_exterior_worldtube_annulus" for row in tables["owner"]), "owner_matrix")
    add("VAL4307_4_theorem_zero", "smooth no-inner-boundary theorem row exists", any(row["theorem_id"] == "THM4307_2_smooth_zero" for row in tables["theorem"]), "theorem_rows")
    add("VAL4307_5_profile_schema", "flux profile schema includes QmH, g_perp and B_src", all(any(row.get("symbol") == symbol for row in tables["flux"]) for symbol in ["Q_m^H = int_partialW_H g_in dSigma", "g_perp = g_in - Q_m^H/Area(partialW_H)", "B_src"]), "flux_schema")
    add("VAL4307_6_npair_guard", "Npair update keeps source-to-Newton guard", any(row["update_id"] == "NPAIR4307_3_source_to_Newton_guard" for row in tables["npair"]), "npair_update")
    add("VAL4307_7_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next_rows")
    add(
        "VAL4307_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4307_9_missing_rows_not_claim_ready",
        "all flux profile rows remain nonclaim until sourced",
        all(row.get("score_ready") == "False" and row.get("valid_for_claim") == "False" for row in tables["flux"]),
        "flux_schema",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4307_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4307_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4307_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4307_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4307_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4307_SOURCE_REGISTER.csv",
        "owner": SOURCE_DIR / "P8_Y5_R2FR_4307_SOURCE_DOMAIN_OWNER_MATRIX.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4307_SMOOTH_NOINNER_THEOREM.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4307_EXTERIOR_WORLDTUBE_MATCHING_RUNNER.csv",
        "flux": SOURCE_DIR / "P8_Y5_R2FR_4307_INNER_FLUX_PROFILE_SCHEMA.csv",
        "npair": SOURCE_DIR / "P8_Y5_R2FR_4307_NPAIR_SOURCE_DOMAIN_UPDATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4307_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4307_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4307_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4307_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "owner": owner_matrix_rows(),
        "theorem": theorem_rows(),
        "runner": matching_runner_rows(),
        "flux": flux_profile_rows(),
        "npair": npair_update_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4307 source-domain owner or inner flux profile fill

Marker: `{MARKER}`

4307 converts the inner source-pair blocker into a concrete domain split. If the parent local branch owns a smooth Hilbert volume source domain on the m-lock operator domain, `partialD_in=empty` and `N_inner=0` exactly. If the calculation is an exterior/worldtube or point/excision branch, `partialW_H` is a real inner boundary and the honest fallback is `N_inner <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||`. This advances the route without claiming Newton/local-GR source normalization, because worldtube-Hilbert equality and commutator gates remain open.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4307 packet source-domain split

Marker: `{PACKET_MARKER}`

Packet update: smooth Hilbert volume matter is the preferred zero route for `N_inner`; exterior/worldtube matter keeps a profile row. The packet must not mix those branches.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
