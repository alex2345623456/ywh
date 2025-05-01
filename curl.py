import subprocess
import argparse
import re
import concurrent.futures

def run_curl(curl_command, regex_pattern=None):
    try:
        result = subprocess.run(['bash', '-c', curl_command], text=True, capture_output=True)
        output_data = result.stdout
        if regex_pattern:
            output_data = filter_output_with_regex(output_data, regex_pattern)
        return output_data
    except Exception:
        return ""

def filter_output_with_regex(output_data, regex_pattern):
    try:
        matches = re.findall(regex_pattern, output_data, re.DOTALL)
        return '\n'.join(matches) if matches else ""
    except re.error:
        return ""

def process_multiple_commands(curl_command, output_file, regex_pattern=None, num_threads=1):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(run_curl, curl_command, regex_pattern) for _ in range(num_threads)]
        all_results = [future.result() for future in concurrent.futures.as_completed(futures)]

        with open(output_file, 'w') as output:
            for result in all_results:
                output.write(result + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-regex', '--regex')
    parser.add_argument('-t', '--threads', type=int, required=True)
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as file:
            curl_command = file.read().strip()

        if curl_command:
            process_multiple_commands(curl_command, args.output, args.regex, args.threads)
    except FileNotFoundError:
        return

if __name__ == "__main__":
    main()
