import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

st.set_page_config(layout="wide")  #Set layout to wide for side-by-side display
st.title("Beam SFD and BMD Calculator")

#  Container for input on the left side and output on the right side
col1, col2 = st.columns([2, 3])

with col1:
    # Input: Beam Length
    beam_length = st.number_input('Enter the beam length (m):', min_value=1.0, value=10.0, step=1.0) #,min value, default value, step

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
        start_mag = st.number_input(f"Distributed Load {i+1} start magnitude (kN/m):", step=0.5, key=f"dist_load_start_mag_{i}")
        end_mag = st.number_input(f"Distributed Load {i+1} end magnitude (kN/m):", step=0.5, key=f"dist_load_end_mag_{i}")
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


######## CALCULATION
## Reactions
def calculate_reactions(supports, point_loads, distributed_loads, moments, beam_length):
    num_supports = len(supports)
    if num_supports == 1:
        for support_type, position in supports:
            if support_type == "Fixed":
                sum_point_loads = 0
                sum_dist_loads = 0
                sum_point_loads_moments = 0
                sum_dist_loads_moments = 0
                sum_external_moments = 0

                for position, magnitude in point_loads:
                    sum_point_loads += magnitude
                    sum_point_loads_moments += magnitude*(position)
                for start_pos, end_pos, start_mag, end_mag in distributed_loads:
                    sum_dist_loads += 0.5 * (start_mag + end_mag) * (abs(end_pos-start_pos))
                    centroid_left = ((abs(end_pos-start_pos))/3) * ((2*end_mag+start_mag)/(end_mag+start_mag))
                    distance_left = min(start_pos, end_pos)
                    sum_dist_loads_moments += 0.5 * (start_mag + end_mag) * (abs(end_pos-start_pos)) * (centroid_left+distance_left)
                for position, magnitude in moments:
                    sum_external_moments += magnitude

                reaction_1 = -sum_point_loads - sum_dist_loads
                moment_1 = sum_point_loads_moments +sum_dist_loads_moments -sum_external_moments
                return sum_point_loads, sum_dist_loads, reaction_1, sum_point_loads_moments, sum_dist_loads_moments, sum_external_moments, moment_1
            else:
                return False
    elif num_supports == 2:
        if any(support_type == "Fixed" for support_type, position in supports):
            return False
        else:
            sum_point_loads = 0
            sum_dist_loads = 0
            sum_point_loads_moments = 0
            sum_dist_loads_moments = 0
            sum_external_moments = 0

            for position, magnitude in 
            return "Can Solve"
    else:
        return False



