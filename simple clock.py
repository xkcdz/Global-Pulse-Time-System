from datetime import datetime, timezone

def get_gpt_time():
    """
    Calculates the current Global Pulse Time (GPT).
    GPT divides the UTC day (86,400 seconds) into 100,000 pulses.
    Returns the current GPT time formatted as Pxxxxxx.
    """
    # Get current time in UTC
    now = datetime.now(timezone.utc)

    # Calculate seconds elapsed since midnight UTC
    seconds_since_midnight = (
        now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1_000_000
    )

    # Convert seconds to GPT pulses (0-99999)
    gpt_pulse = int((seconds_since_midnight / 86400) * 100000)

    # Format and return GPT time as Pxxxxxx
    return f"P{gpt_pulse:06d}"

# Example usage
if __name__ == "__main__":
    print(f"Current Global Pulse Time (GPT): {get_gpt_time()}")
