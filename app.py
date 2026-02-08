# --- שלב 3: אסימפטוטה אופקית ---
            show_final_plot = False
            
            if show_plot or st.session_state.get('force_plot'):
                st.markdown("---")
                st.header("שלב 3: אסימפטוטה אופקית")
                
                with st.expander("🤔 איך מוצאים אסימפטוטה אופקית?"):
                    st.write("אנחנו בודקים מה קורה לערך ה-y של הפונקציה כאשר x שואף לאינסוף ($x \to \infty$).")
                
                # חישוב אסימפטוטה אופקית אמיתית בעזרת sympy
                horiz_asymp = sp.limit(f, x, sp.oo)
                
                user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (כתוב רק את המספר, למשל: 1):", key="horiz_input")
                
                if user_horiz:
                    try:
                        if np.isclose(float(user_horiz), float(horiz_asymp)):
                            st.success(f"נכון מאוד! האסימפטוטה האופקית היא y = {user_horiz}")
                            show_final_plot = True
                        else:
                            st.error("לא בדיוק. רמז: בדוק את היחס בין המקדמים של החזקה הגבוהה ביותר במונה ובמכנה.")
                    except:
                        st.error("נא להזין מספר תקין.")
                
                if st.button("הצג פתרון ושרטט את המערכת"):
                    st.info(f"האסימפטוטה האופקית היא y = {horiz_asymp}")
                    show_final_plot = True

            # --- שרטוט מערכת הצירים המלאה ---
            if show_final_plot:
                st.subheader("מיקום האסימפטוטות על הצירים:")
                fig = go.Figure()
                
                # אסימפטוטות אנכיות (אדום)
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", 
                                  annotation_text=f"x={pt}", annotation_position="top")
                
                # אסימפטוטה אופקית (כחול)
                fig.add_hline(y=float(horiz_asymp), line_dash="dash", line_color="blue",
                              annotation_text=f"y={horiz_asymp}", annotation_position="right")
                
                # עיצוב צירים מודגשים
                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', showgrid=True, gridcolor='lightgray', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', showgrid=True, gridcolor='lightgray', range=[-10, 10])
                
                fig.update_layout(plot_bgcolor='white', xaxis_title="x", yaxis_title="y", height=500)
                st.plotly_chart(fig)
                
                st.info("מעולה! עכשיו כשיש לנו את ה'שלד', אפשר להמשיך לגזירה.")
                
                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                if st.checkbox("בדוק את הנגזרת שחישבת במחברת"):
                    st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))
