import psutil
import time
import requests

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}"
        bytes /= 1024

def get_network_stats():
	io = psutil.net_io_counters()
	bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
	while True:
		time.sleep(UPDATE_DELAY)
    	# get the stats again
		io_2 = psutil.net_io_counters()
    	# new - old stats gets us the speed
		#ds - download speed
		us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
		download_speed = get_size(ds/UPDATE_DELAY)
		#print(f"Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
		# update the bytes_sent and bytes_recv for next iteration
		bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
		return float(download_speed)

def check_connection():
	try:
		response = requests.get("https://google.com", timeout=5)
		return True
	except requests.ConnectionError:
		return False    
