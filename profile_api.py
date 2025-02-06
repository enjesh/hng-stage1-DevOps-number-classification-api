import cProfile
import pstats
import requests  # Use requests library directly

def profile_api_request(url):
    """Profiles a request to the given URL."""
    try:
        with cProfile.Profile() as pr:
            response = requests.get(url)  # Make the request
            response.raise_for_status() # Check for HTTP errors
            # You can optionally process the response here if needed.
            # For profiling, the request itself is the target
            # print(response.json()) # Example if you want to see the JSON

        pr.dump_stats("classify_number.prof")  # Save profiling data

        stats = pstats.Stats("classify_number.prof")
        stats.sort_stats("time")
        stats.print_stats()  # Print results to console

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    url = "http://127.0.0.1:8080/api/classify-number?number=6"  # Your API endpoint
    profile_api_request(url)
    