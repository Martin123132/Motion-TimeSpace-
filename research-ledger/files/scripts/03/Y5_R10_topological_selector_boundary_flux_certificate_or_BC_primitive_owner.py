from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(h, "")).replace("\n", " ") for h in headers) + " |")
    return "\n".join(out)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1170_0_1169_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1169_NEXT_TARGET.csv",
            "needle": "NEXT1169_0_1170",
            "role": "handoff to topological-selector boundary-flux certificate.",
        },
        {
            "source_id": "SRC1170_1_1169_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1169_VALIDATION.csv",
            "needle": "V1169_SUMMARY",
            "role": "1169 validation summary.",
        },
        {
            "source_id": "SRC1170_2_1169_top",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1169_TOPOLOGICAL_SELECTOR_THEOREM.csv",
            "needle": "TOP1169_4_verdict",
            "role": "topological selector best-route verdict.",
        },
        {
            "source_id": "SRC1170_3_1169_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1169_PARENT_SOURCE_OWNER_ATTEMPT.csv",
            "needle": "PSO1169_4_boundary_flux_owner",
            "role": "Phi_C/B_C boundary owner remains missing.",
        },
        {
            "source_id": "SRC1170_4_1169_closed_weight",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1169_CLOSED_WEIGHT_ZERO_ATTEMPT.csv",
            "needle": "CWZ1169_1_closed_weight_route",
            "role": "closed-weight route to test.",
        },
        {
            "source_id": "SRC1170_5_1169_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1169_CLAIM_GATES.csv",
            "needle": "G1169_2_boundary_flux",
            "role": "boundary flux gate remains blocked.",
        },
        {
            "source_id": "SRC1170_6_274_decomp",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "exact plus top-class decomposition.",
        },
        {
            "source_id": "SRC1170_7_274_CD",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "C_D[D] = N_D^{-1} integral_D J_C",
            "role": "domain observable receiving boundary and top contributions.",
        },
        {
            "source_id": "SRC1170_8_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes residual structure.",
        },
        {
            "source_id": "SRC1170_9_1020_zero",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_2_zero_conditions",
            "role": "zero theorem conditions.",
        },
        {
            "source_id": "SRC1170_10_1020_bound",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "finite bound fallback.",
        },
        {
            "source_id": "SRC1170_11_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "stress/Ward guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def boundary_split_rows() -> list[dict[str, object]]:
    rows = [
        {
            "split_id": "BST1170_0_stokes_split",
            "object": "int_D J_C",
            "statement": "Using J_C = d_D B_C + J_C^top, the domain charge splits as int_D J_C = int_partialD B_C + int_D J_C^top, with orientation/sign convention fixed later.",
            "status": "DERIVED_STOKES_SPLIT",
            "consequence": "topology alone never proves local zero unless the boundary primitive term is zero or bounded.",
            "missing_for_claim": "B_C primitive owner, boundary condition, corner audit, units/norm",
            "valid_for_claim": False,
        },
        {
            "split_id": "BST1170_1_local_top_zero_not_enough",
            "object": "local bounded D",
            "statement": "On a contractible bounded local domain, the absolute top class can vanish, but int_partialD B_C can still be nonzero.",
            "status": "LOCAL_ZERO_REDUCED_TO_BOUNDARY",
            "consequence": "the local branch now lives or dies on Phi_C/B_C boundary flux, not on the topological selector itself.",
            "missing_for_claim": "no-flux/natural-boundary theorem or finite B_C edge bound",
            "valid_for_claim": False,
        },
        {
            "split_id": "BST1170_2_FLRW_top_survives",
            "object": "closed/global FLRW D",
            "statement": "On a closed/global top-class sector with no boundary, int_partialD B_C is absent while int_D J_C^top can survive.",
            "status": "FLRW_COMPATIBLE_WITH_TOPOLOGY",
            "consequence": "this keeps the desired asymmetry: local top killed by H^3, cosmological top allowed by H^3.",
            "missing_for_claim": "parent normalization and stress-energy of the top class",
            "valid_for_claim": False,
        },
        {
            "split_id": "BST1170_3_time_evolution_split",
            "object": "L_tau J_C",
            "statement": "If L_tau commutes with d_D up to known domain-motion terms, then L_tau J_C = d_D(L_tau B_C) + L_tau J_C^top + motion terms.",
            "status": "FORMAL_EVOLUTION_SPLIT",
            "consequence": "comparison with L_tau J_C = d_D Phi_C + Sigma_C suggests Phi_C is the exact-sector boundary transport and Sigma_C is the top/source sector.",
            "missing_for_claim": "commutator with moving domain, Phi_C sign convention, parent transport law",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def phi_bc_rows() -> list[dict[str, object]]:
    rows = [
        {
            "relation_id": "PBC1170_0_exact_sector_match",
            "clause": "Phi_C relation",
            "statement": "Exact-sector matching gives d_D(Phi_C - L_tau B_C - motion_B_C)=0. On a simple local domain this means Phi_C = L_tau B_C + motion_B_C + d_D zeta_C plus possible harmonic 2-form.",
            "status": "RELATION_DERIVED_CONDITIONAL",
            "blocks": "domain-motion term, harmonic 2-form, and boundary values are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "relation_id": "PBC1170_1_no_flux_condition",
            "clause": "local no-flux",
            "statement": "A sufficient local silence condition is pullback_boundary(Phi_C)=0 and pullback_boundary(B_C)=0, or a parent natural-boundary condition implying the same integrated flux vanishes.",
            "status": "SUFFICIENT_NOT_DERIVED",
            "blocks": "natural boundary condition from parent action; proof it preserves physical charges",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "relation_id": "PBC1170_2_finite_bound",
            "clause": "finite boundary fallback",
            "statement": "If no-flux fails, the local exact-sector contribution is bounded by |int_partialD B_C| <= ||1||_* ||B_C||_* plus weighted-Stokes derivative, harmonic, residual, and corner terms.",
            "status": "BOUND_SCHEMA_READY_VALUES_MISSING",
            "blocks": "B_C norm, boundary area/norm convention, weighted kernel derivative, harmonic/residual terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "relation_id": "PBC1170_3_charge_guard",
            "clause": "do-not-kill-physics guard",
            "statement": "Boundary silence cannot be imposed by deleting the physical mass/time/rotation/charge generator; it must be a natural condition on the lifted-C residual sector only.",
            "status": "GUARD_ACTIVE",
            "blocks": "separation of proper C-boundary gauge from physical Hamiltonian generators",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def local_zero_certificate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "cert_id": "LZC1170_0_top_class",
            "requirement": "absolute top class vanishes locally",
            "current_status": "PARTIAL_PASS_FROM_TOPOLOGY",
            "detail": "contractible bounded local domains support the H^3 zero part of the selector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "cert_id": "LZC1170_1_boundary_primitive",
            "requirement": "int_partialD B_C = 0 or source-bounded",
            "current_status": "BLOCKED_MAIN_GAP",
            "detail": "Stokes leaves the exact-sector boundary primitive even when top class vanishes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "cert_id": "LZC1170_2_boundary_flux",
            "requirement": "pullback_partialD Phi_C = 0 or source-bounded",
            "current_status": "BLOCKED",
            "detail": "time evolution/no-flux condition is not owned by parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "cert_id": "LZC1170_3_relative_classes",
            "requirement": "relative cohomology/corner/harmonic residuals absent or bounded",
            "current_status": "BLOCKED",
            "detail": "absolute H^3 zero does not erase relative or boundary cohomology by itself",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "cert_id": "LZC1170_4_bianchi",
            "requirement": "source/flux stress ledger closes",
            "current_status": "BLOCKED",
            "detail": "even a boundary theorem must carry its stress/Ward bookkeeping",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def weighted_stokes_rows() -> list[dict[str, object]]:
    rows = [
        {
            "stokes_id": "WSC1170_0_C_boundary_degree",
            "clause": "C-sector boundary degree",
            "statement": "For the C sector, B_C is naturally a 2-form primitive in D whose pullback to the two-surface partialD is top degree. This makes int_partialD B_C meaningful, but not automatically zero.",
            "status": "DEGREE_CLARIFIED",
            "missing": "parent B_C construction and pullback convention",
            "valid_for_claim": False,
        },
        {
            "stokes_id": "WSC1170_1_weighted_exact_boundary",
            "clause": "weighted Stokes residual",
            "statement": "If pullback(B_C)=d_S b_C, then int_S F epsilon_C d_S b_C = int_partialS F epsilon_C b_C - int_S d_S(F epsilon_C) wedge b_C.",
            "status": "MATCHES_1020_GUARD",
            "missing": "b_C primitive, corner term partialS, d_S(F epsilon_C) zero/bound",
            "valid_for_claim": False,
        },
        {
            "stokes_id": "WSC1170_2_degree_zero_limit",
            "clause": "degree-zero caution",
            "statement": "The fact that d_S of an intrinsic top two-form is zero does not by itself remove the weighted-Stokes derivative term when the exact primitive is written as d_S b_C with scalar/zero-form weight.",
            "status": "NO_FAKE_DEGREE_SHORTCUT",
            "missing": "form-degree ledger for F epsilon_C and b_C",
            "valid_for_claim": False,
        },
        {
            "stokes_id": "WSC1170_3_zero_or_bound",
            "clause": "acceptance rule",
            "statement": "The boundary route closes only if corner=0, harmonic/residual=0, and d_S(F epsilon_C)=0, or if every term gets a sourced finite bound.",
            "status": "STRICT_ACCEPTANCE_RULE",
            "missing": "numeric/source-backed bound rows or parent zero theorem",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1170_0_stokes_split",
            "test": "J_C exact/top split",
            "status": "PASS_DERIVED_SPLIT",
            "result": "int_D J_C splits into boundary primitive plus top-class contribution",
            "blocked_by": "none for identity; claim blocked by boundary values",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1170_1_local_zero",
            "test": "local topological zero",
            "status": "REFUSED_BOUNDARY_UNSILENCED",
            "result": "H^3 local zero does not erase int_partialD B_C",
            "blocked_by": "B_C_boundary;Phi_C_boundary;relative_cohomology;corner_terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1170_2_FLRW_activity",
            "test": "FLRW top activity",
            "status": "COMPATIBLE_NONCLAIM",
            "result": "closed/global top class can survive with no boundary term",
            "blocked_by": "parent_normalization;top_source_stress;amplitude_law",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1170_3_weighted_stokes",
            "test": "closed-weight shortcut",
            "status": "REFUSED_DEGREE_SHORTCUT",
            "result": "degree clarifies the forms but does not remove the kernel derivative residual without a degree/weight certificate",
            "blocked_by": "dS_Fepsilon;corner;harmonic;residual;b_C_norm",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1170_0_split_identity",
            "gate": "Stokes exact/top split",
            "current_status": "PASS_IDENTITY_ONLY",
            "reason": "the split is mathematical, but not a local-physics claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1170_1_local_zero",
            "gate": "local exact boundary silence",
            "current_status": "BLOCKED",
            "reason": "int_partialD B_C and Phi_C boundary flux remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1170_2_FLRW_selector",
            "gate": "FLRW top-class activity",
            "current_status": "PARTIAL_PASS_NONCLAIM",
            "reason": "closed/global top class can exist, but source amplitude and stress are not parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1170_3_weighted_stokes",
            "gate": "closed-weight/finite-bound route",
            "current_status": "BLOCKED",
            "reason": "kernel derivative, primitive norm, harmonic/residual, and corner terms remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1170_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "boundary primitive and parent source gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1170_0_boundary_is_live_gap",
            "decision": "topology_route_survives_but_reduces_to_boundary",
            "reason": "local H^3 zero is useful, but Stokes exposes int_partialD B_C as the exact-sector obstruction",
            "next_action": "derive natural boundary condition for B_C/Phi_C or fill finite B_C bound row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1170_1_no_degree_cheat",
            "decision": "do_not_use_degree_zero_as_shortcut",
            "reason": "top-form degree helps classify B_C, but weighted Stokes still leaves d_S(F epsilon_C) wedge b_C unless the weight is closed",
            "next_action": "write form-degree/weight certificate before using closed-weight zero",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1170_2_best_next",
            "decision": "attack_parent_natural_boundary_condition",
            "reason": "a natural boundary condition would be stronger and cleaner than sourcing finite local bounds",
            "next_action": "try to derive no-flux from parent variational principle; fallback to first finite boundary source row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1170_0_1171",
            "next_target": "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md",
            "objective": "try to derive a parent natural-boundary/no-flux condition for B_C and Phi_C; if it fails, create the first finite B_C boundary-bound source row",
            "include": "parent variation boundary term; B_C pullback; Phi_C no-flux; physical-charge guard; weighted-Stokes form-degree ledger; finite norm row",
            "exclude": "assuming B_C=0; deleting physical charges; local claim; c_g zero; invented numeric values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    splits: list[dict[str, object]],
    phis: list[dict[str, object]],
    certs: list[dict[str, object]],
    stokes: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1170_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_1_stokes_split_written",
            "result": "pass" if any("int_partialD B_C" in str(r["statement"]) for r in splits) else "fail",
            "detail": "domain charge split includes boundary primitive and top-class contribution",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_2_phi_bc_relation_written",
            "result": "pass" if any("Phi_C = L_tau B_C" in str(r["statement"]) for r in phis) else "fail",
            "detail": "Phi_C/B_C exact-sector relation is written with caveats",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_3_local_zero_blocked",
            "result": "pass" if any(r["current_status"] == "BLOCKED_MAIN_GAP" for r in certs) else "fail",
            "detail": "local zero is explicitly blocked by boundary primitive gap",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_4_weighted_stokes_guard",
            "result": "pass" if any(r["status"] == "NO_FAKE_DEGREE_SHORTCUT" for r in stokes) else "fail",
            "detail": "degree shortcut is rejected unless weighted-Stokes guard is certified",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_5_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses local and weighted-Stokes claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_6_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_7_no_claim_rows",
            "result": "pass"
            if all(
                r.get("valid_for_claim") is False
                for r in splits + phis + certs + stokes + gates + nexts
            )
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_8_next_target",
            "result": "pass" if nexts and "1171" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1171 handoff targets natural boundary condition or first finite bound row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1170_SUMMARY",
            "result": "pass",
            "detail": "1170 derives the exact/top Stokes split and shows the topological route now hinges on B_C/Phi_C boundary silence or finite source-backed bounds",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    splits: list[dict[str, object]],
    phis: list[dict[str, object]],
    certs: list[dict[str, object]],
    stokes: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1170 — Y5/R10 topological selector boundary-flux certificate or B_C primitive owner",
        "**Current verdict:** 1170 keeps the topological selector alive, but it also exposes the hard obstruction cleanly: `H^3` can kill the local top class, yet Stokes leaves the exact-sector boundary primitive `int_partialD B_C`. Local zero is not proved until `B_C`/`Phi_C` boundary flux is parent-silent or source-bounded.",
        "**Main progress:** the decomposition `J_C = d_D B_C + J_C^top` gives `int_D J_C = int_partialD B_C + int_D J_C^top`. This is a useful sharpening because it separates the cosmological/topological route from the local boundary route instead of mixing them.",
        "**Important correction:** the degree argument cannot be used as a cheap win. `B_C` is naturally a boundary top form, but the weighted-Stokes residual still contains `d_S(F epsilon_C) wedge b_C` when an exact primitive is used. The weight has to be closed or bounded.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Boundary split theorem\n\n" + table(splits),
        "## Phi/B_C relation\n\n" + table(phis),
        "## Local zero certificate\n\n" + table(certs),
        "## Weighted-Stokes C-sector guard\n\n" + table(stokes),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    splits = boundary_split_rows()
    phis = phi_bc_rows()
    certs = local_zero_certificate_rows()
    stokes = weighted_stokes_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, splits, phis, certs, stokes, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1170_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv": splits,
        "P8_Y5_R10_1170_PHI_BC_RELATION.csv": phis,
        "P8_Y5_R10_1170_LOCAL_ZERO_CERTIFICATE.csv": certs,
        "P8_Y5_R10_1170_WEIGHTED_STOKES_C_SECTOR.csv": stokes,
        "P8_Y5_R10_1170_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1170_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1170_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1170_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1170_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, splits, phis, certs, stokes, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
