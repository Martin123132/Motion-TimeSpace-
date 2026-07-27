from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4125-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_COMMON_BETA_ZERO_CURRENT_SPINE_4125"
CHECKPOINT_ID = "4125"
DECISION = "COMMON_BETA_ZERO_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4125_00_4124_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4124_NEXT_TARGET.csv",
        "4125-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md",
        "4124 selected common beta as next pressure point.",
    ),
    "SRC4125_01_4124_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4124_STATUS.csv",
        "NO_MARKER_THEOREM_UNSIGNED_BETAXZ_COMPONENT_PACK_FILLED_ABSOLUTE_ENVELOPE_ACTIVE",
        "Current-chain no-marker beta component pack handoff.",
    ),
    "SRC4125_02_4124_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_4124_BETAXZ_COMPONENT_PACK.csv",
        "BETA4124_X_0_beta_common",
        "Current-chain beta_common component rows.",
    ),
    "SRC4125_03_4124_envelope": (
        SOURCE_DIR / "P8_Y5_R2FR_4124_BETAXZ_ABSOLUTE_ENVELOPE.csv",
        "ENV4124_Z_2_eta_bound_rule",
        "Current-chain absolute-envelope guard.",
    ),
    "SRC4125_04_3639_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_STATUS.csv",
        "COMMON_BETA_ZERO_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_FILLED",
        "Older common-beta source-normalization runner.",
    ),
    "SRC4125_05_3639_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_COMMON_BETA_IDENTITY.csv",
        "ID3639_0_master_common_beta",
        "Older common beta identity.",
    ),
    "SRC4125_06_3639_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_COMMON_BETA_ZERO_PROOF_AUDIT.csv",
        "CB3639_4_verdict",
        "Older common-beta zero proof audit.",
    ),
    "SRC4125_07_3639_observable": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_COMMON_BETA_OBSERVABLE_ROWS.csv",
        "R10_short_range",
        "Older common-beta observable maps.",
    ),
    "SRC4125_08_3639_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
        "SNR3639_2_common_wEP_guard",
        "Older source-normalization runner rows.",
    ),
    "SRC4125_09_3639_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3639_NEXT_TARGET.csv",
        "3640-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md",
        "Older next target selecting Ward identity/bound fill.",
    ),
    "SRC4125_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4125_common_beta_zero_or_source_normalization_runner.py",
        "Reproducible generator for this 4125 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def identity_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("ID4125_0_master_common_beta_X", "beta_common_X", "beta_common_X=X_N[ln mu_obs_common]=X_N[ln G_eff]+X_N[ln M_eff]+X_N[ln(1+epsilon_mu)]", "dimensionless per normalized X_N", "source_normalization;R10;PPN;Gdot;radial_source_hair;clock_common_mode;EM_common_mode", "EXACT_DECOMPOSITION_NO_ZERO_CLAIM"),
        ("ID4125_1_master_common_beta_Z", "beta_common_Z", "beta_common_Z=Z_N[ln mu_obs_common]=Z_N[ln G_eff]+Z_N[ln M_eff]+Z_N[ln(1+epsilon_mu)]", "dimensionless per normalized Z_N", "source_normalization;R10;PPN;Gdot;radial_source_hair;clock_common_mode;EM_common_mode", "EXACT_DECOMPOSITION_NO_ZERO_CLAIM"),
        ("ID4125_2_time_projection", "dot_mu_over_mu", "d ln mu_obs_common/dt = beta_common_A * dA_N/dt + explicit_t[ln G_eff M_eff(1+epsilon_mu)]", "time^-1", "Gdot;clock_common_mode;ephemeris", "REQUIRES_ADOT_OR_PARENT_ZERO"),
        ("ID4125_3_radial_projection", "partial_r_ln_mu", "partial_r ln mu_obs_common = beta_common_A * partial_r A_N + explicit_r[ln G_eff M_eff(1+epsilon_mu)]", "length^-1", "orbital;inverse_square;R10_range", "REQUIRES_PROFILE_OR_PARENT_ZERO"),
        ("ID4125_4_wep_null_space", "eta_source_AB", "eta_source_AB sees Delta beta_AB, not beta_common_A; beta_common lies in the WEP null direction.", "dimensionless", "WEP_guard", "WEP_CANNOT_CLOSE_COMMON_MODE"),
        ("ID4125_5_em_common", "EM_common_beta", "d ln EM_obs_common = beta_common_A^EM dA_N + explicit EM calibration residuals", "dimensionless or flux-normalized", "EM;Maxwell;Poynting;source_calibration", "EM_COMMON_MODE_LIVE"),
    ]
    for identity_id, symbol, identity, units, observable_link, status in data:
        row = row_base()
        row.update(
            {
                "identity_id": identity_id,
                "symbol": symbol,
                "identity": identity,
                "units": units,
                "observable_link": observable_link,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def proof_audit_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "CB4125_0_definition",
            "beta_common_A := A_N[ln mu_obs] for the species-blind part of mu_obs.",
            "beta_A^m=beta_common_A+delta_beta_A^m and Delta beta_A_mn=delta_beta_A^m-delta_beta_A^n.",
            "definition inherited from 4124 component pack.",
            "DERIVED_IDENTITY",
            "definition alone does not set beta_common_A to zero.",
        ),
        (
            "CB4125_1_quotient_zero_route",
            "If mu_obs=mu_bar(q(Phi)) and A_N in ker(Dq), then beta_common_A=A_N[ln mu_bar(q(Phi))]=0.",
            "A_N[ln mu_obs]=D ln(mu_bar)[Dq(A_N)]=0.",
            "parent signs mu_obs as quotient-owned q-data and A_N as vertical to q-map.",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "measured-GM/source-normalization derivatives remain live residuals.",
        ),
        (
            "CB4125_2_unit_gauge_route",
            "A common source scaling is unobservable only if it is pure calibration gauge.",
            "delta ln G_eff + delta ln M_eff + delta ln(1+epsilon_mu)=0 as parent Ward/gauge identity.",
            "parent action supplies a scale/source-normalization Noether identity, not fitted cancellation.",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "absolute G normalization can be calibration-only, but derivatives need a theorem.",
        ),
        (
            "CB4125_3_scalar_tensor_guard",
            "Universal coupling can pass WEP but still fail PPN/R10/Gdot.",
            "species-blind beta_common cancels from Delta beta_AB, but beta_common^2 contributes to finite-range/PPN/common-source channels.",
            "beta_common=0, infinite mass/range suppression, or numeric bound rows.",
            "COMMON_MODE_NOT_WEP_ERASED",
            "differential WEP is the wrong lock for universal source coupling.",
        ),
        (
            "CB4125_4_em_guard",
            "Universal EM/Poynting source calibration can pass composition WEP while affecting Maxwell/source channels.",
            "beta_common_EM may be species-blind but nonzero.",
            "EM quotient descent, EM common beta zero, or separate EM bound rows.",
            "EM_COMMON_MODE_NOT_WEP_ERASED",
            "EM common mode needs its own theorem/bound row.",
        ),
        (
            "CB4125_5_verdict",
            "The common-beta zero proof cannot be claimed from the current parent corpus.",
            "beta_common_X/Z remain source-normalization residuals with exact observable maps.",
            "next checkpoint must sign Ward/source-normalization identity or fill arena bounds.",
            "ZERO_PROOF_UNSIGNED_OBSERVABLE_RUNNER_FILLED",
            "the route is sharpened into theorem contract, but parent signature is absent.",
        ),
    ]
    for proof_id, claim, relation, closure, status, why in data:
        row = row_base()
        row.update(
            {
                "proof_id": proof_id,
                "claim": claim,
                "derived_relation": relation,
                "closure_condition": closure,
                "status": status,
                "why_not_closed": why,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def observable_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("R10_short_range", "alpha_common(lambda)", "alpha_common(lambda)=K_A beta_common_source beta_common_test tau_R10(lambda)/M_A^2", "for every lambda: |alpha_common(lambda)|<=alpha_bound(lambda), or beta_common=0 by theorem", "K_A;M_A^2;tau_R10(lambda);beta_common_source;beta_common_test;real alpha_bound(lambda)", "NONCLAIM_SYMBOLIC_MAP_FILLED"),
        ("PPN_local_GR", "PPN_residual_vector_common", "Delta_PPN_common~(gamma-1,beta_PPN-1,alpha_i,zeta_i) sourced by beta_common^2 and derivatives", "PPN vector below bounds or parent theorem beta_common=0", "local propagator normalization; beta_common local value; derivative beta'_common; mapping to standard PPN gauge", "NONCLAIM_PPN_MAP_FILLED"),
        ("Gdot_clock", "dln_mu_obs_dt", "dln_mu_obs_dt=beta_common_A Adot_N + explicit_t residuals", "absolute drift below clock/ephemeris bounds or parent time-superselection theorem", "Adot_N local; clock sensitivity map; ephemeris convention; source mass standard", "NONCLAIM_DRIFT_MAP_FILLED"),
        ("orbital_radial", "radial_source_hair", "a_r=-mu_obs(r)/r^2 with partial_r ln mu_obs=beta_common_A partial_r A_N+explicit_r residuals", "no radial profile outside compact support or profile below orbital residual bounds", "A_N(r);source boundary condition;orbital residual covariance;calibrated mu at reference radius", "NONCLAIM_RADIAL_MAP_FILLED"),
        ("source_normalization", "calibration_null_or_physical_beta", "beta_common is gauge only if delta ln mu_obs_common is parent-owned calibration transformation with zero observable derivatives", "signed Ward/superselection identity or explicit residual branch", "parent scale symmetry;measure/coframe descent;boundary silence;calibration convention", "THEOREM_CONTRACT_NOT_SIGNED"),
        ("EM_common_mode", "EM_source_common_beta", "J_EM_common~beta_common_EM T_EM or Poynting/boundary projection", "EM common beta zero by quotient descent or bounded by EM/source observable", "EM stress normalization;Poynting projector;boundary flux;Maxwell limit", "NONCLAIM_EM_MAP_FILLED"),
    ]
    for arena, observable, skeleton, pass_condition, needed, status in data:
        row = row_base()
        row.update(
            {
                "arena": arena,
                "observable": observable,
                "prediction_skeleton": skeleton,
                "pass_condition": pass_condition,
                "needed_inputs": needed,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def source_runner_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("SNR4125_0_calibrated_mu", "mu_obs_common", "mu_obs_common:=G_eff M_eff(1+epsilon_mu)", "A_N[mu_obs_common]=0 because mu_obs_common descends through q or is pure calibration gauge", "retain beta_common and project to R10/PPN/Gdot/radial/EM rows", "q owns measured source normalization; no hidden boundary/projector source term", "ACTIVE_FORK"),
        ("SNR4125_1_no_cancellation", "beta_common_zero", "A_N ln G_eff + A_N ln M_eff + A_N ln(1+epsilon_mu)=0", "accepted only if Ward identity forces the sum to vanish termwise or as symmetry identity", "ordinary cancellation between terms is tuning and not claim-valid", "scale/source-normalization Noether identity with units and boundary terms", "NO_TUNED_CANCELLATION_ALLOWED"),
        ("SNR4125_2_common_wEP_guard", "WEP_null_direction", "Delta beta_AB=0 while beta_common!=0 is allowed", "not available from differential WEP alone", "common mode must be tested by R10/PPN/Gdot/radial/EM channels", "independent common source-current silence theorem", "WEP_NOT_SUFFICIENT"),
        ("SNR4125_3_em_common_guard", "EM_common_mode", "Delta beta_material=0 while beta_common_EM!=0 is allowed", "not available from material WEP alone", "EM common mode must be tested by Maxwell/source/flux channels", "independent EM quotient/source theorem", "EM_WEP_NOT_SUFFICIENT"),
    ]
    for runner_id, target, equation, zero_route, failure_route, required, status in data:
        row = row_base()
        row.update(
            {
                "runner_id": runner_id,
                "target": target,
                "equation": equation,
                "zero_route": zero_route,
                "failure_route": failure_route,
                "required_parent_signature": required,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        ("DEC4125_0_zero_not_claimed", "Do not claim beta_common_X/Z=0 from the current corpus.", "ZERO_PROOF_UNSIGNED", "attempt parent Ward/source-normalization identity next."),
        ("DEC4125_1_runner_filled", "Keep beta_common_X/Z as source-normalization residuals with explicit arena equations.", "OBSERVABLE_RUNNER_FILLED", "carry rows into R10/PPN/Gdot/radial/EM bound fill if Ward identity fails."),
        ("DEC4125_2_wep_guard", "Differential WEP is not a common-mode source-coupling test.", "WEP_NULL_GUARD_LOCKED", "do not use eta_source_AB pass as local-GR/source-normalization pass."),
        ("DEC4125_3_next", "Next target is parent source-normalization Ward identity or beta_common bound fill.", "WARD_IDENTITY_NEXT", "derive Ward identity or fill arena bound rows."),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4125_0",
            "target_doc": "4126-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_4126_parent_source_normalization_ward_identity_or_beta_common_bound_fill.py",
            "objective": "attempt to derive the Ward/source-normalization identity A_N ln mu_obs_common=0 from the parent action, including measure, coframe, connection, boundary, calibration, and EM/source terms; if unsigned, fill numeric/symbolic beta_common bound rows for R10, PPN, Gdot, radial/orbital, clock, and EM arenas",
            "success_gate": "beta_common_X/Z=0 is parent-signed, or every arena has explicit nonclaim beta_common rows with units, source paths, required coefficients, and bound inputs",
            "reason": "4125 maps common beta into all live local-test arenas; the remaining fork is parent Ward identity versus bound fill.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4125_0",
            "result": DECISION,
            "summary": (
                "4125 attempts the common-beta zero proof. The exact quotient route and pure-calibration/Ward route are written, "
                "but neither is parent-signed, so beta_common_X/Z remain live. The useful advance is that common beta is mapped "
                "into R10, PPN, Gdot/clock, radial/orbital, source-normalization, and EM common-mode equations."
            ),
            "common_beta_zero_signed": "False",
            "observable_runner_filled": "True",
            "wep_null_guard_active": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM, or source-normalization pass",
            "next_target": "4126 parent source-normalization Ward identity or beta common bound fill",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4125_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4125_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4125_COMMON_BETA_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4125_COMMON_BETA_IDENTITY.csv",
        "P8_Y5_R2FR_4125_COMMON_BETA_ZERO_PROOF_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4125_COMMON_BETA_ZERO_PROOF_AUDIT.csv",
        "P8_Y5_R2FR_4125_COMMON_BETA_OBSERVABLE_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4125_COMMON_BETA_OBSERVABLE_ROWS.csv",
        "P8_Y5_R2FR_4125_SOURCE_NORMALIZATION_RUNNER_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4125_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
        "P8_Y5_R2FR_4125_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4125_DECISION_GATES.csv",
        "P8_Y5_R2FR_4125_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4125_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4125_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4125_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4125 - Common Beta Zero or Source-Normalization Runner",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Common beta zero route is exact but unsigned: quotient descent or pure calibration/Ward identity would close it.",
        "- Common beta now has explicit nonclaim maps into R10, PPN, Gdot/clock, radial/orbital, source-normalization, and EM.",
        "- Differential WEP cannot close this branch; common beta lives in the WEP null direction.",
        "- No local-GR/source-normalization pass is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Common Beta Identity", "", "| identity_id | symbol | status |", "|---|---|---|"])
    for row in identity_rows():
        sections.append(f"| {row['identity_id']} | {row['symbol']} | {row['status']} |")
    sections.extend(["", "## Zero Proof Audit", "", "| proof_id | status | why_not_closed |", "|---|---|---|"])
    for row in proof_audit_rows():
        sections.append(f"| {row['proof_id']} | {row['status']} | {row['why_not_closed']} |")
    sections.extend(["", "## Observable Maps", "", "| arena | observable | status |", "|---|---|---|"])
    for row in observable_rows():
        sections.append(f"| {row['arena']} | {row['observable']} | {row['status']} |")
    sections.extend(["", "## Next Target", "", "- `4126-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md`", "- Derive the parent Ward/source-normalization identity, or fill arena-specific beta_common bound rows.", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4125_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4125_COMMON_BETA_IDENTITY": identity_rows,
        "P8_Y5_R2FR_4125_COMMON_BETA_ZERO_PROOF_AUDIT": proof_audit_rows,
        "P8_Y5_R2FR_4125_COMMON_BETA_OBSERVABLE_ROWS": observable_rows,
        "P8_Y5_R2FR_4125_SOURCE_NORMALIZATION_RUNNER_ROWS": source_runner_rows,
        "P8_Y5_R2FR_4125_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4125_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4125_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4125_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4125_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4125_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    identity_text = flatten_rows([outputs["P8_Y5_R2FR_4125_COMMON_BETA_IDENTITY"]])
    identity_ok = all(token in identity_text for token in ["beta_common_X", "beta_common_Z", "Gdot", "radial", "EM_common"])
    add("VAL4125_3_identity", "identity rows include X/Z common beta, Gdot, radial, and EM common mode", identity_ok, "identity tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4125_COMMON_BETA_ZERO_PROOF_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "COMMON_MODE_NOT_WEP_ERASED", "EM_COMMON_MODE_NOT_WEP_ERASED", "ZERO_PROOF_UNSIGNED"])
    add("VAL4125_4_audit", "proof audit blocks zero claim and keeps WEP/EM guards", audit_ok, "audit tokens checked")

    observable_text = flatten_rows([outputs["P8_Y5_R2FR_4125_COMMON_BETA_OBSERVABLE_ROWS"]])
    observable_ok = all(token in observable_text for token in ["R10_short_range", "PPN_local_GR", "Gdot_clock", "orbital_radial", "EM_common_mode"])
    add("VAL4125_5_observables", "observable rows cover R10, PPN, Gdot, radial, and EM", observable_ok, "observable tokens checked")

    runner_text = flatten_rows([outputs["P8_Y5_R2FR_4125_SOURCE_NORMALIZATION_RUNNER_ROWS"]])
    runner_ok = all(token in runner_text for token in ["NO_TUNED_CANCELLATION_ALLOWED", "WEP_NOT_SUFFICIENT", "EM_WEP_NOT_SUFFICIENT"])
    add("VAL4125_6_runner", "source-normalization runner forbids tuning and WEP shortcuts", runner_ok, "runner tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4125_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4126-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md"
    add("VAL4125_7_next_target", "next target is 4126 Ward identity or beta bound fill", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4125_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no local_GR" in status_rows_local[0].get("claim_state", "")
    add("VAL4125_8_status", "status records common beta runner and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4125_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4125*")) or any(FORMALIZATION.rglob("4125-Y5-R2FR*"))
    add("VAL4125_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4125_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4125_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
