import datetime
import requests
from gps3 import gps3  # For GPS time retrieval
from ntplib import NTPClient  # For internet-based time retrieval

def get_time_from_gps():
    """
    Retrieve UTC time from a GPS device.
    Returns:
        datetime: Current UTC time from GPS.
    Raises:
        Exception: If GPS is not available or fails.
    """
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()

    try:
        gps_socket.connect()
        gps_socket.watch()
        for report in gps_socket:
            if report:
                data_stream.unpack(report)
                if 'time' in data_stream.TPV:
                    return datetime.datetime.fromisoformat(data_stream.TPV['time'].replace('Z', '+00:00'))
    except Exception as e:
        raise Exception("Failed to retrieve time from GPS") from e

def get_time_from_internet():
    """
    Retrieve UTC time from an NTP server.
    Returns:
        datetime: Current UTC time from the internet.
    Raises:
        Exception: If internet is not available or NTP fails.
    """
    ntp_client = NTPClient()
    try:
        response = ntp_client.request('pool.ntp.org', version=3)
        return datetime.datetime.utcfromtimestamp(response.tx_time)
    except Exception as e:
        raise Exception("Failed to retrieve time from the internet") from e

def get_time_from_local_clock():
    """
    Retrieve UTC time from the local system clock.
    Returns:
        datetime: Current UTC time from the local clock.
    """
    return datetime.datetime.now(datetime.timezone.utc)

def get_utc_time():
    """
    Retrieve UTC time using GPS, internet, or local clock as fallback.
    Returns:
        datetime: Current UTC time.
    """
    try:
        # Attempt to retrieve time from GPS
        return get_time_from_gps()
    except Exception:
        pass

    try:
        # Attempt to retrieve time from the internet
        return get_time_from_internet()
    except Exception:
        pass

    # Fallback to local clock
    return get_time_from_local_clock()

def get_gpt_time():
    """
    Calculates the current Global Pulse Time (GPT).
    GPT divides the UTC day (86,400 seconds) into 100,000 pulses.
    Returns:
        str: The current GPT time formatted as Pxxxxxx.
    """
    # Retrieve the current UTC time using the best available method
    now_utc = get_utc_time()

    # Calculate seconds elapsed since midnight UTC
    seconds_since_midnight = (
        now_utc.hour * 3600 + now_utc.minute * 60 + now_utc.second + now_utc.microsecond / 1_000_000
    )

    # Convert seconds to GPT pulses (0-99999)
    gpt_pulse = int((seconds_since_midnight / 86400) * 100000)

    # Format and return GPT time as Pxxxxxx
    return f"P{gpt_pulse:06d}"

# Example usage
if __name__ == "__main__":
    try:
        print(f"Current Global Pulse Time (GPT): {get_gpt_time()}")
    except Exception as e:
        print(f"Error: {e}")
