#!/usr/bin/env python
###########################################
# Project:    Watch detection             #
# Author:     Alfonso Medela              #
# Contact     alfonso@alfonsomedela.com   #
# Copyright:  alfonsomedela.com           #
# Website:    https://alfonsomedela.com   #
###########################################

import base64
import yaml
import io
from io import BytesIO
from PIL import Image
import streamlit as st
import requests
from requests_toolbelt import MultipartEncoder
import pandas as pd
import numpy as np

def base64str_to_PILImage(base64str):
    base64bytes = base64.decodestring(base64str.encode("utf-8"))
    bytesObj = io.BytesIO(base64bytes)
    return Image.open(bytesObj)

def read_config():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config 

def main(config):
    # logo of sidebar
    svg = """
        <svg width="145" height="73" viewBox="0 0 145 73" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M73.8433 27.722C73.8433 27.7042 73.8433 27.722 73.8433 27.722C73.7998 27.7093 73.8305 27.7093 73.8433 27.722ZM99.8513 17.548C100.576 18.0788 101.636 17.8832 102.233 17.1137C102.837 16.3238 102.75 15.2597 102.038 14.7035C101.336 14.1854 100.276 14.386 99.6541 15.186C99.078 15.9403 99.1625 17.007 99.8513 17.548Z" fill="#363636"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M16.3842 39.8712C16.3842 39.8712 23.3926 38.8934 28.1502 34.2305C28.1502 34.2305 29.1053 32.5314 29.5124 31.9117C37.4477 19.5967 45.4086 20.9682 45.4086 20.9682C49.0958 21.2297 48.8602 23.9091 48.8602 23.9091C48.8013 24.6456 49.1521 24.4882 49.1521 24.4882L50.563 21.9815L54.2093 22.1263L46.6248 35.9168C46.6248 35.9168 44.3459 39.5613 46.4789 40.2064C46.4789 40.2064 50.5477 41.0699 59.0181 31.0482L64.7078 22.2228H68.1594L67.3324 23.7187C67.1275 24.2139 67.5756 24.0564 67.5756 24.0564C67.5756 24.0564 71.309 21.7758 73.4573 22.1771C73.4573 22.1771 75.7285 22.3218 75.4494 24.9733C75.4034 26.1796 74.881 26.7993 74.671 26.9492C74.671 26.9492 77.8334 26.1745 82.9827 20.4907L87.4074 13.5954H91.0537L86.1937 21.3567H90.5185L90.2292 21.984H85.8045L76.8603 36.1607C76.8603 36.1607 74.9322 39.1575 77.3443 39.6324C77.3443 39.6324 79.9177 40.1835 82.4015 38.2838C82.4015 38.2838 90.0141 32.0108 93.1944 27.6273L96.4028 22.2761H99.8058L91.7348 36.8362C91.7348 36.8362 90.2138 39.9423 93.1457 40.0667C93.1457 40.0667 96.9482 40.4426 102.141 32.9302C102.141 32.9302 107.58 22.9263 115.361 21.3567C115.361 21.3567 121.189 20.1021 120.659 24.925C120.659 24.925 120.05 33.0343 106.369 33.6514C106.369 33.6514 103.782 39.1854 108.166 39.6781C108.166 39.6781 114.842 41.4458 128.63 26.6114L131.209 22.4666H135.242L132.617 26.9492C132.576 27.3784 133.006 27.0457 133.006 27.0457C139.039 21.2755 141.902 22.4666 141.902 22.4666C143.889 23.198 143.459 25.0215 143.459 25.0215C143.533 25.1891 143.344 27.3098 141.853 27.3834C140.939 27.3936 140.191 26.5657 140.199 25.6006C140.194 24.605 140.942 23.8101 141.853 23.8177C142.148 23.8072 142.438 23.8919 142.68 24.059H142.729C142.729 24.059 142.076 22.2786 139.229 23.3834C139.229 23.3834 134.269 25.6691 130.187 31.1447L124.403 41.0293H120.027L127.076 29.2654C115.392 42.9366 105.493 41.367 105.493 41.367C99.9825 40.7575 101.506 35.0508 101.506 35.0508C94.9816 43.4572 89.6428 40.8845 89.6428 40.8845C86.186 39.2718 88.3804 35.7264 88.3804 35.7264L90.9564 31.3886C84.2041 38.8934 80.7012 40.2597 80.7012 40.2597C76.8399 42.0782 73.7979 40.3562 73.7979 40.3562C71.058 38.7283 73.7979 34.9568 73.7979 34.9568L81.4796 22.8552C76.3294 28.2144 74.0583 27.7656 73.8529 27.725L73.8465 27.7238C72.853 27.706 71.9261 26.8323 71.903 25.7453C71.9261 24.6736 72.7275 23.7999 73.7006 23.8177C73.9891 23.8035 74.2758 23.8704 74.5276 24.0107C74.3458 22.5301 72.7762 22.8044 72.7762 22.8044C68.4001 23.7466 65.6808 26.7104 65.6808 26.7104L57.9017 40.8362H53.8175L57.6584 34.0375C57.6584 34.0375 51.3082 41.5702 46.3816 41.075C46.3816 41.075 41.4345 41.1918 42.3947 36.6864C42.3947 36.6864 36.0522 41.8216 31.6018 40.9302C31.6018 40.9302 26.9569 40.5239 27.9556 35.6273C23.3618 39.7162 16.5327 40.7854 16.5327 40.7854C5.31222 43.2007 3.79635 34.2279 3.79635 34.2279C1.43036 20.8539 14.1027 9.30077 14.1027 9.30077C29.5329 -4.59394 39.8162 2.83977 39.8162 2.83977C41.2655 4.19851 45.1653 2.35976 45.1653 2.35976L39.9135 9.78585C39.9135 9.78585 41.012 3.44168 36.8536 2.11849C36.8536 2.11849 24.7241 -0.992642 15.7569 11.1344C15.7569 11.1344 6.73847 21.984 8.02389 33.8927C8.02389 33.8927 8.76902 41.0115 16.3842 39.8712ZM116.865 21.7884C116.865 21.7884 112.387 21.3541 107.434 31.7211C107.434 31.7211 106.95 32.4678 107.778 32.5897C107.778 32.5897 115.554 32.2164 118.081 25.4532C118.081 25.4532 119.159 22.2354 116.865 21.7884ZM32.1837 34.9034C32.1837 34.9034 30.7984 38.9974 33.2054 39.485C33.2054 39.485 37.6352 40.6939 43.901 33.7935L47.0607 28.4906C47.0607 28.4906 49.5983 24.3687 47.45 22.5604C47.45 22.5604 44.915 20.6023 40.3033 24.6811C40.3033 24.6811 34.5343 29.2018 32.1837 34.9034Z" fill="#363636"/>
            <path d="M6.08398 59.1973C7.15039 59.1973 8.07324 59.4001 8.85254 59.8057C9.63184 60.2113 10.2266 60.7809 10.6367 61.5146C11.0514 62.2484 11.2588 63.0983 11.2588 64.0645C11.2588 65.0443 11.0537 65.9079 10.6436 66.6553C10.2334 67.3981 9.64323 67.9746 8.87305 68.3848C8.10742 68.7949 7.20508 69 6.16602 69H1.40137V59.1973H6.08398ZM5.83105 67.4893C6.58757 67.4893 7.23698 67.3548 7.7793 67.0859C8.32161 66.8125 8.73405 66.4183 9.0166 65.9033C9.30371 65.3883 9.44727 64.7754 9.44727 64.0645C9.44727 62.9525 9.13965 62.1162 8.52441 61.5557C7.91374 60.9951 7.01595 60.7148 5.83105 60.7148H3.11035V67.4893H5.83105ZM13.46 59.1973H21.916V60.7148H15.1689V62.8408H19.1201V64.3516H15.1689V67.4893H21.916V69H13.46V59.1973ZM24.3564 59.1973H27.0225L29.9619 64.4814H29.9893L32.8877 59.1973H35.5537V69H33.8447V60.9199H33.8174L31.1445 65.6709H28.8066L26.0928 60.9199H26.0654V69H24.3564V59.1973ZM43.1006 69.1367C42.1253 69.1367 41.2298 68.9225 40.4141 68.4941C39.5983 68.0658 38.9512 67.4688 38.4727 66.7031C37.9941 65.9329 37.7549 65.0648 37.7549 64.0986C37.7549 63.1325 37.9941 62.2666 38.4727 61.501C38.9512 60.7308 39.5983 60.1315 40.4141 59.7031C41.2298 59.2747 42.1253 59.0605 43.1006 59.0605C44.0804 59.0605 44.9759 59.2747 45.7871 59.7031C46.5983 60.1315 47.2386 60.7285 47.708 61.4941C48.182 62.2598 48.4189 63.1279 48.4189 64.0986C48.4189 65.0648 48.182 65.9329 47.708 66.7031C47.2386 67.4688 46.5983 68.0658 45.7871 68.4941C44.9759 68.9225 44.0804 69.1367 43.1006 69.1367ZM43.1006 67.5303C43.7477 67.5303 44.3379 67.3867 44.8711 67.0996C45.4089 66.8079 45.8327 66.4023 46.1426 65.8828C46.457 65.3587 46.6143 64.764 46.6143 64.0986C46.6143 63.4333 46.4593 62.8408 46.1494 62.3213C45.8395 61.8018 45.418 61.3962 44.8848 61.1045C44.3516 60.8128 43.7568 60.667 43.1006 60.667C42.4398 60.667 41.8405 60.8128 41.3027 61.1045C40.765 61.3962 40.3411 61.8018 40.0312 62.3213C39.7214 62.8408 39.5664 63.4333 39.5664 64.0986C39.5664 64.7686 39.7236 65.3633 40.0381 65.8828C40.3525 66.4023 40.7786 66.8079 41.3164 67.0996C41.8542 67.3867 42.4489 67.5303 43.1006 67.5303ZM60.792 59.1973C61.4118 59.1973 61.9632 59.3249 62.4463 59.5801C62.9294 59.8353 63.3053 60.1862 63.5742 60.6328C63.8431 61.0794 63.9775 61.5785 63.9775 62.1299C63.9775 62.6995 63.8431 63.21 63.5742 63.6611C63.3099 64.1077 62.9362 64.4587 62.4531 64.7139C61.9701 64.9691 61.4163 65.0967 60.792 65.0967H56.6084V69H54.8994V59.1973H60.792ZM60.6348 63.5791C61.1543 63.5791 61.5553 63.4538 61.8379 63.2031C62.1204 62.9479 62.2617 62.5902 62.2617 62.1299C62.2617 61.6742 62.1204 61.3255 61.8379 61.084C61.5553 60.8379 61.1543 60.7148 60.6348 60.7148H56.6084V63.5791H60.6348ZM66.0283 59.1973H67.7373V67.4893H73.8213V69H66.0283V59.1973ZM84.1436 69L83.125 66.0537H77.8271L76.8223 69H75.0312L78.4902 59.1973H82.4346L85.8936 69H84.1436ZM78.3467 64.543H82.5986L81.2725 60.7148H79.6523L78.3467 64.543ZM90.043 60.7148H85.8662V59.1973H95.9287V60.7148H91.752V69H90.043V60.7148ZM97.8018 59.1973H106.292V60.7148H99.5107V62.8477H103.441V64.3516H99.5107V69H97.8018V59.1973ZM112.267 69.1367C111.291 69.1367 110.396 68.9225 109.58 68.4941C108.764 68.0658 108.117 67.4688 107.639 66.7031C107.16 65.9329 106.921 65.0648 106.921 64.0986C106.921 63.1325 107.16 62.2666 107.639 61.501C108.117 60.7308 108.764 60.1315 109.58 59.7031C110.396 59.2747 111.291 59.0605 112.267 59.0605C113.246 59.0605 114.142 59.2747 114.953 59.7031C115.764 60.1315 116.405 60.7285 116.874 61.4941C117.348 62.2598 117.585 63.1279 117.585 64.0986C117.585 65.0648 117.348 65.9329 116.874 66.7031C116.405 67.4688 115.764 68.0658 114.953 68.4941C114.142 68.9225 113.246 69.1367 112.267 69.1367ZM112.267 67.5303C112.914 67.5303 113.504 67.3867 114.037 67.0996C114.575 66.8079 114.999 66.4023 115.309 65.8828C115.623 65.3587 115.78 64.764 115.78 64.0986C115.78 63.4333 115.625 62.8408 115.315 62.3213C115.006 61.8018 114.584 61.3962 114.051 61.1045C113.518 60.8128 112.923 60.667 112.267 60.667C111.606 60.667 111.007 60.8128 110.469 61.1045C109.931 61.3962 109.507 61.8018 109.197 62.3213C108.887 62.8408 108.732 63.4333 108.732 64.0986C108.732 64.7686 108.89 65.3633 109.204 65.8828C109.519 66.4023 109.945 66.8079 110.482 67.0996C111.02 67.3867 111.615 67.5303 112.267 67.5303ZM129.131 62.0205C129.131 62.5492 129.003 63.0277 128.748 63.4561C128.493 63.8799 128.137 64.2171 127.682 64.4678C127.226 64.7184 126.706 64.8506 126.123 64.8643L129.021 69H126.978L124.236 64.8643H121.495V69H119.786V59.1973H126.014C126.615 59.1973 127.153 59.3203 127.627 59.5664C128.101 59.8125 128.47 60.1497 128.734 60.5781C128.999 61.0065 129.131 61.4873 129.131 62.0205ZM121.495 63.3535H125.856C126.344 63.3535 126.727 63.2373 127.005 63.0049C127.283 62.7679 127.422 62.4398 127.422 62.0205C127.422 61.5921 127.283 61.2686 127.005 61.0498C126.731 60.8265 126.349 60.7148 125.856 60.7148H121.495V63.3535ZM131.585 59.1973H134.251L137.19 64.4814H137.218L140.116 59.1973H142.782V69H141.073V60.9199H141.046L138.373 65.6709H136.035L133.321 60.9199H133.294V69H131.585V59.1973Z" fill="#363636"/>
        </svg>
    """
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" style="margin:auto; padding: 3rem; display:block;"/>' % b64
    st.sidebar.markdown(html, unsafe_allow_html=True)

    # dropdown menu for selecting methods
    detection_type = st.sidebar.selectbox(
        "Select method",
        ("/detect/text",
         "/detect/screw",
         "/detect/jewels",
         "/detect/incabloc",
         "/detect/notches",
         "/detect/all_screws",
         "/detect/all_screws_exp",
         "/detect/axis_system",
         "/detect/watch_model",
         "/detect/watch_rolex_caseback",
         "/authenticate/watch",
         "/cartier-tool")
    )
    
    # drag and drop for uploading the images
    uploaded_files = st.sidebar.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # apply custom css for analyze button
    st.sidebar.markdown(
                   """
                   <style>
                    .stButton {
                        text-align: center;
                    }
                    </style>
                   """, unsafe_allow_html=True
               )

    if st.sidebar.button("Analyze Data"):
        if len(uploaded_files) != 0:
            cols = st.columns(len(uploaded_files), gap="large")

            # apply custom css for width of columns
            if len(uploaded_files) > 1:
               st.markdown(
                   """
                   <style>
                    .main .block-container {
                        max-width: 100% !important;
                        padding-left: 3rem !important;
                        padding-right: 3rem !important;
                    }
                    </style>
                   """, unsafe_allow_html=True
               )

            idx = 0
            while idx < len(uploaded_files):
                with cols[idx]:
                    # changed code for sorting table
                    key_idx = 0
                    st.image(uploaded_files[idx])
                    # mp_encoder = MultipartEncoder(
                    #     fields={"file": (uploaded_files[idx].name, uploaded_files[idx], uploaded_files[idx].type)}
                    # )
                    # url = f"http://{config['url']}:{config['port']}{detection_type}"
                    # response = requests.post(
                    #     url, data=mp_encoder, headers={"Content-Type": mp_encoder.content_type}
                    # )
                    # json_results = response.json()
                    # try:
                    #     image = base64str_to_PILImage(json_results["image"])
                    #     st.image(image, caption="Detections Visualization")
                    #     if detection_type == '/detect/all_screws':
                    #         image_eb = base64str_to_PILImage(json_results["image_em"])
                    #         st.image(image_eb, caption="Detections Visualization")
                    # except:
                    #     pass
                    
                    if detection_type == "/cartier-tool":
                        # Brand
                        brand = "Cartier"
                        col1, col2= st.columns([0.2, 0.8])
                        col1.markdown("Brand:")
                        col2.markdown(brand)

                        # Model
                        model = "Ballon Bleu"
                        col1, col2 = st.columns([0.2, 0.8])
                        col1.markdown("Model:")
                        col2.markdown(model)

                        # Model Number
                        model_num = "4377"
                        col1, col2 = st.columns([0.2, 0.8])
                        col1.markdown("Model Number:")
                        col2.markdown(model_num)

                        # Serial Number
                        serial_num = "47108BX"
                        col1, col2 = st.columns([0.2, 0.8])
                        col1.markdown("Serial Number:")
                        col2.markdown(serial_num)

                        # Axis 
                        axis = "Founded"
                        col1, col2 = st.columns([0.2, 0.8])
                        col1.markdown("Axis:")
                        col2.markdown(axis)

                        # Authentication
                        col1, col2 = st.columns([0.2, 0.8])
                        col1.markdown("Authentication:")
                        col2.markdown("Filename 1 and Filename 2 are same watch")

                        # Texts
                        st.text("Texts:")
                        text_result = ["Cartier", "Automatic", "Stainless Steel"]
                        text_table = pd.DataFrame(data = {"Text": text_result})
                        # changed code for sorting table
                        st.data_editor(text_table, use_container_width=True, key=f'{uploaded_files[idx].file_id}_text_{str(key_idx + 1)}') 

                        # Screws
                        st.text("Screws:")
                        screw_angle = ["30", "40", "65"]
                        screw_number = ["S0", "S2", "S1"]
                        screw_table = pd.DataFrame(data = {"Angle": screw_angle, "Screw Number": screw_number})
                        # changed code for sorting table
                        st.data_editor(screw_table, use_container_width=True, key=f'{uploaded_files[idx].file_id}_screw_{str(key_idx + 1)}')

                    else:
                        st.text("Result")            
                        # st.json(json_results)
                idx += 1
    

def login(config):
    st.set_page_config(page_title="Watches project")

    if "auth_status" not in st.session_state:
        st.session_state['auth_status'] = None

    if st.session_state['auth_status'] is None:
        login_form = st.empty()
        with login_form.form("Login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            st.markdown(
                    """
                    <style>
                        .stButton {
                            text-align: center;
                        }
                        .stButton>Button {
                            width: 25%
                        }
                        </style>
                    """, unsafe_allow_html=True
                )
            submit = st.form_submit_button("Login")

            if submit:
                if email == config['credentials']['usernames']['demo']['email'] and password == config['credentials']['usernames']['demo']['password']:
                    login_form.empty()
                    st.session_state['auth_status'] = True
                    main(config)
                else:
                    st.warning("Email or password are incorrect.")
    else:
        main(config)


if __name__ == "__main__":
    login(read_config())

