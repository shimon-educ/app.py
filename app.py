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
            במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.
            **השלבים:** משווים את המכנה לאפס ומפתור את המשוואה.
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
                    
                    # --- רמזים ופתרון מפורט ---
                    st.markdown("### 💡 עזרה בפתרון המכנה:")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק לגורמים?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון מפורט והמשך"):
                        st.info("מהלך הפתרון באמצעות נוסחת השורשים:")
                        
                        # חישוב אוטומטי של מקדמי המשוואה הריבועית
                        try:
                            p = sp.Poly(den, x)
                            coeffs = p.all_coeffs()
                            if len(coeffs) == 3:
                                a, b, c = [float(v) for v in coeffs]
                                delta = b**2 - 4*a*c
                                
                                st.write(f"המקדמים הם: $a={format_num(a)}, b={format_num(b)}, c={format_num(c)}$")
                                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                                st.latex(f"x_{{1,2}} = \\frac{{-({format_num(b)}) \\pm \\sqrt{{{format_num(b)}^2 - 4 \\cdot {format_num(a)} \\cdot {format_num(c)}}}}}{{2 \\cdot {format_num(a)}}}")
                                st.write(f"הדיסקרימיננטה ($\Delta$) היא: {format_num(delta)}")
                                
                                if delta >= 0:
                                    x1 = (-b + np.sqrt(delta)) / (2*a)
                                    x2 = (-b - np.sqrt(delta)) / (2*a)
                                    st.success(f"השורשים הם: {format_num(x1)}, {format_num(x2)}")
                            else:
                                st.write("פתרון המשוואה:")
                                st.latex(sp.latex(sp.solve(den, x)))
                        except:
                            st.write("לא ניתן להציג נוסחת שורשים למשוואה זו, אך הפתרונות הם:")
                        
                        st.success(f"תחום ההגדרה הוא כל x פרט ל: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2') or show_step_2:
            # --- שלב 2: אסימפטוטות ---
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            user_asymp = st.text_input("1. מהן משוואות האסימפטוטות האנכיות?", key="asymp_input")
            user_horiz = st.text_input("2. מהי משוואת האסימפטוטה האופקית?", key="horiz_input")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("💡 איך מוצאים אנכית?"):
                    st.write("אלו נקודות אי-ההגדרה שמצאת: " + f"**{true_pts_str}**")
                    st.write("🔗 [הסבר נוסף](https://www.m-math.co.il/differential-calculus/function-investigation/vertical-asymptote/)")
            with col2:
                with st.expander("💡 איך מוצאים אופקית?"):
                    st.write("משווים חזקות גבוהות במונה ובמכנה.")
                    st.write("🔗 [הסבר נוסף](https://www.m-math.co.il/differential-calculus/function-investigation/horizontal-asymptote/)")

            if st.button("סרטט אסימפטוטות"):
                fig = go.Figure()
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
                h_val = sp.limit(f, x, sp.oo)
                if h_val.is_finite:
                    fig.add_hline(y=float(h_val), line_dash="dash", line_color="blue")
                fig.update_layout(height=400, template="simple_white")
                st.plotly_chart(fig)

    except Exception as e:
        st.error("ביטוי לא תקין.")

if st.sidebar.button("התחל מחדש"):
    st.session_state.clear()
    st.rerun()
