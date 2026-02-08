import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בונים את פתרון הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיגול מספרים להצגה נוחה
def fmt(n):
    try:
        val = float(n)
        return int(val) if val.is_integer() else round(val, 2)
    except: return n

# הזנת פונקציה בתפריט הצד
expr_input = st.sidebar.text_input("הזן פונקציה:", "x**2 / (x**2 + 2*x - 3)")

if expr_input:
    x_sym = sp.symbols('x')
    try:
        f_sym = sp.sympify(expr_input)
        num_sym, den_sym = sp.fraction(f_sym)
        
        # חישוב נתוני אמת
        raw_v = sp.solve(den_sym, x_sym)
        true_v = sorted([fmt(p.evalf()) for p in raw_v])
        true_v_str = ", ".join([str(p) for p in true_v])
        
        raw_h = sp.limit(f_sym, x_sym, sp.oo)
        true_h = fmt(raw_h.evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f_sym))
        
        with st.expander("🤔 איך מוצאים? (תיאוריה)"):
            st.write("נשווה את המכנה לאפס כדי למצוא אילו איקסים 'אסורים' לשימוש.")

        user_s1 = st.text_input("אילו ערכים מאפסים את המכנה?", key="input_s1")
        s1_done = False
        
        if user_s1:
            try:
                u_vals = sorted([float(p.strip()) for p in user_s1.split(",")])
                if np.allclose(u_vals, [float(p) for p in true_v]):
                    st.success("מעולה! אלו בדיוק הערכים.")
                    s1_done = True
                else: st.error("לא בדיוק, נסה שוב.")
            except: st.warning("הזן מספרים מופרדים בפסיק.")

        if not s1_done:
            if st.button("התייאשתי, הצג פתרון"):
                st.info(f"השווינו את המכנה לאפס: {sp.latex(den_sym)}=0")
                st.write(f"הערכים הם: {true_v_str}")
                st.session_state['skip_s1'] = True
        
        if st.session_state.get('skip_s1'): s1_done = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        s2_done = False
        if s1_done:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            user_s2 = st.text_input("מהן האסימפטוטות האנכיות? (x=?)", key="input_s2")
            if user_s2:
                try:
                    u_v_vals = sorted([float(p.strip()) for p in user_s2.split(",")])
                    if np.allclose(u_v_vals, [float(p) for p in true_v]):
                        st.success("נכון! אלו הקווים האנכיים.")
                        s2_done = True
                    else: st.error("אלו לא האסימפטוטות. רמז: הסתכל על תחום ההגדרה.")
                except: pass
            
            if not s2_done and st.button("התייאשתי, סמן בגרף"):
                st.session_state['skip_s2'] = True
        
        if st.session_state.get('skip_s2'): s2_done = True

        # --- שלב 3: אסימפטוטות אופקיות ---
        s3_done = False
        if s2_done:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            with st.expander("🤔 איך מוצאים אופקית? (הסבר)"):
                st.write("**שיטת יחס המקדמים:**")
                st.write("אם החזקה הכי גבוהה במונה ובמכנה זהה (למשל $x^2$), מחלקים את המקדמים שלהם.")
                st.write("**דוגמה:** ב- $f(x)=\\frac{2x^2}{1x^2+1}$ האסימפטוטה היא $y = \\frac{2}{1} = 2$.")

            user_s3 = st.text_input("מהי האסימפטוטה האופקית? (y=?)", key="input_s3")
            if user_s3:
                try:
                    if np.isclose(float(user_s3), float(true_h)):
                        st.success(f"נכון מאוד! y = {true_h}")
                        s3_done = True
                    else: st.error("לא נכון. בדוק שוב את יחס המקדמים של החזקות הגבוהות.")
                except: pass
            
            if not s3_done and st.button("התייאשתי, הוסף לגרף"):
                st.info(f"האסימפטוטה האופקית היא y = {true_h}")
                st.session_state['skip_s3'] = True

        if st.session_state.get('skip_s3'): s3_done = True
