def setup_proxy(chrome_options, proxy_addr):
    chrome_options.add_argument(f'--proxy-server={proxy_addr}')
    chrome_options.add_argument(f'--ignore-certificate-errors')
    return chrome_options
