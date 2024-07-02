import time
import streamlit as st
import replicate

st.markdown('# :rainbow[AI Генератор картинок]')

REPLICATE_API_TOKEN = st.secrets['REPLICATE_API_TOKEN']


def configure_sidebar():
    with st.sidebar:
        with st.form('my_form'):
            width = st.number_input('Ширина картинки', min_value=256, max_value=2048, value=1024, step=16)
            height = st.number_input('Высота картинки', min_value=256, max_value=2048, value=1024, step=16)
            prompt = st.text_area('Введите текст:')
            submitted = st.form_submit_button('Отправить', type='primary')

        return {
            'width': width,
            'height': height,
            'prompt': prompt,
            'submitted': submitted,
        }


def main_page(
        width: int,
        height: int,
        prompt: str,
        submitted: bool,
):
    if submitted:
        with st.spinner('В процессе...'):
            result = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    'prompt': prompt,
                    'width': width,
                    'height': height,
                },
            )
            images = result[0]
            with st.container():
                st.image(images, caption='Ваше изображение')


def main():
    data = configure_sidebar()
    main_page(**data)


if __name__ == '__main__':
    main()
