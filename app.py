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
                    st.info("נראה שזו לא התשובה הנכונה. אני ממליץ לך להסתכל ברמזים למטה ולנסות שוב. אם תרצה, תוכל גם ללחוץ על 'התייאשתי' כדי לראות את הדרך.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.info("מהלך הפתרון באמצעות נוסחת השורשים:")
                        try:
                            p = sp.Poly(den, x)
                            coeffs = p.all_coeffs()
                            if len(coeffs) == 3:
                                a, b, c = [format_num(v) for v in coeffs]
                                st.write(f"המקדמים הם: $a={a}, b={b}, c={c}$")
                                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                                delta = b**2 - 4*a*c
                                st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}")
                                st.latex(f"x_{{1,2}} = \\frac{{{-b} \\pm \\sqrt{{{delta}}}}}{{{2*a}}}")
                        except: pass
                        st.success(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            st.subheader("1. אסימפטוטות אנכיות")
            with st.expander("💡 רמז מפורט: איך מוצאים אסימפטוטה אנכית?"):
                st.write("אלו ה'קירות' של הפונקציה. הן נמצאות בערכי ה-x שמאפסים את המכנה.")
                st.info(f"הערכים שמצאת בשלב 1 הם: **{true_pts_str}**")
                st.write("המשוואה צריכה להיראות כך: **x = מספר**.")

            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (x = ?):", key="asymp_input")
            
            st.subheader("2. אסימפטוטה אופקית")
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                st.success("מצוין! בוא נמשיך לחיתוך עם הצירים.")
                show_step_3 = True

        # --- שלב 3: חיתוך עם ציר x ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            st.subheader("חיתוך עם ציר x")

            with st.expander("💡 רמז: איך מוצאים נקודות חיתוך עם ציר x?"):
                st.write("כדי למצוא איפה הפונקציה חוצה את ציר ה-x, אנחנו צריכים לבדוק מתי ה-y הוא אפס ($f(x)=0$).")
                st.write("בפונקציית שבר, זה קורה כשה**מונה** שווה לאפס.")
                st.write("**דוגמה:**")
                st.latex(r"f(x) = \frac{x-4}{x+2} \implies x-4=0 \implies x=4 \implies (4,0)")
                st.info("אם אין ערך שמאפס את המונה (או שהערך מחוץ לתחום ההגדרה), כתוב 'אין'.")

            user_x_intercepts = st.text_input("מהן נקודות החיתוך עם ציר x? (רשום את ערכי ה-x בלבד, מופרדים בפסיק):", key="x_intercept_input")

            # חישוב חיתוך x אמיתי לבדיקה
            x_roots = sp.solve(num, x)
            # סינון נקודות מחוץ לתחום הגדרה
            valid_x_roots = [p for p in x_roots if p not in true_domain]
            true_x_ints = sorted([format_num(p.evalf()) for p in valid_x_roots])

            show_final_step = False
            if user_x_intercepts:
                try:
                    if user_x_intercepts.lower() == "אין":
                        correct_x = (len(true_x_ints) == 0)
                    else:
                        user_val_list = sorted([float(p.strip()) for p in user_x_intercepts.split(",")])
                        correct_x = np.allclose(user_val_list, [float(p) for p in true_x_ints])

                    if correct_x:
                        st.success("כל הכבוד! מצאת את נקודות החיתוך עם ציר x.")
                        show_final_step = True
                    else:
                        st.info("לא, זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט.")
                except:
                    st.warning("נא להזין מספרים תקינים מופרדים בפסיק.")

            if st.button("הצג פיתרון ושרטט"):
                show_final_step = True

            if show_final_step:
                st.write(f"נקודות החיתוך עם ציר x הן: **{', '.join(map(str, true_x_ints)) if true_x_ints else 'אין'}**")
                
                # יצירת גרף עם הנקודות
                fig = go.Figure()
                # הוספת קווי אסימפטוטות
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
                
                # הוספת נקודות החיתוך כנקודות ירוקות על הגרף
                for val in true_x_ints:
                    fig.add_trace(go.Scatter(x=[val], y=[0], mode='markers', marker=dict(color='green', size=12), name=f"חיתוך x: ({val},0)"))

                fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(title="מיקום נקודות החיתוך על הצירים", showlegend=True)
                st.plotly_chart(fig)

                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                if st.checkbox("בדוק את הנגזרת שחישבת"):
                    st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
