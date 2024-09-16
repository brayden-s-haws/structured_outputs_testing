import streamlit as st
from book_analysis import (
    get_oai_instructor_book_info,
    get_claude_instructor_book_info,
    get_llama_instructor_book_info,
    get_oai_structured_outputs_book_info
)

def format_book_info(book_info):
    formatted = ""
    for key, value in book_info.dict().items():
        formatted += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
    return formatted

def main():
    st.title("Book Summary Analysis")

    user_book_summary = st.text_area("Enter your book summary:", height=200)

    if st.button("Analyze Summary"):
        if user_book_summary:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.subheader("OpenAI Instructor")
                with st.spinner("Analyzing..."):
                    oai_instructor_book_info, oai_model = get_oai_instructor_book_info(user_book_summary)
                st.markdown(f"**Model:** {oai_model}")
                st.markdown(format_book_info(oai_instructor_book_info))

            with col2:
                st.subheader("Claude Instructor")
                with st.spinner("Analyzing..."):
                    claude_instructor_book_info, claude_model = get_claude_instructor_book_info(user_book_summary)
                st.markdown(f"**Model:** {claude_model}")
                st.markdown(format_book_info(claude_instructor_book_info))

            with col3:
                st.subheader("Llama (Groq) Instructor")
                with st.spinner("Analyzing..."):
                    groq_instructor_book_info, groq_model = get_llama_instructor_book_info(user_book_summary)
                st.markdown(f"**Model:** {groq_model}")
                st.markdown(format_book_info(groq_instructor_book_info))

            with col4:
                st.subheader("OpenAI Native")
                with st.spinner("Analyzing..."):
                    oai_structured_outputs_book_info, oai_structured_model = get_oai_structured_outputs_book_info(user_book_summary)
                st.markdown(f"**Model:** {oai_structured_model}")
                st.markdown(format_book_info(oai_structured_outputs_book_info))
        else:
            st.warning("Please enter a book summary before analyzing.")

if __name__ == "__main__":
    main()