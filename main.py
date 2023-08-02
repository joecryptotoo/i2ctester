import time
import board
import busio
import argparse
import secrets

from adafruit_atecc.adafruit_atecc import ATECC, _WAKE_CLK_FREQ

parser = argparse.ArgumentParser(description='Description of your script.')
parser.add_argument('-i','--iterations', help='Number of iterations to run', required=False, default=100)
parser.add_argument('-s','--slot', help='slot to use', required=False, default='0')
parser.add_argument('-a','--i2c_address', help='i2c address to use', required=False, default='0x60')
parser.add_argument('-r','--random', help='use 32 bytes of random data', required=False, default=False)
arg = parser.parse_args()

slotId = int(arg.slot)
it = int(arg.iterations)
i2c = busio.I2C(board.SCL, board.SDA, frequency=_WAKE_CLK_FREQ)

atecc = ATECC(i2c,address=int(arg.i2c_address,16),debug=True)

results = []

# print the public key
print("Public Key: ", atecc.gen_key(bytearray(64),slotId).hex())

def sign(loop):
    first = time.perf_counter()
    if arg.random:
        data = secrets.token_bytes(32)
    
    else:
        # with 32 bytes of 0x00
        data = b'\x00' * 32

    print("Data: ", data.hex())

    sig = atecc.ecdsa_sign(slotId,data)

    print("Signature: ", sig.hex())

    last = time.perf_counter()
    delta = (last - first )* 1000
    print(f"{loop+1}: {delta:.2f}ms")
    results.append(delta)

def run():
    for i in range(0, it):
        sign(i)
        time.sleep(0.001) 
    low =  min(results)
    high = max(results)
    average = sum(results) / len(results)
    avdelta = (high - low)
    print(f"Count: {it}\nLowest: {low:.2f}ms\nHighest: {high:.2f}ms\nAverage: {average:.2f}ms\nAverage Delta: {avdelta:.2f}ms")

if __name__ == "__main__":
    print("ATECC Serial: ", atecc.serial_number)
    run()
