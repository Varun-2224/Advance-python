import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Different shades of blue
blue_shades = [
    "#E3F2FD",  # Very Light Blue
    "#BBDEFB",
    "#90CAF9",
    "#64B5F6",
    "#42A5F5",
    "#2196F3",
    "#1E88E5",
    "#1976D2",
    "#1565C0",
    "#0D47A1"   # Dark Blue
]

fig, ax = plt.subplots(figsize=(8, 5))

# Draw rectangles for each shade
for i, shade in enumerate(blue_shades):
    ax.add_patch(
        patches.Rectangle((0, i), 5, 1, facecolor=shade)
    )
    ax.text(5.2, i + 0.5, shade, va='center', fontsize=10)

# Set ;plot limits
ax.set_xlim(0, 8)
ax.set_ylim(0, len(blue_shades))
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Different Shades of Blue")

plt.show()