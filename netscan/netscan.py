#!/usr/bin/env python3

import argparse
import socket
import ipaddress
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import logging
import csv

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

PORT_MEANINGS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}

def scan_host(ip, ports=None, timeout=0.01):
    """Scan a given IP for a list of ports or a single port."""
    if ports is None:
        ports = [80]  # Default to port 80 if no ports are provided
    results = []
    for port in ports:
        try:
            logging.debug(f"Scanning IP {ip}, Port {port}")
            with socket.create_connection((str(ip), port), timeout=timeout):
                results.append((port, True))
        except (socket.timeout, ConnectionRefusedError, OSError):
            results.append((port, False))
    return results

def scan_network(network_cidr, ports=None, timeout=0.01):
    """Scan all hosts in a given CIDR network for a list of ports."""
    if ports is None:
        ports = [80]  # Default to port 80 if no ports are provided
    results = []
    net = ipaddress.ip_network(network_cidr, strict=False)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=net.num_addresses)
        for ip in net.hosts():
            logging.debug(f"Scanning IP {ip}")
            port_results = scan_host(ip, ports=ports, timeout=timeout)
            hostname = resolve_hostname(str(ip))
            results.append((str(ip), hostname, port_results))
            progress.update(task, advance=1)
    
    return results

def display_results(results, show_all=False):
    """Display scan results using a rich table."""
    table = Table(title="Scan Results")
    table.add_column("IP Address", style="bold")
    table.add_column("Hostname", style="cyan")
    table.add_column("Port", style="magenta")
    table.add_column("Service", style="yellow")
    table.add_column("Status", style="green")

    for ip, hostname, port_results in results:
        for port, status in port_results:
            if not show_all and not status:
                continue
            service = PORT_MEANINGS.get(port, "Unknown")
            table.add_row(ip, hostname, str(port), service, "🟢 Up" if status else "🔴 Down")

    console.print(table)

def resolve_hostname(ip):
    """Try to resolve the hostname of an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "-"

def main():
    parser = argparse.ArgumentParser(
        description="Simple network scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("network", help="CIDR network range to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--port", type=int, nargs="*", help="TCP port(s) to scan (e.g., -p 80 443)")
    parser.add_argument("--common-ports", action="store_true", help="Scan a list of common ports")
    parser.add_argument("-t", "--timeout", type=float, default=0.01, help="Connection timeout in seconds (default: 0.01)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode for detailed logs")
    parser.add_argument("--output-csv", type=str, help="Path to output results in CSV format")
    parser.add_argument("--show-all", action="store_true", help="Show all results, including closed ports")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled")
    else:
        logging.getLogger().setLevel(logging.WARNING)

    logging.debug(f"Arguments: {args}")

    # Validate network or hostname argument
    try:
        # Check if it's a valid IP network
        ipaddress.ip_network(args.network, strict=False)
    except ValueError:
        # If not, check if it's a valid hostname
        try:
            resolved_ip = socket.gethostbyname(args.network)
            console.print(f"[bold blue]Resolved hostname '{args.network}' to IP '{resolved_ip}'[/bold blue]")
            args.network = resolved_ip + '/32'  # Treat as a single-host network
        except socket.gaierror:
            console.print(f"[bold red]Error: Invalid network range or hostname '{args.network}'[/bold red]")
            exit(1)

    # Validate port argument
    if args.port:
        for port in args.port:
            if port < 1 or port > 65535:
                console.print(f"[bold red]Error: Invalid port number '{port}'. Port must be between 1 and 65535.[/bold red]")
                exit(1)

    # Validate timeout argument
    if args.timeout <= 0:
        console.print("[bold red]Error: Timeout must be a positive number.[/bold red]")
        exit(1)

    ports = COMMON_PORTS if args.common_ports else (args.port if args.port else [80])
    console.print(f"[bold blue]Scanning {args.network} on ports {ports} with timeout {args.timeout}s[/bold blue]")
    results = scan_network(args.network, ports=ports, timeout=args.timeout)
    display_results(results, show_all=args.show_all)

    if args.output_csv:
        with open(args.output_csv, mode="w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["IP Address", "Hostname", "Port", "Service", "Status"])
            for ip, hostname, port_results in results:
                for port, status in port_results:
                    service = PORT_MEANINGS.get(port, "Unknown")
                    csv_writer.writerow([ip, hostname, port, service, "Up" if status else "Down"])
        console.print(f"[bold green]Results written to {args.output_csv}[/bold green]")

if __name__ == "__main__":
    main()
