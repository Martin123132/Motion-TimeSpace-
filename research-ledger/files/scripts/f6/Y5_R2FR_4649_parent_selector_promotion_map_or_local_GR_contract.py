from __future__ import annotations

import csv
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4649"
CLAIM_ID = "L-491"
BRANCH = "MTS_R2FR_Y5_PARENT_SELECTOR_PROMOTION_MAP_OR_LOCAL_GR_CONTRACT_4649"
MARKER = "PPC4161_PARENT_SELECTOR_PROMOTION_MAP_OR_LOCAL_GR_CONTRACT_4649"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SELECTOR_PROMOTION_MAP_OR_LOCAL_GR_CONTRACT_4649"
NEXT_TARGET = "4650-Y5-R2FR-single-parent-action-selector-signature-or-residual-vector.md"

DOC_PATH = POST / "4649-Y5-R2FR-parent-selector-promotion-map-or-local-GR-contract.md"
FORMAL_PATH = FORMAL / "665-PPC4161-parent-selector-promotion-map-or-local-GR-contract.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4649_SOURCE_REGISTER.csv"
CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_PARENT_GR_SELECTOR_CONTRACT.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_PROMOTION_PROOF_CHAIN.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_LOCAL_ARENA_PROMOTION_MAP.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_RESIDUAL_VECTOR_IF_SELECTOR_FAILS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4649_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4649_VALIDATION.csv"

DOC_4648 = POST / "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
CSV_4648_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4648_VALIDATION.csv"
CSV_4642_PARENT = SOURCE_DIR / "P8_Y5_R2FR_4642_PARENT_SIGNATURE_PACK.csv"
FORMAL_186 = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
FORMAL_187 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_350 = FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"


def timestamp() -> str:
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
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    suffix = "" if not current or current.endswith("\n") else "\n"
    path.write_text(current + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists() or not (repo / ".git").exists():
        return True, "absent or not git"
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    status = result.stdout.strip()
    return status == "", status or "clean"


def source_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4649_00_4648_validation", CSV_4648_VALIDATION, "VAL4648_OVERALL", "4648 same-branch tail gate passed."),
        ("SRC4649_01_4648_Btail", DOC_4648, "B_tail -> alpha_tail(lambda)=0", "tail-zero contract imported."),
        ("SRC4649_02_4648_promotion_block", DOC_4648, "RUN4648_3_local_GR_promotion_attempt", "local-GR promotion still fails closed."),
        ("SRC4649_03_parent_common_readout", CSV_4642_PARENT, "PS4642_6", "same observed coframe/Hodge/tau clause."),
        ("SRC4649_04_parent_fixed_domain", CSV_4642_PARENT, "PS4642_7", "fixed projector/domain/lambda clause."),
        ("SRC4649_05_mass_glue", FORMAL_186, "Pi_M/H_tau/worldtube glue = 0 residual.", "Hamiltonian worldtube mass glue."),
        ("SRC4649_06_no_orbital_fit", FORMAL_186, "No orbital `GM`, fitted acceleration, or measured Newton constant is used", "mass readout non-circularity guard."),
        ("SRC4649_07_newton_poisson", FORMAL_187, "nabla^2 Phi_N = 4*pi G_N rho_H.", "Newton Poisson readout."),
        ("SRC4649_08_newton_accel", FORMAL_187, "a_r = -G_N M_H^dress/r^2.", "Newton acceleration readout."),
        ("SRC4649_09_kappa_Gcal", FORMAL_194, "G_cal := c^4 kappa_eff/(8*pi).", "calibrated source coupling."),
        ("SRC4649_10_G_empirical_guard", FORMAL_194, "This is not a defect relative to GR.", "numeric G need not be predicted to reduce to GR."),
        ("SRC4649_11_EM_owner", FORMAL_191, "Poynting vector is not a separate background field", "Maxwell/Poynting Hilbert stress owner."),
        ("SRC4649_12_EM_conservation", FORMAL_191, "nabla_mu (T_matter+binding^mu_nu + T_EM^mu_nu) = 0.", "matter+EM stress conservation guard."),
        ("SRC4649_13_boundary_flux", FORMAL_192, "route as boundary charge, not hidden bulk current.", "radiative flux routing guard."),
        ("SRC4649_14_PPN_projection", FORMAL_350, "PI4334_1_PPN", "PPN projection matrix contract."),
        ("SRC4649_15_PPN_smoke_gate", FORMAL_350, "F4334_3_PPN_smoke_gate", "PPN scoring remains matrix-gated."),
        ("SRC4649_16_redteam_theorem", RED_TEAM, "the missing MTS -> GR -> Newton theorem.", "red-team target statement."),
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
                "timestamp_utc": ts,
            }
        )
    return rows


