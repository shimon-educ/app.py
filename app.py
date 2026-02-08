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
                    st.error("לא בדיוק... הערכים האלו לא מאפסים את המכנה.")
                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות אנכיות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            st.write("מהן משוואות האסימפטוטות האנכיות?")
            user_asymp = st.text_input("הזן את ערכי ה-x (למשל: 3, 1-):", key="asymp_input")
            
            if user_asymp:
                try:
                    user_asy_pts = sorted([float(p.strip()) for p in user_asymp.split(",")])
                    if np.allclose(user_asy_pts, [float(p) for p in true_pts]):
                        st.success(f"נכון מאוד! x = {user_asymp}")
                        show_step_3 = True
                    else:
                        st.error("אלו לא האסימפטוטות.")
                except: pass

        # --- שלב 3: אסימפטוטה אופקית (התוספת החדשה) ---
        show_plot = False
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: אסימפטוטה אופקית")
            st.write("מה קורה לערך ה-y של הפונקציה כאשר x שואף לאינסוף?")
            user_horiz = st.text_input("הזן את משוואת האסימפטוטה האופקית (y=?):", key="horiz_input")
            
            if user_horiz:
                # חישוב האסימפטוטה האמיתית לצורך בדיקה
                true_horiz = sp.limit(f, x, sp.oo)
                try:
                    if np.isclose(float(user_horiz), float(true_horiz)):
                        st.success(f"מצוין! y = {user_horiz}")
                        show_plot = True
                    else:
                        st.error("לא בדיוק. רמז: בדוק את יחס המקדמים של החזקות הגבוהות.")
                except: pass

        # --- הצגת הגרף (המערכת המקורית שלך) ---
        if show_plot:
            st.subheader("מיקום האסימפטוטות על הצירים:")
            fig = go.Figure()
            
            # הוספת אסימפטוטות אנכיות
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red", 
                              annotation_text=f"x={pt}", annotation_position="top")
            
            # הוספת אסימפטוטה אופקית
            h_val = float(sp.limit(f, x, sp.oo))
            fig.add_hline(y=h_val, line_dash="dash", line_color="blue", annotation_text=f"y={h_val}")
            
            # מערכת הצירים המודגשת שלך
            fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', showgrid=True, gridcolor='lightgray', range=[-10, 10])
            fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', showgrid=True, gridcolor='lightgray', range=[-10, 10])
            
            fig.update_layout(plot_bgcolor='white', height=500)
            st.plotly_chart(fig)
            
            st.markdown("---")
            st.subheader("השלב הבא: גזירה")
            if st.checkbox("בדוק את הנגזרת שחישבת במחברת"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
