import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 5.6), dpi=150)
ax.set_xlim(0, 12); ax.set_ylim(0, 5.6); ax.axis('off')

C = {'blue': ('#dbe8f7', '#2a6fdb'), 'green': ('#e2f2df', '#3c8d3c'), 'orange': ('#fbe6d4', '#d9822b'),
     'yellow': ('#fdf4cf', '#c9a227'), 'red': ('#f8dcdc', '#c0392b'), 'purple': ('#ece4f5', '#7d4fb0')}

def box(x, y, w, h, text, col, fs=8.6):
    f, e = C[col]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', fc=f, ec=e, lw=1.3))
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fs, wrap=True)
    return (x, y, w, h)

def arrow(p, q, text=None, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=11, color='#444', lw=1.1,
                                 connectionstyle=f'arc3,rad={rad}'))
    if text:
        ax.text((p[0]+q[0])/2, (p[1]+q[1])/2 + 0.12, text, fontsize=7.5, color='#555', ha='center')

ax.text(6, 5.4, 'Workflow of a trustworthy A/B test (and of the simulation in this blog)', ha='center', fontsize=11)

# Lane 1: design
ax.text(0.1, 4.85, 'BEFORE LAUNCH: design (fixed in advance)', fontsize=8.5, color='#2a6fdb', fontweight='bold')
w, h, y1 = 1.95, 0.85, 3.8
b1 = box(0.1, y1, w, h, '1. Hypothesis +\none primary metric\n+ guardrails', 'blue')
b2 = box(2.45, y1, w, h, '2. Baseline rate p₁\n+ MDE (business\nvalue)', 'blue')
b3 = box(4.8, y1, w, h, '3. α, power →\nsample size n\nper arm', 'blue')
b4 = box(7.15, y1, w, h, '4. Duration =\nn ÷ daily traffic\n(round to weeks)', 'blue')
b5 = box(9.5, y1, 2.3, h, '5. Look schedule +\nstopping boundary\n(fixed / Pocock / OBF)', 'green')
for a, b in [(b1, b2), (b2, b3), (b3, b4), (b4, b5)]:
    arrow((a[0]+a[2], y1+h/2), (b[0], y1+h/2))

# Lane 2: run
ax.text(11.8, 2.95, 'DURING THE TEST: monitoring at each planned look k = 1 … K', fontsize=8.5, color='#d9822b', fontweight='bold', ha='right')
y2 = 1.9
c1 = box(0.1, y2, w, h, 'A. Randomize users\n50/50 (check SRM)', 'yellow')
c2 = box(2.45, y2, w, h, 'B. Collect\nconversions\nfor both arms', 'blue')
c3 = box(4.8, y2, w, h, 'C. Two-proportion\nz-test at look k', 'orange')
c4 = box(7.15, y2, w, h, 'D. |z| > boundary[k]?', 'purple')
c5 = box(9.5, y2, 2.3, h, 'E. k = K reached?\n(planned sample\ncollected)', 'purple')
arrow((b5[0]+0.3, y1), (c1[0]+w/2, y2+h))
for a, b in [(c1, c2), (c2, c3), (c3, c4)]:
    arrow((a[0]+a[2], y2+h/2), (b[0], y2+h/2))
arrow((c4[0]+w, y2+h/2), (c5[0], y2+h/2), 'no')
arrow((c5[0]+0.6, y2), (c2[0]+w/2, y2), rad=-0.25)
ax.text(3.3, 1.05, 'no → wait for next look', fontsize=7.5, color='#555')

# Lane 3: decide
y3 = 0.15
d1 = box(4.3, y3, 3.4, 0.8, 'Stop early: declare winner\n(boundary crossed — error rate still ≤ α)', 'green')
d2 = box(8.3, y3, 3.5, 0.8, 'Final analysis: lift + 95% CI vs. MDE,\nguardrails, Holm/Bonferroni if many metrics', 'red')
arrow((c4[0]+0.5, y2), (d1[0]+2.4, y3+0.8), 'yes')
arrow((c5[0]+1.6, y2), (d2[0]+2.4, y3+0.8), 'yes')

plt.savefig('figures/fig0_workflow.png', bbox_inches='tight', facecolor='white')
