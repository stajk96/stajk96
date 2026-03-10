from __future__ import annotations

import streamlit as st

from core.models import LeverParameterDef


def render_parameter_input(param: LeverParameterDef, key: str):
    if param.input_type == "toggle":
        return st.checkbox(param.label, value=bool(param.default), key=key, help=param.description)
    if param.input_type == "selectbox":
        options = param.options or [param.default]
        default_index = options.index(param.default) if param.default in options else 0
        return st.selectbox(param.label, options=options, index=default_index, key=key, help=param.description)
    if param.input_type == "number_input":
        return st.number_input(
            param.label,
            min_value=float(param.min if param.min is not None else 0),
            max_value=float(param.max if param.max is not None else 999999),
            value=float(param.default),
            step=float(param.step if param.step is not None else 1),
            key=key,
            help=param.description,
        )
    return st.slider(
        param.label,
        min_value=float(param.min if param.min is not None else 0),
        max_value=float(param.max if param.max is not None else 1),
        value=float(param.default),
        step=float(param.step if param.step is not None else 0.05),
        key=key,
        help=param.description,
    )
