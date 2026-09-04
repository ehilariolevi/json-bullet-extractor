import streamlit as st
import pandas as pd
import json
from io import BytesIO

# ======================================================
# PAGE SETTINGS
# ======================================================

st.set_page_config(
    page_title="Levi JSON Bullet Extractor",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Levi JSON Bullet Extractor")

st.write(
    "Upload an Excel file containing Shopify Rich Text JSON and extract Bullet_1 to Bullet_8 plus Model_Info."
)

# ======================================================
# BULLET EXTRACTION FUNCTION
# ======================================================

def extract_bullets(json_string):

    bullets = []

    try:

        if pd.isna(json_string):
            return [""] * 9

        data = json.loads(str(json_string))

        def find_list_items(node):

            if isinstance(node, dict):

                if node.get("type") == "list-item":

                    text_parts = []

                    def collect_text(child):

                        if isinstance(child, dict):

                            if child.get("type") == "text":
                                text_parts.append(
                                    child.get("value", "")
                                )

                            for c in child.get(
                                "children", []
                            ):
                                collect_text(c)

                    for child in node.get(
                        "children", []
                    ):
                        collect_text(child)

                    bullets.append(
                        "".join(text_parts).strip()
                    )

                for child in node.get(
                    "children", []
                ):
                    find_list_items(child)

            elif isinstance(node, list):

                for item in node:
                    find_list_items(item)

        find_list_items(data)

    except Exception:
        return [""] * 9

    if not bullets:
        return [""] * 9

    model_info = ""

    last_bullet = bullets[-1].strip()

    if last_bullet.lower().startswith("model"):

        model_info = last_bullet

        remaining = bullets[:-1]

    else:

        remaining = bullets

    remaining = remaining[:8]

    while len(remaining) < 8:
        remaining.append("")

    return remaining + [model_info]

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    try:

        df = pd.read_excel(
            uploaded_file,
            dtype={
                "PC-9": str,
                "PC9": str,
                "ID": str
            }
        )

        st.success("File loaded successfully!")

        st.write(
            f"Rows found: {len(df)}"
        )

        required_columns = [
            "PC-9",
            "PC9",
            "ID",
            "Handle",
            "fit_description"
        ]

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:

            st.error(
                "Missing required column(s): "
                + ", ".join(missing)
            )

        else:

            st.success(
                "All required columns found."
            )

            if st.button("Extract Bullets"):

                output_columns = [
                    "Bullet_1",
                    "Bullet_2",
                    "Bullet_3",
                    "Bullet_4",
                    "Bullet_5",
                    "Bullet_6",
                    "Bullet_7",
                    "Bullet_8",
                    "Model_Info"
                ]

                df[output_columns] = df[
                    "fit_description"
                ].apply(
                    lambda x: pd.Series(
                        extract_bullets(x)
                    )
                )

                output_df = df[
                    [
                        "PC-9",
                        "PC9",
                        "ID",
                        "Handle"
                    ] + output_columns
                ]

                output = BytesIO()

                with pd.ExcelWriter(
                    output,
                    engine="openpyxl"
                ) as writer:

                    output_df.to_excel(
                        writer,
                        index=False
                    )

                output.seek(0)

                st.success(
                    "Extraction complete!"
                )

                st.write(
                    f"Rows Processed: {len(df)}"
                )

                st.download_button(
                    label="Download Output File",
                    data=output,
                    file_name="output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:

        st.error(str(e))