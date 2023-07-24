import time
import board
import busio
import argparse

from adafruit_atecc.adafruit_atecc import ATECC, _WAKE_CLK_FREQ

parser = argparse.ArgumentParser(description='Description of your script.')
parser.add_argument('-i','--iterations', help='Number of iterations to run', required=False, default=100)
parser.add_argument('-s','--slot', help='slot to use', required=False, default='0')
parser.add_argument('-a','--i2c_address', help='i2c address to use', required=False, default='0x60')
arg = parser.parse_args()

slotId = int(arg.slot)
it = int(arg.iterations)
i2c = busio.I2C(board.SCL, board.SDA, frequency=_WAKE_CLK_FREQ)

atecc = ATECC(i2c,address=int(arg.i2c_address,16),debug=False)
data = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31\x32'
results = []

def sign(loop):
    first = time.perf_counter()

    sig = atecc.ecdsa_sign(slotId,data)

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

