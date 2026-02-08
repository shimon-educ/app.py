import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיצוב מספרים
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת פתרונות נקיים
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("""
            **מה זה בכלל תחום הגדרה?**
            במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.
            """)
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק...")
                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except: st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (למשל: 3, 1-):", key="asymp_input")
            
            if user_asymp:
                try:
                    user_asy_pts = sorted([float(p.strip()) for p in user_asymp.split(",")])
                    if np.allclose(user_asy_pts, [float(p) for p in true_pts]):
                        st.success(f"נכון מאוד! x = {user_asymp}")
                        show_step_3 = True
                    else:
                        st.error("אלו לא האסימפטוטות.")
                        if st.button("המשך לשלב הבא"):
                            st.session_state['force_step_3'] = True
                            st.rerun()
                except: pass

        if st.session_state.get('force_step_3'):
            show_step_3 = True

        # --- שלב 3: אסימפטוטה אופקית (חדש!) ---
        show_plot = False
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            
            with st.expander("🤔 איך מוצאים אסימפטוטה אופקית?"):
                st.write("אנחנו בודקים מה קורה לערך ה-y של הפונקציה כאשר x שואף לאינסוף או למינוס אינסוף.")
            
            # חישוב אסימפטוטה אופקית אמיתית
            horiz_asymp = sp.limit(f, x, sp.oo)
            
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (כתוב את ערך ה-y, למשל: 1):", key="horiz_input")
            
            if user_horiz:
                try:
                    if float(user_horiz) == float(horiz_asymp):
                        st.success(f"מצוין! האסימפטוטה האופקית היא y = {user_horiz}")
                        show_plot = True
                    else:
                        st.error(f"לא מדויק. רמז: בדוק את היחס בין המקדם של החזקה הכי גבוהה במונה לבין המכנה.")
                        if st.button("הצג פתרון ושרטט"):
                            st.info(f"האסימפטוטה האופקית היא y = {horiz_asymp}")
                            st.session_state['force_plot'] = True
                            st.rerun()
                except: pass

        if st.session_state.get('force_plot'):
            show_plot = True

        # מערכת צירים משודרגת
        if show_plot:
            st.subheader("מערכת הצירים עם האסימפטוטות:")
            fig = go.Figure()
            
            # אסימפטוטות אנכיות
