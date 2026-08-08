from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3689"
BRANCH_ID = "MTS_R2FR_Y5_CANONICAL_GAMMA_KHAT_ADOPTION_LAW_OR_LEGACY_SYMBOL_QUARANTINE_3689"
DOC = ROOT / "3689-Y5-R2FR-canonical-Gamma-Khat-adoption-law-or-legacy-symbol-quarantine.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3688", RESIDUALS / "P8_Y5_R2FR_3688_NEXT_TARGET.csv", "canonical", "3688 selected canonical Gamma/Khat adoption or legacy quarantine"),
        ("inventory_3688", RESIDUALS / "P8_Y5_R2FR_3688_LIVE_SYMBOL_INVENTORY.csv", "LSI3688_1_Khat", "live symbol inventory before adoption"),
        ("match_3688", RESIDUALS / "P8_Y5_R2FR_3688_COMPONENT_MATCH_MATRIX.csv", "CMM3688_9_verdict", "component match matrix before quarantine"),
        ("bounds_3688", RESIDUALS / "P8_Y5_R2FR_3688_DELTAK_COMPONENT_BOUND_ROWS.csv", "DKB3688_0_total", "DeltaK component envelope"),
        ("qloc_3688", RESIDUALS / "P8_Y5_R2FR_3688_QLOC_PROFILE_INPUT_ROWS.csv", "QPI3688_1_Euler_source", "q_loc profile and J_A source law"),
        ("clean_3686", RESIDUALS / "P8_Y5_R2FR_3686_RESPONSE_ACTION_CANDIDATE_ROWS.csv", "RAC3686_0_clean_action", "clean response action candidate"),
        ("helmholtz_3687", RESIDUALS / "P8_Y5_R2FR_3687_HELMHOLTZ_MATRIX_ROWS.csv", "HMX3687_0_clean_bulk_operator", "clean bulk Helmholtz theorem"),
        ("scalar_3628", RESIDUALS / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv", "GSD3628_2_even_response_doublet", "even response doublet candidate"),
        ("parent_clause_3630", RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv", "PAC3630_1_total_action", "single parent action clause with quotient descent"),
        ("adoption_3419", RESIDUALS / "P8_Y5_R2FR_3419_LIVE_SYMBOL_ADOPTION_MAP.csv", "LSA3419_0_symbol_Khat", "older adoption rule for Khat as K_metric or residual"),
        ("gate_3076", RESIDUALS / "P8_Y5_R2FR_3076_GK_ACTION_ADOPTION_GATE.csv", "GKA3076_7_verdict", "strong GK action adoption failed in old source set"),
        ("decision_1665", RESIDUALS / "P8_Y5_PARENT_QLOC_1665_ADOPTION_OR_DEMOTION_DECISION.csv", "ADD1665_3_best_route", "prior decision selected parent object-language/vertical generator route"),
        ("quarantine_1458", RESIDUALS / "P8_Y5_R10_1458_QUARANTINE_TEMPLATE_REGISTER.csv", "QT1458_0_official_readout", "quarantine discipline pattern"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def canonical_branch_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "CAN3689_0_branch_status",
            "canonical private branch",
            "Use action-defined Gamma_can/K_can as the only canonical Gamma/Khat symbols for future local-GR derivations.",
            "Gamma_can and K_can are adopted as private derivation definitions, not as public/local-GR evidence.",
            "ADOPT_PRIVATE_BRANCH_NONCLAIM",
            True,
        ),
        (
            "CAN3689_1_action",
            "canonical S_GK",
            "S_GK^can[Z;g] = -int sqrt(-g)[Gamma0 + 1/2 G_AB g^{mu nu} D_mu Z^A D_nu Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)] + S_boundary^can + S_flux^phys_if_present",
            "This selects the clean response action as the canonical local-response branch.",
            "DEFINITION_ADOPTED_FOR_PRIVATE_DERIVATIONS",
            True,
        ),
        (
            "CAN3689_2_Gamma",
            "canonical Gamma",
            "Gamma_can := Gamma0 + 1/2 G_AB g^{mu nu} D_mu Z^A D_nu Z^B + 1/2 M_AB Z^A Z^B + O(Z^4) + Gamma_boundary^can + Gamma_flux^phys",
            "Gamma_eff without a source-backed map is now legacy notation; canonical branch uses Gamma_can.",
            "CANONICAL_DEFINITION_WRITTEN",
            True,
        ),
        (
            "CAN3689_3_Khat",
            "canonical Khat",
            "K_can^{mu nu} := K_metric^{mu nu}[Gamma_can] := Gamma_can g^{mu nu} - T_GK^{mu nu}, with T_GK^{mu nu}:=-2/sqrt(-g) delta S_GK^can/delta g_{mu nu}",
            "K_hat without this metric-response identity is not canonical evidence.",
            "CANONICAL_METRIC_RESPONSE_DEFINITION_WRITTEN",
            True,
        ),
        (
            "CAN3689_4_Helmholtz",
            "canonical Helmholtz",
            "H_can=0 in the bulk by construction if G_AB/M_AB are symmetric, D_mu is pairing-compatible, gauge/constraints are removed and boundary adjoint terms are fixed/no-flux.",
            "3687 makes Helmholtz a theorem for the canonical bulk branch.",
            "BULK_HELMHOLTZ_INHERITED_CONDITIONALLY",
            True,
        ),
        (
            "CAN3689_5_DeltaK",
            "canonical DeltaK",
            "Delta_K^can := K_can - K_metric[Gamma_can] = 0 by definition inside the canonical branch; Delta_K^legacy := K_hat^legacy - K_can is retained for old symbols.",
            "This is the actual adoption/quarantine split.",
            "CANONICAL_ZERO_LEGACY_RESIDUAL_SPLIT",
            True,
        ),
        (
            "CAN3689_6_q_loc",
            "canonical q_loc profile",
            "q_can^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho) for the canonical branch; q_legacy^nu = q_can^nu - P_loc^nu_rho nabla_mu Delta_K_legacy^{mu rho}.",
            "local silence still requires E_A=0, B_GK=0, P_loc owner and source coupling closure.",
            "PROFILE_RULE_WRITTEN_NONCLAIM",
            True,
        ),
        (
            "CAN3689_7_public_claim",
            "current theory claim status",
            "Canonical branch adoption does not by itself prove current MTS local-GR/Newton, because Z physical map, quotient descent, source coupling, boundary, P_loc and arena coefficients remain unsigned.",
            "The adoption is a disciplined fork, not a claim shortcut.",
            "NO_PUBLIC_CLAIM",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "canonical_id": canonical_id,
            "object": object_name,
            "mathematical_rule": mathematical_rule,
            "meaning": meaning,
            "status": status,
            "adopted_as_private_branch": adopted_as_private_branch,
            "claim_allowed": False,
            "score_ready": False,
        }
        for canonical_id, object_name, mathematical_rule, meaning, status, adopted_as_private_branch in specs
    ]


def adoption_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "AG3689_0_clean_action",
            "explicit action-defined Gamma/Khat branch",
            "S_GK^can, Gamma_can and K_can are written in one convention",
            "PASS_PRIVATE",
            "none inside canonical branch",
        ),
        (
            "AG3689_1_Helmholtz",
            "bulk variational integrability",
            "clean bulk Helmholtz closes under symmetric/coercive/self-adjoint response data",
            "PASS_CONDITIONAL_PRIVATE",
            "R_H_boundary+R_H_conn remain if boundary/projector is not fixed",
        ),
        (
            "AG3689_2_legacy_compat",
            "legacy Gamma/Khat map",
            "old symbols must map to Gamma_can/K_can with Delta_K_legacy=0 or be quarantined",
            "FAIL_LIVE_COMPATIBILITY",
            "R_DeltaK_legacy",
        ),
        (
            "AG3689_3_Z_physical_map",
            "Z^A physical residual basis",
            "Z coordinates must cover q_loc/PPN/source/boundary residual channels with a parent vertical generator",
            "OPEN",
            "R_Zmap",
        ),
        (
            "AG3689_4_JA_zero",
            "source coupling silence",
            "J_A=0 by quotient descent/evenness or finite sourced coefficient bound",
            "OPEN_CORE",
            "R_JA",
        ),
        (
            "AG3689_5_boundary",
            "boundary/no-flux handoff",
            "B_GK=0 or fixed-reference/no-flux on local collars",
            "OPEN",
            "R_boundary",
        ),
        (
            "AG3689_6_Ploc",
            "projector/readout ownership",
            "P_loc parent-owned and compatible with canonical branch",
            "OPEN",
            "R_Ploc",
        ),
        (
            "AG3689_7_verdict",
            "strong adoption as current MTS theorem",
            "all adoption gates pass",
            "PRIVATE_CANONICAL_BRANCH_ADOPTED_STRONG_CLAIM_BLOCKED",
            "R_current_claim = R_DeltaK_legacy+R_Zmap+R_JA+R_boundary+R_Ploc",
        ),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "residual_if_failed": residual_if_failed,
            "claim_allowed": False,
            "score_ready": False,
        }
        for gate_id, gate, requirement, status, residual_if_failed in specs
    ]


