import transmitter
import quadcopter
import time


def main():
    drone = quadcopter.Quadcopter()
    # drone.calibrate_esc()

    t = transmitter.Transmitter(drone)

    try:
        t.start()
        time.sleep(60)
        print('Time is up, cleaning up...')
    except KeyboardInterrupt:
        print('Keyboard Interrupt, cleaning up...')
    finally:
        t.close()
        drone.turn_off_esc()

    print('Finished')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

