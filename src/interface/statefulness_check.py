import streamlit as st

st.header("Counter")

if 'counter1' not in st.session_state:
    st.session_state.counter1 = 0
if 'counter2' not in st.session_state:
    st.session_state.counter2 = 0

col1, col2 = st.columns(2)
with col1:
    button1 = st.button('Increment1')
with col2:
    button2 = st.button('Increment2')

if button1:
    st.session_state.counter1 += 1
    with open("evaluation.txt", "a") as file:
                file.write(f"Counter1: {st.session_state.counter1}\n")
if button2:
    st.session_state.counter2 += 1
    with open("evaluation.txt", "a") as file:
                file.write(f"Counter2: {st.session_state.counter2}\n")

with col1:
    st.write('Counter1 = ', st.session_state.counter1)
with col2:
    st.write('Counter2 = ', st.session_state.counter2)