import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

st.set_page_config(layout="wide")  #Set layout to wide for side-by-side display
st.title("Beam SFD and BMD Calculator")

#  Container for input on the left side and output on the right side
col1, col2 = st.columns(2)

with col1:
    # Input: Beam Length
    beam_length = st.number_input('Enter the beam length (m):', min_value=.0, value=10.0, step=0.5) #,min value, default value, step

    # Input: Supports
    st.write('#### Define Supports') # The more the #, the font size will become smaller, and there must be a space after #
    support_types = ["Fixed", "Hinge", "Roller"]
    num_supports = st.number_input('Number of Supports', min_value=1, max_value=2, value=1)
    supports = []
    for i in range(int(num_supports)):
        select_support_type = st.selectbox(f"Support {i+1} type:", support_types, key=f"support_type_{i}") #This key parameter gives each dropdown a unique identifier based on the loop index i
        if select_support_type == "Fixed":
            position = st.selectbox(f'Position of support {i+1} (m from left):', options=[0.0, beam_length], key=f"support_pos_{i}")
        else:
            position = st.number_input(f'Position of support {i+1} (m from left):',min_value=0.0, max_value=beam_length, key=f"support_pos_{i}")
        supports.append((select_support_type, position))
    st.write(supports)

    # Input: Point Loads
    st.write("#### Define Point Loads")
    num_point_loads = st.number_input('Number of point loads', min_value=0, max_value=5, value=0)
    point_loads = []
    for i in range(int(num_point_loads)):
        position = st.number_input(f"Point Load {i+1} position (m from left):", min_value=0.0, max_value=beam_length, key=f"point_load_pos_{i}")
        magnitude = st.number_input(f'Point Load {i+1} magnitude (kN):', step=0.5, key=f"point_load_mag_{i}")
        point_loads.append((position, magnitude))
    st.write(point_loads)

    #Input: Distributed Loads
    st.write("#### Define Distributed loads")
    num_distributed_loads = st.number_input("Number of Distributed Loads", min_value=0, max_value=3, value=0)
    distributed_loads = []
    for i in range(int(num_distributed_loads)):
        start_pos = st.number_input(f"Distributed Load {i+1} starting position (m from left):", min_value=0.0, max_value=beam_length, key=f"dist_load_start_{i}")
        end_pos = st.number_input(f"Distributed Load {i+1} ending position (m from left):", min_value=0.0, max_value=beam_length, key=f"dist_load_end_{i}")
        start_mag = st.number_input(f"Distributed Load {i+1} start magnitude (kN/m):", step=1.0, key=f"dist_load_start_mag_{i}")
        end_mag = st.number_input(f"Distributed Load {i+1} end magnitude (kN/m):", step=1.0, key=f"dist_load_end_mag_{i}")
        distributed_loads.append((start_pos, end_pos, start_mag, end_mag))
    st.write(distributed_loads)

    # Input: Moments
    st.write("#### Define Moments")
    num_moments = st.number_input("Number of Moments:", min_value=0, max_value=3, value=0)
    moments = []
    for i in range(int(num_moments)):
        moment_position = st.number_input(f"Moment {i+1} position (m from left):", min_value=0.0, max_value=beam_length, key=f"moment_pos_{i}")
        moment_magnitude = st.number_input(f"Moment {i+1} magnitude (kNm)", step=1.0, key=f"moment_mag_{i}")
        moments.append((moment_position,moment_magnitude))
    st.write(moments)




with col2:
    # Display the beam with supports, loads and moments
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot([0, beam_length], [0,0], 'b-', lw=20)

    ##Support
    # Load icons for each support type
    fixed_left_icon_path = 'icons/fixed_support_left.png'
    fixed_right_icon_path = 'icons/fixed_support_right.png'
    hinge_icon_path = 'icons/hinge_support.png'
    roller_icon_path = 'icons/roller_support.png'

    # Load the images using the correct path
    hinge_icon = mpimg.imread(hinge_icon_path)
    fixed_icon_left = mpimg.imread(fixed_left_icon_path)
    fixed_icon_right = mpimg.imread(fixed_right_icon_path)
    roller_icon = mpimg.imread(roller_icon_path)

    ax.set_xlim(-.5, beam_length+.5)
    # ax.set_ylim(0, 1)
    ax.get_yaxis().set_visible(False) # Hide y-axis

    for support_type, position in supports:
        if support_type == "Fixed":
            # Use the fixed support icon
            if position == beam_length:
                imagebox = OffsetImage(fixed_icon_right, zoom=0.5)
            else:
                imagebox = OffsetImage(fixed_icon_left, zoom=0.5)
            ab = AnnotationBbox(imagebox, (position, 0), frameon=False)
            ax.add_artist(ab)
        elif support_type == "Hinge":
            # Use the hinge support icon
            imagebox = OffsetImage(hinge_icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (position, -.01), frameon=False)
            ax.add_artist(ab)
        elif support_type == "Roller":
            # Use the roller support icon
            imagebox = OffsetImage(roller_icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (position, -.01), frameon=False)
            ax.add_artist(ab)

    ##Point Load

    st.pyplot(fig)
    plt.show()