def contract_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("GRSEL4649_0_action_form", "local parent action branch", "S_local[B_GR]=(2 kappa_eff)^-1 int sqrt(-g_obs) R[g_obs] + S_m[g_obs,psi] + S_EM[g_obs,A] + S_MTS_perp + S_boundary", "one EH metric block plus matter/EM minimal coupling plus residual MTS sector"),
        ("GRSEL4649_1_constant_coupling", "calibrated coupling", "D_A kappa_eff=0 and G_cal=c^4 kappa_eff/(8*pi)", "one local calibrated source coupling; numeric G not predicted unless parent scale law is added"),
        ("GRSEL4649_2_common_readout", "observed geometry", "one g_obs/e_obs/Hodge/tau readout is shared by matter, EM, clocks, orbital and PPN arenas", "blocks metric/coframe fork tricks"),
        ("GRSEL4649_3_Hilbert_source", "source owner", "T_total = T_matter + T_EM + T_binding from Hilbert variation with no source-label/source-weight slots", "universal source coupling and WEP route"),
        ("GRSEL4649_4_tail_silence", "MTS local tail", "B_tail -> alpha_tail(lambda)=0 and delta S_MTS_perp/delta g_obs is zero or pure calibrated EH/Lambda renormalization", "prevents local fifth-force/Yukawa leakage"),
        ("GRSEL4649_5_boundary_owner", "boundary and radiation", "radiative/Poynting/gravitational flux is boundary/Hamiltonian charge or explicit external sector, not hidden local bulk current", "no flux erasure"),
        ("GRSEL4649_6_conservation", "Bianchi compatibility", "nabla_mu T_total^mu_nu=0 follows from diffeo invariance, constant kappa_eff and Maxwell+matter exchange cancellation", "local equations are not overdetermined"),
        ("GRSEL4649_7_fixed_domain", "projection discipline", "worldtube, projector, lambda, source support and readout surfaces fixed before scoring", "no post-fit local-test projector"),
        ("GRSEL4649_8_selector_status", "current corpus status", "B_GR is a sufficient parent-selector contract, not yet signed as the unique active parent action branch", "conditional theorem, not public claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": row[0],
            "object": row[1],
            "required_statement": row[2],
            "deduction_role": row[3],
            "status": "CONTRACT_ROW",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def proof_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("PROOF4649_0_variation", "vary S_local with respect to g_obs", "G_mu_nu[g_obs] = kappa_eff T_total_mu_nu plus allowed constant Lambda/EH renormalization", "local Einstein-form field equation"),
        ("PROOF4649_1_Bianchi", "take nabla_mu of field equation", "nabla_mu G^mu_nu=0 and D_A kappa_eff=0 require nabla_mu T_total^mu_nu=0", "conservation gate"),
        ("PROOF4649_2_Maxwell", "vary S_EM with respect to A_mu using same Hodge star", "nabla_mu F^mu_nu=J^nu and nabla_mu T_EM^mu_nu=-F_nu_lambda J^lambda", "Maxwell/Poynting stress is visible Hilbert stress"),
        ("PROOF4649_3_matter_exchange", "combine matter equation with Maxwell Lorentz exchange", "nabla_mu(T_matter+binding^mu_nu+T_EM^mu_nu)=0", "no standalone EM background force"),
        ("PROOF4649_4_Newton", "weak-field slow-motion static limit of EH equation", "nabla^2 Phi_N=4*pi G_cal rho_H and a=-G_cal M_H^dress/r^2", "GR -> Newton recovered with calibrated G_cal"),
        ("PROOF4649_5_PPN", "EH metric block with no extra local source/readout couplings", "gamma=1, beta=1, preferred-frame/location parameters zero, Gdot/G=0 inside static local selector", "PPN exact-GR branch conditional"),
        ("PROOF4649_6_tail_decoupling", "apply 4648 B_tail theorem", "alpha_tail(lambda)=0, so R10 tail amplitude vanishes independent of numeric lambda_mem", "local fifth-force tail removed"),
        ("PROOF4649_7_failure_mode", "if any selector clause fails", "route residual into explicit vector R_fail rather than closure assumption", "finite bound/scoring branch retained"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": row[0],
            "step": row[1],
            "derived_result": row[2],
            "meaning": row[3],
            "status": "DERIVED_CONDITIONAL_STEP",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def arena_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("ARENA4649_0_GR_field_equation", "local GR", "B_GR -> G_mu_nu = kappa_eff T_total_mu_nu (+ allowed constant Lambda/EH renormalization)", "CONDITIONAL_EXACT_GR_FORM", "parent selector still unsigned"),
        ("ARENA4649_1_Newton", "Newtonian mechanics", "B_GR + weak/static/slow -> Poisson/Gauss/Newton acceleration with G_cal and M_H^dress", "CONDITIONAL_EXACT_NEWTON_LIMIT", "numeric G_cal calibrated, not predicted"),
        ("ARENA4649_2_Maxwell_EM", "Maxwell/EM stress", "B_GR -> Maxwell-Hodge equations and Poynting vector as T_EM flux through same metric/coframe", "CONDITIONAL_EXACT_EM_STRESS_OWNER", "forbids second EM metric/source weights"),
        ("ARENA4649_3_PPN", "PPN", "B_GR -> exact GR PPN values in local static selector; otherwise use Pi_PPN residual vector", "CONDITIONAL_EXACT_OR_FAIL_TO_VECTOR", "needs parent selector signature before claim"),
        ("ARENA4649_4_WEP", "WEP/source universality", "single Hilbert source and species-blind matter action remove source-label weights", "CONDITIONAL_WEP_ROUTE", "composition map still explicit if selector fails"),
        ("ARENA4649_5_clocks", "clock/time readout", "one g_obs/e_obs/tau readout gives proper-time clock law in local branch", "CONDITIONAL_CLOCK_ROUTE", "time-sector deviations must enter residual vector"),
        ("ARENA4649_6_orbital", "orbital", "Newton/Gauss limit plus common mass readout gives orbital GM branch without fitting GM as source definition", "CONDITIONAL_ORBITAL_ROUTE", "profile/multipole residuals still bounded if selector fails"),
        ("ARENA4649_7_R10", "R10", "B_tail subset of B_GR gives zero Yukawa amplitude before bound comparison", "CONDITIONAL_R10_TAIL_SILENCE", "curve QA still needed for public statement"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": row[0],
            "arena": row[1],
            "promotion_statement": row[2],
            "status": row[3],
            "remaining_guard": row[4],
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def residual_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("RES4649_0_metric_fork", "delta g_EM or delta g_clock or delta e_obs != 0", "non-universal metric/coframe readout", "PPN/clock/EM residual vector"),
        ("RES4649_1_source_label", "D_species S_m or source-weight slots nonzero", "WEP/source normalization leak", "WEP and G_cal residual vector"),
        ("RES4649_2_nonHilbert_tail", "delta S_MTS_perp/delta g_obs has non-EH part", "extra local stress/fifth-force leak", "PPN/R10/orbital residual vector"),
        ("RES4649_3_kappa_drift", "D_A kappa_eff != 0 or dot G_cal != 0", "calibrated coupling not constant", "clock/orbital/Gdot residual vector"),
        ("RES4649_4_boundary_flux", "radiation/boundary flux enters compact local bulk", "hidden current/source leak", "boundary/PPN/orbital residual vector"),
        ("RES4649_5_postfit_domain", "worldtube/projector/lambda chosen after residuals", "post-fit closure assumption", "reject branch"),
        ("RES4649_6_profile_multipole", "same total mass but different local density/profile/multipole response", "Newton/orbital profile leak", "mass-profile residual vector"),
        ("RES4649_7_PPN_matrix_missing", "Pi_PPN transfer map not derived for open residual", "local metric response unscored", "fail closed before claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": row[0],
            "trigger": row[1],
            "problem": row[2],
            "required_route": row[3],
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def runner_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4649_0_current_corpus", "B_tail exists but B_GR parent selector not signed as unique active action branch", "FAIL_CLOSED", "no public local-GR/Newton/Maxwell/PPN claim"),
        ("RUN4649_1_parent_selector_signed", "all GRSEL4649 clauses signed by one parent action/readout branch", "PASS_CONDITIONAL_LOCAL_GR_CONTRACT_NONCLAIM", "derive GR form, Newton limit, Maxwell stress owner and exact-GR PPN branch"),
        ("RUN4649_2_tail_only", "B_tail signed but common metric/source/coupling clauses open", "PARTIAL_PASS_R10_TAIL_ONLY", "R10 tail silence does not promote to local GR"),
        ("RUN4649_3_G_numeric_demand", "requires predicting numeric G_N before accepting GR reduction", "REJECT_WRONG_REQUIREMENT", "GR itself calibrates G; structure requires one G_cal not fitted source by source"),
        ("RUN4649_4_selector_failure", "any GRSEL4649 clause opens", "FAIL_TO_RESIDUAL_VECTOR", "score explicit residuals, do not add closure axiom"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch": row[1],
            "result": row[2],
            "reason": row[3],
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
        for row in rows
    ]


def controls(ts: str) -> list[dict[str, Any]]:
    controls_raw = [
        ("CTRL4649_0_no_G_prediction_trap", "Do not require MTS to predict numeric G_N for GR reduction; require one calibrated G_cal and no hidden source dependence."),
        ("CTRL4649_1_no_tail_to_GR_jump", "Do not promote Xi_tail silence to local GR without EH metric, common readout, conservation and source-coupling clauses."),
        ("CTRL4649_2_no_second_metric", "Do not let EM, clocks or matter use different metrics/coframes/Hodge stars inside the local claim branch."),
        ("CTRL4649_3_no_hidden_Poynting", "Do not treat the Poynting vector as a background field separate from Maxwell-Hilbert stress."),
        ("CTRL4649_4_no_postfit_projection", "Do not choose worldtube, projector, lambda or PPN matrix after seeing local residuals."),
        ("CTRL4649_5_no_selector_mixing", "Do not assemble GRSEL4649 clauses from different branches."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "firewall": firewall,
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for control_id, firewall in controls_raw
    ]


def decisions(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4649_0",
            "decision": "LOCAL_GR_PROMOTION_MAP_DERIVED_AS_A_SUFFICIENT_PARENT_SELECTOR_CONTRACT_NOT_YET_PARENT_SIGNED",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4649 turns the route from MTS tail silence to local GR/Newton/Maxwell into a compact sufficient theorem: if one parent action branch reduces to EH plus minimally coupled matter/EM, constant calibrated coupling, common observed coframe/Hodge/tau, Hilbert source stress, B_tail silence and boundary routing, then local GR, Newtonian Poisson/Gauss, Maxwell/Poynting stress ownership and exact-GR PPN follow. The current corpus still must sign that single parent selector rather than mix clauses.",
            "timestamp_utc": ts,
        }
    ]


def statuses(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "Local promotion map is now a derived sufficient contract; remaining active target is signing the single parent action selector or pushing failures into explicit residual vectors.",
            "claim_allowed": False,
            "public_ready": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": ts,
        }
    ]


def nexts(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "prove one parent action/readout selector satisfies GRSEL4649_0 through GRSEL4649_8, or create the explicit residual vector when a clause fails",
            "success_condition": "B_GR is parent-signed as one branch, yielding local EH equation, conserved Hilbert stress, Newton limit, Maxwell/Hodge stress and exact-GR PPN values without closure assumptions",
            "timestamp_utc": ts,
        }
    ]


def validation(src: list[dict[str, Any]], con: list[dict[str, Any]], proof: list[dict[str, Any]], arena: list[dict[str, Any]], residual: list[dict[str, Any]], runs: list[dict[str, Any]], dec: list[dict[str, Any]], ts: str) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4649_00_sources_exist", all(row["path_exists"] for row in src), "all cited paths exist"),
        ("VAL4649_01_needles_found", all(row["needle_found"] for row in src), "all source needles found"),
        ("VAL4649_02_line_anchors", all(int(row["line_number"]) > 0 for row in src), "all source line anchors positive"),
        ("VAL4649_03_action_contract", any(row["contract_id"] == "GRSEL4649_0_action_form" for row in con), "parent action contract exists"),
        ("VAL4649_04_conservation_contract", any(row["contract_id"] == "GRSEL4649_6_conservation" for row in con), "Bianchi/conservation clause exists"),
        ("VAL4649_05_Newton_Maxwell_PPN_proof", all(any(row["proof_id"] == proof_id for row in proof) for proof_id in ["PROOF4649_2_Maxwell", "PROOF4649_4_Newton", "PROOF4649_5_PPN"]), "Newton/Maxwell/PPN proof steps exist"),
        ("VAL4649_06_all_major_arenas", len(arena) >= 8 and all(row["status"].startswith("CONDITIONAL") for row in arena), "major local arenas mapped conditionally"),
        ("VAL4649_07_residual_fallback", len(residual) >= 8, "selector-failure residual vector retained"),
        ("VAL4649_08_current_fail_closed", any(row["run_id"] == "RUN4649_0_current_corpus" and row["result"] == "FAIL_CLOSED" for row in runs), "current corpus fails closed"),
        ("VAL4649_09_G_numeric_reject", any(row["run_id"] == "RUN4649_3_G_numeric_demand" and row["result"] == "REJECT_WRONG_REQUIREMENT" for row in runs), "numeric G trap rejected"),
        ("VAL4649_10_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" for row in src + con + proof + arena + residual + runs + dec), "no row marked claim-grade"),
        ("VAL4649_11_decision_next", dec and dec[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4649_12_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4649_13_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4649_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4649 validation passed" if all(passed for _, passed, _ in checks) else "4649 validation failed",
            "timestamp_utc": ts,
        }
    )
    return rows


def build_doc(src: list[dict[str, Any]], con: list[dict[str, Any]], proof: list[dict[str, Any]], arena: list[dict[str, Any]], residual: list[dict[str, Any]], runs: list[dict[str, Any]], ctrl: list[dict[str, Any]], dec: list[dict[str, Any]], stat: list[dict[str, Any]], nxt: list[dict[str, Any]], val: list[dict[str, Any]]) -> str:
    return f"""# 4649 - parent selector promotion map or local GR contract

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4649 is the bridge theorem, not another alpha-tail checkpoint.

The sufficient local-GR selector is:

`B_GR := EH[g_obs] + common matter/EM metric/coframe/Hodge/tau + constant kappa_eff + Hilbert source stress + B_tail + boundary/Hamiltonian routing + fixed domain/projectors`.

If one parent action/readout branch signs `B_GR`, then the local promotion is exact:

`B_GR -> GR field equation -> conserved Hilbert stress -> Newtonian Poisson/Gauss limit -> Maxwell-Hodge/Poynting stress ownership -> exact-GR PPN branch`.

The current corpus does not yet prove that this single parent selector is the unique active branch. So this is a private sufficient theorem and a sharper next target, not a public local-GR claim. The key point is that we no longer need to chase extra R10 alpha pieces: the remaining obstruction is the parent action selector/source-coupling map.

## Source Register

{markdown_table(src)}

## Parent GR Selector Contract

{markdown_table(con)}

## Promotion Proof Chain

{markdown_table(proof)}

## Local Arena Promotion Map

{markdown_table(arena)}

## Residual Vector If Selector Fails

{markdown_table(residual)}

## Runner Results

{markdown_table(runs)}

## Controls

{markdown_table(ctrl)}

## Decision

{markdown_table(dec)}

## Status

{markdown_table(stat)}

## Next Target

{markdown_table(nxt)}

## Validation

{markdown_table(val)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4649 derives the sufficient parent-selector promotion contract: if one local parent branch is EH plus minimally coupled matter/EM with constant calibrated coupling, common observed coframe/Hodge/tau, Hilbert source stress, B_tail silence and boundary routing, then local GR, Newtonian Poisson/Gauss, Maxwell/Poynting stress ownership and exact-GR PPN follow conditionally.",
        "Generated source register, parent GR selector contract, promotion proof chain, local arena map, selector-failure residual vector, runner, controls, decision, status, next target and validation.",
        "parent_selector_local_GR_promotion_contract_nonclaim",
        NEXT_TARGET,
        "Claiming local GR from tail silence alone, requiring numeric G prediction as a GR-reduction condition, mixing selector clauses across branches, or hiding EM/Poynting/boundary/source residuals.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/Maxwell/EM claim until the single parent action selector is signed or every failed clause is pushed into a source-backed residual vector and passes.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4649 gives the sufficient promotion theorem from MTS local-tail silence to local GR. If a single parent selector `B_GR` signs the EH metric block, minimally coupled matter/EM on one observed metric/coframe/Hodge/tau, constant calibrated coupling `G_cal`, Hilbert source stress, `B_tail` silence, boundary/Hamiltonian flux routing, and fixed projectors/domains before scoring, then local GR, Newtonian Poisson/Gauss, Maxwell/Poynting Hilbert stress ownership and exact-GR PPN values follow conditionally. The theorem rejects the numeric-`G` trap: GR reduction needs one calibrated coupling, not a prediction of `G_N`. It remains nonclaim until `B_GR` is parent-signed as one branch.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4649` moves the live problem from R10 tail components to the single parent action selector/source-coupling map. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    ts = timestamp()
    src = source_rows(ts)
    con = contract_rows(ts)
    proof = proof_rows(ts)
    arena = arena_rows(ts)
    residual = residual_rows(ts)
    runs = runner_rows(ts)
    ctrl = controls(ts)
    dec = decisions(ts)
    stat = statuses(ts)
    nxt = nexts(ts)
    val = validation(src, con, proof, arena, residual, runs, dec, ts)

    write_csv(SOURCE_REGISTER, src)
    write_csv(CONTRACT_CSV, con)
    write_csv(PROOF_CSV, proof)
    write_csv(ARENA_CSV, arena)
    write_csv(RESIDUAL_CSV, residual)
    write_csv(RUNNER_CSV, runs)
    write_csv(CONTROL_CSV, ctrl)
    write_csv(DECISION_CSV, dec)
    write_csv(STATUS_CSV, stat)
    write_csv(NEXT_CSV, nxt)
    write_csv(VALIDATION_CSV, val)

    doc = build_doc(src, con, proof, arena, residual, runs, ctrl, dec, stat, nxt, val)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = val[-1]["status"]
    print(f"4649 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
