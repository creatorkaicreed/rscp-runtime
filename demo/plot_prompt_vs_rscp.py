import matplotlib.pyplot as plt

# Real benchmark data
vault = [100, 1000, 10000]
naive_chars = [1270, 12790, 128890]
rscp_chars = [381, 383, 383]

plt.figure(figsize=(8, 5.2))

# Plot lines
plt.plot(
    vault,
    naive_chars,
    marker="o",
    markersize=8,
    linewidth=3,
    label="Naive Prompt Context",
)

plt.plot(
    vault,
    rscp_chars,
    marker="s",
    markersize=8,
    linewidth=3,
    label="RSCP Bounded Reasoning",
)

# Log scale on X axis
plt.xscale("log")

# Titles and labels
plt.title("Prompt Explosion vs RSCP Bounded Reasoning", fontsize=16)
plt.xlabel("Stored Knowledge / Vault Size (cards)", fontsize=12)
plt.ylabel("Active Reasoning Size (chars)", fontsize=12)

# Grid
plt.grid(True, linestyle="--", alpha=0.4)

# Legend
plt.legend()

# Annotate the big naive curve
plt.annotate(
    "Prompt Explosion",
    xy=(10000, 128890),
    xytext=(1600, 90000),
    arrowprops=dict(arrowstyle="->", lw=1.5),
    fontsize=12,
)

# Annotate the bounded RSCP line
plt.annotate(
    "Bounded Reasoning",
    xy=(1000, 383),
    xytext=(150, 5000),
    arrowprops=dict(arrowstyle="->", lw=1.5),
    fontsize=12,
)

# Add labels to RSCP values
for x, y in zip(vault, rscp_chars):
    plt.text(x, y + 250, f"{y}", ha="center", fontsize=9)

# Make layout tight
plt.tight_layout()

# Save publication-quality outputs
plt.savefig("prompt_vs_rscp.png", dpi=300, bbox_inches="tight")
plt.savefig("prompt_vs_rscp.pdf", bbox_inches="tight")

# Show figure
plt.show()