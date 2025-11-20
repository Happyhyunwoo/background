import io

import streamlit as st
from rembg import remove
from PIL import Image


# ====== 스타일 정의 (CSS) ======
CUSTOM_CSS = """
<style>
/* 전체 앱 배경과 기본 폭 조정 */
.stApp {
    background: radial-gradient(circle at top left, #f9fafb 0, #e5e7eb 40%, #e0f2fe 100%);
}

.main .block-container {
    max-width: 960px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* 제목 아래 카드 스타일 */
.app-card {
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 18px;
    padding: 1.75rem 1.75rem 1.5rem 1.75rem;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(8px);
}

/* 섹션 제목 스타일 */
.section-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.3rem;
}

/* 설명 텍스트 스타일 */
.helper-text {
    font-size: 0.95rem;
    color: #4b5563;
}

/* 파일 업로더 주변 여백 */
.uploader-wrapper {
    border-radius: 14px;
    border: 1px dashed #cbd5f5;
    background-color: #f9fafb;
    padding: 1.1rem 1rem 1.4rem 1rem;
}

/* 결과 영역 카드 */
.result-card {
    background-color: #f9fafb;
    border-radius: 16px;
    padding: 1rem 1.1rem 0.6rem 1.1rem;
    border: 1px solid #e5e7eb;
}

/* 작은 라벨칩 */
.tag-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.14rem 0.6rem;
    border-radius: 999px;
    background-color: #eef2ff;
    color: #4338ca;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.3rem;
}

/* 푸터 텍스트 */
.footer-text {
    font-size: 0.8rem;
    color: #6b7280;
    margin-top: 1.8rem;
    text-align: center;
}

/* 반응형: 화면이 좁을 때 여백 조절 */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 1rem;
    }
}
</style>
"""

# 상단 일러스트 (SVG)
HERO_SVG = """
<div style="display:flex; justify-content:center; margin-bottom:0.5rem;">
<svg width="220" height="120" viewBox="0 0 420 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="24" y="35" rx="22" ry="22" width="180" height="150" fill="#e5e7eb"/>
  <circle cx="84" cy="88" r="34" fill="#c4b5fd"/>
  <path d="M52 152C60 132 72 120 84 120C96 120 108 132 116 152" stroke="#9ca3af" stroke-width="6" stroke-linecap="round"/>
  <circle cx="148" cy="72" r="10" fill="#f97316"/>
  <rect x="210" y="55" rx="18" ry="18" width="180" height="130" fill="white" stroke="#d1d5db" stroke-width="3"/>
  <rect x="228" y="78" rx="6" ry="6" width="88" height="12" fill="#e5e7eb"/>
  <rect x="228" y="104" rx="6" ry="6" width="136" height="12" fill="#eef2ff"/>
  <rect x="228" y="130" rx="6" ry="6" width="120" height="12" fill="#e0f2fe"/>
  <rect x="228" y="156" rx="6" ry="6" width="92" height="12" fill="#fee2e2"/>
  <circle cx="362" cy="82" r="9" fill="#a5b4fc"/>
  <circle cx="362" cy="108" r="9" fill="#6ee7b7"/>
  <circle cx="362" cy="134" r="9" fill="#fb7185"/>
</svg>
</div>
"""


def remove_background(image: Image.Image) -> Image.Image:
    """
    rembg를 이용해 배경을 제거하는 함수.
    """
    return remove(image)


def main():
    st.set_page_config(
        page_title="Image Background Remover",
        page_icon="🪄",
        layout="centered"
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ====== 사이드바 안내 ======
    with st.sidebar:
        st.markdown("### ✨ 사용 팁")
        st.write(
            "1. 배경과 피사물이 색 대비가 확실한 사진일수록 결과가 깔끔합니다.\n"
            "2. 결과 이미지는 항상 투명 배경의 PNG로 저장됩니다.\n"
            "3. 프레젠테이션, 썸네일, 포트폴리오 등에 바로 사용할 수 있습니다."
        )
        st.markdown("---")
        st.markdown("#### ℹ️ 안내")
        st.write(
            "사진의 복잡도와 해상도에 따라 처리 시간이 늘어날 수 있습니다. "
            "너무 큰 이미지는 업로드 전에 크기를 적당히 줄여 주세요."
        )

    # ====== 헤더 ======
    st.markdown(HERO_SVG, unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:0.3rem;'>"
        "Image Background Remover</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:0.96rem; color:#4b5563;'>"
        "업로드한 이미지에서 배경을 자동으로 제거하고, "
        "투명한 PNG 파일로 바로 다운로드해 보세요."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ====== 메인 카드 ======
    with st.container():
        st.markdown('<div class="app-card">', unsafe_allow_html=True)

        # 태그 라벨
        st.markdown(
            '<span class="tag-pill">AI 기반 배경 제거</span>'
            '<span class="tag-pill">PNG 투명 배경</span>'
            '<span class="tag-pill">Streamlit 앱</span>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">1. 이미지 업로드</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="helper-text">'
            "배경을 제거하고 싶은 이미지를 업로드하세요. "
            "JPG, JPEG, PNG 형식을 지원합니다."
            "</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="uploader-wrapper">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            label="이미지 파일을 여기에 드롭하거나 클릭해서 선택하세요.",
            type=["png", "jpg", "jpeg"],
            label_visibility="visible",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded_file is not None:
            try:
                input_image = Image.open(uploaded_file).convert("RGBA")
            except Exception:
                st.error(
                    "이미지 파일을 불러오는 중 오류가 발생했습니다. "
                    "다른 파일로 다시 시도해 주세요."
                )
                st.markdown("</div>", unsafe_allow_html=True)
                return

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">2. 원본과 결과 비교</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="helper-text">'
                "왼쪽은 원본 이미지, 오른쪽은 배경이 제거된 결과입니다."
                "</p>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.caption("원본 이미지")
                st.image(input_image, use_column_width=True)

            with col2:
                st.caption("배경 제거 결과")
                with st.spinner("배경을 제거하는 중입니다..."):
                    try:
                        output_image = remove_background(input_image)
                    except Exception as e:
                        st.error(
                            "배경 제거 중 오류가 발생했습니다. "
                            "잠시 후 다시 시도하거나, 다른 이미지를 사용해 주세요."
                        )
                        st.text(f"기술적 상세: {e}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        return
                st.image(output_image, use_column_width=True)

            # 결과 다운로드 영역
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">3. 결과 이미지 다운로드</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="helper-text">'
                "배경이 투명한 PNG 형식으로 저장됩니다. "
                "파일명은 자유롭게 변경해 저장해도 괜찮습니다."
                "</p>",
                unsafe_allow_html=True,
            )

            buf = io.BytesIO()
            output_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="💾 배경 제거된 이미지 다운로드 (PNG)",
                data=byte_im,
                file_name="output_no_bg.png",
                mime="image/png",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.info(
                "이미지를 업로드하면 이 영역에 원본과 결과가 나란히 표시됩니다.",
                icon="📷",
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ====== 푸터 ======
    st.markdown(
        '<div class="footer-text">배경 제거 결과가 마음에 들지 않는다면, '
        '배경과 인물의 대비가 더 뚜렷한 사진으로 다시 시도해 보세요.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
