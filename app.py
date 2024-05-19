import streamlit as st
from utm import UTM
from tm import TuringMachine
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import time

def main():
    
    with st.columns(3)[1]:
     st.image("assets/bml-color-logo.svg", width=200, use_column_width=True)
    st.title("Universal Turing Machine Simulator")

    st.sidebar.header("Define Turing Machine")
    states = ','.join([x.strip() for x in st.sidebar.text_input("Enter States (comma-separated):", key="states").split(',') if x.strip()])
    tape_symbols = ','.join([x.strip() for x in st.sidebar.text_input("Enter Tape alphabets (comma-separated):", key="tape_symbols").split(',') if x.strip()])
    alphabet = ','.join([x.strip() for x in st.sidebar.text_input("Enter Input symbols (comma-separated):", key="input").split(',') if x.strip()])
    blank_symbol = '_'
    st.sidebar.code("Blank symbol: _ ")
    initial_state = st.sidebar.text_input("Enter Initial state:", key="initial_state").strip()
    accept_states = ','.join([x.strip() for x in st.sidebar.text_input("Enter Accept states (comma-separated):", key="accept_states").split(',') if x.strip()])

    
    transitions = {}
    st.sidebar.subheader("Transitions")
    transition_counter = 1 
    while True:
        transition = st.sidebar.text_input(f"Enter transition {transition_counter} (state, symbol): (next_state, write_symbol, move):", key=f"transition_{transition_counter}").strip().replace(" ", "")
        if not transition:
            break
        transition_parts = transition.split(':')
        if len(transition_parts) != 2:
            st.error("Invalid transition format. Please use the format 'current_state, symbol: next_state, write_symbol, move'.")
            continue
        current_state, symbol = transition_parts[0].strip().split(',')
        next_state, write_symbol, move = transition_parts[1].strip().split(',')
        if move not in ['L', 'R']:
            st.error("Invalid movement direction. Please use 'L' for left or 'R' for right.")
            continue
        transitions[(current_state, symbol)] = (next_state, write_symbol, move)
        transition_counter += 1

    tm = TuringMachine(set(states.split(',')),set(tape_symbols.split(',')), set(alphabet.split(',')),blank_symbol,initial_state, set(accept_states.split(',')), transitions)

    input_string = st.text_input("Enter input string:", key="input_string")

    columns = st.columns([1, 1])
    animate = columns[0].checkbox("Enable Animation", key="animate_checkbox", value=False)
    binary_encoding = columns[1].checkbox("Binary Encoding")

    
    if st.button("Generate Transition Graph"):
        G = tm.generate_transition_graph()
        pos = nx.spring_layout(G)
        node_colors = ['lightgreen' if node == initial_state else 'lightcoral' if node == accept_states else 'skyblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=1500, font_size=10, arrows=True, node_color=node_colors)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)})
        # Create legend
        legend_elements = [
            Patch(facecolor='lightgreen', edgecolor='black', label='Initial State'),
            Patch(facecolor='lightcoral', edgecolor='black', label='Final State'),
            Patch(facecolor='skyblue', edgecolor='black', label='Other States')
        ]
        plt.legend(handles=legend_elements)
        st.pyplot(plt)

    def validate_input_string(input_string, input_symbols):
        for char in input_string:
            if char not in input_symbols:
                return False
        return True

    if not validate_input_string(input_string, set(alphabet.split(','))):
        st.error("Input string contains characters not present in the input symbols.")
        return

    if st.button("Simulate"):
        if not input_string:
            st.error("Please provide an input string.")
            return
            
        if binary_encoding:
            utm = UTM(states, tape_symbols, transitions, initial_state, accept_states, blank_symbol)
            result = utm.simulate_turing_machine(input_string)
        else:
            result = tm.simulate(input_string,animate)
            
        st.markdown("---")

        if result:
            st.success("Input string accepted.")
        else:
            st.error("Input string rejected.")


if __name__ == "__main__":
    main()