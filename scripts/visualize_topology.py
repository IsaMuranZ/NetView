# scripts/visualize_topology.py

import networkx as nx
import matplotlib.pyplot as plt
# modules for creating graphs to visualize our data
from app import create_app
from app.models import Device
# access to the Device model and app context


# function that creates a graph to be used on the frontend
def visualize_topology():
    app = create_app()
    with app.app_context():
        # Create a graph
        g = nx.Graph()

        # Fetch devices from the database
        devices = Device.query.all()

        # Add nodes and edges based on IP addresses
        for device in devices:
            g.add_node(device.ip_address, label=device.hostname or device.ip_address)
            # Optionally add more edges or attributes here

        # Draw the network topology
        pos = nx.spring_layout(g)  # Layout for node positioning
        nx.draw(g, pos, with_labels=True, node_size=2000, node_color='lightblue',
                font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Network Topology")
        plt.show()


if __name__ == "__main__":
    visualize_topology()
