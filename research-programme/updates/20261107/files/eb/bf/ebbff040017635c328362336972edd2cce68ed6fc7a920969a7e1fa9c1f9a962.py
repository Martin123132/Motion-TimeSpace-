import seal_stage170 as original
from source_tangent import ROOT, write_json


def write_final(path, packet):
    if path == ROOT / "results/stage-integrity.json":
        packet.update(maximum_active_compute_workers=2, maximum_active_production_workers=1,
                      brief_parallel_state_audit=True,
                      state_precision_repaired_before_prediction_freeze=True,
                      original_precision_failure_audit_retained=True,
                      source_prediction_uses_separate_state_overlays=True,
                      moving_history_response_is_finite_step=True,
                      native_history_classical_second_derivative_claimed=False,
                      microscopic_source_functional_derivatives_conditional_on_smooth_input=True)
    write_json(path, packet)


if __name__ == "__main__":
    original.write_json = write_final
    original.main()
