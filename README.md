# AWSFinder

AWSFinder is a script that helps you locate AWS EC2 instances based on various parameters like IP address, instance ID, or instance name. It reads AWS credentials from the standard AWS credentials file and searches across all regions and accounts specified in the file.

## Prerequisites

- Python 3.x
- Boto3
- AWS credentials configured in `~/.aws/credentials` (Linux/macOS) or `C:\Users\<YourUsername>\.aws\credentials` (Windows)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/jandress/awsfinder.git
   cd awsfinder
   ```

2. Install the required Python packages:
   ```sh
   pip install boto3
   ```

## Usage

To run the script, use the following command syntax:

```sh
python3 awsfinder.py [OPTIONS]
```

### Options:

- `-a`, `--address` : Internal or external IP address to search for
- `-i`, `--instance` : Instance ID to search for
- `-n`, `--name` : Instance name to search for

### Examples:

1. Search by instance name:
   ```sh
   python3 awsfinder.py -n linux_test
   ```

2. Search by instance ID:
   ```sh
   python3 awsfinder.py -i i-1234567890abcdef0
   ```

3. Search by IP address:
   ```sh
   python3 awsfinder.py -a 192.168.1.1
   ```

