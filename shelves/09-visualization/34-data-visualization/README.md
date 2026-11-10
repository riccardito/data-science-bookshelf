# 34 · Data Visualization

*Shelf IX · Data Visualization & Communication · FHNW modules: gdv, ivi*

## Why It Matters

Visualization makes the invisible visible. The best analysis is useless if nobody can see the insight. Data visualization is the bridge between "the data says X" and "the decision-maker understands X."

> "A data scientist is a cave explorer. You only have a flashlight."
> — Prof. Dr. Daniel Perruchoud

The flashlight IS visualization. It's how you illuminate what's in the cave.

## Key Concepts

### Principles (Tufte, Few, Bertin)
- **Data-ink ratio**: maximize data, minimize decoration
- **Lie factor**: visual representation must match the data
- **Chartjunk**: avoid unnecessary visual elements
- **Pre-attentive processing**: color, size, position, orientation — what the eye sees first
- **Gestalt principles**: proximity, similarity, closure, continuity
- **Small multiples**: same chart, different subsets — enables comparison

### Chart Selection

| Data Relationship | Chart Type |
|---|---|
| Distribution (1 variable) | Histogram, density plot, box plot, violin plot |
| Comparison (categories) | Bar chart, grouped bar, lollipop chart |
| Trend over time | Line chart, area chart |
| Correlation (2 variables) | Scatter plot, hexbin plot |
| Composition (parts of whole) | Stacked bar, pie (rarely), treemap |
| Ranking | Horizontal bar chart, slope chart |
| Geospatial | Choropleth, point map, heatmap |
| High-dimensional | Parallel coordinates, radar chart, PCA projection |

### Color
- Sequential: light → dark for ordered data
- Diverging: two hues meeting at a neutral midpoint (e.g., red-white-blue)
- Categorical: distinct hues for unrelated categories
- Colorblind-safe palettes: viridis, cividis, ColorBrewer
- Never use rainbow (perceptually non-uniform)

### Interactive Visualization
- Zoom, pan, filter, details-on-demand
- Linked views: selection in one chart highlights in another
- Tooltips: show exact values on hover
- Animation: use sparingly, only when time dimension matters

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `matplotlib` | The foundation — low-level, full control |
| `seaborn` | Statistical visualization on top of matplotlib |
| `altair` | Declarative visualization (Vega-Lite) |
| `bokeh` | Interactive web-ready charts |
| `d3.js` | JavaScript — the ultimate flexibility (low-level) |
| `Chart.js` | Simple JS charts for dashboards |

## Storytelling with Data (→ see [36-storytelling.md](36-storytelling.md))

A chart without context is noise. The sequence:
1. **Context**: What's the question?
2. **Data**: What does the data show?
3. **Narrative**: What does it mean?
4. **Action**: What should we do?

"50 kilos of coffee through grinders every day" is more vivid than "high daily throughput." Specificity beats abstraction — in data viz too.

## Chapters

Read in order: each chapter builds on the one before it.

1. Perception
2. Choosing a chart
3. Matplotlib
4. Plotly
5. Colour and accessibility

## Challenge

**redesign**: three published charts redrawn, before and after · how many lookups a reader needs, before and after

## Where it was learned

FHNW `gdv`
