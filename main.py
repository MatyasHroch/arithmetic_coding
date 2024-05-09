# this code is an implementation of arithmetic integer encoding and decoding
import math

cx = 0


def to_binary(num: int, size: int) -> list[int]:
    binary = []
    while num > 0:
        binary.insert(0, num % 2)
        num = num // 2

    while len(binary) < size:
        binary.insert(0, 0)
    return binary


def shift_range(low_bin: list[int], upper_bin: list[int]):
    low_bin = low_bin[1:]
    upper_bin = upper_bin[1:]
    low_bin.append(0)
    upper_bin.append(1)
    return low_bin, upper_bin


def to_decimal(binary: list[int]) -> int:
    decimal = 0
    for i in range(len(binary)):
        decimal += binary[i] * pow(2, len(binary) - i - 1)
    return decimal


def write_bit(bit: int, output):
    output.append(bit)
    negation = 1 - bit
    global cx
    if cx:
        for _ in range(cx):
            output.append(negation)
        cx = 0


def recalc_ranges_and_write(low: int, upper: int, output: list[int], data_size: int):
    low_bin = to_binary(low, data_size)
    upper_bin = to_binary(upper, data_size)

    while True:
        if low_bin[0] == upper_bin[0]:
            print(f"Equal Case, both bits are {low_bin[0]}")
            write_bit(low_bin[0], output)
            low_bin, upper_bin = shift_range(low_bin, upper_bin)
            continue

        if low_bin[0] == 0 and upper_bin[0] == 1:
            if low_bin[1] == 1 and upper_bin[1] == 0:
                print("Third case, second bit is 1 and 0")
                global cx
                cx += 1
                low_bin, upper_bin = shift_range(low_bin, upper_bin)
                low_bin[0] = 0
                upper_bin[0] = 1
                continue
            else:
                break

    low = to_decimal(low_bin)
    upper = to_decimal(upper_bin)
    return low, upper


def new_ranges(
    symbol: str, frequency: dict[str, int], low, upper, data_size: int
) -> tuple[int, int]:
    interval_size = upper - low + 1
    print(f"interval_size: {interval_size}")

    part = interval_size // data_size
    print(f"Part: {part}")

    frequency_sum = 0
    for key in frequency:
        if key == symbol:
            break
        frequency_sum += frequency[key]

    print(f"Frequency sum: {frequency_sum}")

    low = low + part * frequency_sum
    upper = low + part * frequency[symbol] - 1

    print(f"New Low: {low}")
    print(f"New Upper: {upper}")

    return low, upper


def encode(data: str):
    data_size: int = len(data)
    frequency: dict[str, int] = {}

    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    print(f"Frequency: {frequency}")
    print(f"Data size: {data_size}")

    encoded_data: list[int] = []

    low = 0
    m = math.ceil(math.log2(data_size * 4) + 1)
    upper = pow(2, m) - 1

    for symbol in data:
        print(f"\nSymbol: {symbol}")
        print(f"Low: {low}")
        print(f"Upper: {upper}")
        low, upper = new_ranges(symbol, frequency, low, upper, data_size)
        low, upper = recalc_ranges_and_write(low, upper, encoded_data, data_size)

    # print(f"Encoded data: {encoded_data}")
    return encoded_data, frequency


# def main():
#     words = ["hippopotamus"]
#     encoded_words = []
#     print("Hello, World!")
#     data: str = "hello"
#     for word in words:
#         encoded_word = encode(word)
#         print(f"\nWord: {word}")
#         print(f"Encoded Word: {encoded_word}\n")
#         print(f"cx: {cx}")


# if __name__ == "__main__":
#     main()


def shift_encoded_data(encoded_data: list[int]) -> list[int]:
    global cx
    shift_count = cx + 1
    cx = 0
    return encoded_data[shift_count:]


def recalc_ranges_decoding(
    low: int, upper: int, encoded_data: list[int], data_size: int
):
    low_bin = to_binary(low, data_size)
    upper_bin = to_binary(upper, data_size)

    while True:
        if low_bin[0] == upper_bin[0]:
            print(f"Equal Case, both bits are {low_bin[0]}")
            encoded_data = shift_encoded_data(encoded_data)
            low_bin, upper_bin = shift_range(low_bin, upper_bin)
            continue

        if low_bin[0] == 0 and upper_bin[0] == 1:
            if low_bin[1] == 1 and upper_bin[1] == 0:
                print("Third case, second bit is 1 and 0")
                global cx
                cx += 1
                low_bin, upper_bin = shift_range(low_bin, upper_bin)
                low_bin[0] = 0
                upper_bin[0] = 1
                continue
            else:
                break

    low = to_decimal(low_bin)
    upper = to_decimal(upper_bin)
    return low, upper, encoded_data


def decode(encoded_data: list[int], frequency: dict[str, int], data_size: int) -> str:
    m = math.ceil(math.log2(data_size * 4) + 1)
    low = 0
    upper = pow(2, m) - 1
    decoded_data = []

    i = 0

    while len(decoded_data) < m:
        i += 1
        print("\n")
        while len(encoded_data) < m:
            encoded_data.append(0)

        window = encoded_data[:m]
        int_window = to_decimal(window)

        interval_size = upper - low + 1
        part = interval_size // data_size
        cum_value = low
        symbol = None

        for key, the_freq in frequency.items():
            the_part = part * the_freq
            if cum_value + the_part > int_window:
                symbol = key
                break
            cum_value += the_part

        print("Decoded symbol: " + symbol)
        print(f"Range: ({low} - {upper}) ")
        print(f"Part: {part}")

        low = low + cum_value
        upper = low + part * frequency[symbol] - 1

        decoded_data.append(symbol)

        print(f"New Low: {low}")
        print(f"New Upper: {upper}")

        low, upper, encoded_data = recalc_ranges_decoding(
            low, upper, encoded_data, data_size
        )

    return decoded_data


def main():
    global cx
    word_to_encode = "klokan"
    encoded_data, frequency = encode(word_to_encode)
    print("Encoded data:", encoded_data, "\n\n\n")

    cx = 0

    decoded_data = decode(encoded_data, frequency, len(word_to_encode))
    print("Decoded data:", decoded_data)


if __name__ == "__main__":
    main()
