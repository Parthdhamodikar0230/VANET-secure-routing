import random
import hashlib
import matplotlib.pyplot as plt
import time
import pandas as pd

class Vehicle:
    def __init__(self, vehicle_id, speed, position):
        self.id = vehicle_id
        self.speed = speed
        self.position = position
        self.salt = "vanet" + str(random.random())

    def move(self, dt):
        self.position = (
            self.position[0] + self.speed * dt * random.uniform(0.9, 1.1),
            self.position[1] + self.speed * dt * random.uniform(0.9, 1.1)
        )

    def check_collision(self, other, threshold=1):
        distance = ((self.position[0] - other.position[0]) ** 2 +
                    (self.position[1] - other.position[1]) ** 2) ** 0.5
        return distance < threshold

    def generate_message(self):
        message = {
            "vehicle_id": self.id,
            "speed": self.speed,
            "position": self.position,
        }
        return message, self.hash_message(message)

    def hash_message(self, message):
        message_bytes = str(message).encode()
        hashes = {}
        for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']:
            start_time = time.time()
            digest = getattr(hashlib, algo)(message_bytes + self.salt.encode()).hexdigest()
            hashes[algo] = digest
            hashes[algo + "_time"] = time.time() - start_time
        return hashes

    def check_integrity(self, message, hashes):
        fresh_hashes = self.hash_message(message)
        for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']:
            if hashes.get(algo) != fresh_hashes.get(algo):
                return False
        return True

    def receive_message(self, message, hashes):
        print(f"Vehicle {self.id} received message from {message['vehicle_id']}: {message}")
        if self.check_integrity(message, hashes):
            print("✅ Message integrity is valid.\n")
        else:
            print("❌ Message integrity is NOT valid!\n")

def simulate(vehicles, dt, steps):
    hash_times = {algo: [] for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']}
    for _ in range(steps):
        for v in vehicles:
            v.move(dt)
            message, hashes = v.generate_message()

            # Simulate random tampering
            if random.randint(0, 9) == 3:
                message["speed"] += 30  # tampered

            for other in vehicles:
                if other != v:
                    other.receive_message(message.copy(), hashes.copy())

            for algo in hash_times:
                hash_times[algo].append(hashes[algo + "_time"])

    return hash_times

def plot_hash_times(hash_times):
    df = pd.DataFrame([
        {"algo": algo, "time": t}
        for algo, times in hash_times.items()
        for t in times
    ])
    df.boxplot(by="algo", column="time", showmeans=True)
    plt.title("Hash Generation Times")
    plt.xlabel("Hash Function")
    plt.ylabel("Time (s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/hash_times.png")
    plt.close()
def plot_speeds(vehicles, steps, dt):
    times = list(range(steps))
    data = {v.id: [] for v in vehicles}
    for _ in times:
        for v in vehicles:
            v.move(dt)
            data[v.id].append(v.speed)
    df = pd.DataFrame(data, index=times)
    df.plot(title="Vehicle Speeds Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Speed")
    plt.tight_layout()
    plt.savefig("plots/vehicle_speeds.png")
    plt.close()

def plot_positions(vehicles, steps, dt):
    positions = {v.id: [] for v in vehicles}
    for _ in range(steps):
        for v in vehicles:
            v.move(dt)
            positions[v.id].append(v.position)
    for vid, coords in positions.items():
        x, y = zip(*coords)
        plt.plot(x, y, label=vid)
    plt.title("Vehicle Positions")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plots/vehicle_positions.png")
    plt.close()

# ---- Simulation Start ----
if __name__ == "__main__":
    # Vehicle setup
    v1 = Vehicle("V1", 65, (0, 0))
    v2 = Vehicle("V2", 50, (10, 20))
    v3 = Vehicle("V3", 35, (30, 50))
    v4 = Vehicle("V4", 20, (10, 50))
    v5 = Vehicle("V5", 95, (30, 10))
    v6 = Vehicle("V6", 70, (70, 10))

    # Test messages (valid & tampered)
    m1, h1 = v1.generate_message()
    v2.receive_message(m1, h1)
    m1_t = m1.copy(); m1_t["speed"] = 100
    v2.receive_message(m1_t, h1)

    m2, h2 = v3.generate_message()
    v4.receive_message(m2, h2)
    m2_t = m2.copy(); m2_t["speed"] = 100
    v4.receive_message(m2_t, h2)

    # Run simulation for pairs
    simulate([v1, v2], 0.1, 100)
    plot_speeds([v1, v2], 100, 0.1)
    plot_positions([v1, v2], 100, 0.1)

    simulate([v3, v4], 0.1, 100)
    plot_speeds([v3, v4], 100, 0.1)
    plot_positions([v3, v4], 100, 0.1)

    # Final plot
    ht = simulate([v5, v6], 0.1, 100)
    plot_hash_times(ht)
