import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Web Scraper", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            margin-top: 28px;  /* Add your desired margin here */
        }
        .stForm {
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        .stImage {
            margin-bottom: 10px;
        }
        .st-emotion-cache-7ym5gk ef3psqc7 {
            margin-top: 27px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>Web Scraper</h1>", unsafe_allow_html=True)

# Form for keyword input
with st.form("search"):
    col1, col2, col3, col4 = st.columns(4)
    keyword = col2.text_input("Enter your keyword")
    search = col3.form_submit_button("search")

    if search:
        if keyword:
            # Process the keyword for URL
            keywordwords = keyword.replace(' ', '-') if len(keyword.split(' ')) > 1 else keyword

            # Fetch the webpage
            page = requests.get(f"https://unsplash.com/s/photos/{keywordwords}")
            if page.status_code == 200:
                # Parse the content with BeautifulSoup
                soup = BeautifulSoup(page.content, 'html.parser')

                # Select all img tags within the div with class 'HcSeS'
                imgs = soup.select('div.HcSeS img')
                data = []

                for img in imgs:
                    srcset = img.get('srcset')
                    if isinstance(srcset, str): 
                        if '?' in srcset:  
                            myindex = srcset.index('?')
                            myimage = srcset[:myindex]
                            data.append({'srcset': srcset, 'myindex': myindex, 'myimage': myimage})

                if data:
                    df = pd.DataFrame(data)
                    cols = st.columns(3) 
                    for index, row in df.iterrows():
                        col = cols[index % 3]
                        col.markdown(
                            f"""
                            <a href="{row['myimage']}" target="_blank">
                                <img src="{row['myimage']}" width="100%">
                            </a>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No images found.")
            else:
                st.error("Failed to retrieve content from Unsplash.")
        else:
            st.error("Please enter a keyword to search.")
