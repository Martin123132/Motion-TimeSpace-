from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "860-Y5-R10-parent-amplitude-law-and-GR-limit-derivation-contract.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_860_SOURCE_REGISTER.csv"
AMPLITUDE_ALIGNMENT_PATH = RESIDUALS / "P8_Y5_R10_860_EXACT_2OVER27_ALIGNMENT.csv"
PARENT_LAW_PATH = RESIDUALS / "P8_Y5_R10_860_PARENT_AMPLITUDE_LAW_PROOF_OBLIGATIONS.csv"
CONDITIONAL_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_860_CONDITIONAL_THEOREM_STACK.csv"
LOCAL_GR_PATH = RESIDUALS / "P8_Y5_R10_860_LOCAL_GR_NEWTON_GATE_STACK.csv"
WARD_PROJECTOR_PATH = RESIDUALS / "P8_Y5_R10_860_WARD_PROJECTOR_BLOCKER_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_860_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_860_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_860_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_860_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_860_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_860_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_859_VALIDATION.csv"
CURVATURE_PATH = RESIDUALS / "P8_Y5_R10_859_EMPIRICAL_CURVATURE_LEDGER.csv"
INVERSION_PATH = RESIDUALS / "P8_Y5_R10_859_PARENT_AMPLITUDE_INVERSION_LEDGER.csv"

STATUS = "Y5_R10_860_exact_2over27_parent_law_and_GR_limit_contract_written_nonclaim"
CLAIM_CEILING = "conditional_theorem_stack_only_no_parent_derivation_no_local_GR_or_Newton_claim"
NEXT_TARGET = "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md"

TWO_OVER_27 = 2.0 / 27.0
TWO_OVER_9 = 2.0 / 9.0

SOURCE_SPECS = [
    {
        "source_id": "859_doc",
        "path": POST_CHECKPOINT / "859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md",
        "needles": [
            "empirical parent-only corridor has been converted into a derivation gate",
            "0.06_to_0.10_private_corridor",
            "860-Y5-R10-parent-amplitude-law-and-GR-limit-derivation-contract.md",
        ],
        "role": "immediate derivation gate handoff",
    },
    {
        "source_id": "859_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V859_4_derivation_contract_ready,pass",
            "V859_6_GR_Newton_limit_open,pass",
            "V859_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "859_curvature",
        "path": CURVATURE_PATH,
        "needles": [
            "estimated_empirical_optimum_b_parent",
            "0.0739750196008",
            "diagnostic_only_not_derivation",
        ],
        "role": "empirical parent-only optimum",
    },
    {
        "source_id": "859_inversion",
        "path": INVERSION_PATH,
        "needles": [
            "AI859_best_target_corridor",
            "3*b_P*eta^2",
            "empirical_target_corridor_only",
        ],
        "role": "parent-law target inversion guard",
    },
    {
        "source_id": "107_two_ninth_scout",
        "path": POST_CHECKPOINT / "107-two-ninth-fixed-amplitude-scout.md",
        "needles": [
            "DeltaR = 2/9",
            "B_mem = DeltaR/3 = 2/27",
            "two_ninth_promising_not_derived",
        ],
        "role": "original exact locked-amplitude scout",
    },
    {
        "source_id": "108_two_ninth_robustness",
        "path": POST_CHECKPOINT / "108-two-ninth-fixed-amplitude-robustness.md",
        "needles": [
            "two_ninth_locked_amplitude_survives_matrix",
            "derive normalized boundary-charge contrast 2/9",
            "local GR/PPN silence",
        ],
        "role": "locked-amplitude robustness theorem target",
    },
    {
        "source_id": "109_two_ninth_theorem_attempt",
        "path": POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needles": [
            "two_ninth_theorem_status",
            "not_derived_but_target_sharpened",
            "boundary_charge_unit_defined",
        ],
        "role": "failed boundary-charge derivation attempt",
    },
    {
        "source_id": "316_FLRW_projection",
        "path": POST_CHECKPOINT / "316-FLRW-memory-projection-amplitude-contract.md",
        "needles": [
            "FLRW shape: conditionally derived",
            "p = 3",
            "Bianchi does not fix B_mem",
        ],
        "role": "conditional FLRW shape and conservation derivation",
    },
    {
        "source_id": "347_local_GR_attempt",
        "path": POST_CHECKPOINT / "347-local-GR-parent-reduction-theorem-attempt.md",
        "needles": [
            "N5_projector_stress_Bianchi_safe",
            "conditional GR-reduction theorem",
            "T_projector",
        ],
        "role": "local GR conditional theorem and hard blocker",
    },
    {
        "source_id": "382_parent_local_action",
        "path": POST_CHECKPOINT / "382-parent-local-action-minimal-contract.md",
        "needles": [
            "minimal parent local action contract written",
            "Required Variation Identities",
            "Ward identity",
        ],
        "role": "parent local action variation contract",
    },
    {
        "source_id": "393_Newtonian_source",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "nabla^2 Phi = 4 pi G_eff rho_eff",
            "measured GM",
            "not parent-derived",
        ],
        "role": "Newtonian source-normalization blocker",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def empirical_optimum() -> float:
    rows = read_csv(CURVATURE_PATH)
    row = next(item for item in rows if item["curvature_id"] == "EC859_0_bic_window")
    return float(row["estimated_empirical_optimum_b_parent"])


