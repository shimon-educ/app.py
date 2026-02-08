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
                    st.error("לא בדיוק... נסה שוב.")
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.button("התייאשתי, הצג פתרון והמשך"):
            st.info(f"הערכים המאפסים הם: {true_pts_str}")
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            # אסימפטוטה אנכית
            st.subheader("אסימפטוטה אנכית")
            st.write(f"האסימפטוטות האנכיות הן בערכי ה-x שמאפסים את המכנה: x = {true_pts_str}")
            
            # אסימפטוטה אופקית - שאלה פשוטה
            st.subheader("אסימפטוטה אופקית")
            true_horiz = sp.limit(f, x, sp.oo)
            user_horiz = st.text_input("מהי האסימפטוטה האופקית? (y=?)", key="horiz_input")
            
            if user_horiz:
                try:
                    if np.isclose(float(user_horiz), float(true_horiz)):
                        st.success(f"נכון! y = {user_horiz}")
                    else:
                        st.error(f"לא בדיוק. רמז: בדוק את החזקה הגבוהה ביותר.")
                except: pass

            # שרטוט מערכת הצירים עם האסימפטוטות
            fig = go.Figure()
            # אנכיות
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            # אופקית (אם המשתמש צדק או ביקש לראות)
            fig.add_hline(y=float(true_horiz), line_dash="dash", line_color="blue")
            
            # הצלב השחור שלך
            fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
            fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
            fig.update_layout(plot_bgcolor='white', height=500)
            
            st.plotly_chart(fig)

            st.markdown("---")
            st.subheader("השלב הבא: נגזרת")
            if st.checkbox("בדוק את הנגזרת שלך"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי לא תקין.")