def legacy_quarantine_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "LQ3689_0_Gamma_eff_legacy",
            "Gamma_eff legacy symbol",
            "may be used only as Gamma_can after source-backed equality map; otherwise Gamma_eff^legacy is a residual/readout notation",
            "R_Gamma_legacy := Gamma_eff^legacy - Gamma_can",
            "QUARANTINED_UNTIL_MAPPED",
        ),
        (
            "LQ3689_1_Khat_legacy",
            "K_hat legacy symbol",
            "may be used only as K_can=K_metric[Gamma_can]; otherwise it contributes Delta_K_legacy",
            "Delta_K_legacy^{mu nu}:=K_hat_legacy^{mu nu}-K_can^{mu nu}",
            "QUARANTINED_UNTIL_COMPONENT_MATCH",
        ),
        (
            "LQ3689_2_q_loc_legacy",
            "q_loc legacy expression",
            "may be used only through q_can plus explicit legacy DeltaK divergence",
            "q_legacy^nu = q_can^nu - P_loc^nu_rho nabla_mu Delta_K_legacy^{mu rho}",
            "REWRITTEN_AS_CANONICAL_PLUS_RESIDUAL",
        ),
        (
            "LQ3689_3_Kconn_legacy",
            "K_conn legacy residue",
            "metric-only connection response is canonical only if no independent connection/hypermomentum branch is signed",
            "R_Kconn_legacy <= C_conn(||delta Gamma_LC||O1+||delta G_AB||O2+||delta star||O3+||delta D||O4)",
            "BOUND_INTERFACE_RETAINED",
        ),
        (
            "LQ3689_4_P4_legacy",
            "P4 non-LC residue",
            "torsion/nonmetricity/projective/hypermomentum terms are absent only after parent metric-only/no-hypermomentum proof",
            "R_P4_legacy",
            "QUARANTINED_AS_NONLC_RESIDUAL",
        ),
        (
            "LQ3689_5_flux_legacy",
            "flux/Poynting shortcut",
            "physical flux may enter only as S_flux^phys with explicit F,W,J and Hilbert stress",
            "R_flux_legacy if hidden in q_loc closure",
            "QUARANTINED_UNLESS_PHYSICAL_STRESS",
        ),
        (
            "LQ3689_6_shortcut_claims",
            "any q_loc=0/local-GR shortcut based on old symbols",
            "not allowed without canonical branch gates plus residual zeros/bounds",
            "R_shortcut_claim",
            "CLAIM_SHORTCUT_BLOCKED",
        ),
    ]
    return [
        {
            **base(ts),
            "quarantine_id": quarantine_id,
            "legacy_item": legacy_item,
            "policy": policy,
            "residual_or_rewrite": residual_or_rewrite,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for quarantine_id, legacy_item, policy, residual_or_rewrite, status in specs
    ]


def compatibility_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "BC3689_0_identity_shape",
            "old q_loc identity shape",
            "nabla Gamma - div Khat",
            "compatible only if Gamma_eff^legacy=Gamma_can and Khat^legacy=K_can",
            "CONDITIONAL_COMPATIBILITY",
            "Delta_K_legacy divergence otherwise",
        ),
        (
            "BC3689_1_even_response",
            "old double-zero mechanism",
            "F1=0 / local plateau",
            "compatible with canonical branch because even response gives Gamma_can-Gamma0=O(Z^2)",
            "COMPATIBLE_IN_CANONICAL_BRANCH",
            "Z physical map still required",
        ),
        (
            "BC3689_2_source_coupling",
            "old source-normalization silence",
            "ordinary matter does not source local residual",
            "not automatic; canonical branch still needs quotient descent or J_A bound",
            "INCOMPATIBLE_AS_ASSUMPTION",
            "R_JA",
        ),
        (
            "BC3689_3_connection",
            "old K_conn zero hope",
            "metric-only/LC stack gives no extra residue",
            "compatible only after no independent connection/no hypermomentum/no shadow operator clauses close",
            "CONDITIONAL_NOT_ADOPTED",
            "R_Kconn_legacy+R_P4_legacy",
        ),
        (
            "BC3689_4_boundary",
            "old boundary silence",
            "boundary exact terms do not source local force/mass",
            "not automatic; canonical branch carries B_GK until no-flux/fixed-reference is signed",
            "OPEN",
            "R_boundary",
        ),
        (
            "BC3689_5_observables",
            "old PPN/R10/WEP readiness",
            "q_loc maps to arenas",
            "not compatible with claims until units, P_loc and arena coefficients are sourced",
            "OPEN",
            "R_arena_projection",
        ),
    ]
    return [
        {
            **base(ts),
            "compat_id": compat_id,
            "legacy_claim": legacy_claim,
            "legacy_form": legacy_form,
            "canonical_requirement": canonical_requirement,
            "compatibility_status": compatibility_status,
            "residual_if_not_met": residual_if_not_met,
            "claim_allowed": False,
            "score_ready": False,
        }
        for compat_id, legacy_claim, legacy_form, canonical_requirement, compatibility_status, residual_if_not_met in specs
    ]


