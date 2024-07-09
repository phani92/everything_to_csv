# Author: Phani
# Date: 2021-06-24
# This script reads I2C data from a CSV file exported by a logic analyzer and converts it into a human-readable format.

import csv

def read_i2c_data(file_path):
    """Read I2C data from a CSV file exported by a logic analyzer."""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)

def parse_i2c_data(data, valid_address=None, include_timestamps=True, include_start_stop=True, skip_illegal_operations=True):
    """Parse the I2C data into a human-readable format."""
    parsed_data = []
    current_message = []
    current_read_bytes = []
    current_write_bytes = []
    current_registers = []
    current_operation = None
    repeat_read_mode = False

    for row in data:
        if len(row) != 3:
            print(f"Unexpected number of items in row: {row}")
            continue

        id, timestamp, signal = row
        timestamp = float(timestamp)
        timestamp_str = f"{timestamp:.2f} ns: " if include_timestamps else ""

        try:
            if "Start" in signal:
                if current_message and (valid_address is None or not skip_illegal_operations or any(f"Address {hex(valid_address)}" in msg for msg in current_message)):
                    if current_read_bytes:
                        current_message.append("Data " + " ".join(current_read_bytes))
                    if current_registers:
                        current_message.append("Register " + " ".join(current_registers))
                    if current_write_bytes:
                        current_message.append("Data " + " ".join(current_write_bytes))
                    if current_message:
                        parsed_data.append(current_message)
                current_message = [f"{timestamp_str}START"] if include_start_stop else []
                current_read_bytes = []
                current_write_bytes = []
                current_registers = []
                current_operation = None
                repeat_read_mode = False

            elif "Stop" in signal:
                if current_message and (valid_address is None or not skip_illegal_operations or any(f"Address {hex(valid_address)}" in msg for msg in current_message)):
                    if current_read_bytes:
                        current_message.append("Data " + " ".join(current_read_bytes))
                    if current_registers:
                        current_message.append("Register " + " ".join(current_registers))
                    if current_write_bytes:
                        current_message.append("Data " + " ".join(current_write_bytes))
                    if include_start_stop:
                        current_message.append(f"{timestamp_str}STOP")
                    if current_message:
                        parsed_data.append(current_message)
                current_message = []
                current_read_bytes = []
                current_write_bytes = []
                current_registers = []
                current_operation = None
                repeat_read_mode = False

            elif "Address write" in signal or "Address read" in signal:
                parts = signal.split(":")
                address_data = parts[1].strip()
                try:
                    address = int(address_data.strip("[]"), 16)
                    rw = "Read" if address & 1 else "Write"
                    address >>= 1
                    if valid_address is not None and address != valid_address:
                        print(f"Skipping operation with address: {hex(address)}")
                        continue
                    if current_operation != rw and current_read_bytes and current_operation == "Read":
                        current_message.append("Data " + " ".join(current_read_bytes))
                        current_read_bytes = []
                    if current_operation != rw and current_write_bytes and current_operation == "Write":
                        current_message.append("Data " + " ".join(current_write_bytes))
                        current_write_bytes = []
                    current_operation = rw
                    current_message.append(f"{timestamp_str}Address {hex(address)} ({rw})")
                except ValueError:
                    print(f"Invalid address detected: {address_data}")
                    continue

            elif "Repeat" in signal:
                repeat_read_mode = True

            elif "Data write" in signal or "Data read" in signal:
                if valid_address is None or not skip_illegal_operations or any(f"Address {hex(valid_address)}" in msg for msg in current_message):
                    parts = signal.split(":")
                    data_value = parts[1].strip().strip("[]")
                    if "Data read" in signal:
                        if repeat_read_mode:
                            current_message.append("Repeat Read")
                            repeat_read_mode = False
                        current_read_bytes.append(data_value)
                    else:
                        if len(current_registers) < 2:
                            current_registers.append(data_value)
                        else:
                            current_write_bytes.append(data_value)

            # Skip ACK and NACK signals
        except ValueError as e:
            print(f"Error parsing row {row}: {e}")

    if current_message and (valid_address is None or not skip_illegal_operations or any(f"Address {hex(valid_address)}" in msg for msg in current_message)):
        if current_read_bytes:
            current_message.append("Data " + " ".join(current_read_bytes))
        if current_registers:
            current_message.append("Register " + " ".join(current_registers))
        if current_write_bytes:
            current_message.append("Data " + " ".join(current_write_bytes))
        parsed_data.append(current_message)

    return parsed_data

def format_parsed_data(parsed_data):
    """Format the parsed data into a human-readable string."""
    formatted_output = []
    for message in parsed_data:
        if message:  # Ensure no empty messages are appended
            formatted_output.append("\n".join(message))
    return "\n\n".join(formatted_output)

def save_output(file_path, output):
    """Save the formatted output to a file."""
    with open(file_path, 'w') as file:
        file.write(output)

def main(input_file, output_file, valid_address=None, include_timestamps=True, include_start_stop=True, skip_illegal_operations=True):
    data = read_i2c_data(input_file)
    parsed_data = parse_i2c_data(data, valid_address, include_timestamps, include_start_stop, skip_illegal_operations)
    if not parsed_data:
        print("Failed to parse I2C data")
        return
    formatted_output = format_parsed_data(parsed_data)
    save_output(output_file, formatted_output)
    print(f"Formatted I2C data saved to {output_file}")

# Example usage
input_file = ""# Set to the path of the CSV file exported by the logic analyzer
output_file = ""# Set to the path where the formatted output should be saved
valid_address = ""# Set to the address you want to validate against
include_timestamps = False  # Set to False to skip timestamps
include_start_stop = False  # Set to False to skip START and STOP
skip_illegal_operations = True  # Set to False to include illegal operations
main(input_file, output_file, valid_address, include_timestamps, include_start_stop, skip_illegal_operations)