with col2:
    st.write('Upward Load +ve & Clockwise Moment +ve')

    # Display the beam with supports, loads and moments
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot([0, beam_length], [0,0], 'b-', lw=20)

    ax.set_xlim(-beam_length * 0.1, beam_length * 1.1)
    ax.set_ylim(-1, 1)
    ax.get_yaxis().set_visible(False) # Hide y-axis

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
            ab = AnnotationBbox(imagebox, (position, -.14), frameon=False)
            ax.add_artist(ab)
        elif support_type == "Roller":
            # Use the roller support icon
            imagebox = OffsetImage(roller_icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (position, -.14), frameon=False)
            ax.add_artist(ab)

    ##Point Load
    max_magnitude = max((abs(mag) for _, mag in point_loads), default=0) # Find the maximum magnitude
    # st.write(max_magnitude)
    # Loop through point loads to draw arrows with adjusted positions and directions
    for position, magnitude in point_loads:
        if max_magnitude == 0:
            continue
        # Calculate arrow length based on magnitude, scaled to fit within the y-limits
        direction = 1 if magnitude > 0 else (-1 if magnitude < 0 else 0)  # Downward if positive, upward if negative

        if direction == 0:
            continue

        # Determine the starting y-coordinate based on load direction and beam thickness
        start_y = -.22 * direction if magnitude > 0 else -.22 * direction

        # Draw the arrow with the adjusted y-coordinate and length based on the load's sign and magnitude
        ax.arrow(
            position,              # x-coordinate of arrow's starting point
            start_y,               # y-coordinate of arrow's starting point
            0,                     # No horizontal movement, vertical arrow
            direction * .01,  # Adjust length by direction and scaled magnitude
            head_width=0.2,        # Width of the arrow head
            head_length=0.1,       # Length of the arrow head
            fc='red',              # Fill color of arrow
            ec='red'               # Edge color of arrow
        )
        # Calculate the line length proportionally based on the max magnitude
        line_length = direction * max(0.3, (abs(magnitude) / max_magnitude) * 0.8)
        # st.write(line_length)

        # Draw the red line from the arrowhead
        ax.plot([position, position], [start_y, -line_length], 'r-', lw=1.5)
        
        point_loads_text = -line_length - 0.10 if magnitude > 0 else -line_length + 0.05
        ax.text(position, point_loads_text, f'{abs(magnitude)} kN', color='red', ha='center')



    ## Distributed Load
    max_dist_magnitude = max((abs(mag) for _, _, mag1, mag2 in distributed_loads for mag in [mag1, mag2]), default=0)
    # st.write(max_dist_magnitude)

    for start_pos, end_pos, start_mag, end_mag in distributed_loads:
        if max_dist_magnitude == 0:
            continue

        # Calculate directions based on magnitude signs
        start_direction = 1 if start_mag > 0 else (-1 if start_mag < 0 else 0)
        end_direction = 1 if end_mag > 0 else (-1 if end_mag < 0 else 0)

        # Determine starting y-coordinates
        start_y = -0.22 * start_direction if start_direction != 0 else 0
        end_y = -0.22 * end_direction if end_direction != 0 else 0

        # Calculate line lengths proportionally based on max magnitude
        start_line_length = start_direction * max(0.3, (abs(start_mag) / max_dist_magnitude) * 0.8) if start_direction != 0 else 0
        end_line_length = end_direction * max(0.3, (abs(end_mag) / max_dist_magnitude) * 0.8) if end_direction != 0 else 0

        # Draw arrows at the start and end positions if direction is non-zero
        if start_direction != 0:
            ax.arrow(
                start_pos,
                start_y,
                0,
                start_direction * 0.01,
                head_width=0.2,
                head_length=0.1,
                fc='green',
                ec='green'
            )
        if end_direction != 0:
            ax.arrow(
                end_pos,
                end_y,
                0,
                end_direction * 0.01,
                head_width=0.2,
                head_length=0.1,
                fc='green',
                ec='green'
            )

        # Draw the green lines from the arrowheads or connect the fill directly to y=0
        ax.plot([start_pos, start_pos], [start_y, -start_line_length], 'g-', lw=1.5)
        ax.plot([end_pos, end_pos], [end_y, -end_line_length], 'g-', lw=1.5)

        # Connect the ends of the arrows and fill the area between
        x_coords = [start_pos, start_pos, end_pos, end_pos]
        y_coords = [-start_line_length if start_direction != 0 else 0, 0, 0, -end_line_length if end_direction != 0 else 0]
        ax.fill(x_coords, y_coords, color='green', alpha=0.3)

        # Label distributed load magnitudes at the start and end positions if direction is non-zero
        if start_direction != 0:
            start_pos_text = -start_line_length - 0.10 if start_mag > 0 else -start_line_length + 0.03
            ax.text(
                start_pos,
                start_pos_text,
                f'{abs(start_mag)} kN/m',
                color='green',
                ha='center'
            )
        if end_direction != 0:
            end_pos_text = -end_line_length - 0.10 if end_mag > 0 else -end_line_length + 0.03
            ax.text(
                end_pos,
                end_pos_text,
                f'{abs(end_mag)} kN/m',
                color='green',
                ha='center'
            )

    ## Moment
    clockwise_moment_icon_path = 'icons/moment_clockwise.png'
    anticlockwise_moment_icon_path = 'icons/moment_anticlockwise.png'

    clockwise_moment_icon = mpimg.imread(clockwise_moment_icon_path)
    anticlockwise_moment_icon = mpimg.imread(anticlockwise_moment_icon_path)

    for moment_position, moment_magnitude in moments:
        if moment_magnitude > 0:
            imagebox = OffsetImage(clockwise_moment_icon, zoom=0.13)
            ab = AnnotationBbox(imagebox, (moment_position, 0.0), frameon=False)
            ax.add_artist(ab)

            ax.text(moment_position, 0.3, f'{abs(moment_magnitude)} kNm', color='black', ha='center')

        elif moment_magnitude < 0:
            imagebox = OffsetImage(anticlockwise_moment_icon, zoom=0.13)
            ab = AnnotationBbox(imagebox, (moment_position, 0), frameon=False)
            ax.add_artist(ab)

            ax.text(moment_position, 0.3, f'{abs(moment_magnitude)} kNm', color='black', ha='center')

    st.pyplot(fig)
    plt.show()



    ## RESULTS
    reactions= calculate_reactions(supports, point_loads, distributed_loads, moments, beam_length)
    if reactions == False:
        st.warning("Can't Solve")
    else:
        st.write(f"Reaction at support A: {reactions[2]} kN")
        st.write(f"Moment at support A: {reactions[6]} kNm")
        st.write(reactions)





    