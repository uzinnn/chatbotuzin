import streamlit as st
from openai import OpenAI


st.title("♻️ 재활용 도우미 챗봇")
st.write("분리수거 방법이 헷갈리나요? 챗봇에게 물어보세요!")

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("재활용 도우미를 사용하려면 OpenAI API 키를 입력하세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 재활용 도우미입니다. 무엇을 도와드릴까요?"}
        ]

    # 기존 채팅 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 필드
    if prompt := st.chat_input("예: '페트병은 어떻게 버려야 하나요?'"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답을 스트리밍으로 표시하고 세션 상태에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
