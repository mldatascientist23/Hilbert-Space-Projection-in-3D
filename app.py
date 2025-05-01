import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy.spatial import ConvexHull

st.set_page_config(layout="wide", page_title="Hilbert Space 3D Explorer")
st.title("🚀 Interactive Hilbert Space Projection in 3D")

# Base vectors
origin = np.array([0, 0, 0])
axes = {
    'M': (np.array([1, 0, 0]), 'Motivation & Alternatives', 'red'),
    'R': (np.array([0, 1, 0]), 'Resource Endowment', 'green'),
    'I': (np.array([0, 0, 1]), 'Innovation & Growth', 'blue'),
}

# Points and centroids
n1, n2 = np.array([0.2, 0.3, 0.1]), np.array([0.4, 0.2, 0.2])
o1, o2 = np.array([0.7, 0.8, 0.6]), np.array([0.6, 0.7, 0.5])
mu_N = np.mean([n1, n2], axis=0)
mu_O = np.mean([o1, o2], axis=0)
delta = mu_O - mu_N

n_points = [n1, n2]
o_points = [o1, o2]

fig = go.Figure()

# Axes
for key, (vec, label, color) in axes.items():
    fig.add_trace(go.Cone(
        x=[0], y=[0], z=[0], u=[vec[0]], v=[vec[1]], w=[vec[2]],
        sizemode="scaled", sizeref=0.5, anchor="tail",
        colorscale=[[0, color], [1, color]], showscale=False, name=f'Axis {key}'
    ))
    fig.add_trace(go.Scatter3d(
        x=[vec[0] * 1.1], y=[vec[1] * 1.1], z=[vec[2] * 1.1],
        mode='text', text=[f'{label} ({key})'], showlegend=False
    ))

# Points
def add_labeled_point(point, label, color, name):
    fig.add_trace(go.Scatter3d(
        x=[point[0]], y=[point[1]], z=[point[2]],
        mode='markers+text', marker=dict(size=6, color=color),
        text=[label], textposition='top center',
        name=name, showlegend=False
    ))

for pt, lbl in zip(n_points, ['|n₁⟩', '|n₂⟩']):
    add_labeled_point(pt, lbl, '#66c2a5', 'Necessity')

for pt, lbl in zip(o_points, ['|o₁⟩', '|o₂⟩']):
    add_labeled_point(pt, lbl, '#fc8d62', 'Opportunity')

add_labeled_point(mu_N, 'μ_N', 'purple', 'μ_N')
add_labeled_point(mu_O, 'μ_O', 'orange', 'μ_O')

# Vectors
def draw_line(start, end, color='gray', width=3, name=None):
    fig.add_trace(go.Scatter3d(
        x=[start[0], end[0]], y=[start[1], end[1]], z=[start[2], end[2]],
        mode='lines', line=dict(color=color, width=width),
        name=name, showlegend=bool(name)
    ))

for pt in n_points + o_points:
    draw_line(origin, pt, color='lightgray')

draw_line(origin, mu_N, color='gray')
draw_line(origin, mu_O, color='gray')
draw_line(mu_N, mu_O, color='black', name='‖μ_N - μ_O‖')

# Subspaces
def add_convex_mesh(points, color, label):
    hull = ConvexHull(points)
    fig.add_trace(go.Mesh3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        i=hull.simplices[:, 0], j=hull.simplices[:, 1], k=hull.simplices[:, 2],
        color=color, opacity=0.2, name=label
    ))
    center = points.mean(axis=0)
    fig.add_trace(go.Scatter3d(
        x=[center[0]], y=[center[1]], z=[center[2] + 0.05],
        mode='text', text=[label], showlegend=False
    ))

n_verts = np.array([[0.1,0.1,0],[0.5,0.1,0.3],[0.4,0.4,0.1],[0.1,0.3,0.2]])
o_verts = np.array([[0.5,0.6,0.4],[0.9,0.6,0.7],[0.8,0.9,0.5],[0.6,0.8,0.8]])
add_convex_mesh(n_verts, '#a6bddb', 'H_N')
add_convex_mesh(o_verts, '#fdb462', 'H_O')

# Layout
fig.update_layout(
    title="Hilbert Space ℋ Projected to 3D",
    scene=dict(
        xaxis=dict(title='Motivation & Alternatives (M)', range=[-0.1, 1.1]),
        yaxis=dict(title='Resource Endowment (R)', range=[-0.1, 1.1]),
        zaxis=dict(title='Innovation & Growth (I)', range=[-0.1, 1.1]),
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(x=0.8, y=0.9)
)

st.plotly_chart(fig, use_container_width=True)