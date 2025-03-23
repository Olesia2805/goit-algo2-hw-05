import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * self.size

    def add(self, password):
        for i in range(self.num_hashes):
            hash_value = mmh3.hash(password, i) % self.size
            self.bit_array[hash_value] = 1
        # print(f"Password '{password}' added to bit array at index {hash_value}")


def check_password_uniqueness(bloom_passwords, passwords):
    results = {}

    for password in passwords:
        result = "not unique"

        for i in range(bloom_passwords.num_hashes):
            hash_value = mmh3.hash(password, i) % bloom_passwords.size
            if bloom_passwords.bit_array[hash_value] == 0:
                result = "unique"
                break
        results[password] = result

        # print(f"Пароль '{password}' - {result}.")
    return results


if __name__ == "__main__":
    # Initialize Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Check new passwords
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print results
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
