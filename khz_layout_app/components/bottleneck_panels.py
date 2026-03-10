import streamlit as st


def render_bottlenecks(values: dict[str, float]):
    st.markdown("### Bottleneck Heat Bars")
    for k, v in sorted(values.items(), key=lambda x: x[1], reverse=True):
        ratio = min(max(v / 140, 0.0), 1.0)
        label = "caution" if v > 105 else "balanced"
        st.progress(ratio, text=f"{k}: {v:.1f} ({label})")
