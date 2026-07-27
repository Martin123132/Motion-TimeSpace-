from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "824-Y5-R10-C2A-Noether-boundary-stress-owner-or-closure-demotion.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_824_SOURCE_REGISTER.csv"
NOETHER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv"
OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_824_BOUNDARY_OWNER_ATTEMPT.csv"
WALL_STRESS_PATH = RESIDUALS / "P8_Y5_R10_824_WALL_STRESS_BOUND_CONTRACT.csv"
CLOSURE_GATE_PATH = RESIDUALS / "P8_Y5_R10_824_CLOSURE_DEMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_824_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_824_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_824_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_824_VALIDATION.csv"

STATUS = "Y5_R10_824_Noether_boundary_owner_not_derived_C2A_domain_route_demoted_to_closure_nonclaim"
CLAIM_CEILING = "explicit_C2A_closure_contract_only_no_parent_Noether_owner_no_local_GR_claim"
NEXT_TARGET = "825-Y5-R10-C2A-closure-contract-and-parent-route-reset.md"

SOURCE_SPECS = [
    {
        "source_id": "823_doc",
        "path": POST_CHECKPOINT / "823-Y5-R10-C2A-boundary-current-representative-or-domain-demotion.md",
        "needles": [
            "Current result: **a kinematic `J_rel` representative exists",
            "T823_3_Noether_gap",
            "824-Y5-R10-C2A-Noether-boundary-stress-owner-or-closure-demotion.md",
        ],
        "role": "immediate handoff: kinematic current exists but Noether/stress owner is missing",
    },
    {
        "source_id": "823_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_823_VALIDATION.csv",
        "needles": [
            "V823_4_Noether_stress_failure_recorded,pass",
            "V823_7_next_target_selected,pass,824-Y5-R10-C2A-Noether-boundary-stress-owner-or-closure-demotion.md",
            "V823_8_all_rows_nonclaim,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "143_domain_selector",
        "path": POST_CHECKPOINT / "143-domain-selector-variational-action-attempt.md",
        "needles": [
            "D is the main blocker.",
            "algebraic multiplier boundary | open | derive Noether identity with `D` variation",
            "boundary exchange owned | fail open | `J_rel` representative not derived",
            "boundary not hand tuned = fail open.",
        ],
        "role": "domain action attempt and boundary-owner obstruction",
    },
    {
        "source_id": "138_pressure_kernel",
        "path": POST_CHECKPOINT / "138-coherent-volume-pressure-kernel-theorem.md",
        "needles": [
            "boundary terms owned by `J_rel` | open",
            "safe boundary variation / J_rel;",
            "local N_D = 0 and delta N_D = 0 theorem;",
        ],
        "role": "coherent-volume stress mechanics and boundary terms",
    },
    {
        "source_id": "797_Ward_contract",
        "path": POST_CHECKPOINT / "797-Y5-R10-parent-relaxation-source-action-contract-and-Gammaeff-screening-gate.md",
        "needles": [
            "PAC797_3_Ward_identity",
            "Show the relaxation stress/exchange contribution preserves total diffeomorphism Ward identity and Bianchi consistency.",
            "missing_stress_variation",
        ],
        "role": "Ward/Bianchi consistency contract for any repair term",
    },
    {
        "source_id": "formal_red_team",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": [
            "### 1.1 The Bianchi identity problem is the main gate",
            "Any future sector that varies `Gamma_eff` while omitting `q^nu` or `K_hat` is hiding nonconservation.",
            "Do not claim the local PPN problem is solved until source support, boundary amplitude",
        ],
        "role": "anti-cheat conservation and local boundary warning",
    },
    {
        "source_id": "85_XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "transition shells remain local PPN obligations,",
            "not galaxy/cosmology sources.",
            "source-power closure open.",
        ],
        "role": "firewall preventing transition shells becoming hidden large-scale sources",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


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


def noether_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "N824_0_diffeomorphism_identity",
            "statement": "For a true domain sector S_D[g, Phi, D] with diffeomorphism invariance, delta_xi S_D=0 gives a Ward identity: nabla_mu T_D^{mu nu}=sum_A E_A nabla^nu Phi_A plus boundary terms.",
            "attempted_derivation": "Use Lie variation of g and fields, integrate by parts, and require either field equations or natural boundary/jump conditions.",
            "result": "conditional_identity_only",
            "missing_input": "explicit parent S_D and domain variables are absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "N824_1_boundary_current_owner",
            "statement": "A Noether-safe J_rel must be the boundary projection of a stress/current, schematically n_mu T_D^{mu nu} or an equivalent Noether charge on partial D.",
            "attempted_derivation": "Identify the 823 scalar flux Phi_rel with a variational boundary flux.",
            "result": "fails_as_derivation",
            "missing_input": "823 defines only a kinematic flux representative, not T_D, a Noether charge, or boundary equations of motion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "N824_2_nonunique_representative",
            "statement": "Phi_rel=int_partialD v_rel dSigma=int_D div_D J_rel dV fixes only the divergence/flux class, so J_rel can be shifted by divergence-free pieces without changing 823.",
            "attempted_derivation": "Try to promote the representative itself to a physical current.",
            "result": "blocked_by_gauge_nonuniqueness",
            "missing_input": "equivalence class, gauge condition, or action principle selecting a unique representative",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "N824_3_Ccoh_multiplier_limit",
            "statement": "The C_coh auxiliary multiplier can enforce chi_D=C_coh[D] after D is supplied.",
            "attempted_derivation": "Vary the multiplier sector and then vary D/boundary data.",
            "result": "selector_not_owner",
            "missing_input": "zero-knob Euler equation selecting D and cancelling boundary terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "N824_4_Bianchi_conservation_gate",
            "statement": "Any boundary exchange that modifies Gamma_eff or K_hat must appear in the total conservation identity rather than as an unowned local metric source.",
            "attempted_derivation": "Use the formal q^nu/K_hat conservation spine as the anti-cheat rule.",
            "result": "gate_confirmed_not_closed",
            "missing_input": "stress variation and total conserved tensor for the boundary/domain sector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def owner_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "O824_0_phase_field_domain",
            "candidate_owner": "promote D to a smooth phase field chi with kinetic/gradient/potential action",
            "what_it_would_buy": "standard Hilbert stress and natural boundary conditions",
            "failure_mode": "introduces a new scale, surface tension, extra modes, and local stress unless all are parent-derived and bounded",
            "verdict": "reject_for_promotion_keep_as_possible_future_parent_if_coefficients_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "O824_1_domain_wall_embedding",
            "candidate_owner": "treat partial D as an embedding with wall action S_wall=-sigma_D int_Sigma dSigma plus couplings",
            "what_it_would_buy": "boundary stress tensor and jump conditions",
            "failure_mode": "nonzero sigma_D creates exactly the transition-shell wall stress that local PPN/R10 gates fear; sigma_D=0 removes the dynamical owner",
            "verdict": "fails_without_sourced_sigma_bound_or_zero_wall_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "O824_2_auxiliary_Ccoh_multiplier",
            "candidate_owner": "use the existing algebraic C_coh multiplier as the owner",
            "what_it_would_buy": "clean branch bookkeeping with minimal new dynamics",
            "failure_mode": "it constrains chi_D after the domain is supplied but does not select D or own moving-boundary stress",
            "verdict": "closure_not_parent_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "O824_3_volume_transport_current",
            "candidate_owner": "use the 823 Reynolds/volume-transport J_rel representative directly",
            "what_it_would_buy": "local frozen and FLRW comoving limits remain algebraically clean",
            "failure_mode": "kinematic current has no stress tensor, no unique representative, and no Ward identity",
            "verdict": "bookkeeping_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "O824_4_nonlocal_quarantine_owner",
            "candidate_owner": "route boundary current into a nonlocal/quarantined sector rather than local metric gravity",
            "what_it_would_buy": "could avoid direct local PPN projection while preserving conservation bookkeeping",
            "failure_mode": "no parent kernel/action currently derives the quarantine projector or observable response zero",
            "verdict": "possible_later_closure_not_a_Noether_owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def wall_stress_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "W824_0_wall_energy",
            "quantity": "sigma_D or equivalent boundary energy density",
            "required_bound": "kappa_GR*sigma_D*L_test and any induced delta g must be below the strictest local PPN/R10/clock/orbital budget",
            "current_status": "missing_numeric_and_parent_source",
            "why_it_matters": "a domain wall that owns J_rel can itself become the excluded local stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "W824_1_boundary_divergence",
            "quantity": "P_loc nabla_mu T_D^{mu nu} on transition shells",
            "required_bound": "zero by Ward identity or below q_loc response bounds after projection",
            "current_status": "missing_TD_and_projection_map",
            "why_it_matters": "local safety needs the divergence source, not only the integrated flux, to be owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "W824_2_jump_conditions",
            "quantity": "metric/connection/memory jumps across partial D",
            "required_bound": "natural boundary conditions force no PPN-sized discontinuity or hair",
            "current_status": "missing_boundary_Euler_equations",
            "why_it_matters": "hand-picked continuity would smuggle in the plateau axiom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "W824_3_matter_readout",
            "quantity": "ordinary matter coupling to boundary/domain variables",
            "required_bound": "species-independent descent or explicit WEP/clock bound",
            "current_status": "missing_matter_descent",
            "why_it_matters": "an owned boundary sector can still fail if matter sees it directly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G824_0_Noether_owner_exists",
            "gate": "Can J_rel be derived as a Noether/stress current from present parent sources?",
            "result": "fail",
            "consequence": "no parent-derived C2A domain mechanics and no local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G824_1_boundary_stress_bounded",
            "gate": "Is transition-shell wall stress zero or quantitatively below local bounds?",
            "result": "fail_open",
            "consequence": "boundary owner attempts create the same stress object they must suppress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G824_2_closure_demotion",
            "gate": "Should the C2A domain route be retained?",
            "result": "demote_to_explicit_closure_only",
            "consequence": "keep the useful FLRW/local bookkeeping grammar, but label it as closure until a parent owner exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G824_3_data_firewall",
            "gate": "Can this branch be used for SN/BAO/CMB/growth or local claims?",
            "result": "fail",
            "consequence": "no data run or claim until parent coefficients or a declared closure model are explicitly separated",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D824_0",
            "decision": "Noether/boundary-stress owner is not derived from the current corpus",
            "reason": "the symbolic Ward identity is known, but the action, domain variables, stress tensor, boundary equations, and wall-stress bounds are missing",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D824_1",
            "decision": "C2A domain mechanics is demoted to explicit closure-only",
            "reason": "the branch remains useful as a private grammar for local/FLRW bookkeeping, but it is not a parent field theory until the owner exists",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "write the explicit C2A closure contract, firewall it from parent-derived claims, and select the next parent route after the domain-owner failure",
            "allowed_work": "closure contract, claim labels, source/action route reset, parent coefficient checklist",
            "forbidden_work": "public claim, data fitting as evidence, local-GR pass, or treating C2A closure as derived",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "a conditional Ward identity shape and a useful local/FLRW domain-transport closure grammar",
            "what_failed": "parent Noether owner, unique J_rel, domain Euler equation, wall-stress bound, and local-GR promotion",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    noether_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V824_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_823, clean_823_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_823_VALIDATION.csv")
    add("V824_1_prior_823_clean", clean_823, clean_823_detail)
    add(
        "V824_2_Noether_identity_recorded",
        any(row["audit_id"] == "N824_0_diffeomorphism_identity" for row in noether_rows),
        "conditional diffeomorphism/Ward identity recorded",
    )
    add(
        "V824_3_owner_attempts_fail_without_parent_action",
        any(row["attempt_id"] == "O824_2_auxiliary_Ccoh_multiplier" and row["verdict"] == "closure_not_parent_derivation" for row in owner_rows)
        and any(row["attempt_id"] == "O824_3_volume_transport_current" and row["verdict"] == "bookkeeping_only" for row in owner_rows),
        "C_coh and J_rel attempts are explicitly non-parent closures",
    )
    add(
        "V824_4_wall_stress_contract_present",
        {"W824_0_wall_energy", "W824_1_boundary_divergence", "W824_2_jump_conditions"}.issubset({row["bound_id"] for row in stress_rows}),
        "wall energy, divergence, and jump condition bounds recorded",
    )
    add(
        "V824_5_closure_demotion_selected",
        any(row["gate_id"] == "G824_2_closure_demotion" and row["result"] == "demote_to_explicit_closure_only" for row in closure_rows),
        "C2A domain route demoted to closure-only",
    )
    add(
        "V824_6_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V824_7_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + noether_rows + owner_rows + stress_rows + closure_rows + decisions + next_rows + summary
    add(
        "V824_8_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V824_9_no_data_or_local_GR_claim",
        all("data fitting as evidence" in row["forbidden_work"] and "local-GR pass" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V824_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V824_11_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    noether_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 824 - Y5 R10 C2A Noether Boundary-Stress Owner Or Closure Demotion",
            (
                "Current result: **the Noether/boundary-stress owner is not derived from the current corpus, so the C2A domain route is demoted to explicit closure-only**. "
                "The good news is that the exact missing object is now clean: a parent action must own the domain variable, the boundary current, the boundary stress, and the Ward identity together."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Noether Variation Audit\n\n" + markdown_table(noether_rows, ["audit_id", "statement", "attempted_derivation", "result", "missing_input", "valid_for_claim"]),
            "## Boundary Owner Attempt\n\n" + markdown_table(owner_rows, ["attempt_id", "candidate_owner", "what_it_would_buy", "failure_mode", "verdict", "valid_for_claim"]),
            "## Wall-Stress Bound Contract\n\n" + markdown_table(stress_rows, ["bound_id", "quantity", "required_bound", "current_status", "why_it_matters", "valid_for_claim"]),
            "## Closure Demotion Gate\n\n" + markdown_table(closure_rows, ["gate_id", "gate", "result", "consequence", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a demotion, not a collapse. The route still helps as a disciplined closure grammar, but it cannot be sold to ourselves as derived field theory. "
            "The next move is to quarantine C2A as closure, then reset to the least-cheaty parent-source route with an explicit coefficient/action checklist.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    noether_rows = noether_audit_rows(generated_utc)
    owner_rows = owner_attempt_rows(generated_utc)
    stress_rows = wall_stress_rows(generated_utc)
    closure_rows = closure_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, noether_rows, owner_rows, stress_rows, closure_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(NOETHER_AUDIT_PATH, noether_rows, ["audit_id", "statement", "attempted_derivation", "result", "missing_input", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_ATTEMPT_PATH, owner_rows, ["attempt_id", "candidate_owner", "what_it_would_buy", "failure_mode", "verdict", "valid_for_claim", "generated_utc"])
    write_csv(WALL_STRESS_PATH, stress_rows, ["bound_id", "quantity", "required_bound", "current_status", "why_it_matters", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_GATE_PATH, closure_rows, ["gate_id", "gate", "result", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, noether_rows, owner_rows, stress_rows, closure_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"824 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
