class Rangerchat < Formula
    desc "A command-line tool to interact with OpenAI's GPT-4 model"
    homepage "https://github.com/davidtkeane/homebrew-rangerchat.git"
    url "https://github.com/davidtkeane/rangerchat/archive/refs/tags/v0.1.0.tar.gz"
    sha256 "8bd0b9205f95e4bc1db3afe50779cd51b4a4a8ab45f8436ab0df1dc1c5d9ff26"
    license "MIT"
  
    depends_on "python@3.10"  # Or whatever Python version your project requires
  
    def install
      # Install Python dependencies
      system "pip3", "install", "-r", "requirements.txt"
  
      # Install the script
      bin.install "rgpt.py" => "rgpt"
    end
  
    test do
      # Test the formula (optional)
      system "#{bin}/rgpt", "--help"
    end
  end
  