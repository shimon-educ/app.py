import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy - מעבדת החקירה", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיצוב מספרים (הסרת .0 ממספרים שלמים)
def format_num(n):
    n_float = float(n)
    return int(n_float) if n_float.is_integer() else round(n_float, 2)

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת רשימת פתרונות נקייה (מספרים שלמים או עשרוניים ללא .0 מיותר)
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        # יצירת מחרוזת יפה להצגה (למשל: 1, 3-)
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(f"f(x) = {sp.latex(f)}")
        st.write("כדי למצוא את תחום ההגדרה, עלינו למצוא אילו ערכי $x$ מאפסים את המכנה.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                # השוואה עם סובלנות לטעויות עיגול קטנות
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("הערכים האלו לא מאפסים את המכנה. נסה שוב.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write(f"עליך לפתור את המשוואה: ${sp.latex(den)} = 0$")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        factored_den = sp.factor(den)
                        st.write(f"אפשר לכתוב את המכנה כך: ${sp.latex(factored_den)} = 0$")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.info(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות וגרף ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: הצגה גרפית")
            st.write(f"נקודות אי-
