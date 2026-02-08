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
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק...")
                    if st.button("התייאשתי, המשך לשלב הבא"):
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
                        if st.button("דלג לשלב הבא"):
                            st.session_state['force_step_3'] = True
                            st.rerun()
                except: pass

        if st.session_state.get('force_step_3'):
            show_step_3 = True

        # --- שלב 3: אסימפטוטה אופקית (התוספת החדשה) ---
        show_plot = False
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            
            # חישוב אסימפטוטה אופקית אמיתית
            horiz_asymp_val = sp.limit(f, x, sp.oo)
            
            st.write("כדי למצוא אסימפטוטה אופקית, נבדוק מה קורה ל-y כשה-x שואף לאינסוף.")
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (רשום את המספר בלבד, למשל: 1):", key="horiz_input")
            
            if user_horiz:
                try:
                    if float(user_horiz) == float(horiz_asymp_val):
                        st.success(f"מעולה! האסימפטוטה האופקית היא y = {user_horiz}")
                        show_plot = True
                    else:
                        st.error("רמז: הסתכל על המקדמים של החזקה הכי גבוהה.")
                        if st.button("הצג פתרון ושרטט"):
                            st.info(f"האסימפטוטה האופקית היא y = {horiz_asymp_val}")
                            st.session_state['force_plot'] = True
                            st.rerun()
                except: pass

        if st.session_state.get('force_plot'):
            show_plot = True

        # שרטוט מערכת הצירים והאסימפטוטות
        if show_plot:
            st.subheader("ה'שלד' של הפונקציה על מערכת הצירים:")
            fig = go.Figure()
            
            # הוספת אסימפטוטות אנכיות (באדום)
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
            
            # הוספת אסימפטוטה אופקית (בכחול)
            h_val = float(sp.limit(f, x, sp.oo))
            fig.add_hline(y=h_val, line_dash="dash", line_color="blue", annotation_text=f"y={
