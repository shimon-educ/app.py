import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיצוב מספרים (הסרת .0 ממספרים שלמים)
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

# הזנת פונקציה בתפריט הצד
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת פתרונות נקיים להצגה
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # שלב 1: תחום הגדרה
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        st.write("כדי למצוא את תחום ההגדרה, עלינו למצוא אילו ערכי x מאפסים את המכנה.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    st.session_state['step1_done'] = True
                else:
                    st.error("לא בדיוק... הערכים האלו לא מאפסים את המכנה.")
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        # מנגנון רמזים ופתרון מלא (מופיע רק אם השלב לא הושלם)
        if not st.session_state.get('step1_done'):
            col1, col2, col3 = st.columns(3)
            with col1:
                hint1 = st.checkbox("רמז 1: המשוואה")
            with col2:
                hint2 = st.checkbox("רמז 2: פירוק")
            with col3:
                give_up = st.button("התייאשתי, הצג פתרון")

            if hint1:
                st.info("עליך לפתור את המשוואה:")
                st.latex(sp.latex(den) + "= 0")
            
            if hint2:
                st.info("אפשר לפרק את המכנה לגורמים (טרינום):")
                st.latex(sp.latex(sp.factor(den)) + "= 0")

            if give_up or st.session_state.get('show_full_sol'):
                st.session_state['show_full_sol'] = True
                st.markdown("---")
                st.subheader("💡 פתרון מלא באמצעות נוסחת השורשים")
                
                # חילוץ מקדמים אוטומטי למשוואה ריבועית
                try:
                    p = sp.Poly(den, x)
                    a = format_num(p.coeff_inst(x, 2)) if p.degree() >= 2 else 0
                    b = format_num(p.coeff_inst(x, 1))
                    c = format_num(p.coeff_inst(x, 0))
                    
                    st.write(f"עבור המכנה שלנו, המקדמים הם: $a={a}, b={b}, c={c}$")
                    st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                    
                    disc = b**2 - 4*a*c
                    st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}")
                    st.write(f"הערכים המאפסים הם: **{true_pts_str}**")
                    
                    if st.button("הבנתי, המשך לחקירה"):
                        st.session_state['step1_done'] = True
                        st.rerun()
                except:
                    st.write(f"הערכים המאפסים הם: **{true_pts_str}**")
                    if st.button("הבנתי, המשך"):
                        st.session_state['step1_done'] = True
                        st.rerun()

        # שלב 2: גרף (מופיע לאחר הצלחה או צפייה בפתרון)
        if st.session_state.get('step1_done'):
            st.markdown("---")
            st.header("שלב 2: הצגה גרפית")
            st.write(f"נקודות אי-ההגדרה $x = {true_pts_str}$ הן האסימפטוטות האנכיות.")
            
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='#1f77b4', width=2)))
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            
            st.plotly_chart(fig)
            
            st.subheader("האתגר הבא: גזירה")
            if st.checkbox("בדוק את הנגזרת שחישבת במחברת"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
