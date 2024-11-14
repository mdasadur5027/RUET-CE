import streamlit as st
import matplotlib.pyplot as plt

st.title("Shear Force Diagram (SFD) and Bending Moment Diagram (BMD)")

# Position values
a = [i for i in range(15)]
v = []  # Shear force values
m = []  # Bending moment values

# Calculate values for the first segment
for i in range(7):
    V = 2 * i
    M = -i * i
    v.append(V)
    m.append(M)

# Calculate values for the second segment
for i in range(7, 15):
    V = 2 * i + 5
    M = -i * i - 30
    v.append(V)
    m.append(M)

# Display calculated values
st.write("Shear Force Values:", v)
st.write("Bending Moment Values:", m)

# Plotting the SFD and BMD
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))

ax1.plot(a, v, '-b', marker='o')
ax1.set_title('SFD')
ax1.set_xlabel('Position')
ax1.set_ylabel('Shear Force')
ax1.grid(True)

ax2.plot(a, m, '-r', marker='o')
ax2.set_title('BMD')
ax2.set_xlabel('Position')
ax2.set_ylabel('Bending Moment')
ax2.grid(True)

st.pyplot(fig)
