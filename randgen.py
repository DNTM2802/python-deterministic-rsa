from prbg import PRBG
import argparse
import matplotlib.pyplot as plt
import time
import random
import string
import numpy as np
from PIL import Image
import sys

def main():
    '''
    This application implements the Pseudo-random Byte Generator (PRBG).
    It may do one of two things:
    - Perform benchmarking of the PRBG setup - uses random passwords, confusion strings and iteration
      counters to test the setup of the generator, and produces a number of different statistics to the
      statistics folder. For that, only the flag --benchmark is needed. It may take a long time.
    - Output NOB or infinite number of pseudo-random bytes to stdout - using the given password, confusion
      string and iteration count. For that, the flags --pwd, --cs, --ic, and --nob are needed. It NOB < 1,
      the program will output an infine number of bytes.
    '''

    # Argument parser
    parser = argparse.ArgumentParser(description='Deterministic RSA key generation (D-RSA): randgen')
    parser.add_argument('--pwd', required='--benchmark' not in sys.argv, type=str, help='password (textual)')
    parser.add_argument('--cs', required='--benchmark' not in sys.argv, type=str, help='confusion string (textual)')
    parser.add_argument('--ic', required='--benchmark' not in sys.argv, type=str, help='iteration count (number)')
    parser.add_argument('--nob', required='--benchmark' not in sys.argv, type=int, help='number of bytes to output (number)')
    parser.add_argument('--benchmark', action='store_true', help='Perform benchmarking with random parameters')
    args = parser.parse_args()

    # Generate random password
    password = get_random_string(10)
    prbg = None

    # Compute benchmarks
    if args.benchmark:
        
        # plot charts ilustrating the contribution of the two input parameters:
        # - confusion string and number of iterations
        # to the setup time of the pseudo-random number generator

        print("Task: Plot charts comparing the setup time for different cs and ic.")
        f = open(f"statistics/times-{time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())}.txt", "w")
        data_ic = [[],[],[],[],[],[],[]]
        for cs_size in range(3):
            data_cs = []
            for count, ic in enumerate([1, 5, 10, 20, 50, 100, 200]):

                # Generator init
                prbg = PRBG(password, get_random_string(cs_size+1), ic)
                print(f"  Setting gen up for cs_len={cs_size+1} and ic={ic}")

                # Count setup time
                start_time = time.time()
                prbg.setup()
                tot_time = time.time() - start_time

                # Save data for later plot
                data_cs.append([ic, tot_time])
                data_ic[count].append([cs_size+1, tot_time])

                # Write to times file
                f.write(f"cs_size={cs_size+1}\tic={ic}\ttime={tot_time}\n")
            
            # Plot Time per iteration
            fig, ax = plt.subplots( nrows=1, ncols=1 )
            ax.set_title(f"Time per iteration, for confusion string size={cs_size+1}")
            ax.set_ylabel("Time (seconds)")
            ax.set_xlabel("Iteration count")
            #ax.set_yscale('log')
            ax.scatter([tpl[0] for tpl in data_cs], [tpl[1] for tpl in data_cs])
            fig.savefig(f'statistics/t_per_ic_cs{cs_size+1}.png')
            plt.close(fig)
        
        f.write(f"\nFinished. {time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())}")
        f.close()

        # Plot Time per confusion string size
        for count, ic_data in enumerate([1, 5, 10, 20, 50, 100, 200]):
            fig, ax = plt.subplots( nrows=1, ncols=1 )
            ax.set_title(f"Time per confusion string size, for iteration count={ic_data}")
            ax.set_ylabel("Time (seconds)")
            ax.set_xlabel("Confusion string size")
            #ax.set_yscale('log')
            ax.scatter([tpl[0] for tpl in data_ic[count]], [tpl[1] for tpl in data_ic[count]])
            fig.savefig(f'statistics/t_per_cs_ic{ic_data}.png')
            plt.close(fig)
            
        # Statistical info
        print("Task: Plot statistical info - randomness and byte distribution")
        print(prbg)

        height = 1000
        width = 1000
        im = Image.new("RGB", (width,height))
        im = np.array(im)

        hist_dict = dict()
        buffer = []
        
        for i in range(width):
            for k in range (height):
                
                # Add 3 bytes to image buffer
                buffer.append(prbg.next_byte())
                buffer.append(prbg.next_byte())
                buffer.append(prbg.next_byte())

                # Add previous 3 bytes to the histogram
                for b in buffer:
                    if b in hist_dict:
                        hist_dict[b] += 1
                    else:
                        hist_dict[b] = 1

                im[i][k] = buffer
                buffer = []

        # Save randomness image
        print(f"  Saving randomness in statistics/hist_{width*height*3}_bytes.png...", end="")
        img = Image.fromarray(im, 'RGB')
        img.save(f"statistics/randomness_{width*height*3}.png")
        print("done.")

        # Save histogram
        print(f"  Saving byte histogram in statistics/randomness_{width*height*3}.png...", end="")
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        ax.set_title(f"Distribution of values of {width*height*3} bytes")
        ax.set_ylabel("Ammount")
        ax.set_xlabel("Byte value (0-255)")
        ax.bar([i for i in hist_dict],[hist_dict[i] for i in hist_dict])
        fig.savefig(f'statistics/hist_{width*height*3}_bytes.png')
        print("done.")
        plt.close(fig)

    # stdout bytes
    else:
        prbg = PRBG(args.pwd, args.cs, args.ic)
        prbg.setup()

        # Output given number of bytes
        if args.nob >= 1:
            for _ in range(args.nob):
                sys.stdout.buffer.write(prbg.next_byte().item().to_bytes(1,byteorder='big'))
        # Output bytes forever
        else:
            while True:
                sys.stdout.buffer.write(prbg.next_byte().item().to_bytes(1,byteorder='big'))

def get_random_string(length):
    '''
    Uses the Python random module to produce random alphabetic strings
    with the given length. Used for test purposes only.
    '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

if __name__ == "__main__":
    main()