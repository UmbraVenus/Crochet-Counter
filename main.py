"""
crochet_counter_v2.py

Streamlit app with step counters per rep.
Each rep has:
 - One number input for standard stitches (SC)
 - One number input for increased stitches (INC), which counts double
Sidebar lets you configure max SC and INC per rep, and shows progress summary.
"""

import streamlit as st

# ── Defaults ─────────────────────────────────────────────────────────────────
DEFAULT_SC   = 2
DEFAULT_INC  = 1
DEFAULT_REPS = 6

def reset_all():
    keys = list(st.session_state.keys())
    for k in keys:
        if k.startswith("rep"):
            del st.session_state[k]
    st.session_state["sc_per_rep"] = DEFAULT_SC
    st.session_state["inc_per_rep"] = DEFAULT_INC
    st.session_state["reps_count"]  = DEFAULT_REPS

def main():
    st.title("🧶 Crochet Step Counter")

    # ── Sidebar Config ────────────────────────────────────────────────────────
    st.sidebar.header("Configuration")

    sc_per_rep = st.sidebar.number_input(
        "Standard stitches per rep",
        min_value=0, value=DEFAULT_SC, step=1, key="sc_per_rep"
    )
    inc_per_rep = st.sidebar.number_input(
        "Increased stitches per rep",
        min_value=0, value=DEFAULT_INC, step=1, key="inc_per_rep"
    )
    reps_count = st.sidebar.number_input(
        "Total reps in row",
        min_value=1, value=DEFAULT_REPS, step=1, key="reps_count"
    )

    if st.sidebar.button("🔄 Reset All"):
        reset_all()

    # ── Derived totals ────────────────────────────────────────────────────────
    stitches_per_rep = sc_per_rep + inc_per_rep * 2
    total_stitches = stitches_per_rep * reps_count

    total_done = 0
    reps_completed = 0

    # ── Display counters for each rep ─────────────────────────────────────────
    for rep in range(1, reps_count + 1):
        st.markdown(f"### Rep {rep} / {reps_count}")

        sc_key = f"rep{rep}_sc"
        inc_key = f"rep{rep}_inc"

        col1, col2 = st.columns(2)
        sc = col1.number_input(
            "Standard stitches", min_value=0, max_value=sc_per_rep,
            key=sc_key, step=1
        )
        inc = col2.number_input(
            "Increased stitches", min_value=0, max_value=inc_per_rep * 2,
            key=inc_key, step=1
        )

        done = sc + inc
        total_done += done

        if sc == sc_per_rep and inc == inc_per_rep * 2:
            reps_completed += 1

    # ── Sidebar summary ───────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader("Progress")
    st.sidebar.write(f"Completed stitches: **{total_done} / {total_stitches}**")
    st.sidebar.write(f"Completed reps: **{reps_completed} / {reps_count}**")


if __name__ == "__main__":
    main()
