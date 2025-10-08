import socket
from ClientBase import BettingAnswer

# Server Configuration
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

class PokerClient:
    def __init__(self):
        self.current_hand = []
        self.state = {}
        self.buffer = ""

    def evaluate_hand_strength(self, hand):
        """Evaluates the hand strength based on card rankings."""
        hand_strength = 0
        rank_counts = {}
        for card in hand:
            rank = card[:-1]
            rank_counts[rank] = rank_counts.get(rank, 0) + 1

        pairs = sum(1 for count in rank_counts.values() if count == 2)
        if pairs:
            hand_strength += pairs * 10
        return hand_strength

    def process_line(self, s, line):
        """Processes a single line from the server."""
        line = line.strip()
        if not line:
            print("Empty line received. Skipping.")
            return

        message = line.split()
        if not message:
            print("Malformed or empty message. Skipping.")
            return

        command = message[0]
        print(f"Processing command: {command}")

        if command == "Name?":
            s.send("Name ReflexAgent\n".encode())

        elif command == "Chips":
            if len(message) >= 3:
                player_name, chips = message[1], int(message[2])
                self.state[player_name] = chips
                print(f"{player_name} has {chips} chips.")
            else:
                print(f"Malformed 'Chips' message: {message}. Skipping.")

        elif command == "Cards":
            self.current_hand = message[1:]
            print(f"Current hand: {self.current_hand}")

        elif command == "Game_Over":
            print("Game Over.")
            return "END"

        else:
            print(f"Unknown command: {command}. Skipping.")

    def run(self):
        """Main function to run the poker client."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        try:
            while True:
                # Receive data from server
                data = s.recv(BUFFER_SIZE).decode("utf-8")
                if not data:
                    print("No data received. Connection might be closed.")
                    break

                # Add data to buffer and process complete lines
                self.buffer += data
                lines = self.buffer.split("\n")
                self.buffer = lines.pop()  # Retain the last partial line for the next iteration

                for line in lines:
                    result = self.process_line(s, line)
                    if result == "END":
                        return
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            s.close()


if __name__ == "__main__":
    client = PokerClient()
    client.run()
