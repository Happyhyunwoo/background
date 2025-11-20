import io

import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
import cv2


def remove_bg_keep_foreground(input_image: Image.Image) -> Image.Image:
    """기존 방식: 배경을 투명하게 만들고 피사체만 남기는 함수"""
    # rembg가 PIL 이미지를 직접 받을 수 있음
    output_image = remove(input_image)
    return output_image


def remove_foreground_keep_background(input_image: Image.Image) -> Image.Image:
    """
    전경(사람/물체)을 제거하고, 그 자리를 주변 배경으로 자동 채우는 함수.
    1) rembg로 전경 마스크 생성
    2) 해당 영역을 OpenCV inpaint로 배경 채우기
    """
    # inpaint는 RGB 이미지가 필요하므로 RGBA -> RGB 변환
    rgb_image = input_image.convert("RGB")
    img_np = np.array(rgb_image)

    # OpenCV는 BGR을 쓰므로 변환
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # 전경 마스크 생성 (피사체가 있는 부분이 흰색인 마스크)
    mask_pil = remove(rgb_image, only_mask=True)
    mask_gray = np.array(mask_pil.convert("L"))

    # 이진 마스크로 변환 (0/255)
    _, mask_bin = cv2.threshold(
        mask_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # 가장자리 아티팩트를 줄이기 위해 살짝 팽창
    kernel = np.ones((3, 3), np.uint8)
    mask_dilated = cv2.dilate(mask_bin, kernel, iterations=1)

    # inpaint: 마스크가 255인 영역을 주변 배경으로 채움
    inpainted_bgr = cv2.inpaint(
        img_bgr,
        mask_dilated,
        inpaintRadius=3,
        flags=cv2.INPAINT_TELEA,
    )

    # 다시 RGB, PIL 이미지로 변환
    inpainted_rgb = cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(inpainted_rgb)

    return result_image


def main():
    st.set_page_config(
        page_title="Background Tool",
        page_icon="🪄",
        layout="centered",
    )

    st.title("🪄 Background Tool")

    st.write(
        "이미지를 업로드한 뒤, 아래 두 가지 모드 중 하나를 선택할 수 있습니다.\n"
        "1) 배경 제거: 피사체만 남기고 배경을 투명하게 만들기\n"
        "2) 피사체 제거: 사람/물체를 지우고, 그 자리를 자동으로 배경으로 채우기"
    )

    mode = st.radio(
        "사용할 기능을 선택하세요.",
        (
            "배경 제거 (피사체만 남기기)",
            "피사체 제거 (배경만 남기기 + 자동 채우기)",
        ),
    )

    uploaded_file = st.file_uploader(
        "이미지를 업로드하세요 (PNG / JPG / JPEG)",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file).convert("RGBA")

        st.subheader("원본 이미지")
        st.image(input_image, use_column_width=True)

        if mode == "배경 제거 (피사체만 남기기)":
            with st.spinner("배경을 제거하는 중입니다..."):
                result_image = remove_bg_keep_foreground(input_image)

            st.subheader("배경 제거 결과 (투명 배경, 피사체만 남김)")
            st.image(result_image, use_column_width=True)

            buf = io.BytesIO()
            result_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="배경 제거 이미지 다운로드 (PNG)",
                data=byte_im,
                file_name="foreground_only.png",
                mime="image/png",
            )

        else:
            with st.spinner("피사체를 제거하고 배경을 채우는 중입니다..."):
                result_image = remove_foreground_keep_background(input_image)

            st.subheader("피사체 제거 결과 (배경만 남김 + 자동 채우기)")
            st.image(result_image, use_column_width=True)

            buf = io.BytesIO()
            result_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="배경만 남긴 이미지 다운로드 (PNG)",
                data=byte_im,
                file_name="background_filled.png",
                mime="image/png",
            )

        st.info(
            "피사체 제거 모드는 주변 배경 정보를 이용해서 자동으로 채우기 때문에, "
            "배경이 단색이거나 패턴이 단순할수록 더 자연스럽게 보입니다."
        )


if __name__ == "__main__":
    main()
