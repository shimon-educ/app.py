import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בונים את פתרון הפונקציה צעד אחר צעד.")

# פונקציות עזר
def fmt(n):
    try:
        num = float(n)
        return int(num) if num.is_integer() else round(num, 2)
    except: return n

# קלט מהמשתמש
expr_str = st.sidebar.text_input("הזן פונקציה:", "x**2 / (x**2 + 2*x - 3)")

if expr_str:
    x = sp.symbols('x')
    try:
        f = sp.sympify(expr_str)
        num, den = sp.fraction(f)
        
        # חישוב נתונים מתמטיים
        asym_v_raw = sp.solve(den, x)
        asym_v_pts = sorted([fmt(p.evalf()) for p in asym_v_raw])
        v_str = ", ".join([str(p) for p in asym_v_pts])
        
        asym_h_val = fmt(sp.limit(f, x, sp.oo).evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        with st.expander("🤔 איך מוצאים? (תיאוריה)"):
            st.write("משווים את המכנה לאפס ($Mecane=0$) כדי למצוא איפה הפונקציה 'מתפוצצת'.")

        ans1 = st.text_input("אילו ערכים מאפסים את המכנה?", key="ans1")
        s1_ok = False
        
        if ans1:
            try:
                u_pts = sorted([float(p.strip()) for p in ans1.split(",")])
                if np.allclose(u_pts, [float(p) for p in asym_v_pts]):
                    st.success("נכון!")
                    s1_ok = True
                else: st.error("לא מדויק.")
            except: st.warning("הזן מספרים עם פסיק.")

        if not s1_ok and st.button("התייאשתי, הצג דרך"):
            st.info("נפתור את המכנה בעזרת נוסחת השורשים:")
            try:
                poly = sp.Poly(den, x)
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3:
                    a, b, c = [fmt(v) for v in coeffs]
                    st.latex(rf"x_{{1,2}} = \frac{{-{b} \pm \sqrt{{{b}^2 - 4 \cdot {a} \cdot {c}}}}}{{2 \cdot {a}}}")
            except: pass
            st.write(f"הערכים הם: {v_str}")
            st.session_state['skip1'] = True

        if st.session_state.get('skip1'): s1_ok = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        s2_ok = False
        if s1_ok:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            ans2 = st.text_input("מהן משוואות האסימפטוטות האנכיות (x=)?", key="ans2")
            if ans2:
                try:
                    u_v = sorted([float(p.strip()) for p in ans2.split(",")])
                    if np.allclose(u_v, [float(p) for p in asym_v_pts]):
                        st.success("מעולה!")
                        s2_ok = True
