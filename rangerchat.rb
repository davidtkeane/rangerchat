class Rangerchat < Formula
  desc "A command-line tool to interact with OpenAI's GPT-4 model"
  homepage "https://github.com/davidtkeane/rangerchat"
  url "https://github.com/davidtkeane/rangerchat/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "8f3a1994a39e75f1628c6795e610b144994d17821b1a4cfc55caffffcaa747a5"
  license "MIT"

  depends_on "python@3.10"  # You can adjust this based on the Python version you want

  def install
    # Welcome message
    ohai "Welcome to RangerChat! 💀 Installing the tool now..."

    # Check if Python is installed
    python_installed = system "python3", "--version"
    if python_installed
      system "python3", "--version"
    else
      # Install Python if not found
      ohai "Python is not installed. Installing Python..."
      system "brew", "install", "python@3.10"
    end

    # Display the Python version after installation
    system "python3", "--version"

    # Run the setup.py script
    system "python3", "setup.py", "install"

    # Install the script and set up the rgpt command
    bin.install "rgpt.py" => "rgpt"

    # Exit message
    ohai "RangerChat has been successfully installed! 🎉 You can now use 'rgpt' from the command line."
  end

  test do
    # Test the formula by checking if the help command works
    system "#{bin}/rgpt", "--help"
  end
end
