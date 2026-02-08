import networkx as nx
import numpy as np
import pandas as pd
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkManager:
    def __init__(self, num_hubs=4, num_spokes=40):
        self.G = nx.Graph()
        self.num_hubs = num_hubs
        self.num_spokes = num_spokes
        self.major_hubs = ["JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Bank of America", "Citigroup", "HSBC", "BNP Paribas", "Deutsche Bank"]
        self.regional_banks = [
            "Silicon Valley Bank", "Signature Bank", "First Republic", "Credit Suisse", "Barclays",
            "Societe Generale", "UBS", "Wells Fargo", "Santander", "Standard Chartered",
            "Mitsubishi UFJ", "Sumitomo Mitsui", "Mizuho", "Bank of China", "ICBC",
            "Royal Bank of Canada", "Toronto-Dominion", "Scotiabank", "BMO", "CIBC",
            "Lloyds Banking Group", "NatWest", "Commerzbank", "ING Group", "UniCredit",
            "Intesa Sanpaolo", "BBVA", "Nordea", "Danske Bank", "DNB",
            "National Australia Bank", "Commonwealth Bank", "Westpac", "ANZ", "DBS Bank",
            "OCBC", "UOB", "Standard Bank", "Absa Group", "Nedbank"
        ]
        self.initialize_network()

    def initialize_network(self):
        """
        Creates a hub-and-spoke financial network with realistic bank names.
        """
        # Assign real names to hubs and spokes
        hubs = random.sample(self.major_hubs, k=min(self.num_hubs, len(self.major_hubs)))
        available_spokes = self.regional_banks + [f"Regional Bank {i}" for i in range(max(0, self.num_spokes - len(self.regional_banks)))]
        spokes = random.sample(available_spokes, k=self.num_spokes)
        
        self.G.add_nodes_from(hubs, type='hub')
        self.G.add_nodes_from(spokes, type='spoke')
        
        # Connect hubs to each other (Systemic Core)
        for i in range(len(hubs)):
            for j in range(i + 1, len(hubs)):
                self.G.add_edge(hubs[i], hubs[j], weight=random.uniform(0.7, 1.0))
        
        # Connect spokes to hubs (Preferential attachment)
        for spoke in spokes:
            # Each spoke connects to 1-2 hubs (Interbank exposure)
            target_hubs = random.sample(hubs, k=random.randint(1, 2))
            for hub in target_hubs:
                self.G.add_edge(spoke, hub, weight=random.uniform(0.2, 0.6))

        # Initial Wealth Distribution
        wealths = np.random.pareto(1.5, len(hubs) + len(spokes)) + 1
        wealths = (wealths / np.max(wealths)) * 150000 
        sorted_wealths = sorted(wealths, reverse=True)
        
        node_data = {}
        for i, node in enumerate(hubs):
            node_data[node] = {
                'wealth': sorted_wealths[i],
                'leverage': 1.0,
                'status': 'healthy',
                'color': 'green'
            }
        
        for i, node in enumerate(spokes):
            node_data[node] = {
                'wealth': sorted_wealths[len(hubs) + i],
                'leverage': 1.0,
                'status': 'healthy',
                'color': 'green'
            }
        
        nx.set_node_attributes(self.G, node_data)

    def fail_node(self, node_name):
        """Manually trigger a failure for a specific bank."""
        if node_name in self.G.nodes:
            self.G.nodes[node_name]['status'] = 'failed'
            self.G.nodes[node_name]['wealth'] = 0
            self.G.nodes[node_name]['color'] = 'red'
            return True
        return False

    def update_contagion(self, ccp=None):
        """
        Simulates systemic stress propagation with optional CCP intervention. 
        Returns a list of impacted nodes and the intervention report.
        """
        impacted = []
        intervention_report = None
        
        # Identify nodes that are already failed
        failed_nodes = [n for n, d in self.G.nodes(data=True) if d['status'] == 'failed']
        
        for failed_node in failed_nodes:
            neighbors = list(self.G.neighbors(failed_node))
            if not neighbors: continue
            
            # Calculate potential hits for all neighbors of this failed bank
            loss_per_bank = {}
            for neighbor in neighbors:
                if self.G.nodes[neighbor]['status'] != 'failed':
                    # Hit neighbor wealth (Contagion factor: 30%)
                    loss_per_bank[neighbor] = self.G.nodes[neighbor]['wealth'] * 0.3
            
            if not loss_per_bank: continue
            
            # Try to get CCP to absorb these hits
            if ccp:
                intervention_report = ccp.process_failures(failed_node, neighbors, loss_per_bank)
                # Adjust hits based on what CCP absorbed
                for event in intervention_report['detailed_events']:
                    bank = event['target_bank']
                    loss_per_bank[bank] -= event['allotment']
            
            # Apply remaining hits to neighbor wealth
            for bank, remaining_hit in loss_per_bank.items():
                if remaining_hit > 1: # Only apply significant hits
                    self.G.nodes[bank]['wealth'] -= remaining_hit
                    self.G.nodes[bank]['status'] = 'stressed'
                    self.G.nodes[bank]['color'] = 'orange'
                    impacted.append(bank)
                    
                    # Check for secondary failure
                    if self.G.nodes[bank]['wealth'] < 300: # Failure threshold
                        self.G.nodes[bank]['status'] = 'failed'
                        self.G.nodes[bank]['color'] = 'red'
        
        return list(set(impacted)), intervention_report

    def get_graph_data(self):
        return self.G

if __name__ == "__main__":
    nm = NetworkManager()
    print(f"Network initialized with {nm.G.number_of_nodes()} nodes and {nm.G.number_of_edges()} edges.")
    # Simulate one failure
    hub0 = "HUB_0"
    nm.G.nodes[hub0]['status'] = 'failed'
    nm.G.nodes[hub0]['color'] = 'red'
    nm.update_contagion()
    for node, data in nm.G.nodes(data=True):
        if data['color'] != 'green':
            print(f"Node {node}: {data['status']} (Wealth: {data['wealth']:.2f})")
