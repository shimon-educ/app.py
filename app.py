import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# --- סרגל צד: הנחיות כתיבה והזנת פונקציה ---
st.sidebar.header("📝 איך מזינים פונקציה?")
st.sidebar.info("""
השתמש בסימנים הבאים:
* **חזקה:** `**` (למשל `x**2`)
* **כפל:** `*` (למשל `2*x`)
* **חילוק:** `/` (למשל `1/x`)
* **דוגמה:** `x**2 / (x**2 - 4)`
""")

# קבלת הקלט וניקוי רווחים אוטומטי
raw_input = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")
input_func = raw_input.replace(" ", "")

# פונקציית עזר לעיצוב מספרים
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        
        # חישוב תחום הגדרה (רק פתרונות ממשיים למניעת שגיאות בחזקות גבוהות)
        true_domain_raw = sp.solve(den, x)
        true_pts = sorted([format_num(sol.evalf()) for sol in true_domain_raw if sol.is_real])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("""
            **מה זה בכלל תחום הגדרה?**
            במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.
            **השלבים:** משווים את המכנה לאפס ($המכנה = 0$) ופתורים את המשוואה.
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
                    st.info("נראה שזו לא התשובה הנכונה. נסה שוב בעזרת הרמזים למטה.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.success(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            # --- אסימפטוטות אנכיות ---
            st.subheader("1. אסימפטוטות אנכיות")
            with st.expander("💡 רמז מפורט: אסימפטוטה אנכית"):
                st.write("הן נמצאות בערכי ה-x שגורמים למכנה להיות אפס.")
                st.info(f"הערכים שמצאת בשלב הקודם הם: **{true_pts_str}**")
                st.write("התשובה צריכה להיכתב כ: **x = מספר**.")

            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (x = ?):", key="asymp_input")
            
            # --- אסימפטוטה אופקית ---
            st.subheader("2. אסימפטוטה אופקית")
            with st.expander("💡 רמז מפורט: אסימפטוטה אופקית"):
                st.markdown("""
                1. **חזקה גבוהה למטה:** $y = 0$.
                2. **חזקות שוות:** מחלקים את המקדמים של החזקות הגבוהות.
                3. **חזקה גבוהה למעלה:** אין אסימפטוטה אופקית.
                """)
                st.write("התשובה צריכה להיכתב כ: **y = מספר** (או 'אין').")

            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            show_plot = False
            if user_asymp and user_horiz:
                true_horiz_lim = sp.limit(f, x, sp.oo)
                try:
                    clean_asymp = user_asymp.replace('x', '').replace('=', '').strip()
                    clean_hor
