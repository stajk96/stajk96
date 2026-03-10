from core.formulas import clamp, indexed_kpi, sat_gain


def test_clamp():
    assert clamp(2, 0, 1) == 1


def test_sat_gain_increasing():
    assert sat_gain(0.5) > sat_gain(0.2)


def test_indexed_kpi_caps():
    assert indexed_kpi(100, 10, 0) <= 150
