# The following app will be connected to the pinecone databasea and retrieve information according to important search terms
import streamlit as st
import backend as bk
import numpy as np

# Set config for whole page
st.set_page_config(layout="wide")

# Show streamlit title
st.title("Directorio Inteligente de Startups Latam 🧠⚡")

st.write(
    """
Mediante este buscador, podrás encontrar fácilmente **startups latinoamericanas** que se ajusten a tus necesidades, simplemente describiendo lo que estás buscando.
"""
)

st.write(
    """
Actualmente, el directorio incluye a las startups de **Platzi Startups Latam 2023**. Si deseas agregar tu startup a la base de datos, no dudes en contactarme a través del **Email** 📪 o **Twitter** 💙 que encontrarás al final de la página.
"""
)

st.write("Mira el video de presentación: [link](https://youtu.be/8Yv64dUA7UQ)")


query = st.text_area(
    "Quiero una StarUp que...",
)

if st.button("Buscar"):
    with st.spinner("Wait for it..."):
        df = bk.get_business(query)

        st.write(
            "A continuación encontrarás los 10 resultados más relevantes a tu búsqueda listados en orden de relevacia a tu busqueda:"
        )

        # replace non-finite values with 0 and max integer value
        df = df.replace(
            [np.nan, np.inf, -np.inf],
            [0, np.iinfo(np.int32).max, np.iinfo(np.int32).min],
        )

        float_cols = df.select_dtypes(include=["float"]).columns.tolist()
        df[float_cols] = df[float_cols].astype(int)

    st.dataframe(
        df[
            [
                "name",
                "description",
                "website",
            ]
        ].head(10)
    )


st.write(
    """
   Sigueme en Twitter 💙 [@JLopez_160](https://twitter.com/JLopez_160)
   
   Email 📪: jd.lopez160@gmail.com
"""
)
