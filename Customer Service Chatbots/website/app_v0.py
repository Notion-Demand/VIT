from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Load the data
data = pd.read_csv('./data.csv')

# Helper function to generate graphs
def create_graphs():
    # 1. Current week graph
    week_days = ['Weekstart', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    resolution_levels = ['None', 'Low', 'Medium', 'High', '20']
    current_week_fig = go.Figure(data=go.Heatmap(
        z=[[None, 20, 'Low', 'Medium', 'High']] * len(week_days),
        x=resolution_levels,
        y=week_days,
        colorscale='Viridis',
        showscale=True
    ))
    current_week_fig.update_layout(
        title='Current Week Overview',
        xaxis_title='Resolution Level',
        yaxis_title='Day of Week'
    )

    # 2. Data origin breakdown
    data_origin_fig = go.Figure()
    data_origin_fig.add_trace(go.Bar(
        y=['Email', 'Manual Entry', 'Phone Call', 'Web Form'],
        x=[200, 150, 400, 250],
        orientation='h',
        name="Data Origin"
    ))
    data_origin_fig.update_layout(
        title="Data Origin Breakdown",
        xaxis_title="Count",
        yaxis_title="Origin"
    )

    # 3. Average resolution time
    avg_resolution_fig = go.Figure(data=[
        go.Bar(y=['Over 2 hours', '1-2 hours', 'Under 1 hour'], x=[30, 50, 70], name='Custom'),
        go.Bar(y=['Over 2 hours', '1-2 hours', 'Under 1 hour'], x=[20, 40, 60], name='Real-time'),
        go.Bar(y=['Over 2 hours', '1-2 hours', 'Under 1 hour'], x=[10, 30, 50], name='Dynamic'),
        go.Bar(y=['Over 2 hours', '1-2 hours', 'Under 1 hour'], x=[5, 25, 45], name='Advanced'),
        go.Bar(y=['Over 2 hours', '1-2 hours', 'Under 1 hour'], x=[3, 20, 40], name='AI-driven')
    ])
    avg_resolution_fig.update_layout(
        title="Average Resolution Time",
        xaxis_title="Resolution Time",
        yaxis_title="Time Categories",
        barmode='group'
    )

    # Return graphs as HTML divs
    graphs = {
        'current_week': current_week_fig.to_html(full_html=False),
        'data_origin': data_origin_fig.to_html(full_html=False),
        'avg_resolution': avg_resolution_fig.to_html(full_html=False)
    }

    return graphs

@app.route('/')
def index():
    # Generate graphs
    graphs = create_graphs()
    
    # Cards info (these would be dynamic based on data, for now static)
    cards = {
        'retailers': 50,
        'customers': 120,
        'escalations': 6,
        'issues': 15
    }
    
    # Pass graphs and cards to the HTML template
    return render_template('dashboard.html', graphs=graphs, cards=cards)

if __name__ == '__main__':
    app.run(debug=True)
