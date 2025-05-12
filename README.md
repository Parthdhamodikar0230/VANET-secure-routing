VANET Secure Routing using NS-3

Project Overview

This project implements a secure routing protocol for Vehicular Ad hoc Networks (VANETs) using the NS-3 network simulator. The goal is to ensure secure communication between vehicles and infrastructure, addressing common security threats in VANETs, such as eavesdropping and data manipulation. The project employs cryptographic techniques, including digital signatures and public key infrastructure, for data integrity, confidentiality, and authentication.

Features

Secure Routing Protocol: Implements secure routing in VANETs using cryptographic techniques.

NS-3 Simulation: Uses the NS-3 simulator to model vehicle mobility, communication, and network behavior.

Performance Evaluation: Analyzes performance metrics like throughput, delay, packet loss, and security effectiveness.

Security Measures: Focuses on protecting data from various network-based attacks.


Requirements

To run this project, you need the following:

NS-3: Version 3.x (Installation instructions can be found on the NS-3 website)

Linux/Unix system (Recommended)


Installation

1. Clone the repository to your local machine:

git clone https://github.com/yourusername/VANET-Secure-Routing-NS3.git


2. Navigate to the project directory:

cd VANET-Secure-Routing-NS3


3. Install NS-3 following the instructions on the official NS-3 installation guide.


4. Build the project:

./waf configure
./waf build



Usage

1. After building the project, you can run the simulation script:

./waf --run <your-simulation-script>


2. Modify the simulation parameters (such as vehicle density, routing protocol, etc.) within the script as needed.


3. After the simulation completes, you can analyze the output in the results directory.



Contribution

Feel free to fork this repository and submit pull requests for any improvements or fixes. All contributions are welcome!
