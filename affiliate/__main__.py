from affiliate.worker import affiliate_handle


def main():
    pass


def auto_test():
    affiliate_handle.affiliate()


if __name__ == '__main__':
    test_mode = True

    if test_mode:
        auto_test()
    else:
        main()
