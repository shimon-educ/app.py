import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("כאן בונים את הפונקציה צעד אחר צעד.")

def format_num(n):
    try:
        val = float(n)
        return int(val) if val.is_integer() else round(val, 2)
    except:
        return n

input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        
        # חישוב נתונים
        domain_solutions = sp.solve(den, x)
        true_pts = sorted([format_num(p.evalf()) for p in domain_solutions])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        horiz_limit = sp.limit(f, x, sp.oo)
        horiz_val = format_num(horiz_limit.evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        with st.expander("🤔 איך מוצאים תחום הגדרה?"):
            st.write("משווים את המכנה לאפס ($המכנה = 0$) ומוצאים את ה-x הבעייתיים.")

        u_domain = st.text_input("מהם הערכים שמאפסים את המכנה?", key="s1_in")
        s1_passed = False
        
        if u_domain:
            try:
                u_pts = sorted([float(p.strip()) for p in u_domain.split(",")])
                if np.allclose(u_pts, [float(p) for p in true_pts]):
                    st.success("נכון!")
                    s1_passed = True
                else:
                    st.error("לא מדויק.")
            except: st.warning("הזן מספרים מופרדים בפסיק.")

        if not s1_passed and st.button("התייאשתי, הצג פתרון"):
            st.info(f"מהלך הפתרון: פותרים את {sp.latex(den)}=0")
            st.write(f"הערכים הם: {true_pts_str}")
            st.session_state['f_s1'] = True

        if st.session_state.get('f_s1'): s1_passed = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        s2_passed = False
        if s1_passed:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            u_v = st.text_input("מהן האסימפטוטות האנכיות? (x=?)", key="s2_in")
            if u_v:
                try:
                    v_vals = sorted([float(p.strip()) for p in u_v.split(",")])
                    if np.allclose(v_vals, [float(p) for p in true_pts]):
                        st.success("מעולה!")
                        s2_passed = True
                except: pass
            
            if not s2_passed and st.button("התייאשתי, סמן בגרף"):
                st.session_state['f_s2'] = True
        
        if st.session_state.get('f_s2'): s2_passed = True

        # --- שלב 3: אסימפטוטה אופקית ---
        s3_passed = False
        if s2_passed:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            with st.expander("🤔 איך מוצאים אסימפטוטה אופקית?"):
                st.write("**כלל יחס המקדמים:** אם דרגת המונה והמכנה שווה, מחלקים את המקדמים של החזקה הכי גבוהה.")
                st.write("**למשל:** ב-$f(x)=\\frac{3x^2}{1x^2}$ האסימפטוטה היא $y=3$.")

            u_h = st.text_input("מהי האסימפטוטה האופקית? (y=?)", key="s3_in")
            if u_h:
                try:
                    if np.isclose(float(u_h), float(horiz_val)):
                        st.success(f"נכון! y = {horiz_val}")
                        s3_passed = True
                    else: st.error("טעות. בדוק את יחס המקדמים.")
                except: pass
            
            if not s3_passed and st.button("התייאשתי, הצג אופקית"):
                st.info(f"האסימפטוטה היא y = {horiz_val}")
                st.session_state['f_s3'] = True

        if st.session_
