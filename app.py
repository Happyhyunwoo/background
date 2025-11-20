import io

import streamlit as st
from rembg import remove
from PIL import Image, ImageOps  # ImageOps 추가


def main():
    st.set_page_config(
        page_title="Image Background Remover",
        page_icon="🪄",
        layout="centered"
    )

    st.title("🪄 Image Background Remover")
    st.write(
        "이미지를 업로드하면 배경과 전경을 자동으로 분리해 줍니다. "
        "원하는 모드를 선택해서 사용해 보세요."
    )

    mode = st.radio(
        "처리 방식 선택",
        ("배경 제거 (사람만 남기기)", "배경만 남기기")
    )

    uploaded_file = st.file_uploader(
        "이미지를 업로드하세요 (PNG / JPG / JPEG)",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file).convert("RGBA")
        st.subheader("원본 이미지")
        st.image(input_image, use_column_width=True)

        with st.spinner("이미지 처리 중입니다..."):
            if mode == "배경 제거 (사람만 남기기)":
                # 기존처럼 배경 제거 → 사람/물체만 남기기
                output_image = remove(input_image)

            else:  # "배경만 남기기"
                # 전경(사람/물체) 마스크만 얻기 (흰색=전경, 검은색=배경)
                mask = remove(input_image, only_mask=True).convert("L")
                # 마스크를 반전해서 전경만 투명하게 만들기
                inv_mask = ImageOps.invert(mask)

                # 원본 이미지에 반전 마스크를 알파 채널로 입히기
                bg_only = input_image.copy()
                bg_only.putalpha(inv_mask)
                output_image = bg_only

        st.subheader("처리 결과")
        st.image(output_image, use_column_width=True)

        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        if mode == "배경 제거 (사람만 남기기)":
            filename = "foreground_only.png"
            label = "사람/물체만 남긴 이미지 다운로드 (PNG)"
        else:
            filename = "background_only.png"
            label = "배경만 남긴 이미지 다운로드 (PNG)"

        st.download_button(
            label=label,
            data=byte_im,
            file_name=filename,
            mime="image/png"
        )

        if mode == "배경 제거 (사람만 남기기)":
            st.info("배경은 투명 처리되고, 사람/물체만 남은 PNG 파일입니다.")
        else:
            st.info("사람/물체 영역은 투명 처리되고, 배경만 남은 PNG 파일입니다.")


if __name__ == "__main__":
    main()
