import transmitter
import time


def main():
    t = transmitter.Transmitter()
    try:
        t.start()
        time.sleep(60)
        print('Time is up, cleaning up...')
    except KeyboardInterrupt:
        print('Keyboard Interrupt, cleaning up...')
    finally:
        t.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

