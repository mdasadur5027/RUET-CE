import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title
st.title("Beam SFD and BMD Calculator")

# Input: Beam length
beam_length = st.number_input("Enter the beam length (m):", min_value=1.0, value=10.0, step=0.5)

# Input: Point load
st.write("Define point loads (magnitude and position along the beam)")
num_loads = st.number_input("Number of point loads", min_value=0, max_value=5, value=2)

loads = []
for i in range(int(num_loads)):
    magnitude = st.number_input(f"Load {i+1} magnitude (kN):", step=1.0)
    position = st.number_input(f"Load {i+1} position (m from left):", min_value=0.0, max_value=beam_length)
    loads.append((magnitude, position))

# Calculate reactions for a simply supported beam (assuming supports at x=0 and x=beam_length)
A_y = sum([load[0] * (beam_length - load[1]) for load in loads]) / beam_length
B_y = sum([load[0] for load in loads]) - A_y

# Shear Force and Bending Moment calculations
positions = np.linspace(0, beam_length, 1000)  # 1000 points along the beam
shear_force = np.zeros_like(positions)
bending_moment = np.zeros_like(positions)

for i, x in enumerate(positions):
    V = A_y
    M = 0
    for load, pos in loads:
        if x >= pos:
            V -= load
            M -= load * (x - pos)
    shear_force[i] = V
    bending_moment[i] = A_y * x - sum(load * max(0, x - pos) for load, pos in loads)

# Plotting the beam with supports and loads
fig, ax = plt.subplots(figsize=(10, 2))
ax.plot([0, beam_length], [0, 0], 'k-', lw=5)  # Beam line

# Plot supports
ax.plot(0, 0, 'go', markersize=10, label="Support A")  # Left support
ax.plot(beam_length, 0, 'go', markersize=10, label="Support B")  # Right support

# Plot loads
for magnitude, position in loads:
    ax.arrow(position, 0.1, 0, -0.1, head_width=0.2, head_length=0.05, fc='red', ec='red')
    ax.text(position, 0.15, f'{magnitude} kN', color='red', ha='center')

ax.set_xlim(-1, beam_length + 1)
ax.set_ylim(-1, 1)
ax.set_title("Beam with Supports and Loads")
ax.set_xlabel("Position along the beam (m)")
ax.axis('off')
ax.legend(loc='upper right')

# Display the beam plot
st.pyplot(fig)

# Plotting SFD and BMD
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle("Shear Force and Bending Moment Diagrams")

# Plot SFD
ax1.plot(positions, shear_force, 'b', label="Shear Force")
ax1.set_title("Shear Force Diagram (SFD)")
ax1.set_xlabel("Position along the beam (m)")
ax1.set_ylabel("Shear Force (kN)")
ax1.grid(True)
ax1.legend()

# Plot BMD
ax2.plot(positions, bending_moment, 'r', label="Bending Moment")
ax2.set_title("Bending Moment Diagram (BMD)")
ax2.set_xlabel("Position along the beam (m)")
ax2.set_ylabel("Bending Moment (kNm)")
ax2.grid(True)
ax2.legend()

# Display the SFD and BMD plots
st.pyplot(fig)

# Display calculated reactions
st.write(f"Reaction at A (left support): {A_y:.2f} kN")
st.write(f"Reaction at B (right support): {B_y:.2f} kN")