def residual_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RES3689_0_current_claim",
            "abs(R_current_claim)/N_H",
            "(|R_DeltaK_legacy|+|R_Zmap|+|R_JA|+|R_boundary|+|R_Ploc|+|R_arena_projection|)/N_H",
            "dimensionless no-cancellation envelope",
            "FORMULA_READY_INPUTS_MISSING",
            "what remains before canonical branch can claim local GR/Newton in physical arenas",
            "AG3689_7_verdict",
        ),
        (
            "RES3689_1_legacy_DeltaK",
            "abs(R_DeltaK_legacy)/N_H",
            "(|R_Gamma_legacy|+|Delta_K_legacy|+|R_Kconn_legacy|+|R_P4_legacy|+|R_flux_legacy|)/N_H",
            "dimensionless",
            "LEGACY_QUARANTINE_RESIDUAL",
            "old symbols are not deleted; they are paid for as residuals",
            "LQ3689_1_Khat_legacy",
        ),
        (
            "RES3689_2_JA",
            "abs(R_JA)/N_H",
            "MISSING_J_A_ZERO_THEOREM_OR_SOURCE_BACKED_GREEN_PROFILE_COEFFICIENT",
            "dimensionless/source-profile units",
            "CORE_COUPLING_INPUT_MISSING",
            "next major target",
            "AG3689_4_JA_zero",
        ),
        (
            "RES3689_3_Zmap",
            "abs(R_Zmap)/N_H",
            "MISSING_PARENT_VERTICAL_GENERATOR_AND_FULL_RANK_PHYSICAL_RESIDUAL_MAP",
            "dimensionless",
            "MISSING_PHYSICAL_MAP",
            "Z must represent physical local residuals, not just auxiliary math",
            "AG3689_3_Z_physical_map",
        ),
        (
            "RES3689_4_boundary_Ploc",
            "abs(R_boundary)+abs(R_Ploc)",
            "MISSING_BOUNDARY_NOFLUX_AND_PARENT_PLOC_COMMUTATOR_BOUNDS",
            "dimensionless/local-force units",
            "BOUNDARY_PROJECTOR_INPUTS_MISSING",
            "still required for local tests",
            "AG3689_5_boundary",
        ),
    ]
    return [
        {
            **base(ts),
            "residual_id": residual_id,
            "quantity": quantity,
            "formula_or_bound": formula_or_bound,
            "units": units,
            "status": status,
            "interpretation": interpretation,
            "source_anchor": source_anchor,
            "claim_allowed": False,
            "score_ready": False,
        }
        for residual_id, quantity, formula_or_bound, units, status, interpretation, source_anchor in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3689_0_result", "PRIVATE_CANONICAL_BRANCH_ADOPTED", "Gamma_can/K_can are now the private canonical branch for future derivations", "legacy Gamma/Khat must map to canonical branch or become residual"),
        ("DEC3689_1_not_claim", "STRONG_CURRENT_CLAIM_BLOCKED", "canonical adoption is not the same as proving current MTS local GR", "do not claim Newton/local-GR/PPN/R10/WEP yet"),
        ("DEC3689_2_legacy", "LEGACY_SYMBOLS_QUARANTINED", "old free Gamma/Khat/q_loc shortcuts are forbidden as evidence", "use explicit DeltaK_legacy rows"),
        ("DEC3689_3_coupling", "JA_COUPLING_IS_NEXT", "after canonicalization, the biggest physical blocker is source coupling J_A", "derive quotient-descent J_A=0 or finite Green-profile bound"),
        ("DEC3689_4_next", "NEXT_BEST_TARGET", "canonical branch makes the coupling test cleaner", "run 3690 canonical source-coupling J_A zero theorem or Green-profile coefficient bound"),
        ("DEC3689_5_private", "PRIVATE_NONCLAIM", "no GitHub/public action", "continue private framework derivation"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "status": status,
            "decision": decision,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, status, decision, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3689_0_current_MTS", "claim canonical branch is full current MTS", "BLOCKED_PARENT_SIGNATURES", "Z map, quotient descent, source, boundary and projector clauses are unsigned"),
        ("CG3689_1_local_GR", "claim local GR/Newton derived", "BLOCKED_RESIDUALS", "R_current_claim remains nonzero/non-sourced"),
        ("CG3689_2_legacy_shortcut", "use old Gamma/Khat/q_loc as proof", "BLOCKED_QUARANTINE", "legacy symbols now require explicit compatibility or residual rows"),
        ("CG3689_3_source_coupling", "claim J_A=0", "BLOCKED_NEXT_TARGET", "quotient descent/evenness/source orthogonality not yet proved"),
        ("CG3689_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3689_0",
            "status": "PRIVATE_CANONICAL_GAMMA_KHAT_BRANCH_ADOPTED_LEGACY_SYMBOLS_QUARANTINED_STRONG_CLAIM_BLOCKED",
            "summary": "3689 adopts the clean action-defined Gamma_can/K_can branch for private future derivations, defines canonical q_can and DeltaK_legacy, and quarantines old Gamma_eff/K_hat/q_loc shortcuts as explicit residuals. It does not claim local GR/Newton because Z mapping, J_A coupling, boundary, P_loc and arena projections remain open.",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3689_0",
            "target_doc": "3690-Y5-R2FR-canonical-source-coupling-JA-zero-theorem-or-Green-profile-bound.md",
            "target_script": "scripts/Y5_R2FR_3690_canonical_source_coupling_JA_zero_theorem_or_Green_profile_bound.py",
            "objective": "try to prove J_A=0 in the canonical branch from quotient descent/evenness/source-current orthogonality; if not, derive the finite Green-profile bound Z^A=-(L^-1)^{AB}J_B plus boundary terms and source-ready coefficient rows",
            "success_gate": "J_A is zero by a parent-signed descent theorem, or R_JA is converted into a finite nonclaim profile/bound interface without local-GR/Newton claims",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    canonical: list[dict[str, object]],
    gates: list[dict[str, object]],
    quarantine: list[dict[str, object]],
    compatibility: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3689 - Canonical Gamma/Khat adoption law or legacy symbol quarantine",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint takes the leap: the clean action-defined branch becomes the private canonical `Gamma/Khat` branch for future derivations. Old free-floating `Gamma_eff`, `K_hat`, and `q_loc` symbols are not deleted, but they are quarantined unless they are mapped into the canonical branch.",
        "",
        "## Main result",
        "",
        "Canonical action:",
        "",
        "`S_GK^can[Z;g] = -int sqrt(-g)[Gamma0 + 1/2 G_AB g^{mu nu} D_mu Z^A D_nu Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)] + S_boundary^can + S_flux^phys_if_present`.",
        "",
        "Canonical metric response:",
        "",
        "`K_can^{mu nu} := K_metric^{mu nu}[Gamma_can] := Gamma_can g^{mu nu} - T_GK^{mu nu}`.",
        "",
        "`T_GK^{mu nu}:=-2/sqrt(-g) delta S_GK^can/delta g_{mu nu}`.",
        "",
        "Adoption/quarantine split:",
        "",
        "`Delta_K^can = 0` by definition inside the canonical branch.",
        "",
        "`Delta_K^legacy := K_hat^legacy - K_can` is retained for old symbols.",
        "",
        "Canonical/legacy q profile:",
        "",
        "`q_can^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho)`.",
        "",
        "`q_legacy^nu = q_can^nu - P_loc^nu_rho nabla_mu Delta_K_legacy^{mu rho}`.",
        "",
        "Current-claim residual:",
        "",
        "`abs(R_current_claim)/N_H <= (|R_DeltaK_legacy|+|R_Zmap|+|R_JA|+|R_boundary|+|R_Ploc|+|R_arena_projection|)/N_H`.",
        "",
        "## Canonical branch rows",
    ]
    for row in canonical:
        lines.append(f"- `{row['canonical_id']}`: {row['status']} - {row['object']} -> {row['meaning']}")
    lines.extend(["", "## Adoption gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Legacy quarantine"])
    for row in quarantine:
        lines.append(f"- `{row['quarantine_id']}`: {row['status']} - {row['legacy_item']} -> `{row['residual_or_rewrite']}`")
    lines.extend(["", "## Backward compatibility"])
    for row in compatibility:
        lines.append(f"- `{row['compat_id']}`: {row['compatibility_status']} - {row['legacy_claim']} -> {row['residual_if_not_met']}")
    lines.extend(["", "## Residual rows"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}`: {row['status']} - `{row['quantity']}` -> `{row['formula_or_bound']}`; {row['interpretation']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    canonical: list[dict[str, object]],
    gates: list[dict[str, object]],
    quarantine: list[dict[str, object]],
    compatibility: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + canonical + gates + quarantine + compatibility + residuals + decisions + claim_gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3689*", "3689-Y5-R2FR-*", "P8_Y5*3689*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    canonical_by_id = {str(row["canonical_id"]): row for row in canonical}
    gate_by_id = {str(row["gate_id"]): row for row in gates}
    quarantine_by_id = {str(row["quarantine_id"]): row for row in quarantine}
    residual_by_id = {str(row["residual_id"]): row for row in residuals}

    add("VAL3689_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3689_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3689_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3689 outputs written")
    add("VAL3689_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3689_4_private_adoption", canonical_by_id["CAN3689_0_branch_status"]["adopted_as_private_branch"] is True and canonical_by_id["CAN3689_0_branch_status"]["status"] == "ADOPT_PRIVATE_BRANCH_NONCLAIM", "canonical branch adopted privately only")
    add("VAL3689_5_canonical_K", "K_metric" in canonical_by_id["CAN3689_3_Khat"]["mathematical_rule"] and "delta S_GK^can" in canonical_by_id["CAN3689_3_Khat"]["mathematical_rule"], "canonical Khat is metric response")
    add("VAL3689_6_legacy_quarantine", "Delta_K_legacy" in quarantine_by_id["LQ3689_1_Khat_legacy"]["residual_or_rewrite"] and quarantine_by_id["LQ3689_6_shortcut_claims"]["status"] == "CLAIM_SHORTCUT_BLOCKED", "legacy Khat and shortcuts are quarantined")
    add("VAL3689_7_strong_claim_blocked", gate_by_id["AG3689_7_verdict"]["status"] == "PRIVATE_CANONICAL_BRANCH_ADOPTED_STRONG_CLAIM_BLOCKED", "strong current claim remains blocked")
    add("VAL3689_8_residual_formula", all(term in residual_by_id["RES3689_0_current_claim"]["formula_or_bound"] for term in ["R_DeltaK_legacy", "R_Zmap", "R_JA", "R_boundary", "R_Ploc"]), "current-claim residual contains required blockers")
    add("VAL3689_9_next_target", next_target[0]["target_doc"].startswith("3690-") and "J_A" in next_target[0]["objective"], "3690 targets canonical J_A coupling")
    add("VAL3689_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in claim_gates), "claim gates remain blocked")
    add("VAL3689_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3689_12_doc_written", "S_GK^can" in doc_text and "Delta_K^legacy" in doc_text and "R_current_claim" in doc_text, "doc records canonical branch, legacy quarantine and residual")
    add("VAL3689_13_no_formalization_leak", not leaks, "no 3689 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    canonical = canonical_branch_rows(ts)
    gates = adoption_gate_rows(ts)
    quarantine = legacy_quarantine_rows(ts)
    compatibility = compatibility_rows(ts)
    residuals = residual_rows(ts)
    decisions = decision_rows(ts)
    claim_gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3689_SOURCE_REGISTER.csv",
        "canonical": RESIDUALS / "P8_Y5_R2FR_3689_CANONICAL_GAMMA_KHAT_BRANCH_ROWS.csv",
        "adoption": RESIDUALS / "P8_Y5_R2FR_3689_ADOPTION_GATE_ROWS.csv",
        "quarantine": RESIDUALS / "P8_Y5_R2FR_3689_LEGACY_SYMBOL_QUARANTINE.csv",
        "compatibility": RESIDUALS / "P8_Y5_R2FR_3689_BACKWARD_COMPATIBILITY_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3689_RESIDUAL_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3689_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3689_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3689_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3689_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3689_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["canonical"], canonical)
    write_csv(outputs["adoption"], gates)
    write_csv(outputs["quarantine"], quarantine)
    write_csv(outputs["compatibility"], compatibility)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, canonical, gates, quarantine, compatibility, residuals, decisions, claim_gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, canonical, gates, quarantine, compatibility, residuals, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3689 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3689 checkpoint: private canonical Gamma/Khat branch adopted; legacy symbols quarantined; strong claim blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
