#!/bin/bash

# Function to remove installed tools
remove_install() {
    echo "[INFO] Removing installed tools..."
    # Remove tgpt
    echo "[INFO] Removing tgpt from /usr/local/bin..."
    sudo rm -f /usr/local/bin/tgpt && echo "[SUCCESS] tgpt removed." || echo "[ERROR] Failed to remove tgpt."
    # Remove tg-archive
    echo "[INFO] Removing tg-archive from /usr/local/bin..."
    sudo rm -f /usr/local/bin/tg-archive && echo "[SUCCESS] tg-archive removed." || echo "[ERROR] Failed to remove tg-archive."
    # Remove Porch Pirate
    echo "[INFO] Removing Porch Pirate from /usr/local/bin..."
    sudo rm -f /usr/local/bin/porch-pirate && echo "[SUCCESS] Porch Pirate removed." || echo "[ERROR] Failed to remove Porch Pirate."
    # Remove palacepirate
    echo "[INFO] Removing palacepirate from /usr/local/bin..."
    sudo rm -f /usr/local/bin/palacepirate && echo "[SUCCESS] palacepirate removed." || echo "[ERROR] Failed to remove palacepirate."
    # Remove virtual environment
    echo "[INFO] Removing virtual environment..."
    rm -rf venv && echo "[SUCCESS] Virtual environment removed." || echo "[ERROR] Failed to remove virtual environment."
    echo "[INFO] Tools removed."
}

# Show usage function
show_usage() {
    echo "Usage: $0 [install|remove|reinstall]"
    exit 1
}

# Parse command line options
if [[ -z "$1" ]]; then
    show_usage
fi

case "$1" in
    install)
        echo "[INFO] Starting installation of tools..."
        ;;
    remove)
        remove_install
        exit 0
        ;;
    reinstall)
        remove_install
        echo "[INFO] Reinstalling tools..."
        ;;
    *)
        show_usage
        ;;
esac

# Activate virtual environment if it exists, otherwise create it
if [ -d "venv" ]; then
    echo "[INFO] Activating existing virtual environment..."
    source venv/bin/activate && echo "[SUCCESS] Virtual environment activated." || echo "[ERROR] Failed to activate virtual environment."
else
    echo "[INFO] Creating a new virtual environment..."
    python3 -m venv venv && echo "[SUCCESS] Virtual environment created." || echo "[ERROR] Failed to create virtual environment."
    source venv/bin/activate && echo "[SUCCESS] Virtual environment activated." || echo "[ERROR] Failed to activate virtual environment."
fi

# Install tgpt
echo "[INFO] Installing tgpt..."
curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin && echo "[SUCCESS] tgpt installed." || echo "[ERROR] Failed to install tgpt."

# Clone and install tg-archive
echo "[INFO] Cloning tg-archive repository..."
git clone https://github.com/knadh/tg-archive.git && echo "[SUCCESS] tg-archive repository cloned." || echo "[ERROR] Failed to clone tg-archive repository."
cd tg-archive
make && echo "[SUCCESS] tg-archive built." || echo "[ERROR] Failed to build tg-archive."
sudo make install PREFIX=/usr/local && echo "[SUCCESS] tg-archive installed." || echo "[ERROR] Failed to install tg-archive."
cd ..
rm -rf tg-archive && echo "[INFO] Removed tg-archive repository."

sudo mv tg-archive/tg-archive /usr/local/bin && echo "[SUCCESS] tg-archive added to /usr/local/bin." || echo "[ERROR] Failed to add tg-archive to /usr/local/bin."

# Clone and install Porch Pirate using pip
echo "[INFO] Cloning Porch Pirate repository..."
git clone https://github.com/MandConsultingGroup/porch-pirate.git && echo "[SUCCESS] Porch Pirate repository cloned." || echo "[ERROR] Failed to clone Porch Pirate repository."
cd porch-pirate
pip install . && echo "[SUCCESS] Porch Pirate installed." || echo "[ERROR] Failed to install Porch Pirate."
PORCH_PIRATE_PATH=$(pwd)

# Install Python requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installing Python requirements from requirements.txt..."
    pip install -r requirements.txt && echo "[SUCCESS] Python requirements installed." || echo "[ERROR] Failed to install Python requirements."
fi

cd ..
rm -rf porch-pirate && echo "[INFO] Removed Porch Pirate repository."

# Copy palacepirate.py to /usr/local/bin and add to PATH
echo "[INFO] Copying palacepirate.py to /usr/local/bin..."
sudo cp palacepirate.py /usr/local/bin/palacepirate && echo "[SUCCESS] palacepirate copied to /usr/local/bin." || echo "[ERROR] Failed to copy palacepirate."

# Update PATH if not already in PATH
if [[ ":$PATH:" != *":/usr/local/bin:"* ]]; then
    export PATH=/usr/local/bin:$PATH && echo "[SUCCESS] PATH updated." || echo "[ERROR] Failed to update PATH."
fi
if [[ ":$PATH:" != *":$PORCH_PIRATE_PATH:"* ]]; then
    export PATH=$PORCH_PIRATE_PATH:$PATH && echo "[SUCCESS] PATH updated." || echo "[ERROR] Failed to update PATH."
fi

# Permanently update PATH in ~/.bashrc or ~/.zshrc if not already present
if ! grep -q "/usr/local/bin" ~/.bashrc; then
    echo "export PATH=/usr/local/bin:\$PATH" >> ~/.bashrc && echo "[SUCCESS] PATH permanently updated in ~/.bashrc." || echo "[ERROR] Failed to update PATH in ~/.bashrc."
fi
if ! grep -q "/usr/local/bin" ~/.zshrc; then
    echo "export PATH=/usr/local/bin:\$PATH" >> ~/.zshrc && echo "[SUCCESS] PATH permanently updated in ~/.zshrc." || echo "[ERROR] Failed to update PATH in ~/.zshrc."
fi

echo "[INFO] Don't forget to source your ~/.bashrc or ~/.zshrc to apply the changes:"
echo "source ~/.bashrc or source ~/.zshrc"
