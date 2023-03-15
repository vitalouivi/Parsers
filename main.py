import amre_supply_logoff as aslo
import amre_supply_login as asli
import reliable_parts_logoff as allroff
import time


def main():
    start1 = time.time()
    asli.amre_run()
    end1 = time.time()
    print("Time for scraping is ", end1 - start1)
    """
    # FOR AMRESUPPLY
    start1 = time.time()
    aslo.amre_run()
    end1 = time.time()
    print("Time for scraping is ", end1 - start1)
    
    th = Thread(target=aslo.amre_run(), args=())
    th.start()
    end1 = time.time()
    print("Time for scraping with thread is ", end1 - start1)

    start1 = time.time()
    aslo.amre_run()
    end1 = time.time()
    print("Time for scraping without thread is ", end1 - start1)
    
    start2 = time.time()
    asli.amre_run()
    end2 = time.time()
    print("Time for scraping is ", end2 - start2)

    # FOR RELIABLEPARTS
    start1 = time.time()
    aslo.amre_run()
    end1 = time.time()
    print("Time for scraping is ", end1 - start1)

    start2 = time.time()
    asli.amre_run()
    end2 = time.time()
    print("Time for scraping is ", end2 - start2)
    # FOR MARCONE

    starttime = time.time()
    endtime = starttime
    #aloff.amre_run()
    #allroff.reliable_run()
    alon.amre_run()
    endtime = time.time()
    print("Time for scraping is ", endtime - starttime)
    """


if __name__ == '__main__':
    main()
