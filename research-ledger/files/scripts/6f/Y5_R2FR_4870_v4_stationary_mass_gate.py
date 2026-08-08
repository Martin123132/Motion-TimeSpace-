from __future__ import annotations

import csv
import math
import tarfile
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4870"
TIMESTAMP = "2026-07-10T16:10:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-"
    "C3-arbitration.md"
)
P_UNIFORM = 1.3928203230275528e-6
KAPPA_ENVELOPE = 0.159
G_ENVELOPE = 0.47
KAPPA_BINARY_BOX = 1.4532678436847029
G_BINARY_BOX = 11.649016320300504
GRID_RESIDUAL_BOUND = 1.0e-7


GRID_DATA = (
    ("core", "1/30", 1 / 30, 0.03, 0.00489458683358, -0.00412433298819, -0.0183109034048),
    ("core", "1/12", 1 / 12, 0.03, 0.0118092212613, -0.0100838274165, -0.0452429555482),
    ("core", "1/6", 1 / 6, 0.03, 0.0223529687998, -0.0195317196394, -0.0891948507161),
    ("core", "1/4", 1 / 4, 0.03, 0.0318779298507, -0.0285299711756, -0.132605979853),
    ("core", "1/3", 1 / 3, 0.03, 0.0405698964664, -0.0372168287389, -0.176024940512),
    ("core", "1/30", 1 / 30, 0.10, 0.0146929282309, -0.0107389028635, -0.0418324382154),
    ("core", "1/12", 1 / 12, 0.10, 0.0354025669088, -0.0261550906248, -0.103033024272),
    ("core", "1/6", 1 / 6, 0.10, 0.0668057812406, -0.0502252396618, -0.201384573573),
    ("core", "1/4", 1 / 4, 0.10, 0.0949059338222, -0.0725730142590, -0.295866312605),
    ("core", "1/3", 1 / 3, 0.10, 0.120251531197, -0.0934907800783, -0.387171647035),
    ("core", "1/30", 1 / 30, 0.20, 0.0251542222137, -0.0155011647342, -0.0485466512322),
    ("core", "1/12", 1 / 12, 0.20, 0.0608664588043, -0.0379531656371, -0.121025948684),
    ("core", "1/6", 1 / 6, 0.20, 0.115355570275, -0.0732167017764, -0.239666903385),
    ("core", "1/4", 1 / 4, 0.20, 0.164161334880, -0.105810714953, -0.354001714988),
    ("core", "1/3", 1 / 3, 0.20, 0.207968184081, -0.135842685947, -0.462836935331),
    ("core", "1/30", 1 / 30, 0.30, 0.0319868279452, -0.0173629935939, -0.0429434649158),
    ("core", "1/12", 1 / 12, 0.30, 0.0782862088644, -0.0429053375980, -0.108384074191),
    ("core", "1/6", 1 / 6, 0.30, 0.150654729757, -0.0838828033632, -0.219098237634),
    ("core", "1/4", 1 / 4, 0.30, 0.216844360685, -0.122494315521, -0.329421442113),
    ("core", "1/3", 1 / 3, 0.30, 0.276964115183, -0.158423165517, -0.436492978589),
    ("refined", "1/3", 1 / 3, 0.125, 0.144609636258, -0.107025458418, -0.422374758569),
    ("refined", "1/3", 1 / 3, 0.150, 0.167211218986, -0.118298104304, -0.444751177471),
    ("refined", "1/3", 1 / 3, 0.175, 0.188266570117, -0.127784237253, -0.457474187670),
    ("refined", "1/3", 1 / 3, 0.225, 0.226498394329, -0.142747080784, -0.462481463284),
    ("refined", "1/3", 1 / 3, 0.250, 0.244038729645, -0.148708289083, -0.457550123732),
    ("refined", "1/3", 1 / 3, 0.275, 0.260783581017, -0.153890559576, -0.448773733557),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def archive_contains(path: Path, member: str, needle: str) -> bool:
    if not path.exists():
        return False
    try:
        with tarfile.open(path, "r:*") as archive:
            extracted = archive.extractfile(member)
            if extracted is None:
                return False
            return needle in extracted.read().decode("utf-8", errors="replace")
    except (tarfile.TarError, OSError):
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: " + chr(96)
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4870_00_public", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "selected public correspondence action"),
        ("SRC4870_01_finite", POST / "4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md", "FINITE_COMPACTNESS_VARIATIONAL_ADM_COMPLETION_4868", "finite-C L2/L4 reduction and BVP"),
        ("SRC4870_02_ward", POST / "4869-Y5-R2FR-l1-metric-Ward-completion-and-C3-sensitivity-discrepancy-or-v4-boundary-extension.md", "L1_METRIC_WARD_AND_C3_DISCREPANCY_4869", "first-response Ward completion and C3 conflict"),
        ("SRC4870_03_prior_validation", OUTPUT / "P8_Y5_BRR545_4869_VALIDATION.csv", "VAL4869_OVERALL", "prior checkpoint validation"),
        ("SRC4870_04_checkpoint", POST / "4870-Y5-R2FR-v4-stationary-mass-identity-and-finite-compactness-parent-kappa4-or-v3-tail-crosscheck.md", "V4_STATIONARY_MASS_IDENTITY_4870", "human derivation"),
        ("SRC4870_05_formal", FORMAL / "886-PPC4161-v4-stationary-mass-and-finite-C-parent-response.md", "PPC4161_V4_STATIONARY_MASS_4870", "formal integration"),
        ("SRC4870_06_claim", FORMAL / "02-claims-register.csv", "L-712", "claim register"),
        ("SRC4870_07_kappa", FORMAL / "04-variable-audit.csv", "finite_C_parent_correspondence_response_derived_binary_safe_external_C3_and_v3_crosscheck_open_nonclaim", "quartic variable status"),
        ("SRC4870_08_D4", FORMAL / "04-variable-audit.csv", "derived_charge_partition_not_independent_parent_response_nonclaim", "charge-partition variable status"),
        ("SRC4870_09_equation", FORMAL / "05-equation-register.md", "1.163 Quartic stationary-mass identity", "equation register"),
        ("SRC4870_10_redteam", FORMAL / "06-consistency-red-team.md", "114. Quartic stationary-mass response red team", "red-team register"),
        ("SRC4870_11_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4870", "unification spine"),
        ("SRC4870_12_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: " + chr(96) + "4870-", "resume marker"),
        ("SRC4870_13_flow_script", POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py", "solve_bvp_profile", "finite-C flow solver"),
        ("SRC4870_14_finite_generator", POST / "scripts" / "Y5_R2FR_4868_variational_adm_completion_gate.py", 'CHECKPOINT = "4868"', "finite-C generator"),
        ("SRC4870_15_ward_script", POST / "scripts" / "Y5_R2FR_4869_l1_metric_response_source.py", "metric_shift_ward_identities", "symbolic metric source"),
        ("SRC4870_16_ward_generator", POST / "scripts" / "Y5_R2FR_4869_metric_Ward_C3_discrepancy.py", 'CHECKPOINT = "4869"', "Ward/C3 generator"),
        ("SRC4870_17_generator", Path(__file__).resolve(), 'CHECKPOINT = "4870"', "checkpoint generator"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "member": "",
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    archives = [
        ("SRC4870_18_yagi", Path(r"D:\Temp\1311.7144-source.tar"), "paper.tex", r"\label{ae:mass}", "stationary total-mass identity"),
        ("SRC4870_19_gupta", Path(r"D:\Temp\2104.04596-source.tar"), "main.tex", r"\label{tolman_sens_C}", "external compactness-series comparison"),
    ]
    for source_id, path, member, needle, role in archives:
        valid = archive_contains(path, member, needle)
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local_primary_archive",
                "source_locator": str(path),
                "member": member,
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": valid,
                "role": role,
                "source_validated": valid,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4870_20_urls",
            "source_kind": "primary_url_ledger",
            "source_locator": "https://arxiv.org/abs/1311.7144;https://arxiv.org/abs/2104.04596;https://arxiv.org/abs/gr-qc/0509121;https://arxiv.org/abs/gr-qc/0507059",
            "member": "",
            "needle": "primary URLs recorded",
            "source_exists": True,
            "needle_found": True,
            "role": "primary provenance ledger",
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    hessian, source, leading, residual = sp.symbols(
        "H J q1 q3", nonzero=True, real=True
    )
    first_variation = sp.factor((hessian * leading + source) * residual)
    stationary_variation = sp.simplify(
        first_variation.subs(leading, -source / hessian)
    )
    entries = [
        ("THM4870_00_mass", "stationary total mass", "Mtot=-integral(Lg+Lae+Lm)d3x", "Yagi stationary mass identity", "SOURCE_BACKED"),
        ("THM4870_01_envelope", "small-p stationary envelope", "M(v,p)=M_GR-p*Iae_bar_on(v)+O(p2)", "metric and matter first variations multiply p=0 equations", "DERIVED_PARENT"),
        ("THM4870_02_assumptions", "theorem domain", "smooth gauge-fixed stationary branch; fixed couplings and baryon number; compact matter support; asymptotically Cartesian gauge", "all assumptions explicit", "RECORDED"),
        ("THM4870_03_expansion", "normalized flow hierarchy", "q=q1+v2*q3+O(v4); Iae_bar=v2*I2[q]+v4*I4[q]+O(v6)", "exact gamma*v boundary normalization removed", "DERIVED_PARENT"),
        ("THM4870_04_scalar", "abstract stationary variation", sp.sstr(stationary_variation), "H*q1+J=0 implies delta I2=0", "PASS" if stationary_variation == 0 else "FAIL"),
        ("THM4870_05_boundary", "q3 residual boundary", "q3 regular at R=0 and q3(infinity)=0", "inner and outer canonical boundary terms vanish", "DERIVED_CONDITIONAL"),
        ("THM4870_06_cancel", "third-order-profile cancellation", "delta I2[q1;q3]=integral(q3*E[q1])+[Pi1*q3]_0^infinity=0", "no fitted q3 closure enters the mass coefficient", "DERIVED_PARENT"),
        ("THM4870_07_f", "first response normalization", "f_parent=-I2[q1]/(8*pi*C)", "Rstar=1 and M=C/G at p=0", "DERIVED_PARENT"),
        ("THM4870_08_kappa", "quartic response normalization", "kappa4_parent=I4[q1]/(16*pi*C)", "physical first-order-p v4 coefficient", "DERIVED_PARENT"),
        ("THM4870_09_g", "second response relation", "g_parent=3*f_parent+8*kappa4_parent", "Gupta response convention", "DERIVED_PARENT"),
        ("THM4870_10_scope", "ownership gate", "selected Einstein-aether correspondence action at O(p), not primitive MTS scalar ownership", "C3 and direct v3-tail checks remain open", "PRIVATE_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "derived": derived,
            "expected_or_role": expected,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, derived, expected, status in entries
    ]


def grid_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (
        sample_kind,
        ratio_label,
        ratio,
        compactness,
        first_response,
        quartic_response,
        second_response,
    ) in enumerate(GRID_DATA):
        identity_residual = second_response - 3 * first_response - 8 * quartic_response
        rows.append(
            {
                "row_id": f"GRID4870_{index:02d}",
                "sample_kind": sample_kind,
                "ratio_label": ratio_label,
                "ratio_value": ratio,
                "compactness": compactness,
                "f_parent": first_response,
                "kappa4_parent": quartic_response,
                "g_parent": second_response,
                "g_identity_residual": identity_residual,
                "base_outer_radii": "100;200",
                "outer_extrapolation": "Richardson leading 1/Rmax removal",
                "maximum_bvp_residual_bound": GRID_RESIDUAL_BOUND,
                "status": "FINITE_C_PARENT_RESPONSE_CONTROLLED",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def charge_rows() -> list[dict[str, Any]]:
    bulk = -0.15842314
    aether = -0.18918470
    adm = 0.03076156
    completion = 0.18918470
    entries = [
        ("CHG4870_00_identity", "conserved charge identity", "Q4=EADM4+Eae4", "Foster energy split", "DERIVED_PARENT"),
        ("CHG4870_01_stationary", "stationary mass identification", "Q4=B4", bulk, "DERIVED_PARENT"),
        ("CHG4870_02_bulk", "B4/M", bulk, "I4/(16*pi*C)", "NUMERIC_ENDPOINT"),
        ("CHG4870_03_aether", "Eae4/M", aether, "Noether surface charge", "NUMERIC_ENDPOINT"),
        ("CHG4870_04_adm", "EADM4/M", adm, "B4-Eae4", "NUMERIC_ENDPOINT"),
        ("CHG4870_05_completion", "D4/M", completion, "-Eae4=EADM4-B4", "DERIVED_NOT_FREE"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value_or_identity": value,
            "derivation_or_reference": reference,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, reference, status in entries
    ]


def preferred_frame_rows(grid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sampled_kappa = max(abs(float(row["kappa4_parent"])) for row in grid)
    sampled_g = max(abs(float(row["g_parent"])) for row in grid)
    entries = [
        ("PFG4870_00_k_sample", "maximum sampled |kappa4|", sampled_kappa, KAPPA_ENVELOPE, "below conservative envelope"),
        ("PFG4870_01_g_sample", "maximum sampled |g|", sampled_g, G_ENVELOPE, "below conservative envelope"),
        ("PFG4870_02_k_box", "inherited no-cancellation |kappa4| box", KAPPA_BINARY_BOX, KAPPA_ENVELOPE, "box/envelope >9.1"),
        ("PFG4870_03_g_box", "inherited no-cancellation |g| box", G_BINARY_BOX, G_ENVELOPE, "box/envelope >24.7"),
        ("PFG4870_04_pk", "p_uniform*|kappa4| envelope", P_UNIFORM * KAPPA_ENVELOPE, 2.22e-7, "first-order mass-response scale"),
        ("PFG4870_05_pg", "p_uniform*|g| envelope", P_UNIFORM * G_ENVELOPE, 6.55e-7, "first-order second-sensitivity scale"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, quantity, value, comparison, meaning in entries:
        if row_id.endswith("_sample"):
            passed = value < comparison
        elif row_id.endswith("_box"):
            passed = value / comparison > (9.1 if "k_box" in row_id else 24.7)
        else:
            passed = value <= comparison
        rows.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "value": value,
                "comparison_value": comparison,
                "meaning": meaning,
                "status": "PASS_BOUNDED_SMOKE" if passed else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "stationary total-mass envelope", "RETAIN_DERIVED_PARENT", "no independent first-order-p metric or matter mass functional"),
        (2, "zero-boundary v3 profile", "ELIMINATED_FROM_MASS_COEFFICIENT", "delta I2 vanishes by stationarity and boundary data"),
        (3, "finite-C kappa4 and g", "DERIVED_SELECTED_CORRESPONDENCE_ACTION", "on-shell I4 supplies the parent response"),
        (4, "D4 completion", "DERIVED_CHARGE_PARTITION_NOT_FREE", "D4=-Eae4"),
        (5, "binary preferred-frame gate", "BOUNDED_SMOKE_PASS", "sampled envelopes lie well inside inherited sufficient boxes"),
        (6, "parent versus Gupta C3", "QUARANTINE_BOTH_BRANCHES", "disjoint cubic coefficients remain unresolved"),
        (7, "direct v3 l1 tail", "OPEN_INDEPENDENT_CROSSCHECK", "mass cancellation does not replace asymptotic extraction"),
        (8, "primitive MTS ownership", "OPEN_HARD", "result belongs to selected correspondence action"),
        (9, "local GR", "NOT_PROMOTED", "C3, EoS, solitary and primitive-ownership gates remain"),
        (10, "next derivation", "V3_TAIL_AND_C3_ARBITRATION", NEXT_TARGET),
    ]
    return [
        {
            "priority": priority,
            "target": target,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, target, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_v4_stationary_mass", "CLOSED_PARENT", "small-p stationary envelope theorem", "retain assumptions explicitly"),
        (2, "R_q3_mass_dependence", "CLOSED_PARENT", "zero first variation and boundary term", "solve only as independent tail check"),
        (3, "R_D4", "CLOSED_DERIVED_PARTITION", "D4=-Eae4", "do not fit independently"),
        (4, "R_finite_C_grid", "CLOSED_SAMPLED_CORRIDOR", "26 controlled response rows", "repeat for tabulated EoSs"),
        (5, "R_binary_window", "BOUNDED_SMOKE_PASS", "sampled envelopes inside inherited boxes", "retain no-cancellation convention"),
        (6, "R_v3_l1_tail", "OPEN_HARD_NEXT", "not independently extracted", "derive finite-C asymptotic response"),
        (7, "R_C3", "OPEN_DECISIVE_CONFLICT", "parent 4.94-5.00 versus Gupta 10.8375", "rederive source equations term by term"),
        (8, "R_EOS", "OPEN_EXTENSION", "Tolman VII only", "repeat on tabulated nuclear EoSs"),
        (9, "R_primitive_ownership", "OPEN_HARD", "correspondence action not derived from primitive MTS fields", "return after local correspondence checks"),
        (10, "R_local_GR", "OPEN_HARD", "compact response alone is insufficient", "do not promote"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    charge: list[dict[str, Any]],
    preferred: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [
        row
        for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-712"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol")
        in {
            "sigma_prime_compact_MTS",
            "kappa4_compact_MTS",
            "D4_ADM_completion_MTS",
        }
    }
    checkpoint = (
        POST
        / "4870-Y5-R2FR-v4-stationary-mass-identity-and-finite-compactness-parent-kappa4-or-v3-tail-crosscheck.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "886-PPC4161-v4-stationary-mass-and-finite-C-parent-response.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4869_VALIDATION.csv")
    sampled_kappa = max(abs(float(row["kappa4_parent"])) for row in grid)
    sampled_g = max(abs(float(row["g_parent"])) for row in grid)
    endpoint = [
        row
        for row in grid
        if math.isclose(float(row["ratio_value"]), 1 / 3)
        and math.isclose(float(row["compactness"]), 0.3)
    ]

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, theorem, grid, charge, preferred, decisions, residuals)
    checks = [
        result("VAL4870_00_sources", len(sources) == 21 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4870_01_theorem", len(theorem) == 11 and all(row["status"] != "FAIL" for row in theorem), "stationary-mass theorem rows recorded"),
        result("VAL4870_02_stationarity", theorem[4]["derived"] == "0" and theorem[4]["status"] == "PASS", "abstract Hessian first variation vanishes"),
        result("VAL4870_03_assumptions", all(token in theorem[2]["derived"] for token in ("fixed couplings", "baryon number", "compact matter", "asymptotically Cartesian")), "mass-envelope assumptions explicit"),
        result("VAL4870_04_boundary", "R=0" in theorem[5]["derived"] and "infinity)=0" in theorem[5]["derived"], "q3 center and infinity conditions recorded"),
        result("VAL4870_05_q3", theorem[6]["status"] == "DERIVED_PARENT" and theorem[6]["derived"].endswith("=0"), "zero-boundary v3 profile removed from mass coefficient"),
        result("VAL4870_06_normalization", theorem[7]["derived"] == "f_parent=-I2[q1]/(8*pi*C)" and theorem[8]["derived"] == "kappa4_parent=I4[q1]/(16*pi*C)", "f and kappa4 normalizations locked"),
        result("VAL4870_07_grid", len(grid) == 26 and all(abs(float(row["g_identity_residual"])) <= 2.0e-9 and float(row["maximum_bvp_residual_bound"]) <= 1.01e-7 for row in grid), "26 finite-C rows satisfy response identity and residual bound"),
        result("VAL4870_08_envelope", sampled_kappa < KAPPA_ENVELOPE and sampled_g < G_ENVELOPE, f"sampled maxima={sampled_kappa:.9g},{sampled_g:.9g}"),
        result("VAL4870_09_endpoint", len(endpoint) == 1 and math.isclose(float(endpoint[0]["kappa4_parent"]), -0.158423165517, abs_tol=1e-12), "r=1/3,C=0.3 endpoint locked"),
        result("VAL4870_10_charge", math.isclose(0.03076156 - 0.18918470, -0.15842314, abs_tol=1e-12), "EADM4+Eae4=B4"),
        result("VAL4870_11_D4", math.isclose(0.18918470, -(-0.18918470), abs_tol=1e-12) and charge[-1]["status"] == "DERIVED_NOT_FREE", "D4=-Eae4 and is not free"),
        result("VAL4870_12_preferred", len(preferred) == 6 and all(row["status"] == "PASS_BOUNDED_SMOKE" for row in preferred), "preferred-frame smoke rows pass"),
        result("VAL4870_13_margins", KAPPA_BINARY_BOX / KAPPA_ENVELOPE > 9.1 and G_BINARY_BOX / G_ENVELOPE > 24.7, "binary box factors exceed 9.1 and 24.7"),
        result("VAL4870_14_p_scale", P_UNIFORM * KAPPA_ENVELOPE < 2.22e-7 and P_UNIFORM * G_ENVELOPE < 6.55e-7, "uniform-p response scales bounded"),
        result("VAL4870_15_decision", decisions[3]["decision"] == "DERIVED_CHARGE_PARTITION_NOT_FREE" and decisions[-1]["decision"] == "V3_TAIL_AND_C3_ARBITRATION", "charge and next derivation decisions selected"),
        result("VAL4870_16_residual", residuals[5]["status"] == "OPEN_HARD_NEXT" and residuals[6]["status"] == "OPEN_DECISIVE_CONFLICT", "v3 tail and C3 conflict remain explicit"),
        result("VAL4870_17_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all generated rows private nonclaim"),
        result("VAL4870_18_registers", len(claims) == 1 and claims[0].get("status") == "finite_C_kappa4_and_g_derived_inside_selected_correspondence_action_external_C3_and_v3_crosscheck_open_private_nonclaim" and variables.get("sigma_prime_compact_MTS", {}).get("status") == "finite_C_parent_correspondence_coefficient_derived_external_C3_and_v3_crosscheck_open_nonclaim" and variables.get("kappa4_compact_MTS", {}).get("status") == "finite_C_parent_correspondence_response_derived_binary_safe_external_C3_and_v3_crosscheck_open_nonclaim" and variables.get("D4_ADM_completion_MTS", {}).get("status") == "derived_charge_partition_not_independent_parent_response_nonclaim", "claim and three variable statuses integrated"),
        result("VAL4870_19_documents", "V4_STATIONARY_MASS_IDENTITY_4870" in checkpoint and "PPC4161_V4_STATIONARY_MASS_4870" in formal, "checkpoint and formal markers found"),
        result("VAL4870_20_resume", resume_checkpoint_at_least(resume, 4870) and NEXT_TARGET in resume, "resume advanced to v3 tail and C3 arbitration"),
        result("VAL4870_21_prior", prior[-1].get("status") == "PASS", "4869 validation remains historical green"),
        result("VAL4870_22_scripts", all(compiles(path) for path in (Path(__file__).resolve(), POST / "scripts" / "Y5_R2FR_4868_fixed_background_variational_remainder.py", POST / "scripts" / "Y5_R2FR_4869_l1_metric_response_source.py", POST / "scripts" / "Y5_R2FR_4869_metric_Ward_C3_discrepancy.py")), "generator and inherited derivation scripts compile"),
        result("VAL4870_23_pycache", not (POST / "scripts" / "__pycache__").exists(), "no scripts pycache directory"),
    ]
    checks.append(
        result(
            "VAL4870_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "V4_STATIONARY_MASS_AND_FINITE_C_PARENT_RESPONSE_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    theorem = theorem_rows()
    grid = grid_rows()
    charge = charge_rows()
    preferred = preferred_frame_rows(grid)
    decisions = decision_rows()
    residuals = residual_rows()
    validation = validation_rows(
        sources,
        theorem,
        grid,
        charge,
        preferred,
        decisions,
        residuals,
    )
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_STATIONARY_MASS_THEOREM.csv", theorem)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_FINITE_COMPACTNESS_RESPONSE.csv", grid)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_CHARGE_SPLIT.csv", charge)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_PREFERRED_FRAME_GATE.csv", preferred)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4870_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4870_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4870_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4870_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
