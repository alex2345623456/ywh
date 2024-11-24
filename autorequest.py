import argparse
import subprocess
import concurrent.futures
import time

# Fungsi untuk menjalankan command dan mengumpulkan hasil statistik
def run_command(header_file, request_file, target_url, repeat_count):
    command = [
        'python3', 'request.py', 
        '-H', header_file, 
        '-r', request_file, 
        '-target', target_url, 
        '-x', str(repeat_count)
    ]
    
    start_time = time.time()
    try:
        # Menjalankan command dan menangkap output
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        end_time = time.time()
        
        # Mengambil hasil output
        output = result.stdout
        elapsed_time = end_time - start_time
        
        # Mengumpulkan statistik dari output
        stats = parse_output(output, elapsed_time)
        
        return stats
    
    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan command: {e}")
        return None

# Fungsi untuk parsing output dari setiap command
def parse_output(output, elapsed_time):
    stats = {
        'total_requests': 0,
        'status_codes': {},
    }
    
    # Mem-parsing hasil output untuk mendapatkan statistik yang dibutuhkan
    lines = output.splitlines()
    for line in lines:
        if line.startswith("Total requests sent:"):
            stats['total_requests'] = int(line.split(":")[1].strip())
        elif "Status code" in line:
            parts = line.split(":")
            code = parts[0].split()[-1].strip()
            count = int(parts[1].split()[0].strip())
            stats['status_codes'][code] = count
    
    return stats

# Fungsi utama
def main():
    parser = argparse.ArgumentParser(description='Autorequest script for running a command.')
    parser.add_argument('-H', '--header', required=True, help='File header (text1.txt)')
    parser.add_argument('-r', '--request', required=True, help='File request (text2.txt)')
    parser.add_argument('-target', '--target_url', required=True, help='Target URL')
    parser.add_argument('-x', '--repeat', type=int, required=True, help='Repeat count (e.g., 6)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of parallel executions (default is 1)')
    
    # Mengambil argumen yang diberikan pengguna
    args = parser.parse_args()

    # Variabel untuk mengumpulkan statistik dari semua thread
    final_stats = {
        'total_requests': 0,
        'status_codes': {},
    }

    # Menggunakan ThreadPoolExecutor untuk menjalankan command secara paralel
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for _ in range(args.threads):
            futures.append(executor.submit(run_command, args.header, args.request, args.target_url, args.repeat))
        
        # Mengumpulkan hasil dari semua thread
        for future in concurrent.futures.as_completed(futures):
            stats = future.result()
            if stats:
                # Menambahkan hasil statistik dari thread ini ke statistik final
                final_stats['total_requests'] += stats['total_requests']
                
                for code, count in stats['status_codes'].items():
                    if code in final_stats['status_codes']:
                        final_stats['status_codes'][code] += count
                    else:
                        final_stats['status_codes'][code] = count
    
    # Mencetak ringkasan akhir tanpa waktu total
    print("Final Summary:")
    print(f"Total requests sent: {final_stats['total_requests']}")
    
    for code, count in final_stats['status_codes'].items():
        print(f"Status code {code}: {count} times")

if __name__ == '__main__':
    main()
