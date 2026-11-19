# Inspected startup import failure; no physics calculation ran

probe-01 exited1 at its first import because the continuation wrappers imported the parent source module before common.py installed the inherited module paths. The preflight had already imported common first and verified the correct parent module, so it did not exercise this fresh-entrypoint ordering.

Version2entrypoints import common before the unchanged parent helper. This same repair is applied to all production and screen wrappers. A new probe-02 receipt is used; probe-01 logs and code remain unchanged. The campaign reads successful probe-02 timing and invokes only version2wrappers. This is an inspected entrypoint repair, not a blind failed-run retry or a changed scientific calculation.

