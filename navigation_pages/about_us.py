import streamlit as st

col1, col2 = st.columns([2,1], vertical_alignment='center', gap='large')

with col1:
    st.header("What is InvoiceGPT?")

    st.write("""
        InvoiceGPT is an innovative application designed to revolutionize invoice management through artificial intelligence. 
        Developed as a B.Tech Computer Science project at SRM IST, Chennai, it showcases the practical application of 
        cutting-edge AI in solving real-world business challenges.
        """)

    st.subheader("Key Features")

    st.write("""
        InvoiceGPT leverages GPT-4 Vision for advanced OCR, allowing users to upload and process any invoice format. 
        Our AI automatically extracts and interprets key invoice data, storing it securely in Amazon S3 and a MySQL 
        database on AWS RDS.

        With robust data isolation and Google Authentication, we ensure the highest level of data security and privacy. 
        Users can interact with their invoice data using natural language queries, powered by LangChain and GPT-4, 
        making data retrieval intuitive and effortless.
        """)

    st.subheader("How It Works")

    st.write("""
        1. Upload your invoice through our user-friendly Streamlit interface.
        2. Our AI processes the document, extracting and interpreting key information.
        3. Data is securely stored with strict isolation measures.
        4. Access your data anytime using natural language queries via our chatbot interface.

        InvoiceGPT streamlines financial document management, saving time and reducing errors. Experience the future 
        of invoice processing today!
        """)

with col2:
    st.image("images/invoicegpt_icon.png")

st.divider()

col3, col4 = st.columns([1,2], vertical_alignment='center', gap='large')

with col3:
    st.image("images/yv.png")

with col4:
    st.header("About the Developer")

    st.write("""
    Hi! I'm Yohan Vinu, a final-year Computer Science undergraduate at SRM Institute of 
    Science and Technology, with a passion for AI and its applications. I previously worked as a research intern 
    at Samsung R&D, where I collaborated on a computer vision research project and was given
    an award of excellence for our work. Currently, I am an AI engineer intern at Moative, 
    an AI startup, where I focus on building applied AI and LLM-based SaaS products.

    With this experience under my belt, I have developed a strong interest in multimodal 
    (vision + language) applications and LLM-based research. Some of the other projects 
    I've worked on include an eye-blink-to-Morse-code decoder framework using computer vision, 
    as well as a company and people profiling lookup tool, served as a REST API and 
    built with AI agents and retrieval-augmented generation (RAG) pipelines.

    I was also fortunate to be appointed as the IoT lead at Networking Nexus SRM, a 
    student club, where I had the privilege of serving as the main speaker for a 2-day 
    hands-on workshop on microcontrollers and embedded systems, attended by over 150 
    freshmen and sophomores. Additionally, my role as class representative for the past 
    three years has helped me hone my leadership and communication skills. 
    Outside of academics, I'm passionate about fingerstyle guitar, tennis, table tennis, 
    and chess. I'm also a dog enthusiast and a proud owner of a Rottweiler!
    """)
    st.markdown("""
    <p>
    <a href="https://www.linkedin.com/in/yohanvinu/" target="_blank"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" /></a>
    <a href="https://github.com/YohanV1/" target="_blank"><img src="https://img.shields.io/badge/GitHub-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white" /></a>
    <a href="mailto:yohanvvinu@gmail.com"><img alt="Gmail" src="https://img.shields.io/badge/Gmail-white?style=for-the-badge&logo=gmail"></a>
    </p>
    """, unsafe_allow_html=True)

st.subheader("Contribute")
st.write("You can contribute to the project by visiting the [GitHub repository](https://github.com/YohanV1/InvoiceGPT/tree/main).")

st.subheader("License")
st.write("""
InvoiceGPT is licensed under the MIT License, making it open for contribution and modification.
Feel free to improve, modify, or distribute the software as per the license terms.
""")



