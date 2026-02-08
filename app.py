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
            st.write("כדי למצוא תחום הגדרה של פונקציית שבר, עלינו למצוא אילו ערכים מאפסים את המכנה ולהוציא אותם מהתחום.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("מעולה! אלו בדיוק הערכים.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... נסה להיעזר ברמזים.")
                    
                    st.markdown("### 💡 עזרה בפתרון:")
                    if st.checkbox("צריך רמז (המשוואה)?"):
                        st.write("פתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.button("הצג פתרון מלא (נוסחת השורשים) והמשך"):
                        st.info("מהלך הפתרון:")
                        try:
                            p = sp.Poly(den, x)
                            coeffs = p.all_coeffs()
                            if len(coeffs) == 3:
                                a, b, c = [float(v) for v in coeffs]
                                delta = b**2 - 4*a*c
                                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                                st.latex(f"x_{{1,2}} = \\frac{{-({format_num(b)}) \\pm \\sqrt{{{format_num(delta)}}}}}{{{2*format_num(a)}}}")
                                if delta >= 0:
                                    st.write(f"הפתרונות הם: {true_pts_str}")
                        except:
                            st.write(f"הפתרונות למשוואה הם: {true_pts_str}")
                        
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2') or show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("💡 איך מוצאים אנכית?"):
                    st.write("אלו נקודות אי-ההגדרה שמצאת קודם:")
                    st.info(f"x = {true_pts_str}")
                    st.write("🔗 [הסבר מפורט על אסימפטוטה אנכית בשברים](https://ischool.co.il/math/analisys/rational-functions/vertical-asymptote/)")
            
            with col2:
                with st.expander("💡 איך מוצאים אופקית?"):
                    st.write("נבדוק את החזקות הגבוהות:")
                    st.info("1. מכנה חזק: y=0\n2. חזקות שוות: יחס מקדמים\n3. מונה חזק: אין")
                    st.write("🔗 [הסבר מפורט על אסימפטוטה אופקית בשברים](https://ischool.co.il/math/analisys/rational-functions/horizontal-asymptote/)")

            if st.button("סרטט גרף אסימפטוטות"):
                fig = go.Figure()
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                h_val = sp.limit(f, x, sp.oo)
                if h_val.is_finite:
                    fig.add_hline(y=float(h_val), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_val)}")
                fig.update_layout(height=400, template="simple_white")
                st.plotly_chart(fig)
    except:
        st.error("טעות בכתיבת הפונקציה.")
