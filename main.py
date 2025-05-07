import streamlit as st

# ── Defaults ────────────────────────────────────────────────────────────────
DEFAULT_SC     = 2
DEFAULT_INC    = 1
DEFAULT_REPS   = 6
DEFAULT_ROUND  = 1
DEFAULT_DEC    = 0  # New default for decrease stitches

def reset_all():
    # Preserve the round number
    current_round = st.session_state.get("round_number", DEFAULT_ROUND)

    # Clear rep-related state
    for k in list(st.session_state.keys()):
        if k.startswith("rep"):
            del st.session_state[k]

    # Clear everything else
    st.session_state.clear()

    # Restore round number and defaults (including decrease)
    st.session_state["round_number"] = current_round
    st.session_state["sc_per_rep"]   = DEFAULT_SC
    st.session_state["inc_per_rep"]  = DEFAULT_INC
    st.session_state["reps_count"]   = DEFAULT_REPS
    st.session_state["dec_per_rep"]  = DEFAULT_DEC

def main():
    st.title("🧶 Crochet Step Counter")

    # ── Sidebar Config ───────────────────────────────────────────────────────
    st.sidebar.header("Configuration")

    # Init placeholders for session state config
    for key, val in {
        "round_number": DEFAULT_ROUND,
        "sc_per_rep":   DEFAULT_SC,
        "inc_per_rep":  DEFAULT_INC,
        "reps_count":   DEFAULT_REPS,
        "dec_per_rep":  DEFAULT_DEC,  # Initialize decrease stitches
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

    round_number = st.sidebar.number_input(
        "🧵 Current round",
        min_value=1, value=st.session_state["round_number"], step=1,
        key="round_number"
    )
    sc_per_rep = st.sidebar.number_input(
        "Standard stitches per rep", min_value=0,
        value=st.session_state["sc_per_rep"], step=1,
        key="sc_per_rep"
    )
    inc_per_rep = st.sidebar.number_input(
        "Increased stitches per rep", min_value=0,
        value=st.session_state["inc_per_rep"], step=1,
        key="inc_per_rep"
    )
    dec_per_rep = st.sidebar.number_input(
        "Decrease stitches per rep", min_value=0,
        value=st.session_state["dec_per_rep"], step=1,
        key="dec_per_rep"
    )
    reps_count = st.sidebar.number_input(
        "Total reps in row", min_value=1,
        value=st.session_state["reps_count"], step=1,
        key="reps_count"
    )

    st.sidebar.button("🔄 Reset All", on_click=reset_all)

    # ── Derived totals ───────────────────────────────────────────────────────
    stitches_per_rep = sc_per_rep + inc_per_rep * 2 + dec_per_rep
    total_stitches   = stitches_per_rep * reps_count

    total_done       = 0
    reps_completed   = 0

    # ── Display counters for each rep ─────────────────────────────────────────
    for rep in range(1, reps_count + 1):
        st.markdown(f"### Rep {rep} / {reps_count}")

        sc_key  = f"rep{rep}_sc"
        inc_key = f"rep{rep}_inc"
        dec_key = f"rep{rep}_dec"

        col1, col2, col3 = st.columns(3)
        sc = col1.number_input(
            "Standard stitches", min_value=0, max_value=sc_per_rep,
            key=sc_key, step=1
        )
        inc = col2.number_input(
            "Increased stitches", min_value=0, max_value=inc_per_rep * 2,
            key=inc_key, step=1
        )
        dec = col3.number_input(
            "Decrease stitches", min_value=0, max_value=dec_per_rep,
            key=dec_key, step=1
        )

        done = sc + inc + dec
        total_done += done

        # Mark a rep complete only if all stitch types hit their targets
        if sc == sc_per_rep and inc == inc_per_rep * 2 and dec == dec_per_rep:
            reps_completed += 1

    # ── Sidebar summary ───────────────────────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.subheader("Progress")
    st.sidebar.write(f"🧶 Round: **{round_number}**")
    st.sidebar.write(f"Completed stitches: **{total_done} / {total_stitches}**")
    st.sidebar.write(f"Completed reps: **{reps_completed} / {reps_count}**")

if __name__ == "__main__":
    main()
