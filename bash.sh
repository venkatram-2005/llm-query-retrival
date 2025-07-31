#!/bin/bash
set -e

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"
export CARGO_HOME=/tmp/.cargo
export RUSTUP_HOME=/tmp/.rustup
rustup default stable

pip install --upgrade pip
pip install -r ../requirements.txt
