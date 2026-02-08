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
        if abs(n_float) < 1e-10: return 0
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
        
        # חישוב פתרונות אמיתיים לצורך בדיקה
        true_domain_pts = sp.solve(den, x)
        # חיתוך עם X (רק בתחום ההגדרה)
        x_roots = [p for p in sp.solve(num, x) if p not in true_domain_pts]
        true_x_intercepts = sorted([format_num(p.evalf()) for p in x_roots])
        # חיתוך עם Y (אם 0 בתחום)
        true_y_intercept = None
        if 0 not in true_domain_pts:
            true_y_intercept = format_num(f.subs(x, 0).evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="d_in")
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_domain_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.info("נראה שזו לא התשובה הנכונה. כדאי להסתכל ברמזים למעלה או לנסות שוב.")
            except: st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'): show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            user_asymp = st.text_input("אסימפטוטות אנכיות (x=?):", key="a_in")
            user_horiz = st.text_input("אסימפטוטה אופקית (y=?):", key="h_in")
            if user_asymp and user_horiz:
                st.success("המשך לשלב הבא!")
                show_step_3 = True

        # --- שלב 3: נקודות חיתוך עם הצירים ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            # חיתוך עם ציר Y
            st.subheader("1. חיתוך עם ציר y")
            with st.expander("💡 רמז: איך מוצאים חיתוך עם ציר y?"):
                st.write("כדי למצוא איפה הפונקציה פוגשת את ציר $y$, עלינו להציב $x=0$ במשוואה.")
                st.write("**דוגמה:**")
                st.latex(r"f(x) = \frac{x+6}{x-2} \implies f(0) = \frac{0+6}{0-2} = -3 \implies (0, -3)")
                st.warning("שים לב: אם $x=0$ לא בתחום ההגדרה, אין חיתוך עם ציר $y$!")
            
            user_y_int = st.text_input("מהי נקודת החיתוך עם ציר y? (הזן את ערך ה-y בלבד, או כתוב 'אין'):", key="y_int_in")

            # חיתוך עם ציר X
            st.subheader("2. חיתוך עם ציר x")
            with st.expander("💡 רמז: איך מוצאים חיתוך עם ציר x?"):
                st.write("כדי למצוא איפה הפונקציה פוגשת את ציר $x$, עלינו להשוות את הפונקציה לאפס ($y=0$).")
                st.write("בפונקציה רציונלית (שבר), מספיק לבדוק מתי **המונה שווה לאפס**.")
                st.write("**דוגמה:**")
                st.latex(r"f(x) = \frac{x-5}{x+2} \implies x-5=0 \implies x=5 \implies (5, 0)")
            
            user_x_ints = st.text_input("מהן נקודות החיתוך עם ציר x? (הזן ערכי x מופרדים בפסיק, או 'אין'):", key="x_int_in")

            show_final_plot = False
            if user_y_int and user_x_ints:
                try:
                    # בדיקת Y
                    if user_y_int.lower() == "אין":
                        correct_y = (true_y_intercept is None)
                    else:
                        correct_y = np.isclose(float(user_y_int), float(true_y_intercept))
                    
                    # בדיקת X
                    if user_x_ints.lower() == "אין":
                        correct_x = (len(true_x_intercepts) == 0)
                    else:
                        user_x_val = sorted([float(p.strip()) for p in user_x_ints.split(",")])
                        correct_x = np.allclose(user_x_val, [float(p) for p in true_x_intercepts])

                    if correct_x and correct_y:
                        st.success("מצוין! מצאת את כל נקודות החיתוך.")
                        show_final_plot = True
                    else:
                        st.info("לא זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט")
                except:
                    st.warning("ודא שהזנת מספרים תקינים.")

            if st.button("הצג פיתרון ושרטט את הנקודות"):
                show_final_plot = True

            if show_final_plot:
                st.subheader("סיכום ויזואלי של הנקודות:")
                fig = go.Figure()
                
                # שרטוט הפונקציה
                x_vals = np.linspace(-10, 10, 400)
                f_num = sp.lambdify(x, f, "numpy")
                y_vals = f_num(x_vals)
                # ניקוי ערכים באסימפטוטות כדי שהגרף לא יקפוץ
                y_vals[np.abs(y_vals) > 20] = np.nan
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="הפונקציה", line=dict(color='black', width=2)))

                # הוספת נקודות חיתוך X
                for val in true_x_intercepts:
                    fig.add_trace(go.Scatter(x=[val], y=[0], mode='markers+text', 
                                             marker=dict(color='green', size=12),
                                             text=[f"({val},0)"], textposition="bottom center", name="חיתוך X"))
                
                # הוספת נקודת חיתוך Y
                if true_y_intercept is not None:
                    fig.add_trace(go.Scatter(x=[0], y=[true_y_intercept], mode='markers+text', 
                                             marker=dict(color='orange', size=12),
                                             text=[f"(0,{true_y_intercept})"], textposition="middle right", name="חיתוך Y"))

                fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', range=[-10, 10])
                fig.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig)

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")
