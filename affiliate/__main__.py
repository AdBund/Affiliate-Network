import traceback
import logging
import time
import schedule
from affiliate.worker import yeahmobi
from affiliate.worker import avazu


def job():
    start = time.time()
    print("start: job time: " + str(start))
    listTS = [avazu, yeahmobi]

    for ts in listTS:
        try:
            print('start -->' + str(ts))
            ts()
        except Exception as e:
            print(str(ts) + ' is error ,and error : ' + str(e) + " continue next TS !")
            logging.error(traceback.format_exc())
            continue

    end = time.time()

    print("use time :" + str(end - start))


def main():
    print("start job")

    schedule.every(12).hours.do(job).run()  # run: Run the job and immediately reschedule it.

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
