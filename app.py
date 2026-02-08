import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

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
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # חישוב אסימפטוטה אופקית (גבול באינסוף)
        horiz_asy = sp.limit(f, x, sp.oo)
        horiz_val = format_num(horiz_asy.evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("במתמטיקה אסור לחלק באפס. לכן נשווה את המכנה לאפס ונמצא את ה-x הבעייתיים.")
        
        user_domain = st.text_input("הזן ערכים שמאפסים את המכנה:", key="domain_input")
        step_1_passed = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("נכון!")
                    step_1_passed = True
                else:
                    st.error("לא מדויק.")
                    if st.button("התייאשתי, הצג פתרון שורשים"):
                        st.session_state['force_step_2'] = True
            except: st.warning("הזן מספרים עם פסיק.")

        if st.session_state.get('force_step_2'):
            step_1_passed = True
            st.info(f"הערכים הם: {true_pts_str}")

        # --- שלב 2: אסימפטוטות אנכיות ---
        step_2_passed = False
        if step_1_passed:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            st.write("מהן משוואות האסימפטוטות האנכיות?")
            user_asymp_v = st.text_input("הזן ערכי x (למשל: 3, 1-):", key="v_asymp")
            
            if user_asymp_v:
                try:
                    v_pts = sorted([float(p.strip()) for p in user_asymp_v.split(",")])
                    if np.allclose(v_pts, [float(p) for p in true_pts]):
                        st.success("נכון! אלו ה'קירות' האנכיים.")
                        step_2_passed = True
                    else: st.error("נסה שוב.")
                except: pass
            
            if st.button("התייאשתי, סמן אסימפטוטות אנכיות"):
                step_2_passed = True
                st.session_state['v_asymp_done'] = True

        # --- שלב 3: אסימפטוטה אופקית ---
        step_3_passed = False
        if step_2_passed or st.session_state.get('v_asymp_done'):
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            
            with st.expander("🤔 איך מוצאים אסימפטוטה אופקית?"):
                st.write("""
                אסימפטוטה אופקית בודקת מה קורה ל-y כשה-x הופך למספר ענק ($ \infty $).
                **טיפ מהיר:** * אם החזקה הכי גבוהה במונה ובמכנה שווה (כמו $x^2/x^2$), האסימפטוטה היא יחס המקדמים.
                * למשל ב-$f(x) = \\frac{2x^2}{1x^2+5}$, האסימפטוטה היא $y = \\frac{2}{1} = 2$.
                """)

            user_asymp_h = st.text_input("מהי האסימפטוטה האופקית? כתוב רק את המספר (y=?):", key="h_asymp")
            
            if user_asymp_h:
                try:
                    if np.isclose(float(user_asymp_h), float(horiz_val)):
                        st.success(f"מעולה! y = {horiz_val}")
                        step_3_passed = True
                    else: st.error("לא בדיוק. בדוק את יחס המקדמים של החזקה הכי גבוהה.")
                except: pass
            
            if st.button("התייאשתי, הצג אסימפטוטה אופקית"):
                st.info(f"האסימפטוטה האופקית היא y = {horiz_val}")
                step_3_passed = True
                st.session_state['h_asymp_done'] = True

        # --- הגרף האינטראקטיבי המצטבר ---
        if step_2_passed or st.session_state.get('v_asymp_done'):
            st.subheader("מפת הדרכים של הפונקציה (הגרף שלך)")
            fig = go.Figure()

            # הדגשת צירים (x ו-y)
            fig.update_xaxes(showline=True, linewidth=3, linecolor='black', mirror=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')
            fig.update_yaxes(showline=True, linewidth=3, linecolor='black', mirror=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')

            # אסימפטוטות אנכיות (אדום)
            for pt in true_