def amplitude_alignment_rows(generated_utc: str) -> list[dict[str, object]]:
    optimum = empirical_optimum()
    delta = TWO_OVER_27 - optimum
    return [
        {
            "alignment_id": "AA860_0_exact_identity",
            "object": "exact locked parent amplitude",
            "mathematical_form": "eta=1, a_F=1, DeltaR=2/9 => b_P=a_F DeltaR/(3 eta^2)=2/27",
            "value": fmt(TWO_OVER_27),
            "comparison": "matches older locked B_mem theorem target",
            "status": "conditional_exact_if_parent_clauses_are_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "alignment_id": "AA860_1_empirical_alignment",
            "object": "859 parent-only empirical optimum",
            "mathematical_form": "b_empirical_optimum from quadratic diagnostic window",
            "value": fmt(optimum),
            "comparison": f"2/27 minus optimum = {fmt(delta)}; relative = {fmt(delta / TWO_OVER_27)}",
            "status": "alignment_pass_diagnostic_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "alignment_id": "AA860_2_required_product",
            "object": "parent product for exact locked branch",
            "mathematical_form": "a_F DeltaR = 3 b_P eta^2",
            "value": "2/9 * eta^2",
            "comparison": "if eta=1 and a_F=1 this is DeltaR=2/9",
            "status": "target_contract_not_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "alignment_id": "AA860_3_current_claim_ceiling",
            "object": "locked 2/27 status",
            "mathematical_form": "B_mem=2/27 remains closure/theorem target until Q_*, endpoint equations, and Ward trace coupling are derived",
            "value": fmt(TWO_OVER_27),
            "comparison": "107-109 and 344 forbid prediction language",
            "status": "nonclaim_closure_target",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "obligation_id": "PL860_0_eta_lock",
            "symbol": "eta",
            "target_value": "1",
            "law_needed": "eta = H0 L_cg/c and L_cg = c/H0 for the coherent FLRW parent domain",
            "proof_status": "open",
            "blocker": "L_cg selection must be parent-derived and must not become a local fifth-force scale",
            "promotion_if_solved": "normalizes b_P without fitted scale",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "PL860_1_trace_coupling",
            "symbol": "a_F",
            "target_value": "1",
            "law_needed": "Ward-fixed trace coupling between FLRW memory source and the metric/effective stress",
            "proof_status": "open",
            "blocker": "trace normalization is not yet fixed by variation; cannot be chosen to hit 2/27",
            "promotion_if_solved": "removes free amplitude normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "PL860_2_endpoint_charge",
            "symbol": "DeltaR",
            "target_value": "2/9",
            "law_needed": "DeltaR=(Q_early-Q_today)/Q_* with endpoint equations derived before data",
            "proof_status": "open_hard",
            "blocker": "Q_*, Q_early, Q_today, and their Ward-fixed trace coupling remain missing",
            "promotion_if_solved": "turns the empirical locked amplitude into a parent prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "PL860_3_FLRW_shape",
            "symbol": "A_P(z)",
            "target_value": "p=3, u3=1/4 or derived replacement",
            "law_needed": "coherent isotropic FLRW load determinant plus cell/endpoint scale theorem",
            "proof_status": "conditional",
            "blocker": "316 derives p=3 conditionally; u3 and amplitude remain theorem targets",
            "promotion_if_solved": "keeps shape from becoming a fit function",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "PL860_4_Bianchi_FLRW",
            "symbol": "T_mem_FLRW",
            "target_value": "conserved effective stress",
            "law_needed": "rho_mem=B_mem F(N), p_mem=-rho_mem+rho_mem'/3 or parent stress equivalent",
            "proof_status": "conditional_pass_for_supplied_Bmem",
            "blocker": "Bianchi fixes pressure response but does not fix B_mem",
            "promotion_if_solved": "prevents energy-conservation overclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def conditional_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_step": "CT860_0_amplitude",
            "if_clause": "eta=1, a_F=1, DeltaR=2/9 are parent-derived",
            "then_clause": "b_P=2/27 exactly",
            "current_status": "conditional_not_proved",
            "missing": "eta lock, trace coupling, endpoint charge theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "CT860_1_shape",
            "if_clause": "coherent FLRW load tensor and cell scale derive A_P(z)",
            "then_clause": "memory sector supplies fixed shape rather than fitted functional freedom",
            "current_status": "conditional_partial",
            "missing": "u3/cell endpoint theorem and parent kernel ownership",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "CT860_2_local_GR",
            "if_clause": "one coframe, EH exterior, no bulk MTS hair, N5 projector stress Bianchi-safe",
            "then_clause": "local exterior reduces to GR and PPN residuals vanish through the retained order",
            "current_status": "conditional_not_proved",
            "missing": "N5 projector variation closure and no-hair/source-normalization clauses",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "CT860_3_Newton",
            "if_clause": "conditional EH branch plus source-normalized kappa, M_eff, and measured GM absorption",
            "then_clause": "weak-field slow-motion limit gives Poisson/Newton",
            "current_status": "conditional_not_proved",
            "missing": "constant universal GM theorem; no range/time/species source residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "CT860_4_unified_gate",
            "if_clause": "CT860_0 through CT860_3 are all proved by the same parent action",
            "then_clause": "MTS has a serious route to derived late-time memory plus GR/Newton reduction",
            "current_status": "future_promotion_gate",
            "missing": "shared parent action proof, not separate closure islands",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_gr_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "LG860_0_one_metric",
            "requirement": "one physical metric/coframe for matter, clocks, photons, rulers, and PPN",
            "pass_condition": "S_matter[Psi, ehat] with no direct MTS species vertices and ehat=e in local exterior",
            "current_status": "conditional_contract",
            "residual_if_failed": "WEP, clock drift, nonmetric light, composition force",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LG860_1_EH_exterior",
            "requirement": "local exterior operator is Einstein-Hilbert plus harmless boundary terms",
            "pass_condition": "E_MTS_munu -> 0 or retained conserved boundary-only stress",
            "current_status": "conditional_blocked_by_N5",
            "residual_if_failed": "modified gravity operator, gamma/beta drift",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LG860_2_q_loc_suppression",
            "requirement": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) vanishes or is bounded from variation",
            "pass_condition": "Gamma_eff and K_hat are same-parent conserved objects or projector force is retained",
            "current_status": "open_hard",
            "residual_if_failed": "fifth force, local exchange, PPN residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LG860_3_Newton_source",
            "requirement": "source-normalized Newtonian limit",
            "pass_condition": "nabla^2 Phi=4 pi G_eff rho_eff with constant universal measured GM",
            "current_status": "conditional_not_parent_derived",
            "residual_if_failed": "delta_G, Gdot/G, range force, source beta, WEP source charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LG860_4_PPN_vector",
            "requirement": "gamma-1, beta-1, alpha1/alpha2, clock/WEP residuals are zero or bounded",
            "pass_condition": "local no-hair, one coframe, EH exterior, source normalization, no hidden projector stress",
            "current_status": "not_promoted",
            "residual_if_failed": "PPN/local-bound runner required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ward_projector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "WP860_0_N5_projector_stress",
            "blocker": "metric-dependent projector variation may produce T_projector",
            "why_it_matters": "dropping T_projector fakes conservation and invalidates local GR promotion",
            "required_resolution": "derive T_projector=0, boundary-only conserved, pure gauge, or retain it in E_MTS",
            "status": "open_hard",
            "next_action": "write Ward-owned boundary charge plus N5 projector closure test",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "WP860_1_boundary_charge_unit",
            "blocker": "Q_* not parent-defined",
            "why_it_matters": "DeltaR=2/9 cannot be a prediction without a normalized charge unit",
            "required_resolution": "derive Q_* from action, topology, cell measure, or Ward-normalized boundary current",
            "status": "open_hard",
            "next_action": "tie Q_* to same Ward identity that owns projector/boundary stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "WP860_2_endpoint_equations",
            "blocker": "Q_early and Q_today endpoint equations not derived",
            "why_it_matters": "post-fit endpoint choices are target inversion",
            "required_resolution": "stationarity or boundary Euler equation gives endpoints before data",
            "status": "open_hard",
            "next_action": "attempt endpoint Euler/Ward system for DeltaR=2/9",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "WP860_3_trace_coupling",
            "blocker": "boundary charge not yet proven to couple to FLRW trace memory with a_F=1",
            "why_it_matters": "even a derived 2/9 charge is not b_P unless the coupling is fixed",
            "required_resolution": "Ward trace normalization maps charge contrast to FLRW memory source",
            "status": "open",
            "next_action": "include trace-coupling row in 861 proof attempt",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC860_0_selected",
            "route": "Ward_owned_boundary_charge_endpoint_and_N5_projector_closure",
            "status": "selected",
            "reason": "the exact 2/27 target aligns with 859, but both amplitude prediction and local GR are blocked by boundary/projector/Ward ownership",
            "include": "Q_*, endpoint equations, trace coupling, N5 projector stress, q_loc suppression",
            "exclude": "new fitted amplitude, response reopening, local plateau axiom, support claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC860_1_deferred",
            "route": "more_cosmology_scoring",
            "status": "deferred",
            "reason": "the empirical corridor is already sharp enough; derivation and GR reduction are the bottlenecks",
            "include": "only after a derived parent amplitude or failed derivation creates a new testable branch",
            "exclude": "grid-tuning the amplitude corridor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG860_0_no_prediction",
            "claim": "MTS predicts b_P=2/27 or DeltaR=2/9",
            "status": "forbidden",
            "reason": "the exact value is a closure/theorem target until Q_*, endpoints, eta, and a_F are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG860_1_no_local_GR",
            "claim": "MTS derives local GR/Newton",
            "status": "forbidden",
            "reason": "N5 projector stress, q_loc suppression, and source-normalized GM remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG860_2_no_scoring_promotion",
            "claim": "empirical alignment with 2/27 is support-grade",
            "status": "forbidden",
            "reason": "alignment is diagnostic and partly post-fit; derivation must precede prediction language",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG860_3_allowed_conditional_theorem",
            "claim": "conditional theorem stack now shows the exact missing clauses",
            "status": "allowed_private_nonclaim",
            "reason": "860 connects amplitude target, FLRW shape, local GR, and Newton gates without promoting them",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D860_0",
            "finding": "exact_2over27_is_the_best_parent_amplitude_target",
            "reason": "2/27 is exact from eta=1,a_F=1,DeltaR=2/9 and lies within 0.14 percent of the 859 diagnostic optimum",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D860_1",
            "finding": "amplitude_derivation_and_local_GR_share_a_Ward_projector_blocker",
            "reason": "Q_* endpoint charge and N5 projector stress both require the parent action to own boundary/projector variation",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "attempt a Ward-owned normalized boundary-charge endpoint theorem that also closes or retains N5 projector stress",
            "include": "Q_*, Q_early, Q_today, DeltaR=2/9, a_F trace coupling, T_projector, q_loc suppression",
            "exclude": "new cosmology scoring, fitted endpoint values, plateau axiom, public support claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    optimum = empirical_optimum()
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "aligned the 859 parent-only optimum with the exact 2/27 theorem target and wrote the joint amplitude/GR conditional theorem stack",
            "exact_target": "b_P=2/27 from eta=1,a_F=1,DeltaR=2/9",
            "empirical_alignment": f"859 optimum={fmt(optimum)}, exact_minus_optimum={fmt(TWO_OVER_27 - optimum)}",
            "what_is_not_claimed": "parent prediction, local GR/Newton pass, N5 closure, response source, public evidence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    alignment_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    exact_ok = any(row["alignment_id"] == "AA860_0_exact_identity" and "2/27" in row["mathematical_form"] for row in alignment_rows)
    alignment_ok = any(row["alignment_id"] == "AA860_1_empirical_alignment" and row["status"] == "alignment_pass_diagnostic_only" for row in alignment_rows)
    parent_ok = len(parent_rows) == 5 and any(row["symbol"] == "DeltaR" and row["proof_status"] == "open_hard" for row in parent_rows)
    theorem_ok = len(theorem_rows) == 5 and any(row["theorem_step"] == "CT860_4_unified_gate" for row in theorem_rows)
    local_ok = len(local_rows) == 5 and any(row["gate_id"] == "LG860_2_q_loc_suppression" and row["current_status"] == "open_hard" for row in local_rows)
    ward_ok = len(ward_rows) == 4 and any(row["blocker_id"] == "WP860_0_N5_projector_stress" for row in ward_rows)
    route_ok = any(row["route_id"] == "RC860_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, alignment_rows, parent_rows, theorem_rows, local_rows, ward_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V860_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V860_1_prior_859_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V860_2_exact_2over27_identity_recorded", "result": "pass" if exact_ok else "fail", "detail": "eta=1,a_F=1,DeltaR=2/9 implies b_P=2/27"},
        {"check_id": "V860_3_empirical_alignment_nonclaim", "result": "pass" if alignment_ok else "fail", "detail": "859 optimum alignment recorded as diagnostic only"},
        {"check_id": "V860_4_parent_law_obligations_ready", "result": "pass" if parent_ok else "fail", "detail": "eta, a_F, DeltaR, shape, Bianchi obligations recorded"},
        {"check_id": "V860_5_conditional_theorem_stack_ready", "result": "pass" if theorem_ok else "fail", "detail": "amplitude, shape, local GR, Newton, unified theorem steps recorded"},
        {"check_id": "V860_6_local_GR_Newton_gates_open", "result": "pass" if local_ok else "fail", "detail": "q_loc and source-normalized Newton gates remain explicit"},
        {"check_id": "V860_7_Ward_projector_blockers_ready", "result": "pass" if ward_ok else "fail", "detail": "N5 projector and boundary-charge blockers recorded"},
        {"check_id": "V860_8_route_selected", "result": "pass" if route_ok else "fail", "detail": "Ward-owned boundary charge endpoint plus N5 closure selected"},
        {"check_id": "V860_9_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V860_10_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V860_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V860_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V860_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    alignment_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 860 - Y5 R10 Parent Amplitude Law And GR Limit Derivation Contract",
        "",
        "Current result: **the exact locked amplitude `b_P=2/27` is now the clean parent-law target again**, because it follows from the conditional identity `eta=1`, `a_F=1`, `DeltaR=2/9` and lies almost exactly on the 859 parent-only empirical optimum. This is still not a prediction: the same parent action must derive the boundary charge, trace coupling, and local GR/Newton switch-off.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "exact_target", "empirical_alignment", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Exact 2over27 Alignment",
        "",
        csv_table(alignment_rows, ["alignment_id", "object", "mathematical_form", "value", "comparison", "status", "valid_for_claim"]),
        "",
        "## Parent Amplitude Law Proof Obligations",
        "",
        csv_table(parent_rows, ["obligation_id", "symbol", "target_value", "law_needed", "proof_status", "blocker", "promotion_if_solved", "valid_for_claim"]),
        "",
        "## Conditional Theorem Stack",
        "",
        csv_table(theorem_rows, ["theorem_step", "if_clause", "then_clause", "current_status", "missing", "valid_for_claim"]),
        "",
        "## Local GR Newton Gate Stack",
        "",
        csv_table(local_rows, ["gate_id", "requirement", "pass_condition", "current_status", "residual_if_failed", "valid_for_claim"]),
        "",
        "## Ward Projector Blocker Ledger",
        "",
        csv_table(ward_rows, ["blocker_id", "blocker", "why_it_matters", "required_resolution", "status", "next_action", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    alignment_rows = amplitude_alignment_rows(generated_utc)
    parent_rows = parent_law_rows(generated_utc)
    theorem_rows = conditional_theorem_rows(generated_utc)
    local_rows = local_gr_rows(generated_utc)
    ward_rows = ward_projector_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        alignment_rows,
        parent_rows,
        theorem_rows,
        local_rows,
        ward_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(AMPLITUDE_ALIGNMENT_PATH, alignment_rows, ["alignment_id", "object", "mathematical_form", "value", "comparison", "status", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_LAW_PATH, parent_rows, ["obligation_id", "symbol", "target_value", "law_needed", "proof_status", "blocker", "promotion_if_solved", "valid_for_claim", "generated_utc"])
    write_csv(CONDITIONAL_THEOREM_PATH, theorem_rows, ["theorem_step", "if_clause", "then_clause", "current_status", "missing", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_GR_PATH, local_rows, ["gate_id", "requirement", "pass_condition", "current_status", "residual_if_failed", "valid_for_claim", "generated_utc"])
    write_csv(WARD_PROJECTOR_PATH, ward_rows, ["blocker_id", "blocker", "why_it_matters", "required_resolution", "status", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "exact_target", "empirical_alignment", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, alignment_rows, parent_rows, theorem_rows, local_rows, ward_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"exact_target_b_P={fmt(TWO_OVER_27)}")
    print(f"empirical_optimum_b_P={fmt(empirical_optimum())}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
