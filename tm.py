import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

class TuringMachine:
    def __init__(self, states, tape_symbols,alphabet,blank_symbol, initial_state, accept_states, transitions):
        self.states = states # Q
        self.tape_symbols = tape_symbols # T
        self.alphabet = alphabet # E
        self.initial_state = initial_state # q0
        self.accept_states = accept_states # F
        self.transitions = transitions # 8
        self.current_state = initial_state 
        self.tape = [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head_position = 0

    def transition(self, symbol):
        if (self.current_state, symbol) not in self.transitions:
            return False
        next_state, write_symbol, move = self.transitions[(self.current_state, symbol)]
        self.current_state = next_state
        self.tape[self.head_position] = write_symbol
        if move == 'L':
            self.head_position -= 1
            if self.head_position < 0:
                self.tape.insert(0, '_')
                self.head_position = 0
        elif move == 'R':
            self.head_position += 1
            if self.head_position == len(self.tape):
                self.tape.append('_')
        return True

    def simulate(self, input_string,animate):
        self.tape = [self.blank_symbol] + list(input_string) + [self.blank_symbol]  # Initialize tape with input string
        self.head_position = 1
        self.current_state = self.initial_state

        st.write("Simulation Steps:")
        while True:
            self.display_tape()
            if animate:
                time.sleep(1)  # Added sleep for animation effect
            symbol = self.tape[self.head_position]
            if not self.transition(symbol):
                return False
            if self.current_state in self.accept_states:
                return True

    def display_tape(self):
        tape_display = ""
        for i, symbol in enumerate(self.tape):
            if i == self.head_position:
                tape_display += f"<span style='background-color: rgb(255 75 75); padding: 2px;color: white'>{symbol}</span>"
            else:
                tape_display += symbol
        st.markdown("---")
        st.write(f"**State:** {self.current_state}<br><b>Head Position:</b> {self.head_position}, <b>Tape:</b> {tape_display}", unsafe_allow_html=True)

    def reset(self):
        self.current_state = self.initial_state
        self.tape = [self.blank_symbol]
        self.head_position = 0

    def generate_transition_graph(self):
        G = nx.DiGraph()

        initial_state = self.initial_state
        final_state = self.accept_states

        for transition, (next_state, write_symbol, move) in self.transitions.items():
            current_state, symbol = transition
            G.add_edge(current_state, next_state, label=f"{symbol}, {write_symbol}, {move}")
            if current_state == next_state:
                if (current_state, current_state) not in G.edges():
                    G.add_edge(current_state, current_state, label=f"{symbol}, {write_symbol}, {move}")
                else:
                    G.edges[current_state, current_state]['label'] += f"\n{symbol}, {write_symbol}, {move}"
        node_colors = ['lightgreen' if node == initial_state else 'lightcoral' if node == final_state else 'skyblue' for node in G.nodes()]
        nx.set_node_attributes(G, dict(zip(G.nodes(), node_colors)), 'color')

        return G