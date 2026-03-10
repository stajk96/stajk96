from core.audit import log_change


def test_log_change():
    e = log_change("site", "sc", "id", "label", 0, 1, "why", ["v"], ["b"], ["k"])
    assert e.new_value == 1
