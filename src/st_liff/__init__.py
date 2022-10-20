from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called st-liff,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"st_liff", path=str(frontend_dir)
)

# Create the python function that will be called
def st_liff(
    label: str,
    value: Optional[str] = "",
    key: Optional[str] = None,
):
    """
    Create a Streamlit text input that returns the value whenever a key is pressed.
    """
    component_value = _component_func(
        label=label,
        value=value,
        key=key,
        default=value
    )

    return component_value


def main():
    st.write("## Example123")
    value = st_liff("This is a label!")

    st.write(value)

    st.write("## Example with value")
    value2 = st_liff("With a default value!", value="Default value")

    st.write(value2)


if __name__ == "__main__":
    main()

