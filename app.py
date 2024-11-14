import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")  # Set layout to wide for side-by-side display

# Container for input on the left side and output on the right side
col1, col2 = st.columns(2)

with col1:
    st.title("Beam SFD and BMD Calculator")

    # Input: Beam length
    beam_length = st.number_input("Enter the beam length (m):", min_value=1.0, value=10.0, step=0.5)

    # Input: Supports
    st.write("### Define Supports")
    supports = []
    support_types = ["Fixed", "Hinge", "Roller"]

    num_supports = st.number_input("Number of supports", min_value=1, max_value=2, value=2)
    for i in range(int(num_supports)):
        support_type = st.selectbox(f"Support {i+1} type:", support_types, key=f"support_type_{i}")
        position = st.number_input(f"Position of Support {i+1} (m from left):", min_value=0.0, max_value=beam_length, key=f"support_pos_{i}")
        supports.append((support_type, position))

    # Input: Point Loads
    st.write("### Define Point Loads")
    num_point_loads = st.number_input("Number of point loads", min_value=0, max_value=5, value=1)
    point_loads = []
    for i in range(int(num_point_loads)):
        magnitude = st.number_input(f"Point Load {i+1} magnitude (kN):", step=1.0, key=f"point_load_mag_{i}")
        position = st.number_input(f"Point Load {i+1} position (m from left):", min_value=0.0, max_value=beam_length, key=f"point_load_pos_{i}")
        point_loads.append((magnitude, position))

    # Input: Distributed Loads
    st.write("### Define Distributed Loads")
    num_distributed_loads = st.number_input("Number of distributed loads", min_value=0, max_value=3, value=1)
    distributed_loads = []
    for i in range(int(num_distributed_loads)):
        magnitude = st.number_input(f"Distributed Load {i+1} magnitude (kN/m):", step=1.0, key=f"dist_load_mag_{i}")
        start_pos = st.number_input(f"Distributed Load {i+1} start position (m from left):", min_value=0.0, max_value=beam_length, key=f"dist_load_start_{i}")
        end_pos = st.number_input(f"Distributed Load {i+1} end position (m from left):", min_value=0.0, max_value=beam_length, key=f"dist_load_end_{i}")
        distributed_loads.append((magnitude, start_pos, end_pos))

    # Input: Moments
    st.write("### Define Moments")
    num_moments = st.number_input("Number of moments", min_value=0, max_value=3, value=1)
    moments = []
    for i in range(int(num_moments)):
        moment_magnitude = st.number_input(f"Moment {i+1} magnitude (kNm):", step=1.0, key=f"moment_mag_{i}")
        position = st.number_input(f"Moment {i+1} position (m from left):", min_value=0.0, max_value=beam_length, key=f"moment_pos_{i}")
        moments.append((moment_magnitude, position))

with col2:
    # Display the beam with supports and loads
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot([0, beam_length], [0, 0], 'k-', lw=5)  # Beam line

    # Plot supports
    for support_type, position in supports:
        if support_type == "Fixed":
            ax.plot(position, 0, 'go', markersize=10, label="Fixed Support")
        elif support_type == "Hinge":
            ax.plot(position, 0, 'bo', markersize=10, label="Hinge Support")
        elif support_type == "Roller":
            ax.plot(position, 0, 'yo', markersize=10, label="Roller Support")

    # Plot point loads
    for magnitude, position in point_loads:
        ax.arrow(position, 0.1, 0, -0.1, head_width=0.2, head_length=0.05, fc='red', ec='red')
        ax.text(position, 0.15, f'{magnitude} kN', color='red', ha='center')

    # Plot distributed loads
    for magnitude, start_pos, end_pos in distributed_loads:
        ax.fill_betweenx([0.1, -0.1], start_pos, end_pos, color='orange', alpha=0.3)
        ax.text((start_pos + end_pos) / 2, 0.15, f'{magnitude} kN/m', color='orange', ha='center')

    # Plot moments
    for moment, position in moments:
        ax.text(position, -0.2, f'{moment} kNm', color='purple', ha='center')
        ax.plot(position, 0, 'purple', marker='o', markersize=10)

    ax.set_xlim(-1, beam_length + 1)
    ax.set_ylim(-1, 1)
    ax.set_title("Beam with Supports and Loads")
    ax.set_xlabel("Position along the beam (m)")
    ax.axis('off')
    ax.legend(loc='upper right')

    # Display the beam plot
    st.pyplot(fig)

    # Calculate and display SFD and BMD
    # Placeholder values for SFD and BMD calculations based on basic principles
    # This part of code should be updated to correctly calculate based on supports and load types

    # Simple example calculation of shear force and bending moment (not accurate for complex cases)
    positions = np.linspace(0, beam_length, 100)

    # Placeholder values: For the sake of example, we assume a linear SFD and parabolic BMD
    sfd_values = np.zeros_like(positions)
    bmd_values = np.zeros_like(positions)

    # Example: Assuming a simple uniformly distributed load case
    # Here, you would insert the correct calculation based on the inputs.
    for i, pos in enumerate(positions):
        # For demonstration: Simplified assumptions
        sfd_values[i] = -10 * pos  # Placeholder for shear force calculation
        bmd_values[i] = -0.5 * pos**2  # Placeholder for bending moment calculation

    # Plotting the SFD
    fig_sfd, ax_sfd = plt.subplots(figsize=(12, 6))
    ax_sfd.plot(positions, sfd_values, '-b', label="Shear Force")
    ax_sfd.set_title("Shear Force Diagram (SFD)")
    ax_sfd.set_xlabel("Position along the beam (m)")
    ax_sfd.set_ylabel("Shear Force (kN)")
    ax_sfd.grid(True)

    # Plotting the BMD
    fig_bmd, ax_bmd = plt.subplots(figsize=(12, 6))
    ax_bmd.plot(positions, bmd_values, '-r', label="Bending Moment")
    ax_bmd.set_title("Bending Moment Diagram (BMD)")
    ax_bmd.set_xlabel("Position along the beam (m)")
    ax_bmd.set_ylabel("Bending Moment (kNm)")
    ax_bmd.grid(True)

    # Displaying the SFD and BMD plots
    st.pyplot(fig_sfd)
    st.pyplot(fig_bmd)
