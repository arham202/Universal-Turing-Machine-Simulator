import streamlit as st

class UTM:
    def __init__(self, states, input_symbols, transition,inital_state,final_state,blank_symbol):
        self.states = states
        self.input_symbols = input_symbols
        self.blank_symbol = blank_symbol
        self.transition = transition
        self.direction_mapping = {'L': '1', 'R': '11'}
        self.state_mapping = self.generate_state_mapping()
        self.symbol_mapping = self.generate_symbol_mapping()
        self.inital_states = self.state_mapping[inital_state]
        self.final_states = self.state_mapping[final_state]
        self.encode_transitions = self.encode_transition()
        self.tape1 = self.create_tape1(self.encode_transitions)

    def generate_state_mapping(self):
        state_mapping = {}
        states = {state.strip() for state in self.states.split(',')} 
        for index, state in enumerate(states):
            numerical_representation = str(1) * (index + 1)
            state_mapping[state] = numerical_representation
        return state_mapping

    def generate_symbol_mapping(self):
        symbol_mapping = {}
        input_symbols = {input_symbol.strip() for input_symbol in self.input_symbols.split(',')} 
        for index, symbol in enumerate(input_symbols):
            numerical_representation = str(1) * (index + 1)
            symbol_mapping[symbol] = numerical_representation
        return symbol_mapping

    def encode_transition(self):
        encoded_transition = []
        for (current_state, symbol), (next_state, write_symbol, move_direction) in self.transition.items():
            encoded_current_state = self.state_mapping[current_state]
            encoded_symbol = self.symbol_mapping[symbol]
            encoded_next_state = self.state_mapping[next_state]
            encoded_write_symbol = self.symbol_mapping[write_symbol]
            encoded_direction = self.direction_mapping[move_direction]
            
            encoded_key = encoded_current_state + '0' + encoded_symbol
            encoded_value = encoded_next_state + '0' + encoded_write_symbol + '0' + encoded_direction
            
            encoded_transition.append(encoded_key + '0' + encoded_value)
        return encoded_transition

    def create_tape1(self, encoded_transition):
        tape1 = ""
        for value in encoded_transition:
            tape1 = tape1 + value + "00"
        return tape1

    def encode_input_string(self, input_string):
        encoded_string = ""
        for symbol in input_string:
            encoded_symbol = self.symbol_mapping[symbol]
            encoded_string += encoded_symbol + "00"
        encoded_string = encoded_string.rstrip("00")
        return encoded_string

    def simulate_turing_machine(self, input_string):
        input_string += self.blank_symbol
        encoded_input_string = self.encode_input_string(input_string)

        st.write("State Mapping:")
        st.write(self.state_mapping)

        st.write("Symbol Mapping:")
        st.write(self.symbol_mapping)

        st.write("Direction Mapping:")
        st.write(self.direction_mapping)

        st.write("Tape 1:")
        st.write(self.tape1)

        split_by_00 = self.tape1.split("00")
        split_by_00_and_0 = [segment.split("0") for segment in split_by_00]
        split_input = encoded_input_string.split("00") # Tape 2

        head_pos = 0
        curr_state = self.inital_states
        state_symbol = []
        idx = 0

        while True:
            if idx >= len(split_by_00_and_0) - 1:
                break
            state = split_by_00_and_0[idx][0]
            symbol = split_by_00_and_0[idx][1]

            if (state, symbol) not in state_symbol:
                state_symbol.append((state, symbol))

            idx += 1

        while True:
            if head_pos < 0 or head_pos >= len(split_input):
                return False

            current_symbol = split_input[head_pos]
            
            st.markdown("---")

            st.write("Tape 2:")
            st.write(f"Current Symbol: {split_input}")

            st.write("Tape 3:")
            st.write(f"Current State: {curr_state}")

            if (curr_state, current_symbol) not in state_symbol:
                return False

            idx = 0
            while idx < len(split_by_00_and_0):
                if curr_state == split_by_00_and_0[idx][0] and current_symbol == split_by_00_and_0[idx][1]:
                    break
                idx += 1

            curr_state = split_by_00_and_0[idx][2]
            split_input[head_pos] = split_by_00_and_0[idx][3]
            if split_by_00_and_0[idx][4] == '1':
                head_pos -= 1
            else:
                head_pos += 1

            if curr_state == self.final_states:
                return True