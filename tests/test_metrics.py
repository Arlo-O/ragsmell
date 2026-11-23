from ragsmell.metrics import module_metrics


def test_module_metrics_distinguishes_standard_and_external_imports():
    metrics = module_metrics("import os\nimport pandas\n\ndef f(x):\n    return x\n")
    assert metrics["sloc"] == 4
    assert metrics["cc_max"] >= 1
    assert metrics["cbo_mod"] == 1
