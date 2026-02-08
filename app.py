import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בונים את הפונקציה צעד אחר צעד.")

def fmt(n):
    try:
        val = float(n)
        return int(val) if val.is_integer() else round(val, 2)
    except: return n

# קלט פונקציה
expr_in = st.sidebar.text_input("הזן פונקציה:", "x**2 / (x**2 + 2*x - 3)")

if expr_in:
    x_s = sp.symbols('x')
    try:
        f_s = sp.sympify(expr_in)
        num_s, den_s = sp.fraction(f_s)
        
        # חישובי רקע
        pts_raw = sp.solve(den_s, x_s)
        pts_v = sorted([fmt(p.evalf()) for p in pts_raw])
        v_str = ", ".join([str(p) for p in pts_v])
        
        val_h = fmt(sp.limit(f_s, x_s, sp.oo).evalf())

        # שלב 1: תחום הגדרה
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f_s))
        
        u_s1 = st.text_input("אילו ערכים מאפסים את המכנה?", key="s1")
        s1_ok = False
        
        if u_s1:
            try:
                u_v = sorted([float(p.strip()) for p in u_s1.split(",")])
                if np.allclose(u_v, [float(p) for p in pts_v]):
                    st.success("נכון!")
                    s1_ok = True
                else: st.error("לא מדויק.")
            except: st.warning("הזן מספרים עם פסיק.")

        if not s1_ok and st.button("התייאשתי, הצג פתרון"):
            st.info(f"הערכים הם: {v_str}")
            st.session_state['f1'] = True
        
        if st.session_state.get('f1'): s1_ok = True

        # שלב 2: אסימפטוטות אנכיות
        s2_ok = False
        if s1_ok:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            u_s2 = st.text_input("מהן האסימפטוטות האנכיות (x=)?", key="
