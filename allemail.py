import argparse

def process_emails(input_file, output_file, num_lines):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(output_file, 'w') as outfile:
        outfile.writelines(lines[:num_lines])

    with open(input_file, 'w') as infile:
        infile.writelines(lines[num_lines:])

    green = '\033[92m'
    reset = '\033[0m'
    if num_lines == 1:
        print(f"{green}Send 1 email from {input_file} to {output_file}{reset}")
    else:
        print(f"{green}Send {num_lines} emails from {input_file} to {output_file}{reset}")

def main():
    parser = argparse.ArgumentParser(description='Process email file')
    parser.add_argument('-t', type=int, required=True)
    args = parser.parse_args()

    input_file = 'allemail.txt'
    output_file = 'email.txt'
    num_lines = args.t

    process_emails(input_file, output_file, num_lines)

if __name__ == '__main__':
    main()
