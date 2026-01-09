from src.quantum_rng import QuantumRNG
import pytest

def test_random_number_generation_with_num_qubits() -> None:
    rng = QuantumRNG(num_qubits=4)
    random_numbers = [rng.random_number_generation() for _ in range(10)]
    for random_number in random_numbers:
        assert 0 <= random_number < 16, "Random number should be in the range [0, 15]"

def test_random_number_generation_with_range() -> None:
    rng = QuantumRNG(range=(10, 20))
    random_numbers = [rng.random_number_generation() for _ in range(10)]
    for random_number in random_numbers:
        assert 10 <= random_number <= 20, "Random number should be in the range [10, 20]"

def test_random_number_generation_with_both() -> None:
    rng = QuantumRNG(num_qubits=3, range=(5, 25))
    random_numbers = [rng.random_number_generation() for _ in range(10)]
    for random_number in random_numbers:
        assert 5 <= random_number < 13, "Random number should be in the range [5, 12] due to num_qubits precedence"

def test_invalid_initialization() -> None:
    with pytest.raises(ValueError):
        QuantumRNG()  # Neither num_qubits nor range provided
    
def test_with_negative_range() -> None:
    rng = QuantumRNG(range=(-5, -1))
    random_numbers = [rng.random_number_generation() for _ in range(10)]
    for random_number in random_numbers:
        assert -5 <= random_number <= -1, "Random number should be in the range [-5, -1]"

