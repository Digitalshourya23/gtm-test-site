"""Zarthi webinar: audience universe vs. planned reach (two pies)."""
import matplotlib.pyplot as plt

COLORS = {"Meta": "#2A78D6", "Google Demand Gen": "#1BAF7A", "LinkedIn": "#EB6834"}
GREY = "#D5D9DE"

# Targetable universe (mid-point estimates, millions)
universe = {"Meta": 31.5, "Google Demand Gen": 2.0, "LinkedIn": 0.8}

# Planned reach (millions) = budget / CPM x 1000 / frequency 3
#   Meta:     Rs 4.24L  @ Rs 150 CPM  -> ~0.95M
#   Google:   ~Rs 0.90L of Rs 1.51L on Demand Gen @ Rs 120 CPM -> ~0.25M
#   LinkedIn: Rs 1.50L  @ Rs 800 CPM  -> ~0.06M
reach = {"Meta": 0.95, "Google Demand Gen": 0.25, "LinkedIn": 0.06}

total_u = sum(universe.values())
total_r = sum(reach.values())

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), facecolor="#FBFBFB")
fig.suptitle("Zarthi webinar: audience universe and how much we target",
             x=0.03, ha="left", fontsize=18, fontweight="bold")

wedge = dict(edgecolor="white", linewidth=2)

# Pie 1: universe by platform
ax1.pie(universe.values(), colors=[COLORS[k] for k in universe],
        startangle=90, counterclock=False, wedgeprops=wedge)
ax1.set_title(f"Total audience universe: {total_u:.1f}M", fontsize=14,
              fontweight="bold", loc="left")
ax1.legend([f"{k}: {v:.1f}M ({v/total_u:.0%})" for k, v in universe.items()],
           loc="upper center", bbox_to_anchor=(0.5, -0.02), frameon=False, fontsize=12)

# Pie 2: targeted reach vs. untargeted remainder
vals = list(reach.values()) + [total_u - total_r]
ax2.pie(vals, colors=[COLORS[k] for k in reach] + [GREY],
        startangle=90, counterclock=False, wedgeprops=dict(wedge, width=0.38))
ax2.text(0, 0.08, f"{total_r/total_u:.1%}", ha="center", fontsize=28, fontweight="bold")
ax2.text(0, -0.15, f"targeted\n({total_r:.2f}M of {total_u:.1f}M)",
         ha="center", va="top", fontsize=11, color="#555")
ax2.set_title("Share of the universe we target", fontsize=14,
              fontweight="bold", loc="left")
labels = [f"{k}: {reach[k]:.2f}M of {universe[k]:.1f}M ({reach[k]/universe[k]:.1%})"
          for k in reach]
labels.append(f"Not targeted: {total_u - total_r:.1f}M ({1 - total_r/total_u:.1%})")
ax2.legend(labels, loc="upper center", bbox_to_anchor=(0.5, -0.02),
           frameon=False, fontsize=12)

fig.text(0.03, 0.02,
         "Universe sizes are mid-point estimates; people can be on more than one platform. "
         "Planned reach is estimated from budget at assumed CPMs (Meta Rs 150, Google DG Rs 120, "
         "LinkedIn Rs 800) and frequency 3.",
         fontsize=9.5, color="#555")
plt.tight_layout(rect=(0, 0.05, 1, 0.94))
plt.savefig("charts/zarthi_audience_universe.png", dpi=150, facecolor=fig.get_facecolor())
