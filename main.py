from src.quantum_rng import QuantumRNG

def main() -> None:
    # Example usage of QuantumRNG
    rng = QuantumRNG(range=(1, 100))
    random_number = rng.random_number_generation()
    print(f"Generated random number: {random_number}")
    
    # Display the quantum circuit
    print(rng)

if __name__ == "__main__":
    main()