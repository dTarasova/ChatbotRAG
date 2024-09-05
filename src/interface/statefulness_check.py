import streamlit as st

st.header("Counter")

if 'counter' not in st.session_state:
    st.session_state.counter = 0

button = st.button('Increment')

if button:
    st.session_state.counter += 1
    with open("test_buttons.txt", "a") as file:
                file.write(f"Counter: {st.session_state.counter}\n")


st.write('Counter = ', st.session_state.counter)