from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from dataclasses import dataclass
from typing import Optional

@dataclass
class QuantumRNG:
    """
    Args:
        num_qubits (int): Number of qubits to use for generating random bits.
        range (tuple[int, int]): Tuple of (min, max) for the random number range.
    If both range and num_qubits are provided, num_qubits takes precedence.
    """
    num_qubits: Optional[int] = None
    range: Optional[tuple[int, int]] = None

    def __post_init__(self) -> None:
        if self.num_qubits is None:
            if self.range is not None:
                min_val, max_val = self.range
                range_size = max_val - min_val + 1
                self.num_qubits = range_size.bit_length()
            else:
                raise ValueError("Either num_qubits or range must be provided.")

        if self.num_qubits >=9:
            print(f"Number of qubits being used = {self.num_qubits}. This may take a moment to generate.")
        self.qr = QuantumRegister(self.num_qubits, 'q')
        self.cr = ClassicalRegister(self.num_qubits, 'c')
        self.simulator = AerSimulator()

    def _generate_random_bits(self) -> str:

        self.circuit = QuantumCircuit(self.qr, self.cr) # New circuit for each generation, resuing same circuit again and again is conceptually wrong

        # Create superposition
        self.circuit.h(self.qr)

        # Measure the qubits
        self.circuit.measure(self.qr, self.cr)

        # Transpile the circuit for the simulator
        transpiled_circuit = transpile(self.circuit, self.simulator)

        # Execute the circuit on the simulator
        job = self.simulator.run(transpiled_circuit, shots=1)
        result = job.result()

        # Get the measurement result
        counts = result.get_counts()
        random_bits = list(counts.keys())[0]
        return random_bits

    def random_number_generation(self) -> int:
        """Generates a random number within the specified range using quantum randomness.

        Returns:
            int: A random integer within the specified range.
        """
        random_bits = self._generate_random_bits()
        random_int = int(random_bits, 2)

        if self.range is not None:
            min_val, max_val = self.range
            if min_val > max_val:
                raise ValueError("Invalid range: min should be less than or equal to max.")
            while not (min_val <= random_int <= max_val):
                random_bits = self._generate_random_bits()
                random_int = min_val + int(random_bits, 2) # Using modulo created bias.

        return random_int
    
    def _draw_circuit(self) -> None:
        """Utility method to draw the quantum circuit."""
        print(self.circuit.draw())
    
    def __repr__(self) -> str:
        _draw_circuit = self._draw_circuit()
        return f"QuantumRNG(num_qubits={self.num_qubits})"
    
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Quantum Random Number Generator")
    parser.add_argument("--qubits", type=int, help="Number of qubits to use for generating random bits.")
    parser.add_argument("--min", type=int, help="Minimum value of the random number range.")
    parser.add_argument("--max", type=int, help="Maximum value of the random number range.")
    parser.add_argument("--size", type=int, help="Total size of random numbers to generate.")
    args = parser.parse_args()

    if args.min is not None and args.max is not None:
        qrng = QuantumRNG(range=(args.min, args.max))
    elif args.qubits is not None:
        qrng = QuantumRNG(num_qubits=args.qubits)
    else:
        raise ValueError("Either num_qubits or both min and max must be provided.")
    
    __ = 1 if not args.size else args.size
    for _ in range(__):
        random_number = qrng.random_number_generation()
        print(f"Generated random number: {random_number}")